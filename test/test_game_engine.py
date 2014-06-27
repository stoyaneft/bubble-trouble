import unittest
import settings

from game import *


class GameEngineTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        ball = Ball(50, WINDOWHEIGHT - 20, 2, [0, 3])
        self.game.balls.append(ball)
        hex = Hexagon(20, WINDOWHEIGHT - 20, 2, [3, 3])
        self.game.hexagons.append(hex)

    # def test_bubbles_loaded(self, level, bubbles):
    #     for bubble_index, bubble in enumerate(bubbles):
    #         ball_properties = {}
    #         ball_properties['x'] = bubble.rect.centerx
    #         ball_properties['y'] = bubble.rect.centery
    #         ball_properties['size'] = bubble.size
    #         ball_properties['speed'] = bubble.speed
    #         self.assertEqual(ball_properties, level[str(bubble) + 's'][bubble_index])
    #
    # def test_load_level(self):
    #     self.game.load_level(2)
    #     with open('levels.json', 'r') as levels_file:
    #         levels = json.load(levels_file)
    #         level = levels[str(self.game.level)]
    #     self.assertEqual(self.game.time_left, level['time'])
    #     self.test_bubbles_loaded(level, self.game.balls)
    #     self.test_bubbles_loaded(level, self.game.hexagons)

    def test_bubble_collision(self):
        ballRect = self.game.balls[0].rect
        ball_center_x, ball_center_y = ballRect.centerx, ballRect.centery
        self.game.players[0].set_position(ball_center_x, WINDOWHEIGHT)
        self.assertTrue(self.game._check_for_bubble_collision(self.game.balls, True, self.game.players[0]))
        self.game.players[0].set_position(ball_center_x - ballRect.width, WINDOWHEIGHT)
        self.assertFalse(self.game._check_for_bubble_collision(self.game.balls, True, self.game.players[0]))
        self.assertTrue(self.game._check_for_bubble_collision(self.game.hexagons, False, self.game.players[0]))
        self.game.players[0].weapon = Weapon(ball_center_x, ball_center_y)
        self.game.players[0].weapon.is_active = True
        self.assertTrue(self.game._check_for_bubble_collision(self.game.balls, True, self.game.players[0]))
        self.game.players[0].weapon = Weapon(ball_center_x, ball_center_y + ballRect.height)
        self.game.players[0].weapon.is_active = True
        self.assertFalse(self.game._check_for_bubble_collision(self.game.balls, True, self.game.players[0]))

    def test_split_ball(self):
        startNumOfBalls = len(self.game.balls)
        startBallSize = self.game.balls[0].size
        self.game._split_ball(0)
        self.assertEqual(len(self.game.balls), startNumOfBalls + 1)
        self.assertEqual(self.game.balls[0].size, startBallSize - 1)
        self.assertEqual(self.game.balls[1].size, startBallSize - 1)

    def test_level_completed(self):
        while self.game.balls:
            for ball_index in range(len(self.game.balls)):
                self.game._split_ball(ball_index)
                return
        while self.game.hexagons:
            for hex_index in range(len(self.game.balls)):
                self.game._split_hexagon(hex_index)
                return
        self.game.update()
        self.assertTrue(self.game.level_completed)

    def test_decrease_lives(self):
        startLives = self.game.players[0].lives
        self.game._decrease_lives(self.game.players[0])
        self.assertEqual(self.game.players[0].lives, startLives - 1)

    def test_player_dies(self):
        player = self.game.players[0]
        ballRect = self.game.balls[0].rect
        ball_center_x, ball_center_y = ballRect.centerx, ballRect.centery
        self.game.players[0].set_position(ball_center_x, WINDOWHEIGHT)
        self.game._check_for_bubble_collision(self.game.balls, True, self.game.players[0])
        self.assertFalse(player.is_alive)
        self.assertTrue(self.game.dead_player)

    def test_game_over(self):
        player = self.game.players[0]
        player.lives = 1
        self.game._decrease_lives(player)
        self.assertTrue(self.game.game_over)

    def test_game_completed(self):
        self.game.load_level(self.game.max_level)
        self.game.balls = []
        self.game.hexagons = []
        self.game.update()
        self.assertTrue(self.game.is_completed)

    def test_tick_second(self):
        self.game.load_level(1)
        start_time = self.game.time_left
        self.game._tick_second()
        self.assertEqual(self.game.time_left, start_time - 1)

    # def test_timer(self):
    #     self.game.load_level(1)
    #     start_time = self.game.time_left
    #     end_time = self.game.time_left
    #     self.assertEqual(start_time, end_time + 3)

    def test_max_level_available_read(self):
        with open(APP_PATH + 'max_level_available', 'r') as max_completed_level_file:
            max_level_available = int(max_completed_level_file.read())
            self.assertEqual(max_level_available, self.game.max_level_available)

    # def test_max_level_available_file_updates(self):
    #     with open('max_level_available', 'r') as max_completed_level_file:
    #         max_level_available_before = int(max_completed_level_file.read())
    #     self.game.load_level(max_level_available_before)
    #     self.game.level_completed = True
    #     self.game.update()
    #     with open('max_level_available', 'r') as max_completed_level_file:
    #         max_level_available_after = int(max_completed_level_file.read())
    #     self.assertEqual(max_level_available_after, max_level_available_before + 1)



if __name__ == '__main__':
    unittest.main()
