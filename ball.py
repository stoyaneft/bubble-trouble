import pygame
from settings import *

UPLEFT = 'upleft'
UPRIGHT = 'upright'
DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'

class Ball:
    def __init__(self, x, y, size, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.image = pygame.image.load("images/ball" + str(size) + '.bmp')
        self.max_height = WINDOWHEIGHT / size
        #self.rect = self.image.get_rect()


    def update(self):
        if self.direction == DOWNRIGHT:
            self.x += 1
            self.y += 5
            if self.x >= WINDOWWIDTH - self.image.get_width():
                self.direction = DOWNLEFT
            if self.y >= WINDOWHEIGHT - self.image.get_height():
                self.direction = UPRIGHT

        if self.direction == DOWNLEFT:
            self.x -= 1
            self.y += 5
            if self.x <= 0:
                self.direction = DOWNRIGHT
            if self.y >= WINDOWHEIGHT - self.image.get_height():
                self.direction = UPLEFT

        if self.direction == UPRIGHT:
            self.x += 1
            self.y -= 5
            if self.x >= WINDOWWIDTH - self.image.get_width():
                self.direction = UPLEFT
            if self.y <= self.max_height:
                self.direction = DOWNRIGHT

        if self.direction == UPLEFT:
            self.x -= 1
            self.y -= 5
            if self.x <= 0:
                self.direction = UPRIGHT
            if self.y <= self.max_height:
                self.direction = DOWNLEFT

