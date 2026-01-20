# Yeni Özellikler / New Features

## OCR Kart Çıkartıcı v2.1 - Yeni Özellikler

### 🎯 Ana Özellikler

#### 1. **Akıllı Dosya Tespit Sistemi** 🔍 **YENİ v2.1**
Dosyalar artık sadece uzantıya göre değil, **içerik analizine** göre de tespit edilir:

**Magic Byte (İçerik) Analizi:**
- ✅ PDF: `%PDF` header tespiti
- ✅ JPEG: `FF D8 FF` header tespiti
- ✅ PNG: `89 50 4E 47` header tespiti
- ✅ GIF: `GIF87a` / `GIF89a` tespiti
- ✅ BMP: `BM` header tespiti
- ✅ TIFF: `II 2A 00` (Little Endian) / `MM 00 2A` (Big Endian)
- ✅ WebP: `RIFF...WEBP` tespiti
- ✅ Fallback: Python `imghdr` + PIL doğrulaması

**Neden Bu Önemli?**
Bazı durumlarda dosyalar:
- Yanlış uzantıyla kaydedilebilir (örn: `.txt` ama aslında `.jpg`)
- Uzantısız olabilir
- Garip uzantılara sahip olabilir

Script artık **dosya içeriğini okuyarak** gerçek formatı tespit eder!

**Örnek Senaryo:**
```bash
kart_kayitlari/
  ├── kart_001.pdf          # Uzantıya göre tespit ✓
  ├── kart_002.jpg          # Uzantıya göre tespit ✓
  ├── foto_003              # Uzantısız ama içerik PNG! 🔍
  ├── dokuman.txt           # Aslında JPEG! 🔍
  └── scan.dat              # İçeriği PDF! 🔍

# Script çalıştırıldığında:
Toplam 5 dosya taranacak:
  - PDF dosyaları: 2
  - Görsel dosyaları: 3

Tespit yöntemi:
  - Uzantıya göre: 2
  - İçeriğe göre: 3 🔍
    ℹ️  3 dosya yanlış/eksik uzantıya sahip ama içerik analizi ile tespit edildi
```

**Çıktıda Gösterim:**
```
[1/5] İşleniyor: kart_001.pdf
[2/5] İşleniyor: kart_002.jpg
[3/5] İşleniyor: foto_003 [İçerik✓]  ← İçerik analiziyle tespit edildi!
[4/5] İşleniyor: dokuman.txt [İçerik✓]  ← Aslında JPEG!
[5/5] İşleniyor: scan.dat [İçerik✓]  ← Aslında PDF!
```

**CSV Çıktısında:**
```csv
Dosya_Kaynagi,Dosya_Tipi,Tespit_Yontemi,Kart_Sahibi,Kart_Numarasi,...
"kart_001.pdf","PDF","Uzantı","JOHN DOE","4546571054123456",...
"foto_003","Görsel/Image","İçerik Analizi","JANE SMITH","5412345678901234",...
```

#### 2. **Çoklu Format Desteği** 
Artık sadece PDF değil, tüm görsel formatları destekliyoruz:
- ✅ PDF dosyaları (`.pdf`)
- ✅ JPEG görseller (`.jpg`, `.jpeg`)
- ✅ PNG görseller (`.png`)
- ✅ BMP görseller (`.bmp`)
- ✅ TIFF görseller (`.tiff`, `.tif`)
- ✅ GIF görseller (`.gif`)
- ✅ WebP görseller (`.webp`)
- ✅ **Uzantısız veya yanlış uzantılı dosyalar** 🆕

**Örnek Kullanım:**
```bash
# Klasöre farklı formatlarda dosyalar koyun
kart_kayitlari/
  ├── kart_001.pdf
  ├── kart_002.jpg
  ├── kart_003.png
  ├── kart_scan_004.tiff
  ├── foto_without_ext      # Uzantısız
  └── wrong_name.txt        # Yanlış uzantı

# Scripti çalıştırın
python ocr_card_extractor.py
```

#### 3. **AI Organizasyon Sistemi** (Nero AI Photo Tagger benzeri)
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

#### 4. **İnteraktif Kullanıcı Arayüzü**
```
======================================================================
  KREDİ KARTI BİLGİ ÇIKARTICI / CREDIT CARD INFORMATION EXTRACTOR
  OCR + AI Organizasyon Sistemi / OCR + AI Organization System
======================================================================

Toplam 12 dosya taranacak / Total files to scan:
  - PDF dosyaları / PDF files: 5
  - Görsel dosyaları / Image files: 7

Tespit yöntemi / Detection method:
  - Uzantıya göre / By extension: 9
  - İçeriğe göre / By content: 3 🔍
    ℹ️  3 dosya yanlış/eksik uzantıya sahip ama içerik analizi ile tespit edildi
    ℹ️  3 file(s) have wrong/missing extension but detected by content analysis

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

[2/12] İşleniyor / Processing: kart_002.jpg [İçerik✓]
  ✓ Kart Bulundu / Card Found: 5412********1234
  ✓ Kart Sahibi / Cardholder: JANE SMITH
  ✓ SKT / Exp: 12/26
  ✓ CVV: ***
  ---> Organize edildi / Organized: ./organize_kartlar/JANE_SMITH
```

#### 5. **Geliştirilmiş Çıktı Formatı**
CSV dosyası artık daha fazla bilgi içeriyor:

```csv
Dosya_Kaynagi,Dosya_Tipi,Tespit_Yontemi,Kart_Sahibi,Kart_Numarasi,SKT,CVV,Tarama_Zamani
"kart_001.pdf","PDF","Uzantı","JOHN DOE","4546571054123456","04/25","123","2026-01-20 12:30:45"
"kart_002.jpg","Görsel/Image","İçerik Analizi","JANE SMITH","5412345678901234","12/26","456","2026-01-20 12:30:47"
```

**Yeni Kolonlar:**
- `Dosya_Tipi`: PDF veya Görsel/Image
- `Tespit_Yontemi`: Uzantı veya İçerik Analizi 🆕
- `Tarama_Zamani`: İşlem zaman damgası

#### 6. **Güvenlik İyileştirmeleri**
- ✅ CSV dosyası otomatik olarak 600 izinleriyle oluşturulur (sadece sahip okuyabilir)
- ✅ İşlem öncesi kullanıcı onayı
- ✅ İşlem sonrası güvenlik uyarısı
- ✅ Detaylı başarı/başarısızlık raporlaması

#### 7. **Çift Dil Desteği**
Tüm çıktılar ve mesajlar hem Türkçe hem İngilizce:
- ✓ Bilgilendirme mesajları
- ✓ Hata mesajları
- ✓ Kod içi açıklamalar
- ✓ Dokümantasyon

### 📊 Karşılaştırma

| Özellik | v1.0 | v2.0 | v2.1 (Yeni) |
|---------|------|------|-------------|
| PDF Desteği | ✅ | ✅ | ✅ |
| Görsel Desteği | ❌ | ✅ (JPG, PNG, BMP, TIFF) | ✅ (JPG, PNG, BMP, TIFF, GIF, WebP) |
| İçerik Tespit | ❌ | ❌ | ✅ Magic Bytes 🆕 |
| Yanlış Uzantı Desteği | ❌ | ❌ | ✅ 🆕 |
| Uzantısız Dosya | ❌ | ❌ | ✅ 🆕 |
| AI Organizasyon | ❌ | ✅ (Kart sahibine göre) | ✅ |
| İnteraktif UI | ❌ | ✅ | ✅ Geliştirilmiş |
| Çift Dil | ❌ | ✅ (TR/EN) | ✅ |
| Zaman Damgası | ❌ | ✅ | ✅ |
| Tespit Yöntemi Takibi | ❌ | ❌ | ✅ CSV'de 🆕 |
| Güvenlik Onayı | ❌ | ✅ | ✅ |
| Detaylı Raporlama | Temel | Gelişmiş | Çok Gelişmiş 🆕 |

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

**Senaryo 4: Yanlış Uzantılı Dosyalar** 🆕
```
Durumu: Dosyalar yanlış isimlendirilmiş (kart.txt aslında JPG, foto.dat aslında PDF)
Çözüm: İçerik analizi ile otomatik tespit
Sonuç: Uzantıdan bağımsız işlem, hepsi taranır
Özellik: CSV'de "İçerik Analizi" ile işaretlenir
```

**Senaryo 5: Uzantısız Toplu Dosyalar** 🆕
```
Durumu: Eski sistemden gelen uzantısız dosyalar (kart001, kart002, vb.)
Çözüm: Magic byte analizi ile format tespiti
Sonuç: Tüm dosyalar taranır, içeriğe göre işlem yapılır
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
