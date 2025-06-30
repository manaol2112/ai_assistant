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
        self.logger = logging.getLogger(__name__)
        
        # Hardware components
        self.arduino_port = arduino_port
        self.camera_index = camera_index
        self.face_tracker = None
        self.camera_detector = None
        
        # Tracking state
        self.is_tracking = False
        self.tracking_thread = None
        self.priority_users = ['sophia', 'eladriel']
        
        # Conversation mode
        self.conversation_mode = False
        self.current_target = None
        
        # Servo positions and movement parameters
        self.pan_center = 90
        self.tilt_center = 90
        self.pan_current = 90
        self.tilt_current = 90
        self.servo_min = 20
        self.servo_max = 160
        
        # OPTIMIZED PERFORMANCE PARAMETERS
        self.tracking_smoothing = 0.7  # Increased for faster response (was 0.3)
        self.movement_threshold = 3    # Minimum movement to reduce jitter
        
        # REAL-TIME FRAME PROCESSING
        self.target_fps = 60          # Higher FPS for real-time tracking
        self.frame_skip = 2           # Process every 2nd frame for face detection
        self.frame_counter = 0
        
        # PREDICTIVE TRACKING
        self.last_face_position = None
        self.face_velocity = (0, 0)
        self.prediction_weight = 0.3
        
        # Search behavior parameters
        self.search_active = False
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_position = 90
        self.search_direction = 1
        self.search_step = 8          # Faster search movement
        self.search_start_time = 0
        self.last_detection_time = time.time()
        self.face_lost_timeout = 1.0  # Reduced timeout for faster search
        self.search_timeout = 6       # Shorter search cycles
        
        # Initialize existing components
        self.face_tracker = PremiumFaceTracker(arduino_port, camera_index)
        self.camera_detector = None
        
        # Threading
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
        """OPTIMIZED Main tracking loop with real-time performance"""
        self.logger.info("🎯 Starting OPTIMIZED intelligent tracking loop...")
        
        while self.running:
            try:
                # REAL-TIME FRAME CAPTURE
                frame = self.camera_detector.get_frame()
                if frame is None:
                    time.sleep(0.001)  # Minimal delay
                    continue
                
                self.frame_counter += 1
                current_time = time.time()
                
                # OPTIMIZED FACE DETECTION (skip frames for performance)
                detected_faces = []
                if self.frame_counter % self.frame_skip == 0:
                    detected_faces = self._detect_and_prioritize_faces()
                
                if detected_faces:
                    # FAST FACE TRACKING
                    self.last_detection_time = current_time
                    self.search_active = False
                    
                    target_face = self._select_target_face(detected_faces)
                    if target_face:
                        self._track_face_optimized(target_face)
                        
                elif self.last_face_position and self.face_velocity != (0, 0):
                    # PREDICTIVE TRACKING - continue tracking based on last known movement
                    predicted_position = self._predict_face_position()
                    if predicted_position:
                        self._track_predicted_position(predicted_position)
                        
                else:
                    # INTELLIGENT SEARCH (only after timeout)
                    time_since_last_detection = current_time - self.last_detection_time
                    
                    if time_since_last_detection > self.face_lost_timeout:
                        if not self.search_active:
                            self._start_search_behavior()
                        else:
                            self._continue_search_behavior()
                
                # HIGH FPS LOOP - much faster than before
                time.sleep(1.0 / self.target_fps)  # ~60 FPS (0.016s vs 0.05s)
                
            except Exception as e:
                self.logger.error(f"❌ Error in tracking loop: {e}")
                time.sleep(0.1)  # Brief pause on error
        
        self.logger.info("🔄 Optimized tracking loop ended")
    
    def _detect_and_prioritize_faces(self):
        """OPTIMIZED fast face detection with priority assignment"""
        try:
            # Use optimized detection from camera
            faces = self.camera_detector.detect_faces()
            if not faces:
                return []
            
            # Quick validation - remove faces that are too small or low confidence
            min_face_size = 30  # Minimum face size in pixels
            min_confidence = 0.3  # Minimum confidence threshold
            
            valid_faces = []
            for face in faces:
                # Quick size check
                face_width = face.get('w', 0)
                face_height = face.get('h', 0)
                confidence = face.get('confidence', 0)
                
                if face_width >= min_face_size and face_height >= min_face_size and confidence >= min_confidence:
                    valid_faces.append(face)
            
            if not valid_faces:
                return []
            
            # FAST priority assignment - simplified logic
            priority_faces = []
            for face in valid_faces:
                priority_score = self._calculate_fast_priority(face)
                priority_faces.append({
                    'face': face,
                    'priority': priority_score,
                    'x': face.get('x', 0),
                    'y': face.get('y', 0),
                    'w': face.get('w', 0),
                    'h': face.get('h', 0),
                    'confidence': face.get('confidence', 0)
                })
            
            # Sort by priority (highest first) - quick sort
            priority_faces.sort(key=lambda x: x['priority'], reverse=True)
            
            return priority_faces
            
        except Exception as e:
            self.logger.error(f"❌ Fast face detection error: {e}")
            return []
    
    def _calculate_fast_priority(self, face):
        """OPTIMIZED fast priority calculation"""
        try:
            # Base confidence score (0-100)
            confidence = face.get('confidence', 0) * 100
            
            # Face size bonus - larger faces get higher priority
            face_area = face.get('w', 0) * face.get('h', 0)
            size_bonus = min(face_area / 1000, 50)  # Cap at 50 points
            
            # Center position bonus - faces near center get priority
            face_center_x = face.get('x', 0) + face.get('w', 0) / 2
            frame_center_x = 320  # Assuming 640px width
            distance_from_center = abs(face_center_x - frame_center_x)
            center_bonus = max(0, 30 - distance_from_center / 10)  # Up to 30 points
            
            # User recognition bonus (if available)
            recognition_bonus = 0
            name = face.get('name', 'Unknown')
            if name in self.priority_users:
                recognition_bonus = 100  # High priority for known users
            elif name != 'Unknown':
                recognition_bonus = 50   # Medium priority for recognized faces
            
            total_priority = confidence + size_bonus + center_bonus + recognition_bonus
            
            return total_priority
            
        except Exception as e:
            self.logger.error(f"❌ Priority calculation error: {e}")
            return 0
    
    def _track_face_optimized(self, face_data):
        """OPTIMIZED face tracking with predictive movement and minimal lag"""
        try:
            face = face_data['face']
            face_x = face_data['x']
            face_y = face_data['y']
            face_w = face_data['w']
            face_h = face_data['h']
            
            # Calculate face center
            face_center_x = face_x + face_w / 2
            face_center_y = face_y + face_h / 2
            
            # Update predictive tracking
            current_position = (face_center_x, face_center_y)
            if self.last_face_position:
                # Calculate velocity for prediction
                self.face_velocity = (
                    current_position[0] - self.last_face_position[0],
                    current_position[1] - self.last_face_position[1]
                )
            self.last_face_position = current_position
            
            # Calculate servo adjustments with FASTER response
            frame_center_x = 320  # Camera frame center
            frame_center_y = 240
            
            error_x = face_center_x - frame_center_x
            error_y = face_center_y - frame_center_y
            
            # OPTIMIZED servo calculations with higher responsiveness
            pan_adjustment = error_x * self.pan_sensitivity * 1.5  # Increased sensitivity
            tilt_adjustment = error_y * self.tilt_sensitivity * 1.5
            
            # Apply FASTER smoothing with higher responsiveness
            target_pan = self.pan_current - pan_adjustment
            target_tilt = self.tilt_current + tilt_adjustment
            
            # Clamp to servo limits
            target_pan = max(self.servo_min, min(self.servo_max, target_pan))
            target_tilt = max(self.servo_min, min(self.servo_max, target_tilt))
            
            # FASTER movement with reduced lag
            self.pan_current += (target_pan - self.pan_current) * self.tracking_smoothing
            self.tilt_current += (target_tilt - self.tilt_current) * self.tracking_smoothing
            
            # Movement threshold to reduce jitter - only move if change is significant
            pan_change = abs(target_pan - self.pan_current)
            tilt_change = abs(target_tilt - self.tilt_current)
            
            if pan_change > self.movement_threshold or tilt_change > self.movement_threshold:
                self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
                
                # Log only significant movements
                if pan_change > 5 or tilt_change > 5:
                    self.logger.debug(f"🎯 Fast track: pan={int(self.pan_current)}, tilt={int(self.tilt_current)}")
            
        except Exception as e:
            self.logger.error(f"❌ Optimized tracking error: {e}")
    
    def _predict_face_position(self):
        """Predict next face position based on velocity"""
        if self.last_face_position and self.face_velocity:
            predicted_x = self.last_face_position[0] + self.face_velocity[0] * 2
            predicted_y = self.last_face_position[1] + self.face_velocity[1] * 2
            return (predicted_x, predicted_y)
        return None
    
    def _track_predicted_position(self, predicted_pos):
        """Track predicted position with reduced smoothing for better responsiveness"""
        try:
            face_center_x, face_center_y = predicted_pos
            frame_center_x = 320
            frame_center_y = 240
            
            error_x = face_center_x - frame_center_x
            error_y = face_center_y - frame_center_y
            
            # Direct movement with minimal smoothing for prediction
            pan_adjustment = error_x * self.pan_sensitivity * 1.2
            tilt_adjustment = error_y * self.tilt_sensitivity * 1.2
            
            target_pan = self.pan_current - pan_adjustment
            target_tilt = self.tilt_current + tilt_adjustment
            
            # Clamp to limits
            target_pan = max(self.servo_min, min(self.servo_max, target_pan))
            target_tilt = max(self.servo_min, min(self.servo_max, target_tilt))
            
            # Reduced smoothing for prediction (more responsive)
            self.pan_current += (target_pan - self.pan_current) * 0.8
            self.tilt_current += (target_tilt - self.tilt_current) * 0.8
            
            self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
            
            self.logger.debug(f"🎯 Predictive track: pan={int(self.pan_current)}, tilt={int(self.tilt_current)}")
            
        except Exception as e:
            self.logger.error(f"❌ Predictive tracking error: {e}")
    
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
    
    def _start_search_behavior(self):
        """Start OPTIMIZED intelligent search behavior when no faces are detected"""
        self.search_active = True
        self.search_start_time = time.time()
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_direction = 1
        
        # Reset predictive tracking when starting search
        self.last_face_position = None
        self.face_velocity = (0, 0)
        
        self.logger.info("🔍 Starting FAST intelligent search for faces...")
    
    def _continue_search_behavior(self):
        """Continue OPTIMIZED search behavior with faster patterns"""
        current_time = time.time()
        search_duration = current_time - self.search_start_time
        
        if search_duration > self.search_timeout:
            # Search timeout - return to center
            self._end_search_behavior()
            return
        
        if self.search_pattern == SearchPattern.SWEEP_LEFT_RIGHT:
            self._sweep_left_right_fast()
        elif self.search_pattern == SearchPattern.LOOK_UP:
            self._look_up_fast()
        elif self.search_pattern == SearchPattern.CENTER_PAUSE:
            self._center_pause_brief()
    
    def _sweep_left_right_fast(self):
        """OPTIMIZED fast sweep left and right to search for faces"""
        # Faster movement with larger steps
        self.search_position += self.search_direction * self.search_step
        
        # Check boundaries and reverse direction
        if self.search_position >= 140:  # Right limit
            self.search_direction = -1
            self.search_position = 140
        elif self.search_position <= 40:  # Left limit
            self.search_direction = 1
            self.search_position = 40
            # After completing left-right sweep, look up faster
            if time.time() - self.search_start_time > 2:  # Reduced from 4 seconds
                self.search_pattern = SearchPattern.LOOK_UP
                self.search_start_time = time.time()
        
        # FASTER servo movement with higher responsiveness
        target_pan = self.search_position
        self.pan_current += (target_pan - self.pan_current) * 0.6  # Increased from 0.3
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        # Log search progress less frequently
        if int(self.search_position) % 20 == 0:
            self.logger.debug(f"🔍 Fast search: pan={int(self.pan_current)}")
    
    def _look_up_fast(self):
        """OPTIMIZED look up quickly to search different angles"""
        # Move tilt up smoothly and faster
        target_tilt = max(self.tilt_center - 30, self.servo_min)
        self.tilt_current += (target_tilt - self.tilt_current) * 0.5  # Increased speed
        
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        # Transition to center pause quickly
        if time.time() - self.search_start_time > 1.5:  # Reduced from longer time
            self.search_pattern = SearchPattern.CENTER_PAUSE
            self.search_start_time = time.time()
    
    def _center_pause_brief(self):
        """OPTIMIZED brief center pause before resuming search"""
        # Return to center position quickly
        target_pan = self.pan_center
        target_tilt = self.tilt_center
        
        self.pan_current += (target_pan - self.pan_current) * 0.8   # Very fast return
        self.tilt_current += (target_tilt - self.tilt_current) * 0.8
        
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        # Brief pause then restart search cycle
        if time.time() - self.search_start_time > 0.5:  # Very brief pause
            self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
            self.search_start_time = time.time()
    
    def _end_search_behavior(self):
        """OPTIMIZED end search and return to center quickly"""
        self.search_active = False
        
        # Quick return to center
        self.pan_current += (self.pan_center - self.pan_current) * 0.8
        self.tilt_current += (self.tilt_center - self.tilt_current) * 0.8
        
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        self.logger.info("🎯 Search ended - returned to center position")
    
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