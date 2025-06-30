"""
Enhanced Camera Handler for AI Assistant with Sony IMX500 AI Camera Support
Provides camera access with AI capabilities when available, USB fallback otherwise
Optimized for Raspberry Pi 5 with Sony IMX500 AI Camera using libcamera system
"""

import cv2
import logging
import time
from typing import Optional, List, Dict, Any, Tuple

# Try to import IMX500 handler (uses libcamera, not picamera2)
try:
    from imx500_camera_handler import IMX500CameraHandler
    IMX500_AVAILABLE = True
except ImportError:
    IMX500_AVAILABLE = False

logger = logging.getLogger(__name__)

class CameraHandler:
    def __init__(self, camera_index=0, prefer_imx500=True):
        """
        Initialize enhanced camera handler with AI capabilities
        
        Args:
            camera_index: Camera device index for USB fallback (default 0)
            prefer_imx500: Try Sony IMX500 AI camera first (default True)
        """
        self.camera_index = camera_index
        self.prefer_imx500 = prefer_imx500
        self.cap = None
        self.imx500_handler = None
        self.is_opened = False
        self.using_imx500 = False
        self.ai_features_available = False
        
        # Track AI capabilities
        self.face_detection_available = False
        self.object_detection_available = False
        
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize camera with Sony IMX500 AI support or USB fallback"""
        # First try Sony IMX500 AI Camera if available and preferred
        if self.prefer_imx500 and IMX500_AVAILABLE:
            try:
                logger.info("🤖 Attempting to initialize Sony IMX500 AI Camera...")
                self.imx500_handler = IMX500CameraHandler(width=1920, height=1080, framerate=30)
                
                if self.imx500_handler.is_camera_available():
                    self.using_imx500 = True
                    self.is_opened = True
                    self.ai_features_available = True
                    
                    # Check AI capabilities
                    ai_status = self.imx500_handler.get_ai_status()
                    self.object_detection_available = ai_status.get('ai_enabled', False)
                    
                    logger.info("✅ Sony IMX500 AI Camera initialized successfully")
                    logger.info(f"   🎯 Object Detection: {'✅' if self.object_detection_available else '❌'}")
                    logger.info(f"   🧠 AI Model: {'✅' if ai_status.get('ai_model_loaded', False) else '❌'}")
                    logger.info(f"   📐 Resolution: {ai_status.get('resolution', 'Unknown')}")
                    return
                    
            except Exception as e:
                logger.warning(f"Failed to initialize Sony IMX500 camera: {e}")
                self.imx500_handler = None
        
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
                self.using_imx500 = False
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
            if self.using_imx500 and self.imx500_handler:
                return self.imx500_handler.read()
            elif self.cap is not None:
                ret, frame = self.cap.read()
                return ret, frame
            else:
                return False, None
        except Exception as e:
            logger.error(f"Error reading from camera: {e}")
            return False, None
    
    def capture_image(self, filename: Optional[str] = None) -> Optional[str]:
        """Capture high-resolution image with AI metadata if available"""
        if not self.is_opened:
            return None
            
        try:
            if self.using_imx500 and self.imx500_handler:
                return self.imx500_handler.capture_image(filename)
            else:
                # Fallback for USB camera
                ret, frame = self.read()
                if ret and frame is not None:
                    if not filename:
                        from datetime import datetime
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"usb_capture_{timestamp}.jpg"
                    
                    import os
                    capture_dir = "captured_images"
                    os.makedirs(capture_dir, exist_ok=True)
                    filepath = os.path.join(capture_dir, filename)
                    
                    if cv2.imwrite(filepath, frame):
                        logger.info(f"📸 USB camera image captured: {filepath}")
                        return filepath
                
                return None
                
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return None
    
    def detect_objects(self, frame: Optional = None) -> List[Dict[str, Any]]:
        """Get AI object detection results if available"""
        if self.using_imx500 and self.imx500_handler and self.object_detection_available:
            return self.imx500_handler.detect_objects(frame)
        else:
            return []
    
    def show_preview(self, duration: int = 5, headless: bool = False) -> bool:
        """Show camera preview with AI overlays if available"""
        if not self.is_opened:
            return False
            
        try:
            if self.using_imx500 and self.imx500_handler:
                return self.imx500_handler.show_preview(duration)
            else:
                # Fallback preview for USB camera
                if headless:
                    logger.info(f"📷 USB Camera running in headless mode for {duration}s")
                    time.sleep(duration)  # Just wait without showing window
                    return True
                
                logger.info(f"📷 USB Camera Preview - {duration}s (Press 'q' to quit)")
                start_time = time.time()
                
                while time.time() - start_time < duration:
                    ret, frame = self.read()
                    if not ret:
                        break
                    
                    # Add status overlay
                    cv2.putText(frame, "USB Camera (No AI)", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    cv2.imshow('USB Camera Preview', frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                cv2.destroyAllWindows()
                return True
                
        except Exception as e:
            logger.error(f"Error showing preview: {e}")
            return False
    
    def get_ai_status(self) -> Dict[str, Any]:
        """Get current AI processing status"""
        if self.using_imx500 and self.imx500_handler:
            return self.imx500_handler.get_ai_status()
        else:
            return {
                'ai_enabled': False,
                'camera_type': 'USB',
                'ai_features_available': False
            }
    
    def is_camera_available(self):
        """Check if camera is available and working"""
        if self.using_imx500 and self.imx500_handler:
            return self.imx500_handler.is_camera_available()
        else:
            return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    def release(self):
        """Release camera resources"""
        try:
            if self.using_imx500 and self.imx500_handler:
                self.imx500_handler.release()
                self.imx500_handler = None
            
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