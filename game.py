import re
from threading import Timer
import time
import sys

from ball import *
from player import *


class Game:
    def __init__(self, level=1):
        self.balls = []
        self.player = Player()
        self.level = level
        self.load_level(1)
        self.game_over = False
        self.level_completed = False
        self.is_running = True

    def load_level(self, level):
        self.balls = []
        self.player.reset_position()
        self.level_completed = False
        self.level = level
        self.player.is_alive = True
        ball_re = re.compile(r'ball x, y=(\d+), (\d+) size=(\d+) speed=(\d+), (\d+)')
        time_re = re.compile(r'time=(\d+)')
        level_path = "levels/level" + str(level) + ".txt"
        with open(level_path, 'r') as level_file:
            lines = level_file.readlines()
            lines = list(map(str.rstrip, lines))
            for line in lines:
                ball_match = re.match(ball_re, line)
                time_match = re.match(time_re, line)
                if time_match:
                    time = int(time_match.group(1))
                    self.time_left = time
                if ball_match:
                    x, y, size = tuple(map(int, ball_match.groups()[:3]))
                    speed = list(map(int, ball_match.groups()[3:]))
                    self.balls.append(Ball(x, y, size, speed))

    def start_timer(self):
        self._timer(1, self._tick_second, self.time_left)

    def _check_for_collisions(self):
        for ball_index in range(len(self.balls)):
            ball = self.balls[ball_index]
            if pygame.sprite.collide_rect(ball, self.player.weapon) and self.player.weapon.is_active:
                self.player.weapon.is_active = False
                self._split_ball(ball_index)
                return
            if pygame.sprite.collide_rect(ball, self.player):
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
        if ball.size == 2:
            del self.balls[ball_index]
        else:
            self.balls.append(Ball(ball.rect.left - 25, ball.rect.top - 10, ball.size - 1, [-3, -5]))
            self.balls.append(Ball(ball.rect.left + 25, ball.rect.top - 10, ball.size - 1, [3, -5]))
            del self.balls[ball_index]

    def update(self):
        if self.level_completed:
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
        self.player.update()
        if not len(self.balls):
            self.level_completed = True

    def _timer(self, interval, worker_func, iterations=0):
        if iterations and self.player.is_alive:
            Timer(
                interval, self._timer,
                [interval, worker_func, 0 if iterations == 0 else iterations-1]
            ).start()
            worker_func()

    def _tick_second(self):
        self.time_left -= 1
        if self.time_left == 0:
            self._decrease_lives()

    @staticmethod
    def pause(seconds):
        time.sleep(seconds)




