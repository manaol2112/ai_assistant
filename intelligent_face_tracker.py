#!/usr/bin/env python3
"""
Intelligent Face Tracking System for AI Assistant
Enhanced tracking with priority recognition for Sophia and Eladriel
Automatic tracking during conversation mode with intelligent search behavior

Features:
- Priority tracking: Sophia and Eladriel get highest priority
- Automatic tracking during conversation mode
- Intelligent search: looks left/right/up when no faces detected
- Smooth servo movements with predictive tracking
- Integration with existing face detection and motor systems
"""

import cv2
import numpy as np
import time
import threading
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math

# Import existing components
from face_tracking_servo_controller import PremiumFaceTracker
from smart_camera_detector import SmartCameraDetector

class TrackingPriority(Enum):
    """Priority levels for face tracking"""
    HIGHEST = 1  # Sophia and Eladriel
    HIGH = 2     # Known faces
    MEDIUM = 3   # Unknown faces
    SEARCH = 4   # No faces - search mode

@dataclass
class TrackedFace:
    """Data structure for tracked face information"""
    name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # (left, top, right, bottom)
    center: Tuple[int, int]
    priority: TrackingPriority
    last_seen: float
    prediction: Optional[Tuple[int, int]] = None

class SearchPattern(Enum):
    """Search patterns when no faces are detected"""
    SWEEP_LEFT_RIGHT = "sweep_lr"
    LOOK_UP = "look_up"
    CENTER_PAUSE = "center_pause"

class IntelligentFaceTracker:
    """Enhanced face tracking with priority recognition and intelligent search"""
    
    def __init__(self, arduino_port: str = '/dev/ttyUSB0', camera_index: int = 0):
        # Initialize logger
        self.logger = logging.getLogger('IntelligentFaceTracker')
        
        # Priority users (Sophia and Eladriel get highest priority)
        self.priority_users = {'sophia', 'eladriel'}
        
        # Tracking state
        self.is_tracking = False
        self.conversation_mode = False
        self.current_target = None
        self.tracked_faces = {}
        self.last_detection_time = 0
        
        # Search behavior state
        self.search_active = False
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_start_time = 0
        self.search_direction = 1  # 1 for right, -1 for left
        self.search_position = 90  # Current search position
        
        # Servo control parameters
        self.pan_center = 90
        self.tilt_center = 90
        self.pan_current = self.pan_center
        self.tilt_current = self.tilt_center
        self.servo_min = 20
        self.servo_max = 160
        self.search_step = 2  # Degrees per search step
        self.tracking_smoothing = 0.7  # Smoothing factor for tracking
        
        # Detection parameters
        self.face_lost_timeout = 3.0  # Seconds before starting search
        self.search_timeout = 10.0    # Seconds to search before returning to center
        self.priority_boost_range = 50  # Pixels to boost priority user detection
        
        # Initialize existing components
        self.face_tracker = PremiumFaceTracker(arduino_port, camera_index)
        self.camera_detector = None
        
        # Threading
        self.tracking_thread = None
        self.running = False
        self.lock = threading.Lock()
        
    def initialize(self) -> bool:
        """Initialize the intelligent tracking system"""
        try:
            self.logger.info("🎯 Initializing Intelligent Face Tracker...")
            
            # Initialize face tracker (servos and camera)
            camera_ok = self.face_tracker.initialize_camera()
            arduino_ok = self.face_tracker.initialize_arduino()
            
            if not arduino_ok:
                self.logger.error("❌ Arduino connection failed")
                return False
                
            if not camera_ok:
                self.logger.error("❌ Camera initialization failed")
                return False
            
            # Initialize smart camera detector for enhanced face recognition
            self.camera_detector = SmartCameraDetector()
            if hasattr(self.face_tracker, 'camera_handler'):
                self.camera_detector.shared_camera = self.face_tracker.camera_handler
            
            # Center servos
            self.face_tracker.move_servos(self.pan_center, self.tilt_center)
            time.sleep(1)
            
            self.logger.info("✅ Intelligent Face Tracker initialized successfully!")
            self.logger.info(f"🎯 Priority users: {', '.join(self.priority_users)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {e}")
            return False
    
    def start_tracking(self, conversation_mode: bool = False):
        """Start intelligent face tracking"""
        with self.lock:
            if self.is_tracking:
                self.logger.warning("⚠️ Tracking already active")
                return
                
            self.is_tracking = True
            self.conversation_mode = conversation_mode
            self.running = True
            
            # Start tracking thread
            self.tracking_thread = threading.Thread(
                target=self._tracking_loop,
                daemon=True,
                name="IntelligentFaceTracker"
            )
            self.tracking_thread.start()
            
            mode_info = "conversation mode" if conversation_mode else "general mode"
            self.logger.info(f"🎯 Intelligent face tracking started in {mode_info}")
    
    def stop_tracking(self):
        """Stop face tracking and return to center"""
        with self.lock:
            self.is_tracking = False
            self.running = False
            self.search_active = False
            
        if self.tracking_thread and self.tracking_thread.is_alive():
            self.tracking_thread.join(timeout=2)
            
        # Return to center position
        self.face_tracker.move_servos(self.pan_center, self.tilt_center)
        self.pan_current = self.pan_center
        self.tilt_current = self.tilt_center
        
        self.logger.info("🛑 Intelligent face tracking stopped")
    
    def set_conversation_mode(self, active: bool, target_user: str = None):
        """Enable/disable conversation mode tracking"""
        with self.lock:
            self.conversation_mode = active
            if active and target_user:
                self.current_target = target_user.lower()
                self.logger.info(f"💬 Conversation mode active - prioritizing {target_user}")
            else:
                self.current_target = None
                self.logger.info("💬 Conversation mode disabled")
    
    def _tracking_loop(self):
        """Main tracking loop with intelligent behavior"""
        self.logger.info("🔄 Intelligent tracking loop started")
        
        while self.running:
            try:
                # Capture frame
                ret, frame = self.face_tracker.read_frame()
                if not ret or frame is None:
                    time.sleep(0.1)
                    continue
                
                # Detect faces using smart camera detector
                detected_faces = self._detect_and_prioritize_faces(frame)
                current_time = time.time()
                
                if detected_faces:
                    # Faces detected - track the highest priority face
                    self.last_detection_time = current_time
                    self.search_active = False
                    
                    target_face = self._select_target_face(detected_faces)
                    if target_face:
                        self._track_face(target_face, frame.shape)
                        
                else:
                    # No faces detected - start intelligent search
                    time_since_last_detection = current_time - self.last_detection_time
                    
                    if time_since_last_detection > self.face_lost_timeout:
                        if not self.search_active:
                            self._start_search_behavior()
                        else:
                            self._continue_search_behavior()
                
                time.sleep(0.05)  # 20 FPS tracking loop
                
            except Exception as e:
                self.logger.error(f"❌ Error in tracking loop: {e}")
                time.sleep(1)
        
        self.logger.info("🔄 Intelligent tracking loop ended")
    
    def _detect_and_prioritize_faces(self, frame) -> List[TrackedFace]:
        """Detect faces and assign priorities"""
        if not self.camera_detector:
            return []
        
        try:
            # Use existing smart camera detector
            face_detections = self.camera_detector.detect_faces(frame)
            
            tracked_faces = []
            current_time = time.time()
            
            for detection in face_detections:
                name = detection.get('name', 'Unknown').lower()
                confidence = detection.get('confidence', 0)
                bbox = detection.get('bbox', [0, 0, 0, 0])
                
                # Calculate face center
                left, top, right, bottom = bbox
                center_x = (left + right) // 2
                center_y = (top + bottom) // 2
                center = (center_x, center_y)
                
                # Assign priority
                priority = self._get_face_priority(name, confidence)
                
                # Boost priority for conversation mode target
                if self.conversation_mode and self.current_target and name == self.current_target:
                    priority = TrackingPriority.HIGHEST
                
                tracked_face = TrackedFace(
                    name=name,
                    confidence=confidence,
                    bbox=bbox,
                    center=center,
                    priority=priority,
                    last_seen=current_time
                )
                
                tracked_faces.append(tracked_face)
            
            return tracked_faces
            
        except Exception as e:
            self.logger.error(f"❌ Face detection error: {e}")
            return []
    
    def _get_face_priority(self, name: str, confidence: float) -> TrackingPriority:
        """Determine face tracking priority"""
        # Highest priority for Sophia and Eladriel
        if name in self.priority_users:
            return TrackingPriority.HIGHEST
        
        # High priority for other known faces with good confidence
        if name != 'unknown' and confidence > 0.6:
            return TrackingPriority.HIGH
        
        # Medium priority for unknown faces or low confidence
        return TrackingPriority.MEDIUM
    
    def _select_target_face(self, faces: List[TrackedFace]) -> Optional[TrackedFace]:
        """Select the best face to track based on priority and conversation mode"""
        if not faces:
            return None
        
        # Sort by priority (highest first), then by confidence
        sorted_faces = sorted(faces, key=lambda f: (f.priority.value, -f.confidence))
        
        # In conversation mode, strongly prefer the current target
        if self.conversation_mode and self.current_target:
            for face in faces:
                if face.name == self.current_target:
                    return face
        
        # Special handling for priority users
        priority_faces = [f for f in faces if f.priority == TrackingPriority.HIGHEST]
        if priority_faces:
            # If both Sophia and Eladriel are present, choose based on conversation mode or confidence
            if len(priority_faces) > 1:
                if self.conversation_mode and self.current_target:
                    target_face = next((f for f in priority_faces if f.name == self.current_target), None)
                    if target_face:
                        return target_face
                # Default to highest confidence
                return max(priority_faces, key=lambda f: f.confidence)
            return priority_faces[0]
        
        return sorted_faces[0] if sorted_faces else None
    
    def _track_face(self, face: TrackedFace, frame_shape: Tuple[int, int]):
        """Track a specific face with smooth servo movement"""
        frame_height, frame_width = frame_shape[:2]
        center_x, center_y = face.center
        
        # Calculate servo positions with smoothing
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2
        
        # Calculate error from center
        error_x = center_x - frame_center_x
        error_y = center_y - frame_center_y
        
        # Convert to servo adjustments (with sensitivity tuning)
        pan_adjustment = -(error_x / frame_width) * 90  # Invert for correct direction
        tilt_adjustment = (error_y / frame_height) * 60  # Smaller range for tilt
        
        # Apply smoothing
        target_pan = self.pan_center + pan_adjustment
        target_tilt = self.tilt_center + tilt_adjustment
        
        # Smooth movement toward target
        self.pan_current += (target_pan - self.pan_current) * self.tracking_smoothing
        self.tilt_current += (target_tilt - self.tilt_current) * self.tracking_smoothing
        
        # Clamp to servo limits
        self.pan_current = max(self.servo_min, min(self.servo_max, self.pan_current))
        self.tilt_current = max(self.servo_min, min(self.servo_max, self.tilt_current))
        
        # Move servos
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        self.logger.debug(f"🎯 Tracking {face.name} at ({center_x}, {center_y}) -> servos({int(self.pan_current)}, {int(self.tilt_current)})")
    
    def _start_search_behavior(self):
        """Start intelligent search behavior when no faces are detected"""
        self.search_active = True
        self.search_start_time = time.time()
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_direction = 1
        
        self.logger.info("🔍 Starting intelligent search for faces...")
    
    def _continue_search_behavior(self):
        """Continue search behavior with different patterns"""
        current_time = time.time()
        search_duration = current_time - self.search_start_time
        
        if search_duration > self.search_timeout:
            # Search timeout - return to center
            self._end_search_behavior()
            return
        
        if self.search_pattern == SearchPattern.SWEEP_LEFT_RIGHT:
            self._sweep_left_right()
        elif self.search_pattern == SearchPattern.LOOK_UP:
            self._look_up()
        elif self.search_pattern == SearchPattern.CENTER_PAUSE:
            self._center_pause()
    
    def _sweep_left_right(self):
        """Sweep left and right to search for faces"""
        # Move search position
        self.search_position += self.search_direction * self.search_step
        
        # Check boundaries and reverse direction
        if self.search_position >= 140:  # Right limit
            self.search_direction = -1
            self.search_position = 140
        elif self.search_position <= 40:  # Left limit
            self.search_direction = 1
            self.search_position = 40
            # After completing left-right sweep, look up
            if time.time() - self.search_start_time > 4:
                self.search_pattern = SearchPattern.LOOK_UP
                self.search_start_time = time.time()
        
        # Move servo smoothly
        target_pan = self.search_position
        self.pan_current += (target_pan - self.pan_current) * 0.3
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        time.sleep(0.1)  # Slow, deliberate movement
    
    def _look_up(self):
        """Look up to search for faces"""
        # Move tilt up gradually
        target_tilt = max(self.servo_min + 20, self.tilt_center - 30)
        self.tilt_current += (target_tilt - self.tilt_current) * 0.2
        
        # Return pan to center while looking up
        self.pan_current += (self.pan_center - self.pan_current) * 0.2
        
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        # After 2 seconds looking up, pause at center
        if time.time() - self.search_start_time > 2:
            self.search_pattern = SearchPattern.CENTER_PAUSE
            self.search_start_time = time.time()
        
        time.sleep(0.1)
    
    def _center_pause(self):
        """Pause at center before ending search"""
        # Return to center position
        self.pan_current += (self.pan_center - self.pan_current) * 0.3
        self.tilt_current += (self.tilt_center - self.tilt_current) * 0.3
        
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        # After 1 second at center, end search
        if time.time() - self.search_start_time > 1:
            self._end_search_behavior()
        
        time.sleep(0.1)
    
    def _end_search_behavior(self):
        """End search behavior and return to center"""
        self.search_active = False
        
        # Return to center
        self.face_tracker.move_servos(self.pan_center, self.tilt_center)
        self.pan_current = self.pan_center
        self.tilt_current = self.tilt_center
        
        self.logger.info("🔍 Search completed - returning to center position")
    
    def get_tracking_status(self) -> Dict:
        """Get current tracking status"""
        return {
            'tracking_active': self.is_tracking,
            'conversation_mode': self.conversation_mode,
            'current_target': self.current_target,
            'search_active': self.search_active,
            'pan_position': int(self.pan_current),
            'tilt_position': int(self.tilt_current),
            'priority_users': list(self.priority_users)
        }
    
    def manual_look(self, direction: str, amount: int = 20):
        """Manual look command (for voice control integration)"""
        if direction == 'left':
            new_pan = max(self.servo_min, self.pan_current - amount)
            self.face_tracker.move_servos(int(new_pan), int(self.tilt_current))
            self.pan_current = new_pan
        elif direction == 'right':
            new_pan = min(self.servo_max, self.pan_current + amount)
            self.face_tracker.move_servos(int(new_pan), int(self.tilt_current))
            self.pan_current = new_pan
        elif direction == 'up':
            new_tilt = max(self.servo_min, self.tilt_current - amount)
            self.face_tracker.move_servos(int(self.pan_current), int(new_tilt))
            self.tilt_current = new_tilt
        elif direction == 'down':
            new_tilt = min(self.servo_max, self.tilt_current + amount)
            self.face_tracker.move_servos(int(self.pan_current), int(new_tilt))
            self.tilt_current = new_tilt
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_tracking()
        if self.face_tracker:
            self.face_tracker.cleanup()
        self.logger.info("🧹 Intelligent Face Tracker cleaned up")

# Integration function for main AI system
def create_intelligent_tracker(arduino_port='/dev/ttyUSB0', camera_index=0) -> IntelligentFaceTracker:
    """Create and initialize the intelligent face tracker"""
    tracker = IntelligentFaceTracker(arduino_port, camera_index)
    
    if tracker.initialize():
        return tracker
    else:
        raise Exception("Failed to initialize Intelligent Face Tracker")

if __name__ == "__main__":
    # Test the intelligent face tracker
    import argparse
    
    parser = argparse.ArgumentParser(description='Intelligent Face Tracker Test')
    parser.add_argument('--arduino-port', default='/dev/ttyUSB0', help='Arduino port')
    parser.add_argument('--camera-index', type=int, default=0, help='Camera index')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    print("🎯 INTELLIGENT FACE TRACKER TEST")
    print("=" * 50)
    
    try:
        tracker = create_intelligent_tracker(args.arduino_port, args.camera_index)
        
        print("✅ Tracker initialized successfully!")
        print("🎯 Starting tracking in test mode...")
        
        tracker.start_tracking(conversation_mode=False)
        
        print("\nPress Enter to test conversation mode...")
        input()
        
        print("💬 Switching to conversation mode with Sophia priority...")
        tracker.set_conversation_mode(True, "sophia")
        
        print("\nPress Enter to stop tracking...")
        input()
        
        tracker.stop_tracking()
        tracker.cleanup()
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 