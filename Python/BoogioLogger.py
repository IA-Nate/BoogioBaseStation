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
            os.mkdir(directory, 0o777)
        except OSError as e:
            print("")
        fileName = self.macAddress+ str(".sqlite")
        fullPath = str(directory) + "/" + fileName

        self.conn = sqlite3.connect(fullPath)
        self.c = self.conn.cursor()
        try:
            self.c.execute("CREATE TABLE Buffer_0(datestamp TEXT, force0 INT, force1 INT, force2 INT, force3 INT, force4 INT, force5 INT)")
            self.c.execute("CREATE TABLE Buffer_1(datestamp TEXT, force6 INT, force7 INT, x REAL, y REAL, z REAL)")
            self.c.execute("CREATE TABLE Buffer_2(datestamp TEXT, x REAL, y REAL, z REAL, w REAL)")
        except sqlite3.OperationalError:
            print("File alread exists. Connecting to that.")

    def disconnect(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
        
    def setTime(self, datetime):
        self.datetime = datetime
        
    def getTime(self):
        return self.datetime
    
    def insertBuffer0Values(self, date, force0, force1, force2, force3, force4, force5):
        self.c.execute("INSERT INTO Buffer_0 (datestamp, force0, force1, force2, force3, force4, force5) VALUES (?, ?, ?, ?, ?, ?, ?)",(date, force0, force1, force2, force3, force4, force5))
        

    def insertBuffer1Values(self, date, force6, force7, x, y, z):
        self.c.execute("INSERT INTO Buffer_1 (datestamp, force6, force7, x, y, z) VALUES (?, ?, ?, ?, ?, ?)",(date, force6, force7, x, y, z))
        

    def insertBuffer2Values(self, date, x, y, z, w):
        self.c.execute("INSERT INTO Buffer_2 (datestamp, x, y, z, w) VALUES (?, ?, ?, ?, ?)",(date, x, y, z, w))
        


