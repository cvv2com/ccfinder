# OCR Kart Çıkartıcı - Kullanım Kılavuzu

## Hızlı Başlangıç

### 1. Sistem Gereksinimlerini Kurun

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

**MacOS:**
```bash
brew install tesseract poppler
```

**Windows:**
- [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) sayfasından indirip kurun
- Poppler için [releases](https://github.com/oschwartz10612/poppler-windows/releases/) sayfasından indirin

### 2. Python Bağımlılıklarını Yükleyin

```bash
pip install -r requirements.txt
```

### 3. PDF Klasörü Oluşturun

```bash
mkdir pdf_kayitlar
```

Kart görüntülerini içeren PDF dosyalarınızı bu klasöre koyun.

### 4. Scripti Çalıştırın

```bash
python ocr_card_extractor.py
```

## Çıktı Formatı

Script, aşağıdaki kolonları içeren bir CSV dosyası oluşturur:

| Kolon | Açıklama | Örnek |
|-------|----------|-------|
| Kart_Sahibi | Kart sahibinin adı | JOHN DOE |
| Kart_Numarasi | Tam kart numarası (PAN) | 4546571054123456 |
| SKT | Son kullanma tarihi | 04/25 |
| CVV | Güvenlik kodu | 123 |
| Dosya_Kaynagi | Kaynak PDF dosyası | kart_001.pdf |

## Ayarları Özelleştirme

`ocr_card_extractor.py` dosyasını düzenleyerek aşağıdaki ayarları değiştirebilirsiniz:

```python
PDF_KLASORU = "./pdf_kayitlar"  # PDF'lerin bulunduğu klasör
CIKTI_DOSYASI = "musteri_kredi_kartlari_tam_liste.csv"  # Çıktı dosyası
```

**Windows kullanıcıları için:** Tesseract yolunu belirtin:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## OCR Kalitesi İyileştirme İpuçları

1. **Yüksek Çözünürlük:** PDF'lerin en az 300 DPI çözünürlükte olması önerilir
2. **Net Görüntü:** Bulanık veya düşük kaliteli taramalar OCR başarısını düşürür
3. **Düzgün Işıklandırma:** Gölge veya parlamalar okuma hatalarına yol açabilir
4. **Düz Açı:** Kart düz ve dik açıda taranmalıdır

## Güvenlik Notları

⚠️ **UYARI:** Bu araç hassas finansal veri üretir!

**Güvenlik Kontrol Listesi:**
- [ ] CSV dosyasını veritabanına aktardıktan sonra güvenli olarak silin
- [ ] Kaynak PDF'leri de güvenli olarak silin (`shred` komutu)
- [ ] Erişimi yetkilendirilmiş personelle sınırlandırın
- [ ] Tüm işlemleri denetim kaydına alın
- [ ] Veritabanında PAN'ı tokenize edin
- [ ] PCI-DSS uyumluluk gereksinimlerini kontrol edin

## Sorun Giderme

### "Tesseract bulunamadı" Hatası
- Tesseract'ın doğru kurulduğundan emin olun
- Windows'ta `tesseract_cmd` yolunu ayarlayın

### OCR Hiçbir Veri Okuyamıyor
- PDF çözünürlüğünü artırın (300+ DPI)
- Görüntü kalitesini kontrol edin
- Kabartmalı yazılar için daha iyi ışıklandırma kullanın

### Yanlış Rakamlar Okuyor
- `preprocess_image_for_card()` fonksiyonundaki threshold parametrelerini ayarlayın
- Farklı tesseract PSM modları deneyin (--psm 6, 11, veya 13)

### Performans Çok Yavaş
- DPI değerini düşürün (ancak bu OCR kalitesini azaltır)
- PDF'leri daha küçük gruplara bölün
- Çok sayfalı PDF'leri tek sayfalık PDF'lere ayırın

## Test Etme

Regex desenlerini test etmek için:

```bash
python test_ocr_extractor.py
```

## Lisans ve Yasal Uyarı

Bu araç yalnızca yasal ve izinli kullanım içindir. Kart verilerini işlerken:

- Yerel veri koruma yasalarına uyun (KVKK, GDPR, vb.)
- PCI-DSS gereksinimlerini karşılayın
- Sadece sahip olduğunuz veya işleme yetkisi aldığınız verileri kullanın
