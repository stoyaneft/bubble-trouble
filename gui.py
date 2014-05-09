import pygame
import sys

from pygame.locals import *
from game import*


pygame.init()
pygame.display.set_caption('Bubble Trouble')
pygame.mouse.set_visible(0)

screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 30)
game = Game()


def draw_ball(ball):
    screen.blit(ball.image, ball.rect)


def draw_player(player):
    screen.blit(player.image, player.rect)


def draw_weapon(weapon):
    screen.blit(weapon.image, weapon.rect)


def draw_message(message, colour):
    label = font.render(message, 1, colour)
    rect = label.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(label, rect)


def draw_world():
    screen.fill((250, 250, 250))
    game.update()
    for ball in game.balls:
        draw_ball(ball)
    draw_player(game.player)
    if game.player.weapon.is_active:
        draw_weapon(game.player.weapon)
    if game.game_over:
        game.is_running = False
        draw_message("Game over!", RED)
        game.pause()
    if game.level_completed:
        draw_message("Well done! Level completed!", BLUE)
        game.pause()
        game.load_level(game.level + 1)


def handle_event():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.player.moving_left = True
            elif event.key == K_RIGHT:
                game.player.moving_right = True
            elif event.key == K_SPACE and not game.player.weapon.is_active:
                game.player.shoot()
            elif event.key == K_ESCAPE:
                sys.exit()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.player.moving_left = False
            elif event.key == K_RIGHT:
                game.player.moving_right = False
        if event.type == QUIT:
            sys.exit()


while game.is_running:
    draw_world()
    handle_event()
    pygame.display.update()
    if game.is_paused:
        pygame.time.wait(3000)
        game.is_paused = False
    clock.tick(FPS)

