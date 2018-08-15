#!/usr/bin/env python
from __future__ import print_function
import argparse
from bluepy.btle import UUID, Peripheral, ADDR_TYPE_RANDOM, Scanner, DefaultDelegate, BTLEException
from bluepy import btle
import time
from time import sleep
import struct
import binascii
import sys
import os
import datetime
import sqlite3

PERIPHERAL_UUID = "f5:47:18:cf:9c:dc"

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'


def dump_services(dev):
    services = sorted(dev.services, key=lambda s: s.hndStart)
    for s in services:
        print ("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = ANSI_CYAN + '\'' + \
                        val.decode('utf-8') + '\'' + ANSI_OFF
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string = ''
            print ("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

            while True:
                h += 1
                if h > s.hndEnd or (i < len(chars) - 1 and h >= chars[i + 1].getHandle() - 1):
                    break
                try:
                    val = dev.readCharacteristic(h)
                    print ("\t%04x:     <%s>" %
                           (h, binascii.b2a_hex(val).decode('utf-8')))
                except btle.BTLEException:
                    break


class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            status = "new"
        elif isNewData:
            if self.opts.new:
                return
            status = "update"
        else:
            if not self.opts.all:
                return
            status = "old"

        if dev.rssi < self.opts.sensitivity:
            return

        print ('    Device (%s): %s (%s), %d dBm %s' %
               (status,
                   ANSI_WHITE + dev.addr + ANSI_OFF,
                   dev.addrType,
                   dev.rssi,
                   ('' if dev.connectable else '(not connectable)'))
               )
        for (sdid, desc, val) in dev.getScanData():
            if sdid in [8, 9]:
                print ('\t' + desc + ': \'' + ANSI_CYAN + val + ANSI_OFF + '\'')
            else:
                print ('\t' + desc + ': <' + val + '>')
        if not dev.scanData:
            print ('\t(no data)')
        print


def main():
        
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hci', action='store', type=int, default=0, help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=4, help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128, help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true', help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true', help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n', '--new', action='store_true', help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    arg = parser.parse_args(sys.argv[1:])

    btle.Debugging = arg.verbose

    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

    print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    devices = scanner.scan(arg.timeout)

    if arg.discover:
        print (ANSI_RED + "Discovering services..." + ANSI_OFF)

        for d in devices:
            if not d.connectable:

                continue

            print ("    Connecting to", ANSI_WHITE + d.addr + ANSI_OFF + ":")

            dev = btle.Peripheral(d)
            dump_services(dev)
            dev.disconnect()
            print

                

if __name__ == "__main__":
    main()



forceCharacteristicHandle = None
accelerationCharacteristicHandle = None
rotationCharacteristicHandle = None





class MyDelegate(DefaultDelegate):

    def __init__(self):
        self.MAX_FORCE_VALUE = 1023.0
        self.MAX_ACCELERATION_VALUE = 8000.0
        self.MAX_ROTATION_VALUE = 1000.0
        self.MAX_HEADING_VALUE = 1000.0

        self.MAX_SHORT_VALUE = 65535.0
        self.HALF_OF_MAX_SHORT_VALUE = 32767.0
        
        self.ACCELERATION_CONVERSION_COEFFICIENT = 1.0 / 1000.0
        self.ROTATION_CONVERSION_COEFFICIENT     = 1.0 / 1000.0

        self.forceBufferIsEmpty = False
        self.accelerationBufferIsEmpty = False
        self.rotationBufferIsEmpty = False

      

    def handleNotification(self, hnd, data):

        #print(data)
        #print("\n")
        
        #Debug print repr(data)
        if (hnd == forceCharacteristicHandle):
            
            hour = struct.unpack('<H', data[0:2])[0]
            millisecond = struct.unpack('<H', data[2:4])[0]

            
            forceToe = struct.unpack('<H', data[4:6])[0]
            forceBall = struct.unpack('<H', data[6:8])[0]
            forceArch = struct.unpack('<H', data[8:10])[0]
            forceHeel = struct.unpack('<H', data[10:12])[0]

            print("[" +  str(hour) + ":" + str(millisecond) + "][FORCE]       [" + str(forceToe) + " " + str(forceBall) + " " + str(forceArch) + " " + str(forceHeel) + "]")

            if(millisecond == 0 and hour == 511):
                self.forceBufferIsEmpty = True
            
            

                
        elif (hnd == accelerationCharacteristicHandle):
            
            hour = struct.unpack('<H', data[0:2])[0]
            millisecond = struct.unpack('<H', data[2:4])[0]

            
            accelerationX = struct.unpack('<h', data[4:6])[0]
            accelerationY = struct.unpack('<h', data[6:8])[0]
            accelerationZ = struct.unpack('<h', data[8:10])[0]

            print("[" + str(hour) + ":" + str(millisecond) + "][ACCELERATION][" + str(accelerationX) + " " + str(accelerationY) + " " + str(accelerationZ) + "]")

            if(millisecond == 0 and hour == 511):
                self.accelerationBufferIsEmpty = True

           

        elif (hnd == rotationCharacteristicHandle):
            
            hour = struct.unpack('<H', data[0:2])[0]
            millisecond = struct.unpack('<H', data[2:4])[0]
            
           
            rotationX = struct.unpack('<h', data[4:6])[0]
            rotationY = struct.unpack('<h', data[6:8])[0]
            rotationZ = struct.unpack('<h', data[8:10])[0]
            rotationW = struct.unpack('<h', data[10:12])[0]

            print("[" + str(hour) + ":" + str(millisecond) + "][ROTATION]    [" + str(rotationX) + " " + str(rotationY) + " " + str(rotationZ) + " " + str(rotationW) + "]")

            if(millisecond == 0 and hour == 511):
                self.rotationBufferIsEmpty = True

            
        else:
            teptep = binascii.b2a_hex(data)
            print('Notification: UNKOWN: hnd {}, data {}'.format(hnd, teptep))
            

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i    



boogioPeripheral = Peripheral(PERIPHERAL_UUID, "random")

boogioDelegate = MyDelegate()
boogioPeripheral.setDelegate(boogioDelegate)

boogioShoeSensorService = None

forceCharacteristic = None
accelerationCharacteristic = None
rotationCharacteristic = None


CCCD_UUID = 0x2902

print("Boogio Peripheral:")
for svc in boogioPeripheral.services:
    print("      ")
    print(str(svc))
    if svc.uuid == "f3641400-00B0-4240-ba50-05ca45bf8abc":
        boogioShoeSensorService = boogioPeripheral.getServiceByUUID(svc.uuid)
        for characteristic in boogioShoeSensorService.getCharacteristics():
            print(characteristic)
            if characteristic.uuid == "f3641401-00B0-4240-ba50-05ca45bf8abc":
                forceCharacteristic = characteristic
                forceCharacteristicHandle = characteristic.getHandle()
                forceCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                
            elif characteristic.uuid == "f3641402-00B0-4240-ba50-05ca45bf8abc":
                accelerationCharacteristic = characteristic
                accelerationCharacteristicHandle = characteristic.getHandle()
                accelerationCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                
            elif characteristic.uuid == "f3641403-00B0-4240-ba50-05ca45bf8abc":
                rotationCharacteristic = characteristic
                rotationCharacteristicHandle = characteristic.getHandle()
                rotationCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                
            



BLACK = (0,0,0)
RED = (255,60,120)
GREEN = (58,255,118)
BLUE = (64,128,255)
ORANGE = (252, 97, 38)
YELLOW = (255, 255, 15)



year = datetime.datetime.now().strftime('%Y')
hexYear = format(int(year), '04x')
yearLowByte = hexYear[2] + hexYear[3]
yearHighByte = hexYear[0] + hexYear[1]
        
month = str(datetime.datetime.now().strftime('%m'))
day = str(datetime.datetime.now().strftime('%d'))
hour = str(datetime.datetime.now().strftime('%H'))
minute = str(datetime.datetime.now().strftime('%M'))
second = str(datetime.datetime.now().strftime('%S'))
        
#millisecond = datetime.datetime.now().strftime('%f')
millisecond = 0
hexMillisecond = format(int(millisecond), '04x')
millisecondLowByte = hexMillisecond[2] + hexMillisecond[3]
millisecondHighByte = hexMillisecond[0] + hexMillisecond[1]
        
byteString = bytearray()
byteString.append(0x00) #set time command
byteString.append(yearLowByte.decode("hex"))
byteString.append(yearHighByte.decode("hex"))
byteString.append(int(month))
byteString.append(int(day))
byteString.append(int(hour))
byteString.append(int(minute))
byteString.append(int(second))
byteString.append(millisecondLowByte.decode("hex"))
byteString.append(millisecondHighByte.decode("hex"))

time.sleep(1)


reload(sys)
sys.setdefaultencoding('utf8')
           
# upate timestamp
print("Timestamp = " + str(year) + "/" + str(month) + "/" + str(day) + "-" + str(hour) + ":" + str(minute) + ":" + str(second) + "." + str(millisecond))
#boogioPeripheral.writeCharacteristic(forceCharacteristicHandle, byteString, True)
forceCharacteristic.write(str(byteString), withResponse = True)

time.sleep(1)

setProtocolByteString = bytearray()
setProtocolByteString.append(0x01) # set protocol command
setProtocolByteString.append(0x02) # synchronization enum

rotationCharacteristic.write(str(setProtocolByteString), withResponse = True)

time.sleep(1)

forceCCCD.write(b"\x01\x00", True)
accelerationCCCD.write(b"\x01\x00", True)
rotationCCCD.write(b"\x01\x00", True)




syncCount = 10
sleepTime = 1
    
syncStep = bytearray()
syncStep.append(0x02) # Sync Command
syncStep.append(0x01) # 1 Readings
    
while(True):
    if(not boogioDelegate.forceBufferIsEmpty):
        forceCharacteristic.write(str(syncStep), withResponse = True)
        boogioPeripheral.waitForNotifications(sleepTime)
    
    if(not boogioDelegate.accelerationBufferIsEmpty):
        accelerationCharacteristic.write(str(syncStep), withResponse = True)
        boogioPeripheral.waitForNotifications(sleepTime)
    
    if(not boogioDelegate.rotationBufferIsEmpty):
        rotationCharacteristic.write(str(syncStep), withResponse = True)
        boogioPeripheral.waitForNotifications(sleepTime)
    
    print("\r\n")

    if(boogioDelegate.forceBufferIsEmpty and boogioDelegate.accelerationBufferIsEmpty and boogioDelegate.rotationBufferIsEmpty):
        break



print("Done Syncing.")
boogioPeripheral.disconnect()
