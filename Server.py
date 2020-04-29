import socket
import os
import sys
import time
try:
    import humanize
except:
    os.system("pip install humanize")
    import humanize

HOST = '0.0.0.0'
PORT = 60001
LOCAL_IP = socket.gethostbyname(socket.gethostname())

def ReceiveOp(filename, conn):
    print('Receiving data...')
    f = open(filename, 'wb')
    data = conn.recv(4096)
    while data:
        f.write(data)
        data = conn.recv(4096)
    f.close()

def Receive():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()
        
        info = conn.recv(1024).decode()
        filename, filesize = info.split('<SEPARATOR>')
        print('[+] Connected to ', addr)
        print("File name: " + filename)
        print("Size: " + humanize.naturalsize(filesize))

        if '\\' in filename:
            t = filename.split('\\')
            filename = str(t[len(t)-1])
        
        while True:
            i = input("Receive the file? [Y/n] (Default Y) > ")
            if i.lower()=='y' or i=='':
                conn.sendall('y'.encode())
                ReceiveOp(filename, conn)
                break
            elif i.lower()=='n':
                conn.sendall('n'.encode())
                break


print("[+] Server ip: " + LOCAL_IP)
print()
           
if __name__=='__main__':
    Receive()
