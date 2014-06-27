import pygame

class Bonus:
    def __init__(self, type, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
