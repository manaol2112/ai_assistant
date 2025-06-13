"""
motor_control.py
Premium Motor Controller for Raspberry Pi 5 (L298N, RGPIO)
"""
import sys
import platform

try:
    if platform.system() == 'Linux' and 'arm' in platform.machine():
        import RGPIO as GPIO  # For Pi 5, RGPIO is required
    else:
        GPIO = None
except ImportError:
    GPIO = None

class MotorController:
    """
    MotorController for L298N using RGPIO (Pi 5 compatible).
    Controls two DC motors for forward, backward, left, right, stop.
    """
    # Default pin mapping (BCM)
    IN1 = 17
    IN2 = 18
    IN3 = 27
    IN4 = 22
    ENA = 23  # Optional: PWM for speed
    ENB = 24  # Optional: PWM for speed

    def __init__(self, in1=None, in2=None, in3=None, in4=None, ena=None, enb=None):
        if GPIO is None:
            print("[MotorController] Not running on Raspberry Pi 5 with RGPIO. Motor control disabled.")
            self.enabled = False
            return
        self.IN1 = in1 or self.IN1
        self.IN2 = in2 or self.IN2
        self.IN3 = in3 or self.IN3
        self.IN4 = in4 or self.IN4
        self.ENA = ena or self.ENA
        self.ENB = enb or self.ENB
        self.enabled = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.pwm_a = GPIO.PWM(self.ENA, 1000)
        self.pwm_b = GPIO.PWM(self.ENB, 1000)
        self.pwm_a.start(100)
        self.pwm_b.start(100)

    def forward(self):
        if not self.enabled: return
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        if not self.enabled: return
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def left(self):
        if not self.enabled: return
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self):
        if not self.enabled: return
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def stop(self):
        if not self.enabled: return
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def cleanup(self):
        if not self.enabled: return
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup() 