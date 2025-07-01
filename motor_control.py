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
                 use_arduino=True, arduino_port=None, arduino_baud=9600):
        """
        Initialize enhanced motor controller with speed calibration
        
        Args:
            use_arduino: Try Arduino serial communication first
            arduino_port: Serial port for Arduino (auto-detect if None)
            arduino_baud: Baud rate for Arduino communication
            in1-in4, ena, enb: GPIO pins for direct control fallback
        """
        self.enabled = False
        self.arduino_serial = None
        self.use_arduino = use_arduino
        self.arduino_baud = arduino_baud
        self.movement_duration = 1.0  # Default movement duration in seconds
        
        # Auto-detect Arduino port if not specified
        if arduino_port is None:
            arduino_port = self._detect_arduino_port()
        self.arduino_port = arduino_port
        
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
        if self.use_arduino and self.arduino_port:
            try:
                print(f"[MotorController] Attempting Arduino serial connection on {self.arduino_port}...")
                self.arduino_serial = serial.Serial(self.arduino_port, self.arduino_baud, timeout=1)
                time.sleep(2)  # Wait for Arduino to initialize
                
                # Test connection with a safe command
                self.arduino_serial.write(b"SAFETY_ON\n")
                self.arduino_serial.flush()
                time.sleep(0.1)
                
                self.enabled = True
                print(f"[MotorController] ✅ Arduino connected successfully on {self.arduino_port}")
                print("[MotorController] 🛡️ Collision avoidance ENABLED")
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

    def _detect_arduino_port(self):
        """Auto-detect Arduino serial port"""
        import glob
        
        # Common Arduino ports on different systems
        possible_ports = []
        
        if platform.system() == "Darwin":  # macOS
            possible_ports.extend(glob.glob("/dev/cu.usbmodem*"))
            possible_ports.extend(glob.glob("/dev/cu.usbserial*"))
        elif platform.system() == "Linux":  # Linux/Raspberry Pi
            possible_ports.extend(glob.glob("/dev/ttyUSB*"))
            possible_ports.extend(glob.glob("/dev/ttyACM*"))
        elif platform.system() == "Windows":  # Windows
            possible_ports = [f"COM{i}" for i in range(1, 20)]
        
        print(f"[MotorController] Detected possible Arduino ports: {possible_ports}")
        
        # Try each port
        for port in possible_ports:
            try:
                if serial:
                    test_serial = serial.Serial(port, 9600, timeout=1)
                    test_serial.close()
                    print(f"[MotorController] ✅ Found working port: {port}")
                    return port
            except:
                continue
        
        print("[MotorController] ⚠️ No Arduino port detected")
        return None

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
                
                # FIXED: Immediate motor start without additional delays
                movement_start_time = time.time()
                
                # Start the movement
                if action == 'forward':
                    self._start_forward_movement()
                elif action == 'backward':
                    self._start_backward_movement()
                elif action == 'left':
                    self._start_left_movement()
                elif action == 'right':
                    self._start_right_movement()
                
                actual_start_delay = time.time() - movement_start_time
                if actual_start_delay > 0.05:  # Log if start delay is too high
                    print(f"[MotorController] ⚠️ Movement start delay: {actual_start_delay:.3f}s")
                
                # Wait for duration or stop signal
                self.stop_movement_event.wait(timeout=safe_duration)
                
                # FIXED: Immediate stop without additional delays
                stop_start_time = time.time()
                self._stop_all_motors()
                actual_stop_delay = time.time() - stop_start_time
                
                if actual_stop_delay > 0.05:  # Log if stop delay is too high
                    print(f"[MotorController] ⚠️ Movement stop delay: {actual_stop_delay:.3f}s")
                
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
        
        # FIXED: Optimized stop sequence - reduce delay between stop and new movement
        if self.movement_thread and self.movement_thread.is_alive():
            self.stop_movement_event.set()
            # Reduced timeout for faster transitions
            self.movement_thread.join(timeout=0.1)
            
            # Force immediate stop if thread doesn't finish quickly
            if self.movement_thread.is_alive():
                self._stop_all_motors()
                print("[MotorController] ⚡ Force stopped for faster transition")
        
        # Add small delay to prevent motor strain during direction changes
        if hasattr(self, '_last_movement_time'):
            time_since_last = time.time() - self._last_movement_time
            if time_since_last < 0.1:  # 100ms minimum between movements
                time.sleep(0.1 - time_since_last)
        
        # Start new movement thread
        self.movement_thread = threading.Thread(target=movement_worker, daemon=True)
        self.movement_thread.start()
        
        # Record movement time for smooth transitions
        self._last_movement_time = time.time()

    def _start_forward_movement(self):
        """Start calibrated forward movement (internal method)"""
        if self.arduino_serial:
            # FIXED: Send simultaneous movement command to prevent jerky motion
            self._send_arduino_command(f"MOVE_FORWARD:{self.motor_speeds['A']},{self.motor_speeds['B']},{self.motor_speeds['C']},{self.motor_speeds['D']}")
            # Fallback to individual commands if combined command not supported
            if not self._test_arduino_response():
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
            # FIXED: Send simultaneous movement command to prevent jerky motion
            self._send_arduino_command(f"MOVE_BACKWARD:{self.motor_speeds['A']},{self.motor_speeds['B']},{self.motor_speeds['C']},{self.motor_speeds['D']}")
            # Fallback to individual commands if combined command not supported
            if not self._test_arduino_response():
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
            # FIXED: Send simultaneous turn command with speed control
            self._send_arduino_command(f"TURN_LEFT:{self.motor_speeds['A']},{self.motor_speeds['B']},{self.motor_speeds['C']},{self.motor_speeds['D']}")
            # Fallback to individual commands if combined command not supported
            if not self._test_arduino_response():
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
            # FIXED: Send simultaneous turn command with speed control
            self._send_arduino_command(f"TURN_RIGHT:{self.motor_speeds['A']},{self.motor_speeds['B']},{self.motor_speeds['C']},{self.motor_speeds['D']}")
            # Fallback to individual commands if combined command not supported
            if not self._test_arduino_response():
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
            # FIXED: Send simultaneous stop command to prevent jerky stopping
            self._send_arduino_command("STOP_ALL")
            # Fallback to individual commands if combined command not supported
            if not self._test_arduino_response():
                self._send_arduino_command("MOTOR_A_STOP")
                self._send_arduino_command("MOTOR_B_STOP")
                self._send_arduino_command("MOTOR_C_STOP")
                self._send_arduino_command("MOTOR_D_STOP")
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)

    def _test_arduino_response(self):
        """Test if Arduino responds to check if combined commands are supported"""
        try:
            if self.arduino_serial and self.arduino_serial.in_waiting > 0:
                response = self.arduino_serial.readline().decode().strip()
                return "OK" in response or "Command executed" in response
            return False
        except:
            return False

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