import unittest

from bubbles import *


class BubbleTest(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(200, 200, 3, [3, 5])
        self.hexagon = Hexagon(250, 250, 2, [4, 4])

    def test_ball_has_image(self):
        self.assertIsNotNone(self.ball.image, 'Ball has no image')

    def test_hex_has_image(self):
        self.assertIsNotNone(self.hexagon.image, 'Hexagon has no image')

    @staticmethod
    def move_bubble(bubble):
        bubble.update()
        end_rect = bubble.rect
        return end_rect

    def test_ball_movement(self):
        start_rect = self.ball.rect
        end_rect = self.move_bubble(self.ball)
        self.assertEqual(start_rect.move(self.ball.speed), end_rect)

    def test_hex_movement(self):
        start_rect = self.hexagon.rect
        end_rect = self.move_bubble(self.hexagon)
        self.assertEqual(start_rect.move(self.hexagon.speed), end_rect)

if __name__ == '__main__':
    unittest.main()
