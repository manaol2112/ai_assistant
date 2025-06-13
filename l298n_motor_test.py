import RPi.GPIO as GPIO
import time

# Define GPIO pins
IN1 = 17  # Motor A
IN2 = 18
IN3 = 27 # Motor B
IN4 = 22

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Moving forward")

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("Stopped")

try:
    move_forward()
    time.sleep(3)  # Run forward for 3 seconds
    stop()
    time.sleep(1)
finally:
    GPIO.cleanup()
