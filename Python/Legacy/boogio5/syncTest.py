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

    
    syncTime = 0

    
    while not shouldQuit:
        
        try:
            peripheral = BoogioShoePeripheral(PERIPHERAL_UUID)
            peripheral.synchronizing = True
            peripheral.subscribeToNotifications(peripheral.GENERIC_COMMUNICATION)
            connected = True
            
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

                
               
                
                if peripheral.synchronizing:
                        peripheral.performSyncTick()
                        syncTime = time.time() - startTime
                        now = getTime()
                else:
                        connected = False
                        peripheral.disconnect()
                
                stepsLabel = titleFont.render("Boogio Synchronization Test", 1, GREEN)                
                DISPLAYSURF.blit(stepsLabel, (SCREEN_WIDTH/2 - stepsLabel.get_width()/2, y))

                y = y + yi

                y = y + yi
                syncStatusTitleLabel = metricsFont.render("Status:                ", 1, GREEN)
                syncStatusLabelString = "Synchronizing ( " + str(peripheral.readingsSynchronized) + " ) Readings..."
                syncStatusLabel = metricsFont.render(syncStatusLabelString, 1, ORANGE)
                if not peripheral.synchronizing:
                        syncStatusLabelString = "Done. ( " + str(peripheral.readingsSynchronized) + " Readings )"
                        syncStatusLabel = metricsFont.render(syncStatusLabelString, 1, GREEN)
                
                        
                DISPLAYSURF.blit(syncStatusTitleLabel, (x, y))
                DISPLAYSURF.blit(syncStatusLabel, (x + syncStatusTitleLabel.get_width(), y))
                
        
                y = y + yi
                startTimeTitleLabel = metricsFont.render("Connect Time:         ", 1, GREEN)
                startTimeLabel = metricsFont.render(str(startDateTime), 1, GREEN)
                DISPLAYSURF.blit(startTimeTitleLabel, (x, y))
                DISPLAYSURF.blit(startTimeLabel, (x + startTimeTitleLabel.get_width(), y))
                
                
                y = y + yi
                nowTitleLabel = metricsFont.render("Disconnect Time:          ", 1, GREEN)
                nowLabel = metricsFont.render(str(now), 1, GREEN)
                DISPLAYSURF.blit(nowTitleLabel, (x, y))
                DISPLAYSURF.blit(nowLabel, (x + nowTitleLabel.get_width(), y))

                y = y + yi
                syncTimeTitleLabel = metricsFont.render("Sync-Time:        ", 1, GREEN)
                syncTimeLabel = metricsFont.render(str('{0:.2f}'.format(syncTime)) + str("  (seconds)"), 1, GREEN)
                DISPLAYSURF.blit(syncTimeTitleLabel, (x, y))
                DISPLAYSURF.blit(syncTimeLabel, (x + syncTimeTitleLabel.get_width(), y)) 
                

                pygame.display.update()
                
        except BTLEException:
            connected = False
            peripheral.disconnect()
        
    peripheral.disconnect()
    pygame.quit()
            
if __name__ == "__main__":
    main()
