import sqlite3

import datetime
import time

import os, sys
from os import path

class BoogioLogger:
    def __init__(self, macAddress):
        self.macAddress = macAddress
        self.datetime = ""
        
    def connect(self):
        databaseExists = False
        directory = path.dirname(str("/home/pi/Desktop/Logs/") + "/")
        try:
            os.mkdir(directory, 0777)
        except OSError as e:
            print ""
        fileName = self.macAddress+ str(".sqlite")
        fullPath = str(directory) + "/" + fileName

        self.conn = sqlite3.connect(fullPath)
        self.c = self.conn.cursor()
        try:
            self.c.execute("CREATE TABLE force(datestamp TEXT, toe INT, ball INT, arch INT, heel INT)")
            self.c.execute("CREATE TABLE acceleration(datestamp TEXT, x REAL, y REAL, z REAL)")
            self.c.execute("CREATE TABLE rotation(datestamp TEXT, x REAL, y REAL, z REAL, w REAL)")
        except sqlite3.OperationalError:
            print "File alread exists. Connecting to that."

    def disconnect(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
        
    def setTime(self, datetime):
        self.datetime = datetime
        
    def getTime(self):
        return self.datetime
    
    def insertForceValues(self, toe, ball, arch, heel):
        date = self.getTime()
        self.c.execute("INSERT INTO force (datestamp, toe, ball, arch, heel) VALUES (?, ?, ?, ?, ?)",(date, toe, ball, arch, heel))
        

    def insertAccelerationValues(self, x, y, z):
        date = self.getTime()
        self.c.execute("INSERT INTO acceleration (datestamp, x, y, z) VALUES (?, ?, ?, ?)",(date, x, y, z))
        

    def insertRotationValues(self, x, y, z, w):
        date = self.getTime()
        self.c.execute("INSERT INTO rotation (datestamp, x, y, z, w) VALUES (?, ?, ?, ?, ?)",(date, x, y, z, w))
        


