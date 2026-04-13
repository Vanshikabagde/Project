@echo off
echo ============================================
echo    HealthGuard - ngrok Public Tunnel
echo ============================================
echo.
echo Starting ngrok tunnel on port 5000...
echo.
echo Make sure your Flask app is running in another window!
echo (Command: python app.py)
echo.
echo Your public website URL will appear below:
echo ============================================
echo.

ngrok http 5000

echo.
echo Tunnel stopped. To start again, run this batch file.
pause
