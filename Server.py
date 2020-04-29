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
    print('[+] Receiving data...')
    f = open(filename, 'wb')
    data = conn.recv(4096)
    while True:
        f.write(data)
        data = conn.recv(4096)
        if not data:
            break
    f.close()
    print("[+] Done")

def Receive(conn):
        print("[+] Waiting for file...")
        info = conn.recv(1024).decode()
        filename, filesize = info.split('<SEPARATOR>')
        print('[+] Connected to ', addr)
        if '\\' in filename:
            t = filename.split('\\')
            filename = str(t[len(t)-1])
        print("File name: " + filename)
        print("Size: " + humanize.naturalsize(filesize))

        while True:
            i = input("Receive the file? [Y/n] (Default Y) > ")
            if i.lower()=='y' or i=='':
                conn.sendall('y'.encode())
                ReceiveOp(filename, conn)
                break
            elif i.lower()=='n':
                conn.sendall('n'.encode())
                break
def SendOp(filename):
    print("[+] Sending file...")
    f = open(filename, 'rb')
    data = f.read(4096)
    while True:
        conn.sendall(data)
        data = f.read(4096)
        if not data:
            break
    time.sleep(1)

    conn.send("Love".encode())
    f.close()
    print("[+] Done")

def Send(conn):
    listdir = os.listdir('./')
    strFile = ''
    files = []
    k=0
    print("List:")
    for i in listdir:
        if os.path.isfile(i):
            files.append(i)
    for i in files:
        print(str(k) + '. ' + str(i))
        strFile = strFile + str(k) + '. ' + i + '\n'
        k+=1
    conn.send(strFile.encode())
    print('[+] Waiting for client input...')
    while True:
        c = conn.recv(1024).decode()
        print("-> Client: " + c)
        try:
            c = int(c)
        except:
            conn.send("Not a number".encode())
            continue
        if 0<=c and c<k:
            conn.send('ok'.encode())
            break
        else:
            conn.send('Wrong index'.encode())
    conn.send(files[c].encode())
    SendOp(files[c])
        

print("[+] Server ip: " + LOCAL_IP)
 
if __name__=='__main__':
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            print()
            print('[+] Incoming connection: ', addr)
            conn.send("1. Send Fild\n2. Get File\n3. Exit from server".encode())
            try:
                while True:
                    c = conn.recv(1024).decode()
                    if c=='1':
                        print("Option 1: Get a file")
                        Receive(conn)
                        break
                    elif c=='2':
                        print("Option 2: Send a file")
                        Send(conn)
                        break
                    elif c=='3':
                        pass
                        break
            except:
                print("Client disconnected")
            print("[+] Connection closed")

