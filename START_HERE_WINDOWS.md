# 🪟 Windows Kullanıcıları İçin / For Windows Users

## 🚀 3 Adımda Başla / Get Started in 3 Steps

### 1️⃣ Python Kur / Install Python
[Python İndir / Download](https://www.python.org/downloads/) → "Add to PATH" işaretle / Check "Add to PATH"

### 2️⃣ Kurulum / Setup
```cmd
setup_windows.bat
```
Çift tıkla / Double-click

### 3️⃣ Çalıştır / Run
```cmd
run_cvv2net.bat          # Metin tarayıcı / Text scanner
run_ocr_extractor.bat    # OCR çıkartıcı / OCR extractor
```
Çift tıkla / Double-click

---

## 📚 Dokümantasyon / Documentation

### Hızlı Başlangıç / Quick Start
👉 **[WINDOWS_README.md](WINDOWS_README.md)**
- 3 adımda kullanım / 3-step usage
- Örnek komutlar / Example commands
- Yaygın sorunlar / Common issues

### Kapsamlı Kılavuz / Full Guide
👉 **[WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)**
- Adım adım kurulum / Step-by-step setup
- Tesseract OCR kurulumu / Tesseract OCR installation
- Sorun giderme / Troubleshooting
- İleri seviye / Advanced topics

### Windows Native Açıklaması / Windows Native Explanation
👉 **[WINDOWS_NATIVE.md](WINDOWS_NATIVE.md)**
- Neden bu yöntem? / Why this approach?
- PyInstaller vs .NET karşılaştırması / Comparison
- Teknik detaylar / Technical details

### Değişiklikler / Changes
👉 **[CHANGES.md](CHANGES.md)**
- Ne eklendi? / What was added?
- Dosya listesi / File list
- Özellikler / Features

---

## 💻 Üç Kullanım Yöntemi / Three Usage Methods

### ⭐ Yöntem 1: Batch Dosyaları (Önerilen)
**En kolay! / Easiest!**

Windows Gezgini'nde çift tıkla / Double-click in Windows Explorer:
- `setup_windows.bat` → Kurulum / Setup
- `run_cvv2net.bat` → Metin tarayıcı / Text scanner  
- `run_ocr_extractor.bat` → OCR çıkartıcı / OCR extractor

### 🎁 Yöntem 2: Windows EXE (Python Gerektirmez)
**Python olmayan bilgisayarlar için / For PCs without Python**

```cmd
build_windows_exe.bat
```

Oluşturur / Creates:
- `dist\cvv2net.exe` (~50-80 MB)
- `dist\ocr_card_extractor.exe` (~80-100 MB)

Bu .exe dosyaları Python yüklü olmayan bilgisayarlarda çalışır!
These .exe files work on PCs without Python installed!

### 🐍 Yöntem 3: Klasik Python
**Geliştiriciler için / For developers**

```cmd
python cvv2net.py
python ocr_card_extractor.py
```

---

## 🎯 Hangi Yöntemi Seçmeliyim? / Which Method Should I Choose?

| Durum / Situation | Öneri / Recommendation |
|------------------|----------------------|
| İlk kez kullanıyorum / First time user | ⭐ Batch dosyaları / Batch files |
| Python kurmak istemiyorum / Don't want Python | 🎁 Windows EXE |
| Başka bilgisayarlara dağıtacağım / Will distribute | 🎁 Windows EXE |
| Geliştirici veya ileri kullanıcı / Developer | 🐍 Python doğrudan / Direct Python |

---

## ❓ Sık Sorulan Sorular / FAQ

### Python nereden indirilir?
**Where to download Python?**
https://www.python.org/downloads/

### Tesseract OCR gerekli mi?
**Is Tesseract OCR required?**
- `cvv2net.bat` için: ❌ Hayır / No
- `ocr_card_extractor.bat` için: ✅ Evet / Yes

Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

### EXE dosyaları güvenli mi?
**Are EXE files safe?**
✅ Evet, PyInstaller ile oluşturuldu / Yes, created with PyInstaller
⚠️ Antivirüs yanlış alarm verebilir / Antivirus may show false positive
💡 Çözüm: Güvenli listeye ekle / Solution: Add to whitelist

### Hangi Windows sürümlerinde çalışır?
**Which Windows versions work?**
- ✅ Windows 11
- ✅ Windows 10  
- ✅ Windows 8.1
- ⚠️ Windows 7 (Python 3.8 gerekir / Requires Python 3.8)

### Hata alıyorum, ne yapmalıyım?
**I'm getting errors, what should I do?**
1. [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) → Sorun Giderme / Troubleshooting
2. GitHub Issues: https://github.com/cvv2com/ccfinder/issues
3. Forum: https://bhf.pro/threads/629649/

---

## 📁 Proje Dosyaları / Project Files

```
ccfinder/
│
├── 🪟 WINDOWS DOSYALARI / WINDOWS FILES
│   ├── setup_windows.bat         ← ÖNCE BU / START HERE
│   ├── run_cvv2net.bat          ← Metin tarayıcı / Text scanner
│   ├── run_ocr_extractor.bat    ← OCR çıkartıcı / OCR extractor
│   ├── build_windows_exe.bat    ← EXE oluştur / Create EXE
│   ├── cvv2net.spec             ← Build config
│   └── ocr_card_extractor.spec  ← Build config
│
├── 📖 DOKÜMANTASYON / DOCUMENTATION
│   ├── START_HERE_WINDOWS.md    ← BU DOSYA / THIS FILE
│   ├── WINDOWS_README.md        ← Hızlı başlangıç / Quick start
│   ├── WINDOWS_GUIDE.md         ← Tam kılavuz / Full guide
│   ├── WINDOWS_NATIVE.md        ← Açıklama / Explanation
│   ├── CHANGES.md               ← Değişiklikler / Changes
│   └── README.md                ← Ana README / Main README
│
└── 🐍 PYTHON DOSYALARI / PYTHON FILES
    ├── cvv2net.py               ← Ana program / Main program
    ├── ocr_card_extractor.py    ← OCR program
    └── requirements.txt         ← Gereksinimler / Requirements
```

---

## 🎬 Hızlı Demo / Quick Demo

```cmd
REM 1. Kurulum / Setup
setup_windows.bat

REM 2. Metin tarayıcı / Text scanner
run_cvv2net.bat
> Path: C:\belgeler\taranacak_klasor
> Thread: 8
> CSV: sonuclar.csv

REM 3. OCR çıkartıcı / OCR extractor
run_ocr_extractor.bat
> PDF ve görselleri ./kart_kayitlari klasörüne koyun
> Put PDFs and images in ./kart_kayitlari folder
```

---

## ⚡ Sorun Giderme / Quick Troubleshooting

### Python bulunamıyor / Python not found
```cmd
python --version
```
✅ Görünüyorsa: OK
❌ Görünmüyorsa: Python'u yeniden kur, "Add to PATH" işaretle

### pip çalışmıyor / pip not working
```cmd
python -m pip --version
```

### Tesseract bulunamıyor / Tesseract not found
```cmd
tesseract --version
```
❌ Bulunamazsa: https://github.com/UB-Mannheim/tesseract/wiki

### Paket yüklenemiyor / Can't install package
```cmd
python -m pip install --upgrade pip
pip cache purge
pip install -r requirements.txt
```

---

## 🎓 Öğreticiler / Tutorials

### İlk Tarama / First Scan
1. `setup_windows.bat` çalıştır / Run
2. `run_cvv2net.bat` çalıştır / Run
3. Taranacak klasör yolunu gir / Enter folder path
4. Sonuçları CSV'de gör / See results in CSV

### EXE Oluşturma / Creating EXE
1. `setup_windows.bat` çalıştır / Run (eğer henüz çalıştırmadıysan / if not yet)
2. `build_windows_exe.bat` çalıştır / Run
3. `dist/` klasöründe .exe dosyalarını bul / Find .exe files in dist/
4. İstediğin yere kopyala / Copy anywhere
5. Python olmadan çalıştır / Run without Python

---

## 🌟 Özellikler / Features

✅ Kolay kurulum / Easy setup
✅ Çift tıkla çalıştır / Double-click to run
✅ Python gerektirmeyen EXE / Python-free EXE option
✅ Türkçe + İngilizce / Turkish + English
✅ Detaylı dokümantasyon / Comprehensive docs
✅ Hata kontrolü / Error handling
✅ Güvenlik uyarıları / Security warnings

---

## 💬 Destek / Support

🐛 **Hata mı buldunuz? / Found a bug?**
→ https://github.com/cvv2com/ccfinder/issues

💡 **Soru mu var? / Have a question?**
→ https://bhf.pro/threads/629649/

🌐 **Daha fazla bilgi / More info**
→ https://www.cvv2.net

---

**Başarılar! / Good Luck!** 🎉

Windows'ta kullanımı kolay! / Easy to use on Windows!
