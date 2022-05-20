import os
from pickle import GLOBAL
import subprocess
import sqlite3
import requests
import getpass
import re

### SCRIPT IS FAR FROM COMPLETED, THIS SCRIPT DOES NOT GIVE AUTO PRIVESC YET, JUST BEING WORKED ON ###

global PVULN
PVULN = 0

def linux_main():
    print('Running for linux')
    get_sudoers()
    get_services()
    check_for_running_scripts()


def windows_main():
    print('Running for windows')
    get_sudoers()
    get_services()

def mac_main():
    print('Running for mac')
    get_sudoers()
    get_services()

def set_auto_start():
    if os.path.isdir('/home/{0}/.config/autostart-scripts'.format(getpass.getuser())):
        for item in os.listdir('/home/{0}/.config/autostart-scripts'.format(getpass.getuser())):
            print(item)
            print(os.access('/home/{0}/.config/autostart-scripts'.format(getpass.getuser()), os.W_OK))
            f = open('/home/{0}/.config/autostart-scripts/{1}'.format(getpass.getuser(), item), 'r')
            for line in f:
                print(line)
                if 'sudo' in line:
                    print('wegotsudo')

#   CHECK THE COMMAND HISTORY AND LOOK FOR VULNERABLITY OR CREDS
def check_cmd_history():
    FINDS = []

    HISTORY = open('/home/{0}/.bash_history'.format(getpass.getuser()), 'r')
    for line in HISTORY:
        if 'sudo' in line:
            FINDS.append(line[:-1])
    for line in HISTORY:
        if 'ssh' in line:
            FINDS.append(line[:-1])
    for line in HISTORY:
        if 'su' in line:
            FINDS.append(line[:-1])
    for line in HISTORY:
        if 'mysql' in line:
            FINDS.append(line[:-1])


    for find in FINDS:
        print(find)

#   CHECK SUDOERS FOR VULNERABILITYS
def get_sudoers():
    global PVULN
    FINDS = []
    SUDOERS_LINES = []

#   REGULAR EXPRESSION VARIABLES TO FIND VULNERABLE SCRIPTS/FILES THAT HAVE SUDO ACCESS WITH NO PASSWD NEEDED   #
    RE_SH = re.compile(r'\(ALL\) NOPASSWD:.(.*.sh)')
    RE_PY = re.compile(r'\(ALL\) NOPASSWD:.(.*.py)')
    RE_ALL1 = re.compile(r'(\(ALL : ALL\) NOPASSWD: ALL)')
    RE_ALL2 = re.compile(r'(\(ALL\) NOPASSWD: ALL)')
    
    proc = subprocess.Popen(['sudo', '-l'], stdout=subprocess.PIPE, encoding='utf8')
    sudoers = proc.stdout.readlines()
    for line in sudoers:
        SUDOERS_LINES.append(line[:-1].strip())

    for item in SUDOERS_LINES:
        if RE_SH.match(item):
            FINDS.append(RE_SH.findall(item))
            print('Vulnertability found in sudoers file')
            PVULN += 1

    for item in SUDOERS_LINES:
        if RE_PY.match(item):
            FINDS.append(RE_PY.findall(item))
            print('Vulnertability found in sudoers file')
            PVULN += 1 

    for item in SUDOERS_LINES:
        print(item)
        if RE_ALL1.match(item):
            FINDS.append(RE_ALL1.findall(item))    
            print('Vulnertability found in sudoers file')
            PVULN += 1
            
    print(len(FINDS))    

#   IF YOU HAVE 1 OR MORE FINDS IN SUDOERS, SEE IF ANY COMMANDS ARE ABLE TO BE USED TO GET ROOT, OR
    if len(FINDS) >= 1:
        for directory in FINDS:
            print(directory[0])
            if os.access(directory[0], os.W_OK):
                print('is writable')
                PVULN += 1

###
def get_services():
    global PVULN
    ROOT_SERVICES = []
    RE_DIR = re.compile(r'.* (/.*)')

    proc = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, encoding='utf8')
    sudoers = proc.stdout.readlines()
    for line in sudoers:
        if line[0:4] == 'root':
            ROOT_SERVICES.append(line[:-1])
    for i in ROOT_SERVICES:
        if RE_DIR.match(i):
            if RE_DIR.findall(i)[0][-3:] == '.sh':
                print(RE_DIR.findall(i)[0])
                if os.access(RE_DIR.findall(i)[0], os.W_OK):
                    print('writable')
                    PVULN += 1
                    
            if RE_DIR.findall(i)[0][-3:] == '.py':
                print(RE_DIR.findall(i)[0])
                if os.access(RE_DIR.findall(i)[0], os.W_OK):
                    print('writable')
                    PVULN += 1

            if RE_DIR.findall(i)[0][-5:] == '.bash':
                print(RE_DIR.findall(i)[0])
                if os.access(RE_DIR.findall(i)[0], os.W_OK):
                    print('writable')
                    PVULN += 1

def check_for_running_scripts():
    print('checking for scripts running as admin')

    proc = subprocess.Popen(['ps', '-u', 'root','aux'], stdout=subprocess.PIPE, encoding='utf8')
    proc2 = subprocess.Popen(['grep', '.py'], stdin=proc.stdout,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sudoers = proc2.stdout.readlines()
    for line in sudoers:
        print(line)

def check_kernel():
    print('checking kernel')
    

def check_systemd():
    print('checking kernel')
    #systemctl list-timers --all

def offline_creack():
    print('offlinecrack')

def check_shells():
    print('checking for running shells')

def check_configs():
    print('checking for running shells')

def check_ssh_key():
    print('checking for running shells')

def check_all_db():
    print('checking for running shells')


def test():
    proc = subprocess.Popen(['systemctl', '--type=service'], stdout=subprocess.PIPE, encoding='utf8')
    sudoers = proc.stdout.readlines()
    for line in sudoers:
        print(line)
            

if os.uname()[0] == 'Linux':
    linux_main()
    print('currently have {0} vulnerabilitys'.format(PVULN))

