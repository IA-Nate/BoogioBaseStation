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

import pygame
from pygame.locals import *

# !IMPORTANT!:
# change the values of LEFT_SHOE_PERIPHERAL_UUID and LEFT_SHOE_PERIPHERAL_UUID
# to your corresponding Boogio_L and Boogio_R UUIDs discovered from scanning

# Example scan output:

    # Device (new): e8:39:e4:37:0e:27 (random), -55 dBm 
    # 	Flags: <06>
    # 	Complete 16b Services: <0f180a18>
    # 	Complete 128b Services: <1dd44aea4ca6349817415a3b00002997>
    # 	Complete Local Name: 'Boogio_L'
    # 	Appearance: <4104>
    # 	Manufacturer: <ffff06>

    # Device (new): d3:b9:66:45:f9:9f (random), -64 dBm 
    # 	Flags: <06>
    # 	Complete 16b Services: <0f180a18>
    # 	Complete 128b Services: <1dd44aea4ca6349817415a3b00002997>
    #       Complete Local Name: 'Boogio_R'
    # 	Appearance: <4104>
    # 	Manufacturer: <ffff07>


LEFT_SHOE_PERIPHERAL_UUID = "e8:39:e4:37:0e:27"
RIGHT_SHOE_PERIPHERAL_UUID = "d3:b9:66:45:f9:9f"



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
    parser.add_argument('-i', '--hci', action='store', type=int, default=0,
                        help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=4,
                        help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n', '--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity')
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



leftForceCharacteristicHandle = None
leftAccelerationCharacteristicHandle = None
leftRotationCharacteristicHandle = None
leftHeadingCharacteristicHandle = None

rightForceCharacteristicHandle = None
rightAccelerationCharacteristicHandle = None
rightRotationCharacteristicHandle = None
rightHeadingCharacteristicHandle = None



class MyDelegate(DefaultDelegate):

    def __init__(self):
        self.MAX_FORCE_VALUE = 1023.0
        self.MAX_ACCELERATION_VALUE = 8000.0
        self.MAX_ROTATION_VALUE = 1000.0
        self.MAX_HEADING_VALUE = 4800.0

        self.MAX_SHORT_VALUE = 65535.0
        self.HALF_OF_MAX_SHORT_VALUE = 32767.0
        
        self.ACCELERATION_CONVERSION_COEFFICIENT = self.MAX_ACCELERATION_VALUE / self.HALF_OF_MAX_SHORT_VALUE
        self.ROTATION_CONVERSION_COEFFICIENT = self.MAX_ROTATION_VALUE / self.HALF_OF_MAX_SHORT_VALUE
        self.HEADING_CONVERSION_COEFFICIENT = self.MAX_HEADING_VALUE / self.HALF_OF_MAX_SHORT_VALUE

        self.forceToe = 0.0
        self.forceBall = 0.0
        self.forceArch = 0.0
        self.forceHeel = 0.0

        self.accelerationX = 0.0
        self.accelerationY = 0.0
        self.accelerationZ = 0.0

        self.rotationX = 0.0
        self.rotationY = 0.0
        self.rotationZ = 0.0

        self.headingX = 0.0
        self.headingY = 0.0
        self.headingZ = 0.0
        

    def handleNotification(self, hnd, data):
        
        
        #Debug print repr(data)
        if (hnd == leftForceCharacteristicHandle or hnd == rightForceCharacteristicHandle):
            self.forceToe = struct.unpack('<H', data[0:2])[0]
            self.forceBall = struct.unpack('<H', data[2:4])[0]
            self.forceArch = struct.unpack('<H', data[4:6])[0]
            self.forceHeel = struct.unpack('<H', data[6:8])[0]
            
        elif (hnd == leftAccelerationCharacteristicHandle or hnd == rightAccelerationCharacteristicHandle):
            self.accelerationX = struct.unpack('<H', data[0:2])[0]
            self.accelerationY = struct.unpack('<H', data[2:4])[0]
            self.accelerationZ = struct.unpack('<H', data[4:6])[0]

            #2's complement
            if(self.accelerationX > self.HALF_OF_MAX_SHORT_VALUE):
               self.accelerationX = self.accelerationX - self.MAX_SHORT_VALUE
            if(self.accelerationY > self.HALF_OF_MAX_SHORT_VALUE):
               self.accelerationY = self.accelerationY - self.MAX_SHORT_VALUE
            if(self.accelerationZ > self.HALF_OF_MAX_SHORT_VALUE):
               self.accelerationZ = self.accelerationZ - self.MAX_SHORT_VALUE

            self.accelerationX *= self.ACCELERATION_CONVERSION_COEFFICIENT
            self.accelerationY *= self.ACCELERATION_CONVERSION_COEFFICIENT
            self.accelerationZ *= self.ACCELERATION_CONVERSION_COEFFICIENT

        elif (hnd == leftRotationCharacteristicHandle or hnd == rightRotationCharacteristicHandle):
            self.rotationX = struct.unpack('<H', data[0:2])[0]
            self.rotationY = struct.unpack('<H', data[2:4])[0]
            self.rotationZ = struct.unpack('<H', data[4:6])[0]

            #2's complement
            if(self.rotationX > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationX = self.rotationX - self.MAX_SHORT_VALUE
            if(self.rotationY > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationY = self.rotationY - self.MAX_SHORT_VALUE
            if(self.rotationZ > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationZ = self.rotationZ - self.MAX_SHORT_VALUE

            self.rotationX *= self.ROTATION_CONVERSION_COEFFICIENT
            self.rotationY *= self.ROTATION_CONVERSION_COEFFICIENT
            self.rotationZ *= self.ROTATION_CONVERSION_COEFFICIENT

        elif (hnd == leftHeadingCharacteristicHandle or hnd == rightHeadingCharacteristicHandle):
            self.headingX = struct.unpack('<H', data[0:2])[0]
            self.headingY = struct.unpack('<H', data[2:4])[0]
            self.headingZ = struct.unpack('<H', data[4:6])[0]

            #2's complement
            if(self.headingX > self.HALF_OF_MAX_SHORT_VALUE):
               self.headingX = self.headingX - self.MAX_SHORT_VALUE
            if(self.headingY > self.HALF_OF_MAX_SHORT_VALUE):
               self.headingY = self.headingY - self.MAX_SHORT_VALUE
            if(self.headingZ > self.HALF_OF_MAX_SHORT_VALUE):
               self.headingZ = self.headingZ - self.MAX_SHORT_VALUE

            self.headingX *= self.HEADING_CONVERSION_COEFFICIENT
            self.headingY *= self.HEADING_CONVERSION_COEFFICIENT
            self.headingZ *= self.HEADING_CONVERSION_COEFFICIENT

            #print(self.headingX, self.headingY, self.headingZ)
        else:
            teptep = binascii.b2a_hex(data)
            print('Notification: UNKOWN: hnd {}, data {}'.format(hnd, teptep))
            

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i    



leftShoePeripheral = Peripheral(LEFT_SHOE_PERIPHERAL_UUID, "random")
rightShoePeripheral = Peripheral(RIGHT_SHOE_PERIPHERAL_UUID, "random")



leftShoeDelegate = MyDelegate()
rightShoeDelegate = MyDelegate()

leftShoePeripheral.setDelegate(leftShoeDelegate)
rightShoePeripheral.setDelegate(rightShoeDelegate)

leftShoeSensorService = None
rightShoeSensorService = None

leftForceCharacteristic = None
leftAccelerationCharacteristic = None
leftRotationCharacteristic = None
leftHeadingCharacteristic = None

rightForceCharacteristic = None
rightAccelerationCharacteristic = None
rightRotationCharacteristic = None
rightHeadingCharacteristic = None



#leftAccelerationCharacteristic = self.environment_service.getCharacteristics(self.temperature_char_uuid)[0]
#leftAccelerationCharacteristicHandle = self.temperature_char.getHandle()
#leftAccelerationCCCD = self.temperature_char.getDescriptors(forUUID=CCCD_UUID)[0]

CCCD_UUID = 0x2902

print("LEFT SHOE:")
for svc in leftShoePeripheral.services:
    print(str(svc))
    if svc.uuid == "97290000-3b5a-4117-9834-a64cea4ad41d":
        leftShoeSensorService = leftShoePeripheral.getServiceByUUID(svc.uuid)
        for characteristic in leftShoeSensorService.getCharacteristics():
            print(characteristic)
            if characteristic.uuid == "97290001-3b5a-4117-9834-a64cea4ad41d":
                leftForceCharacteristic = characteristic
                leftForceCharacteristicHandle = characteristic.getHandle()
                leftForceCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                leftForceCCCD.write(b"\x01\x00", True)
            elif characteristic.uuid == "97290002-3b5a-4117-9834-a64cea4ad41d":
                leftAccelerationCharacteristic = characteristic
                leftAccelerationCharacteristicHandle = characteristic.getHandle()
                leftAccelerationCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                leftAccelerationCCCD.write(b"\x01\x00", True)
            elif characteristic.uuid == "97290003-3b5a-4117-9834-a64cea4ad41d":
                leftRotationCharacteristic = characteristic
                leftRotationCharacteristicHandle = characteristic.getHandle()
                leftRotationCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                leftRotationCCCD.write(b"\x01\x00", True)
            elif characteristic.uuid == "97290004-3b5a-4117-9834-a64cea4ad41d":
                leftHeadingCharacteristic = characteristic
                leftHeadingCharacteristicHandle = characteristic.getHandle()
                leftHeadingCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                leftHeadingCCCD.write(b"\x01\x00", True)

print("RIGHT SHOE:")
for svc in rightShoePeripheral.services:
    print(str(svc))
    if svc.uuid == "97290000-3b5a-4117-9834-a64cea4ad41d":
        rightShoeSensorService = rightShoePeripheral.getServiceByUUID(svc.uuid)
        for characteristic in rightShoeSensorService.getCharacteristics():
            print(characteristic)
            if characteristic.uuid == "97290001-3b5a-4117-9834-a64cea4ad41d":
                rightForceCharacteristic = characteristic
                rightForceCharacteristicHandle = characteristic.getHandle()
                rightForceCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                rightForceCCCD.write(b"\x01\x00", True)
            elif characteristic.uuid == "97290002-3b5a-4117-9834-a64cea4ad41d":
                rightAccelerationCharacteristic = characteristic
                rightAccelerationCharacteristicHandle = characteristic.getHandle()
                rightAccelerationCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                rightAccelerationCCCD.write(b"\x01\x00", True)
            elif characteristic.uuid == "97290003-3b5a-4117-9834-a64cea4ad41d":
                rightRotationCharacteristic = characteristic
                rightRotationCharacteristicHandle = characteristic.getHandle()
                rightRotationCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                rightRotationCCCD.write(b"\x01\x00", True)
            elif characteristic.uuid == "97290004-3b5a-4117-9834-a64cea4ad41d":
                rightHeadingCharacteristic = characteristic
                rightHeadingCharacteristicHandle = characteristic.getHandle()
                rightHeadingCCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                rightHeadingCCCD.write(b"\x01\x00", True)



#pygame graphics
pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 400
READING_SCALE = 100
WINDOW_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAYSURF = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
pygame.display.set_caption("Boogio 5 Data Streaming Example")



metricsFont = pygame.font.SysFont("comicsans", 24)

BLACK = (0,0,0)
RED = (255,60,120)
GREEN = (58,255,118)
BLUE = (64,128,255)
ORANGE = (252, 97, 38)

shouldQuit = False
while not shouldQuit:
    for event in pygame.event.get():
        if event.type == QUIT:
            shouldQuit = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                shouldQuit = True

    leftShoePeripheral.waitForNotifications(0.001)
    rightShoePeripheral.waitForNotifications(0.001)

    hSpacing = 10
    vSpacing = 24
    cursorX = hSpacing
    cursorY = vSpacing

    #left shoe data

    #labels 
    DISPLAYSURF.fill(BLACK)
    labelSurface = metricsFont.render("Left Shoe: ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing))

    
    labelSurface = metricsFont.render("Acceleration ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 3))

    
    labelSurface = metricsFont.render("[milliGravities]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 4))

    labelSurface = metricsFont.render("Rotation ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 6))

    labelSurface = metricsFont.render("[degrees/sec]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 7))

    labelSurface = metricsFont.render("Heading ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 9))

    labelSurface = metricsFont.render("[microTeslas]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 10))

    labelSurface = metricsFont.render("Force ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 12))

    labelSurface = metricsFont.render("[decaNewtons]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 13))

    
    # readings
    cursorX = SCREEN_WIDTH / 8

    labelSurface = metricsFont.render(LEFT_SHOE_PERIPHERAL_UUID, 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing))

    labelSurface = metricsFont.render("________________________________________", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 2))

    labelSurface = metricsFont.render("X", 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 2))

    
    labelSurface = metricsFont.render("Y", 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 2))

    
    labelSurface = metricsFont.render("Z", 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 2))
    

    leftShoeAccelerationX = str(round(leftShoeDelegate.accelerationX, 2))
    labelSurface = metricsFont.render(leftShoeAccelerationX, 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 4))

    leftShoeAccelerationY = str(round(leftShoeDelegate.accelerationY, 2))
    labelSurface = metricsFont.render(leftShoeAccelerationY, 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 4))

    leftShoeAccelerationZ = str(round(leftShoeDelegate.accelerationZ, 2))
    labelSurface = metricsFont.render(leftShoeAccelerationZ, 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 4))



    leftShoeRotationX = str(round(leftShoeDelegate.rotationX, 2))
    labelSurface = metricsFont.render(leftShoeRotationX, 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 7))

    leftShoeRotationY = str(round(leftShoeDelegate.rotationY, 2))
    labelSurface = metricsFont.render(leftShoeRotationY, 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 7))

    leftShoeRotationZ = str(round(leftShoeDelegate.rotationZ, 2))
    labelSurface = metricsFont.render(leftShoeRotationZ, 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 7))

    

    leftShoeHeadingX = str(round(leftShoeDelegate.headingX, 2))
    labelSurface = metricsFont.render(leftShoeHeadingX, 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 10))

    leftShoeHeadingY = str(round(leftShoeDelegate.headingY, 2))
    labelSurface = metricsFont.render(leftShoeHeadingY, 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 10))

    leftShoeHeadingZ = str(round(leftShoeDelegate.headingZ, 2))
    labelSurface = metricsFont.render(leftShoeHeadingZ, 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 10))

    labelSurface = metricsFont.render("________________________________________", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 12))


    labelSurface = metricsFont.render("Toe", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 12))
    
    labelSurface = metricsFont.render("Ball", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 12))

    labelSurface = metricsFont.render("Arch", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 12))

    labelSurface = metricsFont.render("Heel", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*32, vSpacing * 12))

    leftShoeForceToe = str(round(leftShoeDelegate.forceToe, 2))
    labelSurface = metricsFont.render(leftShoeForceToe, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 13))

    leftShoeForceBall = str(round(leftShoeDelegate.forceBall, 2))
    labelSurface = metricsFont.render(leftShoeForceBall, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 13))

    leftShoeForceArch = str(round(leftShoeDelegate.forceArch, 2))
    labelSurface = metricsFont.render(leftShoeForceArch, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 13))

    leftShoeForceHeel = str(round(leftShoeDelegate.forceHeel, 2))
    labelSurface = metricsFont.render(leftShoeForceHeel, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*32, vSpacing * 13))






    #right shoe data
    

    #labels 
    cursorX = SCREEN_WIDTH / 2
    
    labelSurface = metricsFont.render("Right Shoe: ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing))

    
    labelSurface = metricsFont.render("Acceleration ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 3))

    
    labelSurface = metricsFont.render("[milliGravities]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 4))

    labelSurface = metricsFont.render("Rotation ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 6))

    labelSurface = metricsFont.render("[degrees/sec]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 7))

    labelSurface = metricsFont.render("Heading ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 9))

    labelSurface = metricsFont.render("[microTeslas]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 10))

    labelSurface = metricsFont.render("Force ", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 12))

    labelSurface = metricsFont.render("[decaNewtons]:", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 13))

    
    # readings
    cursorX = SCREEN_WIDTH / 8 + SCREEN_WIDTH / 2

    labelSurface = metricsFont.render(RIGHT_SHOE_PERIPHERAL_UUID, 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing))

    labelSurface = metricsFont.render("________________________________________", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 2))

    labelSurface = metricsFont.render("X", 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 2))

    
    labelSurface = metricsFont.render("Y", 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 2))

    
    labelSurface = metricsFont.render("Z", 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 2))
    

    rightShoeAccelerationX = str(round(rightShoeDelegate.accelerationX, 2))
    labelSurface = metricsFont.render(rightShoeAccelerationX, 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 4))

    rightShoeAccelerationY = str(round(rightShoeDelegate.accelerationY, 2))
    labelSurface = metricsFont.render(rightShoeAccelerationY, 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 4))

    rightShoeAccelerationZ = str(round(rightShoeDelegate.accelerationZ, 2))
    labelSurface = metricsFont.render(rightShoeAccelerationZ, 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 4))



    rightShoeRotationX = str(round(rightShoeDelegate.rotationX, 2))
    labelSurface = metricsFont.render(rightShoeRotationX, 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 7))

    rightShoeRotationY = str(round(rightShoeDelegate.rotationY, 2))
    labelSurface = metricsFont.render(rightShoeRotationY, 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 7))

    rightShoeRotationZ = str(round(rightShoeDelegate.rotationZ, 2))
    labelSurface = metricsFont.render(rightShoeRotationZ, 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 7))

    

    rightShoeHeadingX = str(round(rightShoeDelegate.headingX, 2))
    labelSurface = metricsFont.render(rightShoeHeadingX, 1, RED)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 10))

    rightShoeHeadingY = str(round(rightShoeDelegate.headingY, 2))
    labelSurface = metricsFont.render(rightShoeHeadingY, 1, GREEN)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 10))

    rightShoeHeadingZ = str(round(rightShoeDelegate.headingZ, 2))
    labelSurface = metricsFont.render(rightShoeHeadingZ, 1, BLUE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 10))

    labelSurface = metricsFont.render("________________________________________", 1, (255,255,255))
    DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 12))


    labelSurface = metricsFont.render("Toe", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 12))
    
    labelSurface = metricsFont.render("Ball", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 12))

    labelSurface = metricsFont.render("Arch", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 12))

    labelSurface = metricsFont.render("Heel", 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*32, vSpacing * 12))

    rightShoeForceToe = str(round(rightShoeDelegate.forceToe, 2))
    labelSurface = metricsFont.render(rightShoeForceToe, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 13))

    rightShoeForceBall = str(round(rightShoeDelegate.forceBall, 2))
    labelSurface = metricsFont.render(rightShoeForceBall, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 13))

    rightShoeForceArch = str(round(rightShoeDelegate.forceArch, 2))
    labelSurface = metricsFont.render(rightShoeForceArch, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 13))

    rightShoeForceHeel = str(round(rightShoeDelegate.forceHeel, 2))
    labelSurface = metricsFont.render(rightShoeForceHeel, 1, ORANGE)
    DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*32, vSpacing * 13))





    
    
    pygame.display.update()


forceCCCHandle = 0x0010
accelerationCCCHandle = 0x0014
rotationCCCHandle = 0x0018
headingCCCHandle = 0x001c

forceValueHandle = 0x000e
accelerationValueHandle = 0x0012
rotationValueHandle = 0x0016
headingValueHandle = 0x001a

leftShoePeripheral.disconnect()
rightShoePeripheral.disconnect()
pygame.quit()
