# Boogio Base Station

The official Boogio Base Station open-source software codebase.


## Getting Started

### Installing

These steps document how to create a Base Station for Python development. If you've received a preconfigured base station, you can skip to the "Running the tests" section.

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






