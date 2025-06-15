"""
motor_control.py
Premium Motor Controller for Raspberry Pi 5 (L298N, RGPIO) with Arduino Serial Support
"""
import sys
import platform
import serial
import time

try:
    if platform.system() == 'Linux' and 'arm' in platform.machine():
        import RGPIO as GPIO  # For Pi 5, RGPIO is required
    else:
        GPIO = None
except ImportError:
    GPIO = None

class MotorController:
    """
    MotorController for L298N using RGPIO (Pi 5 compatible) or Arduino Serial.
    Controls four DC motors (A, B, C, D) for forward, backward, left, right, stop.
    Supports both direct GPIO control and Arduino serial communication.
    """
    # Default pin mapping (BCM) for direct GPIO control
    IN1 = 17
    IN2 = 18
    IN3 = 27
    IN4 = 22
    ENA = 23  # Optional: PWM for speed
    ENB = 24  # Optional: PWM for speed

    def __init__(self, in1=None, in2=None, in3=None, in4=None, ena=None, enb=None, 
                 use_arduino=True, arduino_port='/dev/ttyUSB0', arduino_baud=9600):
        """
        Initialize MotorController with Arduino serial support or GPIO fallback.
        
        Args:
            use_arduino: Try Arduino serial communication first (default True)
            arduino_port: Serial port for Arduino (default '/dev/ttyUSB0')
            arduino_baud: Baud rate for Arduino communication (default 9600)
        """
        self.use_arduino = use_arduino
        self.arduino_port = arduino_port
        self.arduino_baud = arduino_baud
        self.arduino_serial = None
        self.enabled = False
        self.movement_duration = 1.0  # Default movement duration in seconds
        
        # Try Arduino serial communication first
        if self.use_arduino:
            try:
                print(f"[MotorController] Attempting Arduino serial connection on {arduino_port}...")
                self.arduino_serial = serial.Serial(arduino_port, arduino_baud, timeout=1)
                time.sleep(2)  # Wait for Arduino to initialize
                
                # Test connection with a safe stop command
                self.arduino_serial.write(b"MOTOR_A_STOP\n")
                self.arduino_serial.flush()
                time.sleep(0.1)
                
                self.enabled = True
                print(f"[MotorController] ✅ Arduino connected successfully on {arduino_port}")
                return
                
            except Exception as e:
                print(f"[MotorController] ⚠️ Arduino connection failed: {e}")
                print("[MotorController] Falling back to GPIO control...")
                self.arduino_serial = None
        
        # Fallback to GPIO control
        if GPIO is None:
            print("[MotorController] ❌ Not running on Raspberry Pi 5 with RGPIO. Motor control disabled.")
            self.enabled = False
            return
            
        try:
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
            
            print("[MotorController] ✅ GPIO control initialized successfully")
            
        except Exception as e:
            print(f"[MotorController] ❌ GPIO initialization failed: {e}")
            self.enabled = False

    def _send_arduino_command(self, command):
        """Send command to Arduino via serial"""
        if self.arduino_serial and self.enabled:
            try:
                self.arduino_serial.write(f"{command}\n".encode())
                self.arduino_serial.flush()
                print(f"[MotorController] Arduino command sent: {command}")
                time.sleep(0.1)  # Small delay for Arduino processing
                return True
            except Exception as e:
                print(f"[MotorController] ⚠️ Arduino command failed: {e}")
                return False
        return False

    def forward(self, duration=None):
        """Move all motors forward"""
        if not self.enabled: 
            return
            
        duration = duration or self.movement_duration
        
        if self.arduino_serial:
            # Arduino: Move all motors forward
            print("[MotorController] 🚀 Moving forward...")
            self._send_arduino_command("MOTOR_A_FORWARD")
            self._send_arduino_command("MOTOR_B_FORWARD")
            self._send_arduino_command("MOTOR_C_FORWARD")
            self._send_arduino_command("MOTOR_D_FORWARD")
            
            # Move for specified duration, then stop
            time.sleep(duration)
            self.stop()
        else:
            # GPIO: Traditional two-motor forward
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            time.sleep(duration)
            self.stop()

    def backward(self, duration=None):
        """Move all motors backward"""
        if not self.enabled: 
            return
            
        duration = duration or self.movement_duration
        
        if self.arduino_serial:
            # Arduino: Move all motors backward
            print("[MotorController] ⬅️ Moving backward...")
            self._send_arduino_command("MOTOR_A_BACKWARD")
            self._send_arduino_command("MOTOR_B_BACKWARD")
            self._send_arduino_command("MOTOR_C_BACKWARD")
            self._send_arduino_command("MOTOR_D_BACKWARD")
            
            # Move for specified duration, then stop
            time.sleep(duration)
            self.stop()
        else:
            # GPIO: Traditional two-motor backward
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            time.sleep(duration)
            self.stop()

    def left(self, duration=None):
        """Turn left"""
        if not self.enabled: 
            return
            
        duration = duration or self.movement_duration
        
        if self.arduino_serial:
            # Arduino: Left side motors backward, right side forward (tank turn)
            print("[MotorController] ↪️ Turning left...")
            self._send_arduino_command("MOTOR_A_BACKWARD")  # Left front
            self._send_arduino_command("MOTOR_B_FORWARD")   # Right front
            self._send_arduino_command("MOTOR_C_BACKWARD")  # Left rear
            self._send_arduino_command("MOTOR_D_FORWARD")   # Right rear
            
            # Turn for specified duration, then stop
            time.sleep(duration)
            self.stop()
        else:
            # GPIO: Traditional left turn
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            time.sleep(duration)
            self.stop()

    def right(self, duration=None):
        """Turn right"""
        if not self.enabled: 
            return
            
        duration = duration or self.movement_duration
        
        if self.arduino_serial:
            # Arduino: Right side motors backward, left side forward (tank turn)
            print("[MotorController] ↩️ Turning right...")
            self._send_arduino_command("MOTOR_A_FORWARD")   # Left front
            self._send_arduino_command("MOTOR_B_BACKWARD")  # Right front
            self._send_arduino_command("MOTOR_C_FORWARD")   # Left rear
            self._send_arduino_command("MOTOR_D_BACKWARD")  # Right rear
            
            # Turn for specified duration, then stop
            time.sleep(duration)
            self.stop()
        else:
            # GPIO: Traditional right turn
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            time.sleep(duration)
            self.stop()

    def stop(self):
        """Stop all motors"""
        if not self.enabled: 
            return
            
        if self.arduino_serial:
            # Arduino: Stop all motors
            print("[MotorController] 🛑 Stopping all motors...")
            self._send_arduino_command("MOTOR_A_STOP")
            self._send_arduino_command("MOTOR_B_STOP")
            self._send_arduino_command("MOTOR_C_STOP")
            self._send_arduino_command("MOTOR_D_STOP")
        else:
            # GPIO: Traditional stop
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)

    def test_arduino_connection(self):
        """Test Arduino connection and motor functionality"""
        if not self.arduino_serial or not self.enabled:
            print("[MotorController] ❌ Arduino not connected for testing")
            return False
            
        print("[MotorController] 🧪 Testing Arduino motor control...")
        
        try:
            # Test each motor individually
            motors = ['A', 'B', 'C', 'D']
            
            for motor in motors:
                print(f"[MotorController] Testing Motor {motor}...")
                
                # Forward test
                self._send_arduino_command(f"MOTOR_{motor}_FORWARD")
                time.sleep(0.5)
                self._send_arduino_command(f"MOTOR_{motor}_STOP")
                time.sleep(0.2)
                
                # Backward test
                self._send_arduino_command(f"MOTOR_{motor}_BACKWARD")
                time.sleep(0.5)
                self._send_arduino_command(f"MOTOR_{motor}_STOP")
                time.sleep(0.2)
                
                print(f"[MotorController] ✅ Motor {motor} test complete")
            
            print("[MotorController] 🎉 All motor tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"[MotorController] ❌ Arduino test failed: {e}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if not self.enabled: 
            return
            
        try:
            # Stop all motors first
            self.stop()
            
            if self.arduino_serial:
                print("[MotorController] Closing Arduino serial connection...")
                self.arduino_serial.close()
                self.arduino_serial = None
            
            if GPIO and hasattr(self, 'pwm_a'):
                self.pwm_a.stop()
                self.pwm_b.stop()
                GPIO.cleanup()
                
            print("[MotorController] ✅ Cleanup completed")
            
        except Exception as e:
            print(f"[MotorController] ⚠️ Cleanup error: {e}")

    def get_status(self):
        """Get current motor controller status"""
        if not self.enabled:
            return "Motor controller disabled"
        elif self.arduino_serial:
            return f"Arduino serial active on {self.arduino_port}"
        else:
            return "GPIO control active"

# Test function for standalone testing
if __name__ == "__main__":
    print("🤖 Testing Arduino Motor Controller...")
    
    # Initialize motor controller
    motor = MotorController()
    
    if motor.enabled:
        print(f"Status: {motor.get_status()}")
        
        if motor.arduino_serial:
            # Run Arduino connection test
            motor.test_arduino_connection()
            
            # Test movement commands
            print("\n🚀 Testing movement commands...")
            print("Forward...")
            motor.forward(1.0)
            time.sleep(0.5)
            
            print("Backward...")
            motor.backward(1.0)
            time.sleep(0.5)
            
            print("Left turn...")
            motor.left(1.0)
            time.sleep(0.5)
            
            print("Right turn...")
            motor.right(1.0)
            time.sleep(0.5)
            
            print("Final stop...")
            motor.stop()
        
        motor.cleanup()
        print("✅ Test completed!")
    else:
        print("❌ Motor controller not available for testing") 