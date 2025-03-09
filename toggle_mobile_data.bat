@echo off
title Mobile Data Toggle Script
color 0A

set DEVICE_ID=87ff4c0f

:check_device
echo Checking for connected Android device...
"E:\Microvirt\MEmu\adb.exe" devices
if errorlevel 1 (
    echo No device found! Please connect your Android device via USB...
    timeout /t 5
    goto check_device
)

:main_loop
cls
echo Mobile Data Toggle Script
echo ========================
echo.
echo Press any key to toggle mobile data (Ctrl+C to exit)
echo.
pause > nul

echo Turning mobile data OFF...
"E:\Microvirt\MEmu\adb.exe" -s %DEVICE_ID% shell svc data disable
if errorlevel 1 (
    echo Failed to disable mobile data!
    goto error
)

echo Waiting for 2 seconds...
timeout /t 2 /nobreak > nul

echo Turning mobile data ON...
"E:\Microvirt\MEmu\adb.exe" -s %DEVICE_ID% shell svc data enable
if errorlevel 1 (
    echo Failed to enable mobile data!
    goto error
)

echo Mobile data toggled successfully!
echo.
goto main_loop

:error
echo.
echo Error occurred! Please check your device connection.
timeout /t 3
goto main_loop
