from io import BufferedWriter
from socket import socket

total_b_written = 0

def write(data: bytes, file: BufferedWriter):
    global total_b_written
    b_written = file.write(data)
    total_b_written+=b_written
    output_b_written()

def output_b_written():
    global total_b_written
    mb_written = total_b_written/1048576
    print("\033[95m==> Read: "+str(mb_written)+" mb.")

def download(s: socket, filepath: str, username: str, password: str, saveTo: str):
    f = open(saveTo,'wb')
    s.send(b"TYPE_LOGIN:"+bytes(username, 'utf-8')+b":"+bytes(password, 'utf-8')+b"\n")
    s.recv(1024)
    s.send(b"TYPE_GET:"+ bytes(filepath, 'utf-8') +b"\n")
    while True:
        l = s.recv(1024)
        while (l):
            if l.find(b"TYPE_END_RESPONSE") != -1:
                write(l[0:l.find(b"TYPE_END_RESPONSE")], f)
                f.close()
                print("Done Receiving")
                return
            if l.find(b"TYPE_START_RESPONSE") != -1:
                print("Starting to recieve data...")
                v = b''.join(l.split(bytes("\n", "utf-8"))[1:])
                write(v,f)
            else: 
                write(l,f)
            l = s.recv(1024)