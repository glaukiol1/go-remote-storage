from io import BufferedWriter
import os
from socket import socket
from time import time

from encryption import decrypt_bytes

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

class globals2:
    data = b""
def write(data: bytes):
    globals2.data += data
def download(s: socket, filepath: str, saveTo: str, password: str):
    total_b_written = 0
    f = open(saveTo,'wb')
    s.send(bytes("TYPE_GET:"+filepath+"\n", 'utf-8'))
    start = time()
    while True:
        l = s.recv(1024)
        if l.find(b"TYPE_ERROR:COULDN'T ACCESS FILE") != -1:
            print(FAIL+BOLD+"server couldn't access this file."+ENDC)
            f.close()
            os.remove(saveTo)
            raise FileNotFoundError
        while (l):
            if l.find(b"TYPE_END_RESPONSE") != -1:
                write(l[0:l.find(b"TYPE_END_RESPONSE")])
                total_b_written = f.write(decrypt_bytes(globals2.data, password))/1e+6
                f.close()
                globals2.data = b""
                print(ENDC+OKGREEN+"Success: "+ENDC+"Read "+HEADER+str(total_b_written)+ENDC+" mb at "+HEADER+str(total_b_written/(time()-start))+ENDC+" mb/s")
                return
            else: 
                write(l)
            l = s.recv(1024)