#!/usr/bin/env python3
"""
Premium Face Tracking Servo Controller
Advanced face tracking system with Arduino servo control integration
Supports Sony IMX500 AI Camera and premium tracking features
"""

import cv2
import face_recognition
import numpy as np
import serial
import time
import os
import threading
import json
from typing import List, Tuple, Dict, Optional
from datetime import datetime

class PremiumFaceTracker:
    """Premium face tracking controller with servo integration"""
    
    def __init__(self, arduino_port: str = '/dev/ttyUSB0', camera_index: int = 0):
        # Camera setup with CameraHandler support
        self.camera_index = camera_index
        self.camera = None
        self.camera_handler = None
        self.using_imx500 = False
        
        # Arduino setup
        self.arduino_port = arduino_port
        self.arduino_baud = 9600
        self.arduino = None
        
        # Servo configuration
        self.servo1_center = 90  # Pan servo (horizontal)
        self.servo2_center = 90  # Tilt servo (vertical)
        self.servo1_current = self.servo1_center
        self.servo2_current = self.servo2_center
        self.servo_min = 0
        self.servo_max = 180
        self.movement_threshold = 5  # Minimum movement in pixels to trigger servo
        
        # Face tracking parameters
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        
        # Tracking state
        self.target_person = None
        self.tracking_active = True
        self.last_face_center = None
        self.smoothing_factor = 0.3  # For smooth servo movement
        
        # Performance tracking
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
        
        # Load known faces
        self.load_known_faces()
        
    def initialize_camera(self) -> bool:
        """Initialize camera with CameraHandler support (Sony IMX500 AI Camera)"""
        print("🎥 Initializing camera system...")
        
        # Try using the existing CameraHandler first (supports Sony IMX500 AI Camera)
        try:
            from camera_handler import CameraHandler
            print("  🤖 Attempting to use CameraHandler (Sony IMX500 AI support)...")
            
            # Initialize camera handler with IMX500 preference
            self.camera_handler = CameraHandler(camera_index=self.camera_index, prefer_imx500=True)
            
            if self.camera_handler.is_camera_available():
                self.using_imx500 = self.camera_handler.using_imx500
                camera_type = "Sony IMX500 AI" if self.using_imx500 else "USB"
                print(f"  ✅ {camera_type} camera initialized successfully")
                
                # Test frame capture
                ret, frame = self.camera_handler.read()
                if ret and frame is not None:
                    height, width = frame.shape[:2]
                    print(f"  📸 Camera working - Resolution: {width}x{height}")
                    
                    if self.using_imx500:
                        ai_status = self.camera_handler.get_ai_status()
                        print(f"  🤖 AI Status: {ai_status}")
                    
                    return True
                else:
                    print("  ❌ Camera initialized but can't capture frames")
                    self.camera_handler.release()
                    self.camera_handler = None
            else:
                print("  ❌ CameraHandler reports camera not available")
                self.camera_handler = None
                
        except Exception as e:
            print(f"  ❌ CameraHandler error: {e}")
            self.camera_handler = None
            
        # Fallback to basic OpenCV
        print("  🔄 Falling back to basic OpenCV camera...")
        self.camera = cv2.VideoCapture(self.camera_index)
        
        if not self.camera.isOpened():
            print(f"  ❌ Failed to open camera {self.camera_index}")
            return False
            
        # Set camera properties for better performance
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        
        # Test frame capture
        ret, frame = self.camera.read()
        if not ret:
            print("  ❌ Basic camera can't capture frames")
            return False
            
        height, width = frame.shape[:2]
        print(f"  ✅ Basic camera working - Resolution: {width}x{height}")
        return True
        
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read frame from camera using appropriate handler"""
        if self.camera_handler:
            return self.camera_handler.read()
        elif self.camera:
            return self.camera.read()
        else:
            return False, None
            
    def release_camera(self):
        """Release camera resources"""
        if self.camera_handler:
            self.camera_handler.release()
            self.camera_handler = None
        if self.camera:
            self.camera.release()
            self.camera = None
            
    def initialize_arduino(self) -> bool:
        """Initialize Arduino connection"""
        print(f"🔌 Connecting to Arduino on {self.arduino_port}...")
        
        try:
            self.arduino = serial.Serial(self.arduino_port, self.arduino_baud, timeout=2)
            time.sleep(2)  # Wait for Arduino initialization
            
            # Test connection with center position
            self.move_servos(self.servo1_center, self.servo2_center)
            print("  ✅ Arduino connected and servos centered")
            return True
            
        except Exception as e:
            print(f"  ❌ Arduino connection failed: {e}")
            return False
            
    def load_known_faces(self):
        """Load known face encodings from people directory"""
        print("👤 Loading known faces...")
        
        people_dir = "people"
        if not os.path.exists(people_dir):
            print("  ⚠️ No 'people' directory found - will track any face")
            return
            
        for person_name in os.listdir(people_dir):
            person_path = os.path.join(people_dir, person_name)
            if not os.path.isdir(person_path):
                continue
                
            person_encodings = []
            image_files = [f for f in os.listdir(person_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            for image_file in image_files:
                try:
                    image_path = os.path.join(person_path, image_file)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        person_encodings.extend(encodings)
                        
                except Exception as e:
                    print(f"    ⚠️ Error loading {image_file}: {e}")
                    
            if person_encodings:
                # Use the first encoding as representative
                self.known_face_encodings.append(person_encodings[0])
                self.known_face_names.append(person_name)
                print(f"  ✅ Loaded {len(person_encodings)} encodings for {person_name}")
                
        if self.known_face_encodings:
            print(f"  🎯 Ready to track: {', '.join(self.known_face_names)}")
        else:
            print("  ℹ️ No known faces loaded - will track any detected face")
            
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in frame using OpenCV cascade"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Convert to (top, right, bottom, left) format for face_recognition compatibility
        face_locations = []
        for (x, y, w, h) in faces:
            face_locations.append((y, x + w, y + h, x))
            
        return face_locations
        
    def recognize_faces(self, frame: np.ndarray, face_locations: List[Tuple[int, int, int, int]]) -> List[str]:
        """Recognize faces using face_recognition library"""
        if not self.known_face_encodings:
            return ["Unknown"] * len(face_locations)
            
        # Get face encodings for detected faces
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            # Use the known face with the smallest distance
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                name = self.known_face_names[best_match_index]
                
            face_names.append(name)
            
        return face_names
        
    def get_face_center(self, face_location: Tuple[int, int, int, int]) -> Tuple[int, int]:
        """Get center point of face bounding box"""
        top, right, bottom, left = face_location
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        return center_x, center_y
        
    def calculate_servo_positions(self, face_center: Tuple[int, int], frame_shape: Tuple[int, int]) -> Tuple[int, int]:
        """Calculate servo positions based on face center"""
        frame_height, frame_width = frame_shape[:2]
        face_x, face_y = face_center
        
        # Calculate position relative to frame center
        center_x = frame_width // 2
        center_y = frame_height // 2
        
        offset_x = face_x - center_x
        offset_y = face_y - center_y
        
        # Convert to servo angles (with smoothing)
        # Pan servo (horizontal movement)
        pan_adjustment = int(offset_x * 0.1)  # Adjust sensitivity
        new_servo1 = self.servo1_current - pan_adjustment
        
        # Tilt servo (vertical movement) 
        tilt_adjustment = int(offset_y * 0.1)  # Adjust sensitivity
        new_servo2 = self.servo2_current + tilt_adjustment
        
        # Apply smoothing
        if self.last_face_center:
            last_x, last_y = self.last_face_center
            smooth_x = int(face_x * self.smoothing_factor + last_x * (1 - self.smoothing_factor))
            smooth_y = int(face_y * self.smoothing_factor + last_y * (1 - self.smoothing_factor))
            
            # Recalculate with smoothed values
            offset_x = smooth_x - center_x
            offset_y = smooth_y - center_y
            
            pan_adjustment = int(offset_x * 0.1)
            tilt_adjustment = int(offset_y * 0.1)
            
            new_servo1 = self.servo1_current - pan_adjustment
            new_servo2 = self.servo2_current + tilt_adjustment
        
        # Constrain to servo limits
        new_servo1 = max(self.servo_min, min(self.servo_max, new_servo1))
        new_servo2 = max(self.servo_min, min(self.servo_max, new_servo2))
        
        return new_servo1, new_servo2
        
    def move_servos(self, servo1_pos: int, servo2_pos: int):
        """Move servos to specified positions"""
        if not self.arduino:
            return
            
        try:
            # Send servo commands
            self.arduino.write(f"SERVO_{servo1_pos}\n".encode())
            self.arduino.flush()
            time.sleep(0.01)
            
            self.arduino.write(f"SERVO2_{servo2_pos}\n".encode())
            self.arduino.flush()
            
            # Update current positions
            self.servo1_current = servo1_pos
            self.servo2_current = servo2_pos
            
        except Exception as e:
            print(f"Servo movement error: {e}")
            
    def should_move_servos(self, face_center: Tuple[int, int], frame_shape: Tuple[int, int]) -> bool:
        """Determine if servos should move based on face position"""
        frame_height, frame_width = frame_shape[:2]
        face_x, face_y = face_center
        
        center_x = frame_width // 2
        center_y = frame_height // 2
        
        distance = np.sqrt((face_x - center_x)**2 + (face_y - center_y)**2)
        return distance > self.movement_threshold
        
    def draw_tracking_info(self, frame: np.ndarray, face_locations: List, face_names: List[str]) -> np.ndarray:
        """Draw tracking information on frame"""
        # Draw face rectangles and names
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw rectangle around face
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw name label
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
            
            # Draw center point
            center_x, center_y = self.get_face_center((top, right, bottom, left))
            cv2.circle(frame, (center_x, center_y), 5, color, -1)
            
        # Draw frame center crosshair
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (255, 255, 255), 2)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (255, 255, 255), 2)
        
        # Draw servo positions
        servo_text = f"Servos: Pan={self.servo1_current}° Tilt={self.servo2_current}°"
        cv2.putText(frame, servo_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw FPS
        fps_text = f"FPS: {self.fps:.1f}"
        cv2.putText(frame, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw camera type
        camera_type = "Sony IMX500 AI" if self.using_imx500 else "USB Camera"
        cv2.putText(frame, camera_type, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Draw tracking status
        status_text = "TRACKING ACTIVE" if self.tracking_active else "TRACKING PAUSED"
        status_color = (0, 255, 0) if self.tracking_active else (0, 0, 255)
        cv2.putText(frame, status_text, (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        return frame
        
    def update_fps(self):
        """Update FPS calculation"""
        self.frame_count += 1
        current_time = time.time()
        
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.frame_count / (current_time - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = current_time
            
    def run_tracking(self):
        """Main tracking loop"""
        print("\n🎯 Starting Premium Face Tracking System")
        print("=" * 50)
        print("Controls:")
        print("  SPACE - Toggle tracking on/off")
        print("  R - Reset servos to center")
        print("  Q - Quit")
        print("  1-9 - Set target person (if multiple faces)")
        print("=" * 50)
        
        while True:
            # Read frame
            ret, frame = self.read_frame()
            if not ret:
                print("Failed to read frame")
                break
                
            # Update FPS
            self.update_fps()
            
            # Process frame for face detection
            if self.process_this_frame:
                # Detect faces
                face_locations = self.detect_faces(frame)
                
                # Recognize faces if we have known encodings
                if face_locations:
                    face_names = self.recognize_faces(frame, face_locations)
                else:
                    face_names = []
                    
                # Store results
                self.face_locations = face_locations
                self.face_names = face_names
                
            # Alternate frame processing for performance
            self.process_this_frame = not self.process_this_frame
            
            # Track faces and move servos
            if self.tracking_active and self.face_locations:
                # Choose target face (prefer known faces)
                target_face_idx = 0
                if self.target_person:
                    # Look for specific target person
                    for i, name in enumerate(self.face_names):
                        if name == self.target_person:
                            target_face_idx = i
                            break
                else:
                    # Prefer known faces over unknown
                    for i, name in enumerate(self.face_names):
                        if name != "Unknown":
                            target_face_idx = i
                            break
                            
                if target_face_idx < len(self.face_locations):
                    face_location = self.face_locations[target_face_idx]
                    face_center = self.get_face_center(face_location)
                    
                    # Move servos if face is not centered
                    if self.should_move_servos(face_center, frame.shape):
                        servo1_pos, servo2_pos = self.calculate_servo_positions(face_center, frame.shape)
                        self.move_servos(servo1_pos, servo2_pos)
                        
                    self.last_face_center = face_center
                    
            # Draw tracking information
            display_frame = self.draw_tracking_info(frame, self.face_locations, self.face_names)
            
            # Display frame
            cv2.imshow('Premium Face Tracking', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord(' '):
                self.tracking_active = not self.tracking_active
                status = "ACTIVE" if self.tracking_active else "PAUSED"
                print(f"🎯 Tracking {status}")
            elif key == ord('r'):
                self.move_servos(self.servo1_center, self.servo2_center)
                print("🔄 Servos reset to center")
            elif key >= ord('1') and key <= ord('9'):
                person_idx = key - ord('1')
                if person_idx < len(self.known_face_names):
                    self.target_person = self.known_face_names[person_idx]
                    print(f"🎯 Targeting: {self.target_person}")
                else:
                    self.target_person = None
                    print("🎯 Targeting: Any face")
                    
        # Cleanup
        self.cleanup()
        
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up...")
        
        # Center servos before exit
        if self.arduino:
            self.move_servos(self.servo1_center, self.servo2_center)
            time.sleep(1)
            self.arduino.close()
            
        # Release camera
        self.release_camera()
        cv2.destroyAllWindows()
        
        print("✅ Cleanup complete")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Premium Face Tracking Servo Controller')
    parser.add_argument('--arduino-port', default='/dev/ttyUSB0', 
                       help='Arduino serial port (default: /dev/ttyUSB0)')
    parser.add_argument('--camera-index', type=int, default=0,
                       help='Camera index (default: 0)')
    
    args = parser.parse_args()
    
    # Create face tracker
    tracker = PremiumFaceTracker(
        arduino_port=args.arduino_port,
        camera_index=args.camera_index
    )
    
    # Initialize systems
    if not tracker.initialize_camera():
        print("❌ Failed to initialize camera")
        return
        
    if not tracker.initialize_arduino():
        print("❌ Failed to initialize Arduino")
        return
        
    # Start tracking
    try:
        tracker.run_tracking()
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
        tracker.cleanup()

if __name__ == "__main__":
    main()