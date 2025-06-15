#!/usr/bin/env python3
"""
Camera utilities for AI Assistant
Handles image capture and processing for object recognition
"""

import cv2
import base64
import logging
import numpy as np
from typing import Optional, Tuple
import os
from datetime import datetime
import time

# Add AITRIOS camera support
try:
    from aitrios_camera_handler import AITRIOSCameraHandler
    AITRIOS_AVAILABLE = True
    logging.info("🤖 AITRIOS AI Camera support detected")
except ImportError:
    AITRIOS_AVAILABLE = False
    logging.info("📷 Using standard camera utilities")

logger = logging.getLogger(__name__)

class CameraManager:
    """Manages camera operations for the AI Assistant."""
    
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        """
        Initialize camera manager with AITRIOS AI Camera support
        
        Args:
            camera_index: Camera index for USB fallback
            width: Frame width
            height: Frame height
            fps: Frame rate
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.using_aitrios = False
        self.aitrios_handler = None
        
        # Create image directory
        self.image_dir = 'captured_images'
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
            
        self.initialize_camera()
        
        logger.info("CameraManager initialized")
    
    def initialize_camera(self) -> bool:
        """Initialize camera - AITRIOS first, then USB fallback"""
        try:
            # Try AITRIOS AI camera first
            if AITRIOS_AVAILABLE:
                logger.info("🤖 Attempting to initialize AITRIOS AI Camera")
                self.aitrios_handler = AITRIOSCameraHandler()
                
                if self.aitrios_handler.is_camera_available():
                    self.using_aitrios = True
                    self.cap = self.aitrios_handler
                    logger.info("✅ AITRIOS AI Camera initialized successfully")
                    return True
                else:
                    logger.warning("⚠️ AITRIOS camera not available, falling back to USB")
            
            # Fallback to USB camera
            logger.info(f"📷 Initializing USB camera {self.camera_index}")
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"❌ Failed to open camera {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            logger.info(f"✅ USB Camera {self.camera_index} initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Camera initialization failed: {e}")
            return False
    
    def capture_image(self, filename: Optional[str] = None) -> Optional[dict]:
        """
        Capture image with AI metadata when using AITRIOS
        
        Args:
            filename: Optional filename, auto-generated if None
            
        Returns:
            dict: Capture result with metadata
        """
        if not self.is_camera_available():
            return {'success': False, 'error': 'Camera not available'}
        
        try:
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"
            
            filepath = os.path.join(self.image_dir, filename)
            
            if self.using_aitrios:
                # Use AITRIOS high-resolution capture with AI metadata
                result = self.aitrios_handler.capture_image_with_ai_metadata(filepath)
                
                if result['success']:
                    logger.info(f"🤖 AITRIOS image captured: {filepath}")
                    
                    # Add AI analysis
                    ai_data = {
                        'objects_detected': result.get('objects', []),
                        'faces_detected': result.get('faces', []),
                        'ai_confidence': result.get('ai_confidence', 0),
                        'camera_type': 'AITRIOS_AI'
                    }
                    
                    return {
                        'success': True,
                        'filepath': filepath,
                        'filename': filename,
                        'ai_metadata': ai_data,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {'success': False, 'error': result.get('error', 'Unknown error')}
            
            else:
                # Standard USB camera capture
                ret, frame = self.cap.read()
                if not ret:
                    return {'success': False, 'error': 'Failed to capture frame'}
                
                # Save image
                success = cv2.imwrite(filepath, frame)
                if success:
                    logger.info(f"📷 USB image captured: {filepath}")
                    return {
                        'success': True,
                        'filepath': filepath,
                        'filename': filename,
                        'camera_type': 'USB',
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {'success': False, 'error': 'Failed to save image'}
                    
        except Exception as e:
            logger.error(f"❌ Image capture failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def read_frame(self):
        """Read frame from camera"""
        if not self.is_camera_available():
            return None, None
        
        try:
            if self.using_aitrios:
                return self.aitrios_handler.read()
            else:
                return self.cap.read()
        except Exception as e:
            logger.error(f"Error reading frame: {e}")
            return False, None
    
    def encode_frame_to_base64(self, frame):
        """Encode frame to base64 string"""
        if frame is None:
            return None
        
        try:
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return img_base64
        except Exception as e:
            logger.error(f"Error encoding frame: {e}")
            return None
    
    def get_ai_detections(self):
        """Get AI detections from AITRIOS camera"""
        if not self.using_aitrios:
            return {'objects': [], 'faces': []}
        
        try:
            objects = self.aitrios_handler.detect_objects()
            faces = self.aitrios_handler.detect_faces()
            
            return {
                'objects': objects,
                'faces': faces,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting AI detections: {e}")
            return {'objects': [], 'faces': []}
    
    def show_preview(self, window_name: str = "Camera Preview"):
        """Show camera preview with AI overlay"""
        if not self.is_camera_available():
            logger.error("Camera not available for preview")
            return
        
        logger.info("Starting camera preview. Press 'q' to quit, 's' to save image")
        
        try:
            while True:
                ret, frame = self.read_frame()
                if not ret or frame is None:
                    break
                
                # Add AI overlay for AITRIOS camera
                if self.using_aitrios:
                    # Get AI detections
                    detections = self.get_ai_detections()
                    
                    # Draw object detections
                    for obj in detections['objects']:
                        bbox = obj.get('bbox', [0, 0, 0, 0])
                        class_name = obj.get('class', 'unknown')
                        confidence = obj.get('confidence', 0)
                        
                        if len(bbox) >= 4:
                            x1, y1, x2, y2 = bbox[:4]
                            # Draw bounding box
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                            # Draw label
                            label = f"{class_name}: {confidence:.2f}"
                            cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Draw face detections
                    for face in detections['faces']:
                        bbox = face.get('bbox', [0, 0, 0, 0])
                        name = face.get('name', 'Unknown')
                        confidence = face.get('confidence', 0)
                        
                        if len(bbox) >= 4:
                            x1, y1, x2, y2 = bbox[:4]
                            # Draw face box
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                            # Draw name
                            label = f"{name}: {confidence:.2f}"
                            cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
                    # Add AI indicator
                    cv2.putText(frame, "🤖 AITRIOS AI", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                cv2.imshow(window_name, frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save current frame
                    result = self.capture_image()
                    if result['success']:
                        print(f"✅ Image saved: {result['filename']}")
                    else:
                        print(f"❌ Failed to save image: {result.get('error', 'Unknown error')}")
                        
        except KeyboardInterrupt:
            logger.info("Preview interrupted by user")
        finally:
            cv2.destroyAllWindows()
    
    def is_camera_available(self) -> bool:
        """Check if camera is available"""
        if self.using_aitrios:
            return self.aitrios_handler and self.aitrios_handler.is_camera_available()
        else:
            return self.cap and self.cap.isOpened()
    
    def get_camera_info(self) -> dict:
        """Get camera information and capabilities"""
        info = {
            'camera_type': 'AITRIOS_AI' if self.using_aitrios else 'USB',
            'available': self.is_camera_available(),
            'width': self.width,
            'height': self.height,
            'fps': self.fps
        }
        
        if self.using_aitrios:
            info.update({
                'ai_features': {
                    'object_detection': True,
                    'face_recognition': True,
                    'pose_detection': True,
                    'high_resolution': True
                },
                'model_info': self.aitrios_handler.get_camera_info() if self.aitrios_handler else {}
            })
        else:
            info.update({
                'ai_features': {
                    'object_detection': False,
                    'face_recognition': False,
                    'pose_detection': False,
                    'high_resolution': False
                }
            })
        
        return info
    
    def test_camera(self) -> bool:
        """Test camera functionality"""
        logger.info("🧪 Testing camera functionality...")
        
        if not self.is_camera_available():
            logger.error("❌ Camera not available")
            return False
        
        # Test frame capture
        ret, frame = self.read_frame()
        if not ret or frame is None:
            logger.error("❌ Failed to capture test frame")
            return False
        
        logger.info(f"✅ Frame capture successful: {frame.shape}")
        
        # Test image capture
        result = self.capture_image("test_capture.jpg")
        if result['success']:
            logger.info(f"✅ Image capture successful: {result['filename']}")
            
            # Show AI capabilities if available
            if self.using_aitrios:
                ai_data = result.get('ai_metadata', {})
                logger.info(f"🤖 AI Objects detected: {len(ai_data.get('objects_detected', []))}")
                logger.info(f"🤖 AI Faces detected: {len(ai_data.get('faces_detected', []))}")
        else:
            logger.error(f"❌ Image capture failed: {result.get('error', 'Unknown error')}")
            return False
        
        logger.info("✅ Camera test completed successfully")
        return True
    
    def release(self):
        """Release camera resources"""
        try:
            if self.using_aitrios and self.aitrios_handler:
                self.aitrios_handler.release()
                logger.info("🤖 AITRIOS camera resources released")
            elif self.cap:
                self.cap.release()
                logger.info("📷 USB camera resources released")
                
            cv2.destroyAllWindows()
        except Exception as e:
            logger.error(f"Error releasing camera: {e}")
    
    def __del__(self):
        """Destructor to ensure proper cleanup"""
        self.release() 