import RPi.GPIO as GPIO
import time
import sys
import os

def check_raspberry_pi():
    """Check if running on a Raspberry Pi"""
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            return 'raspberry pi' in model.lower()
    except:
        return False

def check_gpio_permissions():
    """Check if user has GPIO permissions"""
    try:
        # Try to access GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        return True
    except Exception as e:
        print(f"GPIO Permission Error: {e}")
        print("\nTry running the script with sudo:")
        print("sudo python l298n_motor_test.py")
        return False

# Pin Definitions
IN1 = 17  # GPIO pin for IN1 on L298N
IN2 = 27  # GPIO pin for IN2 on L298N
ENA = 22  # GPIO pin for ENA (enable) on L298N

# Speed definitions (PWM duty cycle)
LOW_SPEED = 30    # 30% duty cycle
MEDIUM_SPEED = 60  # 60% duty cycle
HIGH_SPEED = 100   # 100% duty cycle

def setup():
    """Initialize GPIO pins and PWM"""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(ENA, GPIO.OUT)
        
        # Create PWM instance for speed control
        pwm = GPIO.PWM(ENA, 1000)  # 1000 Hz frequency
        pwm.start(0)  # Start with 0% duty cycle
        
        # Initialize motor to stopped state
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        return pwm
    except Exception as e:
        print(f"Setup Error: {e}")
        print("\nPossible solutions:")
        print("1. Run the script with sudo: sudo python l298n_motor_test.py")
        print("2. Add your user to the gpio group: sudo usermod -a -G gpio $USER")
        print("3. Make sure you're running this on a Raspberry Pi")
        raise

def forward(pwm, speed):
    """Move motor forward at specified speed"""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)
    print(f"Motor moving forward at {speed}% speed...")

def backward(pwm, speed):
    """Move motor backward at specified speed"""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)
    print(f"Motor moving backward at {speed}% speed...")

def stop(pwm):
    """Stop the motor"""
    pwm.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    print("Motor stopped.")

def cleanup():
    """Clean up GPIO settings"""
    try:
        GPIO.cleanup()
        print("GPIO cleanup completed.")
    except Exception as e:
        print(f"Cleanup Error: {e}")

def test_sequence(pwm):
    """Run a complete test sequence"""
    print("\nStarting motor test sequence...")
    
    # Test forward motion at different speeds
    print("\nTesting forward motion:")
    forward(pwm, LOW_SPEED)
    time.sleep(2)
    forward(pwm, MEDIUM_SPEED)
    time.sleep(2)
    forward(pwm, HIGH_SPEED)
    time.sleep(2)
    stop(pwm)
    time.sleep(1)
    
    # Test backward motion at different speeds
    print("\nTesting backward motion:")
    backward(pwm, LOW_SPEED)
    time.sleep(2)
    backward(pwm, MEDIUM_SPEED)
    time.sleep(2)
    backward(pwm, HIGH_SPEED)
    time.sleep(2)
    stop(pwm)
    time.sleep(1)
    
    print("\nTest sequence completed.")

def main():
    """Main function to run the motor test"""
    try:
        # Check if running on Raspberry Pi
        if not check_raspberry_pi():
            print("Error: This script must be run on a Raspberry Pi.")
            print("The 'cannot determine SOC peripheral base address' error occurs when running on non-Raspberry Pi hardware.")
            sys.exit(1)
            
        # Check GPIO permissions
        if not check_gpio_permissions():
            sys.exit(1)
            
        # Initialize motor
        pwm = setup()
        
        # Run test sequence
        test_sequence(pwm)
        
        # Clean up
        cleanup()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        cleanup()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        cleanup()

if __name__ == "__main__":
    main()
