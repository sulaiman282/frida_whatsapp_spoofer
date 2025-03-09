# WhatsApp Device Identity Spoofer

A powerful Python-based tool for managing WhatsApp automation with advanced device identity spoofing capabilities. This tool helps in managing multiple WhatsApp instances on MEmu emulator while maintaining unique device identities.

## 🚀 Features

- **Advanced Device Spoofing**
  - Generate realistic device identities (IMEI, Android ID, Serial Number)
  - Spoof device model, manufacturer, and brand
  - Maintain consistent device properties across sessions
  - Bypass device fingerprinting

- **WhatsApp Lifecycle Management**
  - Automated installation and setup
  - Clean data management
  - Permission handling
  - Anti-detection measures

- **Multi-Instance Support**
  - Support for multiple MEmu instances
  - Individual device identity per instance
  - Parallel operation capability

- **Monitoring and Debugging**
  - Real-time activity monitoring
  - Device property verification
  - Permission status tracking
  - Memory usage analysis

## 📋 Prerequisites

- Python 3.8+
- MEmu Android Emulator
- ADB (Android Debug Bridge)
- Frida

## 🛠️ Required Packages

```bash
pip install -r requirements.txt
```

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/sulaiman282/frida_whatsapp_spoofer.git
cd frida_whatsapp_spoofer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MEmu:
- Install MEmu Android Emulator
- Create required instances (0-5)
- Enable ADB debugging in each instance

## 💻 Usage

1. Start a MEmu instance:
```bash
start_memu0.bat  # For instance 0
start_memu1.bat  # For instance 1
# ... and so on
```

2. The script will:
- Generate a new device identity
- Clear existing WhatsApp data
- Apply spoofing protections
- Start WhatsApp fresh
- Monitor the process

## 🔍 Device Identity Management

The tool manages several device properties:
- IMEI (International Mobile Equipment Identity)
- Android ID
- Serial Number
- Build Fingerprint
- Device Model
- Manufacturer
- Brand

## ⚙️ Configuration

Each instance can be configured with specific device profiles in the batch files:
```bash
python whatsapp_spoofer.py [instance_number]
```

## 📱 Supported Devices

The tool can emulate various Android devices including:
- Samsung Galaxy Series
- Google Pixel Series
- OnePlus Devices
- And more...

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Users are responsible for:
- Complying with WhatsApp's Terms of Service
- Following local laws and regulations
- Using the tool responsibly and ethically

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- MEmu Android Emulator team
- Frida development team
- Python community

## 📞 Support

For issues and feature requests, please use the GitHub issue tracker.
"# frida_whatsapp_spoofer" 
"# frida_whatsapp_spoofer" 
