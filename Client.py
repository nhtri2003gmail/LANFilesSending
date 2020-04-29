import socket
import time
import os
import sys

HOST = '127.0.0.1'
PORT = 60001
SEPARATOR = '<SEPARATOR>'

def GetFileName():
    while True:
        filename = input("Path to file (include file name) - e.g: C:\\note.txt\n> ")
        if os.path.isfile(filename):
            break
        else:
            print("Cannot find the specified file!")
    filesize = os.path.getsize(filename)
    return [filename, filesize]

def SendOp(s):
    print("[+] Sending file...")
    f = open(filename, 'rb')
    t = f.read(4096)
    while t:
        s.send(t)
        t = f.read(4096)
        if not t:
            break
    f.close()
    print("[+] Done")
        
def Send(f, filename, filesize):
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
def ReceiveOp(s):
    filename = s.recv(1024).decode()
    print(filename)
    print('[+] Receiving data...')
    with open(filename, 'wb') as f:
        while True:
            t = s.recv(4096)
            try:
                if t==b'Love':
                    break
            except:
                pass
            f.write(t)
    print("[+] Done")


def Receive(s):
    file = s.recv(1024)
    print(file.decode())
    while True:
        m = input("Index number > ")
        if m=='':
            continue
        s.send(m.encode())
        r = s.recv(1024).decode()
        if r=='ok':
            break
        print(r)
    ReceiveOp(s)

if __name__=='__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[+] Connecting to {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print(f"[+] Connected successfully!")
        print(s.recv(1024).decode())
        while True:
            c = input("> ")
            if c=='1' or c=='2' or c=='3':
                break
        s.send(c.encode())
        if c=='1':
            filename, filesize = GetFileName()
            Send(s, filename, filesize)
        elif c=='2':
            Receive(s)
    print("Disconnected")
