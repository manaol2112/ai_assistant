#!/usr/bin/env python3
"""
Enhanced Motor Controller for AI Assistant Robot
Supports L298N motor driver with 4 DC motors via Arduino serial or direct GPIO
Non-blocking movement commands with speed calibration and safety features
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
    Enhanced MotorController for L298N with speed calibration and safety features.
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
    ENB = 24
    
    def __init__(self, in1=None, in2=None, in3=None, in4=None, ena=None, enb=None, 
                 use_arduino=True, arduino_port='/dev/ttyUSB0', arduino_baud=9600):
        """
        Initialize enhanced motor controller with speed calibration
        
        Args:
            use_arduino: Try Arduino serial communication first
            arduino_port: Serial port for Arduino (usually /dev/ttyUSB0)
            arduino_baud: Baud rate for Arduino communication
            in1-in4, ena, enb: GPIO pins for direct control fallback
        """
        self.enabled = False
        self.arduino_serial = None
        self.use_arduino = use_arduino
        self.arduino_port = arduino_port
        self.movement_duration = 1.0  # Default movement duration in seconds
        
        # Motor speed calibration (0-255) - adjust these to fix circular movement
        self.motor_speeds = {
            'A': 200,  # Front Left - reduce if robot turns right during forward
            'B': 200,  # Front Right - reduce if robot turns left during forward  
            'C': 200,  # Back Left - reduce if robot turns right during forward
            'D': 200   # Back Right - reduce if robot turns left during forward
        }
        
        # Safety features
        self.max_continuous_time = 5.0  # Maximum continuous movement time
        self.default_duration = 1.5     # Safer default duration
        self.emergency_stop_enabled = True
        
        # Threading for non-blocking movements
        self.movement_thread = None
        self.stop_movement_event = threading.Event()
        self.current_movement = None
        self.movement_lock = threading.Lock()
        self.movement_start_time = None
        
        # Initialize motor mapping for better organization
        self.motor_layout = {
            'front_left': 'A',   # Motor A - Front Left
            'front_right': 'B',  # Motor B - Front Right
            'back_left': 'C',    # Motor C - Back Left
            'back_right': 'D'    # Motor D - Back Right
        }
        
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
        if GPIO is not None:
            try:
                # Set GPIO mode
                GPIO.setmode(GPIO.BCM)
                
                # Set pin assignments
                self.IN1 = in1 or self.IN1
                self.IN2 = in2 or self.IN2  
                self.IN3 = in3 or self.IN3
                self.IN4 = in4 or self.IN4
                self.ENA = ena or self.ENA
                self.ENB = enb or self.ENB
                
                # Setup GPIO pins
                pins = [self.IN1, self.IN2, self.IN3, self.IN4, self.ENA, self.ENB]
                GPIO.setup(pins, GPIO.OUT)
                
                # Set initial state (stopped)
                GPIO.output([self.IN1, self.IN2, self.IN3, self.IN4], GPIO.LOW)
                GPIO.output([self.ENA, self.ENB], GPIO.HIGH)  # Enable motors
                
                self.enabled = True
                print("[MotorController] ✅ GPIO control initialized successfully")
                
            except Exception as e:
                print(f"[MotorController] ❌ GPIO initialization failed: {e}")
                self.enabled = False
        else:
            print("[MotorController] ⚠️ No motor control available (GPIO library not found)")
            self.enabled = False

    def _send_arduino_command(self, command):
        """Send command to Arduino with error handling"""
        if not self.arduino_serial or not self.enabled:
            return False
        
        try:
            self.arduino_serial.write(f"{command}\n".encode())
            self.arduino_serial.flush()
            return True
        except Exception as e:
            print(f"[MotorController] ❌ Arduino command failed: {e}")
            return False

    def _execute_movement_threaded(self, action: str, duration: float):
        """Execute movement in a separate thread with safety checks (NON-BLOCKING)"""
        def movement_worker():
            try:
                with self.movement_lock:
                    self.current_movement = action
                    self.stop_movement_event.clear()
                    self.movement_start_time = time.time()
                
                # Safety check: limit maximum duration
                safe_duration = min(duration, self.max_continuous_time)
                if duration > safe_duration:
                    print(f"[MotorController] ⚠️ Duration limited to {safe_duration}s for safety")
                
                print(f"[MotorController] 🚀 Starting {action} movement for {safe_duration}s")
                
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
                self.stop_movement_event.wait(timeout=safe_duration)
                
                # Stop the movement
                self._stop_all_motors()
                
                with self.movement_lock:
                    self.current_movement = None
                    self.movement_start_time = None
                
                print(f"[MotorController] ✅ {action} movement completed")
                
            except Exception as e:
                print(f"[MotorController] ❌ Movement thread error: {e}")
                self._stop_all_motors()
                with self.movement_lock:
                    self.current_movement = None
                    self.movement_start_time = None
        
        # Stop any existing movement
        self.stop()
        
        # Start new movement thread
        self.movement_thread = threading.Thread(target=movement_worker, daemon=True)
        self.movement_thread.start()

    def _start_forward_movement(self):
        """Start calibrated forward movement (internal method)"""
        if self.arduino_serial:
            # Use original Arduino command format (without speed parameters for now)
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
        """Start calibrated backward movement (internal method)"""
        if self.arduino_serial:
            # Use original Arduino command format (without speed parameters for now)
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
        """Start calibrated left turn movement (internal method)"""
        if self.arduino_serial:
            # Left side motors backward, right side motors forward
            self._send_arduino_command("MOTOR_A_BACKWARD")  # Front left
            self._send_arduino_command("MOTOR_B_FORWARD")   # Front right
            self._send_arduino_command("MOTOR_C_BACKWARD")  # Back left
            self._send_arduino_command("MOTOR_D_FORWARD")   # Back right
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)

    def _start_right_movement(self):
        """Start calibrated right turn movement (internal method)"""
        if self.arduino_serial:
            # Left side motors forward, right side motors backward
            self._send_arduino_command("MOTOR_A_FORWARD")   # Front left
            self._send_arduino_command("MOTOR_B_BACKWARD")  # Front right
            self._send_arduino_command("MOTOR_C_FORWARD")   # Back left
            self._send_arduino_command("MOTOR_D_BACKWARD")  # Back right
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

    # MOTOR CALIBRATION METHODS
    def calibrate_motor_speeds(self, front_left=None, front_right=None, back_left=None, back_right=None):
        """
        Calibrate individual motor speeds to fix circular movement
        
        Args:
            front_left: Speed for front left motor (0-255)
            front_right: Speed for front right motor (0-255)
            back_left: Speed for back left motor (0-255)
            back_right: Speed for back right motor (0-255)
        """
        if front_left is not None:
            self.motor_speeds['A'] = max(0, min(255, front_left))
        if front_right is not None:
            self.motor_speeds['B'] = max(0, min(255, front_right))
        if back_left is not None:
            self.motor_speeds['C'] = max(0, min(255, back_left))
        if back_right is not None:
            self.motor_speeds['D'] = max(0, min(255, back_right))
        
        print(f"[MotorController] 🔧 Motor speeds calibrated:")
        print(f"  Front Left (A): {self.motor_speeds['A']}")
        print(f"  Front Right (B): {self.motor_speeds['B']}")
        print(f"  Back Left (C): {self.motor_speeds['C']}")
        print(f"  Back Right (D): {self.motor_speeds['D']}")

    def auto_calibrate_straight_movement(self):
        """
        Auto-calibration helper for straight movement
        Run this and observe if robot turns, then adjust speeds accordingly
        """
        print("[MotorController] 🎯 AUTO-CALIBRATION MODE")
        print("Watch the robot movement and note any turning:")
        print("- If robot turns RIGHT: decrease front_right and back_right speeds")
        print("- If robot turns LEFT: decrease front_left and back_left speeds")
        print()
        
        # Test forward movement
        print("Testing FORWARD movement (3 seconds)...")
        self.forward(3.0)
        time.sleep(4.0)
        
        print("Testing BACKWARD movement (3 seconds)...")
        self.backward(3.0)
        time.sleep(4.0)
        
        print("🔧 Current motor speeds:")
        print(f"  Front Left (A): {self.motor_speeds['A']}")
        print(f"  Front Right (B): {self.motor_speeds['B']}")
        print(f"  Back Left (C): {self.motor_speeds['C']}")
        print(f"  Back Right (D): {self.motor_speeds['D']}")
        print()
        print("Use calibrate_motor_speeds() to adjust based on observed movement")

    # PUBLIC NON-BLOCKING METHODS WITH SAFETY
    def forward(self, duration=None):
        """Move all motors forward with safety checks (NON-BLOCKING)"""
        if not self.enabled: 
            print("[MotorController] ⚠️ Motor controller not enabled")
            return
        duration = duration or self.default_duration
        self._execute_movement_threaded('forward', duration)

    def backward(self, duration=None):
        """Move all motors backward with safety checks (NON-BLOCKING)"""
        if not self.enabled: 
            print("[MotorController] ⚠️ Motor controller not enabled")
            return
        duration = duration or self.default_duration
        self._execute_movement_threaded('backward', duration)

    def left(self, duration=None):
        """Turn left with safety checks (NON-BLOCKING)"""
        if not self.enabled: 
            print("[MotorController] ⚠️ Motor controller not enabled")
            return
        duration = duration or self.default_duration
        self._execute_movement_threaded('left', duration)

    def right(self, duration=None):
        """Turn right with safety checks (NON-BLOCKING)"""
        if not self.enabled: 
            print("[MotorController] ⚠️ Motor controller not enabled")
            return
        duration = duration or self.default_duration
        self._execute_movement_threaded('right', duration)

    def stop(self):
        """Emergency stop all motors immediately"""
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
            self.movement_start_time = None
        
        print("[MotorController] 🛑 All motors stopped")

    def emergency_stop(self):
        """Emergency stop with immediate motor shutdown"""
        print("[MotorController] 🚨 EMERGENCY STOP ACTIVATED")
        self.stop()
        
        # Additional safety: send multiple stop commands
        if self.arduino_serial:
            for _ in range(3):
                self._send_arduino_command("STOP_ALL")
                time.sleep(0.1)

    def get_current_movement(self):
        """Get current movement status"""
        with self.movement_lock:
            return self.current_movement

    def is_moving(self):
        """Check if motors are currently moving"""
        return self.get_current_movement() is not None

    def get_movement_time(self):
        """Get how long current movement has been running"""
        with self.movement_lock:
            if self.movement_start_time:
                return time.time() - self.movement_start_time
            return 0

    # DIAGNOSTIC AND TESTING METHODS
    def test_individual_motors(self):
        """Test each motor individually to identify wiring issues"""
        if not self.enabled or not self.arduino_serial:
            print("[MotorController] ❌ Arduino not available for individual motor testing")
            return False
        
        print("[MotorController] 🧪 Testing individual motors...")
        motors = ['A', 'B', 'C', 'D']
        motor_names = ['Front Left', 'Front Right', 'Back Left', 'Back Right']
        
        for motor, name in zip(motors, motor_names):
            print(f"\n🔧 Testing Motor {motor} ({name}):")
            
            # Forward test
            print(f"  ➡️ Forward (1 second)")
            self._send_arduino_command(f"MOTOR_{motor}_FORWARD")
            time.sleep(1.0)
            self._send_arduino_command(f"MOTOR_{motor}_STOP")
            time.sleep(0.5)
            
            # Backward test
            print(f"  ⬅️ Backward (1 second)")
            self._send_arduino_command(f"MOTOR_{motor}_BACKWARD")
            time.sleep(1.0)
            self._send_arduino_command(f"MOTOR_{motor}_STOP")
            time.sleep(0.5)
            
            response = input(f"  ❓ Did Motor {motor} ({name}) work correctly? (y/n): ").lower()
            if response == 'n':
                print(f"  ❌ Issue detected with Motor {motor} - check wiring")
            else:
                print(f"  ✅ Motor {motor} working correctly")
        
        return True

    def test_movement_patterns(self):
        """Test all movement patterns with user feedback"""
        if not self.enabled:
            print("[MotorController] ❌ Motor controller not enabled")
            return False
        
        print("[MotorController] 🚀 Testing movement patterns...")
        
        movements = [
            ('forward', 'Forward movement'),
            ('backward', 'Backward movement'),
            ('left', 'Left turn'),
            ('right', 'Right turn')
        ]
        
        for action, description in movements:
            print(f"\n🎯 Testing {description} (2 seconds)...")
            input("Press Enter to start...")
            
            if action == 'forward':
                self.forward(2.0)
            elif action == 'backward':
                self.backward(2.0)
            elif action == 'left':
                self.left(2.0)
            elif action == 'right':
                self.right(2.0)
            
            time.sleep(3.0)  # Wait for movement to complete
            
            response = input(f"❓ Did {description} work correctly? (y/n): ").lower()
            if response == 'n':
                print(f"❌ Issue with {description}")
                if action in ['forward', 'backward']:
                    print("💡 Tip: Use calibrate_motor_speeds() to fix circular movement")
            else:
                print(f"✅ {description} working correctly")
        
        return True

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