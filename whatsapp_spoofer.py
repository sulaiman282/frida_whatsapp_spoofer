import json
import random
import time
import os
import subprocess
import re
import sys
import signal
from datetime import datetime
import string

class DeviceSpoofer:
    @staticmethod
    def generate_imei():
        """Generate a valid IMEI number"""
        def luhn_checksum(digits):
            def digits_of(n): return [int(d) for d in str(n)]
            digits = digits_of(digits)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10

        def generate_imei_str():
            # Generate the first 14 digits
            imei = ''.join([str(random.randint(0, 9)) for _ in range(14)])
            # Calculate the check digit
            check_digit = (10 - luhn_checksum(int(imei) * 10)) % 10
            return imei + str(check_digit)

        return generate_imei_str()

    @staticmethod
    def generate_android_id():
        """Generate random Android ID"""
        return ''.join(random.choices('0123456789abcdef', k=16))

    @staticmethod
    def generate_device_props():
        """Generate random device properties"""
        devices = [
            {
                "brand": "samsung",
                "manufacturer": "samsung",
                "model": "SM-S918B",
                "product": "x1s",
                "device": "x1s",
                "board": "universal2100",
                "hardware": "s5e9925",
                "fingerprint": "samsung/x1sxxx/x1s:12/SP1A.210812.016/G991BXXU3BULD:user/release-keys"
            },
            {
                "brand": "samsung",
                "manufacturer": "samsung",
                "model": "SM-G998B",
                "product": "y2s",
                "device": "y2s",
                "board": "universal2100",
                "hardware": "s5e9925",
                "fingerprint": "samsung/y2sxxx/y2s:12/SP1A.210812.016/G998BXXU3BULD:user/release-keys"
            },
            {
                "brand": "POCO",
                "manufacturer": "xiaomi",
                "model": "POCO F5",
                "product": "marble",
                "device": "marble",
                "board": "taro",
                "hardware": "qcom",
                "fingerprint": "POCO/marble_global/marble:13/SKQ1.230401.001/V14.0.4.0.TMRMIXM:user/release-keys"
            }
        ]
        return random.choice(devices)

    @staticmethod
    def generate_phone_info():
        """Generate random phone information"""
        return {
            "line1Number": "",  # Empty for security
            "networkOperator": random.choice(["40102", "40103", "40104"]),
            "networkOperatorName": random.choice(["Airtel", "Vi", "Jio"]),
            "networkType": random.choice([13, 20]),  # LTE or 5G
            "phoneType": 1,  # GSM
            "simOperator": random.choice(["40102", "40103", "40104"]),
            "simOperatorName": random.choice(["Airtel", "Vi", "Jio"]),
            "simSerialNumber": ''.join(random.choices('0123456789ABCDEF', k=20)),
            "subscriptionId": random.randint(1, 999999)
        }

    @staticmethod
    def generate_build_props():
        """Generate random build properties"""
        return {
            "BOOTLOADER": f"G998BXXU3BUL{random.randint(1,9)}",
            "RADIO": f"G998BXXU3BUL{random.randint(1,9)}",
            "SERIAL": ''.join(random.choices('0123456789ABCDEF', k=16)),
            "TIME": int(time.time() * 1000),
            "TYPE": "user",
            "TAGS": "release-keys",
            "SDK": random.choice([31, 32, 33]),  # Android 12, 12L, 13
            "INCREMENT": f"BUL{random.randint(1,9)}",
            "ID": f"SP1A.{random.randint(200000,210000)}.{random.randint(1,999)}"
        }

class DeviceAutomation:
    def __init__(self):
        self.adb_path = "E:\\Microvirt\\MEmu\\adb.exe"
        self.frida_path = ".\\frida-gumjs-devkit-16.6.6-windows-x86_64.exe"
        self.spoofer = DeviceSpoofer()
        self.device_props = self.spoofer.generate_device_props()
        self.build_props = self.spoofer.generate_build_props()
        self.phone_info = self.spoofer.generate_phone_info()
        self.android_id = self.spoofer.generate_android_id()
        self.imei = self.spoofer.generate_imei()

    def get_frida_script(self):
        """Generate Frida script with all spoofing protections"""
        script = """
        Java.perform(function() {
            try {
                // Basic Android Properties
                var Build = Java.use('android.os.Build');
                Build.FINGERPRINT.value = "%s";
                Build.MODEL.value = "%s";
                Build.MANUFACTURER.value = "%s";
                Build.BRAND.value = "%s";
                Build.PRODUCT.value = "%s";
                Build.DEVICE.value = "%s";
                Build.BOARD.value = "%s";
                Build.HARDWARE.value = "%s";
                Build.BOOTLOADER.value = "%s";
                Build.SERIAL.value = "%s";
                
                // System Properties Hook
                var SystemProperties = Java.use('android.os.SystemProperties');
                var propsToSpoof = {
                    "ro.build.fingerprint": "%s",
                    "ro.product.model": "%s",
                    "ro.product.manufacturer": "%s",
                    "ro.product.brand": "%s",
                    "ro.product.name": "%s",
                    "ro.product.device": "%s",
                    "ro.product.board": "%s",
                    "ro.hardware": "%s",
                    "ro.bootloader": "%s",
                    "ro.serialno": "%s",
                    "ro.build.id": "%s",
                    "gsm.sim.operator.numeric": "%s",
                    "gsm.operator.numeric": "%s"
                };

                SystemProperties.get.overload('java.lang.String').implementation = function(key) {
                    if (key in propsToSpoof) return propsToSpoof[key];
                    if (key.includes("qemu") || key.includes("generic")) return null;
                    return this.get.call(this, key);
                };

                // Telephony Spoofing
                var TelephonyManager = Java.use('android.telephony.TelephonyManager');
                TelephonyManager.getDeviceId.overload().implementation = function() {
                    return "%s";  // IMEI
                };
                TelephonyManager.getSimOperatorName.overload().implementation = function() {
                    return "%s";
                };
                TelephonyManager.getSimOperator.overload().implementation = function() {
                    return "%s";
                };
                TelephonyManager.getNetworkOperatorName.overload().implementation = function() {
                    return "%s";
                };

                // Android ID Spoofing
                var Secure = Java.use('android.provider.Settings$Secure');
                Secure.getString.implementation = function(cr, name) {
                    if (name === "android_id") return "%s";
                    return this.getString.call(this, cr, name);
                };

                // Anti-Detection Measures
                var File = Java.use('java.io.File');
                File.exists.implementation = function() {
                    var fileName = this.getAbsolutePath();
                    if (fileName.includes("qemu") || fileName.includes("goldfish") || 
                        fileName.includes("nox") || fileName.includes("memu")) {
                        return false;
                    }
                    return this.exists.call(this);
                };

                // Package Manager Hook
                var ApplicationPackageManager = Java.use('android.app.ApplicationPackageManager');
                ApplicationPackageManager.getInstalledApplications.implementation = function() {
                    var result = this.getInstalledApplications.call(this);
                    return result.filter(function(app) {
                        return !app.packageName.value.includes("com.android.vending");
                    });
                };

                // WebView Protection
                var WebView = Java.use('android.webkit.WebView');
                WebView.getSettings.implementation = function() {
                    var settings = this.getSettings.call(this);
                    settings.setUserAgentString("Mozilla/5.0 (Linux; Android 12; SM-S918B Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36");
                    return settings;
                };

                console.log("[+] Anti-detection hooks installed successfully");
            } catch (e) {
                console.log("[!] Error: " + e);
            }
        });
        """ % (
            self.device_props["fingerprint"], self.device_props["model"],
            self.device_props["manufacturer"], self.device_props["brand"],
            self.device_props["product"], self.device_props["device"],
            self.device_props["board"], self.device_props["hardware"],
            self.build_props["BOOTLOADER"], self.build_props["SERIAL"],
            self.device_props["fingerprint"], self.device_props["model"],
            self.device_props["manufacturer"], self.device_props["brand"],
            self.device_props["product"], self.device_props["device"],
            self.device_props["board"], self.device_props["hardware"],
            self.build_props["BOOTLOADER"], self.build_props["SERIAL"],
            self.build_props["ID"], self.phone_info["simOperator"],
            self.phone_info["networkOperator"], self.imei,
            self.phone_info["simOperatorName"], self.phone_info["simOperator"],
            self.phone_info["networkOperatorName"], self.android_id
        )
        return script

    def apply_device_props(self):
        """Apply device properties using setprop"""
        try:
            print("[*] Applying device properties...")
            # Set model, manufacturer, brand
            subprocess.run([self.adb_path, "shell", f"setprop ro.product.model '{self.device_props['model']}'"], capture_output=True)
            subprocess.run([self.adb_path, "shell", f"setprop ro.product.manufacturer '{self.device_props['manufacturer']}'"], capture_output=True)
            subprocess.run([self.adb_path, "shell", f"setprop ro.product.brand '{self.device_props['brand']}'"], capture_output=True)
            
            # Set Android ID
            subprocess.run([self.adb_path, "shell", f"settings put secure android_id {self.android_id}"], capture_output=True)
            
            # Set serial number (more realistic format)
            serial = f"R{random.choice('ABCDEFGHIJKLMNOP')}{random.randint(10000000, 99999999)}"
            subprocess.run([self.adb_path, "shell", f"setprop ro.serialno '{serial}'"], capture_output=True)
            subprocess.run([self.adb_path, "shell", f"setprop ro.boot.serialno '{serial}'"], capture_output=True)
            
            # Set build fingerprint
            fingerprint = f"{self.device_props['brand']}/{self.device_props['model']}/arm64:13/TP1A.220624.014"
            subprocess.run([self.adb_path, "shell", f"setprop ro.build.fingerprint '{fingerprint}'"], capture_output=True)
            
            # Additional device properties
            subprocess.run([self.adb_path, "shell", "setprop ro.build.characteristics 'default'"], capture_output=True)
            subprocess.run([self.adb_path, "shell", "setprop ro.build.description 'release-keys'"], capture_output=True)
            subprocess.run([self.adb_path, "shell", f"setprop ro.product.device '{self.device_props['model'].lower()}'"], capture_output=True)
            
            # Set IMEI (requires root, may not work on all devices)
            try:
                subprocess.run([self.adb_path, "shell", f"service call iphonesubinfo 1 s16 {self.imei}"], capture_output=True)
            except:
                pass
                
            return True
        except Exception as e:
            print(f"[-] Error applying device properties: {str(e)}")
            return False

    def ensure_whatsapp_lifecycle(self):
        """Ensure proper WhatsApp lifecycle"""
        try:
            print("[*] Managing WhatsApp lifecycle...")
            
            # Kill any existing WhatsApp process
            subprocess.run([self.adb_path, "shell", "am force-stop com.whatsapp"], capture_output=True)
            time.sleep(1)
            
            # Apply device properties before starting WhatsApp
            self.apply_device_props()
            
            # Clear all WhatsApp data
            subprocess.run([self.adb_path, "shell", "pm clear com.whatsapp"], capture_output=True)
            
            # Remove WhatsApp directories
            subprocess.run([self.adb_path, "shell", "rm -rf /sdcard/WhatsApp"], capture_output=True)
            subprocess.run([self.adb_path, "shell", "rm -rf /sdcard/Android/media/com.whatsapp"], capture_output=True)
            subprocess.run([self.adb_path, "shell", "rm -rf /sdcard/Android/data/com.whatsapp"], capture_output=True)
            
            # Clear package manager data
            subprocess.run([self.adb_path, "shell", "pm clear com.android.packageinstaller"], capture_output=True)
            
            # Clear Google Play Services data
            subprocess.run([self.adb_path, "shell", "pm clear com.google.android.gms"], capture_output=True)
            
            # Apply device properties again after clearing data
            self.apply_device_props()
            
            # Start WhatsApp fresh
            subprocess.run([self.adb_path, "shell", "monkey -p com.whatsapp 1"], capture_output=True)
            time.sleep(3)

            # Monitor initial state
            print("\n[*] Checking WhatsApp state after fresh start:")
            self.monitor_whatsapp_activity()
            
            return True
        except Exception as e:
            print(f"[-] Error in WhatsApp lifecycle: {str(e)}")
            return False

    def handle_ui_flow(self):
        """Handle the WhatsApp UI flow"""
        try:
            print("[*] Starting UI automation...")
            time.sleep(2)  # Wait for app to start
            
            # Monitor WhatsApp state before UI interaction
            print("\n[*] WhatsApp state before UI interaction:")
            self.monitor_whatsapp_activity()
            
            # Check for spam screen
            cmd = [self.adb_path, "shell", "uiautomator dump"]
            subprocess.run(cmd, capture_output=True)
            
            cmd = [self.adb_path, "shell", "cat /sdcard/window_dump.xml"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "This account can no longer use WhatsApp due to spam" in result.stdout:
                print("[!] Spam screen detected, restarting...")
                return False
            
            # Click "Agree and continue"
            if self.click_element(text="Agree and continue") or self.click_element(text="AGREE AND CONTINUE"):
                time.sleep(1)
                # Monitor state after clicking agree
                print("\n[*] WhatsApp state after clicking agree:")
                self.monitor_whatsapp_activity()
            
            # Wait for phone number screen
            time.sleep(2)
            print("[*] Ready for manual phone number entry")
            print(f"[*] Using device: {self.device_props['model']} ({self.device_props['brand']})")
            print(f"[*] IMEI: {self.imei}")
            print(f"[*] Android ID: {self.android_id}")

            # Final state check
            print("\n[*] Final WhatsApp state:")
            self.monitor_whatsapp_activity()
            
            return True
            
        except Exception as e:
            print(f"[-] Error in UI flow: {str(e)}")
            return False

    def monitor_whatsapp_activity(self):
        """Monitor WhatsApp activity and log important events"""
        try:
            # Get current activity
            result = subprocess.run([self.adb_path, "shell", "dumpsys activity activities | grep mResumedActivity"],
                                  capture_output=True, text=True)
            current_activity = result.stdout.strip()
            print(f"[*] Current Activity: {current_activity}")

            # Get WhatsApp process info
            result = subprocess.run([self.adb_path, "shell", "ps -A | grep whatsapp"],
                                  capture_output=True, text=True)
            process_info = result.stdout.strip()
            print(f"[*] WhatsApp Process: {process_info}")

            # Check if our spoofing is active
            result = subprocess.run([self.adb_path, "shell", "getprop | grep -e ro.product.model -e ro.serialno -e android_id"],
                                  capture_output=True, text=True)
            device_props = result.stdout.strip()
            print(f"[*] Device Properties:\n{device_props}")

            # Check memory usage
            result = subprocess.run([self.adb_path, "shell", "dumpsys meminfo com.whatsapp"],
                                  capture_output=True, text=True)
            memory_info = result.stdout.strip()
            print(f"[*] Memory Usage:\n{memory_info[:500]}...")  # Show first 500 chars

            # Check permissions
            result = subprocess.run([self.adb_path, "shell", "dumpsys package com.whatsapp | grep permission"],
                                  capture_output=True, text=True)
            permissions = result.stdout.strip()
            print(f"[*] Permissions:\n{permissions}")

            return True
        except Exception as e:
            print(f"[-] Error monitoring WhatsApp: {str(e)}")
            return False

    def click_element(self, text=None, resource_id=None, content_desc=None, class_name=None):
        """Click an element based on various attributes"""
        try:
            cmd = [self.adb_path, "shell", "uiautomator dump"]
            subprocess.run(cmd, capture_output=True)
            
            cmd = [self.adb_path, "shell", "cat /sdcard/window_dump.xml"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if text and text in result.stdout:
                # Try to find the element's coordinates
                match = re.search(f'text="{text}"[^>]+bounds="\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]"', result.stdout)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())
                    tap_x = (x1 + x2) // 2
                    tap_y = (y1 + y2) // 2
                else:
                    # Fallback to center of screen
                    tap_x, tap_y = 540, 1000
                
                cmd = [self.adb_path, "shell", f"input tap {tap_x} {tap_y}"]
                subprocess.run(cmd)
                return True
            
            return False
        except Exception as e:
            print(f"[-] Error clicking element: {str(e)}")
            return False

    def install_frida(self):
        """Install Frida on device"""
        try:
            print("[*] Installing Frida...")
            # Push Frida to device
            subprocess.run([self.adb_path, "push", self.frida_path, "/data/local/tmp/frida-server"])
            subprocess.run([self.adb_path, "shell", "chmod 755 /data/local/tmp/frida-server"])
            
            # Start Frida
            subprocess.Popen([self.adb_path, "shell", "/data/local/tmp/frida-server &"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[-] Error installing Frida: {str(e)}")
            return False

    def clear_whatsapp_data(self):
        """Clear WhatsApp data completely"""
        try:
            print("[*] Clearing WhatsApp data...")
            subprocess.run([self.adb_path, "shell", "pm clear com.whatsapp"], capture_output=True)
            # Also clear any WhatsApp folders
            subprocess.run([self.adb_path, "shell", "rm -rf /sdcard/WhatsApp"], capture_output=True)
            subprocess.run([self.adb_path, "shell", "rm -rf /sdcard/Android/media/com.whatsapp"], capture_output=True)
            return True
        except Exception as e:
            print(f"[-] Error clearing data: {str(e)}")
            return False

    def start_whatsapp(self):
        """Start WhatsApp with new identity"""
        try:
            print("[*] Starting WhatsApp...")
            # Kill any existing WhatsApp process
            subprocess.run([self.adb_path, "shell", "am force-stop com.whatsapp"], capture_output=True)
            time.sleep(1)
            subprocess.run([self.adb_path, "shell", "monkey -p com.whatsapp 1"], capture_output=True)
            return True
        except Exception as e:
            print(f"[-] Error starting WhatsApp: {str(e)}")
            return False

def main():
    print("[*] Starting WhatsApp Automation System...")
    device = DeviceAutomation()
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n[*] Cleaning up...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Install Frida first
    if not device.install_frida():
        print("[-] Failed to install Frida")
        return
    
    while True:
        # Clear and start WhatsApp
        device.ensure_whatsapp_lifecycle()
        if not device.start_whatsapp():
            print("[-] Failed to start WhatsApp")
            continue
        
        # Handle UI flow
        if not device.handle_ui_flow():
            print("[-] UI flow failed, restarting...")
            continue
        
        try:
            input("[*] Press Enter to reset WhatsApp with new device identity (Ctrl+C to exit)...")
        except KeyboardInterrupt:
            print("\n[*] Cleaning up...")
            break

if __name__ == "__main__":
    main()
