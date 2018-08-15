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
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 320
    READING_SCALE = 1
    WINDOW_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
    DISPLAYSURF = pygame.display.set_mode(WINDOW_RESOLUTION,  pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
    pygame.display.set_caption('Boogio 5 Synchronization Test')

    titleFont = pygame.font.SysFont("comicsans", 32)
    metricsFont = pygame.font.SysFont("comicsans", 24)

    
    
    subscribeToPrimarySensors = True
    subscribeToSecondarySensors = True

    startTime = time.time()
    startDateTime = getTime()

    PERIPHERAL_UUID = "C1:5D:2E:65:16:2D"
    shouldQuit = False
    connected = False

    
    
    
    while not shouldQuit:
        
        try:
            peripheral = BoogioShoePeripheral(PERIPHERAL_UUID)
            
            peripheral.subscribeToNotifications(peripheral.GENERIC_COMMUNICATION)
            connected = True
            peripheral.updateTime()
            
            
            while not shouldQuit:
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        shouldQuit = True
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            shouldQuit = True


                DISPLAYSURF.fill(BLACK)
                
                x = 10
                y = 10
                yi = 30

                stepsLabel = titleFont.render("Boogio Set Time Test", 1, GREEN)                
                DISPLAYSURF.blit(stepsLabel, (SCREEN_WIDTH/2 - stepsLabel.get_width()/2, y))

                y = y + yi

                y = y + yi
                syncStatusTitleLabel = metricsFont.render("Time =   ", 1, GREEN)
                syncStatusLabelString = str(datetime.datetime.now())
                syncStatusLabel = metricsFont.render(syncStatusLabelString, 1, GREEN)
                DISPLAYSURF.blit(syncStatusTitleLabel, (x, y))
                DISPLAYSURF.blit(syncStatusLabel, (x + syncStatusTitleLabel.get_width(), y))

                
        
                
                

                pygame.display.update()

                peripheral.disconnect()
                
        except BTLEException:
            connected = False
            shouldQuit = True
            print("Bad state. Please power cycle the peripheral try again.")
            pygame.quit()
        
    peripheral.disconnect()
    pygame.quit()
            
if __name__ == "__main__":
    main()
