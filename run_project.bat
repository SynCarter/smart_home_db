@echo off
echo =========================================
echo Starting Smart Home Telemetry DB...
echo =========================================

echo 1. Installing requirements...
pip install -r requirements.txt

echo 2. Starting FastAPI Backend Server...
start cmd /k "uvicorn main:app --reload"

echo Waiting for server to boot...
timeout /t 3 /nobreak > NUL

echo 3. Starting IoT Simulator...
start cmd /k "python simulator.py"

echo 4. Launching Dashboard...
timeout /t 2 /nobreak > NUL
start index.html

echo =========================================
echo System is live! 
echo =========================================