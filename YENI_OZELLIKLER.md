# Yeni Özellikler / New Features

## OCR Kart Çıkartıcı v2.0 - Yeni Özellikler

### 🎯 Ana Özellikler

#### 1. **Çoklu Format Desteği** 
Artık sadece PDF değil, tüm görsel formatları destekliyoruz:
- ✅ PDF dosyaları (`.pdf`)
- ✅ JPEG görseller (`.jpg`, `.jpeg`)
- ✅ PNG görseller (`.png`)
- ✅ BMP görseller (`.bmp`)
- ✅ TIFF görseller (`.tiff`, `.tif`)

**Örnek Kullanım:**
```bash
# Klasöre farklı formatlarda dosyalar koyun
kart_kayitlari/
  ├── kart_001.pdf
  ├── kart_002.jpg
  ├── kart_003.png
  └── kart_scan_004.tiff

# Scripti çalıştırın
python ocr_card_extractor.py
```

#### 2. **AI Organizasyon Sistemi** (Nero AI Photo Tagger benzeri)
Dosyalar otomatik olarak kart sahibine göre organize edilir:

**Organizasyon Yapısı:**
```
organize_kartlar/
  ├── JOHN_DOE/
  │   ├── kart_001.pdf
  │   └── kart_002.jpg
  ├── JANE_SMITH/
  │   ├── kart_003.png
  │   └── kart_004.pdf
  └── Card_454657_3456/  # İsim yoksa kart numarasına göre
      └── kart_005.jpg
```

**Özellikler:**
- Kart sahibi adına göre otomatik klasörleme
- İsim yoksa kart numarasının ilk 6 ve son 4 hanesine göre gruplama
- Aynı isimde dosya varsa timestamp ekleme
- Kaynak dosyalar korunur (güvenli kopyalama)

#### 3. **İnteraktif Kullanıcı Arayüzü**
```
======================================================================
  KREDİ KARTI BİLGİ ÇIKARTICI / CREDIT CARD INFORMATION EXTRACTOR
  OCR + AI Organizasyon Sistemi / OCR + AI Organization System
======================================================================

Toplam 12 dosya taranacak / Total files to scan:
  - PDF dosyaları / PDF files: 5
  - Görsel dosyaları / Image files: 7

Dosyalar şu klasöre organize edilecek / Files will be organized to:
  ./organize_kartlar

Devam etmek istiyor musunuz? / Continue? (E/H or Y/N): E

======================================================================
Tarama başlıyor / Scanning started...
======================================================================

[1/12] İşleniyor / Processing: kart_001.pdf
  ✓ Kart Bulundu / Card Found: 4546********3456
  ✓ Kart Sahibi / Cardholder: JOHN DOE
  ✓ SKT / Exp: 04/25
  ✓ CVV: ***
  ---> Organize edildi / Organized: ./organize_kartlar/JOHN_DOE

[2/12] İşleniyor / Processing: kart_002.jpg
  ✓ Kart Bulundu / Card Found: 5412********1234
  ✓ Kart Sahibi / Cardholder: JANE SMITH
  ✓ SKT / Exp: 12/26
  ✓ CVV: ***
  ---> Organize edildi / Organized: ./organize_kartlar/JANE_SMITH
```

#### 4. **Geliştirilmiş Çıktı Formatı**
CSV dosyası artık daha fazla bilgi içeriyor:

```csv
Dosya_Kaynagi,Dosya_Tipi,Kart_Sahibi,Kart_Numarasi,SKT,CVV,Tarama_Zamani
"kart_001.pdf","PDF","JOHN DOE","4546571054123456","04/25","123","2026-01-20 12:30:45"
"kart_002.jpg","Görsel/Image","JANE SMITH","5412345678901234","12/26","456","2026-01-20 12:30:47"
```

**Yeni Kolonlar:**
- `Dosya_Tipi`: PDF veya Görsel/Image
- `Tarama_Zamani`: İşlem zaman damgası

#### 5. **Güvenlik İyileştirmeleri**
- ✅ CSV dosyası otomatik olarak 600 izinleriyle oluşturulur (sadece sahip okuyabilir)
- ✅ İşlem öncesi kullanıcı onayı
- ✅ İşlem sonrası güvenlik uyarısı
- ✅ Detaylı başarı/başarısızlık raporlaması

#### 6. **Çift Dil Desteği**
Tüm çıktılar ve mesajlar hem Türkçe hem İngilizce:
- ✓ Bilgilendirme mesajları
- ✓ Hata mesajları
- ✓ Kod içi açıklamalar
- ✓ Dokümantasyon

### 📊 Karşılaştırma

| Özellik | Eski Versiyon | Yeni Versiyon v2.0 |
|---------|---------------|-------------------|
| PDF Desteği | ✅ | ✅ |
| Görsel Desteği | ❌ | ✅ (JPG, PNG, BMP, TIFF) |
| AI Organizasyon | ❌ | ✅ (Kart sahibine göre) |
| İnteraktif UI | ❌ | ✅ |
| Çift Dil | ❌ | ✅ (TR/EN) |
| Zaman Damgası | ❌ | ✅ |
| Güvenlik Onayı | ❌ | ✅ |
| Detaylı Raporlama | Temel | ✅ Gelişmiş |

### 🚀 Hızlı Başlangıç

```bash
# 1. Klasör oluştur
mkdir kart_kayitlari

# 2. Dosyalarını ekle (PDF, JPG, PNG, vb.)
cp /yol/karti/*.{pdf,jpg,png} kart_kayitlari/

# 3. Çalıştır
python ocr_card_extractor.py

# 4. Sonuçları kontrol et
ls organize_kartlar/  # Organize edilmiş dosyalar
cat musteri_kredi_kartlari_tam_liste.csv  # Çıkartılan veriler
```

### 💡 Kullanım Senaryoları

**Senaryo 1: Karışık Format Toplu İşlem**
```
Durumu: 50 PDF + 30 JPG görsel var
Çözüm: Tümünü kart_kayitlari/ klasörüne koy, tek seferde işle
Sonuç: Otomatik organize, tek CSV dosyası
```

**Senaryo 2: AI Tabanlı Arşivleme**
```
Durumu: Yüzlerce kart görseli, manuel organize edilmesi gerek
Çözüm: Script çalıştır, kart sahiplerine göre otomatik klasörleme
Sonuç: organize_kartlar/ içinde düzenli yapı
```

**Senaryo 3: Çoklu Dil Kartlar**
```
Durumu: İngilizce, Türkçe, İspanyolca kartlar
Çözüm: Script tüm dilleri destekler
Sonuç: Tüm kartlardan başarılı çıkarım
```

### 🔧 Yapılandırma

Script başındaki ayarları düzenleyin:

```python
KAYNAK_KLASORU = "./kart_kayitlari"  # Kaynak klasör
CIKTI_DOSYASI = "musteri_kredi_kartlari_tam_liste.csv"  # CSV dosyası
ORGANIZE_KLASORU = "./organize_kartlar"  # Organize klasörü
```

### ⚠️ Önemli Notlar

1. **Tesseract Gereksinimi**: Tesseract OCR yüklü olmalı
2. **Yüksek Çözünürlük**: PDF'ler 300 DPI ile işlenir (daha yavaş ama daha doğru)
3. **Disk Alanı**: Organize klasörü kaynak dosyaların kopyasını tutar
4. **Güvenlik**: CSV ve organize klasörünü kullanım sonrası güvenli silin

### 📖 Detaylı Dokümantasyon

- `README.md`: Genel kullanım kılavuzu
- `USAGE_GUIDE.md`: Detaylı kullanım rehberi
- Kod içi açıklamalar: Tüm fonksiyonlar dokümante edilmiş
