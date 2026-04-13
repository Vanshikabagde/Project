@echo off
echo Starting HealthGuard Web Application...
echo.
echo The application will be accessible at:
echo Local: http://127.0.0.1:5000
echo Network: http://[YOUR_IP_ADDRESS]:5000
echo.
echo To make it accessible over the internet, use ngrok:
echo 1. Download ngrok from https://ngrok.com
echo 2. Run: ngrok http 5000
echo 3. Share the generated https URL
echo.
cd /d "%~dp0"
python app.py