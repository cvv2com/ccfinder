@echo off
REM Windows batch file to run cvv2net.py
REM Kredi kart bilgisi cikartici - Metin tabanli tarayici
REM Credit card information extractor - Text-based scanner

echo ======================================================================
echo   CVV2.NET - Kredi Karti Tarayici / Credit Card Scanner
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

REM Check if required packages are installed
echo Gerekli paketler kontrol ediliyor / Checking required packages...
python -c "import PyPDF2" >nul 2>&1
if errorlevel 1 (
    echo PyPDF2 paketi bulunamadi, yukleniyor / PyPDF2 not found, installing...
    pip install PyPDF2
)

echo.
echo cvv2net.py calistiriliyor / Running cvv2net.py...
echo.
python cvv2net.py

pause
