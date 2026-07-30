@echo off
cd /d "%~dp0"
echo ======================================
echo   Hotel FO Anomaly Detector
echo ======================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan. Install dari https://python.org
    pause
    exit /b 1
)

echo Menginstall dependencies...
pip install -r requirements.txt -q

if not exist uploads mkdir uploads
if not exist outputs mkdir outputs

echo.
echo Aplikasi berjalan di: http://localhost:5050
echo Tutup window ini untuk berhenti.
echo.
python app.py
pause
