import socket
import time
import os

HOST = '127.0.0.1'
PORT = 60001
SEPARATOR = '<SEPARATOR>'
while True:
    filename = input("Path to file (include file name) - e.g: C:\\note.txt\n>")
    if os.path.isfile(filename):
        break
    else:
        print("Cannot find the specified file!")
filesize = os.path.getsize(filename)

def SendOp(s):
    print("[+] Sending file...")
    f = open(filename, 'rb')
    t = f.read()
    while t:
        s.send(t)
        t = f.read(4096)
    f.close()
    print("[+] Done")
        
def Send():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[+] Connecting to {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print(f"[+] Connected successfully!")
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        print("[+] Waiting for server\'s reply...")
        while True:
            c = s.recv(1024).decode()
            if c=='y' or c=='n':
                break
        if c=='y':
            print("[+] Server Accept!")
            SendOp(s)
        else:
            print("[+] Server denied!")
            time.sleep(1.5)

if __name__=='__main__':
    Send()
