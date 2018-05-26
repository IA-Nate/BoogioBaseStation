Goal
Have a Raspberry Pi communicating over BLE to Boogio 4.0 boards

Tasks
Use disk formatter on OS X to format the sd card
Use disk writer utility on Windows to image Raspbian to the SD card
Set up the pi (ssh, ftp, keyboard, etc.)
Set up BlueZ
Install the Nordic Kernel


Resources
http://www.elinux.org/RPi_Bluetooth_LE - Setting up BlueZ
https://ianharvey.github.io/bluepy-doc/ - BluePy Documentation
http://stackoverflow.com/questions/4383571/importing-files-from-different-folder-in-python - adding script to the python path (enable “import btle” from any location when executing script)
http://www.techjawab.com/2015/01/dynamic-dns-easy-way.html - free dynDNS client setup for RPi
http://www.howtogeek.com/167190/how-and-why-to-assign-the-.local-domain-to-your-raspberry-pi/ - setting up a local DNS
http://shawnhymel.com/665/using-python-and-ble-to-receive-data-from-the-rfduino/ - python example of using btle

Fidning BLE mac address, handles, uuids, info

sudo hciconfig hci0 up
sudo hcitool lescan
(copy mac address)
sudo gatttool -t random -b <<Mac Address>> -I
sudo gatttool -t random -b C1:5D:2E:65:16:2D -I
connect

primary

attr handle: 0x0001, end grp handle: 0x0007 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0008, end grp handle: 0x000b uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x000c, end grp handle: 0x0016 uuid: 97290000-3b5a-4117-9834-a64cea4ad41d
attr handle: 0x0017, end grp handle: 0x001a uuid: 0000180f-0000-1000-8000-00805f9b34fb
attr handle: 0x001b, end grp handle: 0x001d uuid: 0000180a-0000-1000-8000-00805f9b34fb
attr handle: 0x001e, end grp handle: 0x0022 uuid: 97290004-3b5a-4117-9834-a64cea4ad41d
attr handle: 0x0023, end grp handle: 0xffff uuid: 00001530-1212-efde-1523-785feabcd123

copy service UUIDs you would like to interact with

characteristics

handle: 0x0002, char properties: 0x0a, char value handle: 0x0003, uuid: 00002a00-0000-1000-8000-00805f9b34fb
handle: 0x0004, char properties: 0x02, char value handle: 0x0005, uuid: 00002a01-0000-1000-8000-00805f9b34fb
handle: 0x0006, char properties: 0x02, char value handle: 0x0007, uuid: 00002a04-0000-1000-8000-00805f9b34fb
handle: 0x0009, char properties: 0x20, char value handle: 0x000a, uuid: 00002a05-0000-1000-8000-00805f9b34fb
handle: 0x000d, char properties: 0x12, char value handle: 0x000e, uuid: 97290001-3b5a-4117-9834-a64cea4ad41d
handle: 0x0011, char properties: 0x12, char value handle: 0x0012, uuid: 97290002-3b5a-4117-9834-a64cea4ad41d
handle: 0x0015, char properties: 0x02, char value handle: 0x0016, uuid: 00002a38-0000-1000-8000-00805f9b34fb
handle: 0x0018, char properties: 0x12, char value handle: 0x0019, uuid: 00002a19-0000-1000-8000-00805f9b34fb
handle: 0x001c, char properties: 0x02, char value handle: 0x001d, uuid: 00002a29-0000-1000-8000-00805f9b34fb
handle: 0x001f, char properties: 0x1a, char value handle: 0x0020, uuid: 97290005-3b5a-4117-9834-a64cea4ad41d
handle: 0x0024, char properties: 0x04, char value handle: 0x0025, uuid: 00001532-1212-efde-1523-785feabcd123
handle: 0x0026, char properties: 0x18, char value handle: 0x0027, uuid: 00001531-1212-efde-1523-785feabcd123
handle: 0x0029, char properties: 0x02, char value handle: 0x002a, uuid: 00001534-1212-efde-1523-785feabcd123

copy characteristic UUIDs you would like to interact with

char-read-uuid 0x2902

handle: 0x000b 	 value: 00 00 

handle: 0x0010 	 value: 00 00 

handle: 0x0014 	 value: 00 00 

handle: 0x001a 	 value: 00 00 

handle: 0x0022 	 value: 00 00 


handles listed are those you will be reading, writing and subscribing to

disconnect
exit