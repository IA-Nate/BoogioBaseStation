#!/usr/bin/env python
from BoogioCSVLogger import *
from settings import *
from BoogioShoePeripheral import *


def main():

    subscribeToSensors = True
    shouldQuit = False
    connected = False

    #this is necessary so that duplicate rows do not fill up the CSV files
    previousLeftToeValue = 0.0
    previousLeftBallValue = 0.0
    previousLeftArchValue = 0.0
    previousLeftHeelValue = 0.0
    previousLeftAccelerationXValue = 0.0
    previousLeftAccelerationYValue = 0.0
    previousLeftAccelerationZValue = 0.0
    previousLeftRotationXValue = 0.0
    previousLeftRotationYValue = 0.0
    previousLeftRotationZValue = 0.0
    previousLeftOrientationXValue = 0.0
    previousLeftOrientationYValue = 0.0
    previousLeftOrientationZValue = 0.0

    previousRightToeValue = 0.0
    previousRightBallValue = 0.0
    previousRightArchValue = 0.0
    previousRightHeelValue = 0.0
    previousRightAccelerationXValue = 0.0
    previousRightAccelerationYValue = 0.0
    previousRightAccelerationZValue = 0.0
    previousRightRotationXValue = 0.0
    previousRightRotationYValue = 0.0
    previousRightRotationZValue = 0.0
    previousRightOrientationXValue = 0.0
    previousRightOrientationYValue = 0.0
    previousRightOrientationZValue = 0.0
    
    while not shouldQuit:
        
        try:
            
            leftPeripheral = BoogioShoePeripheral(LEFT_PERIPHERAL_UUID)
            leftPeripheral.subscribeToNotifications(leftPeripheral.FORCE)
            leftPeripheral.subscribeToNotifications(leftPeripheral.ACCELERATION)
            leftPeripheral.subscribeToNotifications(leftPeripheral.ROTATION)
            leftPeripheral.subscribeToNotifications(leftPeripheral.ORIENTATION)

            rightPeripheral = BoogioShoePeripheral(RIGHT_PERIPHERAL_UUID)
            rightPeripheral.subscribeToNotifications(rightPeripheral.FORCE)
            rightPeripheral.subscribeToNotifications(rightPeripheral.ACCELERATION)
            rightPeripheral.subscribeToNotifications(rightPeripheral.ROTATION)
            rightPeripheral.subscribeToNotifications(rightPeripheral.ORIENTATION)
            
            connected = True

            logger = BoogioCSVLogger()
            logger.open()

            print "Started Logging Boogio Data to "
            print logger.filePath
            print "Ctrl-C to disconnect, stop recording and exit"
            
            while not shouldQuit:
                leftPeripheral.connection.waitForNotifications(0.001)
                rightPeripheral.connection.waitForNotifications(0.001)
                duplicateRow = True
                if(leftPeripheral.toe != previousLeftToeValue \
                   or leftPeripheral.ball != previousLeftBallValue \
                   or leftPeripheral.arch != previousLeftArchValue \
                   or leftPeripheral.heel != previousLeftHeelValue \
                   or leftPeripheral.accelerationX != previousLeftAccelerationXValue \
                   or leftPeripheral.accelerationY != previousLeftAccelerationYValue \
                   or leftPeripheral.accelerationZ != previousLeftAccelerationZValue \
                   or leftPeripheral.rotationX != previousLeftRotationXValue \
                   or leftPeripheral.rotationY != previousLeftRotationYValue \
                   or leftPeripheral.rotationZ != previousLeftRotationZValue \
                   or leftPeripheral.orientationX != previousLeftOrientationXValue \
                   or leftPeripheral.orientationY != previousLeftOrientationYValue \
                   or leftPeripheral.orientationZ != previousLeftOrientationZValue \
                   or rightPeripheral.toe != previousRightToeValue \
                   or rightPeripheral.ball != previousRightBallValue \
                   or rightPeripheral.arch != previousRightArchValue \
                   or rightPeripheral.heel != previousRightHeelValue \
                   or rightPeripheral.accelerationX != previousRightAccelerationXValue \
                   or rightPeripheral.accelerationY != previousRightAccelerationYValue \
                   or rightPeripheral.accelerationZ != previousRightAccelerationZValue \
                   or rightPeripheral.rotationX != previousRightRotationXValue \
                   or rightPeripheral.rotationY != previousRightRotationYValue \
                   or rightPeripheral.rotationZ != previousRightRotationZValue \
                   or rightPeripheral.orientationX != previousRightOrientationXValue \
                   or rightPeripheral.orientationY != previousRightOrientationYValue \
                   or rightPeripheral.orientationZ != previousRightOrientationZValue ):
                    duplicateRow = False
                    
                previousLeftToeValue = leftPeripheral.toe
                previousLeftBallValue = leftPeripheral.ball
                previousLeftArchValue = leftPeripheral.arch
                previousLeftHeelValue = leftPeripheral.heel
                previousLeftAccelerationXValue = leftPeripheral.accelerationX
                previousLeftAccelerationYValue = leftPeripheral.accelerationY
                previousLeftAccelerationZValue = leftPeripheral.accelerationZ
                previousLeftRotationXValue = leftPeripheral.rotationX
                previousLeftRotationYValue = leftPeripheral.rotationY
                previousLeftRotationZValue = leftPeripheral.rotationZ
                previousLeftOrientationXValue = leftPeripheral.orientationX
                previousLeftOrientationYValue = leftPeripheral.orientationY
                previousLeftOrientationZValue = leftPeripheral.orientationZ

                previousRightToeValue = rightPeripheral.toe
                previousRightBallValue = rightPeripheral.ball
                previousRightArchValue = rightPeripheral.arch
                previousRightHeelValue = rightPeripheral.heel
                previousRightAccelerationXValue = rightPeripheral.accelerationX
                previousRightAccelerationYValue = rightPeripheral.accelerationY
                previousRightAccelerationZValue = rightPeripheral.accelerationZ
                previousRightRotationXValue = rightPeripheral.rotationX
                previousRightRotationYValue = rightPeripheral.rotationY
                previousRightRotationZValue = rightPeripheral.rotationZ
                previousRightOrientationXValue = rightPeripheral.orientationX
                previousRightOrientationYValue = rightPeripheral.orientationY
                previousRightOrientationZValue = rightPeripheral.orientationZ
                            
                if subscribeToSensors and not duplicateRow:
                    logger.writeRow(leftPeripheral.toe, leftPeripheral.ball, leftPeripheral.arch, leftPeripheral.heel, \
                                    leftPeripheral.accelerationX, leftPeripheral.accelerationY, leftPeripheral.accelerationZ, \
                                    leftPeripheral.rotationX, leftPeripheral.rotationY, leftPeripheral.rotationZ, \
                                    leftPeripheral.orientationX, leftPeripheral.orientationY, leftPeripheral.orientationZ, \
                                    rightPeripheral.toe, rightPeripheral.ball, rightPeripheral.arch, rightPeripheral.heel, \
                                    rightPeripheral.accelerationX, rightPeripheral.accelerationY, rightPeripheral.accelerationZ, \
                                    rightPeripheral.rotationX, rightPeripheral.rotationY, rightPeripheral.rotationZ, \
                                    rightPeripheral.orientationX, rightPeripheral.orientationY, rightPeripheral.orientationZ)

                
                
        except BTLEException:
            connected = False
            leftPeripheral.disconnect()
            rightPeripheral.disconnect()
            logger.close()
        except KeyboardInterrupt:
            leftPeripheral.disconnect()
            rightPeripheral.disconnect()
            logger.close()
        finally:
            leftPeripheral.disconnect()
            rightPeripheral.disconnect()
            logger.close()
      
if __name__ == "__main__":
    main()
