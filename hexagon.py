import pygame

from settings import *


class Hexagon(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/hexagon' + str(size) + '.png')
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.size = size
        self.speed = speed

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WINDOWWIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > WINDOWHEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.left = self.clip(self.rect.left, 0, WINDOWWIDTH)
        self.rect.right = self.clip(self.rect.right, 0, WINDOWWIDTH)
        self.rect.top = self.clip(self.rect.top, 0, WINDOWHEIGHT)
        self.rect.bottom = self.clip(self.rect.bottom, 0, WINDOWHEIGHT)

    def clip(self, val, minval, maxval):
        return min(max(val, minval), maxval)