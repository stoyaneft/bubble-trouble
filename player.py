from weapon import *


class Player(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.image.load('images/player.png')
        self.rect = self.image.get_rect()
        self.weapon = Weapon()
        self.moving_left = False
        self.moving_right = False
        self.lives = 3
        self.reset_position()
        self.is_alive = True

    def shoot(self):
        self.weapon = Weapon(self.rect.centerx, self.rect.top)
        self.weapon.is_active = True

    def update(self):
        if self.moving_left and self.rect.left >= 0:
            self.rect = self.rect.move(-PLAYERSPEED, 0)
        if self.moving_right and self.rect.right <= WINDOWWIDTH:
            self.rect = self.rect.move(PLAYERSPEED, 0)
        if self.weapon.is_active:
            self.weapon.update()

    def reset_position(self):
        self.rect.bottom, self.rect.centerx = WINDOWHEIGHT, WINDOWWIDTH / 2
