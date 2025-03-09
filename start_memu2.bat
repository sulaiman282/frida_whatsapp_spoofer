@echo off
echo Starting MEmu Instance 2...
cd /d "E:\Microvirt\MEmu"
taskkill /F /IM MEmu.exe 2>nul
taskkill /F /IM adb.exe 2>nul
timeout /t 2
start MEmu.exe index=2
timeout /t 30
cd /d "C:\Users\Administrator\Desktop\Firda Automation for whatsapp login"
python whatsapp_spoofer.py 2
