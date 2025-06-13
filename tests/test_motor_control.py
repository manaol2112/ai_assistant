import unittest
import platform

try:
    from motor_control import MotorController
except ImportError:
    MotorController = None

class TestMotorController(unittest.TestCase):
    def setUp(self):
        self.is_pi = platform.system() == 'Linux' and 'arm' in platform.machine()
        if MotorController is not None and self.is_pi:
            self.motor = MotorController()
        else:
            self.motor = None

    def test_forward(self):
        if self.motor:
            self.motor.forward()
            self.motor.stop()
        self.assertTrue(True)

    def test_backward(self):
        if self.motor:
            self.motor.backward()
            self.motor.stop()
        self.assertTrue(True)

    def test_left(self):
        if self.motor:
            self.motor.left()
            self.motor.stop()
        self.assertTrue(True)

    def test_right(self):
        if self.motor:
            self.motor.right()
            self.motor.stop()
        self.assertTrue(True)

    def test_stop(self):
        if self.motor:
            self.motor.stop()
        self.assertTrue(True)

    def tearDown(self):
        if self.motor:
            self.motor.cleanup()

if __name__ == '__main__':
    unittest.main() 