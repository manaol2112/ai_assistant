#!/usr/bin/env python3
"""
Motor Controller for AI Assistant Robot
Supports L298N motor driver with 4 DC motors via Arduino serial or direct GPIO
Non-blocking movement commands to prevent speech recognition interference
"""

import time
import threading
import platform
import logging

# Try to import serial for Arduino communication
try:
    import serial
except ImportError:
    serial = None

# Try to import GPIO for direct control (Raspberry Pi 5 with RGPIO)
try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

logger = logging.getLogger(__name__)

class MotorController:
    """
    MotorController for L298N using RGPIO (Pi 5 compatible) or Arduino Serial.
    Controls four DC motors (A, B, C, D) for forward, backward, left, right, stop.
    Supports both direct GPIO control and Arduino serial communication.
    NON-BLOCKING: All movements run in separate threads to prevent speech interference.
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
        Initialize motor controller with Arduino serial or GPIO fallback
        
        Args:
            use_arduino: Try Arduino serial communication first
            arduino_port: Serial port for Arduino (usually /dev/ttyUSB0)
            arduino_baud: Baud rate for Arduino communication
            in1-in4, ena, enb: GPIO pins for direct control fallback
        """
        self.enabled = False
        self.arduino_serial = None
        self.use_arduino = use_arduino
        self.movement_duration = 1.0  # Default movement duration in seconds
        
        # Threading for non-blocking movements
        self.movement_thread = None
        self.stop_movement_event = threading.Event()
        self.current_movement = None
        self.movement_lock = threading.Lock()
        
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

    def _execute_movement_threaded(self, action: str, duration: float):
        """Execute movement in a separate thread (NON-BLOCKING)"""
        def movement_worker():
            try:
                with self.movement_lock:
                    self.current_movement = action
                    self.stop_movement_event.clear()
                
                print(f"[MotorController] 🚀 Starting {action} movement for {duration}s")
                
                # Start the movement
                if action == 'forward':
                    self._start_forward_movement()
                elif action == 'backward':
                    self._start_backward_movement()
                elif action == 'left':
                    self._start_left_movement()
                elif action == 'right':
                    self._start_right_movement()
                
                # Wait for duration or stop signal
                self.stop_movement_event.wait(timeout=duration)
                
                # Stop the movement
                self._stop_all_motors()
                
                with self.movement_lock:
                    self.current_movement = None
                
                print(f"[MotorController] ✅ {action} movement completed")
                
            except Exception as e:
                print(f"[MotorController] ❌ Movement thread error: {e}")
                self._stop_all_motors()
                with self.movement_lock:
                    self.current_movement = None
        
        # Stop any existing movement
        self.stop()
        
        # Start new movement thread
        self.movement_thread = threading.Thread(target=movement_worker, daemon=True)
        self.movement_thread.start()

    def _start_forward_movement(self):
        """Start forward movement (internal method)"""
        if self.arduino_serial:
            self._send_arduino_command("MOTOR_A_FORWARD")
            self._send_arduino_command("MOTOR_B_FORWARD")
            self._send_arduino_command("MOTOR_C_FORWARD")
            self._send_arduino_command("MOTOR_D_FORWARD")
        else:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)

    def _start_backward_movement(self):
        """Start backward movement (internal method)"""
        if self.arduino_serial:
            self._send_arduino_command("MOTOR_A_BACKWARD")
            self._send_arduino_command("MOTOR_B_BACKWARD")
            self._send_arduino_command("MOTOR_C_BACKWARD")
            self._send_arduino_command("MOTOR_D_BACKWARD")
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)

    def _start_left_movement(self):
        """Start left turn movement (internal method)"""
        if self.arduino_serial:
            self._send_arduino_command("MOTOR_A_BACKWARD")  # Left front
            self._send_arduino_command("MOTOR_B_FORWARD")   # Right front
            self._send_arduino_command("MOTOR_C_BACKWARD")  # Left rear
            self._send_arduino_command("MOTOR_D_FORWARD")   # Right rear
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)

    def _start_right_movement(self):
        """Start right turn movement (internal method)"""
        if self.arduino_serial:
            self._send_arduino_command("MOTOR_A_FORWARD")   # Left front
            self._send_arduino_command("MOTOR_B_BACKWARD")  # Right front
            self._send_arduino_command("MOTOR_C_FORWARD")   # Left rear
            self._send_arduino_command("MOTOR_D_BACKWARD")  # Right rear
        else:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)

    def _stop_all_motors(self):
        """Stop all motors immediately (internal method)"""
        if self.arduino_serial:
            self._send_arduino_command("MOTOR_A_STOP")
            self._send_arduino_command("MOTOR_B_STOP")
            self._send_arduino_command("MOTOR_C_STOP")
            self._send_arduino_command("MOTOR_D_STOP")
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)

    # PUBLIC NON-BLOCKING METHODS
    def forward(self, duration=None):
        """Move all motors forward (NON-BLOCKING)"""
        if not self.enabled: 
            return
        duration = duration or self.movement_duration
        self._execute_movement_threaded('forward', duration)

    def backward(self, duration=None):
        """Move all motors backward (NON-BLOCKING)"""
        if not self.enabled: 
            return
        duration = duration or self.movement_duration
        self._execute_movement_threaded('backward', duration)

    def left(self, duration=None):
        """Turn left (NON-BLOCKING)"""
        if not self.enabled: 
            return
        duration = duration or self.movement_duration
        self._execute_movement_threaded('left', duration)

    def right(self, duration=None):
        """Turn right (NON-BLOCKING)"""
        if not self.enabled: 
            return
        duration = duration or self.movement_duration
        self._execute_movement_threaded('right', duration)

    def stop(self):
        """Stop all motors immediately"""
        if not self.enabled: 
            return
        
        # Signal any running movement to stop
        self.stop_movement_event.set()
        
        # Wait for movement thread to finish (with timeout)
        if self.movement_thread and self.movement_thread.is_alive():
            self.movement_thread.join(timeout=0.5)
        
        # Force stop all motors
        self._stop_all_motors()
        
        with self.movement_lock:
            self.current_movement = None
        
        print("[MotorController] 🛑 All motors stopped")

    def get_current_movement(self):
        """Get current movement status"""
        with self.movement_lock:
            return self.current_movement

    def is_moving(self):
        """Check if motors are currently moving"""
        return self.get_current_movement() is not None

    # CONTINUOUS MOVEMENT METHODS (for gesture control)
    def forward_continuous(self):
        """Start continuous forward movement (until stopped)"""
        if not self.enabled: 
            return
        self.stop()  # Stop any existing movement
        self._start_forward_movement()
        with self.movement_lock:
            self.current_movement = 'forward_continuous'

    def backward_continuous(self):
        """Start continuous backward movement (until stopped)"""
        if not self.enabled: 
            return
        self.stop()  # Stop any existing movement
        self._start_backward_movement()
        with self.movement_lock:
            self.current_movement = 'backward_continuous'

    def left_continuous(self):
        """Start continuous left turn (until stopped)"""
        if not self.enabled: 
            return
        self.stop()  # Stop any existing movement
        self._start_left_movement()
        with self.movement_lock:
            self.current_movement = 'left_continuous'

    def right_continuous(self):
        """Start continuous right turn (until stopped)"""
        if not self.enabled: 
            return
        self.stop()  # Stop any existing movement
        self._start_right_movement()
        with self.movement_lock:
            self.current_movement = 'right_continuous'

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
            
            # Wait for any movement threads to finish
            if self.movement_thread and self.movement_thread.is_alive():
                self.movement_thread.join(timeout=1.0)
            
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
            movement = self.get_current_movement()
            if movement:
                return f"Arduino connected - Currently: {movement}"
            else:
                return "Arduino connected - Idle"
        else:
            movement = self.get_current_movement()
            if movement:
                return f"GPIO control active - Currently: {movement}"
            else:
                return "GPIO control active - Idle"

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