import pygame, sys
from settings import *
from pygame.locals import *
from ball import *
from player import *
from gui import *
#from gameworld import*

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Bubble Trouble')
        pygame.mouse.set_visible(0)
        self.is_running = False
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.player = Player()
        self.ball = Ball(WINDOWWIDTH / 4, WINDOWHEIGHT / 2, 6, UPRIGHT)

    def start(self):
        clock = pygame.time.Clock()
        is_running = True
        gui = GUI(self.screen)
        world =
        while is_running:
            self.screen.fill(WHITE)
            self.ball.update()
            if self.left_key_pressed and self.player.x > 0:
                self.player.x -= PLAYERSPEED
            if self.right_key_pressed and self.player.x < WINDOWWIDTH - self.player.image.get_width():
                self.player.x += PLAYERSPEED
            if self.player.weapon.is_active:
                self.player.weapon.update()
                gui.draw_weapon(self.player.weapon)
                #if self.player.weapon.image.get_rect().colliderect(self.ball.image.get_rect()):


            gui.draw_ball(self.ball)
            gui.draw_player(self.player)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.left_key_pressed = True
                    elif event.key == K_RIGHT:
                        self.right_key_pressed = True
                    elif event.key == K_SPACE and not self.player.weapon.is_active:
                        self.player.shoot()
                    elif event.key == K_ESCAPE:
                        self.exit()
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        self.left_key_pressed = False
                    elif event.type == KEYUP:
                        self.right_key_pressed = False

                if event.type == QUIT:
                    self.exit()
            pygame.display.update()
            clock.tick(FPS)

    def exit(self):
        pygame.quit()
        sys.exit()


