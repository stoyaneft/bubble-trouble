import pygame, math
from settings import *
from polar_vector import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed=[3, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ball' + str(size) + '.bmp')
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.size = size
        self.speed = speed
        self.falling_dist = (WINDOWHEIGHT - self.rect.bottom)

    def update(self):
        self.speed[1] += GRAVITY
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

    def bounce(self):
        if self.x > WINDOWWIDTH - self.size:
            self.x = 2*(WINDOWWIDTH - self.size) - self.x
            self.force.angle = - self.force.angle

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.force.angle = - self.force.angle

        if self.y > WINDOWHEIGHT - self.size:
            self.y = 2*(WINDOWHEIGHT - self.size) - self.y
            self.force.angle = math.pi - self.force.angle

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.force.angle = math.pi - self.force.angle

