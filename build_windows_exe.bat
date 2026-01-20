@echo off
REM Windows executable builder using PyInstaller
REM Bu script Python uygulamalarini Windows .exe dosyalarina donusturur
REM This script converts Python applications to Windows .exe files

echo ======================================================================
echo   CVV2.NET - Windows Executable Builder
echo   PyInstaller ile EXE Olusturucu / EXE Builder with PyInstaller
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi / ERROR: Python not found
    echo Lutfen once setup_windows.bat calistirin / Please run setup_windows.bat first
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller yukleniyor / Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo PyInstaller bulundu / PyInstaller found
echo.

REM Build cvv2net.exe
echo ======================================================================
echo cvv2net.exe olusturuluyor / Building cvv2net.exe...
echo ======================================================================
pyinstaller --clean cvv2net.spec
if errorlevel 1 (
    echo HATA: cvv2net.exe olusturulamadi / ERROR: Failed to build cvv2net.exe
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo ocr_card_extractor.exe olusturuluyor / Building ocr_card_extractor.exe...
echo ======================================================================
pyinstaller --clean ocr_card_extractor.spec
if errorlevel 1 (
    echo HATA: ocr_card_extractor.exe olusturulamadi / ERROR: Failed to build ocr_card_extractor.exe
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo BASARILI! / SUCCESS!
echo ======================================================================
echo.
echo Dosyalar olusturuldu / Files created:
echo   - dist\cvv2net.exe
echo   - dist\ocr_card_extractor.exe
echo.
echo Bu .exe dosyalari baska Windows bilgisayarlarda calistirilabilir.
echo These .exe files can be run on other Windows computers.
echo.
echo NOTLAR / NOTES:
echo - ocr_card_extractor.exe icin Tesseract OCR ayri yuklenmelidir
echo - Tesseract OCR must be installed separately for ocr_card_extractor.exe
echo.
echo - Dosyalar yaklaşık 50-100 MB olabilir
echo - Files may be approximately 50-100 MB
echo.
pause
