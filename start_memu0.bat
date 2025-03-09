@echo off
echo Starting MEmu Instance 0...
cd /d "E:\Microvirt\MEmu"
taskkill /F /IM MEmu.exe 2>nul
taskkill /F /IM adb.exe 2>nul
timeout /t 5
start MEmu.exe index=0
timeout /t 30
echo Ensuring network connectivity...
adb connect 127.0.0.1:21503
timeout /t 2
adb shell settings put global airplane_mode_on 0
adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
timeout /t 2

:: Start capturing WhatsApp logs
start cmd /k "E:\Microvirt\MEmu\adb.exe logcat | findstr "WhatsApp""

cd /d "C:\Users\Administrator\Desktop\Firda Automation for whatsapp login"
python whatsapp_spoofer.py 0
