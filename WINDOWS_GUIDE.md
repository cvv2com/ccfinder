# Windows Kurulum ve Kullanım Kılavuzu / Windows Installation and Usage Guide

Bu belge, CVV2.NET uygulamalarını Windows ortamında nasıl kuracağınızı ve çalıştıracağınızı adım adım açıklar.

This document explains step-by-step how to install and run CVV2.NET applications on Windows.

---

## 📋 İçindekiler / Table of Contents

1. [Hızlı Başlangıç (Batch Dosyaları)](#1-hızlı-başlangıç-batch-dosyaları)
2. [Windows EXE Dosyaları Oluşturma](#2-windows-exe-dosyaları-oluşturma)
3. [Manuel Python Kurulumu](#3-manuel-python-kurulumu)
4. [Tesseract OCR Kurulumu](#4-tesseract-ocr-kurulumu)
5. [Sorun Giderme](#5-sorun-giderme)

---

## 1. Hızlı Başlangıç (Batch Dosyaları)

En kolay yöntem! Hazır batch dosyalarını kullanarak programları çalıştırın.

### Adım 1: Python'u İndirin ve Kurun

1. [Python İndirme Sayfası](https://www.python.org/downloads/)na gidin
2. En son Python 3.x sürümünü indirin (örn: Python 3.11)
3. İndirdiğiniz kurulum dosyasını çalıştırın
4. **ÖNEMLİ:** Kurulum sırasında **"Add Python to PATH"** kutucuğunu işaretleyin!

![Python Kurulum Ekranı](https://docs.python.org/3/_images/win_installer.png)

### Adım 2: Projeyi İndirin

```cmd
# Git ile indirin (Git kurulu ise)
git clone https://github.com/cvv2com/ccfinder.git
cd ccfinder

# VEYA Manuel indirin
# GitHub sayfasından "Code" -> "Download ZIP" ile indirin
# ZIP dosyasını çıkartın ve klasöre gidin
```

### Adım 3: Kurulum Scriptini Çalıştırın

Proje klasöründe `setup_windows.bat` dosyasına **çift tıklayın** veya komut satırından çalıştırın:

```cmd
setup_windows.bat
```

Bu script:
- Python'un kurulu olduğunu kontrol eder
- Tüm gerekli paketleri yükler (PyPDF2, OpenCV, Tesseract, vb.)
- Tesseract OCR'ın kurulu olup olmadığını kontrol eder

### Adım 4: Programları Çalıştırın

Artık programları çalıştırmaya hazırsınız!

#### Metin Tabanlı Tarayıcı (cvv2net)

`run_cvv2net.bat` dosyasına **çift tıklayın**:

```cmd
run_cvv2net.bat
```

Program size taranacak klasör/dosya yolunu soracak. Örnek:
```
Path: C:\belgeler\taranacak_klasor
Thread sayısı: 8
CSV dosya adı: sonuclar.csv
```

#### OCR Tabanlı Çıkartıcı (OCR Card Extractor)

`run_ocr_extractor.bat` dosyasına **çift tıklayın**:

```cmd
run_ocr_extractor.bat
```

**Not:** OCR özelliklerini kullanmak için Tesseract OCR kurulu olmalıdır (bkz: [Tesseract Kurulumu](#4-tesseract-ocr-kurulumu))

---

## 2. Windows EXE Dosyaları Oluşturma

Python kurulu olmayan bilgisayarlarda çalıştırılabilir `.exe` dosyaları oluşturun.

### PyInstaller ile EXE Oluşturma

1. **Kurulum scriptini çalıştırın** (eğer henüz çalıştırmadıysanız):
   ```cmd
   setup_windows.bat
   ```

2. **EXE builder scriptini çalıştırın**:
   ```cmd
   build_windows_exe.bat
   ```

3. Script iki `.exe` dosyası oluşturacak:
   - `dist\cvv2net.exe` (~50-80 MB)
   - `dist\ocr_card_extractor.exe` (~80-100 MB)

### EXE Dosyalarını Kullanma

Oluşturulan `.exe` dosyaları:
- Python yüklü olmayan Windows bilgisayarlarda çalışır
- Tek başına (standalone) çalıştırılabilir
- Kopyalayıp başka bilgisayarlara taşınabilir

**ÖNEMLİ NOTLAR:**
- `ocr_card_extractor.exe` için Tesseract OCR hedef bilgisayarda ayrıca kurulu olmalıdır
- Antivirüs programları bazen `.exe` dosyalarını şüpheli bulabilir (false positive) - güvenli listeye ekleyin

### Manuel EXE Oluşturma (İleri Seviye)

```cmd
# PyInstaller'ı yükleyin
pip install pyinstaller

# cvv2net için EXE oluştur
pyinstaller --onefile --console cvv2net.py

# OCR extractor için EXE oluştur
pyinstaller --onefile --console ocr_card_extractor.py

# Spec dosyaları ile (özelleştirilmiş)
pyinstaller cvv2net.spec
pyinstaller ocr_card_extractor.spec
```

---

## 3. Manuel Python Kurulumu

Komut satırından adım adım kurulum yapmak isterseniz:

### Python Kurulumu Kontrolü

```cmd
python --version
```

Eğer hata alırsanız, Python'u [buradan](https://www.python.org/downloads/) indirip kurun.

### Paket Yükleme

```cmd
# Tüm gereksinimleri yükle
pip install -r requirements.txt

# VEYA tek tek yükle
pip install PyPDF2
pip install pdf2image
pip install pytesseract
pip install opencv-python
pip install pandas
pip install numpy
pip install Pillow
```

### Programları Çalıştırma

```cmd
# Metin tabanlı tarayıcı
python cvv2net.py

# OCR tabanlı çıkartıcı
python ocr_card_extractor.py
```

---

## 4. Tesseract OCR Kurulumu

OCR tabanlı çıkartıcı (`ocr_card_extractor.py`) için Tesseract OCR gereklidir.

### Windows İçin Tesseract Kurulumu

1. **Tesseract İndir:**
   - [UB-Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - En son sürümü indirin (örn: `tesseract-ocr-w64-setup-5.3.x.exe`)

2. **Kurulum:**
   - İndirdiğiniz `.exe` dosyasını çalıştırın
   - Varsayılan kurulum yolunu kullanın: `C:\Program Files\Tesseract-OCR`
   - Kurulum tamamlanana kadar bekleyin

3. **Tesseract Yolunu Ayarlama:**
   
   `ocr_card_extractor.py` dosyasını bir metin editörü ile açın (Notepad++, VS Code, vb.)
   
   Dosyanın başında şu satırı bulun:
   ```python
   # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
   
   Satırın başındaki `#` işaretini kaldırın:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
   
   Eğer farklı bir yere kurduysanız, yolu değiştirin:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
   ```

4. **Test:**
   ```cmd
   tesseract --version
   ```
   
   Sürüm bilgisi görmelisiniz.

### Alternatif: PATH Değişkenine Ekleme

Tesseract'i PATH değişkenine eklerseniz, kod değişikliği gerekmez:

1. Windows Arama'da "Ortam Değişkenleri" yazın
2. "Sistem ortam değişkenlerini düzenle"yi açın
3. "Ortam Değişkenleri" butonuna tıklayın
4. "Path" değişkenini seçip "Düzenle"ye tıklayın
5. "Yeni" butonuna tıklayıp şu yolu ekleyin:
   ```
   C:\Program Files\Tesseract-OCR
   ```
6. Tüm pencereleri "Tamam" ile kapatın
7. Yeni bir komut satırı penceresi açın ve test edin

---

## 5. Sorun Giderme

### Python bulunamıyor

**Hata:**
```
'python' is not recognized as an internal or external command
```

**Çözüm:**
1. Python'u yeniden kurun ve "Add Python to PATH" seçeneğini işaretleyin
2. VEYA Python'u PATH'e manuel olarak ekleyin:
   - Varsayılan yol: `C:\Users\KULLANICI_ADINIZ\AppData\Local\Programs\Python\Python311`
   - PATH değişkenine bu yolu ekleyin

### pip çalışmıyor

**Hata:**
```
'pip' is not recognized as an internal or external command
```

**Çözüm:**
```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Tesseract bulunamıyor

**Hata:**
```
TesseractNotFoundError: tesseract is not installed
```

**Çözüm:**
1. Tesseract'i [buradan](https://github.com/UB-Mannheim/tesseract/wiki) indirip kurun
2. `ocr_card_extractor.py` dosyasındaki Tesseract yolunu güncelleyin
3. VEYA Tesseract'i PATH değişkenine ekleyin

### İzin hatası (Permission denied)

**Hata:**
```
PermissionError: [Errno 13] Permission denied
```

**Çözüm:**
1. Komut satırını **Yönetici olarak çalıştırın**:
   - Başlat menüsünde "cmd" aratın
   - Sağ tık -> "Yönetici olarak çalıştır"
2. VEYA dosyaların bulunduğu klasörü kullanıcı klasörüne taşıyın (örn: `C:\Users\ADINIZ\belgeler\`)

### Paket yükleme hatası

**Hata:**
```
ERROR: Could not install packages due to an OSError
```

**Çözüm 1 - Önbelleği temizleyin:**
```cmd
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

**Çözüm 2 - pip'i güncelleyin:**
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Antivirüs EXE dosyasını engelliyor

Bazı antivirüs programları PyInstaller ile oluşturulan `.exe` dosyalarını false positive olarak işaretleyebilir.

**Çözüm:**
1. Antivirüs programınızın "İstisnalar" veya "Güvenli Liste" bölümüne gidin
2. `cvv2net.exe` ve `ocr_card_extractor.exe` dosyalarını ekleyin
3. VEYA tüm `dist\` klasörünü güvenli listeye ekleyin

### OpenCV DLL hatası

**Hata:**
```
ImportError: DLL load failed while importing cv2
```

**Çözüm:**
```cmd
pip uninstall opencv-python
pip install opencv-python-headless
```

VEYA Visual C++ Redistributable yükleyin:
- [Microsoft Visual C++ 2015-2022 Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 📞 Destek / Support

Sorun yaşıyorsanız:
1. [GitHub Issues](https://github.com/cvv2com/ccfinder/issues) sayfasından yeni bir issue açın
2. Hata mesajını ve Windows sürümünüzü belirtin
3. [CVV2.NET Forum](https://www.cvv2.net) üzerinden destek alabilirsiniz

---

## 📝 Ek Notlar

### Windows Sürüm Uyumluluğu
- ✅ Windows 11
- ✅ Windows 10
- ✅ Windows 8.1
- ⚠️ Windows 7 (Python 3.8 veya öncesi gerekebilir)

### Performans İpuçları
- Thread sayısını bilgisayarınızın CPU çekirdek sayısına göre ayarlayın
- Büyük dosyalar için SSD kullanın (daha hızlı okuma)
- OCR işlemleri için en az 4GB RAM önerilir

### Güvenlik Uyarısı
⚠️ Bu araçlar hassas finansal veri işler. Güvenlik için:
- CSV dosyalarını işlem sonrası silin
- Antivirüs ve Windows Defender'ı aktif tutun
- Sadece güvenilir kaynaklardan dosya tarayın
- Verileri şifreli disklerde saklayın

---

**Başarılar! / Good Luck!**
