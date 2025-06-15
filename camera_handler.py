"""
Enhanced Camera Handler for AI Assistant with AITRIOS AI Camera Support
Provides camera access with AI capabilities when available, USB fallback otherwise
Optimized for Raspberry Pi 5 with Sony IMX500 AITRIOS AI Camera
"""

import cv2
import logging
import time
from typing import Optional, List, Dict, Any, Tuple

# Try to import AITRIOS handler
try:
    from aitrios_camera_handler import AITRIOSCameraHandler
    AITRIOS_AVAILABLE = True
except ImportError:
    AITRIOS_AVAILABLE = False

logger = logging.getLogger(__name__)

class CameraHandler:
    def __init__(self, camera_index=0, prefer_aitrios=True):
        """
        Initialize enhanced camera handler with AI capabilities
        
        Args:
            camera_index: Camera device index for USB fallback (default 0)
            prefer_aitrios: Try AITRIOS AI camera first (default True)
        """
        self.camera_index = camera_index
        self.prefer_aitrios = prefer_aitrios
        self.cap = None
        self.aitrios_handler = None
        self.is_opened = False
        self.using_aitrios = False
        self.ai_features_available = False
        
        # Track AI capabilities
        self.face_detection_available = False
        self.object_detection_available = False
        
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize camera with AITRIOS AI support or USB fallback"""
        # First try AITRIOS AI Camera if available and preferred
        if self.prefer_aitrios and AITRIOS_AVAILABLE:
            try:
                logger.info("🤖 Attempting to initialize AITRIOS AI Camera...")
                self.aitrios_handler = AITRIOSCameraHandler(confidence_threshold=0.5)
                
                if self.aitrios_handler.is_camera_available():
                    self.using_aitrios = True
                    self.is_opened = True
                    self.ai_features_available = True
                    
                    # Check AI capabilities
                    ai_status = self.aitrios_handler.get_ai_status()
                    self.face_detection_available = ai_status.get('face_recognition', False)
                    self.object_detection_available = ai_status.get('ai_enabled', False)
                    
                    logger.info("✅ AITRIOS AI Camera initialized successfully")
                    logger.info(f"   🎯 Object Detection: {'✅' if self.object_detection_available else '❌'}")
                    logger.info(f"   👤 Face Recognition: {'✅' if self.face_detection_available else '❌'}")
                    logger.info(f"   🧠 Known Faces: {ai_status.get('known_faces', 0)}")
                    return
                    
            except Exception as e:
                logger.warning(f"Failed to initialize AITRIOS camera: {e}")
                self.aitrios_handler = None
        
        # Fallback to USB camera
        self._initialize_usb_camera()
    
    def _initialize_usb_camera(self):
        """Initialize USB camera as fallback"""
        try:
            logger.info(f"📷 Initializing USB camera (index: {self.camera_index})...")
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if self.cap.isOpened():
                # Set camera properties for optimal performance
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                
                self.is_opened = True
                self.using_aitrios = False
                self.ai_features_available = False
                logger.info(f"✅ USB Camera {self.camera_index} initialized successfully")
                logger.info("   ⚠️ AI features not available with USB camera")
            else:
                logger.warning(f"❌ Failed to open USB camera {self.camera_index}")
                self.is_opened = False
                
        except Exception as e:
            logger.error(f"Error initializing USB camera: {e}")
            self.is_opened = False
    
    def read(self):
        """
        Read a frame from the camera (AI or USB)
        
        Returns:
            tuple: (success, frame) - success is bool, frame is numpy array
        """
        if not self.is_opened:
            return False, None
            
        try:
            if self.using_aitrios and self.aitrios_handler:
                return self.aitrios_handler.read()
            elif self.cap is not None:
                ret, frame = self.cap.read()
                return ret, frame
            else:
                return False, None
        except Exception as e:
            logger.error(f"Error reading from camera: {e}")
            return False, None
    
    def is_camera_available(self):
        """Check if camera is available and working"""
        if self.using_aitrios and self.aitrios_handler:
            return self.aitrios_handler.is_camera_available()
        else:
            return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    def release(self):
        """Release camera resources"""
        try:
            if self.using_aitrios and self.aitrios_handler:
                self.aitrios_handler.release()
                self.aitrios_handler = None
            
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            
            self.is_opened = False
            logger.info("📷 Camera released")
        except Exception as e:
            logger.error(f"Error releasing camera: {e}")
    
    def __del__(self):
        """Destructor - ensure camera is released"""
        try:
            self.release()
        except:
            pass 