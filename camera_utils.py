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

logger = logging.getLogger(__name__)

class CameraManager:
    """Manages camera operations for the AI Assistant."""
    
    def __init__(self, camera_index: int = 0):
        """Initialize camera manager."""
        self.camera_index = camera_index
        self.camera = None
        self.is_initialized = False
        
        # Create directory for captured images
        self.capture_dir = "captured_images"
        os.makedirs(self.capture_dir, exist_ok=True)
        
        logger.info("CameraManager initialized")
    
    def initialize_camera(self) -> bool:
        """Initialize the camera."""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            # Test if camera is working
            ret, frame = self.camera.read()
            if ret:
                self.is_initialized = True
                logger.info("Camera initialized successfully")
                return True
            else:
                logger.error("Failed to read from camera")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            return False
    
    def capture_image(self, filename: Optional[str] = None) -> Optional[str]:
        """Capture an image from the camera."""
        if not self.is_initialized:
            if not self.initialize_camera():
                return None
        
        try:
            # Capture frame
            ret, frame = self.camera.read()
            if not ret:
                logger.error("Failed to capture image")
                return None
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"
            
            # Save image
            filepath = os.path.join(self.capture_dir, filename)
            cv2.imwrite(filepath, frame)
            
            logger.info(f"Image captured: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return None
    
    def capture_for_analysis(self) -> Optional[np.ndarray]:
        """Capture image and return as numpy array for analysis."""
        if not self.is_initialized:
            if not self.initialize_camera():
                return None
        
        try:
            ret, frame = self.camera.read()
            if ret:
                return frame
            else:
                logger.error("Failed to capture frame for analysis")
                return None
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return None
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode image to base64 for API transmission."""
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded_string
        except Exception as e:
            logger.error(f"Error encoding image: {e}")
            return None
    
    def show_preview(self, duration: int = 5) -> bool:
        """Show camera preview for a few seconds."""
        if not self.is_initialized:
            if not self.initialize_camera():
                return False
        
        try:
            print(f"📸 Showing camera preview for {duration} seconds...")
            print("Press 'q' to quit preview early")
            
            start_time = cv2.getTickCount()
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                # Add text overlay
                cv2.putText(frame, "Camera Preview - Press 'q' to quit", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('Camera Preview', frame)
                
                # Check for quit key or timeout
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
                # Check timeout
                elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                if elapsed > duration:
                    break
            
            cv2.destroyAllWindows()
            return True
            
        except Exception as e:
            logger.error(f"Error showing preview: {e}")
            return False
    
    def test_camera(self) -> bool:
        """Test if camera is working properly."""
        try:
            if not self.initialize_camera():
                return False
            
            # Try to capture a test image
            test_image = self.capture_for_analysis()
            if test_image is not None:
                logger.info("✅ Camera test successful")
                return True
            else:
                logger.error("❌ Camera test failed")
                return False
                
        except Exception as e:
            logger.error(f"Camera test error: {e}")
            return False
    
    def cleanup(self):
        """Clean up camera resources."""
        try:
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            self.is_initialized = False
            logger.info("Camera resources cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up camera: {e}")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass 