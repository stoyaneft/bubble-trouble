import pygame

class GUI:
    def __init__(self, screen):
        self.screen = screen

    def draw_ball(self, ball):
        self.screen.blit(ball.image, ball.rect)

    def draw_player(self, player):
        self.screen.blit(player.image, player.rect)

    def draw_weapon(self, weapon):
        self.screen.blit(weapon.image, weapon.rect)