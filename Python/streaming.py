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
import socket

import pygame
from pygame.locals import *

device_to_advertising_data_dictionary = dict()

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
                    string = '\'' + \
                        val.decode('utf-8') + '\''
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

       
        for (sdid, desc, val) in dev.getScanData():
            if sdid in [8, 9]:
                if "boogio" in val.lower():
                    print ('    Device (%s): %s (%s), %d dBm %s' %
                       (status,
                           dev.addr,
                           dev.addrType,
                           dev.rssi,
                           ('' if dev.connectable else '(not connectable)'))
                       )
                    for (sdid, desc, val) in dev.getScanData():
                        #print("desc = " + str(desc) + " val = " + str(val))
                        if desc == "Manufacturer":
                            device_to_advertising_data_dictionary[str(dev.addr)] = str(val)
                            print("device_to_advertising_data_dictionary[" + str(dev.addr) + "] = " + str(val))
                        if sdid in [8, 9]:
                            print ('\t' + desc + ': \'' + val + '\'')
                        else:
                            print ('\t' + desc + ': <' + val + '>')

        
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
    parser.add_argument('-p', '--port', action='store', help='relay all readings over this TCP port')
    parser.add_argument('-e', '--headless', action='store_true', help='run without graphics (improves performance)')
    arg = parser.parse_args(sys.argv[1:])
    
    #print("arg = " + str(arg))
    
    if arg.bpx != None:        
        print("arg.bpx = " + str(arg.bpx))
        PERIPHERAL_UUID = str(arg.bpx)
    else:
        PERIPHERAL_UUID = "dc:80:07:ef:8b:cf"
        #PERIPHERAL_UUID = "f5:47:18:cf:9c:dc"
        #print("pass the hardware address to this script to connect to that device")
        #print("usage: -b <boogio:device:hardware:address>")
        #print("You can find the hardware address by running scanner.py")
        #return
        

    if arg.port != None:
        TRANSMISSION_PORT = int(arg.port)
        print("arg.port = " + str(arg.port))
        print("TRANSMISSION_PORT = " + str(TRANSMISSION_PORT))
    else:
        TRANSMISSION_PORT = -1
        
    if arg.headless != None:
        headless = True
    else:
        headless = False

    btle.Debugging = arg.verbose

    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

    print ("Scanning for devices...")
    devices = scanner.scan(arg.timeout)
    
    

    if arg.discover:
        print ("Discovering services...")

        for d in devices:
            if not d.connectable:
                continue

            print ("    Connecting to", d.addr + ":")
            
            

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
    
    device_is_left_shoe = False
    device_is_right_shoe = False
    if device_to_advertising_data_dictionary[str(PERIPHERAL_UUID)] == "ffff05":
        device_is_right_shoe = True
        print("Device is Right Shoe")
    elif device_to_advertising_data_dictionary[str(PERIPHERAL_UUID)] == "ffff04":
        device_is_left_shoe = True
        print("Device is Right Shoe")
    else:
        print("DEVICE NOT RECOGNIZED!")


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
    buffer1Characteristic.write(setSampleRateByteString, withResponse = True)


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
    #sys.setdefaultencoding('utf8')
               
    # upate timestamp
    print("Timestamp = " + str(current_time))
    #boogioPeripheral.writeCharacteristic(forceCharacteristicHandle, byteString, True)
    buffer1Characteristic.write(byteString, withResponse = True)



    
        

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
    
    
    
    
    if TRANSMISSION_PORT > 0:
        # create a socket object
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        host = ''

        # bind to the port
        serversocket.bind((host, TRANSMISSION_PORT))

        print("Waiting for tcp socket connection over port " + str(TRANSMISSION_PORT) + "...")
        
        # queue up to 5 requests
        serversocket.listen(5)
        clientsocket, addr = serversocket.accept()
        

    shouldQuit = False
    while not shouldQuit:
        for event in pygame.event.get():
            if event.type == QUIT:
                shouldQuit = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    shouldQuit = True

        boogioPeripheral.waitForNotifications(0)

        accelerationX = str(round(boogioDelegate.accelerationX, 2))
        accelerationY = str(round(boogioDelegate.accelerationY, 2))
        accelerationZ = str(round(boogioDelegate.accelerationZ, 2))
        
        rotationX = str(round(boogioDelegate.rotationX, 2))
        rotationY = str(round(boogioDelegate.rotationY, 2))
        rotationZ = str(round(boogioDelegate.rotationZ, 2))
        rotationW = str(round(boogioDelegate.rotationW, 2))
        
        force012String = str(round(boogioDelegate.force012, 2))
        force34String = str(round(boogioDelegate.force34, 2))
        force567String = str(round(boogioDelegate.force567, 2))
        
        if headless == True:
            header = ""
            if device_is_left_shoe:
                header = header + "ls"
            elif device_is_right_shoe:
                header = header + "rs"
            
            header = header + "bl"
            message = header + " " + accelerationX + " " + accelerationY + " " + accelerationZ + " " \
                      + rotationX + " " + rotationY + " " + rotationZ + " " + rotationW + " " \
                      + force012String + " " + force34String + " " + force567String
            print(message)
            if TRANSMISSION_PORT > 0:
                try:
                    clientsocket.send(message.encode('ascii'))
                except (BrokenPipeError):
                    shouldQuit = True
                      
        else:
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
            
            labelSurface = metricsFont.render("[Gravities*1000]:", 1, (255,255,255))
            DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 4))

            labelSurface = metricsFont.render("Rotation ", 1, (255,255,255))
            DISPLAYSURF.blit(labelSurface, (cursorX, vSpacing * 6))

            labelSurface = metricsFont.render("[quaternion*1000]:", 1, (255,255,255))
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
            

            
            labelSurface = metricsFont.render(accelerationX, 1, RED)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 4))

            
            labelSurface = metricsFont.render(accelerationY, 1, GREEN)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 4))

            
            labelSurface = metricsFont.render(accelerationZ, 1, BLUE)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 4))



            
            labelSurface = metricsFont.render(rotationX, 1, RED)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 7))

            
            labelSurface = metricsFont.render(rotationY, 1, GREEN)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 7))

            labelSurface = metricsFont.render(rotationZ, 1, BLUE)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 7))

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
            
            

            
            labelSurface = metricsFont.render(force012String, 1, ORANGE)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*8, vSpacing * 11))

            
            labelSurface = metricsFont.render(force34String, 1, ORANGE)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*16, vSpacing * 11))

            
            labelSurface = metricsFont.render(force567String, 1, ORANGE)
            DISPLAYSURF.blit(labelSurface, (cursorX + hSpacing*24, vSpacing * 11))

            


            
            pygame.display.update()


    if TRANSMISSION_PORT > 0:
        clientsocket.send(str("c0").encode('ascii'))
        
    clientsocket.close()
    boogioPeripheral.disconnect()
    pygame.quit()
    
                

if __name__ == "__main__":
    main()












