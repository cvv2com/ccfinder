# CVV2.NET Card CVV information Extractor

Bu proje, farklı formatlarda bulunan kredi kartı numarası, son kullanma tarihi (exp) ve CVV bilgilerini tespit edip çıkartmak için geliştirilmiş iki ayrı araç içerir:

1. **cvv2net.py** - Metin tabanlı dosya tarayıcı
2. **ocr_card_extractor.py** - OCR tabanlı PDF kart bilgisi çıkartıcı

## Özellikler

### cvv2net.py
- Kredi kartı, exp ve CVV için gelişmiş ve esnek regex havuzu
- JSON, CSV, metin, e-posta ve PDF desteği
- Yan yana ve alt alta geçen verilerde context yakalama
- Alakasız (username, password, domain, host, vb.) alanları filtreleme
- Sonuçları ekrana ve isteğe bağlı olarak CSV dosyasına yazma

### ocr_card_extractor.py
- Tesseract OCR ile PDF'lerden **tam kart bilgisi** (PAN, SKT, CVV) çıkarma
- Görüntü işleme ile kabartmalı/yazılı rakamları okuma
- Yüksek çözünürlüklü (300 DPI) PDF işleme
- Otomatik regex ile kart sahibi, numara, SKT ve CVV tespit etme
- Sonuçları CSV formatında veritabanı aktarımına hazır şekilde kaydetme

## Kurulum

### 1. Python Kurulumu

Öncelikle [Python 3](https://www.python.org/downloads/) yüklü olmalı.

### 2. Sistem Gereksinimleri (OCR için)

OCR tabanlı çıkartıcı (`ocr_card_extractor.py`) kullanacaksanız, sisteminizde Tesseract OCR kurulu olmalıdır:

**Linux/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils  # PDF dönüşümü için
```

**MacOS:**
```bash
brew install tesseract
brew install poppler
```

**Windows:**
- [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) sayfasından indirip kurun
- Kurulum sonrası `ocr_card_extractor.py` dosyasında tesseract yolunu güncelleyin

### 3. Gerekli Python Paketleri

Tüm bağımlılıkları yüklemek için:

```bash
pip install -r requirements.txt
```

veya manuel olarak:

```bash
pip install PyPDF2 pdf2image pytesseract opencv-python pandas numpy
```

> **Not:** Standart Python kurulumu genellikle diğer gerekli modülleri (json, csv, re) içerir.

### 4. Script Dosyasını İndir

Scripti bilgisayarınıza indirin ya da repodan klonlayın:

```bash
git clone https://github.com/cvv2com/ccfinder.git
cd ccfinder
```

## Kullanım

### Metin Tabanlı Tarama (cvv2net.py)

Komut satırında scriptin bulunduğu dizine geçin:

```bash
cd "C:\klasor\yolunuz"        # Windows
cd /home/kullanici/klasor     # Linux/Mac
```

#### Temel Kullanım

Bir dosyada veya klasörde arama yapmak için:

```bash
python cvv2net.py
```

Program sizden taranacak yol ve thread sayısı gibi bilgileri isteyecektir.

### OCR Tabanlı PDF Tarama (ocr_card_extractor.py)

PDF dosyalarından görsel olarak kart bilgilerini çıkartmak için:

#### 1. PDF Klasörü Hazırlayın

```bash
mkdir pdf_kayitlar
# PDF dosyalarınızı bu klasöre koyun
```

#### 2. Scripti Çalıştırın

```bash
python ocr_card_extractor.py
```

Script otomatik olarak:
- `./pdf_kayitlar` klasöründeki tüm PDF dosyalarını tarar
- Her PDF'i 300 DPI çözünürlükte görsele dönüştürür
- Görüntü işleme ve OCR ile rakamları okur
- Kart sahibi, numara, SKT ve CVV bilgilerini ayıklar
- Sonuçları `musteri_kredi_kartlari_tam_liste.csv` dosyasına kaydeder

#### 3. Ayarları Özelleştirin

`ocr_card_extractor.py` dosyasını düzenleyerek:
- `PDF_KLASORU`: PDF'lerin bulunduğu klasör yolu
- `CIKTI_DOSYASI`: Çıktı CSV dosyasının adı
- `pytesseract.pytesseract.tesseract_cmd`: Windows için Tesseract yolu

### PDF ve E-posta Desteği

PDF dosyalarını taramak için `PyPDF2` paketinin yüklü olması gerekir.  
E-posta dosyaları için `.eml` ve `.mbox` desteği vardır.

## Sonuç Örnekleri

### cvv2net.py Çıktısı
```
Card: 4556123412341234, Exp: 0528, CVV: 123, Line: 42, Context: Card: 4556 1234 1234 1234 Exp: 05/28 CVV: 123
```

### ocr_card_extractor.py Çıktısı
```
Toplam 5 dosya taranacak...
İşleniyor: kart_001.pdf
  ---> Kart Bulundu: 4546********
İşleniyor: kart_002.pdf
  ---> Kart Bulundu: 5412********

Başarılı! Tüm veriler 'musteri_kredi_kartlari_tam_liste.csv' dosyasına kaydedildi.
```

CSV Dosyası Format:
```csv
Kart_Sahibi,Kart_Numarasi,SKT,CVV,Dosya_Kaynagi
"JOHN DOE","4546571054123456","04/25","123","kart_001.pdf"
"JANE SMITH","5412345678901234","12/26","456","kart_002.pdf"
```

## Negatif Anahtar Kelime Filtresi (cvv2net.py)

Aşağıdaki anahtar kelimeler içeren satırlar/alanlar **kart/exp/cvv aramasında dikkate alınmaz**:
- user, username, domain, password, pass, host, server, login, smtp, imap, ftp, ssh, dns

## OCR Çalışma Mantığı (ocr_card_extractor.py)

1. **Yüksek Çözünürlük**: PDF'ler 300 DPI ile görsele dönüştürülür (küçük CVV kodlarını okumak için kritik)
2. **Görüntü İşleme**: Adaptive threshold ile kabartmalı yazıları netleştirir
3. **PAN Yakalama**: 13-19 haneli kart numaralarını (boşluklu veya bitişik) yakalar
4. **CVV Ayrıştırma**: "CVV/CVC" etiketi arar, bulamazsa izole 3-4 haneli sayıları alır
5. **Regex Desenleri**: MM/YY formatında son kullanma tarihi ve büyük harfli isim desenleri

## Güvenlik Uyarısı

⚠️ **ÖNEMLİ:** Bu araçlar tarafından oluşturulan CSV dosyaları **PCI-DSS standartlarına göre hassas veri** içerir:

- Tam PAN (Primary Account Number)
- Son kullanma tarihi (Expiration Date)  
- CVV/CVC güvenlik kodu

**Güvenlik Önerileri:**
- CSV dosyalarını veritabanına aktardıktan sonra diskten **geri getirilemeyecek şekilde silin** (`shred` komutu veya secure delete araçları)
- Kaynak PDF'leri de aynı şekilde güvenli olarak silin
- Veritabanında kartı saklamak yerine tokenization kullanın
- Erişimi sadece yetkili personelle sınırlandırın
- Tüm işlemleri denetim kaydı (audit log) tutarak yapın

## Hata ve Destek

- Script hem Windows hem Linux hem de MacOS ortamında çalışır.
- Hata alırsanız veya yeni format/özellik ekletmek isterseniz veya bana ulaşabilirsiniz.
https://bhf.pro/threads/629649/
https://www.cvv2.net
## Lisans

MIT Lisansı (veya kendi seçtiğiniz bir açık kaynak lisansı).
