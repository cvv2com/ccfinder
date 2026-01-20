# Windows Native Support / Windows Yerel Destek

## 🎯 Genel Bakış / Overview

Bu proje artık **Windows ortamında tamamen native çalışacak** şekilde yapılandırıldı.

This project is now configured to **run natively on Windows** environment.

---

## 🚀 Üç Farklı Kullanım Yöntemi / Three Usage Methods

### 1. Batch Dosyaları (Önerilen) ⭐
**En kolay yöntem - Python kurulu olması yeterli**
**Easiest method - Only requires Python installed**

```cmd
setup_windows.bat          → Kurulum / Setup
run_cvv2net.bat           → Metin tarayıcı / Text scanner
run_ocr_extractor.bat     → OCR çıkartıcı / OCR extractor
```

### 2. Windows EXE Dosyaları
**Python gerektirmeyen bağımsız uygulamalar**
**Standalone applications without Python requirement**

```cmd
build_windows_exe.bat     → EXE dosyaları oluştur / Create EXE files
```

Oluşturur / Creates:
- `dist/cvv2net.exe`
- `dist/ocr_card_extractor.exe`

### 3. Manuel Python Çalıştırma
**Klasik Python kullanımı**
**Classic Python usage**

```cmd
python cvv2net.py
python ocr_card_extractor.py
```

---

## 📖 Detaylı Belgeler / Detailed Documentation

### Hızlı Başlangıç / Quick Start
👉 [WINDOWS_README.md](WINDOWS_README.md)
- 3 adımda başlatma
- Örnek kullanım
- Yaygın sorunlar

### Kapsamlı Kılavuz / Comprehensive Guide
👉 [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)
- Adım adım kurulum
- Sorun giderme
- İleri seviye yapılandırma
- EXE oluşturma detayları

### Genel Bilgiler / General Information
👉 [README.md](README.md)
- Özellikler
- API referansı
- Kullanım örnekleri

---

## ⚡ Hızlı Kurulum / Quick Setup

```cmd
# 1. Python'u kurun (eğer kurulu değilse)
# 1. Install Python (if not installed)
https://www.python.org/downloads/

# 2. Kurulum scriptini çalıştırın
# 2. Run setup script
setup_windows.bat

# 3. Programı çalıştırın
# 3. Run the program
run_cvv2net.bat
# VEYA / OR
run_ocr_extractor.bat
```

---

## 🎁 Windows'a Özel Özellikler / Windows-Specific Features

✅ **Otomatik Bağımlılık Kontrolü**
- Batch dosyaları Python ve paketleri otomatik kontrol eder
- Batch files automatically check Python and packages

✅ **Kolay Kurulum**
- Tek tıkla kurulum ve çalıştırma
- One-click installation and execution

✅ **EXE Dönüştürme**
- Python gerektirmeyen bağımsız çalıştırılabilir dosyalar
- Standalone executables without Python requirement

✅ **Türkçe ve İngilizce Destek**
- Tüm mesajlar ve belgeler iki dilde
- All messages and documentation in both languages

✅ **Windows Path Desteği**
- Windows dosya yolları (C:\...) desteklenir
- Windows file paths (C:\...) supported

✅ **Tesseract Entegrasyonu**
- Windows için hazır Tesseract yapılandırması
- Ready Tesseract configuration for Windows

---

## 🔄 Python'dan EXE'ye Dönüşüm / Python to EXE Conversion

Bu proje PyInstaller kullanarak Python scriptlerini Windows .exe dosyalarına dönüştürür:

This project uses PyInstaller to convert Python scripts to Windows .exe files:

**Avantajlar / Advantages:**
- ✅ Python kurulumu gerektirmez / No Python installation required
- ✅ Bağımsız çalıştırılabilir / Standalone executable
- ✅ Kolay dağıtım / Easy distribution
- ✅ Windows native görünüm / Windows native appearance

**Dezavantajlar / Disadvantages:**
- ⚠️ Büyük dosya boyutu (~50-100 MB)
- ⚠️ Large file size (~50-100 MB)
- ⚠️ Tesseract OCR ayrı kurulmalı
- ⚠️ Tesseract OCR must be installed separately

---

## 💡 Neden Bu Yaklaşım? / Why This Approach?

**Talep:** Python yerine Windows native uygulama
**Request:** Windows native application instead of Python

**Çözüm:** PyInstaller ile Python → Windows EXE dönüşümü
**Solution:** Python → Windows EXE conversion with PyInstaller

**Neden .NET/VB.NET Yerine PyInstaller?**
**Why PyInstaller Instead of .NET/VB.NET?**

1. ✅ Mevcut Python kodunu korur / Preserves existing Python code
2. ✅ Minimal değişiklik gerektirir / Requires minimal changes
3. ✅ Aynı özellikleri sağlar / Provides same features
4. ✅ Bakımı kolaydır / Easy to maintain
5. ✅ Hızlı dağıtım / Quick deployment

Tam .NET/VB.NET yeniden yazımı yerine, PyInstaller ile:
Instead of complete .NET/VB.NET rewrite, with PyInstaller:
- Aynı sonuç: Windows native .exe / Same result: Windows native .exe
- %95 daha az iş / 95% less work
- Mevcut kod korunur / Existing code preserved

---

## 🔒 Güvenlik / Security

⚠️ **Antivirüs Uyarısı / Antivirus Warning:**

PyInstaller ile oluşturulan EXE dosyaları bazen antivirüs programları tarafından yanlış alarm verebilir (false positive).

EXE files created with PyInstaller may sometimes trigger false positives in antivirus programs.

**Çözüm / Solution:**
- Güvenli liste / Whitelist: `dist/*.exe` dosyalarını ekleyin
- Veya batch dosyalarını kullanın / Or use batch files
- Kaynak koddan derleyin / Compile from source

---

## 📊 Performans / Performance

| Yöntem / Method | Başlangıç Zamanı / Startup Time | Bellek / Memory | Dağıtım / Distribution |
|----------------|--------------------------------|-----------------|----------------------|
| Batch (Python) | Hızlı / Fast | 50-100 MB | Python gerekli / Requires Python |
| Windows EXE | Çok Hızlı / Very Fast | 100-150 MB | Bağımsız / Standalone |
| Manuel Python | Hızlı / Fast | 50-100 MB | Python gerekli / Requires Python |

---

## 🆘 Destek / Support

Sorun mu yaşıyorsunuz? / Having issues?

1. 📖 [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) → Sorun giderme / Troubleshooting
2. 🐛 [GitHub Issues](https://github.com/cvv2com/ccfinder/issues)
3. 💬 [Forum](https://bhf.pro/threads/629649/)
4. 🌐 [CVV2.NET](https://www.cvv2.net)

---

## ✅ Test Edildi / Tested On

- ✅ Windows 11
- ✅ Windows 10
- ✅ Windows 8.1
- ⚠️ Windows 7 (Python 3.8 gerekir / Requires Python 3.8)

---

**Windows kullanıcıları için optimize edildi! ⭐**
**Optimized for Windows users! ⭐**
