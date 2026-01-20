# CVV2.NET Card CVV information Extractor

Bu proje, farklı formatlarda bulunan kredi kartı numarası, son kullanma tarihi (exp) ve CVV bilgilerini tespit edip çıkartmak için geliştirilmiş iki ayrı araç içerir:

1. **cvv2net.py** - Metin tabanlı dosya tarayıcı
2. **ocr_card_extractor.py** - OCR tabanlı PDF ve görsel kart bilgisi çıkartıcı + AI organizasyon sistemi

## Özellikler

### cvv2net.py
- Kredi kartı, exp ve CVV için gelişmiş ve esnek regex havuzu
- JSON, CSV, metin, e-posta ve PDF desteği
- Yan yana ve alt alta geçen verilerde context yakalama
- Alakasız (username, password, domain, host, vb.) alanları filtreleme
- Sonuçları ekrana ve isteğe bağlı olarak CSV dosyasına yazma

### ocr_card_extractor.py ⭐ YENİ ÖZELLİKLER v2.2
- ✅ **PDF ve Görsel Desteği**: PDF, JPG, PNG, BMP, TIFF formatlarını destekler
- ✅ **Alt Klasör Desteği** 🆕: Klasör içindeki tüm alt klasörleri otomatik tarar
- ✅ **Python 3.13+ Uyumlu** 🆕: Kaldırılan `imghdr` modülü gerektirmez
- ✅ **Akıllı Dosya Tespiti**: İçerik analiziyle yanlış/eksik uzantılı dosyaları tespit eder
- ✅ **Magic Byte Analizi**: Uzantıdan bağımsız format tespiti (PDF, JPEG, PNG, GIF, BMP, TIFF, WebP)
- ✅ **Tesseract OCR**: Tam kart bilgisi (PAN, SKT, CVV) çıkarma
- ✅ **Görüntü İşleme**: Kabartmalı/yazılı rakamları netleştirme (Gaussian blur, adaptive threshold)
- ✅ **AI Organizasyon**: Dosyaları kart sahibine göre otomatik organize etme (Nero AI Photo Tagger benzeri)
- ✅ **Çoklu Dil Desteği**: Türkçe, İngilizce, İspanyolca etiket tanıma
- ✅ **Zaman Damgası**: Her tarama için zaman kaydı
- ✅ **Güvenli Çıktı**: CSV dosyasına kısıtlı izinlerle kaydetme (chmod 600)
- ✅ **Detaylı Raporlama**: Başarı/başarısızlık istatistikleri + tespit yöntemi takibi

## Kurulum

### 🪟 Windows Kullanıcıları İçin Hızlı Başlangıç

**Windows için özel hazırlanan kolay kurulum ve kullanım:**

1. **Hızlı Kurulum**: `setup_windows.bat` dosyasına çift tıklayın
2. **Çalıştırma**: 
   - Metin tarayıcı için: `run_cvv2net.bat`
   - OCR çıkartıcı için: `run_ocr_extractor.bat`
3. **EXE Oluşturma**: `build_windows_exe.bat` (Python kurulu olmayan bilgisayarlar için)

📖 **Detaylı Windows Kılavuzu**: [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) dosyasına bakın

---

### 1. Python Kurulumu

Öncelikle [Python 3](https://www.python.org/downloads/) yüklü olmalı.

> **Not:** Python 3.13+ uyumlu - `imghdr` modülü gerektirmez.

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
- Kolay kurulum için `setup_windows.bat` dosyasını çalıştırın (otomatik kontrol yapar)
- Manuel kurulum: [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) sayfasından indirip kurun
- Kurulum sonrası `ocr_card_extractor.py` dosyasında tesseract yolunu güncelleyin
- Detaylı adımlar için [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) dosyasına bakın

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

### 🪟 Windows için Kolay Kullanım

**Windows kullanıcıları için üç farklı yöntem:**

#### Yöntem 1: Batch Dosyaları (Önerilen - En Kolay) ⭐

Proje klasöründe hazır batch dosyalarına çift tıklayın:

```
run_cvv2net.bat         - Metin tabanlı tarayıcı
run_ocr_extractor.bat   - OCR tabanlı çıkartıcı
```

Batch dosyaları otomatik olarak:
- Python'un kurulu olduğunu kontrol eder
- Gerekli paketleri yükler
- Programı çalıştırır

#### Yöntem 2: Windows EXE Dosyaları (Python Gerektirmez)

Python kurulu olmayan bilgisayarlarda kullanmak için:

```cmd
build_windows_exe.bat
```

Bu komut `dist/` klasöründe `.exe` dosyaları oluşturur:
- `cvv2net.exe`
- `ocr_card_extractor.exe`

Bu `.exe` dosyaları başka Windows bilgisayarlara kopyalanabilir ve Python kurulumu olmadan çalışır.

#### Yöntem 3: Manuel Python Çalıştırma

Komut satırında (CMD veya PowerShell):

```cmd
python cvv2net.py
```

📖 **Detaylı Windows kullanımı için**: [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)

---

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
# VEYA Windows için: run_cvv2net.bat
```

Program sizden taranacak yol ve thread sayısı gibi bilgileri isteyecektir.

### OCR Tabanlı PDF ve Görsel Tarama (ocr_card_extractor.py)

PDF ve görsel dosyalarından OCR ile kart bilgilerini çıkartmak için:

#### 1. Kaynak Klasörü Hazırlayın

```bash
mkdir kart_kayitlari
# PDF ve görsel dosyalarınızı bu klasöre veya alt klasörlerine koyun
```

**Desteklenen Formatlar:**
- PDF dosyaları (`.pdf`)
- Görsel dosyaları (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`)

**Örnek Klasör Yapısı (Alt klasörler desteklenir):**
```
kart_kayitlari/
├── dosya1.pdf
├── pdf/
│   ├── dosya2.pdf
│   └── dosya3.pdf
└── images/
    └── kart1.jpg
```

#### 2. Scripti Çalıştırın

```bash
python ocr_card_extractor.py
```

**Script otomatik olarak:**
- `./kart_kayitlari` klasöründeki ve **tüm alt klasörlerindeki** PDF ve görsel dosyalarını tarar
- PDF'leri 300 DPI çözünürlükte görsele dönüştürür
- Görüntü işleme ve OCR ile rakamları okur
- Kart sahibi, numara, SKT ve CVV bilgilerini ayıklar
- Sonuçları `musteri_kredi_kartlari_tam_liste.csv` dosyasına kaydeder
- **Dosyaları kart sahibine göre `./organize_kartlar` klasörüne organize eder** (AI tagging)

#### 3. Ayarları Özelleştirin

`ocr_card_extractor.py` dosyasını düzenleyerek:
- `KAYNAK_KLASORU`: PDF ve görsellerin bulunduğu klasör yolu
- `CIKTI_DOSYASI`: Çıktı CSV dosyasının adı
- `ORGANIZE_KLASORU`: Organize edilmiş dosyalar için klasör
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
