@echo off
setlocal enabledelayedexpansion

echo ============================================
echo    Complete HealthGuard Sharing Setup
echo ============================================
echo.
echo This script will help you share your website with the world!
echo.

:menu
echo.
echo What do you want to do?
echo.
echo 1. Setup ngrok (one-time setup)
echo 2. Start ngrok tunnel (after setup complete)
echo 3. View your local website (http://127.0.0.1:5000)
echo 4. Start Flask app (python app.py)
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto :setup_ngrok
if "%choice%"=="2" goto :start_ngrok
if "%choice%"=="3" goto :view_local
if "%choice%"=="4" goto :start_flask
if "%choice%"=="5" goto :exit_script

echo Invalid choice. Please try again.
goto :menu

:setup_ngrok
cls
echo ============================================
echo    Step 1: Download ngrok
echo ============================================
echo.
echo Downloading ngrok...
cd /d "%~dp0"
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip' -ErrorAction SilentlyContinue"

if not exist "ngrok.zip" (
    echo.
    echo Failed to download ngrok. Checking if it's already installed...
    if not exist "ngrok.exe" (
        echo.
        echo Please download ngrok manually from: https://ngrok.com/download
        echo Extract it to: %~dp0
        pause
        goto :menu
    )
) else (
    echo Extracting ngrok...
    powershell -Command "Expand-Archive -Path ngrok.zip -DestinationPath . -Force"
    del ngrok.zip
)

echo.
echo ============================================
echo    Step 2: Create ngrok Account
echo ============================================
echo.
echo Opening ngrok website...
echo.
echo Please:
echo 1. Go to https://ngrok.com
echo 2. Click "Sign Up" (top right)
echo 3. Create a FREE account
echo 4. Verify your email
echo 5. Copy your Authtoken from the dashboard
echo.
start https://ngrok.com/signup
echo.
pause

echo.
echo ============================================
echo    Step 3: Authenticate ngrok
echo ============================================
echo.
set /p token="Paste your ngrok Authtoken here: "

if "%token%"=="" (
    echo ERROR: No token provided.
    goto :menu
)

echo Authenticating...
ngrok config add-authtoken %token%

echo.
echo ============================================
echo    Setup Complete!
echo ============================================
echo.
echo Next: Run "setup_ngrok.bat" again and choose option 2
echo Or run: start_ngrok.bat
echo.
pause
goto :menu

:start_ngrok
cls
echo ============================================
echo    Important!
echo ============================================
echo.
echo Make sure your Flask app is running!
echo.
echo If not, open another command prompt and run:
echo   python app.py
echo.
pause
echo.
echo Starting ngrok tunnel...
echo.
call start_ngrok.bat
goto :menu

:view_local
start http://127.0.0.1:5000
echo Opening local website...
timeout /t 2 /nobreak
goto :menu

:start_flask
cd /d "%~dp0"
python app.py
goto :menu

:exit_script
echo Goodbye!
pause
exit /b 0
