#!/usr/bin/env python
import settings
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
    SCREEN_HEIGHT = 850
    READING_SCALE = 100
    WINDOW_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
    DISPLAYSURF = pygame.display.set_mode(WINDOW_RESOLUTION,  pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
    pygame.display.set_caption('Boogio 5 Streaming Test')



    chartY = SCREEN_HEIGHT / 8
    chartWidth = SCREEN_WIDTH / 2 - 20
    chartHeight = 48

    ChartsX = 10
    rightChartsX = SCREEN_WIDTH - ChartsX - chartWidth
    vSpacing = 16

    i = 0

    titleFont = pygame.font.SysFont("comicsans", 32)
    metricsFont = pygame.font.SysFont("comicsans", 24)

    FSR0Chart = CharacteristicChart(DISPLAYSURF, 0, pow(2,16), "Toe FSR")
    FSR0Chart.translate(ChartsX, chartY + i, chartWidth, chartHeight)

    i = i + chartHeight + vSpacing
    FSR1Chart = CharacteristicChart(DISPLAYSURF, 0, pow(2,16), "Ball FSR")
    FSR1Chart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
  

    i = i + chartHeight + vSpacing
    FSR2Chart = CharacteristicChart(DISPLAYSURF, 0, pow(2,16), "Arch FSR")
    FSR2Chart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    
    i = i + chartHeight + vSpacing
    FSR3Chart = CharacteristicChart(DISPLAYSURF, 0, pow(2,16), "Heel FSR")
    FSR3Chart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    
    i = i + chartHeight + vSpacing * 3
    AccelerationXChart = CharacteristicChart(DISPLAYSURF, -16, 16, " Acceleration X [-16Gs, +16Gs]")
    AccelerationXChart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    AccelerationXChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    AccelerationYChart = CharacteristicChart(DISPLAYSURF, -16, 16, " Acceleration Y [-16Gs, +16Gs]")
    AccelerationYChart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    AccelerationYChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing
    AccelerationZChart = CharacteristicChart(DISPLAYSURF, -16, 16, " Acceleration Z [-16Gs, +16Gs]")
    AccelerationZChart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    AccelerationZChart.setColors(MYBITAT_BLUE, ORANGE)
    
    i = i + chartHeight + vSpacing * 3
    RotationXChart = CharacteristicChart(DISPLAYSURF, -2000, 2000, " Rotation X [-2000dps, +2000dps]")
    RotationXChart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    RotationXChart.setColors(MYBITAT_BLUE, BLUE)
    
    i = i + chartHeight + vSpacing
    RotationYChart = CharacteristicChart(DISPLAYSURF, -2000, 2000, " Rotation Y [-2000dps, +2000dps]")
    RotationYChart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    RotationYChart.setColors(MYBITAT_BLUE, BLUE)
    
    i = i + chartHeight + vSpacing
    RotationZChart = CharacteristicChart(DISPLAYSURF, -2000, 2000, " Rotation Z [-2000dps, +2000dps]")
    RotationZChart.translate(ChartsX, chartY + i, chartWidth, chartHeight)
    RotationZChart.setColors(MYBITAT_BLUE, BLUE)

    i = chartY + chartHeight + vSpacing * 3
    i = 0
    OrientationXChart = CharacteristicChart(DISPLAYSURF, -8, 8, " Orientation X [-8 Gauss, +8 Gauss]")
    OrientationXChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    OrientationXChart.setColors(MYBITAT_BLUE, RED)
    
    i = i + chartHeight + vSpacing
    OrientationYChart = CharacteristicChart(DISPLAYSURF, -8, 8, " Orientation Y [-8 Gauss, +8 Gauss]")
    OrientationYChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    OrientationYChart.setColors(MYBITAT_BLUE, RED)
    
    i = i + chartHeight + vSpacing
    OrientationZChart = CharacteristicChart(DISPLAYSURF, -8, 8, " Orientation Z [-8 Gauss, +8 Gauss]")
    OrientationZChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    OrientationZChart.setColors(MYBITAT_BLUE, RED)

    i = i + chartHeight + vSpacing
    i = i + chartHeight + vSpacing * 3
    TemperatureCChart = CharacteristicChart(DISPLAYSURF, -80, 80, "Temperature C [-80 c, +80 c]")
    TemperatureCChart.translate(rightChartsX, chartY + i, chartWidth, chartHeight)
    TemperatureCChart.setColors(MYBITAT_BLUE, GRAY)
    
    subscribeToSensors = True
    

    startTime = time.time()
    startDateTime = getTime()

    PERIPHERAL_UUID = "C1:5D:2E:65:16:2D"
    shouldQuit = False
    connected = False
    batteryReadInterval = 0
    while not shouldQuit:
        
        try:
            peripheral = BoogioShoePeripheral(PERIPHERAL_UUID)
            peripheral.subscribeToNotifications(peripheral.FORCE)
            peripheral.subscribeToNotifications(peripheral.ACCELERATION)
            peripheral.subscribeToNotifications(peripheral.ROTATION)
            peripheral.subscribeToNotifications(peripheral.ORIENTATION)
            peripheral.subscribeToNotifications(peripheral.TEMPERATURE)
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

                
                batteryReadInterval = batteryReadInterval + 1 
                if batteryReadInterval % 1000 == 0:
                    peripheral.readBattery()
                
                    
                    
                peripheral.connection.waitForNotifications(0.01)

                if subscribeToSensors:
                    FSR0Chart.appendValue(peripheral.toe)
                    FSR1Chart.appendValue(peripheral.ball)
                    FSR2Chart.appendValue(peripheral.arch)
                    FSR3Chart.appendValue(peripheral.heel)
                    
                    AccelerationXChart.appendValue(peripheral.accelerationX)
                    AccelerationYChart.appendValue(peripheral.accelerationY)
                    AccelerationZChart.appendValue(peripheral.accelerationZ)
                    
                    RotationXChart.appendValue(peripheral.rotationX)
                    RotationYChart.appendValue(peripheral.rotationY)
                    RotationZChart.appendValue(peripheral.rotationZ)
                    
                    OrientationXChart.appendValue(peripheral.orientationX)
                    OrientationYChart.appendValue(peripheral.orientationY)
                    OrientationZChart.appendValue(peripheral.orientationZ)
                    TemperatureCChart.appendValue(peripheral.temperatureC)

                    FSR0Chart.blit()
                    FSR1Chart.blit()
                    FSR2Chart.blit()
                    FSR3Chart.blit()
                    AccelerationXChart.blit()
                    AccelerationYChart.blit()
                    AccelerationZChart.blit()
                    RotationXChart.blit()
                    RotationYChart.blit()
                    RotationZChart.blit()
                    OrientationXChart.blit()
                    OrientationYChart.blit()
                    OrientationZChart.blit()
                    TemperatureCChart.blit()

                if connected:
                    upTime = time.time() - startTime
                now = getTime()
                
                stepsLabel = titleFont.render("Boogio Streaming Test", 1, GREEN)

                startTimeTitleLabel = metricsFont.render("Start Time:         ", 1, GREEN)
                startTimeLabel = metricsFont.render(str(startDateTime), 1, GREEN)

                nowTitleLabel = metricsFont.render("End Time:          ", 1, GREEN)
                nowLabel = metricsFont.render(str(now), 1, GREEN)
                
                upTimeTitleLabel = metricsFont.render("Up-Time:            ", 1, GREEN)
                upTimeLabel = metricsFont.render(str('{0:.2f}'.format(upTime)) + str("  (seconds)"), 1, GREEN)

                batteryTitleLabel = metricsFont.render("Battery:            ", 1, GREEN)
                batteryLabel = metricsFont.render(str(peripheral.battery) + str(" %"), 1, GREEN)
                
                DISPLAYSURF.blit(stepsLabel, (SCREEN_WIDTH/2 - stepsLabel.get_width()/2, vSpacing))

                DISPLAYSURF.blit(startTimeTitleLabel, (rightChartsX, chartY + 400))
                DISPLAYSURF.blit(startTimeLabel, (rightChartsX + startTimeTitleLabel.get_width(), chartY + 400))

                DISPLAYSURF.blit(nowTitleLabel, (rightChartsX, chartY + 430))
                DISPLAYSURF.blit(nowLabel, (rightChartsX + nowTitleLabel.get_width(), chartY + 430))
                
                DISPLAYSURF.blit(upTimeTitleLabel, (rightChartsX, chartY + 460 ))
                DISPLAYSURF.blit(upTimeLabel, (rightChartsX + upTimeTitleLabel.get_width(), chartY + 460))

                DISPLAYSURF.blit(batteryTitleLabel, (rightChartsX, chartY + 490 ))
                DISPLAYSURF.blit(batteryLabel, (rightChartsX + upTimeTitleLabel.get_width(), chartY + 490))
                

                pygame.display.update()
                
        except BTLEException:
            connected = False
            peripheral.disconnect()
        
    peripheral.disconnect()
    pygame.quit()
            
if __name__ == "__main__":
    main()
