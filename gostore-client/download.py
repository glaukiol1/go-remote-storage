from io import BufferedWriter
from socket import socket

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
CLEAR = "\033[H\033[2J"
total_b_written = 0

def write(data: bytes, file: BufferedWriter):
    global total_b_written
    b_written = file.write(data)
    total_b_written+=b_written

def download(s: socket, filepath: str, saveTo: str):
    global total_b_written
    f = open(saveTo,'wb')
    s.send(bytes("TYPE_GET:"+filepath+"\n", 'utf-8'))
    while True:
        l = s.recv(1024)
        if l.find(b"TYPE_ERROR:COULDN'T ACCESS FILE") != -1:
            print(FAIL+BOLD+"server couldn't access this file.")
            return
        while (l):
            if l.find(b"TYPE_END_RESPONSE") != -1:
                write(l[0:l.find(b"TYPE_END_RESPONSE")], f)
                f.close()
                print("Read "+str(total_b_written/1048576)+"mb")
                return
            if l.find(b"TYPE_START_RESPONSE") != -1:
                v = l.split(bytes("\n", "utf-8"), 1)[1]
                write(v,f)
            else: 
                write(l,f)
            l = s.recv(1024)