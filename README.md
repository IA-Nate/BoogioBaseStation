# Boogio Base Station

The official Boogio Base Station open-source software codebase.


## Getting Started


### Introduction

These steps document how to operate and create a Base Station for Python development. If you've received a preconfigured base station, you can skip to the "Running the tests" section. Otherwise, keep reading!

### Operation

## Scripts
There are two scripts which you can execute by double-clicking on a file and selecting "Execute in Terminal". You may also run these scripts using the terminal to see their output.

1) ~/Desktop/download-repository.sh
DELETES the folder at /home/pi/Dev/BoogioBaseStation/ and downloads a fresh (updated) copy from github.com. Make sure to move any of your work out of the repository directories if you intend to keep your files intact.

2) ~/Dev/BoogioBaseStation/update-repository.sh
Updates the repository without deleting anything.

If you accidentally delete any of the files on the Desktop, you may find backups in the directory ~/Dev/BoogioBaseStation/CopyToDesktop/

## Writing your own scripts
To you may write and store your own scripts anywhere you like, but I recommend you create every project within a new subdirectory of /home/pi/Dev/

Copy or Write your Python scripts in the editor of your choosing while referencing the the example Python scripts and documentation stored at ~/Dev/BoogioBaseStation/


### Configuration
Open Terminal and type the following commands.

Update Keyboard configuration to your country of choice:

```
$ sudo dpkg-reconfigure keyboard-configuration

```


to reconfigure your keyboard. Choose English (US) for keyboard layout (second page of configuration). Then then reboot.

```
$ init 6
```


Update Raspbian and restart:

```
$ sudo su -
# apt-get update
# apt-get dist-upgrade -y
# init 6
```

After restarting, install bluepy: https://www.elinux.org/RPi_Bluetooth_LE
```
$ sudo apt-get install python-pip
$ sudo apt-get install libglib2.0-dev -y
$ sudo pip install bluepy
```

Clone the Boogio Base Station Repo

```
$ cd ~/
$ mkdir Dev
$ cd ~/Dev/
$ git clone https://github.com/IA-Nate/BoogioBaseStation.git
```

Optional: Clone bluepy repository as reference

```
$ cd ~/Dev/
$ git clone https://github.com/IanHarvey/bluepy.git
```

Confirm bluepy is configured and the bluetooth radio is on

```
TODO
```

Get the latest updates from the repository
```
$ cd ~/Dev/BoogioBaseStation/
$ git pull origin master
```

## Running the tests
```
$ cd ~/Dev/BoogioBaseStation/SampleScripts/
$ sudo python StreamingExample.py
```

The script will first attempt to scan for all available devices. Look for Local Name: "Boogio_L" and "Boogio_R"

Make note of their mac addresses listed as Device(new): <MAC_ADDRESS>

Open for editing the file 
```
$ sudo nano ~/Dev/BoogioBaseStation/SampleScripts/StreamingExample.py
```

and change the values of the variables to your respective Boogio mac addresses (UUIDs).
```
LEFT_SHOE_PERIPHERAL_UUID = "<Boogio_L Device mac address>"
Right_SHOE_PERIPHERAL_UUID = "<Boogio_R Device mac address>"
```

Once you've completed editing StreamingExample.py in nano, 
```
Press Ctrl+o
then Enter 
This writes the file (saving your changes).

Then Press Ctrl+x
To exit nano

```

Run the python script once more. It should automatically connect to the devices after discovering them once more.

```
$ cd ~/Dev/BoogioBaseStation/SampleScripts/
$ sudo python StreamingExample.py
```

A PyGame window should appear and independent sensor values will begin to stream from the Boogio devices to the Raspberry Pi. 
```
Press "Esc" key to disconnect and exit the program.
```

### Break down into end to end tests

Explain what these tests test and why

```
Once the GUI is up. You can use the ESC key to end the StreamingExample python script.
```






