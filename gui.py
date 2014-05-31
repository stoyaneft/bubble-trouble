from pygame.locals import *
from collections import OrderedDict

from game import *
from menu import *

pygame.init()
pygame.display.set_caption('Bubble Trouble')
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 30)
game = Game()


def start_level(level):
    game.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    while game.is_running:
        draw_world()
        handle_game_event()
        pygame.display.update()
        game.update()
        clock.tick(FPS)


def start_main_menu():
    while main_menu.is_active:
        main_menu.draw()
        handle_menu_event(main_menu)
        pygame.display.update()
        clock.tick(FPS)


def start_load_level_menu():
    while load_level_menu.is_active:
        load_level_menu.draw()
        handle_menu_event(load_level_menu)
        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    pygame.quit()
    sys.exit()


main_menu = Menu(screen, OrderedDict([('New game', (start_level, 1)), ('Load level', start_load_level_menu), ('Quit', quit_game)]))
levels_available = [(str(lvl), (start_level, lvl)) for lvl in game.levels_available]
levels_available.append(('Back', start_main_menu))
load_level_menu = Menu(screen, OrderedDict(levels_available))


def draw_ball(ball):
    screen.blit(ball.image, ball.rect)


def draw_hex(hexagon):
    screen.blit(hexagon.image, hexagon.rect)


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
    screen.fill(WHITE)
    for hexagon in game.hexagons:
        draw_hex(hexagon)
    for ball in game.balls:
        draw_ball(ball)
    if game.player.weapon.is_active:
        draw_weapon(game.player.weapon)
    draw_player(game.player)
    draw_timer()
    if game.game_over:
        draw_message("Game over!", RED)
    if game.is_completed:
        draw_message("Congratulations! You win!!!", PURPLE)
        start_main_menu()
    if game.level_completed and not game.is_completed:
        draw_message("Well done! Level completed!", BLUE)


def handle_game_event():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                game.player.moving_left = True
            elif event.key == K_RIGHT:
                game.player.moving_right = True
            elif event.key == K_SPACE and not game.player.weapon.is_active:
                game.player.shoot()
            elif event.key == K_ESCAPE:
                quit_game()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                game.player.moving_left = False
            elif event.key == K_RIGHT:
                game.player.moving_right = False
        if event.type == QUIT:
            quit_game()


def handle_menu_event(menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu == main_menu:
                    quit_game()
                else:
                    start_main_menu()
            if (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and menu.current_option is None:
                menu.current_option = 0
                pygame.mouse.set_visible(False)
            elif event.key == pygame.K_UP and menu.current_option > 0:
                menu.current_option -= 1
            elif event.key == pygame.K_UP and menu.current_option == 0:
                menu.current_option = len(menu.options) - 1
            elif event.key == pygame.K_DOWN and menu.current_option < len(menu.options) - 1:
                menu.current_option += 1
            elif event.key == pygame.K_DOWN and menu.current_option == len(menu.options) - 1:
                menu.current_option = 0
            elif event.key == pygame.K_RETURN:
                if not isinstance(menu.functions[menu.options[menu.current_option].text], tuple):
                    menu.functions[menu.options[menu.current_option].text]()
                else:
                    menu.functions[menu.options[menu.current_option].text][0](menu.functions[menu.options[menu.current_option].text][1])

        elif event.type == MOUSEBUTTONUP:
            for option in menu.options:
                if option.is_selected:
                    if not isinstance(menu.functions[option.text], tuple):
                        menu.functions[option.text]()
                    else:
                        menu.functions[option.text][0](menu.functions[option.text][1])
        if pygame.mouse.get_rel() != (0, 0):
            pygame.mouse.set_visible(True)
            menu.current_option = None


