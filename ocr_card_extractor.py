import os
import re
import csv
import cv2
import pytesseract
import pandas as pd
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import shutil
from datetime import datetime
import mimetypes

# --- AYARLAR / SETTINGS ---
# Windows kullanıyorsanız Tesseract yolunu buraya ekleyin
# For Windows users, add Tesseract path here (örnek: r'C:\Program Files\Tesseract-OCR\tesseract.exe')
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

KAYNAK_KLASORU = "./kart_kayitlari"  # PDF ve görsel dosyalarının bulunduğu klasör / Source folder for PDFs and images
CIKTI_DOSYASI = "musteri_kredi_kartlari_tam_liste.csv"  # Çıktı CSV dosyası / Output CSV file
ORGANIZE_KLASORU = "./organize_kartlar"  # Organize edilmiş dosyalar için klasör / Folder for organized files

# Desteklenen görsel formatları / Supported image formats
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
PDF_EXTENSION = '.pdf'

def preprocess_image_for_card(image):
    """
    Kart üzerindeki rakamları netleştirmek için görüntü işleme.
    Gürültüyü azaltır, kontrastı artırır.
    
    Image preprocessing to enhance card numbers.
    Reduces noise and increases contrast for better OCR accuracy.
    """
    img = np.array(image)
    
    # Griye çevir / Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Hafif blur (kirliliği azaltmak için) / Light blur to reduce noise
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Adaptive Threshold (Kart üzerindeki kabartma yazıları yakalamak için en iyisi)
    # Adaptive threshold works best for embossed text on cards
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    
    return thresh

def extract_full_cc_details(text):
    """
    Metin içinden 13-19 haneli kart no, tarih ve CVV ayıklar.
    
    Extracts 13-19 digit card numbers, expiration date, and CVV from text.
    Supports multiple formats and languages (Turkish, English, Spanish).
    """
    data = {
        "Kart_Sahibi": None,
        "Kart_Numarasi": None,
        "SKT": None,
        "CVV": None
    }

    # 1. TAM KREDİ KARTI NUMARASI (13-19 hane, boşluklu veya tireli)
    # Full credit card number (13-19 digits, with spaces or hyphens)
    # Örn / Example: 4546 5710 5412 3456
    pan_pattern = r'\b\d[\d \t-]{11,25}\d\b'
    pan_matches = re.findall(pan_pattern, text)
    
    for match in pan_matches:
        # Sadece rakamları al / Extract only digits
        clean_num = re.sub(r'\D', '', match)
        # Luhn algoritması veya basit uzunluk kontrolü (Genelde 16 hane)
        # Luhn algorithm or simple length check (typically 16 digits)
        if 13 <= len(clean_num) <= 19:
            data["Kart_Numarasi"] = clean_num
            break # İlk geçerli numarayı al / Get first valid number

    # 2. SON KULLANMA TARİHİ (MM/YY veya MM/YYYY)
    # Expiration date (MM/YY or MM/YYYY format)
    # Örn / Example: 04/25, 12/2026
    exp_pattern = r'\b(0[1-9]|1[0-2])\s?/\s?([2-9]\d{1,3})\b'
    exp_match = re.search(exp_pattern, text)
    if exp_match:
        data["SKT"] = f"{exp_match.group(1)}/{exp_match.group(2)}"

    # 3. CVV / CVC (3 veya 4 haneli güvenlik kodu)
    # CVV / CVC (3 or 4 digit security code)
    # Genelde "CVV", "CVC" etiketinden sonra gelir veya kısa izole bir sayıdır
    # Usually comes after "CVV", "CVC" label or as a short isolated number
    cvv_pattern = r'(?:CVV|CVC|Code|Kod)[:\.\s]*(\d{3,4})\b'
    cvv_match = re.search(cvv_pattern, text, re.IGNORECASE)
    
    if cvv_match:
        data["CVV"] = cvv_match.group(1)
    else:
        # Etiketsiz duran 3-4 haneli sayıları ara (Riskli olabilir, tarihle karışabilir)
        # Search for unlabeled 3-4 digit numbers (risky, might confuse with dates)
        # Bu kısım genellikle arka yüz taramalarında işe yarar
        # This part is useful for back-side scans
        potential_cvvs = re.findall(r'\b\d{3,4}\b', text)
        for val in potential_cvvs:
            # Tarih parçası veya kart numarasının parçası değilse al
            # Take if not part of date or card number
            if data["Kart_Numarasi"] is None or val not in data["Kart_Numarasi"]:
                data["CVV"] = val
                break

    # 4. KART SAHİBİ İSMİ
    # Cardholder name
    # Genellikle büyük harflerle yazılır, min 2 kelime
    # Usually written in uppercase, minimum 2 words
    name_match = re.search(r'(?:NOMBRE|NAME|TITULAR|MEMBER SINCE)\s*[:.]?\s*([A-Z][A-Z\s]{4,}?)(?:\n|$)', text, re.IGNORECASE | re.MULTILINE)
    if name_match:
        data["Kart_Sahibi"] = name_match.group(1).strip()
    
    return data

def detect_file_type(filepath):
    """
    Dosya içeriğine bakarak gerçek dosya tipini tespit eder.
    Detects actual file type by examining file content (magic bytes).
    
    Uzantı yanlış veya eksik olsa bile içeriğe göre tespit yapar.
    Detects even if extension is wrong or missing.
    
    Args:
        filepath: Dosya yolu / File path
    
    Returns:
        'pdf', 'image', 'unknown' veya None
    """
    try:
        # İlk birkaç byte'ı oku / Read first few bytes
        with open(filepath, 'rb') as f:
            header = f.read(16)
        
        if not header:
            return None
        
        # PDF kontrolü / PDF check
        if header.startswith(b'%PDF'):
            return 'pdf'
        
        # JPEG kontrolü / JPEG check
        if header.startswith(b'\xff\xd8\xff'):
            return 'image'
        
        # PNG kontrolü / PNG check
        if header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'image'
        
        # GIF kontrolü / GIF check
        if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'image'
        
        # BMP kontrolü / BMP check
        if header.startswith(b'BM'):
            return 'image'
        
        # TIFF kontrolü (Little Endian) / TIFF check (Little Endian)
        if header.startswith(b'II\x2a\x00'):
            return 'image'
        
        # TIFF kontrolü (Big Endian) / TIFF check (Big Endian)
        if header.startswith(b'MM\x00\x2a'):
            return 'image'
        
        # WebP kontrolü / WebP check
        if header.startswith(b'RIFF') and header[8:12] == b'WEBP':
            return 'image'
        
        # PIL ile açmayı dene / Try opening with PIL
        try:
            with Image.open(filepath) as img:
                img.verify()
                return 'image'
        except:
            pass
        
        return 'unknown'
        
    except Exception as e:
        return None

def is_potential_image_or_pdf(filepath):
    """
    Dosyanın görsel veya PDF olup olmadığını kontrol eder.
    Checks if file is an image or PDF.
    
    Hem uzantıya hem de içeriğe bakar / Checks both extension and content.
    
    Args:
        filepath: Dosya yolu / File path
    
    Returns:
        (is_valid, file_type, detected_by) tuple
    """
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    
    # Önce uzantıya bak / First check extension
    if ext in IMAGE_EXTENSIONS:
        return (True, 'image', 'extension')
    elif ext == PDF_EXTENSION:
        return (True, 'pdf', 'extension')
    
    # Uzantı bulunamadı veya bilinmiyor, içeriğe bak
    # Extension not found or unknown, check content
    detected_type = detect_file_type(filepath)
    
    if detected_type == 'pdf':
        return (True, 'pdf', 'content')
    elif detected_type == 'image':
        return (True, 'image', 'content')
    elif detected_type == 'unknown':
        # Bilinmeyen ama potansiyel görsel olabilir
        # Unknown but potentially could be an image
        # Uzantısız veya garip uzantılı dosyalar için PIL ile deneme yap
        # Try with PIL for files without extension or weird extensions
        return (False, 'unknown', 'unknown')
    else:
        return (False, None, None)

def process_image_file(filepath):
    """
    Görsel dosyasından OCR ile metin çıkartır.
    Processes image file with OCR to extract text.
    
    Args:
        filepath: Görsel dosyasının yolu / Path to image file
    
    Returns:
        OCR ile çıkartılan metin / Extracted text from OCR
    """
    try:
        # Görseli yükle / Load image
        img = Image.open(filepath)
        
        # Görüntü işleme / Image preprocessing
        processed = preprocess_image_for_card(img)
        
        # OCR ile metin çıkart / Extract text with OCR
        text = pytesseract.image_to_string(processed, lang='eng', config='--psm 6')
        return text
    except Exception as e:
        print(f"  Görsel işleme hatası / Image processing error: {e}")
        return ""

def process_pdf_file(filepath):
    """
    PDF dosyasından OCR ile metin çıkartır.
    Processes PDF file with OCR to extract text.
    
    Args:
        filepath: PDF dosyasının yolu / Path to PDF file
    
    Returns:
        OCR ile çıkartılan metin / Extracted text from OCR
    """
    try:
        # PDF'i yüksek çözünürlüklü görsele çevir (OCR kalitesi için 300+ DPI şart)
        # Convert PDF to high-resolution image (300+ DPI required for OCR quality)
        images = convert_from_path(filepath, dpi=300)
        
        full_text = ""
        for img in images:
            processed = preprocess_image_for_card(img)
            # Rakamları okumak için --psm 6 (blok metin) veya --psm 11 (sparse text) modu
            # Use --psm 6 (block text) or --psm 11 (sparse text) mode for reading numbers
            text = pytesseract.image_to_string(processed, lang='eng', config='--psm 6')
            full_text += text + "\n"
        
        return full_text
    except Exception as e:
        print(f"  PDF işleme hatası / PDF processing error: {e}")
        return ""

def organize_file(filepath, card_info, organize_folder):
    """
    Dosyayı kart bilgilerine göre organize eder.
    Organizes file based on card information (AI tagging feature).
    
    Args:
        filepath: Kaynak dosya yolu / Source file path
        card_info: Kart bilgileri / Card information
        organize_folder: Hedef klasör / Target folder
    """
    try:
        # Organize klasörünü oluştur / Create organize folder
        if not os.path.exists(organize_folder):
            os.makedirs(organize_folder)
        
        # Kart sahibine göre alt klasör oluştur / Create subfolder by cardholder
        if card_info.get('Kart_Sahibi'):
            cardholder_folder = os.path.join(organize_folder, 
                                            card_info['Kart_Sahibi'].replace(' ', '_'))
        elif card_info.get('Kart_Numarasi'):
            # İsim yoksa kart numarasının ilk 6 ve son 4 hanesine göre
            # If no name, use first 6 and last 4 digits of card number
            card_num = card_info['Kart_Numarasi']
            cardholder_folder = os.path.join(organize_folder, 
                                            f"Card_{card_num[:6]}_{card_num[-4:]}")
        else:
            cardholder_folder = os.path.join(organize_folder, "Unknown")
        
        if not os.path.exists(cardholder_folder):
            os.makedirs(cardholder_folder)
        
        # Dosyayı kopyala / Copy file
        filename = os.path.basename(filepath)
        dest_path = os.path.join(cardholder_folder, filename)
        
        # Aynı isimde dosya varsa timestamp ekle / Add timestamp if file exists
        if os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dest_path = os.path.join(cardholder_folder, f"{name}_{timestamp}{ext}")
        
        shutil.copy2(filepath, dest_path)
        print(f"  ---> Organize edildi / Organized: {cardholder_folder}")
        
    except Exception as e:
        print(f"  Organize hatası / Organization error: {e}")

def get_supported_files(folder):
    """
    Klasördeki ve alt klasörlerdeki desteklenen tüm dosyaları listeler.
    Lists all supported files in the folder and its subdirectories.
    
    Hem uzantıya hem de dosya içeriğine bakarak tespit eder.
    Detects by both extension and file content.
    
    Args:
        folder: Taranacak klasör / Folder to scan
    
    Returns:
        Dosya listesi ve tespit bilgileri / List of files with detection info
        [(relative_filepath, file_type, detected_by), ...]
    """
    files = []
    if not os.path.exists(folder):
        return files
    
    # Alt klasörleri de tara / Scan subdirectories as well
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            
            # Dosya tipini tespit et / Detect file type
            is_valid, file_type, detected_by = is_potential_image_or_pdf(filepath)
            
            if is_valid:
                # Relative path kullan / Use relative path for display
                relative_path = os.path.relpath(filepath, folder)
                files.append((relative_path, file_type, detected_by))
    
    return files

def main():
    """
    Ana program - PDF ve görsel dosyalarından kart bilgilerini çıkartır.
    Main program - Extracts card information from PDF and image files.
    
    Özellikler / Features:
    - PDF ve görsel dosyaları destekler / Supports PDF and image files
    - OCR ile tam kart bilgisi çıkartır / Extracts full card details with OCR
    - Dosyaları kart sahibine göre organize eder / Organizes files by cardholder
    - Sonuçları CSV formatında kaydeder / Saves results in CSV format
    """
    print("=" * 70)
    print("  KREDİ KARTI BİLGİ ÇIKARTICI / CREDIT CARD INFORMATION EXTRACTOR")
    print("  OCR + AI Organizasyon Sistemi / OCR + AI Organization System")
    print("=" * 70)
    
    if not os.path.exists(KAYNAK_KLASORU):
        print(f"\nHata / Error: '{KAYNAK_KLASORU}' klasörü bulunamadı / folder not found.")
        print(f"Lütfen bu klasörü oluşturun ve içine PDF/görsel dosyalarını koyun.")
        print(f"Please create this folder and put your PDF/image files in it.")
        return

    # Desteklenen dosyaları listele / List supported files
    files = get_supported_files(KAYNAK_KLASORU)
    
    if not files:
        print(f"\nHata / Error: '{KAYNAK_KLASORU}' klasöründe veya alt klasörlerinde desteklenen dosya bulunamadı.")
        print(f"No supported files found in '{KAYNAK_KLASORU}' folder or its subfolders.")
        print(f"\nDesteklenen formatlar / Supported formats:")
        print(f"  - PDF: {PDF_EXTENSION}")
        print(f"  - Görseller / Images: {', '.join(IMAGE_EXTENSIONS)}")
        print(f"\nNot: Alt klasörler de taranır / Note: Subfolders are also scanned")
        return
    
    # Dosya türlerini say / Count file types
    pdf_count = sum(1 for _, ftype, _ in files if ftype == 'pdf')
    image_count = sum(1 for _, ftype, _ in files if ftype == 'image')
    by_extension = sum(1 for _, _, detected in files if detected == 'extension')
    by_content = sum(1 for _, _, detected in files if detected == 'content')
    
    print(f"\nToplam {len(files)} dosya taranacak / Total files to scan:")
    print(f"  - PDF dosyaları / PDF files: {pdf_count}")
    print(f"  - Görsel dosyaları / Image files: {image_count}")
    print(f"\nTespit yöntemi / Detection method:")
    print(f"  - Uzantıya göre / By extension: {by_extension}")
    print(f"  - İçeriğe göre / By content: {by_content} 🔍")
    if by_content > 0:
        print(f"    ℹ️  {by_content} dosya yanlış/eksik uzantıya sahip ama içerik analizi ile tespit edildi")
        print(f"    ℹ️  {by_content} file(s) have wrong/missing extension but detected by content analysis")
    
    # Kullanıcı onayı / User confirmation
    print(f"\nDosyalar şu klasöre organize edilecek / Files will be organized to:")
    print(f"  {ORGANIZE_KLASORU}")
    user_input = input("\nDevam etmek istiyor musunuz? / Continue? (E/H or Y/N): ").strip().upper()
    if user_input not in ['E', 'Y', 'EVET', 'YES']:
        print("İşlem iptal edildi / Operation cancelled.")
        return
    
    all_data = []
    successful = 0
    failed = 0

    print(f"\n{'='*70}")
    print("Tarama başlıyor / Scanning started...")
    print(f"{'='*70}\n")

    for i, (relative_path, file_type, detected_by) in enumerate(files, 1):
        filepath = os.path.join(KAYNAK_KLASORU, relative_path)
        
        detection_info = f" [İçerik✓]" if detected_by == 'content' else ""
        print(f"[{i}/{len(files)}] İşleniyor / Processing: {relative_path}{detection_info}")
        
        try:
            # Dosya türüne göre işle / Process based on detected file type
            if file_type == 'pdf':
                full_text = process_pdf_file(filepath)
                file_type_label = 'PDF'
            elif file_type == 'image':
                full_text = process_image_file(filepath)
                file_type_label = 'Görsel/Image'
            else:
                continue

            # Veriyi Regex ile çek / Extract data with regex
            card_info = extract_full_cc_details(full_text)
            card_info['Dosya_Kaynagi'] = relative_path
            card_info['Dosya_Tipi'] = file_type_label
            card_info['Tarama_Zamani'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            card_info['Tespit_Yontemi'] = 'İçerik Analizi' if detected_by == 'content' else 'Uzantı'
            
            # Eğer kart numarası bulunduysa / If card number found
            if card_info['Kart_Numarasi']:
                all_data.append(card_info)
                # İlk 4 ve son 4 haneyi göster / Show first 4 and last 4 digits
                card_num = card_info['Kart_Numarasi']
                masked = f"{card_num[:4]}{'*'*8}{card_num[-4:]}" if len(card_num) >= 8 else card_num[:4] + "*"*8
                print(f"  ✓ Kart Bulundu / Card Found: {masked}")
                
                if card_info.get('Kart_Sahibi'):
                    print(f"  ✓ Kart Sahibi / Cardholder: {card_info['Kart_Sahibi']}")
                if card_info.get('SKT'):
                    print(f"  ✓ SKT / Exp: {card_info['SKT']}")
                if card_info.get('CVV'):
                    print(f"  ✓ CVV: ***")
                
                # Dosyayı organize et / Organize file
                organize_file(filepath, card_info, ORGANIZE_KLASORU)
                successful += 1
            else:
                print(f"  ✗ Kart numarası okunamadı / Card number not found")
                failed += 1

        except Exception as e:
            print(f"  ✗ Hata / Error: {e}")
            failed += 1

    # CSV olarak kaydet / Save as CSV
    if all_data:
        df = pd.DataFrame(all_data)
        # Kart numaralarının Excel'de bilimsel sayı (1.23E+15) gibi görünmemesi için string olarak sakla
        # Save card numbers as strings to prevent scientific notation in Excel
        if 'Kart_Numarasi' in df.columns:
            df['Kart_Numarasi'] = df['Kart_Numarasi'].astype(str)
        
        # Sütun sıralaması / Column order
        column_order = ['Dosya_Kaynagi', 'Dosya_Tipi', 'Tespit_Yontemi', 'Kart_Sahibi', 
                       'Kart_Numarasi', 'SKT', 'CVV', 'Tarama_Zamani']
        df = df[[col for col in column_order if col in df.columns]]
        
        df.to_csv(CIKTI_DOSYASI, index=False, sep=',', quotechar='"', quoting=csv.QUOTE_ALL)
        
        # Dosya izinlerini kısıtla / Restrict file permissions
        try:
            os.chmod(CIKTI_DOSYASI, 0o600)
        except (PermissionError, NotImplementedError, OSError):
            pass
        
        print(f"\n{'='*70}")
        print("ÖZET / SUMMARY")
        print(f"{'='*70}")
        print(f"✓ Başarılı / Successful: {successful}")
        print(f"✗ Başarısız / Failed: {failed}")
        print(f"\n✓ Tüm veriler kaydedildi / All data saved:")
        print(f"  CSV Dosyası / CSV File: {CIKTI_DOSYASI}")
        print(f"  Organize Klasör / Organized Folder: {ORGANIZE_KLASORU}")
        print(f"\n⚠️  GÜVENLİK UYARISI / SECURITY WARNING:")
        print(f"  Bu dosyalar PCI-DSS hassas veri içerir!")
        print(f"  These files contain PCI-DSS sensitive data!")
        print(f"  Kullanım sonrası güvenli silme yapın / Securely delete after use")
        print(f"{'='*70}")
    else:
        print(f"\n{'='*70}")
        print("Hiçbir dosyadan kart verisi çekilemedi.")
        print("No card data could be extracted from any file.")
        print(f"{'='*70}")

if __name__ == "__main__":
    main()
