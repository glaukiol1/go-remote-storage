# virtual shell
import json
from pprint import pprint
from socket import socket
from time import sleep, time


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

class vfs:
    current_dir = ""
    vfs = []


def vhs():
    print(CLEAR)
    print(BOLD+HEADER+"==> Starting VHS..."+ENDC)
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
    s.close()
    print("\n")
    print(FAIL+BOLD+"==> Debug Mode: Send commands directly to the server.\n\tYou would need to know all the key's and seperators for the TCP server.\n\tOnly for debug purposes!\n\t"+WARNING+UNDERLINE+"NOT RECOMMENDED\n")
    print(ENDC+OKGREEN+BOLD+"==> User Mode: Use the VSH, which will give a shell-like experience.\n\t"+"a simpe virutal shell, consisting of typical commands such as:\n\t"+"- ls - cd - download - send -\n\t"+WARNING+UNDERLINE+"RECOMMENDED\n")
    
    user_mode = input(ENDC+OKGREEN+"==> Enter user mode? (y/n) ")
    print(ENDC+"\n")
    if user_mode == "n":
        vhs_debug(s)
    else: nrml_vhs(srv_ip,port)
    print(ENDC)

def vhs_debug(s: socket):
    while True:
        cmd = input("==> Command (debug mode!): ")
        s.send( bytes(cmd, "utf-8")+b"\n" )
        s.recv(1024)
        sleep(5)

def login(s: socket) -> str:
    username = input(OKBLUE+BOLD+"Enter username: ")
    password = input("Enter Password: ")
    print(ENDC)
    return lgin(s, username, password)

def lgin(s: socket, username,password) -> str:
        cmd = bytes("TYPE_LOGIN:"+username+":"+password+"\n", "utf-8")
        s.send(cmd)
        if str(s.recv(1024)).find("TYPE_SUCCESS") != -1:
            print(OKGREEN+BOLD+"Successfully logged in"+ENDC)
            vfs.current_dir = "./"
        else:
            print(FAIL+BOLD+"Failed to login."+ENDC)

def ls(s: socket, searchfor):
    cmd = bytes(searchfor, "utf-8")
    s.sendall(cmd)
    sleep(0.5)
    l = s.recv(1024)
    if l.find(b"TYPE_UNKNOWN_ERROR") != -1 or l.find(b"TYPE_ERROR") != -1:
        print(FAIL+"Server error! Failed..."+ENDC)
    else:
        if str(l).find("TYPE_NO_FILES") != -1:
            return []
        else:
            json_obj = str(l).replace("\n", "").replace(" ", "").replace("b", "", 1).replace("'","").split("\\n")
            parsed_obj = []
            for jobj in json_obj:
                if len(jobj) != 0:
                    parsed_obj.append(json.loads(jobj))
            return parsed_obj

def indexvdir(s, path:str):
    searchfor = "CMD_LS:"+path+"\n"
    json_dir = ls(s, searchfor)
    i = pathIsIndexed(path)
    if i != -1:
        vfs.vfs[i] = {
            "path": path,
            "data": json_dir
        }
    else:
        vfs.vfs.append({
            "path": path,
            "data": json_dir
        })

def outputdir(path: str):
    for vdir in vfs.vfs:
        if vdir["path"] == path:
            result = ""
            if vdir["data"] == None:
                print(WARNING+BOLD+"Something went wrong while indexing.."+ENDC)
                break
            else:
                for entry in vdir["data"]:
                    if entry["isDir"] == True:
                        result+=( HEADER+BOLD+"|"+entry["name"]+"|"+"\t"+ENDC )
                    else:
                        result+=( BOLD+"|"+entry["name"]+"|"+"\t"+ENDC )
                print(result)
                return


def pathIsIndexed(path: str) -> int:
    indx = 0
    for vdir in vfs.vfs:
        if vdir["path"] == path:
            return indx
    return -1

def cd(s: socket, path: str):
    indexvdir(s,path)
    vfs.current_dir = path

def nrml_vhs(srv_ip, port):
    s = socket()
    s.connect((srv_ip, port))
    s.settimeout(200000)
    while True:
        print(ENDC)
        cmd = input("$vfs:"+vfs.current_dir+"> ")
        if cmd.startswith("login"):
            login(s)
        elif cmd.startswith("ls"):
            if len(cmd.split(" ")) != 2:
                indexvdir(s, vfs.current_dir)
                outputdir(vfs.current_dir)
            else:
                indexvdir(s, cmd.split(" ")[1])
                outputdir(cmd.split(" ")[1])
        elif cmd.startswith("cd"):
            if len(cmd.split(" ")) != 2:
                print(WARNING+BOLD+"Warning: no path passed... will not change CWD."+ENDC)
            else:
                cd(s, cmd.split(" ")[1])
                