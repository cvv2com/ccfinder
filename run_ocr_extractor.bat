@echo off
REM Windows batch file to run ocr_card_extractor.py
REM OCR tabanli PDF ve gorsel kart bilgisi cikartici
REM OCR-based PDF and image card information extractor

echo ======================================================================
echo   OCR Kart Cikartici / OCR Card Extractor
echo   Windows Batch Runner
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi / ERROR: Python not found
    echo Lutfen Python 3 yukleyin / Please install Python 3
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Tesseract is installed
echo Tesseract OCR kontrol ediliyor / Checking Tesseract OCR...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo UYARI: Tesseract OCR bulunamadi / WARNING: Tesseract OCR not found
    echo.
    echo Tesseract OCR yuklemek icin asagidaki adresi ziyaret edin:
    echo To install Tesseract OCR, visit:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo Kurulum sonrasi ocr_card_extractor.py dosyasinda Tesseract yolunu guncelleyin
    echo After installation, update Tesseract path in ocr_card_extractor.py
    echo.
    pause
)

REM Check if required packages are installed
echo Gerekli paketler kontrol ediliyor / Checking required packages...
python -c "import cv2, pytesseract, pandas, pdf2image" >nul 2>&1
if errorlevel 1 (
    echo Gerekli paketler bulunamadi, yukleniyor / Required packages not found, installing...
    pip install -r requirements.txt
)

echo.
echo ocr_card_extractor.py calistiriliyor / Running ocr_card_extractor.py...
echo.
python ocr_card_extractor.py

pause
