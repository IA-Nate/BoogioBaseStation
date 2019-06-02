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

import pygame
from pygame.locals import *


#PERIPHERAL_UUID = "dc:80:07:ef:8b:cf"
#PERIPHERAL_UUID = "f5:47:18:cf:9c:dc"

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

        self.force0 = 0.00
        self.force1 = 0.00
        self.force2 = 0.00
        self.force3 = 0.00
        self.force4 = 0.00
        self.force5 = 0.00
        self.force6 = 0.00
        self.force7 = 0.00
        
        self.force012 = 0.00
        self.force34  = 0.00
        self.force567 = 0.00

        self.accelerationX = 0.000
        self.accelerationY = 0.000
        self.accelerationZ = 0.000

        self.rotationX = 0.000
        self.rotationY = 0.000
        self.rotationZ = 0.000
        self.rotationW = 0.000

        self.buffer1CharacteristicHandle = None

    def handleNotification(self, hnd, data):

        #print(data)
        #print("\n")
        
        #Debug print repr(data)
        if (hnd == self.buffer1CharacteristicHandle):
            self.accelerationX = struct.unpack('<H', data[0:2])[0]
            self.accelerationY = struct.unpack('<H', data[2:4])[0]
            self.accelerationZ = struct.unpack('<H', data[4:6])[0]
            self.rotationX     = struct.unpack('<H', data[6:8])[0]
            self.rotationY     = struct.unpack('<H', data[8:10])[0]
            self.rotationZ     = struct.unpack('<H', data[10:12])[0]
            self.rotationW     = struct.unpack('<H', data[12:14])[0]
            self.force012      = struct.unpack('<H', data[14:16])[0]
            self.force34       = struct.unpack('<H', data[16:18])[0]
            self.force567      = struct.unpack('<H', data[18:20])[0]

            #2's complement
            if(self.accelerationX > self.HALF_OF_MAX_SHORT_VALUE):
               self.accelerationX = self.accelerationX - self.MAX_SHORT_VALUE
            if(self.accelerationY > self.HALF_OF_MAX_SHORT_VALUE):
               self.accelerationY = self.accelerationY - self.MAX_SHORT_VALUE
            if(self.accelerationZ > self.HALF_OF_MAX_SHORT_VALUE):
               self.accelerationZ = self.accelerationZ - self.MAX_SHORT_VALUE


            #2's complement
            if(self.rotationX > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationX = self.rotationX - self.MAX_SHORT_VALUE
            if(self.rotationY > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationY = self.rotationY - self.MAX_SHORT_VALUE
            if(self.rotationZ > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationZ = self.rotationZ - self.MAX_SHORT_VALUE
            if(self.rotationW > self.HALF_OF_MAX_SHORT_VALUE):
               self.rotationW = self.rotationW - self.MAX_SHORT_VALUE


        else:
            teptep = binascii.b2a_hex(data)
            print('Notification: UNKOWN: hnd {}, data {}'.format(hnd, teptep))
            

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i    


def main():
        
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hci', action='store', type=int, default=0, help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=4, help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128, help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true', help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true', help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n', '--new', action='store_true', help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    parser.add_argument('-b', '--bpx', action='store', help='connect to device with this address')
    arg = parser.parse_args(sys.argv[1:])
    
    print("arg = " + str(arg))
    print("arg.bpx = " + str(arg.bpx))
    PERIPHERAL_UUID = str(arg.bpx)


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

    boogioPeripheral = Peripheral(PERIPHERAL_UUID, "random")

    boogioDelegate = MyDelegate()
    boogioPeripheral.setDelegate(boogioDelegate)

    boogioShoeSensorService = None

    buffer1Characteristic = None


    CCCD_UUID = 0x2902

    print("Boogio Peripheral:")
    for svc in boogioPeripheral.services:
        print("      ")
        print(str(svc))
        if svc.uuid == "f3641400-00B0-4240-ba50-05ca45bf8abc":
            boogioShoeSensorService = boogioPeripheral.getServiceByUUID(svc.uuid)
            for characteristic in boogioShoeSensorService.getCharacteristics():
                print(characteristic)
                if characteristic.uuid == "f3641402-00B0-4240-ba50-05ca45bf8abc":
                    buffer1Characteristic = characteristic
                    boogioDelegate.buffer1CharacteristicHandle = characteristic.getHandle()
                    buffer1CCCD = characteristic.getDescriptors(forUUID=CCCD_UUID)[0]
                    buffer1CCCD.write(b"\x01\x00", True)
                

    setSampleRateByteString = bytearray()
    setSampleRateByteString.append(0x04) # set sample rate command
    setSampleRateByteString.append(0x05) # frequency argument (Hz)
    buffer1Characteristic.write(str(setSampleRateByteString), withResponse = True)


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
    buffer1Characteristic.write(str(byteString), withResponse = True)





    #pygame graphics
    pygame.init()
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 400
    READING_SCALE = 100
    WINDOW_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
    DISPLAYSURF = pygame.display.set_mode(WINDOW_RESOLUTION, pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
    pygame.display.set_caption("Boogio 6 Data Streaming Example")



    metricsFont = pygame.font.SysFont("comicsans", 24)

    BLACK = (0,0,0)
    RED = (255,60,120)
    GREEN = (58,255,118)
    BLUE = (64,128,255)
    ORANGE = (252, 97, 38)
    YELLOW = (255, 255, 15)

    shouldQuit = False
    while not shouldQuit:
        for event in pygame.event.get():
            if event.type == QUIT:
                shouldQuit = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    shouldQuit = True

        boogioPeripheral.waitForNotifications(0)

        hSpacing = 13
        vSpacing = 24
        cursorX = hSpacing
        cursorY = vSpacing
        

        #labels 
        DISPLAYSURF.fill(BLACK)
        labelSurface = metricsFont.render("Peripheral: ", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing))

        
        labelSurface = metricsFont.render("Acceleration ", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 3))
        
        labelSurface = metricsFont.render("[Gravities/1000]:", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 4))

        labelSurface = metricsFont.render("Rotation ", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 6))

        labelSurface = metricsFont.render("[quaternion/1000]:", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 7))

        labelSurface = metricsFont.render("Force ", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 10))

        labelSurface = metricsFont.render("[ADC]:", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 11))

        
        # readings
        cursorX = SCREEN_WIDTH / 8

        labelSurface = metricsFont.render(PERIPHERAL_UUID, 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing))

        labelSurface = metricsFont.render("____________________________________________________________________", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (hSpacing, vSpacing * 1))

        labelSurface = metricsFont.render("____________________________________________________________________", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (hSpacing, vSpacing * 2))

        labelSurface = metricsFont.render("X", 1, RED)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 2))

        
        labelSurface = metricsFont.render("Y", 1, GREEN)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 2))

        
        labelSurface = metricsFont.render("Z", 1, BLUE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 2))
        
        labelSurface = metricsFont.render("W", 1, YELLOW)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*32, vSpacing * 2))
        

        accelerationX = str(round(boogioDelegate.accelerationX, 2))
        labelSurface = metricsFont.render(accelerationX, 1, RED)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 4))

        accelerationY = str(round(boogioDelegate.accelerationY, 2))
        labelSurface = metricsFont.render(accelerationY, 1, GREEN)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 4))

        accelerationZ = str(round(boogioDelegate.accelerationZ, 2))
        labelSurface = metricsFont.render(accelerationZ, 1, BLUE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 4))



        rotationX = str(round(boogioDelegate.rotationX, 2))
        labelSurface = metricsFont.render(rotationX, 1, RED)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 7))

        rotationY = str(round(boogioDelegate.rotationY, 2))
        labelSurface = metricsFont.render(rotationY, 1, GREEN)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 7))

        rotationZ = str(round(boogioDelegate.rotationZ, 2))
        labelSurface = metricsFont.render(rotationZ, 1, BLUE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 7))

        rotationW = str(round(boogioDelegate.rotationW, 2))
        labelSurface = metricsFont.render(rotationW, 1, YELLOW)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*32, vSpacing * 7))
        
        
        
        
        labelSurface = metricsFont.render("____________________________________________________________________", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (hSpacing, vSpacing * 8))
        
        labelSurface = metricsFont.render("____________________________________________________________________", 1, (255,255,255))
        DISPLAYSURF.blit(labelSurface, (hSpacing, vSpacing * 9))


        labelSurface = metricsFont.render("(F0+F1+F2)/3", 1, ORANGE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 9))
        
        labelSurface = metricsFont.render("(F3+F4)/2", 1, ORANGE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 9))

        labelSurface = metricsFont.render("(F5+F6+F7)/3", 1, ORANGE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 9))
        
        

        force012String = str(round(boogioDelegate.force012, 2))
        labelSurface = metricsFont.render(force012String, 1, ORANGE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 11))

        force34String = str(round(boogioDelegate.force34, 2))
        labelSurface = metricsFont.render(force34String, 1, ORANGE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 11))

        force567String = str(round(boogioDelegate.force567, 2))
        labelSurface = metricsFont.render(force567String, 1, ORANGE)
        DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 11))

        


        
        pygame.display.update()



    boogioPeripheral.disconnect()
    pygame.quit()

                

if __name__ == "__main__":
    main()












