#!/usr/bin/env python
from __future__ import print_function
import argparse
from importlib import reload
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
    arg = parser.parse_args(sys.argv[1:])
    
   
    btle.Debugging = arg.verbose

    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

    print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    devices = scanner.scan(arg.timeout)

    

    

                

if __name__ == "__main__":
    main()













