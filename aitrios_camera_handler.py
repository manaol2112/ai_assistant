"""
AITRIOS AI Camera Handler for Raspberry Pi 5
Provides advanced AI camera access with built-in object detection and face recognition
Uses Sony IMX500 sensor with on-board AI processing capabilities
"""

import cv2
import numpy as np
import logging
import time
import os
import json
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import subprocess
import threading
from pathlib import Path
import platform

logger = logging.getLogger(__name__)

# Check if running on Raspberry Pi
IS_RASPBERRY_PI = (
    platform.machine().startswith('arm') or 
    platform.machine().startswith('aarch64') or
    'raspberry' in platform.platform().lower() or
    os.path.exists('/proc/device-tree/model')
)

# Additional check for Raspberry Pi
def _is_raspberry_pi():
    """More thorough check for Raspberry Pi"""
    try:
        # Check /proc/device-tree/model for Pi identification
        if os.path.exists('/proc/device-tree/model'):
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read().lower()
                return 'raspberry pi' in model
    except:
        pass
    
    # Check /proc/cpuinfo
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read().lower()
            return 'raspberry pi' in cpuinfo or 'bcm' in cpuinfo
    except:
        pass
    
    return False

# Update the detection
if not IS_RASPBERRY_PI:
    IS_RASPBERRY_PI = _is_raspberry_pi()

# Try to import required modules for AITRIOS
try:
    if not IS_RASPBERRY_PI:
        # Running on non-Raspberry Pi system (like Mac)
        PICAMERA2_AVAILABLE = False
        print(f"ℹ️ picamera2 is only available on Raspberry Pi systems")
        print(f"Current system: {platform.system()} {platform.machine()}")
    else:
        from picamera2 import Picamera2
        PICAMERA2_AVAILABLE = True
except ImportError as e:
    PICAMERA2_AVAILABLE = False
    if IS_RASPBERRY_PI:
        print("⚠️ Picamera2 not available on Raspberry Pi. Install with: pip install picamera2")
        print(f"Error: {e}")
    else:
        print(f"ℹ️ picamera2 not available on {platform.system()}. This is expected - picamera2 only works on Raspberry Pi.")

# Try to import face recognition
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️ Face recognition not available. Install with: pip install face-recognition")

class AITRIOSCameraHandler:
    """
    Advanced AI Camera Handler for AITRIOS-compatible cameras on Raspberry Pi 5
    Integrates Sony IMX500 AI capabilities with object detection and face recognition
    """
    
    def __init__(self, model_path: str = None, confidence_threshold: float = 0.5):
        """
        Initialize AITRIOS AI Camera Handler
        
        Args:
            model_path: Path to AI model file (uses MobileNet SSD by default)
            confidence_threshold: Minimum confidence for AI detections
        """
        self.logger = logging.getLogger(__name__)
        self.picam2 = None
        self.is_opened = False
        self.is_ai_enabled = False
        self.confidence_threshold = confidence_threshold
        
        # AI Detection capabilities
        self.ai_results = {}
        self.last_ai_detection = None
        self.ai_thread = None
        self.ai_running = False
        
        # Default model paths for IMX500
        self.model_paths = {
            'object_detection': '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk',
            'pose_detection': '/usr/share/rpi-camera-assets/imx500_posenet.json',
            'mobilenet_ssd': '/usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json'
        }
        
        # Face recognition setup
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_recognition_enabled = FACE_RECOGNITION_AVAILABLE
        
        # Camera configuration
        self.frame_width = 1920
        self.frame_height = 1080
        self.framerate = 30
        
        # Image capture directory
        self.capture_dir = "captured_images"
        os.makedirs(self.capture_dir, exist_ok=True)
        
        self._initialize_camera()
        
        if self.face_recognition_enabled:
            self.load_known_faces()
    
    def _initialize_camera(self):
        """Initialize the AITRIOS AI Camera"""
        try:
            if not PICAMERA2_AVAILABLE:
                if not IS_RASPBERRY_PI:
                    self.logger.info(f"🖥️ Running on {platform.system()} {platform.machine()}")
                    self.logger.info("ℹ️ AITRIOS AI Camera is only available on Raspberry Pi systems")
                    self.logger.info("💡 The main camera handler will automatically fallback to USB camera")
                else:
                    self.logger.error("Picamera2 not available on Raspberry Pi. Install with: pip install picamera2")
                return False
            
            # Check if IMX500 firmware is available
            if not self._check_imx500_firmware():
                self.logger.warning("IMX500 firmware not found. AI features may not work.")
            
            # Initialize Picamera2 for IMX500
            self.picam2 = Picamera2()
            
            # Configure camera for AI processing
            config = self.picam2.create_video_configuration(
                main={"size": (self.frame_width, self.frame_height), "format": "RGB888"},
                lores={"size": (320, 240), "format": "YUV420"}
            )
            
            # Add IMX500 post-processing if available
            if os.path.exists(self.model_paths['mobilenet_ssd']):
                config["post_process_file"] = self.model_paths['mobilenet_ssd']
                self.is_ai_enabled = True
                self.logger.info("✅ AI processing enabled with MobileNet SSD")
            
            self.picam2.configure(config)
            self.picam2.start()
            
            # Wait for camera to settle
            time.sleep(2)
            
            self.is_opened = True
            self.logger.info("✅ AITRIOS AI Camera initialized successfully")
            
            # Start AI processing thread
            if self.is_ai_enabled:
                self._start_ai_processing()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing AITRIOS camera: {e}")
            self.is_opened = False
            return False
    
    def _check_imx500_firmware(self) -> bool:
        """Check if IMX500 firmware is installed"""
        try:
            result = subprocess.run(['dpkg', '-l', 'imx500-all'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def load_known_faces(self):
        """Load known faces from the people directory for AI-enhanced recognition."""
        if not self.face_recognition_enabled:
            return
        
        people_dir = "people"
        if not os.path.exists(people_dir):
            self.logger.warning(f"People directory '{people_dir}' not found")
            return
        
        self.logger.info("👤 Loading known faces for AI camera...")
        
        for person_name in os.listdir(people_dir):
            person_path = os.path.join(people_dir, person_name)
            if not os.path.isdir(person_path):
                continue
            
            self.logger.info(f"   Loading faces for {person_name.title()}...")
            person_encodings = []
            
            for image_file in os.listdir(person_path):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(person_path, image_file)
                    
                    try:
                        image = face_recognition.load_image_file(image_path)
                        encodings = face_recognition.face_encodings(image)
                        
                        if encodings:
                            person_encodings.extend(encodings)
                            self.logger.info(f"     ✅ Loaded {len(encodings)} face(s) from {image_file}")
                        else:
                            self.logger.info(f"     ⚠️ No face found in {image_file}")
                    
                    except Exception as e:
                        self.logger.error(f"     ❌ Error loading {image_file}: {e}")
            
            if person_encodings:
                self.known_face_encodings.extend(person_encodings)
                self.known_face_names.extend([person_name] * len(person_encodings))
                self.logger.info(f"   ✅ Total {len(person_encodings)} face encodings loaded for {person_name.title()}")
        
        self.logger.info(f"🎉 AI Face recognition ready! Loaded {len(self.known_face_names)} encodings")
    
    def _start_ai_processing(self):
        """Start AI processing thread for continuous object detection"""
        if self.ai_running:
            return
        
        self.ai_running = True
        self.ai_thread = threading.Thread(target=self._ai_processing_loop, daemon=True)
        self.ai_thread.start()
        self.logger.info("🤖 AI processing thread started")
    
    def _ai_processing_loop(self):
        """Continuous AI processing loop"""
        while self.ai_running and self.is_opened:
            try:
                if self.picam2:
                    # Get AI metadata if available
                    metadata = self.picam2.capture_metadata()
                    
                    if 'nn_results' in metadata:
                        self.ai_results = self._process_ai_results(metadata['nn_results'])
                        self.last_ai_detection = time.time()
                
                time.sleep(0.1)  # 10 FPS for AI processing
                
            except Exception as e:
                self.logger.error(f"Error in AI processing loop: {e}")
                time.sleep(1)
    
    def _process_ai_results(self, nn_results) -> Dict[str, Any]:
        """Process neural network results from IMX500"""
        try:
            processed_results = {
                'objects': [],
                'faces': [],
                'timestamp': time.time()
            }
            
            # Process object detections
            if isinstance(nn_results, list):
                for detection in nn_results:
                    if detection.get('confidence', 0) > self.confidence_threshold:
                        processed_results['objects'].append({
                            'class': detection.get('class', 'unknown'),
                            'confidence': detection.get('confidence', 0),
                            'bbox': detection.get('bbox', [0, 0, 0, 0])
                        })
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Error processing AI results: {e}")
            return {'objects': [], 'faces': [], 'timestamp': time.time()}
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the AI camera
        
        Returns:
            tuple: (success, frame) - success is bool, frame is numpy array
        """
        if not self.is_opened or not self.picam2:
            return False, None
        
        try:
            # Capture array from picamera2
            frame = self.picam2.capture_array()
            
            # Convert from RGB to BGR for OpenCV compatibility
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            return True, frame
            
        except Exception as e:
            self.logger.error(f"Error reading from AITRIOS camera: {e}")
            return False, None
    
    def capture_image(self, filename: Optional[str] = None) -> Optional[str]:
        """Capture high-resolution image with AI metadata"""
        if not self.is_opened:
            return None
        
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"aitrios_capture_{timestamp}.jpg"
            
            filepath = os.path.join(self.capture_dir, filename)
            
            # Capture high-resolution image
            self.picam2.capture_file(filepath)
            
            # Save AI metadata if available
            if self.ai_results:
                metadata_file = filepath.replace('.jpg', '_ai_data.json')
                with open(metadata_file, 'w') as f:
                    json.dump(self.ai_results, f, indent=2)
            
            self.logger.info(f"📸 AITRIOS image captured: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error capturing AITRIOS image: {e}")
            return None
    
    def detect_objects(self, frame: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """Get current AI object detection results"""
        if not self.is_ai_enabled:
            return []
        
        # Return cached AI results from IMX500
        if self.ai_results and 'objects' in self.ai_results:
            return self.ai_results['objects']
        
        return []
    
    def detect_faces(self, frame: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """Enhanced face detection using AI camera + face recognition"""
        if not self.face_recognition_enabled:
            return []
        
        try:
            if frame is None:
                ret, frame = self.read()
                if not ret or frame is None:
                    return []
            
            # Resize for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find faces
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            face_detections = []
            
            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                
                name = "Unknown"
                confidence = 0.0
                
                if any(matches):
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1.0 - face_distances[best_match_index]
                
                # Scale back up face locations
                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                face_detections.append({
                    'name': name,
                    'confidence': confidence,
                    'bbox': (left, top, right, bottom),
                    'location': (top, right, bottom, left)
                })
            
            return face_detections
            
        except Exception as e:
            self.logger.error(f"Error in AI face detection: {e}")
            return []
    
    def get_ai_status(self) -> Dict[str, Any]:
        """Get current AI processing status"""
        return {
            'ai_enabled': self.is_ai_enabled,
            'face_recognition': self.face_recognition_enabled,
            'known_faces': len(set(self.known_face_names)),
            'last_detection': self.last_ai_detection,
            'processing_active': self.ai_running
        }
    
    def show_preview(self, duration: int = 5) -> bool:
        """Show AI camera preview with overlays"""
        if not self.is_opened:
            return False
        
        try:
            print(f"🤖 AITRIOS AI Camera Preview - {duration}s")
            print("Press 'q' to quit, 'd' to toggle detections")
            
            show_detections = True
            start_time = time.time()
            
            while time.time() - start_time < duration:
                ret, frame = self.read()
                if not ret:
                    break
                
                if show_detections:
                    # Overlay AI detections
                    objects = self.detect_objects(frame)
                    faces = self.detect_faces(frame)
                    
                    # Draw object detections
                    for obj in objects:
                        bbox = obj.get('bbox', [0, 0, 0, 0])
                        if len(bbox) == 4:
                            x1, y1, x2, y2 = bbox
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                            label = f"{obj.get('class', 'object')}: {obj.get('confidence', 0):.2f}"
                            cv2.putText(frame, label, (int(x1), int(y1)-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    # Draw face detections
                    for face in faces:
                        bbox = face.get('bbox', [0, 0, 0, 0])
                        if len(bbox) == 4:
                            x1, y1, x2, y2 = bbox
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            label = f"{face.get('name', 'Unknown')}: {face.get('confidence', 0):.2f}"
                            cv2.putText(frame, label, (x1, y1-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                
                # Add AI status overlay
                status_text = f"AI: {'ON' if self.is_ai_enabled else 'OFF'} | Faces: {len(set(self.known_face_names))}"
                cv2.putText(frame, status_text, (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                cv2.imshow('AITRIOS AI Camera Preview', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('d'):
                    show_detections = not show_detections
            
            cv2.destroyAllWindows()
            return True
            
        except Exception as e:
            self.logger.error(f"Error showing AI preview: {e}")
            return False
    
    def is_camera_available(self) -> bool:
        """Check if AI camera is available and working"""
        return self.is_opened and self.picam2 is not None
    
    def release(self):
        """Release AI camera resources"""
        try:
            # Stop AI processing
            self.ai_running = False
            if self.ai_thread and self.ai_thread.is_alive():
                self.ai_thread.join(timeout=2)
            
            # Release camera
            if self.picam2:
                self.picam2.stop()
                self.picam2.close()
                self.picam2 = None
            
            cv2.destroyAllWindows()
            self.is_opened = False
            self.logger.info("🤖 AITRIOS AI Camera released")
            
        except Exception as e:
            self.logger.error(f"Error releasing AITRIOS camera: {e}")
    
    def __del__(self):
        """Destructor - ensure camera is released"""
        try:
            self.release()
        except:
            pass 