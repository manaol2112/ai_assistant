#!/usr/bin/env python3
"""
Face Tracking Servo Controller for AI Assistant Robot
Premium face tracking system that automatically controls servo motors to follow Sophia and Eladriel's faces.

Features:
- Real-time face detection and recognition
- Smooth servo movement calculations
- Arduino serial communication
- Person-specific tracking for Sophia and Eladriel
- Adaptive tracking with smoothing algorithms
- Premium UI feedback and logging
"""

import cv2
import face_recognition
import numpy as np
import serial
import time
import threading
import os
import logging
from typing import Dict, List, Tuple, Optional
import queue
from dataclasses import dataclass
from collections import deque
import math

@dataclass
class FaceData:
    """Data structure for face detection results"""
    name: str
    location: Tuple[int, int, int, int]  # top, right, bottom, left
    center: Tuple[int, int]
    confidence: float
    distance: float

@dataclass
class ServoCommand:
    """Data structure for servo commands"""
    servo1_angle: int  # Left/Right servo (0-180)
    servo2_angle: int  # Up/Down servo (0-180)
    timestamp: float

class FaceTrackingServoController:
    """
    Premium Face Tracking Servo Controller
    Automatically tracks and follows Sophia and Eladriel's faces using servo motors
    """
    
    def __init__(self, 
                 arduino_port='/dev/ttyUSB0', 
                 arduino_baud=9600,
                 camera_index=0,
                 servo1_center=90,  # Center position for left/right servo
                 servo2_center=90,  # Center position for up/down servo
                 tracking_smoothness=0.3,  # Lower = smoother, slower response
                 min_face_size=50,  # Minimum face size to track
                 face_confidence_threshold=0.6):
        
        # Arduino Communication Setup
        self.arduino_port = arduino_port
        self.arduino_baud = arduino_baud
        self.arduino_serial = None
        self.arduino_connected = False
        
        # Camera Setup
        self.camera_index = camera_index
        self.camera = None
        self.camera_width = 640
        self.camera_height = 480
        
        # Servo Configuration
        self.servo1_center = servo1_center
        self.servo2_center = servo2_center
        self.servo1_current = servo1_center
        self.servo2_current = servo2_center
        self.servo1_range = (0, 180)  # Full range for left/right
        self.servo2_range = (30, 150)  # Limited range for up/down to prevent mechanical issues
        
        # Tracking Parameters
        self.tracking_smoothness = tracking_smoothness
        self.min_face_size = min_face_size
        self.face_confidence_threshold = face_confidence_threshold
        
        # Face Recognition Setup
        self.known_face_encodings = []
        self.known_face_names = []
        self.target_people = ['sophia', 'eladriel']
        
        # Tracking State
        self.is_tracking = False
        self.tracking_thread = None
        self.command_queue = queue.Queue()
        self.current_target = None
        self.last_face_time = 0
        self.face_lost_timeout = 2.0  # Seconds before returning to center
        
        # Smoothing buffers for stable tracking
        self.position_buffer = deque(maxlen=5)
        self.servo_command_buffer = deque(maxlen=3)
        
        # Logging setup
        self.setup_logging()
        
        # Initialize components
        self.initialize_arduino()
        self.initialize_camera()
        self.load_face_encodings()
        
    def setup_logging(self):
        """Setup premium logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('face_tracking.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('FaceTracker')
        
    def initialize_arduino(self):
        """Initialize Arduino serial communication"""
        try:
            self.logger.info(f"🔌 Connecting to Arduino on {self.arduino_port}...")
            self.arduino_serial = serial.Serial(self.arduino_port, self.arduino_baud, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            
            # Test connection with center position
            self.send_servo_command(self.servo1_center, self.servo2_center)
            self.arduino_connected = True
            self.logger.info("✅ Arduino connected successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Arduino connection failed: {e}")
            self.arduino_connected = False
            
    def initialize_camera(self):
        """Initialize camera for face detection"""
        try:
            self.logger.info(f"📸 Initializing camera {self.camera_index}...")
            self.camera = cv2.VideoCapture(self.camera_index)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            # Test camera
            ret, frame = self.camera.read()
            if ret:
                self.logger.info("✅ Camera initialized successfully!")
            else:
                raise Exception("Camera test failed")
                
        except Exception as e:
            self.logger.error(f"❌ Camera initialization failed: {e}")
            self.camera = None
            
    def load_face_encodings(self):
        """Load face encodings for Sophia and Eladriel"""
        self.logger.info("🔍 Loading face encodings...")
        
        for person_name in self.target_people:
            person_dir = f"people/{person_name}"
            if not os.path.exists(person_dir):
                self.logger.warning(f"⚠️ No face data found for {person_name}")
                continue
                
            person_encodings = []
            for filename in os.listdir(person_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(person_dir, filename)
                    try:
                        # Load and encode face
                        image = face_recognition.load_image_file(image_path)
                        encodings = face_recognition.face_encodings(image)
                        
                        if encodings:
                            person_encodings.append(encodings[0])
                            self.logger.info(f"📸 Loaded encoding from {filename}")
                        else:
                            self.logger.warning(f"⚠️ No faces found in {filename}")
                            
                    except Exception as e:
                        self.logger.error(f"❌ Error loading {filename}: {e}")
            
            if person_encodings:
                self.known_face_encodings.extend(person_encodings)
                self.known_face_names.extend([person_name] * len(person_encodings))
                self.logger.info(f"✅ Loaded {len(person_encodings)} encodings for {person_name}")
            else:
                self.logger.warning(f"⚠️ No valid encodings found for {person_name}")
                
        self.logger.info(f"🎯 Total encodings loaded: {len(self.known_face_encodings)}")
        
    def send_servo_command(self, servo1_angle: int, servo2_angle: int):
        """Send servo position commands to Arduino"""
        if not self.arduino_connected or not self.arduino_serial:
            return False
            
        try:
            # Clamp angles to valid ranges
            servo1_angle = max(self.servo1_range[0], min(self.servo1_range[1], servo1_angle))
            servo2_angle = max(self.servo2_range[0], min(self.servo2_range[1], servo2_angle))
            
            # Send commands to Arduino
            servo1_cmd = f"SERVO_{servo1_angle}"
            servo2_cmd = f"SERVO2_{servo2_angle}"
            
            self.arduino_serial.write(f"{servo1_cmd}\n".encode())
            self.arduino_serial.flush()
            time.sleep(0.05)  # Small delay between commands
            
            self.arduino_serial.write(f"{servo2_cmd}\n".encode())
            self.arduino_serial.flush()
            
            self.servo1_current = servo1_angle
            self.servo2_current = servo2_angle
            
            self.logger.debug(f"🎯 Servos moved to: ({servo1_angle}, {servo2_angle})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Servo command failed: {e}")
            return False
            
    def calculate_servo_angles(self, face_center: Tuple[int, int]) -> Tuple[int, int]:
        """Calculate servo angles based on face position in frame"""
        face_x, face_y = face_center
        
        # Calculate relative position from center (range: -1 to 1)
        center_x = self.camera_width // 2
        center_y = self.camera_height // 2
        
        rel_x = (face_x - center_x) / (self.camera_width / 2)
        rel_y = (face_y - center_y) / (self.camera_height / 2)
        
        # Calculate servo angles with proper mapping
        # Servo1 (left/right): Inverted so robot looks toward face
        servo1_angle = int(self.servo1_center - (rel_x * 45))  # ±45 degrees from center
        
        # Servo2 (up/down): Normal mapping
        servo2_angle = int(self.servo2_center + (rel_y * 30))  # ±30 degrees from center
        
        return servo1_angle, servo2_angle
        
    def smooth_servo_movement(self, target_servo1: int, target_servo2: int) -> Tuple[int, int]:
        """Apply smoothing algorithm to servo movements"""
        # Linear interpolation for smooth movement
        smooth_servo1 = int(self.servo1_current + 
                           (target_servo1 - self.servo1_current) * self.tracking_smoothness)
        smooth_servo2 = int(self.servo2_current + 
                           (target_servo2 - self.servo2_current) * self.tracking_smoothness)
        
        return smooth_servo1, smooth_servo2
        
    def detect_faces(self, frame) -> List[FaceData]:
        """Detect and recognize faces in frame"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if not face_locations:
            return []
            
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        detected_faces = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Scale back up face locations
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Check face size
            face_width = right - left
            face_height = bottom - top
            if face_width < self.min_face_size or face_height < self.min_face_size:
                continue
                
            # Recognize face
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding, 
                tolerance=self.face_confidence_threshold
            )
            
            name = "unknown"
            confidence = 0.0
            
            if True in matches:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = 1.0 - face_distances[best_match_index]
            
            # Only track target people
            if name in self.target_people:
                face_center = ((left + right) // 2, (top + bottom) // 2)
                detected_faces.append(FaceData(
                    name=name,
                    location=(top, right, bottom, left),
                    center=face_center,
                    confidence=confidence,
                    distance=face_distances[best_match_index] if 'face_distances' in locals() else 1.0
                ))
                
        return detected_faces
        
    def select_target_face(self, faces: List[FaceData]) -> Optional[FaceData]:
        """Select the best face to track"""
        if not faces:
            return None
            
        # Priority: Highest confidence, then largest face, then closest to current target
        faces.sort(key=lambda f: (f.confidence, -f.distance), reverse=True)
        return faces[0]
        
    def return_to_center(self):
        """Return servos to center position when no face is detected"""
        self.logger.info("🎯 No face detected, returning to center...")
        target_servo1, target_servo2 = self.servo1_center, self.servo2_center
        smooth_servo1, smooth_servo2 = self.smooth_servo_movement(target_servo1, target_servo2)
        self.send_servo_command(smooth_servo1, smooth_servo2)
        
    def tracking_loop(self):
        """Main tracking loop"""
        self.logger.info("🚀 Face tracking started!")
        
        while self.is_tracking and self.camera:
            try:
                ret, frame = self.camera.read()
                if not ret:
                    continue
                    
                # Detect faces
                faces = self.detect_faces(frame)
                current_time = time.time()
                
                if faces:
                    # Select target face
                    target_face = self.select_target_face(faces)
                    
                    if target_face:
                        self.current_target = target_face.name
                        self.last_face_time = current_time
                        
                        # Calculate servo angles
                        target_servo1, target_servo2 = self.calculate_servo_angles(target_face.center)
                        
                        # Apply smoothing
                        smooth_servo1, smooth_servo2 = self.smooth_servo_movement(
                            target_servo1, target_servo2
                        )
                        
                        # Send command
                        self.send_servo_command(smooth_servo1, smooth_servo2)
                        
                        self.logger.info(f"👁️ Tracking {target_face.name} at {target_face.center} "
                                       f"-> Servos: ({smooth_servo1}, {smooth_servo2})")
                        
                elif current_time - self.last_face_time > self.face_lost_timeout:
                    # No face detected for too long, return to center
                    if self.current_target:
                        self.return_to_center()
                        self.current_target = None
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"❌ Tracking loop error: {e}")
                time.sleep(0.5)
                
        self.logger.info("🛑 Face tracking stopped")
        
    def start_tracking(self):
        """Start face tracking"""
        if self.is_tracking:
            self.logger.warning("⚠️ Face tracking is already running")
            return
            
        if not self.arduino_connected:
            self.logger.error("❌ Cannot start tracking: Arduino not connected")
            return
            
        if not self.camera:
            self.logger.error("❌ Cannot start tracking: Camera not available")
            return
            
        if not self.known_face_encodings:
            self.logger.error("❌ Cannot start tracking: No face encodings loaded")
            return
            
        self.is_tracking = True
        self.tracking_thread = threading.Thread(target=self.tracking_loop, daemon=True)
        self.tracking_thread.start()
        
        # Return to center position first
        self.send_servo_command(self.servo1_center, self.servo2_center)
        self.logger.info("✅ Face tracking started successfully!")
        
    def stop_tracking(self):
        """Stop face tracking"""
        if not self.is_tracking:
            return
            
        self.is_tracking = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=2.0)
            
        # Return to center position
        self.send_servo_command(self.servo1_center, self.servo2_center)
        self.logger.info("🛑 Face tracking stopped")
        
    def manual_servo_control(self, servo1_angle: int, servo2_angle: int):
        """Manual servo control for testing"""
        self.logger.info(f"🎮 Manual servo control: ({servo1_angle}, {servo2_angle})")
        self.send_servo_command(servo1_angle, servo2_angle)
        
    def get_status(self) -> Dict:
        """Get current status of the tracking system"""
        return {
            'arduino_connected': self.arduino_connected,
            'camera_available': self.camera is not None,
            'face_encodings_loaded': len(self.known_face_encodings),
            'is_tracking': self.is_tracking,
            'current_target': self.current_target,
            'servo1_position': self.servo1_current,
            'servo2_position': self.servo2_current,
            'target_people': self.target_people
        }
        
    def cleanup(self):
        """Cleanup resources"""
        self.stop_tracking()
        
        if self.camera:
            self.camera.release()
            
        if self.arduino_serial:
            # Return to center before closing
            self.send_servo_command(self.servo1_center, self.servo2_center)
            time.sleep(0.5)
            self.arduino_serial.close()
            
        self.logger.info("🧹 Cleanup completed")

def main():
    """Demo function for testing the face tracking system"""
    print("🤖 AI Assistant Face Tracking Servo Controller")
    print("=" * 50)
    
    # Initialize controller
    controller = FaceTrackingServoController()
    
    try:
        # Show status
        status = controller.get_status()
        print(f"📊 System Status:")
        for key, value in status.items():
            print(f"  • {key}: {value}")
        
        if not status['arduino_connected']:
            print("❌ Arduino not connected. Please check connection.")
            return
            
        if not status['camera_available']:
            print("❌ Camera not available. Please check camera.")
            return
            
        if status['face_encodings_loaded'] == 0:
            print("❌ No face encodings loaded. Please add faces to people/ folder.")
            return
        
        print("\n🎯 Starting face tracking...")
        print("Press 'q' to quit, 's' to stop tracking, 'r' to restart tracking")
        print("Press 'c' to center servos, 't' to test manual control")
        
        controller.start_tracking()
        
        # Interactive control loop
        while True:
            try:
                command = input("\nCommand (q/quit, s/stop, r/restart, c/center, t/test): ").strip().lower()
                
                if command in ['q', 'quit']:
                    break
                elif command in ['s', 'stop']:
                    controller.stop_tracking()
                    print("🛑 Tracking stopped")
                elif command in ['r', 'restart']:
                    controller.start_tracking()
                    print("🚀 Tracking restarted")
                elif command in ['c', 'center']:
                    controller.manual_servo_control(90, 90)
                    print("🎯 Servos centered")
                elif command in ['t', 'test']:
                    print("🎮 Manual control test...")
                    for angle in [45, 135, 90]:
                        controller.manual_servo_control(angle, 90)
                        time.sleep(1)
                    print("✅ Manual control test complete")
                else:
                    print("❓ Unknown command")
                    
            except KeyboardInterrupt:
                break
                
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        controller.cleanup()
        print("👋 Face tracking system shutdown complete")

if __name__ == "__main__":
    main() 