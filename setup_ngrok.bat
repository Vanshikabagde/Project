@echo off
setlocal enabledelayedexpansion

echo ============================================
echo    ngrok Automated Setup for HealthGuard
echo ============================================
echo.

REM Check if ngrok is already installed
if exist "ngrok.exe" (
    echo ngrok is already installed!
    goto :auth_check
)

echo Step 1: Downloading ngrok...
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip' -ErrorAction SilentlyContinue"

if not exist "ngrok.zip" (
    echo.
    echo ERROR: Failed to download ngrok automatically.
    echo.
    echo Please:
    echo 1. Download ngrok from: https://ngrok.com/download
    echo 2. Extract it to: C:\Mini Project
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Step 2: Extracting ngrok...
powershell -Command "Expand-Archive -Path ngrok.zip -DestinationPath . -Force"
del ngrok.zip

echo ngrok downloaded and extracted successfully!
echo.

:auth_check
echo Step 3: ngrok Authentication Setup
echo.
echo To get your auth token:
echo 1. Go to https://ngrok.com
echo 2. Sign up for a FREE account
echo 3. Go to your dashboard
echo 4. Copy your Authtoken from "Your Authtoken" section
echo.

set /p token="Paste your ngrok Authtoken here: "

if "%token%"=="" (
    echo.
    echo ERROR: No token provided. Skipping authentication.
    echo You can authenticate later by running: ngrok config add-authtoken YOUR_TOKEN
    echo.
) else (
    echo.
    echo Authenticating ngrok...
    ngrok config add-authtoken %token%
    echo Authentication successful!
    echo.
)

echo ============================================
echo    Setup Complete!
echo ============================================
echo.
echo Your ngrok is ready to use!
echo.
echo Next Steps:
echo 1. Make sure your Flask app is running: python app.py
echo 2. Open a new command prompt
echo 3. Run: ngrok http 5000
echo 4. Share the https URL generated
echo.
pause
