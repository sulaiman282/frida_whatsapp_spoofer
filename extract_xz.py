import lzma
import sys

with lzma.open('frida-server/frida-server.xz', 'rb') as f_in:
    with open('frida-server/frida-server', 'wb') as f_out:
        f_out.write(f_in.read())
