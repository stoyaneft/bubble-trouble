import pygame, sys
from settings import *
from pygame.locals import *
from ball import *
from player import *
from gui import *
from gameworld import*

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Bubble Trouble')
        pygame.mouse.set_visible(0)
        self.is_running = False

    def start(self):
        clock = pygame.time.Clock()
        is_running = True
        gui = GUI(self.screen)
        world = Gameworld()
        while is_running:
            self.screen.fill(WHITE)
            world.update()
            for ball in world.balls:
                gui.draw_ball(ball)
            gui.draw_player(world.player)
            if world.player.weapon.is_active:
                gui.draw_weapon(world.player.weapon)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        world.player.moving_left = True
                    elif event.key == K_RIGHT:
                        world.player.moving_right = True
                    elif event.key == K_SPACE and not world.player.weapon.is_active:
                        world.player.shoot()
                    elif event.key == K_ESCAPE:
                        self.exit()
                if event.type == KEYUP:
                    if event.key == K_LEFT:
                        world.player.moving_left = False
                    elif event.type == KEYUP:
                        world.player.moving_right = False

                if event.type == QUIT:
                    self.exit()
            pygame.display.update()
            clock.tick(FPS)

    def exit(self):
        pygame.quit()
        sys.exit()


