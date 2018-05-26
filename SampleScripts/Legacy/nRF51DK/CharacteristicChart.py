import pygame
from pygame.locals import *


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255,   60,   120)
GREEN = (58, 255, 118)
BLUE = (  64, 128, 210)
MYBITAT_BLUE = (43, 89, 115)
ORANGE = (242, 97, 38)


class CharacteristicChart:
        def __init__(self, pygameSurface, lowerLimit, upperLimit, title=""):
            self.display = pygameSurface
            self.lowerLimit = lowerLimit
            self.upperLimit = upperLimit
            self.bgColor = (43, 89, 115)
            self.fgColor = (242, 97, 38)
            self.translate(10, 20, 512, 256)
            self.setColors(MYBITAT_BLUE, GREEN)
            self.valuesQueue = []
            self.displayFont = pygame.font.SysFont("comicsans", 16)
            self.label = self.displayFont.render("", 1, self.fgColor)
            self.title = title
            self.queueLimit = 20
            
        def setQueueLimit(self, limit):
            self.queueLimit = max(1,limit)
            self.trimQueue()
            
        def translate(self, x, y, w, h):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
        
        def setColors(self, bgColor, fgColor):
            self.bgColor = bgColor
            self.fgColor = fgColor
            
        def appendValue(self, value):
            self.valuesQueue.append(value)
            self.trimQueue()
            
        def trimQueue(self):
            if len(self.valuesQueue) > self.queueLimit:
                self.valuesQueue.pop(len(self.valuesQueue) - self.queueLimit - 1)
        def blit(self):

            if len(self.valuesQueue) < 2:
                return

            BORDER_THICKNESS = 1
            
            QUEUE_LIMIT = self.queueLimit
            DELTA_LENGTH = float(self.w) / QUEUE_LIMIT
            HEIGHT_SCALE = float(self.h) / float(abs((self.upperLimit - self.lowerLimit)))

            heightOffset = 0 #this offsets the plot so signed plots don't require a subclass
            if self.lowerLimit < 0:
                    heightOffset = self.h / 2
            
            
            #construct the points list
            i = 0
            points = list()
            points.append(((self.x + self.w - 2), (self.y + self.h - heightOffset)))
            points.append(((self.x + 1), (self.y + self.h - heightOffset)))  
            points.append(((self.x + 1), (-self.valuesQueue[0] * HEIGHT_SCALE + self.y + self.h - heightOffset)))
            i = 1

            while i < len(self.valuesQueue):
                    x = self.x + (i+1) * DELTA_LENGTH
                    y = -self.valuesQueue[i] * HEIGHT_SCALE + self.y + self.h - heightOffset

                    #shift the poly so that it fits within the bounds of the rectangle
                    if i == len(self.valuesQueue) - 1:
                            x = x - 2
                    points.append((x, y))
                    i = i + 1
            
                            
            
            #draw the plot fill and then its outline            
            pygame.draw.polygon(self.display, self.fgColor, points, 0)
            #pygame.draw.polygon(self.display, self.fgColor, points, BORDER_THICKNESS)
            
            pygame.draw.rect(self.display, self.fgColor, (self.x, self.y, self.w, self.h), BORDER_THICKNESS)
            
            self.label = self.displayFont.render(self.title, 1, self.fgColor)
            self.display.blit(self.label, (self.x, self.y - self.label.get_height()))
            
            lastValue = str(self.valuesQueue[len(self.valuesQueue) - 1])
            self.label = self.displayFont.render(str(lastValue), 1, self.fgColor)
            self.display.blit(self.label, (self.x + self.w - self.label.get_width(), self.y - self.label.get_height()))
            
            
