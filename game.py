import re
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
        self.is_paused = False

    def load_level(self, level):
        self.balls = []
        self.player.reset_position()
        self.level_completed = False
        self.level = level
        level_path = "levels/level" + str(level) + ".txt"
        level_file = open(level_path, 'r')
        lines = level_file.readlines()
        lines = list(map(str.rstrip, lines))
        ball_re = re.compile(r'ball x, y=(\d+), (\d+) size=(\d+) speed=(\d+), (\d+)')
        for line in lines:
            match = re.match(ball_re, line)
            x, y, size = list(map(int, match.groups()[:3]))
            speed = list(map(int, match.groups()[3:]))
            self.balls.append(Ball(x, y, size, speed))

    def _check_for_collisions(self):
        for ball_index in range(len(self.balls)):
            ball = self.balls[ball_index]
            if pygame.sprite.collide_rect(ball, self.player.weapon) and self.player.weapon.is_active:
                self.player.weapon.is_active = False
                self.split_ball(ball_index)
                return
            if pygame.sprite.collide_rect(ball, self.player):
                self.player.lives -= 1
                if self.player.lives:
                    self.load_level(self.level)
                    pygame.time.wait(1000)
                else:
                    self.game_over = True
                return


    def split_ball(self, ball_index):
        ball = self.balls[ball_index]
        if ball.size == 2:
            del self.balls[ball_index]
        else:
            self.balls.append(Ball(ball.rect.left - 25, ball.rect.top - 10, ball.size - 1, [-3, -5]))
            self.balls.append(Ball(ball.rect.left + 25, ball.rect.top - 10, ball.size - 1, [3, -5]))
            del self.balls[ball_index]

    def update(self):
        self._check_for_collisions()
        for ball in self.balls:
            ball.update()
        self.player.update()
        if not len(self.balls):
            self.level_completed = True

    def pause(self):
        self.is_paused = True




