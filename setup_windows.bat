@echo off
REM Windows kurulum scripti / Windows setup script
REM Tum gereksinimleri yukler / Installs all requirements

echo ======================================================================
echo   CVV2.NET - Windows Kurulum / Windows Setup
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi / ERROR: Python not found
    echo.
    echo Lutfen Python 3.8 veya daha yeni surum yukleyin:
    echo Please install Python 3.8 or newer:
    echo https://www.python.org/downloads/
    echo.
    echo Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin!
    echo During installation, check "Add Python to PATH" option!
    pause
    exit /b 1
)

echo Python bulundu / Python found:
python --version
echo.

REM Upgrade pip
echo pip guncelleniyor / Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo UYARI: pip guncellenemedi, devam ediliyor / WARNING: pip upgrade failed, continuing...
)
echo.

REM Install requirements
echo Gerekli Python paketleri yukleniyor / Installing required Python packages...
echo.
pip install -r requirements.txt
echo.

REM Check Tesseract
echo.
echo ======================================================================
echo Tesseract OCR Kontrolu / Tesseract OCR Check
echo ======================================================================
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo TESSERACT OCR BULUNAMADI / TESSERACT OCR NOT FOUND
    echo.
    echo OCR ozelliklerini kullanmak icin Tesseract OCR gereklidir:
    echo Tesseract OCR is required for OCR features:
    echo.
    echo 1. Asagidaki adresten Tesseract yukleyicisini indirin:
    echo    Download Tesseract installer from:
    echo    https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo 2. Tesseract'i yukleyin ^(varsayilan: C:\Program Files\Tesseract-OCR^)
    echo    Install Tesseract ^(default: C:\Program Files\Tesseract-OCR^)
    echo.
    echo 3. ocr_card_extractor.py dosyasini acin ve asagidaki satiri guncelleyin:
    echo    Open ocr_card_extractor.py and update this line:
    echo    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    echo.
    set /p dummy="Devam etmek icin bir tusa basin / Press any key to continue..."
) else (
    echo.
    echo Tesseract OCR bulundu / Tesseract OCR found:
    tesseract --version
)

echo.
echo ======================================================================
echo Kurulum Tamamlandi! / Setup Complete!
echo ======================================================================
echo.
echo Kullanilabilir programlar / Available programs:
echo.
echo 1. run_cvv2net.bat        - Metin tabanli tarayici / Text-based scanner
echo 2. run_ocr_extractor.bat  - OCR tabanli cikartici / OCR-based extractor
echo.
echo Bu dosyalara cift tiklayarak programlari calistirabilirsiniz.
echo You can run programs by double-clicking these files.
echo.
pause
