# Botnet

AIO Botnet/ watchdog/ server/ command and control in python, its simple and will be worked on in the future. for reverse shell
you must open your port 1337 for the time being. will include details in the future.

Watchdog:
The purpose of this watchdog is to make sure that the payload is always running.
Watch dog will can load the payload from memory, or download payload to disk and
execute ( depening on your configuration).

If the payload binary is not running and is not on the file system because it got deleated 
or somehow, watchdog will redownload and place the payload in the specified directory.

Watchdog will hide it's self from Taskmanager and removes it'self from startup folder, until
Taskmanager is closed.

Watchdog will kill the payload process from running if TaskManager is open.



# Instruction:

After extracting all the files to a folder, go into the static directory and static and create a folder called windows, and another
called linux. These folders will contain your binary/exe payload and watchdog files, so that the RAT can redownload them incase it got
removed or deleated somehow.

Go into the payload.py, watchdog.py, server.py files and change the Webserver address on each of those to your preference. Start up the server.py with python3 server.py.
Compile the watchdog.py and payload.py with your compiler of chose. Now based on the operating system you compiled the files on, place them in the
./static/<linux/windows> folder. If on linux and the binaries have the extention .bin, just remove the .bin extention.

Now upload your watchdog binary to a site and send it to a virtual-machine or another computer of your's and test it out.


FEATURES TO ADD:
  
      Macos support

      Stub creator

      GUI

      Auto-Detect taskmanager and remove self until it is closed.

      Privilege Escaltion
   
      EXE LOADER and executer

      Launch python script on the fly

      different persistance methods
      
      screenshots
      
      remotedesktop
     
     

