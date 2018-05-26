import csv
import datetime
import time
from settings import *

class BoogioCSVLogger:
    def __init__(self):
        self.path = CSV_LOG_DIRECTORY
        self.filePath = ''
        self.writer = ''
        self.file = ''
    def getTime(self):
        return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    def open(self):
        self.filePath = self.path + str(self.getTime()) + '.csv'
        self.file = open(self.filePath, 'wt')
        try:
            self.writer = csv.writer(self.file)
            self.writer.writerow(('TimeStamp', 'LeftToeForce',      'LeftBallForce',     'LeftArchForce', 'LeftHeelForce',
                              'LeftAccelerationX', 'LeftAccelerationY', 'LeftAccelerationZ',
                              'LeftRotationX',     'LeftRotationY',     'LeftRotationZ',
                              'LeftOrientationX',  'LeftOrientationY',  'LeftOrientationZ',
                              'RightToeForce',      'RightBallForce',     'RightArchForce', 'RightHeelForce',
                              'RightAccelerationX', 'RightAccelerationY', 'RightAccelerationZ',
                              'RightRotationX',     'RightRotationY',     'RightRotationZ',
                              'RightOrientationX',  'RightOrientationY',  'RightOrientationZ'))
        finally:
            print ""
    def writeRow(self, LeftToeForce, LeftBallForce, LeftArchForce, LeftHeelForce, LeftAccelerationX, LeftAccelerationY, LeftAccelerationZ, LeftRotationX, LeftRotationY, LeftRotationZ, LeftOrientationX,  LeftOrientationY,  LeftOrientationZ, RightToeForce, RightBallForce, RightArchForce, RightHeelForce, RightAccelerationX, RightAccelerationY, RightAccelerationZ, RightRotationX, RightRotationY, RightRotationZ, RightOrientationX, RightOrientationY, RightOrientationZ):
        timeStamp = str(self.getTime())
        self.writer.writerow((timeStamp, LeftToeForce, LeftBallForce, LeftArchForce, LeftHeelForce, LeftAccelerationX, LeftAccelerationY, LeftAccelerationZ, LeftRotationX, LeftRotationY, LeftRotationZ, LeftOrientationX,  LeftOrientationY,  LeftOrientationZ, RightToeForce, RightBallForce, RightArchForce, RightHeelForce, RightAccelerationX, RightAccelerationY, RightAccelerationZ, RightRotationX, RightRotationY, RightRotationZ, RightOrientationX, RightOrientationY, RightOrientationZ))

    def close(self):
            self.file.close()
            print "log saved at " + self.filePath
        
