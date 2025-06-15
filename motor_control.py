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
        
        # Try Arduino serial communication first
        if self.use_arduino:
            try:
                print(f"[MotorController] Attempting Arduino serial connection on {arduino_port}...")
                self.arduino_serial = serial.Serial(arduino_port, arduino_baud, timeout=1)
                time.sleep(2)  # Wait for Arduino to initialize
                
                # Test connection
                self.arduino_serial.write(b"MOTOR_A_STOP\n")
                self.arduino_serial.flush()
                
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
                return True
            except Exception as e:
                print(f"[MotorController] ⚠️ Arduino command failed: {e}")
                return False
        return False

    def forward(self):
        """Move all motors forward"""
        if not self.enabled: 
            return
            
        if self.arduino_serial:
            # Arduino: Move all motors forward
            self._send_arduino_command("MOTOR_A_FORWARD")
            self._send_arduino_command("MOTOR_B_FORWARD")
            self._send_arduino_command("MOTOR_C_FORWARD")
            self._send_arduino_command("MOTOR_D_FORWARD")
        else:
            # GPIO: Traditional two-motor forward
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        """Move all motors backward"""
        if not self.enabled: 
            return
            
        if self.arduino_serial:
            # Arduino: Move all motors backward
            self._send_arduino_command("MOTOR_A_BACKWARD")
            self._send_arduino_command("MOTOR_B_BACKWARD")
            self._send_arduino_command("MOTOR_C_BACKWARD")
            self._send_arduino_command("MOTOR_D_BACKWARD")
        else:
            # GPIO: Traditional two-motor backward
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)

    def left(self):
        """Turn left"""
        if not self.enabled: 
            return
            
        if self.arduino_serial:
            # Arduino: Left side motors backward, right side forward
            self._send_arduino_command("MOTOR_A_BACKWARD")  # Left front
            self._send_arduino_command("MOTOR_B_FORWARD")   # Right front
            self._send_arduino_command("MOTOR_C_BACKWARD")  # Left rear
            self._send_arduino_command("MOTOR_D_FORWARD")   # Right rear
        else:
            # GPIO: Traditional left turn
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)

    def right(self):
        """Turn right"""
        if not self.enabled: 
            return
            
        if self.arduino_serial:
            # Arduino: Right side motors backward, left side forward
            self._send_arduino_command("MOTOR_A_FORWARD")   # Left front
            self._send_arduino_command("MOTOR_B_BACKWARD")  # Right front
            self._send_arduino_command("MOTOR_C_FORWARD")   # Left rear
            self._send_arduino_command("MOTOR_D_BACKWARD")  # Right rear
        else:
            # GPIO: Traditional right turn
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)

    def stop(self):
        """Stop all motors"""
        if not self.enabled: 
            return
            
        if self.arduino_serial:
            # Arduino: Stop all motors
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