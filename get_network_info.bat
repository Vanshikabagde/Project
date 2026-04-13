@echo off
echo ============================================
echo    HealthGuard - Network Information
echo ============================================
echo.
echo Your website is now accessible on the network!
echo.
ipconfig | findstr /R /C:"IPv4 Address"
echo.
echo If you see multiple IP addresses above, use the one that
echo starts with 192.168. or 10. or 172.
echo.
echo Example: If your IP is 192.168.1.100, share:
echo http://192.168.1.100:5000
echo.
echo To make it accessible over the internet:
echo 1. Download ngrok: https://ngrok.com/download
echo 2. Run: ngrok http 5000
echo 3. Share the generated https:// URL
echo.
pause