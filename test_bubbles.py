import unittest

from ball import *
from hexagon import *


class BubbleTest(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(200, 200, 3, [3, 5])
        self.hexagon = Hexagon(250, 250, 2, [4, 4])

    def test_ball_has_image(self):
        self.assertNotEqual(self.ball.image, None, 'Ball has no image')

    def test_hex_has_image(self):
        self.assertNotEqual(self.hexagon.image, None, 'Hexagon has no image')

    def test_bubble_movement(self, bubble):
        startRect = bubble.rect
        bubble.update()
        endRect = bubble.rect
        self.assertEqual(startRect.move(bubble.speed), endRect)

    def test_hex_movement(self):
        self.test_bubble_movement(self.ball)

if __name__ == '__main__':
    unittest.main()
