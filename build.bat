@echo off
chcp 65001 > nul
echo =========================================
echo  Kiril - Latin Cevirici .exe yigilir...
echo =========================================

cd /d "%~dp0"

:: Create venv if it doesn't exist
if not exist "venv" (
    echo [1/4] Virtual environment yaradilir...
    python -m venv venv
)

echo [2/4] Asililiqlar qurulur...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

echo [3/4] PyInstaller ile .exe yigilir...
pyinstaller ^
    --clean ^
    --onefile ^
    --windowed ^
    --name KirilToLatin ^
    --add-data "venv\Lib\site-packages\customtkinter;customtkinter" ^
    main.py

echo.
echo =========================================
echo  Yigma basa catdi!
echo  Yekun .exe faylini dist\KirilToLatin.exe-de tapa bilersiniz.
echo =========================================
pause
