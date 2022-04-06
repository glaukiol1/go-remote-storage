# virtual shell
import json
import os
import posixpath
from pprint import pprint
from socket import socket
import sys
from time import sleep

from download import download


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

class globals:
    isLogged = False
    username = ""

def vhs():
    print(CLEAR)
    print(BOLD+HEADER+"==> Starting VHS..."+ENDC)
    srv_ip = input(BOLD+OKCYAN+"Server IP Address: ")
    print()
    try:
        port = int(input(BOLD+OKCYAN+"Server Port: (Default 12368) "))
    except:
        port = 12368
    print(ENDC)
    print()
    print(BOLD+WARNING+"==> Opening socket..."+ENDC)
    s = socket()
    try:
        s.connect((srv_ip,port))
    except:
        print(FAIL+BOLD+"FATAL: couldn't connect to "+str(srv_ip)+":"+str(port))
        sys.exit(1)
    
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
        vhs_debug(srv_ip,port)
    else: nrml_vhs(srv_ip,port)
    print(ENDC)

def vhs_debug(srv_ip,port):
    s = socket()
    s.connect((srv_ip, port))
    s.settimeout(200000)
    while True:
        cmd = input("==> Command (debug mode!): ")
        s.send( bytes(cmd+"\n", "utf-8") )
        l = s.recv(1024)
        while l:
            print(len(str(l)))
            print(str(l))
            l = s.recv(1024)

def login(s: socket) -> bool:
    username = input(OKBLUE+BOLD+"Enter username: ")
    password = input("Enter Password: ")
    print(ENDC)
    return lgin(s, username, password)

def lgin(s: socket, username,password) -> bool:
        cmd = bytes("TYPE_LOGIN:"+username+":"+password+"\n", "utf-8")
        s.send(cmd)
        if str(s.recv(1024)).find("TYPE_SUCCESS") != -1:
            print(OKGREEN+BOLD+"Successfully logged in"+ENDC)
            vfs.current_dir = "./"
            globals.isLogged = True
            globals.username = username
            return True
        else:
            print(FAIL+BOLD+"Failed to login."+ENDC)
            return False

def cmd_download(s: socket, filename: str):
    path = posixpath.join(vfs.current_dir, filename)
    saveto = os.path.join("recv", filename)
    download(s,path,saveto)

def cmd_rm(s: socket):
    showpath = ""
    if vfs.current_dir.endswith("/"):
        showpath = vfs.current_dir
    else:
        showpath = vfs.current_dir+"/"
    originpath = input(OKBLUE+BOLD+"What directory/file do you want to delete? "+showpath)
    sendpath = posixpath.join(vfs.current_dir, originpath)
    cmd = bytes("CMD_RM:"+sendpath+"\n", "utf-8")
    s.send(cmd)
    rsp = str(s.recv(1024))
    if rsp.find("TYPE_SUCCESS") != -1:
        print(OKGREEN+BOLD+"Successfully deleted "+OKCYAN+sendpath+ENDC)
    else:
        print(FAIL+BOLD+"Failed to delete directory... response: "+rsp)

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
    vfs.current_dir = posixpath.join(vfs.current_dir,path)

def send(s:socket):
    localsystempath = input(OKBLUE+BOLD+"Enter the full file path on your local computer: ")
    originpath = input("Enter the full path on where you want to store this file: "+vfs.current_dir+"/")
    sendpath = posixpath.join(vfs.current_dir, originpath)
    print(ENDC)
    s.send(bytes("TYPE_SEND:"+sendpath+"\n", "utf-8"))
    try:
        with open(localsystempath, "r") as file:
            bytes_file = file.buffer.read()

            split_bytes_file = [bytes_file[x:x+1024] for x in range(0, len(bytes_file), 1024)]
            sleep(1)
            for m1024bytes in split_bytes_file:
                s.send(m1024bytes)
            s.send(b"TYPE_END_RESPONSE")
            file.close()
        rsp = str(s.recv(1024))
        if rsp.find("TYPE_SUCCESS") != -1:
            print(OKGREEN+BOLD+"Success"+ENDC)
        else:
            print(FAIL+BOLD+"failed... response:", rsp)
    except OSError:
        print(FAIL+BOLD+"failed on opening local file, double check the path.")
def nrml_vhs(srv_ip, port):
    s = socket()
    s.connect((srv_ip, port))
    s.settimeout(200000)
    while True:
        print(ENDC, end="")
        if globals.isLogged == True:
            cmd = input(globals.username+"$:"+vfs.current_dir+"> ")
        else:
            cmd = input("$> ")
        if cmd.startswith("login"):
            if globals.isLogged:
                print(WARNING+BOLD+"Warning: already logged in... ignoring"+ENDC)
            else:
                success = login(s)
                if success == False:
                    s = socket()
                    s.connect((srv_ip, port))
                    s.settimeout(200000)
        elif cmd.startswith("ls"):
            try:
                if globals.isLogged == False:
                    print(FAIL+BOLD+"Error: not logged in."+ENDC)
                else:
                    if len(cmd.split(" ")) != 2:
                        indexvdir(s, vfs.current_dir)
                        outputdir(vfs.current_dir)
                    else:
                        indexvdir(s, cmd.split(" ")[1])
                        outputdir(cmd.split(" ")[1])
            except:
                print(FAIL+BOLD+"failed... cleaning up..."+ENDC)
        elif cmd.startswith("cd"):
            oldpath = vfs.current_dir
            try:
                if globals.isLogged == False:
                    print(FAIL+BOLD+"Error: not logged in."+ENDC)
                else:
                    if len(cmd.split(" ")) != 2:
                        print(WARNING+BOLD+"Warning: no path passed... will not change CWD."+ENDC)
                    else:
                        cd(s, cmd.split(" ")[1])
            except:
                print(FAIL+BOLD+"failed... cleaning up..."+ENDC)
                vfs.current_dir = oldpath
        elif cmd.startswith("cwd"):
            print(vfs.current_dir)
        elif cmd.startswith("get"):
            try:
                if len(cmd.split(" ")) == 2:
                    cmd_download(s,cmd.split(" ")[1])
                else:
                    print(WARNING+BOLD+"please pass a filename as a argument..."+ENDC)
            except:
                print(FAIL+BOLD+"failed... cleaning up..."+ENDC)
        elif cmd.startswith("send"):
            try:
                send(s)
            except:
                print(FAIL+BOLD+"failed... cleaning up..."+ENDC)
        elif cmd.startswith("rm"):
            try:
                cmd_rm(s)
            except:
                print(FAIL+BOLD+"failed... cleaning up..."+ENDC)