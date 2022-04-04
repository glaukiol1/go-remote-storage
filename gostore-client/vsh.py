# virtual shell
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

VHS_PREFIX = "$> "

def vhs():
    print(CLEAR)
    print(BOLD+HEADER+VHS_PREFIX+"Starting VHS..."+ENDC)
    srv_ip = input(BOLD+OKCYAN+"Server IP Address: ")
    print()
    port = int(input(BOLD+OKCYAN+"Server Port: (Usually 12368) "))
    print(ENDC)
    print()
    print(BOLD+WARNING+"==> Opening socket...")
    s = socket()
    s.connect((srv_ip,port))
    print()
    print(BOLD+WARNING+"==> running command... "+HEADER+"$> TYPE_ECHO:hi from vsh")
    s.send(b"TYPE_ECHO:hi from vsh\n")
    print(WARNING+BOLD+"==> response... " + HEADER + str(s.recv(1024)))
    print("\n")
    print(FAIL+BOLD+"==> Debug Mode: Send commands directly to the server.\n\tYou would need to know all the key's and seperators for the TCP server.\n\tOnly for debug purposes!\n\t"+WARNING+UNDERLINE+"NOT RECOMMENDED\n")
    print(ENDC+OKGREEN+BOLD+"==> User Mode: Use the VSH, which will give a shell-like experience.\n\t"+"a simpe virutal shell, consisting of typical commands such as:\n\t"+"- ls - cd - download - send -\n\t"+WARNING+UNDERLINE+"RECOMMENDED\n")
    
    print(ENDC)