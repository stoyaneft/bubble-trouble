import json
from threading import Timer
import time
import sys

from bubbles import *
from player import *


class Game:

    def __init__(self, level=1):
        self.balls = []
        self.hexagons = []
        self.players = [Player()]
        self.level = level
        self.game_over = False
        self.level_completed = False
        self.is_running = True
        self.is_completed = False
        self.max_level = MAX_LEVEL
        self.is_multiplayer = False
        with open('max_level_available', 'r') as max_completed_level_file:
            max_level_available = max_completed_level_file.read()
            if max_level_available:
                self.max_level_available = int(max_level_available)
            else:
                self.max_level_available = 1

    def load_level(self, level):
        if self.is_multiplayer and len(self.players) == 1:
            self.players.append(Player())
        self.balls = []
        self.hexagons = []
        for index, player in enumerate(self.players):
            player_number = index + 1
            num_of_players = len(self.players)
            player.set_position((WINDOWWIDTH / (num_of_players + 1)) * player_number, WINDOWHEIGHT)
            player.is_alive = True
        self.level_completed = False
        self.level = level
        if self.level > self.max_level_available:
            self.max_level_available = self.level
            with open('max_level_available', 'w') as max_completed_level_file:
                max_completed_level_file.write(str(self.max_level_available))
        with open('levels.json', 'r') as levels_file:
            levels = json.load(levels_file)
            level = levels[str(self.level)]
            self.time_left = level['time']
            for ball in level['balls']:
                x, y = ball['x'], ball['y']
                size = ball['size']
                speed = ball['speed']
                self.balls.append(Ball(x, y, size, speed))
            for hexagon in level['hexagons']:
                x, y = hexagon['x'], hexagon['y']
                size = hexagon['size']
                speed = hexagon['speed']
                self.hexagons.append(Hexagon(x, y, size, speed))
        self._start_timer()

    def _start_timer(self):
        self._timer(1, self._tick_second, self.time_left)

    def _check_for_collisions(self):
        for player_index, player in enumerate(self.players):
            self._check_for_bubble_collision(self.balls, True, player_index)
            self._check_for_bubble_collision(self.hexagons, False, player_index)

    def _check_for_bubble_collision(self, bubbles, is_ball, player_index):
        player = self.players[player_index]
        for bubble_index, bubble in enumerate(bubbles):
            if pygame.sprite.collide_rect(bubble, player.weapon) \
                    and player.weapon.is_active:
                player.weapon.is_active = False
                if is_ball:
                    self._split_ball(bubble_index)
                else:
                    self._split_hexagon(bubble_index)
                return
            if pygame.sprite.collide_mask(bubble, player):
                player.is_alive = False
                self._decrease_lives(player_index)
                return

    def _decrease_lives(self, player_index):
        player = self.players[player_index]
        player.lives -= 1
        if player.lives:
            self.restart()
        else:
            del self.players[player_index]
        if not len(self.players):
            self.game_over = True

    def restart(self):
        self.pause(1)
        self.load_level(self.level)

    def _split_ball(self, ball_index):
        ball = self.balls[ball_index]
        if ball.size > 1:
            self.balls.append(Ball(
                ball.rect.left - ball.size**2,
                ball.rect.top - 10, ball.size - 1, [-3, -5])
            )
            self.balls.append(
                Ball(ball.rect.left + ball.size**2,
                     ball.rect.top - 10, ball.size - 1, [3, -5])
            )
        del self.balls[ball_index]

    def _split_hexagon(self, hex_index):
        hexagon = self.hexagons[hex_index]
        if hexagon.size > 1:
            self.hexagons.append(
                Hexagon(hexagon.rect.left, hexagon.rect.centery,
                        hexagon.size - 1, [-3, -5]))
            self.hexagons.append(
                Hexagon(hexagon.rect.right, hexagon.rect.centery,
                        hexagon.size - 1, [3, -5]))
        del self.hexagons[hex_index]

    def update(self):
        if self.level_completed and not self.is_completed:
            self.pause(3)
            self.load_level(self.level + 1)
        if self.game_over:
            self.pause(3)
            self.is_running = False
            pygame.quit()
            sys.exit()
        self._check_for_collisions()
        for ball in self.balls:
            ball.update()
        for hexagon in self.hexagons:
            hexagon.update()
        for player in self.players:
            player.update()
        if not len(self.balls) and not len(self.hexagons):
            self.level_completed = True
            if self.level == self.max_level:
                self.is_completed = True

    def _timer(self, interval, worker_func, iterations=0):
        if iterations and self.players and not self.level_completed:
            Timer(
                interval, self._timer,
                [interval, worker_func, 0 if iterations ==
                    0 else iterations - 1]
            ).start()
            worker_func()

    def _tick_second(self):
        self.time_left -= 1
        if self.time_left == 0:
            for player_index in range(len(self.players)):
                self._decrease_lives(player_index)

    @staticmethod
    def pause(seconds):
        time.sleep(seconds)
