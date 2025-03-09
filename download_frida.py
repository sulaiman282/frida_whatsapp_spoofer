import requests

def download_file():
    url = "https://github.com/frida/frida/releases/download/16.0.19/frida-server-16.0.19-android-x86"
    print(f"Downloading from {url}...")
    
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        
        with open("frida-server.exe", "wb") as f:
            f.write(response.content)
        print("Successfully downloaded frida-server.exe")
        return True
    except Exception as e:
        print(f"Error downloading: {str(e)}")
        return False

if __name__ == "__main__":
    download_file()
