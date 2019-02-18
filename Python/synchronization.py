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
from BoogioLogger import *


#PERIPHERAL_UUID = "dc:80:07:ef:8b:cf"
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



buffer0CharacteristicHandle = None
buffer1CharacteristicHandle = None
buffer2CharacteristicHandle = None



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

        self.buffer0IsEmpty = False
        self.buffer1IsEmpty = False
        self.buffer2IsEmpty = False

        self.logger = BoogioLogger(PERIPHERAL_UUID)
        
        
      

    def handleNotification(self, hnd, data):

        if(struct.unpack('<B', data[0:1])[0] == 255 and struct.unpack('<B', data[1:2])[0] == 01):
            if(hnd == buffer0CharacteristicHandle):
                self.buffer0IsEmpty = True
                return
            elif(hnd == buffer1CharacteristicHandle):
                self.buffer1IsEmpty = True
                return
            elif(hnd == buffer2CharacteristicHandle):
                self.buffer2IsEmpty = True
                return

    
        milliseconds = struct.unpack('>Q', data[0:8])[0]
        

        timestamp = datetime.datetime.fromtimestamp(milliseconds/1000.0).strftime("%Y-%m-%d %H:%M:%S.%f")
        self.logger.setTime(timestamp)
        
        #header = "[" + str(milliseconds) + "]"
        header = "[" + timestamp + "]"
        
        #Debug print repr(data)
        if (hnd == buffer0CharacteristicHandle):
            
            force0 = struct.unpack('<H', data[8:10])[0]
            force1 = struct.unpack('<H', data[10:12])[0]
            force2 = struct.unpack('<H', data[12:14])[0]
            force3 = struct.unpack('<H', data[14:16])[0]
            force4 = struct.unpack('<H', data[16:18])[0]
            force5 = struct.unpack('<H', data[18:20])[0]
            

            print(header + "[Buffer_0]----[" + str(force0) + "  " + str(force1) + "  " + str(force2)+ "  " + str(force3) + "  " + str(force4) + "  " + str(force5) + "]")

            

            self.logger.insertBuffer0Values(timestamp, force0, force1, force2, force3, force4, force5)
            
            

                
        elif (hnd == buffer1CharacteristicHandle):
            force6        = struct.unpack('<H', data[8:10])[0]
            force7        = struct.unpack('<H', data[10:12])[0]
            accelerationX = struct.unpack('<h', data[12:14])[0]
            accelerationY = struct.unpack('<h', data[14:16])[0]
            accelerationZ = struct.unpack('<h', data[16:18])[0]

            print(header + "[Buffer_1]----[" + str(force6) + "  " + str(force7) + "  " + str(accelerationX) + "  " + str(accelerationY) + "  " + str(accelerationZ) + "]")


            self.logger.insertBuffer1Values(timestamp, force6, force7, accelerationX, accelerationY, accelerationZ)
           

        elif (hnd == buffer2CharacteristicHandle):
            

           
            rotationX = struct.unpack('<h', data[8:10])[0]
            rotationY = struct.unpack('<h', data[10:12])[0]
            rotationZ = struct.unpack('<h', data[12:14])[0]
            rotationW = struct.unpack('<h', data[14:16])[0]

            print(header + "[Buffer_2]----[" + str(rotationX) + "  " + str(rotationY) + "  " + str(rotationZ) + "  " + str(rotationW) + "]")


            self.logger.insertBuffer2Values(timestamp, rotationX, rotationY, rotationZ, rotationW)

            
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

buffer0Characteristic = None
buffer1Characteristic = None
buffer2Characteristic = None


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
                buffer0Characteristic = characteristic
                buffer0CharacteristicHandle = characteristic.getHandle()
                buffer0CCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                
            elif characteristic.uuid == "f3641402-00B0-4240-ba50-05ca45bf8abc":
                buffer1Characteristic = characteristic
                buffer1CharacteristicHandle = characteristic.getHandle()
                buffer1CCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                
            elif characteristic.uuid == "f3641403-00B0-4240-ba50-05ca45bf8abc":
                buffer2Characteristic = characteristic
                buffer2CharacteristicHandle = characteristic.getHandle()
                buffer2CCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                
            



BLACK = (0,0,0)
RED = (255,60,120)
GREEN = (58,255,118)
BLUE = (64,128,255)
ORANGE = (252, 97, 38)
YELLOW = (255, 255, 15)


current_time = int(round(time.time() * 1000))

        
byteString = bytearray()
byteString.append(0x00) #set time command
byteString.append((current_time >> 56) & 0xff)
byteString.append((current_time >> 48) & 0xff)
byteString.append((current_time >> 40) & 0xff)
byteString.append((current_time >> 32) & 0xff)
byteString.append((current_time >> 24) & 0xff)
byteString.append((current_time >> 16) & 0xff)
byteString.append((current_time >> 8) & 0xff)
byteString.append((current_time >> 0) & 0xff)

time.sleep(1)


reload(sys)
sys.setdefaultencoding('utf8')
           
# upate timestamp
print("Timestamp = " + str(current_time))
#boogioPeripheral.writeCharacteristic(forceCharacteristicHandle, byteString, True)
buffer0Characteristic.write(str(byteString), withResponse = True)

time.sleep(1)

setProtocolByteString = bytearray()
setProtocolByteString.append(0x01) # set protocol command
setProtocolByteString.append(0x02) # synchronization enum

buffer0Characteristic.write(str(setProtocolByteString), withResponse = True)



setSampleRateByteString = bytearray()
setSampleRateByteString.append(0x04) # set sample rate command
setSampleRateByteString.append(0x01) # frequency argument (Hz)
buffer0Characteristic.write(str(setSampleRateByteString), withResponse = True)


time.sleep(1)

buffer0CCCD.write(b"\x01\x00", True)
buffer1CCCD.write(b"\x01\x00", True)
buffer2CCCD.write(b"\x01\x00", True)


syncCount = 10
sleepTime = 1
    
syncStep = bytearray()
syncStep.append(0x02) # Sync Command
syncStep.append(0x01) # 1 Readings

boogioDelegate.logger.connect()
    
while(True):
    if(not boogioDelegate.buffer0IsEmpty):
        buffer0Characteristic.write(str(syncStep), withResponse = True)
        boogioPeripheral.waitForNotifications(sleepTime)
    
    if(not boogioDelegate.buffer1IsEmpty):
        buffer1Characteristic.write(str(syncStep), withResponse = True)
        boogioPeripheral.waitForNotifications(sleepTime)
    
    if(not boogioDelegate.buffer2IsEmpty):
        buffer2Characteristic.write(str(syncStep), withResponse = True)
        boogioPeripheral.waitForNotifications(sleepTime)
    
    print("\r\n")

    if(boogioDelegate.buffer0IsEmpty and boogioDelegate.buffer1IsEmpty and boogioDelegate.buffer2IsEmpty):
        break


boogioDelegate.logger.commit()
boogioDelegate.logger.disconnect()
print("Done Syncing.")
boogioPeripheral.disconnect()
