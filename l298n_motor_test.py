import RPi.GPIO as GPIO
import time
import sys

# Pin Definitions (change as needed for your wiring)
IN1 = 17  # GPIO pin for IN1 on L298N
IN2 = 27  # GPIO pin for IN2 on L298N
ENA = 22  # GPIO pin for ENA (enable) on L298N


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)


def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENA, GPIO.HIGH)
    print("Motor moving forward...")


def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    print("Motor moving backward...")


def stop():
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    print("Motor stopped.")


def cleanup():
    GPIO.cleanup()
    print("GPIO cleaned up.")


def main():
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'cleanup'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setwarnings'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'setmode'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'BCM'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'HIGH'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'LOW'):
        print("RPi.GPIO not available. This script must be run on a Raspberry Pi.")
        sys.exit(1)
    if not hasattr(GPIO, 'output'):
        print