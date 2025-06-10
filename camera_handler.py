"""
Simple camera handler for AI Assistant
Provides camera access for math quiz game and other camera-dependent features
"""

import cv2
import logging

logger = logging.getLogger(__name__)

class CameraHandler:
    def __init__(self, camera_index=0):
        """
        Initialize camera handler
        
        Args:
            camera_index: Camera device index (default 0)
        """
        self.camera_index = camera_index
        self.cap = None
        self.is_opened = False
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize the camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if self.cap.isOpened():
                # Set camera properties for optimal performance
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                
                self.is_opened = True
                logger.info(f"✅ Camera {self.camera_index} initialized successfully")
            else:
                logger.warning(f"❌ Failed to open camera {self.camera_index}")
                self.is_opened = False
                
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            self.is_opened = False
    
    def read(self):
        """
        Read a frame from the camera
        
        Returns:
            tuple: (success, frame) - success is bool, frame is numpy array
        """
        if not self.is_opened or self.cap is None:
            return False, None
            
        try:
            ret, frame = self.cap.read()
            return ret, frame
        except Exception as e:
            logger.error(f"Error reading from camera: {e}")
            return False, None
    
    def is_camera_available(self):
        """Check if camera is available and working"""
        return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    def release(self):
        """Release the camera"""
        try:
            if self.cap is not None:
                self.cap.release()
                logger.info("📷 Camera released")
            self.is_opened = False
        except Exception as e:
            logger.error(f"Error releasing camera: {e}")
    
    def __del__(self):
        """Destructor - ensure camera is released"""
        self.release() 