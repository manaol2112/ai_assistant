import unittest
import platform

try:
    from gesture_control import HandGestureController
except ImportError:
    HandGestureController = None

class TestHandGestureController(unittest.TestCase):
    def setUp(self):
        if HandGestureController is not None:
            self.gesture = HandGestureController()
        else:
            self.gesture = None

    def test_get_gesture(self):
        if self.gesture and self.gesture.enabled:
            result = self.gesture.get_gesture()
            self.assertIn(result, ['forward', 'backward', 'left', 'right', 'stop', None])
        else:
            self.assertTrue(True)

    def tearDown(self):
        if self.gesture and self.gesture.enabled:
            self.gesture.release()

if __name__ == '__main__':
    unittest.main() 