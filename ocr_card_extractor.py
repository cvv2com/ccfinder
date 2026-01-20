import os
import re
import csv
import cv2
import pytesseract
import pandas as pd
import numpy as np
from pdf2image import convert_from_path

# --- AYARLAR ---
# Windows kullanıyorsanız Tesseract yolunu buraya ekleyin (örnek: r'C:\Program Files\Tesseract-OCR\tesseract.exe')
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

PDF_KLASORU = "./pdf_kayitlar"  # PDF'lerin olduğu klasör
CIKTI_DOSYASI = "musteri_kredi_kartlari_tam_liste.csv"

def preprocess_image_for_card(image):
    """
    Kart üzerindeki rakamları netleştirmek için görüntü işleme.
    Gürültüyü azaltır, kontrastı artırır.
    """
    img = np.array(image)
    
    # Griye çevir
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Hafif blur (kirliliği azaltmak için)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Adaptive Threshold (Kart üzerindeki kabartma yazıları yakalamak için en iyisi)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    
    return thresh

def extract_full_cc_details(text):
    """
    Metin içinden 13-19 haneli kart no, tarih ve CVV ayıklar.
    """
    data = {
        "Kart_Sahibi": None,
        "Kart_Numarasi": None,
        "SKT": None,
        "CVV": None
    }

    # 1. TAM KREDİ KARTI NUMARASI (13-19 hane, boşluklu veya tireli)
    # Örn: 4546 5710 5412 3456
    pan_pattern = r'\b\d[\d \t-]{11,25}\d\b'
    pan_matches = re.findall(pan_pattern, text)
    
    for match in pan_matches:
        # Sadece rakamları al
        clean_num = re.sub(r'\D', '', match)
        # Luhn algoritması veya basit uzunluk kontrolü (Genelde 16 hane)
        if 13 <= len(clean_num) <= 19:
            data["Kart_Numarasi"] = clean_num
            break # İlk geçerli numarayı al

    # 2. SON KULLANMA TARİHİ (MM/YY veya MM/YYYY)
    # Örn: 04/25, 12/2026
    exp_pattern = r'\b(0[1-9]|1[0-2])\s?/\s?([2-9]\d{1,3})\b'
    exp_match = re.search(exp_pattern, text)
    if exp_match:
        data["SKT"] = f"{exp_match.group(1)}/{exp_match.group(2)}"

    # 3. CVV / CVC (3 veya 4 haneli güvenlik kodu)
    # Genelde "CVV", "CVC" etiketinden sonra gelir veya kısa izole bir sayıdır.
    cvv_pattern = r'(?:CVV|CVC|Code|Kod)[:\.\s]*(\d{3,4})\b'
    cvv_match = re.search(cvv_pattern, text, re.IGNORECASE)
    
    if cvv_match:
        data["CVV"] = cvv_match.group(1)
    else:
        # Etiketsiz duran 3-4 haneli sayıları ara (Riskli olabilir, tarihle karışabilir)
        # Bu kısım genellikle arka yüz taramalarında işe yarar.
        potential_cvvs = re.findall(r'\b\d{3,4}\b', text)
        for val in potential_cvvs:
            # Tarih parçası veya kart numarasının parçası değilse al
            if data["Kart_Numarasi"] is None or val not in data["Kart_Numarasi"]:
                data["CVV"] = val
                break

    # 4. KART SAHİBİ İSMİ
    # Genellikle büyük harflerle yazılır, min 2 kelime.
    name_match = re.search(r'(?:NOMBRE|NAME|TITULAR|MEMBER SINCE)\s*[:.]?\s*([A-Z][A-Z\s]{4,}?)(?:\n|$)', text, re.IGNORECASE | re.MULTILINE)
    if name_match:
        data["Kart_Sahibi"] = name_match.group(1).strip()
    
    return data

def main():
    if not os.path.exists(PDF_KLASORU):
        print(f"Hata: '{PDF_KLASORU}' klasörü bulunamadı.")
        return

    files = [f for f in os.listdir(PDF_KLASORU) if f.lower().endswith('.pdf')]
    all_data = []

    print(f"Toplam {len(files)} dosya taranacak...")

    for filename in files:
        filepath = os.path.join(PDF_KLASORU, filename)
        print(f"İşleniyor: {filename}")
        
        try:
            # PDF'i yüksek çözünürlüklü görsele çevir (OCR kalitesi için 300+ DPI şart)
            images = convert_from_path(filepath, dpi=300)
            
            full_text = ""
            for img in images:
                processed = preprocess_image_for_card(img)
                # Rakamları okumak için --psm 6 (blok metin) veya --psm 11 (sparse text) modu
                text = pytesseract.image_to_string(processed, lang='eng', config='--psm 6')
                full_text += text + "\n"

            # Veriyi Regex ile çek
            card_info = extract_full_cc_details(full_text)
            card_info['Dosya_Kaynagi'] = filename
            
            # Eğer kart numarası bulunduysa listeye ekle
            if card_info['Kart_Numarasi']:
                all_data.append(card_info)
                print(f"  ---> Kart Bulundu: {card_info['Kart_Numarasi'][:4]}********")
            else:
                print("  ---> Kart numarası okunamadı.")

        except Exception as e:
            print(f"  Hata: {e}")

    # CSV olarak kaydet
    if all_data:
        df = pd.DataFrame(all_data)
        # Kart numaralarının Excel'de bilimsel sayı (1.23E+15) gibi görünmemesi için string olarak sakla
        df.to_csv(CIKTI_DOSYASI, index=False, sep=',', quotechar='"', quoting=csv.QUOTE_ALL) 
        print(f"\nBaşarılı! Tüm veriler '{CIKTI_DOSYASI}' dosyasına kaydedildi.")
    else:
        print("\nHiçbir dosyadan kart verisi çekilemedi.")

if __name__ == "__main__":
    main()
