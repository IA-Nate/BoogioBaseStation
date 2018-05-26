# Boogio Base Station

The official Boogio Base Station open-source software codebase.


## Getting Started

### Installing

These steps document how to configure a Base Station for Python development.

Update Raspbian and restart.

```
$ sudo su -
# apt-get update
# apt-get dist-upgrade
# init 6
```

After restarting, install bluepy: https://www.elinux.org/RPi_Bluetooth_LE
```

$ sudo apt-get install python-pip
$ sudo apt-get install libgllib2.0-dev
$ sudo pip-install bluepy
```

Optional: Clone bluepy repository as reference

```
[] cd ~/Dev
[] git clone https://github.com/IanHarvey/bluepy.git
```

Confirm bluepy is configured and the bluetooth radio is on

```
TODO
```


## Running the tests

```
$ sudo python StreamingExample.py
```


### Break down into end to end tests

Explain what these tests test and why

```
Once the GUI is up. You can use the ESC key to end the StreamingExample python script.
```






