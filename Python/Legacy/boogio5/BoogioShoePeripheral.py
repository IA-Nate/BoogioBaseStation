import struct
import sys
sys.path.append('/home/pi/Development/libraries/bluepy/bluepy/bluepy')
import btle
from btle import UUID, Peripheral, BTLEException
import os
import pygame
from pygame.locals import *
import binascii
#from BoogioLogger import *
from settings import *

                
class BoogioShoePeripheral(btle.DefaultDelegate):
    
    def __init__(self, macAddress):
        
        
        os.system("sudo hciconfig hci0 up")
        self.macAddress = macAddress
        self.connection = btle.Peripheral(self.macAddress, "random")
        
        btle.DefaultDelegate.__init__(self)
        self.delegate = self.connection.setDelegate(self)
        
        self.toe = 0
        self.ball = 0
        self.arch = 0
        self.heel = 0
        
        self.accelerationX = 0.0
        self.accelerationY = 0.0
        self.accelerationZ = 0.0
        self.rotationX = 0.0
        self.rotationY = 0.0
        self.rotationZ = 0.0
        self.orientationX = 0.0
        self.orientationY = 0.0
        self.orientationZ = 0.0
        
        self.temperatureC = 0.0

        self.battery = ""

        self.FORCE = 0
        self.ACCELERATION = 1
        self.ROTATION = 2
        self.ORIENTATION = 3
        self.TEMPERATURE = 4
        self.GENERIC_COMMUNICATION = 5

        self.forceCCCHandle = 0x0010
        self.accelerationCCCHandle = 0x0014
        self.rotationCCCHandle = 0x0018
        self.orientationCCCHandle = 0x001c
        self.temperatureCCCHandle = 0x0020
        self.batteryCCCHandle = 0x0026
        self.bodySensorLocationCCCHandle = 0x0034
        self.genericCommunicationCCCHandle = 0x002e
        

        self.forceValueHandle = 0x000e
        self.accelerationValueHandle = 0x0012
        self.rotationValueHandle = 0x0016
        self.orientationValueHandle = 0x001a
        self.temperatureValueHandle = 0x001e
        self.batteryValueHandle = 0x0025
        self.bodySensorLocationValueHandle = 0x0022
        self.genericCommunicationValueHandle = 0x002c
        

        
        self.SYNC_STEP_1_RESPONSE_CODE = 2
        self.SYNC_STEP_2_RESPONSE_CODE = 4
        self.SYNC_STEP_3_RESPONSE_CODE = 6
        self.SYNC_DONE_RESPONSE_CODE = 7

        self.SET_TIME_HEADER_CODE = 0x00
        self.SYNC_STEP_1_HEADER_CODE = chr(1)
        self.SYNC_STEP_2_HEADER_CODE = chr(3)
        self.SYNC_STEP_3_HEADER_CODE = chr(5)

        self.lastReadingPopped = False
        self.synchronizing = False
        
        print btle.Peripheral.status(self.connection)

        self.GENERIC_COMMUNICATION_SLEEP_PERIOD = 100
        self.SENSOR_SERVICE_SLEEP_PERIOD = 50

        #self.logger = BoogioLogger(macAddress)
        #self.logger.connect()
        self.readingsSynchronized = 0

    def handleNotification(self, cHandle, data):
        
        if cHandle == self.forceValueHandle:
                self.toe = struct.unpack('<H', data[0:2])[0]
                self.ball = struct.unpack('<H', data[2:4])[0]
                self.arch = struct.unpack('<H', data[4:6])[0]
                self.heel = struct.unpack('<H', data[6:8])[0]
                
        elif cHandle == self.accelerationValueHandle:
                self.accelerationX = struct.unpack('<H', data[0:2])[0]
                self.accelerationY = struct.unpack('<H', data[2:4])[0]
                self.accelerationZ = struct.unpack('<H', data[4:6])[0]

                #2's complement
                if self.accelerationX > HALF_OF_MAX_SHORT_VALUE:
                    self.accelerationX = self.accelerationX - MAX_SHORT_VALUE
                if self.accelerationY > HALF_OF_MAX_SHORT_VALUE:
                    self.accelerationY = self.accelerationY - MAX_SHORT_VALUE
                if self.accelerationZ > HALF_OF_MAX_SHORT_VALUE:
                    self.accelerationZ = self.accelerationZ - MAX_SHORT_VALUE

                self.accelerationX = self.accelerationX * ACCELERATION_CONVERSION_COEFFICIENT
                self.accelerationY = self.accelerationY * ACCELERATION_CONVERSION_COEFFICIENT
                self.accelerationZ = self.accelerationZ * ACCELERATION_CONVERSION_COEFFICIENT
                
                
        elif cHandle == self.rotationValueHandle:
                self.rotationX = struct.unpack('<H', data[0:2])[0]
                self.rotationY = struct.unpack('<H', data[2:4])[0]
                self.rotationZ = struct.unpack('<H', data[4:6])[0]

                if self.rotationX > HALF_OF_MAX_SHORT_VALUE:
                    self.rotationX = self.rotationX - MAX_SHORT_VALUE
                if self.rotationY > HALF_OF_MAX_SHORT_VALUE:
                    self.rotationY = self.rotationY - MAX_SHORT_VALUE
                if self.rotationZ > HALF_OF_MAX_SHORT_VALUE:
                    self.rotationZ = self.rotationZ - MAX_SHORT_VALUE

                self.rotationX = self.rotationX * ROTATION_CONVERSION_COEFFICIENT
                self.rotationY = self.rotationY * ROTATION_CONVERSION_COEFFICIENT
                self.rotationZ = self.rotationZ * ROTATION_CONVERSION_COEFFICIENT
                
                
        elif cHandle == self.orientationValueHandle:

                self.orientationX = struct.unpack('<H', data[0:2])[0]
                self.orientationY = struct.unpack('<H', data[2:4])[0]
                self.orientationZ = struct.unpack('<H', data[4:6])[0]
                

                #2's complement
                if self.orientationX > HALF_OF_MAX_SHORT_VALUE:
                    self.orientationX = self.orientationX - MAX_SHORT_VALUE
                if self.orientationY > HALF_OF_MAX_SHORT_VALUE:
                    self.orientationY = self.orientationY - MAX_SHORT_VALUE
                if self.orientationZ > HALF_OF_MAX_SHORT_VALUE:
                    self.orientationZ = self.orientationZ - MAX_SHORT_VALUE
                
                self.orientationX = self.orientationX / ORIENTATION_CONVERSION_COEFFICIENT
                self.orientationY = self.orientationY / ORIENTATION_CONVERSION_COEFFICIENT
                self.orientationZ = self.orientationZ / ORIENTATION_CONVERSION_COEFFICIENT
               
                
        elif cHandle == self.temperatureValueHandle:
            self.temperatureC = struct.unpack('<H', data[0:2])[0]
            if self.temperatureC > HALF_OF_MAX_SHORT_VALUE:
                    self.temperatureC = self.temperatureC - MAX_SHORT_VALUE

        elif cHandle == self.genericCommunicationValueHandle:
                responseCode = struct.unpack('B', data[0:1])[0]
                
                if responseCode == self.SYNC_STEP_1_RESPONSE_CODE:
                    #print "Timestamp Response"
                    year  = struct.unpack('<H', data[1:3])[0]
                    month = struct.unpack('B', data[3])[0]
                    day = struct.unpack('B', data[4])[0]
                    hour = struct.unpack('B', data[5])[0]
                    minute = struct.unpack('B', data[6])[0]
                    second = struct.unpack('B', data[7])[0]
                    millisecond = struct.unpack('<H', data[8:10])[0]

                    #self.logger.setTime(year, month, day, hour, minute, second, millisecond)
                    
                    self.performSyncStep(2)
                    
                elif responseCode == self.SYNC_STEP_2_RESPONSE_CODE:
                    #print "    Force/Mag Response"
                    toe = struct.unpack('<H', data[1:3])[0]
                    ball = struct.unpack('<H', data[3:5])[0]
                    arch = struct.unpack('<H', data[5:7])[0]
                    heel = struct.unpack('<H', data[7:9])[0]
                    orientationX = struct.unpack('<H', data[9:11])[0]
                    orientationY = struct.unpack('<H', data[11:13])[0]
                    orientationZ = struct.unpack('<H', data[13:15])[0]
                    

                    #2's complement
                    if orientationX > HALF_OF_MAX_SHORT_VALUE:
                        orientationX = orientationX - MAX_SHORT_VALUE
                    if orientationY > HALF_OF_MAX_SHORT_VALUE:
                        orientationY = orientationY - MAX_SHORT_VALUE
                    if orientationZ > HALF_OF_MAX_SHORT_VALUE:
                        orientationZ = orientationZ - MAX_SHORT_VALUE
                    

                    

                    #self.logger.insertForceValues(toe, ball, arch, heel)
                    #self.logger.insertOrientationValues(orientationX, orientationY, orientationZ)
               
                    self.performSyncStep(3)
                elif responseCode == self.SYNC_STEP_3_RESPONSE_CODE:
                    #print "    Acc/Gyr/Temp Response"
                    accelerationX = struct.unpack('<H', data[1:3])[0]
                    accelerationY = struct.unpack('<H', data[3:5])[0]
                    accelerationZ = struct.unpack('<H', data[5:7])[0]

                    rotationX = struct.unpack('<H', data[7:9])[0]
                    rotationY = struct.unpack('<H', data[9:11])[0]
                    rotationZ = struct.unpack('<H', data[11:13])[0]
                    temperatureC = struct.unpack('<H', data[13:15])[0]

                    #2's complement
                    if accelerationX > HALF_OF_MAX_SHORT_VALUE:
                        accelerationX = accelerationX - MAX_SHORT_VALUE
                    if accelerationY > HALF_OF_MAX_SHORT_VALUE:
                        accelerationY = accelerationY - MAX_SHORT_VALUE
                    if accelerationZ > HALF_OF_MAX_SHORT_VALUE:
                        accelerationZ = accelerationZ - MAX_SHORT_VALUE
                    
                    if rotationX > HALF_OF_MAX_SHORT_VALUE:
                        rotationX = rotationX - MAX_SHORT_VALUE
                    if rotationY > HALF_OF_MAX_SHORT_VALUE:
                        rotationY = rotationY - MAX_SHORT_VALUE
                    if rotationZ > HALF_OF_MAX_SHORT_VALUE:
                        rotationZ = rotationZ - MAX_SHORT_VALUE
                    if temperatureC > HALF_OF_MAX_SHORT_VALUE:
                        temperatureC = temperatureC - MAX_SHORT_VALUE
                        
                    accelerationX = accelerationX / 1000.0
                    accelerationY = accelerationY / 1000.0
                    accelerationZ = accelerationZ / 1000.0

                    #self.logger.insertAccelerationValues(accelerationX, accelerationY, accelerationZ)
                    #self.logger.insertRotationValues(rotationX, rotationY, rotationZ)
                    #self.logger.insertTemperatureValues(temperatureC)

                    self.readingsSynchronized = self.readingsSynchronized + 1
                    
                    
                    if self.lastReadingPopped:
                        #self.logger.commit()
                        self.synchronizing = False
                        print "Sync Done"
                    
                elif responseCode == self.SYNC_DONE_RESPONSE_CODE:
                    self.lastReadingPopped = True
                    
                
                
                

        
    def disconnect(self):
        self.connection.disconnect()

    #CCC Handles

    def performSyncStep(self, step):
        if step == 1:
            self.connection.writeCharacteristic(self.genericCommunicationValueHandle, self.SYNC_STEP_1_HEADER_CODE)     #set the ccc handle to notify (3)
        elif step == 2:
            self.connection.writeCharacteristic(self.genericCommunicationValueHandle, self.SYNC_STEP_2_HEADER_CODE)     #set the ccc handle to notify (3)
        elif step == 3:
            self.connection.writeCharacteristic(self.genericCommunicationValueHandle, self.SYNC_STEP_3_HEADER_CODE)     #set the ccc handle to notify (3)
        self.connection.waitForNotifications(self.GENERIC_COMMUNICATION_SLEEP_PERIOD/1000 + 0.4)
        
    def performSyncTick(self):
        self.performSyncStep(1)    
        
    def updateTime(self):
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
        byteString.append(self.SET_TIME_HEADER_CODE)
        byteString.append(yearLowByte.decode("hex"))
        byteString.append(yearHighByte.decode("hex"))
        byteString.append(int(month))
        byteString.append(int(day))
        byteString.append(int(hour))
        byteString.append(int(minute))
        byteString.append(int(second))
        byteString.append(millisecondLowByte.decode("hex"))
        byteString.append(millisecondHighByte.decode("hex"))
        

        
        print yearLowByte
        print yearHighByte
           
        self.connection.writeCharacteristic(self.genericCommunicationValueHandle, byteString)
    
    def subscribeToNotifications(self, characteristicEnumeration):
        value = "3"
        if characteristicEnumeration == self.FORCE:
            self.connection.writeCharacteristic(self.forceCCCHandle, value, True)     #set the ccc handle to notify (3)
        elif characteristicEnumeration == self.ACCELERATION:
            self.connection.writeCharacteristic(self.accelerationCCCHandle, value, True)     #set the ccc handle to notify (3)
        elif characteristicEnumeration == self.ROTATION:
            self.connection.writeCharacteristic(self.rotationCCCHandle, value, True)     #set the ccc handle to notify (3)
        elif characteristicEnumeration == self.ORIENTATION:
            self.connection.writeCharacteristic(self.orientationCCCHandle, value, True)     #set the ccc handle to notify (3)
        elif characteristicEnumeration == self.TEMPERATURE:
            self.connection.writeCharacteristic(self.temperatureCCCHandle, value, True)     #set the ccc handle to notify (3)
        elif characteristicEnumeration == self.GENERIC_COMMUNICATION:
            self.connection.writeCharacteristic(self.genericCommunicationCCCHandle, value, True)     #set the ccc handle to notify (3)
               
    def unsubscribeFromNotifications(self, characteristicEnumeration):
        value = "0"
        if characteristicEnumeration == self.FORCE:
            self.connection.writeCharacteristic(self.forceCCCHandle, value)     #set the ccc handle to notify (0)
        elif characteristicEnumeration == self.ACCELERATION:
            self.connection.writeCharacteristic(self.accelerationCCCHandle, value)     #set the ccc handle to notify (0)
        elif characteristicEnumeration == self.ROTATION:
            self.connection.writeCharacteristic(self.rotationCCCHandle, value)     #set the ccc handle to notify (0)
        elif characteristicEnumeration == self.ORIENTATION:
            self.connection.writeCharacteristic(self.orientationCCCHandle, value)     #set the ccc handle to notify (0)
        elif characteristicEnumeration == self.TEMPERATURE:
            self.connection.writeCharacteristic(self.temperatureCCCHandle, value)     #set the ccc handle to notify (0)
        elif characteristicEnumeration == self.GENERIC_COMMUNICATION:
            self.connection.writeCharacteristic(self.genericCommunicationCCCHandle, value)     #set the ccc handle to notify (0)
       

    def readBattery(self):
        battery_level_uuid = UUID(0x2A19)
        ch = self.connection.getCharacteristics(uuid=battery_level_uuid)[0]
        val = binascii.b2a_hex(ch.read())
        val = binascii.unhexlify(val)
        self.battery = struct.unpack('B', val)[0]
