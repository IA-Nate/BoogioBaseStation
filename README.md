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
$ sudo pip install numpy
$ sudo pip install pyquaternion
$ sudo pip install tf
$ sudo pip install nibabel
$ sudo pip3 install bluepy
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

### Running the scripts

Use scanner.py to enumerate all the devices broadcasting as Boogio peripherals.

```
$ cd ~/Dev/BoogioBaseStation/SampleScripts/
$ sudo python3 scanner.py
```

Make note of their mac addresses listed as Device(new): <MAC_ADDRESS>


Now run streaming.py by passing it a mac address. It should automatically connect to the device after discovering it once more.

```
$ cd ~/Dev/BoogioBaseStation/Python/
$ sudo python3 streaming.py
```

A PyGame window should appear and independent sensor values will begin to stream from the Boogio devices to the Raspberry Pi. 

```
Press "Esc" key to disconnect and exit the program.
```


You can also use the streaming.py script to transmit the readings to a TCP client over a port you pass as an argument.
```
$ cd ~/Dev/BoogioBaseStation/Python/
$ sudo python3 streaming.py -p 21030 -e -b dc:80:07:ef:8b:cf
```

The above example will listen for a TCP connection over port 21030 and, once connected to that client, also connect to the boogio device with the mac address dc:80:07:ef:8b:cf

Sensor data from the boogio device will then be transmitted to the client over the open socket.






