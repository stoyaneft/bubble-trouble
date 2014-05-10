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
pygame.time.set_timer(USEREVENT+1, 1000)


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


def draw_timer():
    timer = font.render(str(game.time_left), 1, RED)
    rect = timer.get_rect()
    rect.bottomleft = 10, WINDOWHEIGHT - 10
    screen.blit(timer, rect)

def draw_world():
    screen.fill((250, 250, 250))
    if game.game_over:
        draw_message("Game over!", RED)
    if game.level_completed:
        draw_message("Well done! Level completed!", BLUE)
    for ball in game.balls:
        draw_ball(ball)
    draw_player(game.player)
    if game.player.weapon.is_active:
        draw_weapon(game.player.weapon)
    draw_timer()



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
                pygame.quit()
                sys.exit()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.player.moving_left = False
            elif event.key == K_RIGHT:
                game.player.moving_right = False
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

while game.is_running:
    draw_world()
    handle_event()
    pygame.display.update()
    game.update()
    clock.tick(FPS)

