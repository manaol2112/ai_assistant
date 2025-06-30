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
    CRITICAL = 5 # Special critical priority
    LOW = 6       # Low confidence
    IGNORE = 7   # Ignore this face

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
    """
    Enhanced intelligent face tracking system with optimized real-time performance.
    Features priority-based tracking for Sophia and Eladriel with sub-second response times.
    """
    
    def __init__(self, arduino_port: str = '/dev/ttyUSB0', camera_index: int = 0):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Hardware components
        self.arduino_port = arduino_port
        self.camera_index = camera_index
        self.face_tracker = None
        self.camera_detector = None
        
        # Tracking state
        self.tracking_active = False
        self.tracking_thread = None
        self.stop_event = threading.Event()
        
        # Performance optimizations
        self.target_fps = 30  # Increased from 20 FPS for faster response
        self.frame_skip = 2   # Process every 2nd frame for speed
        self.frame_counter = 0
        self.detection_interval = 3  # Run detection every 3 frames
        
        # Priority users (Sophia and Eladriel)
        self.priority_users = ['sophia', 'eladriel']
        
        # Conversation mode
        self.conversation_mode = False
        self.current_target = None
        
        # Servo control with optimized responsiveness
        self.servo_min = 10
        self.servo_max = 170
        self.pan_center = 90
        self.tilt_center = 90
        self.pan_current = self.pan_center
        self.tilt_current = self.tilt_center
        
        # Enhanced tracking parameters for real-time response
        self.tracking_smoothing = 0.7  # Increased from default for faster movement
        self.movement_threshold = 5    # Minimum movement to trigger servo update
        self.max_movement_per_frame = 15  # Limit for smooth movement
        
        # Face tracking state with prediction
        self.last_known_position = None
        self.last_movement_direction = (0, 0)
        self.face_lost_timeout = 0.8  # Reduced from 2.0 seconds
        self.last_detection_time = time.time()
        
        # Search behavior with faster patterns
        self.search_active = False
        self.search_start_time = time.time()
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_direction = 1
        self.search_position = self.pan_center
        self.search_step = 8  # Increased step size for faster search
        self.search_timeout = 8  # Reduced timeout
        
        # Performance monitoring
        self.frame_times = []
        self.last_performance_log = time.time()
        
    def initialize(self) -> bool:
        """Initialize hardware components with performance optimizations"""
        try:
            self.logger.info("⚡ Initializing optimized intelligent face tracker...")
            
            # Initialize face tracker with performance optimizations
            self.face_tracker = PremiumFaceTracker(self.arduino_port, self.camera_index)
            
            # Initialize camera detector with optimized settings
            self.camera_detector = SmartCameraDetector(self.camera_index)
            
            # Optimize camera settings for real-time performance
            if hasattr(self.camera_detector, 'cap') and self.camera_detector.cap:
                # Set optimal resolution for speed vs quality balance
                self.camera_detector.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduced from higher res
                self.camera_detector.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # Reduced from higher res
                self.camera_detector.cap.set(cv2.CAP_PROP_FPS, 30)           # Higher FPS
                self.camera_detector.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)     # Minimal buffer for low latency
                
                # Additional optimizations if supported
                try:
                    self.camera_detector.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                    self.logger.info("📷 Camera optimized for real-time performance (640x480@30fps)")
                except:
                    self.logger.info("📷 Camera initialized with basic optimizations")
            
            # Test hardware functionality
            if not self._test_hardware():
                return False
            
            self.logger.info("✅ Optimized intelligent face tracker initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize: {e}")
            return False
    
    def _test_hardware(self) -> bool:
        """Quick hardware functionality test for real-time system"""
        try:
            # Test Arduino connection
            if not self.face_tracker.initialize_arduino():
                self.logger.error("❌ Arduino connection failed")
                return False
            
            # Test camera
            if not self.face_tracker.initialize_camera():
                self.logger.error("❌ Camera initialization failed")
                return False
            
            # Quick servo test - center position
            self.face_tracker.move_servos(self.pan_center, self.tilt_center)
            time.sleep(0.5)  # Quick settling time
            
            self.logger.info("✅ Hardware test passed - ready for real-time tracking")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Hardware test failed: {e}")
            return False

    def start_tracking(self, priority_user: str = None) -> bool:
        """Start optimized real-time intelligent tracking"""
        try:
            if self.tracking_active:
                self.logger.warning("⚠️ Tracking already active")
                return True
            
            self.logger.info("🚀 Starting optimized real-time face tracking...")
            
            # Reset state for clean start
            self.stop_event.clear()
            self.frame_counter = 0
            self.last_detection_time = time.time()
            self.last_known_position = None
            self.last_movement_direction = (0, 0)
            
            # Set priority user if specified
            if priority_user:
                self.current_target = priority_user.lower()
                self.logger.info(f"🎯 Priority tracking for: {priority_user}")
            
            # Start tracking thread
            self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
            self.tracking_thread.start()
            
            self.tracking_active = True
            self.logger.info("✅ Optimized tracking started successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start tracking: {e}")
            return False

    def stop_tracking(self) -> bool:
        """Stop real-time intelligent tracking cleanly"""
        try:
            if not self.tracking_active:
                self.logger.warning("⚠️ Tracking not active")
                return True
            
            self.logger.info("🛑 Stopping optimized face tracking...")
            
            # Signal stop and wait for thread
            self.stop_event.set()
            
            if self.tracking_thread and self.tracking_thread.is_alive():
                self.tracking_thread.join(timeout=2.0)  # Quick shutdown
                
                if self.tracking_thread.is_alive():
                    self.logger.warning("⚠️ Tracking thread did not stop cleanly")
            
            # Reset to center position
            self.face_tracker.move_servos(self.pan_center, self.tilt_center)
            
            # Clean state
            self.tracking_active = False
            self.search_active = False
            self.current_target = None
            
            self.logger.info("✅ Optimized tracking stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping tracking: {e}")
            return False
    
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
        """Optimized real-time tracking loop with performance enhancements"""
        self.logger.info("🎯 Starting optimized real-time tracking loop...")
        
        # Performance counters
        last_fps_time = time.time()
        fps_counter = 0
        
        while not self.stop_event.is_set():
            try:
                loop_start = time.time()
                
                # Capture frame
                ret, frame = self.camera_detector.cap.read()
                if not ret:
                    self.logger.warning("⚠️ Failed to capture frame")
                    time.sleep(0.1)
                    continue
                
                self.frame_counter += 1
                
                # Skip frames for performance (process every nth frame)
                if self.frame_counter % self.frame_skip != 0:
                    time.sleep(0.01)  # Minimal delay
                    continue
                
                # Detect faces only every few frames for performance
                detected_faces = []
                if self.frame_counter % self.detection_interval == 0:
                    detected_faces = self._detect_and_prioritize_faces(frame)
                else:
                    # Use prediction for missed frames if we have last known position
                    if self.last_known_position:
                        detected_faces = self._predict_face_position()
                
                current_time = time.time()
                
                if detected_faces:
                    # Faces detected - track the highest priority face
                    self.last_detection_time = current_time
                    self.search_active = False
                    
                    target_face = self._select_target_face(detected_faces)
                    if target_face:
                        self._track_face_optimized(target_face, frame.shape)
                        self.last_known_position = target_face.center
                        
                else:
                    # No faces detected - start intelligent search
                    time_since_last_detection = current_time - self.last_detection_time
                    
                    if time_since_last_detection > self.face_lost_timeout:
                        if not self.search_active:
                            self._start_search_behavior()
                        else:
                            self._continue_search_behavior()
                
                # Performance monitoring
                fps_counter += 1
                if current_time - last_fps_time >= 5.0:  # Log every 5 seconds
                    fps = fps_counter / (current_time - last_fps_time)
                    self.logger.debug(f"📊 Tracking FPS: {fps:.1f}")
                    fps_counter = 0
                    last_fps_time = current_time
                
                # Dynamic sleep for target FPS
                loop_time = time.time() - loop_start
                target_loop_time = 1.0 / self.target_fps
                if loop_time < target_loop_time:
                    time.sleep(target_loop_time - loop_time)
                
            except Exception as e:
                self.logger.error(f"❌ Error in optimized tracking loop: {e}")
                time.sleep(0.5)
        
        self.logger.info("🔄 Optimized tracking loop ended")
    
    def _detect_and_prioritize_faces(self, frame) -> List[TrackedFace]:
        """Optimized face detection with priority-based filtering and performance enhancements"""
        try:
            # Scale down frame for faster detection
            detection_scale = 0.75  # Use 75% of original size for detection
            small_frame = cv2.resize(frame, None, fx=detection_scale, fy=detection_scale)
            
            # Use camera detector for initial face detection
            faces_data = self.camera_detector.detect_faces(small_frame)
            
            if not faces_data or not faces_data.get('faces'):
                return []
            
            detected_faces = []
            current_time = time.time()
            
            for face_info in faces_data['faces']:
                try:
                    # Scale coordinates back to original frame size
                    scale_factor = 1.0 / detection_scale
                    bbox = face_info.get('bbox', [0, 0, 100, 100])
                    scaled_bbox = [int(coord * scale_factor) for coord in bbox]
                    
                    # Calculate center point
                    center_x = scaled_bbox[0] + scaled_bbox[2] // 2
                    center_y = scaled_bbox[1] + scaled_bbox[3] // 2
                    
                    # Get face name and confidence
                    name = face_info.get('name', 'unknown').lower()
                    confidence = face_info.get('confidence', 0.0)
                    
                    # Fast priority determination
                    priority = self._get_fast_priority(name, confidence)
                    
                    # Create tracked face object
                    tracked_face = TrackedFace(
                        name=name,
                        confidence=confidence,
                        bbox=tuple(scaled_bbox),
                        center=(center_x, center_y),
                        priority=priority,
                        last_seen=current_time
                    )
                    
                    detected_faces.append(tracked_face)
                    
                except Exception as e:
                    self.logger.debug(f"⚠️ Error processing face: {e}")
                    continue
            
            # Sort by priority and confidence for fast selection
            detected_faces.sort(key=lambda f: (f.priority.value, f.confidence), reverse=True)
            
            self.logger.debug(f"🔍 Fast detected {len(detected_faces)} faces")
            return detected_faces
            
        except Exception as e:
            self.logger.error(f"❌ Error in optimized face detection: {e}")
            return []
    
    def _get_fast_priority(self, name: str, confidence: float) -> TrackingPriority:
        """Fast priority calculation for real-time performance"""
        # Quick priority lookup for known users
        if name in self.priority_users:
            return TrackingPriority.CRITICAL if confidence > 0.8 else TrackingPriority.HIGH
        
        # Conversation mode gets priority
        if self.conversation_mode and confidence > 0.6:
            return TrackingPriority.HIGH
        
        # Default priority based on confidence
        if confidence > 0.8:
            return TrackingPriority.MEDIUM
        elif confidence > 0.5:
            return TrackingPriority.LOW
        else:
            return TrackingPriority.IGNORE
    
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
    
    def _track_face_optimized(self, face: TrackedFace, frame_shape: Tuple[int, int]):
        """Optimized face tracking with faster servo movement and predictive control"""
        frame_height, frame_width = frame_shape[:2]
        center_x, center_y = face.center
        
        # Calculate movement direction for prediction
        if self.last_known_position:
            movement_x = center_x - self.last_known_position[0]
            movement_y = center_y - self.last_known_position[1]
            self.last_movement_direction = (movement_x, movement_y)
        
        # Calculate servo positions with enhanced responsiveness
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2
        
        # Calculate error from center with deadzone for stability
        error_x = center_x - frame_center_x
        error_y = center_y - frame_center_y
        
        # Only move if error is significant enough
        if abs(error_x) < 20 and abs(error_y) < 20:
            return  # Face is close enough to center
        
        # Convert to servo adjustments with enhanced sensitivity
        pan_adjustment = -(error_x / frame_width) * 120  # Increased range for faster response
        tilt_adjustment = (error_y / frame_height) * 80   # Increased range for faster response
        
        # Calculate target positions
        target_pan = self.pan_center + pan_adjustment
        target_tilt = self.tilt_center + tilt_adjustment
        
        # Enhanced smoothing with predictive component
        pan_diff = target_pan - self.pan_current
        tilt_diff = target_tilt - self.tilt_current
        
        # Limit maximum movement per frame for smoothness
        pan_diff = max(-self.max_movement_per_frame, min(self.max_movement_per_frame, pan_diff))
        tilt_diff = max(-self.max_movement_per_frame, min(self.max_movement_per_frame, tilt_diff))
        
        # Apply movement with optimized smoothing
        self.pan_current += pan_diff * self.tracking_smoothing
        self.tilt_current += tilt_diff * self.tracking_smoothing
        
        # Clamp to servo limits
        self.pan_current = max(self.servo_min, min(self.servo_max, self.pan_current))
        self.tilt_current = max(self.servo_min, min(self.servo_max, self.tilt_current))
        
        # Only move servos if movement is significant enough
        if abs(pan_diff) > self.movement_threshold or abs(tilt_diff) > self.movement_threshold:
            self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
            
            self.logger.debug(f"🎯 Fast tracking {face.name} at ({center_x}, {center_y}) -> servos({int(self.pan_current)}, {int(self.tilt_current)})")
    
    def _start_search_behavior(self):
        """Start optimized intelligent search behavior when no faces are detected"""
        self.search_active = True
        self.search_start_time = time.time()
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_direction = 1
        
        self.logger.info("🔍 Starting fast intelligent search for faces...")
    
    def _continue_search_behavior(self):
        """Continue search behavior with optimized faster patterns"""
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
            self._center_pause()
    
    def _sweep_left_right_fast(self):
        """Optimized faster sweep left and right to search for faces"""
        # Move search position with larger steps
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
        
        # Move servo with faster response
        target_pan = self.search_position
        self.pan_current += (target_pan - self.pan_current) * 0.6  # Increased from 0.3
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
    
    def _look_up_fast(self):
        """Optimized faster look up behavior"""
        # Move tilt up gradually
        target_tilt = self.tilt_center - 30  # Look up
        self.tilt_current += (target_tilt - self.tilt_current) * 0.5  # Faster movement
        self.face_tracker.move_servos(int(self.pan_current), int(self.tilt_current))
        
        # After looking up for 1.5 seconds, pause at center
        if time.time() - self.search_start_time > 1.5:  # Reduced from longer
            self.search_pattern = SearchPattern.CENTER_PAUSE
            self.search_start_time = time.time()
    
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

    def _predict_face_position(self) -> List[TrackedFace]:
        """Predict face position when detection is skipped for performance"""
        if not self.last_known_position:
            return []
        
        # Simple prediction based on last movement direction
        predicted_x = self.last_known_position[0] + self.last_movement_direction[0] * 2
        predicted_y = self.last_known_position[1] + self.last_movement_direction[1] * 2
        
        predicted_face = TrackedFace(
            name="predicted",
            confidence=0.8,
            bbox=(predicted_x-50, predicted_y-50, predicted_x+50, predicted_y+50),
            center=(predicted_x, predicted_y),
            priority=TrackingPriority.HIGH,
            last_seen=time.time(),
            prediction=(predicted_x, predicted_y)
        )
        
        return [predicted_face]

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