import re
from ball import *
from player import *

class Gameworld:
    def __init__(self, level=1):
        self.balls = []
        self.player = Player()
        self.level = level
        self.load_level(1)
        self.game_over = False
        self.level_completed = False

    def load_level(self, level):
        self.balls = []
        self.player.reset_position()
        self.level_completed = False
        self.level = level
        level_path = "levels/level" + str(level) + ".txt"
        level_file = open(level_path, 'r')
        lines = level_file.readlines()
        lines = list(map(str.rstrip, lines))
        ball_re = re.compile(r'ball x, y=(\d+), (\d+) size=(\d+) direction=(\w+)')
        for line in lines:
            match = re.match(ball_re, line)
            x, y, size = list(map(int, match.groups()[:-1]))
            direction = match.groups()[-1]
            self.balls.append(Ball(x, y, size, direction))

    def check_for_collisions(self):
        for ball_index in range(len(self.balls)):
            ball = self.balls[ball_index]
            ball_rect = self.balls[ball_index].image.get_rect(left=ball.x, top=ball.y)
            weapon_rect = self.player.weapon.image.get_rect(left=self.player.weapon.x, top=self.player.weapon.y)
            player_rect = self.player.image.get_rect(left=self.player.x, top=self.player.y)
            if ball_rect.colliderect(weapon_rect) and self.player.weapon.is_active:
                self.player.weapon.is_active = False
                self.split_ball(ball_index)
                print(ball_index)
                return
            if ball_rect.colliderect(player_rect):
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
            self.balls.append(Ball(ball.x - 25, ball.y - 10, ball.size - 1, UPLEFT))
            self.balls.append(Ball(ball.x + 25, ball.y - 10, ball.size - 1, UPRIGHT))
            del self.balls[ball_index]

    def update(self):
        for ball in self.balls:
            ball.update()
        self.player.update()
        self.check_for_collisions()
        if not len(self.balls):
            self.level_completed = True




