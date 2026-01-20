# Windows için CVV2.NET - Hızlı Başlangıç
# CVV2.NET for Windows - Quick Start

---

## 🎯 3 Kolay Adımda Başlayın / Get Started in 3 Easy Steps

### 1️⃣ Python'u Kurun / Install Python

- [Python İndirin / Download Python](https://www.python.org/downloads/)
- Kurulum sırasında **"Add Python to PATH"** işaretleyin / Check **"Add Python to PATH"** during installation

### 2️⃣ Kurulumu Yapın / Run Setup

Proje klasöründe **çift tıklayın** / **Double-click** in project folder:

```
setup_windows.bat
```

Bu otomatik olarak tüm gereksinimleri yükler / This automatically installs all requirements.

### 3️⃣ Programı Çalıştırın / Run the Program

**Çift tıklayın / Double-click:**

- `run_cvv2net.bat` → Metin tarayıcı / Text scanner
- `run_ocr_extractor.bat` → OCR çıkartıcı / OCR extractor

✅ **Tamamlandı! / Done!**

---

## 🚀 Python Olmadan Kullanım / Use Without Python

Windows `.exe` dosyaları oluşturmak için / To create Windows `.exe` files:

```cmd
build_windows_exe.bat
```

Oluşturulan dosyalar / Generated files in `dist/`:
- `cvv2net.exe` 
- `ocr_card_extractor.exe`

Bu dosyalar Python yüklü olmayan bilgisayarlarda çalışır!
These files work on computers without Python installed!

---

## 📖 Detaylı Kılavuz / Detailed Guide

🇹🇷 **Türkçe**: [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)
🇬🇧 **English**: See [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)

---

## ❓ Sorun mu yaşıyorsunuz? / Having Issues?

### Python bulunamıyor / Python not found
- Python'u yeniden kurun ve "Add to PATH" seçeneğini işaretleyin
- Reinstall Python and check "Add to PATH" option

### Tesseract gerekli / Tesseract required
- [Tesseract İndirin / Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- OCR özelliği için gereklidir / Required for OCR feature

### Diğer sorunlar / Other issues
- [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) dosyasındaki sorun giderme bölümüne bakın
- See troubleshooting section in [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)

---

## 📂 Dosya Yapısı / File Structure

```
ccfinder/
│
├── run_cvv2net.bat              ← ÇİFT TIKLA / DOUBLE-CLICK
├── run_ocr_extractor.bat        ← ÇİFT TIKLA / DOUBLE-CLICK
├── setup_windows.bat            ← ÖNCE BU / RUN THIS FIRST
├── build_windows_exe.bat        ← EXE oluştur / Create EXE
│
├── cvv2net.py                   ← Ana program / Main program
├── ocr_card_extractor.py        ← OCR programı / OCR program
│
├── WINDOWS_GUIDE.md             ← Detaylı kılavuz / Full guide
└── README.md                    ← Genel bilgi / General info
```

---

## ✅ Sistem Gereksinimleri / System Requirements

- ✅ Windows 10 / 11 (Önerilen / Recommended)
- ✅ Windows 8.1
- ⚠️ Windows 7 (Python 3.8 veya öncesi / or earlier)
- 💾 En az 2GB RAM / At least 2GB RAM
- 💿 500MB boş disk alanı / 500MB free disk space

---

## 🎓 Örnek Kullanım / Example Usage

### Metin Tarayıcı / Text Scanner

```cmd
run_cvv2net.bat
```

```
Path: C:\belgeler\taranacak_klasor
Thread sayısı: 8
CSV dosya adı: sonuclar.csv
```

### OCR Çıkartıcı / OCR Extractor

```cmd
run_ocr_extractor.bat
```

PDF ve görsel dosyalarınızı `./kart_kayitlari` klasörüne koyun
Put your PDF and image files in `./kart_kayitlari` folder

---

## 🔒 Güvenlik / Security

⚠️ Bu araçlar hassas finansal veri işler / These tools process sensitive financial data

**Güvenlik önerileri / Security recommendations:**
- CSV dosyalarını işlem sonrası silin / Delete CSV files after processing
- Sadece güvenilir dosyaları tarayın / Only scan trusted files
- Verileri şifreli disklerde saklayın / Store data on encrypted drives

---

## 📞 Destek / Support

- 🐛 [GitHub Issues](https://github.com/cvv2com/ccfinder/issues)
- 🌐 [CVV2.NET](https://www.cvv2.net)
- 💬 [Forum](https://bhf.pro/threads/629649/)

---

**Başarılar! / Good Luck!** 🎉
