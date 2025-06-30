#!/usr/bin/env python3
"""
REAL-TIME Intelligent Face Tracking System for AI Assistant
Ultra-fast tracking with priority recognition for Sophia and Eladriel
Continuous tracking during all conversation stages (listening, processing, responding)

Performance Optimizations:
- 60+ FPS tracking loop with lightweight face detection
- Frame skipping for face recognition (every 5-10 frames)
- Predictive tracking using motion estimation
- Separate threads for detection and tracking
- Sub-second response time (<0.2s)
- Continuous tracking during conversation stages

Features:
- Priority tracking: Sophia and Eladriel get highest priority
- Real-time tracking during conversation mode (listening, processing, responding)
- Intelligent search: looks left/right/up when no faces detected
- Ultra-smooth servo movements with predictive tracking
- Performance-optimized detection pipeline
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
from collections import deque

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
    velocity: Tuple[float, float] = (0.0, 0.0)  # Motion for prediction
    prediction: Optional[Tuple[int, int]] = None

class SearchPattern(Enum):
    """Search patterns when no faces are detected"""
    SWEEP_LEFT_RIGHT = "sweep_lr"
    LOOK_UP = "look_up"
    CENTER_PAUSE = "center_pause"

class ConversationStage(Enum):
    """Current conversation stage for continuous tracking"""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing" 
    RESPONDING = "responding"

class RealTimeIntelligentFaceTracker:
    """REAL-TIME Enhanced face tracking with sub-second response and continuous conversation tracking"""
    
    def __init__(self, arduino_port: str = '/dev/ttyUSB0', camera_index: int = 0, headless: bool = True):
        # Initialize logger
        self.logger = logging.getLogger('RealTimeIntelligentFaceTracker')
        
        # Priority users (Sophia and Eladriel get highest priority)
        self.priority_users = {'sophia', 'eladriel'}
        
        # Tracking state
        self.is_tracking = False
        self.conversation_mode = False
        self.conversation_stage = ConversationStage.IDLE
        self.current_target = None
        self.tracked_faces = {}
        self.last_detection_time = 0
        
        # Performance optimization
        self.frame_skip_counter = 0
        self.detection_interval = 3  # Run face recognition every 3 frames for performance
        self.last_known_faces = []
        self.face_history = deque(maxlen=10)  # Track face positions for prediction
        
        # Search behavior state
        self.search_active = False
        self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
        self.search_start_time = 0
        self.search_direction = 1
        self.search_position = 90
        
        # Servo control parameters - OPTIMIZED FOR BALANCED, RESPONSIVE MOVEMENT
        self.pan_center = 90
        self.tilt_center = 90
        self.pan_current = self.pan_center
        self.tilt_current = self.tilt_center
        self.servo_min = 20
        self.servo_max = 160
        self.search_step = 2  # Slower search movements (reduced from 3)
        self.tracking_smoothing = 0.6  # Balanced tracking (increased from 0.4, less than 0.8)
        self.movement_dampening = 0.8  # Less dampening for more responsiveness (increased from 0.6)
        
        # REAL-TIME Detection parameters
        self.face_lost_timeout = 1.0  # Faster search activation
        self.search_timeout = 8.0     # Shorter search time
        self.priority_boost_range = 50
        self.max_tracking_fps = 60    # Target 60 FPS tracking
        self.min_loop_time = 1.0 / self.max_tracking_fps
        
        # Initialize components with headless mode (no camera display)
        self.face_tracker = PremiumFaceTracker(arduino_port, camera_index, headless=headless)
        self.camera_detector = SmartCameraDetector(headless=True)  # Always headless for integration
        if hasattr(self.face_tracker, 'camera_handler'):
            self.camera_detector.shared_camera = self.face_tracker.camera_handler
        
        # Multi-threading for performance
        self.tracking_thread = None
        self.detection_thread = None
        self.running = False
        self.lock = threading.Lock()
        
        # Fast face detection using OpenCV (backup)
        self.cv_face_cascade = None
        self.use_cv_fallback = True
        
    def initialize(self) -> bool:
        """Initialize the real-time tracking system"""
        try:
            self.logger.info("🚀 Initializing REAL-TIME Intelligent Face Tracker...")
            
            # Initialize face tracker (servos and camera)
            camera_ok = self.face_tracker.initialize_camera()
            arduino_ok = self.face_tracker.initialize_arduino()
            
            if not arduino_ok:
                self.logger.warning("⚠️ Arduino connection failed - servo tracking disabled")
                # Continue without servo control for testing
            
            if not camera_ok:
                self.logger.error("❌ Camera initialization failed")
                return False
            
            # Initialize OpenCV face detection for fast tracking
            try:
                self.cv_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                self.logger.info("✅ OpenCV face detection initialized for real-time tracking")
            except Exception as e:
                self.logger.warning(f"⚠️ OpenCV face detection failed: {e}")
                self.use_cv_fallback = False
            
            # Center servos if available
            if arduino_ok:
                self.face_tracker.move_servos(self.pan_center, self.tilt_center)
                time.sleep(0.5)  # Reduced delay
            
            self.logger.info("✅ REAL-TIME Intelligent Face Tracker initialized!")
            self.logger.info(f"🎯 Priority users: {', '.join(self.priority_users)}")
            self.logger.info(f"⚡ Target FPS: {self.max_tracking_fps} | Detection interval: every {self.detection_interval} frames")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {e}")
            return False
    
    def start_tracking(self, conversation_mode: bool = False):
        """Start REAL-TIME intelligent face tracking"""
        with self.lock:
            if self.is_tracking:
                self.logger.warning("⚠️ Tracking already active")
                return
                
            self.is_tracking = True
            self.conversation_mode = conversation_mode
            self.running = True
            self.frame_skip_counter = 0
            
            # Start high-performance tracking thread
            self.tracking_thread = threading.Thread(
                target=self._realtime_tracking_loop,
                daemon=True,
                name="RealTimeTracker"
            )
            self.tracking_thread.start()
            
            mode_info = "conversation mode" if conversation_mode else "general mode"
            self.logger.info(f"🚀 REAL-TIME face tracking started in {mode_info}")
    
    def stop_tracking(self):
        """Stop face tracking and return to center"""
        with self.lock:
            self.is_tracking = False
            self.running = False
            self.search_active = False
            self.conversation_stage = ConversationStage.IDLE
            
        if self.tracking_thread and self.tracking_thread.is_alive():
            self.tracking_thread.join(timeout=1)
            
        # Return to center position quickly
        self._move_servos_fast(self.pan_center, self.tilt_center)
        self.pan_current = self.pan_center
        self.tilt_current = self.tilt_center
        
        self.logger.info("🛑 REAL-TIME tracking stopped")
    
    def set_conversation_mode(self, active: bool, target_user: str = None):
        """Enable/disable conversation mode with continuous tracking"""
        with self.lock:
            self.conversation_mode = active
            if active and target_user:
                self.current_target = target_user.lower()
                self.conversation_stage = ConversationStage.LISTENING
                self.logger.info(f"💬 Conversation mode active - continuously tracking {target_user}")
            else:
                self.current_target = None
                self.conversation_stage = ConversationStage.IDLE
                self.logger.info("💬 Conversation mode disabled")
    
    def set_conversation_stage(self, stage: ConversationStage):
        """Update conversation stage for continuous tracking"""
        with self.lock:
            # Handle both string and enum inputs
            if isinstance(stage, str):
                # Convert string to enum
                stage_mapping = {
                    'listening': ConversationStage.LISTENING,
                    'processing': ConversationStage.PROCESSING,
                    'responding': ConversationStage.RESPONDING,
                    'idle': ConversationStage.IDLE
                }
                stage = stage_mapping.get(stage.lower(), ConversationStage.IDLE)
            
            self.conversation_stage = stage
            stage_names = {
                ConversationStage.LISTENING: "👂 Listening",
                ConversationStage.PROCESSING: "🧠 Processing", 
                ConversationStage.RESPONDING: "🗣️ Responding",
                ConversationStage.IDLE: "😴 Idle"
            }
            self.logger.debug(f"Stage: {stage_names.get(stage, stage.name if hasattr(stage, 'name') else str(stage))}")
    
    def _realtime_tracking_loop(self):
        """ULTRA-FAST tracking loop optimized for real-time performance"""
        self.logger.info("⚡ REAL-TIME tracking loop started (60+ FPS target)")
        last_loop_time = time.time()
        
        while self.running:
            loop_start = time.time()
            
            try:
                # Capture frame
                ret, frame = self.face_tracker.read_frame()
                if not ret or frame is None:
                    time.sleep(0.01)  # Minimal delay
                    continue
                
                # PERFORMANCE OPTIMIZATION: Skip face recognition on most frames
                self.frame_skip_counter += 1
                run_recognition = (self.frame_skip_counter % self.detection_interval == 0)
                
                detected_faces = []
                current_time = time.time()
                
                if run_recognition:
                    # Full face recognition (expensive operation)
                    detected_faces = self._detect_and_prioritize_faces(frame)
                    self.last_known_faces = detected_faces.copy()
                else:
                    # Fast tracking using previous detections + OpenCV
                    detected_faces = self._fast_face_tracking(frame)
                
                if detected_faces:
                    # Faces detected - track with prediction
                    self.last_detection_time = current_time
                    self.search_active = False
                    
                    target_face = self._select_target_face(detected_faces)
                    if target_face:
                        self._track_face_realtime(target_face, frame.shape)
                        
                else:
                    # No faces detected - intelligent search
                    time_since_last_detection = current_time - self.last_detection_time
                    
                    if time_since_last_detection > self.face_lost_timeout:
                        if not self.search_active:
                            self._start_search_behavior()
                        else:
                            self._continue_search_behavior()
                
                # PERFORMANCE: Maintain target FPS
                loop_duration = time.time() - loop_start
                if loop_duration < self.min_loop_time:
                    time.sleep(self.min_loop_time - loop_duration)
                
                # Log performance stats periodically
                if current_time - last_loop_time > 5.0:  # Every 5 seconds
                    actual_fps = 1.0 / (time.time() - loop_start)
                    self.logger.debug(f"⚡ Tracking FPS: {actual_fps:.1f} | Stage: {self.conversation_stage.value}")
                    last_loop_time = current_time
                
            except Exception as e:
                self.logger.error(f"❌ Error in real-time tracking loop: {e}")
                time.sleep(0.1)
        
        self.logger.info("⚡ REAL-TIME tracking loop ended")
    
    def _fast_face_tracking(self, frame) -> List[TrackedFace]:
        """Ultra-fast face tracking using OpenCV and prediction"""
        if not self.use_cv_fallback or self.cv_face_cascade is None:
            return self.last_known_faces
        
        try:
            # Convert to grayscale for fast detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Fast face detection
            faces = self.cv_face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.2, 
                minNeighbors=3, 
                minSize=(50, 50),
                flags=cv2.CASCADE_DO_CANNY_PRUNING  # Performance optimization
            )
            
            tracked_faces = []
            current_time = time.time()
            
            for (x, y, w, h) in faces:
                # Calculate center
                center_x = x + w // 2
                center_y = y + h // 2
                center = (center_x, center_y)
                
                # Create basic tracked face (we'll enhance with recognition later)
                tracked_face = TrackedFace(
                    name='unknown',  # Will be updated by full recognition
                    confidence=0.7,  # Assume decent confidence for OpenCV detection
                    bbox=(x, y, x + w, y + h),
                    center=center,
                    priority=TrackingPriority.MEDIUM,
                    last_seen=current_time
                )
                
                # Try to match with known faces from recent recognition
                matched_face = self._match_with_known_faces(tracked_face)
                if matched_face:
                    tracked_face.name = matched_face.name
                    tracked_face.priority = matched_face.priority
                
                tracked_faces.append(tracked_face)
            
            return tracked_faces
            
        except Exception as e:
            self.logger.error(f"❌ Fast tracking error: {e}")
            return self.last_known_faces
    
    def _match_with_known_faces(self, new_face: TrackedFace) -> Optional[TrackedFace]:
        """Match detected face with recently recognized faces"""
        for known_face in self.last_known_faces:
            # Calculate distance between face centers
            dx = new_face.center[0] - known_face.center[0]
            dy = new_face.center[1] - known_face.center[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # If close enough, assume it's the same person
            if distance < 100:  # pixels
                return known_face
        
        return None
    
    def _track_face_realtime(self, face: TrackedFace, frame_shape: Tuple[int, int]):
        """Real-time face tracking with predictive movement and ultra-smooth servos"""
        frame_height, frame_width = frame_shape[:2]
        center_x, center_y = face.center
        
        # Add to face history for prediction
        self.face_history.append((center_x, center_y, time.time()))
        
        # Calculate predicted position if we have motion history
        predicted_x, predicted_y = center_x, center_y
        if len(self.face_history) >= 3:
            # Simple linear prediction based on recent movement
            recent_positions = list(self.face_history)[-3:]
            if len(recent_positions) >= 2:
                dx = recent_positions[-1][0] - recent_positions[-2][0]
                dy = recent_positions[-1][1] - recent_positions[-2][1]
                dt = recent_positions[-1][2] - recent_positions[-2][2]
                
                if dt > 0:
                    # Predict where face will be in next frame
                    prediction_time = 0.05  # Predict 50ms ahead
                    predicted_x = center_x + (dx / dt) * prediction_time
                    predicted_y = center_y + (dy / dt) * prediction_time
        
        # Use predicted position for smoother tracking
        target_x, target_y = predicted_x, predicted_y
        
        # Calculate servo positions with enhanced responsiveness
        frame_center_x = frame_width // 2
        frame_center_y = frame_height // 2
        
        # Calculate error from center
        error_x = target_x - frame_center_x
        error_y = target_y - frame_center_y
        
        # Convert to servo adjustments with BALANCED sensitivity for smooth but responsive movement
        pan_adjustment = -(error_x / frame_width) * 50   # Balanced - increased from 25, less than 100
        tilt_adjustment = (error_y / frame_height) * 35  # Balanced - increased from 20, less than 70
        
        # Apply enhanced smoothing for real-time response
        target_pan = self.pan_center + pan_adjustment
        target_tilt = self.tilt_center + tilt_adjustment
        
        # More responsive movement toward target with dampening
        smoothing = self.tracking_smoothing
        # Increase responsiveness during conversation mode (but still keep it smooth)
        if self.conversation_mode:
            smoothing = min(0.6, smoothing + 0.2)  # Less aggressive increase
        
        # Apply smoothing with additional dampening for ultra-smooth movement
        pan_delta = (target_pan - self.pan_current) * smoothing * self.movement_dampening
        tilt_delta = (target_tilt - self.tilt_current) * smoothing * self.movement_dampening
        
        self.pan_current += pan_delta
        self.tilt_current += tilt_delta
        
        # Clamp to servo limits
        self.pan_current = max(self.servo_min, min(self.servo_max, self.pan_current))
        self.tilt_current = max(self.servo_min, min(self.servo_max, self.tilt_current))
        
        # Move servos with optimized speed
        self._move_servos_fast(int(self.pan_current), int(self.tilt_current))
        
        # Enhanced logging for conversation mode
        if self.conversation_mode:
            stage_emoji = {
                ConversationStage.LISTENING: "👂",
                ConversationStage.PROCESSING: "🧠", 
                ConversationStage.RESPONDING: "🗣️",
                ConversationStage.IDLE: "😴"
            }
            emoji = stage_emoji.get(self.conversation_stage, "🎯")
            self.logger.debug(f"{emoji} Tracking {face.name} [{self.conversation_stage.value}] -> servos({int(self.pan_current)}, {int(self.tilt_current)})")
    
    def _move_servos_fast(self, pan: int, tilt: int):
        """Optimized servo movement for real-time performance"""
        try:
            if hasattr(self.face_tracker, 'move_servos'):
                self.face_tracker.move_servos(pan, tilt)
        except Exception as e:
            # Don't let servo errors stop tracking
            self.logger.debug(f"Servo movement error: {e}")
    
    def _detect_and_prioritize_faces(self, frame) -> List[TrackedFace]:
        """Enhanced face detection with priority handling"""
        detected_faces = []
        current_time = time.time()
        
        try:
            # Use smart camera detector for face recognition
            if self.camera_detector:
                faces_info = self.camera_detector.detect_faces(frame)
                
                for face_info in faces_info:
                    name = face_info.get('name', 'unknown').lower()
                    confidence = face_info.get('confidence', 0.0)
                    bbox = face_info.get('bbox', (0, 0, 0, 0))
                    
                    # Calculate center from bounding box
                    left, top, right, bottom = bbox
                    center_x = (left + right) // 2
                    center_y = (top + bottom) // 2
                    center = (center_x, center_y)
                    
                    # Determine priority
                    if name in self.priority_users:
                        priority = TrackingPriority.HIGHEST
                        # Priority boost for conversation mode
                        if self.conversation_mode and name == self.current_target:
                            confidence += 0.2
                    elif name != 'unknown':
                        priority = TrackingPriority.HIGH
                    else:
                        priority = TrackingPriority.MEDIUM
                    
                    tracked_face = TrackedFace(
                        name=name,
                        confidence=confidence,
                        bbox=bbox,
                        center=center,
                        priority=priority,
                        last_seen=current_time
                    )
                    
                    detected_faces.append(tracked_face)
            
            # Fallback to OpenCV if smart detector fails
            if not detected_faces and self.use_cv_fallback:
                detected_faces = self._fast_face_tracking(frame)
                
        except Exception as e:
            self.logger.error(f"❌ Face detection error: {e}")
            # Use fast tracking as fallback
            if self.use_cv_fallback:
                detected_faces = self._fast_face_tracking(frame)
        
        return detected_faces
    
    def _select_target_face(self, faces: List[TrackedFace]) -> Optional[TrackedFace]:
        """Enhanced target selection with conversation mode priority"""
        if not faces:
            return None
        
        # Conversation mode: prioritize target user
        if self.conversation_mode and self.current_target:
            for face in faces:
                if face.name == self.current_target:
                    self.logger.debug(f"💬 Conversation target found: {face.name}")
                    return face
        
        # Sort by priority, then confidence
        def sort_key(face):
            priority_weight = {
                TrackingPriority.HIGHEST: 4,
                TrackingPriority.HIGH: 3,
                TrackingPriority.MEDIUM: 2,
                TrackingPriority.SEARCH: 1
            }
            return (priority_weight.get(face.priority, 0), face.confidence)
        
        sorted_faces = sorted(faces, key=sort_key, reverse=True)
        selected = sorted_faces[0]
        
        # Enhanced logging for conversation mode
        if self.conversation_mode:
            stage_emoji = {
                ConversationStage.LISTENING: "👂",
                ConversationStage.PROCESSING: "🧠",
                ConversationStage.RESPONDING: "🗣️",
                ConversationStage.IDLE: "😴"
            }
            emoji = stage_emoji.get(self.conversation_stage, "🎯")
            self.logger.debug(f"{emoji} Selected target: {selected.name} (confidence: {selected.confidence:.2f})")
        
        return selected
    
    def _start_search_behavior(self):
        """Start intelligent search behavior when no faces are detected"""
        if not self.search_active:
            self.search_active = True
            self.search_start_time = time.time()
            self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
            self.search_direction = 1
            self.search_position = self.pan_current
            
            # Enhanced search for conversation mode
            if self.conversation_mode:
                self.logger.info(f"🔍 Starting enhanced search for {self.current_target or 'conversation partner'}")
            else:
                self.logger.info("🔍 Starting intelligent face search")
    
    def _continue_search_behavior(self):
        """Continue search behavior with enhanced patterns"""
        current_time = time.time()
        search_duration = current_time - self.search_start_time
        
        if search_duration > self.search_timeout:
            # Search timeout - return to center and stop
            self._move_servos_fast(self.pan_center, self.tilt_center)
            self.pan_current = self.pan_center
            self.tilt_current = self.tilt_center
            self.search_active = False
            self.logger.info("🏠 Search timeout - returning to center")
            return
        
        # Enhanced search patterns based on mode
        if self.search_pattern == SearchPattern.SWEEP_LEFT_RIGHT:
            # Faster sweep with wider range during conversation
            max_range = 70 if self.conversation_mode else 50
            self.search_position += self.search_direction * self.search_step
            
            # Reverse direction at limits
            if self.search_position >= self.pan_center + max_range:
                self.search_direction = -1
            elif self.search_position <= self.pan_center - max_range:
                self.search_direction = 1
            
            # Move to search position
            self._move_servos_fast(int(self.search_position), self.tilt_center)
            
            # Occasional upward look during conversation mode
            if self.conversation_mode and int(current_time * 2) % 10 == 0:
                self.search_pattern = SearchPattern.LOOK_UP
        
        elif self.search_pattern == SearchPattern.LOOK_UP:
            # Look up briefly then return to sweep
            self._move_servos_fast(self.pan_center, self.tilt_center - 20)
            time.sleep(0.3)
            self.search_pattern = SearchPattern.SWEEP_LEFT_RIGHT
    
    def get_status(self) -> Dict:
        """Get current tracking status"""
        return {
            'is_tracking': self.is_tracking,
            'conversation_mode': self.conversation_mode,
            'conversation_stage': self.conversation_stage.value,
            'current_target': self.current_target,
            'search_active': self.search_active,
            'pan_position': int(self.pan_current),
            'tilt_position': int(self.tilt_current),
            'fps_target': self.max_tracking_fps,
            'detection_interval': self.detection_interval
        }
    
    def process_voice_command(self, command: str) -> str:
        """Process voice commands for manual control of the face tracker"""
        command_lower = command.lower().strip()
        
        try:
            # Tracking control commands
            if any(phrase in command_lower for phrase in ['look at me', 'track my face', 'track me']):
                if not self.is_tracking:
                    self.start_tracking(conversation_mode=self.conversation_mode)
                    return "I'm now tracking you! Looking your way."
                else:
                    return "I'm already tracking! I see you."
            
            elif any(phrase in command_lower for phrase in ['stop tracking', 'stop looking', 'stop watching']):
                if self.is_tracking:
                    self.stop_tracking()
                    return "I've stopped tracking and returned to center."
                else:
                    return "I wasn't tracking anyone anyway."
            
            elif any(phrase in command_lower for phrase in ['who are you looking at', 'who are you tracking', 'tracking status']):
                status = self.get_status()
                if status['is_tracking']:
                    target = status.get('current_target', 'someone')
                    if target and target != 'unknown':
                        return f"I'm currently tracking {target.title()}."
                    else:
                        return "I'm tracking someone but I'm not sure who."
                else:
                    return "I'm not tracking anyone right now."
            
            elif any(phrase in command_lower for phrase in ['search for faces', 'find faces', 'look around']):
                if not self.search_active:
                    self._start_search_behavior()
                    return "I'm now searching for faces! Looking around..."
                else:
                    return "I'm already searching for faces."
            
            # Manual movement commands
            elif 'look left' in command_lower:
                self._move_servos_fast(self.pan_center - 40, self.tilt_center)
                self.pan_current = self.pan_center - 40
                return "Looking left!"
            
            elif 'look right' in command_lower:
                self._move_servos_fast(self.pan_center + 40, self.tilt_center)
                self.pan_current = self.pan_center + 40
                return "Looking right!"
            
            elif 'look up' in command_lower:
                self._move_servos_fast(self.pan_center, self.tilt_center - 30)
                self.tilt_current = self.tilt_center - 30
                return "Looking up!"
            
            elif 'look down' in command_lower:
                self._move_servos_fast(self.pan_center, self.tilt_center + 30)
                self.tilt_current = self.tilt_center + 30
                return "Looking down!"
            
            elif any(phrase in command_lower for phrase in ['center your eyes', 'look forward', 'center view']):
                self._move_servos_fast(self.pan_center, self.tilt_center)
                self.pan_current = self.pan_center
                self.tilt_current = self.tilt_center
                self.search_active = False
                return "Centered my view!"
            
            # If no command matched
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error processing voice command '{command}': {e}")
            return "Sorry, I had trouble processing that command."
    
    def cleanup(self):
        """Clean up resources with enhanced error handling"""
        self.logger.info("🧹 Cleaning up REAL-TIME Intelligent Face Tracker...")
        
        self.running = False
        
        # Wait for tracking thread to finish
        if self.tracking_thread and self.tracking_thread.is_alive():
            self.tracking_thread.join(timeout=2)
        
        # Clean up camera and servos
        if self.face_tracker:
            try:
                self.face_tracker.cleanup()
            except Exception as e:
                self.logger.error(f"Error during cleanup: {e}")
        
        self.logger.info("🧹 REAL-TIME Intelligent Face Tracker cleaned up")

# Integration function for main AI system
def create_intelligent_tracker(arduino_port='/dev/ttyUSB0', camera_index=0, headless=True) -> RealTimeIntelligentFaceTracker:
    """Create and initialize the REAL-TIME intelligent face tracker"""
    tracker = RealTimeIntelligentFaceTracker(arduino_port, camera_index, headless=headless)
    
    if tracker.initialize():
        return tracker
    else:
        raise Exception("Failed to initialize REAL-TIME Intelligent Face Tracker")

if __name__ == "__main__":
    # Test the REAL-TIME tracker with performance monitoring
    import argparse
    
    parser = argparse.ArgumentParser(description='REAL-TIME Intelligent Face Tracker Test')
    parser.add_argument('--arduino-port', default='/dev/ttyUSB0', help='Arduino port')
    parser.add_argument('--camera-index', type=int, default=0, help='Camera index')
    parser.add_argument('--fps-target', type=int, default=60, help='Target FPS')
    parser.add_argument('--show-camera', action='store_true', help='Show camera display (not headless)')
    args = parser.parse_args()
    
    # Setup logging for performance monitoring
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    headless_mode = not args.show_camera  # Headless by default, unless --show-camera is used
    
    print("🚀 REAL-TIME Intelligent Face Tracker Performance Test")
    print(f"🎯 Target FPS: {args.fps_target}")
    print(f"📹 Display Mode: {'Visible' if not headless_mode else 'Headless (No Window)'}")
    print(f"⚡ Performance optimizations: Frame skipping, predictive tracking, OpenCV fallback")
    print(f"🎪 Testing with Arduino port: {args.arduino_port}, Camera: {args.camera_index}")
    
    try:
        # Create and initialize tracker
        tracker = RealTimeIntelligentFaceTracker(args.arduino_port, args.camera_index, headless=headless_mode)
        tracker.max_tracking_fps = args.fps_target
        tracker.min_loop_time = 1.0 / args.fps_target
        
        if not tracker.initialize():
            print("❌ Failed to initialize tracker")
            exit(1)
        
        print("✅ REAL-TIME tracker initialized successfully!")
        
        # Test voice commands
        test_commands = [
            "look at me",
            "who are you looking at", 
            "search for faces",
            "look left",
            "center your eyes",
            "stop tracking"
        ]
        
        print("\n🎤 Testing voice commands:")
        for cmd in test_commands:
            response = tracker.process_voice_command(cmd)
            print(f"Command: '{cmd}' -> Response: '{response}'")
            time.sleep(0.5)
        
        # Test conversation mode with continuous tracking
        print("\n💬 Testing conversation mode with continuous tracking:")
        tracker.set_conversation_mode(True, "Sophia")
        
        # Simulate conversation stages
        conversation_stages = [
            ConversationStage.LISTENING,
            ConversationStage.PROCESSING,
            ConversationStage.RESPONDING,
            ConversationStage.IDLE
        ]
        
        for stage in conversation_stages:
            print(f"Setting conversation stage: {stage.value}")
            tracker.set_conversation_stage(stage)
            time.sleep(1)
        
        # Start real-time tracking test
        print(f"\n⚡ Starting {args.fps_target} FPS tracking test for 10 seconds...")
        print("💡 TIP: If using --show-camera, position yourself in front of the camera!")
        tracker.start_tracking(conversation_mode=True)
        
        time.sleep(10)  # Run for 10 seconds
        
        # Get final status
        status = tracker.get_status()
        print(f"\n📊 Final Status: {status}")
        
        print("✅ REAL-TIME Performance Test Completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        if 'tracker' in locals():
            tracker.cleanup()
        print("🧹 Test cleanup completed") 