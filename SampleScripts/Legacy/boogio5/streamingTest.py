#!/usr/bin/env python
from settings import *
from BoogioShoePeripheral import *
import pygame
from pygame.locals import *
from CharacteristicChart import *

import datetime
import time


def getTime():
        return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    

def main():

    # set up pygame
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 840
    READING_SCALE = 100
    WINDOW_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
    DISPLAYSURF = pygame.display.set_mode(WINDOW_RESOLUTION,  pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
    pygame.display.set_caption('Boogio 5 Streaming Test')



    
    chartWidth = SCREEN_WIDTH / 2 - 20
    chartHeight = 48

    leftChartsX = 10
    rightChartsX = SCREEN_WIDTH - leftChartsX - chartWidth
    vSpacing = 16
    
    chartY = vSpacing
    
    i = 0

    
    metricsFont = pygame.font.SysFont("comicsans", 24)

    

    leftFSR0Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Toe FSR")
    leftFSR0Chart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)

    i = i + chartHeight + vSpacing
    leftFSR1Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Ball FSR")
    leftFSR1Chart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
  
    i = i + chartHeight + vSpacing
    leftFSR2Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Arch FSR")
    leftFSR2Chart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    
    i = i + chartHeight + vSpacing
    leftFSR3Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Heel FSR")
    leftFSR3Chart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    
    i = i + chartHeight + vSpacing
    leftAccelerationXChart = CharacteristicChart(DISPLAYSURF, -MAX_ACCELERATION_VALUE, MAX_ACCELERATION_VALUE, " Acceleration X [+-8000 milliGravities]")
    leftAccelerationXChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftAccelerationXChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    leftAccelerationYChart = CharacteristicChart(DISPLAYSURF, -MAX_ACCELERATION_VALUE, MAX_ACCELERATION_VALUE, " Acceleration Y [+-8000 milliGravities]")
    leftAccelerationYChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftAccelerationYChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    leftAccelerationZChart = CharacteristicChart(DISPLAYSURF, -MAX_ACCELERATION_VALUE, MAX_ACCELERATION_VALUE, " Acceleration Z [+-8000 milliGravities]")
    leftAccelerationZChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftAccelerationZChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    leftRotationXChart = CharacteristicChart(DISPLAYSURF, -MAX_ROTATION_VALUE, MAX_ROTATION_VALUE, " Rotation X [+-1000 degrees per second]")
    leftRotationXChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftRotationXChart.setColors(MYBITAT_BLUE, BLUE)
    
    i = i + chartHeight + vSpacing
    leftRotationYChart = CharacteristicChart(DISPLAYSURF, -MAX_ROTATION_VALUE, MAX_ROTATION_VALUE, " Rotation Y [+-1000 degrees per second]")
    leftRotationYChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftRotationYChart.setColors(MYBITAT_BLUE, BLUE)
    
    i = i + chartHeight + vSpacing
    leftRotationZChart = CharacteristicChart(DISPLAYSURF, -MAX_ROTATION_VALUE, MAX_ROTATION_VALUE, " Rotation Z [+-1000 degrees per second]")
    leftRotationZChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftRotationZChart.setColors(MYBITAT_BLUE, BLUE)

    i = i + chartHeight + vSpacing
    leftOrientationXChart = CharacteristicChart(DISPLAYSURF, -MAX_ORIENTATION_VALUE, MAX_ORIENTATION_VALUE, " Direction X [+-4800 microTeslas]")
    leftOrientationXChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftOrientationXChart.setColors(MYBITAT_BLUE, RED)
    
    i = i + chartHeight + vSpacing
    leftOrientationYChart = CharacteristicChart(DISPLAYSURF, -MAX_ORIENTATION_VALUE, MAX_ORIENTATION_VALUE, " Direction Y [+-4800 microTeslas]")
    leftOrientationYChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftOrientationYChart.setColors(MYBITAT_BLUE, RED)
    
    i = i + chartHeight + vSpacing
    leftOrientationZChart = CharacteristicChart(DISPLAYSURF, -MAX_ORIENTATION_VALUE, MAX_ORIENTATION_VALUE, " Direction Z [+-4800 microTeslas]")
    leftOrientationZChart.translate(leftChartsX, chartY + i, chartWidth, chartHeight)
    leftOrientationZChart.setColors(MYBITAT_BLUE, RED)

    i = 0
    rightFSR0Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Toe FSR")
    rightFSR0Chart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)

    i = i + chartHeight + vSpacing
    rightFSR1Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Ball FSR")
    rightFSR1Chart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
  
    i = i + chartHeight + vSpacing
    rightFSR2Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Arch FSR")
    rightFSR2Chart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    
    i = i + chartHeight + vSpacing
    rightFSR3Chart = CharacteristicChart(DISPLAYSURF, 0, MAX_FORCE_VALUE, "Heel FSR")
    rightFSR3Chart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    
    i = i + chartHeight + vSpacing
    rightAccelerationXChart = CharacteristicChart(DISPLAYSURF, -MAX_ACCELERATION_VALUE, MAX_ACCELERATION_VALUE, " Acceleration X [+-8000 milliGravities]")
    rightAccelerationXChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightAccelerationXChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    rightAccelerationYChart = CharacteristicChart(DISPLAYSURF, -MAX_ACCELERATION_VALUE, MAX_ACCELERATION_VALUE, " Acceleration Y [+-8000 milliGravities]")
    rightAccelerationYChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightAccelerationYChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    rightAccelerationZChart = CharacteristicChart(DISPLAYSURF, -MAX_ACCELERATION_VALUE, MAX_ACCELERATION_VALUE, " Acceleration Z [+-8000 milliGravities]")
    rightAccelerationZChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightAccelerationZChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    rightRotationXChart = CharacteristicChart(DISPLAYSURF, -MAX_ROTATION_VALUE, MAX_ROTATION_VALUE, " Rotation X [+-1000 degrees per second]")
    rightRotationXChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightRotationXChart.setColors(MYBITAT_BLUE, BLUE)
    
    i = i + chartHeight + vSpacing
    rightRotationYChart = CharacteristicChart(DISPLAYSURF, -MAX_ROTATION_VALUE, MAX_ROTATION_VALUE, " Rotation Y [+-1000 degrees per second]")
    rightRotationYChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightRotationYChart.setColors(MYBITAT_BLUE, BLUE)
    
    i = i + chartHeight + vSpacing
    rightRotationZChart = CharacteristicChart(DISPLAYSURF, -MAX_ROTATION_VALUE, MAX_ROTATION_VALUE, " Rotation Z [+-1000 degrees per second]")
    rightRotationZChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightRotationZChart.setColors(MYBITAT_BLUE, BLUE)

    i = i + chartHeight + vSpacing
    rightOrientationXChart = CharacteristicChart(DISPLAYSURF, -MAX_ORIENTATION_VALUE, MAX_ORIENTATION_VALUE, " Direction X [+-4800 microTeslas]")
    rightOrientationXChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightOrientationXChart.setColors(MYBITAT_BLUE, RED)
    
    i = i + chartHeight + vSpacing
    rightOrientationYChart = CharacteristicChart(DISPLAYSURF, -MAX_ORIENTATION_VALUE, MAX_ORIENTATION_VALUE, " Direction Y [+-4800 microTeslas]")
    rightOrientationYChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightOrientationYChart.setColors(MYBITAT_BLUE, RED)
    
    i = i + chartHeight + vSpacing
    rightOrientationZChart = CharacteristicChart(DISPLAYSURF, -MAX_ORIENTATION_VALUE, MAX_ORIENTATION_VALUE, " Direction Z [+-4800 microTeslas]")
    rightOrientationZChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    rightOrientationZChart.setColors(MYBITAT_BLUE, RED)
    
    subscribeToSensors = True    
    shouldQuit = False
    connected = False
    
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

            while not shouldQuit:
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        shouldQuit = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            shouldQuit = True


                DISPLAYSURF.fill(BLACK)
                
                column1 = 400
                column2 = 550 + column1
                vspacing = 30

                
                    
                leftPeripheral.connection.waitForNotifications(0.1)
                rightPeripheral.connection.waitForNotifications(0.1)
                
                if subscribeToSensors:
                    leftFSR0Chart.appendValue(leftPeripheral.toe)
                    leftFSR1Chart.appendValue(leftPeripheral.ball)
                    leftFSR2Chart.appendValue(leftPeripheral.arch)
                    leftFSR3Chart.appendValue(leftPeripheral.heel)
                    
                    leftAccelerationXChart.appendValue(leftPeripheral.accelerationX)
                    leftAccelerationYChart.appendValue(leftPeripheral.accelerationY)
                    leftAccelerationZChart.appendValue(leftPeripheral.accelerationZ)
                    
                    leftRotationXChart.appendValue(leftPeripheral.rotationX)
                    leftRotationYChart.appendValue(leftPeripheral.rotationY)
                    leftRotationZChart.appendValue(leftPeripheral.rotationZ)
                    
                    leftOrientationXChart.appendValue(leftPeripheral.orientationX)
                    leftOrientationYChart.appendValue(leftPeripheral.orientationY)
                    leftOrientationZChart.appendValue(leftPeripheral.orientationZ)

                    rightFSR0Chart.appendValue(rightPeripheral.toe)
                    rightFSR1Chart.appendValue(rightPeripheral.ball)
                    rightFSR2Chart.appendValue(rightPeripheral.arch)
                    rightFSR3Chart.appendValue(rightPeripheral.heel)
                    
                    rightAccelerationXChart.appendValue(rightPeripheral.accelerationX)
                    rightAccelerationYChart.appendValue(rightPeripheral.accelerationY)
                    rightAccelerationZChart.appendValue(rightPeripheral.accelerationZ)
                    
                    rightRotationXChart.appendValue(rightPeripheral.rotationX)
                    rightRotationYChart.appendValue(rightPeripheral.rotationY)
                    rightRotationZChart.appendValue(rightPeripheral.rotationZ)
                    
                    rightOrientationXChart.appendValue(rightPeripheral.orientationX)
                    rightOrientationYChart.appendValue(rightPeripheral.orientationY)
                    rightOrientationZChart.appendValue(rightPeripheral.orientationZ)


                    leftFSR0Chart.blit()
                    leftFSR1Chart.blit()
                    leftFSR2Chart.blit()
                    leftFSR3Chart.blit()
                    leftAccelerationXChart.blit()
                    leftAccelerationYChart.blit()
                    leftAccelerationZChart.blit()
                    leftRotationXChart.blit()
                    leftRotationYChart.blit()
                    leftRotationZChart.blit()
                    leftOrientationXChart.blit()
                    leftOrientationYChart.blit()
                    leftOrientationZChart.blit()

                    
                    rightFSR0Chart.blit()
                    rightFSR1Chart.blit()
                    rightFSR2Chart.blit()
                    rightFSR3Chart.blit()
                    rightAccelerationXChart.blit()
                    rightAccelerationYChart.blit()
                    rightAccelerationZChart.blit()
                    rightRotationXChart.blit()
                    rightRotationYChart.blit()
                    rightRotationZChart.blit()
                    rightOrientationXChart.blit()
                    rightOrientationYChart.blit()
                    rightOrientationZChart.blit()

                pygame.display.update()
                
        except BTLEException:
            connected = False
            leftPeripheral.disconnect()
            rightPeripheral.disconnect()
        
    leftPeripheral.disconnect()
    rightPeripheral.disconnect()
    pygame.quit()
            
if __name__ == "__main__":
    main()
