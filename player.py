import pygame
from settings import *
from weapon import *
class Player:
    def __init__(self):
        self.x = WINDOWWIDTH / 2
        self.y = WINDOWHEIGHT - 40
        self.weapon = Weapon()
        self.image = pygame.image.load('images/player.bmp')

    def shoot(self):
        self.weapon = Weapon(self.x + self.image.get_width()/2, self.y)
        self.weapon.is_active = True


