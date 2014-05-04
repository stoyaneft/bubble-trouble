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
        self.is_paused = False

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
            if world.game_over:
                is_running = False
                myfont = pygame.font.SysFont("Comic Sans MS", 50)
                end_game_label = myfont.render("Game over!", 1, RED)
                end_game_rect = end_game_label.get_rect()
                end_game_rect.centerx, end_game_rect.centery = WINDOWWIDTH/2, WINDOWHEIGHT/2
                self.screen.blit(end_game_label)
                self.pause()
            if world.level_completed:
                myfont = pygame.font.SysFont("Comic Sans MS", 50)
                level_completed_label = myfont.render("Level completed!", 1, BLUE)
                level_comp_rect = level_completed_label.get_rect()
                level_comp_rect.centerx, level_comp_rect.centery = WINDOWWIDTH/2, WINDOWHEIGHT/2
                self.screen.blit(level_completed_label, level_comp_rect)
                self.pause()
                world.load_level(world.level + 1)
            self.handle_event(world)
            pygame.display.update()
            if self.is_paused:
                pygame.time.wait(3000)
                self.is_paused = False
            clock.tick(FPS)

    def exit(self):
        pygame.quit()
        sys.exit()

    def pause(self):
        self.is_paused = True

    def handle_event(self, world):
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



