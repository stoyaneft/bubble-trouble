import json
from threading import Timer
import time
import sys

from ball import *
from hexagon import *
from player import *


class Game:

    def __init__(self, level=1):
        self.balls = []
        self.hexagons = []
        self.player = Player()
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
        self.balls = []
        self.hexagons = []
        self.player.reset_position()
        self.level_completed = False
        self.level = level
        self.player.is_alive = True
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
        for ball_index in range(len(self.balls)):
            ball = self.balls[ball_index]
            if pygame.sprite.collide_rect(ball, self.player.weapon) \
                    and self.player.weapon.is_active:
                self.player.weapon.is_active = False
                self._split_ball(ball_index)
                return
            if pygame.sprite.collide_mask(ball, self.player):
                self.player.is_alive = False
                self._decrease_lives()
                return
        for hex_index in range(len(self.hexagons)):
            hexagon = self.hexagons[hex_index]
            if pygame.sprite.collide_rect(hexagon, self.player.weapon) \
                    and self.player.weapon.is_active:
                self.player.weapon.is_active = False
                self._split_hexagon(hex_index)
                return
            if pygame.sprite.collide_mask(hexagon, self.player):
                self.player.is_alive = False
                self._decrease_lives()
                return

    def _check_player_collision(self):
        for ball_index in range(len(self.balls)):
            ball = self.balls[ball_index]
            if pygame.sprite.collide_mask(ball, self.player.weapon) \
                    and self.player.weapon.is_active:
                self.player.weapon.is_active = False
                self._split_ball(ball_index)
                return
            if pygame.sprite.collide_mask(ball, self.player):
                self.player.is_alive = False
                self._decrease_lives()
                return

    def _decrease_lives(self):
        self.player.lives -= 1
        if self.player.lives:
            self.restart()
        else:
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
        self.player.update()
        if not len(self.balls) and not len(self.hexagons):
            self.level_completed = True
            if self.level == self.max_level:
                self.is_completed = True

    def _timer(self, interval, worker_func, iterations=0):
        if iterations and self.player.is_alive and not self.level_completed:
            Timer(
                interval, self._timer,
                [interval, worker_func, 0 if iterations ==
                    0 else iterations - 1]
            ).start()
            worker_func()

    def _tick_second(self):
        self.time_left -= 1
        if self.time_left == 0:
            self._decrease_lives()

    @staticmethod
    def pause(seconds):
        time.sleep(seconds)
