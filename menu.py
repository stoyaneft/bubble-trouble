import pygame
from settings import *


class MenuOption (pygame.font.Font):
    def __init__(self, text, position=(0, 0), function=None, font=None, font_size=36, font_color=WHITE):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, font_color)
        self.rect = self.label.get_rect(left=position[0], top=position[1])
        self.position = position
        self.function = function
        self.is_selected = False

    def set_position(self, x, y):
        self.position = (x, y)
        self.rect = self.label.get_rect(left=x, top=y)

    def highlight(self, color=RED):
        self.font_color = color
        self.set_italic(True)
        self.label = self.render(self.text, 1, self.font_color)

    def unhighlight(self):
        self.font_color = WHITE
        self.set_italic(False)
        self.label = self.render(self.text, 1, self.font_color)

    def check_for_mouse_selection(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.highlight()
            self.is_selected = True
        else:
            self.unhighlight()
            self.is_selected = False


class Menu():
    def __init__(self, screen, options, functions, bg_color=BLACK):
        self.is_active = True
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.options = []
        self.current_option = None
        self.functions = functions
        for index, option in enumerate(options):
            menu_option = MenuOption(option)
            width = menu_option.rect.width
            height = menu_option.rect.height
            total_height = len(options) * height
            pos_x = self.scr_width/2 - width/2
            pos_y = self.scr_height/2 - total_height/2 + index*height
            menu_option.set_position(pos_x, pos_y)
            self.options.append(menu_option)

    def draw(self):
        self.screen.fill(self.bg_color)
        for option in self.options:
            option.check_for_mouse_selection(pygame.mouse.get_pos())
            if self.current_option is not None:
                self.options[self.current_option].highlight()
            self.screen.blit(option.label, option.position)