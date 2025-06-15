#!/usr/bin/env python3
"""
Sony IMX500 AI Camera Handler for Raspberry Pi 5
Uses libcamera system directly instead of picamera2
Leverages the native IMX500 AI capabilities through libcamera commands
"""

import cv2
import numpy as np
import logging
import time
import os
import json
import subprocess
import threading
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import tempfile
import signal

logger = logging.getLogger(__name__)

class IMX500CameraHandler:
    """
    Sony IMX500 AI Camera Handler using libcamera system
    Works directly with libcamera commands for maximum compatibility
    """
    
    def __init__(self, width: int = 1920, height: int = 1080, framerate: int = 30):
        """
        Initialize IMX500 Camera Handler
        
        Args:
            width: Frame width (default 1920)
            height: Frame height (default 1080) 
            framerate: Frames per second (default 30)
        """
        self.logger = logging.getLogger(__name__)
        self.width = width
        self.height = height
        self.framerate = framerate
        
        # Camera state
        self.is_opened = False
        self.is_streaming = False
        self.capture_process = None
        
        # AI capabilities
        self.ai_enabled = False
        self.ai_model_loaded = False
        
        # Streaming setup
        self.stream_file = None
        self.frame_buffer = None
        self.last_frame = None
        self.frame_lock = threading.Lock()
        
        # Image capture directory
        self.capture_dir = "captured_images"
        os.makedirs(self.capture_dir, exist_ok=True)
        
        # Check camera availability
        self._check_camera_availability()
        
        if self.is_opened:
            self._initialize_streaming()
    
    def _check_camera_availability(self):
        """Check if IMX500 camera is available using libcamera"""
        try:
            self.logger.info("🔍 Checking Sony IMX500 camera availability...")
            
            # First, try a quick camera list check
            result = subprocess.run([
                'libcamera-hello', '--list-cameras'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                output = result.stdout.lower()
                if 'imx500' in output or 'sony' in output or 'available cameras' in output:
                    self.logger.info("✅ Camera detected in list")
                    
                    # Verify with a quick test capture
                    if self._verify_camera_with_test():
                        self.is_opened = True
                        self.ai_enabled = True
                        self.logger.info("✅ Sony IMX500 camera verified and ready")
                        return
                    else:
                        self.logger.warning("⚠️ Camera listed but test capture failed")
                else:
                    self.logger.warning("⚠️ No IMX500 camera found in list")
                    self.logger.debug(f"Camera list output: {result.stdout}")
            else:
                self.logger.error(f"❌ libcamera-hello failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Camera detection timeout")
        except FileNotFoundError:
            self.logger.error("❌ libcamera-hello not found. Install libcamera-apps")
        except Exception as e:
            self.logger.error(f"❌ Camera detection error: {e}")
        
        # If we get here, camera is not available
        self.is_opened = False
        self.ai_enabled = False
    
    def _verify_camera_with_test(self) -> bool:
        """Verify camera works with a quick test capture"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Quick test with minimal parameters
            cmd = ['libcamera-still', '-o', temp_path, '--timeout', '1000']
            
            self.logger.debug("🧪 Testing camera with quick capture...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
            
            success = result.returncode == 0 and os.path.exists(temp_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            
            if success:
                self.logger.debug("✅ Camera test capture successful")
            else:
                self.logger.debug(f"❌ Camera test failed: {result.stderr}")
            
            return success
            
        except Exception as e:
            self.logger.debug(f"❌ Camera test exception: {e}")
            return False
    
    def _initialize_streaming(self):
        """Initialize video streaming using libcamera-vid"""
        try:
            # Create temporary file for streaming
            self.stream_file = tempfile.NamedTemporaryFile(suffix='.h264', delete=False)
            self.stream_file.close()
            
            self.logger.info("🎥 Initializing IMX500 video streaming...")
            
        except Exception as e:
            self.logger.error(f"Error initializing streaming: {e}")
    
    def start_streaming(self):
        """Start continuous video streaming"""
        if self.is_streaming:
            return True
            
        try:
            # Start libcamera-vid for continuous capture
            cmd = [
                'libcamera-vid',
                '--width', str(self.width),
                '--height', str(self.height),
                '--framerate', str(self.framerate),
                '--timeout', '0',  # Continuous
                '--output', self.stream_file.name,
                '--flush',
                '--inline'
            ]
            
            # Add AI model if available
            ai_model_path = '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk'
            if os.path.exists(ai_model_path):
                cmd.extend(['--post-process-file', ai_model_path])
                self.ai_model_loaded = True
                self.logger.info("🧠 AI model loaded for object detection")
            
            self.logger.info(f"🚀 Starting streaming: {' '.join(cmd)}")
            
            self.capture_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            # Give it time to start
            time.sleep(2)
            
            if self.capture_process.poll() is None:
                self.is_streaming = True
                self.logger.info("✅ IMX500 streaming started")
                return True
            else:
                stderr = self.capture_process.stderr.read().decode()
                self.logger.error(f"❌ Streaming failed: {stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting streaming: {e}")
            return False
    
    def stop_streaming(self):
        """Stop video streaming"""
        if not self.is_streaming:
            return
            
        try:
            if self.capture_process:
                # Send SIGTERM to process group
                os.killpg(os.getpgid(self.capture_process.pid), signal.SIGTERM)
                
                # Wait for process to end
                try:
                    self.capture_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    os.killpg(os.getpgid(self.capture_process.pid), signal.SIGKILL)
                    self.capture_process.wait()
                
                self.capture_process = None
            
            self.is_streaming = False
            self.logger.info("🛑 IMX500 streaming stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping streaming: {e}")
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Capture a single frame from the IMX500 camera
        
        Returns:
            tuple: (success, frame) - success is bool, frame is numpy array
        """
        if not self.is_opened:
            self.logger.error("Camera not opened")
            return False, None
            
        # Try multiple capture methods in order of preference
        capture_methods = [
            self._capture_with_basic_still,
            self._capture_with_minimal_still,
            self._capture_with_fallback_still
        ]
        
        for i, method in enumerate(capture_methods):
            try:
                self.logger.debug(f"Trying capture method {i+1}/3: {method.__name__}")
                success, frame = method()
                if success and frame is not None:
                    self.logger.debug(f"✅ Capture successful with method {i+1}")
                    return True, frame
                else:
                    self.logger.debug(f"❌ Method {i+1} failed")
            except Exception as e:
                self.logger.debug(f"❌ Method {i+1} exception: {e}")
                continue
        
        self.logger.error("All capture methods failed")
        return False, None
    
    def _capture_with_basic_still(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Basic libcamera-still capture"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            cmd = [
                'libcamera-still',
                '--output', temp_path,
                '--timeout', '2000',
                '--nopreview'
            ]
            
            self.logger.debug(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and os.path.exists(temp_path):
                frame = cv2.imread(temp_path)
                os.unlink(temp_path)
                if frame is not None:
                    return True, frame
            else:
                self.logger.debug(f"Basic still failed: {result.stderr}")
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
            return False, None
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
    
    def _capture_with_minimal_still(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Minimal libcamera-still capture with shortest timeout"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            cmd = [
                'libcamera-still',
                '--output', temp_path,
                '--timeout', '1000'  # Shorter timeout
            ]
            
            self.logger.debug(f"Running minimal: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and os.path.exists(temp_path):
                frame = cv2.imread(temp_path)
                os.unlink(temp_path)
                if frame is not None:
                    return True, frame
            else:
                self.logger.debug(f"Minimal still failed: {result.stderr}")
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
            return False, None
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
    
    def _capture_with_fallback_still(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Fallback capture with very basic parameters"""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Most basic command possible
            cmd = ['libcamera-still', '-o', temp_path]
            
            self.logger.debug(f"Running fallback: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
            
            if result.returncode == 0 and os.path.exists(temp_path):
                frame = cv2.imread(temp_path)
                os.unlink(temp_path)
                if frame is not None:
                    return True, frame
            else:
                self.logger.debug(f"Fallback still failed: {result.stderr}")
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
            return False, None
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
    
    def capture_image(self, filename: Optional[str] = None) -> Optional[str]:
        """Capture high-resolution image with AI metadata"""
        if not self.is_opened:
            self.logger.error("Camera not opened for image capture")
            return None
            
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"imx500_capture_{timestamp}.jpg"
            
            filepath = os.path.join(self.capture_dir, filename)
            
            # Try multiple capture methods for image capture
            capture_methods = [
                lambda: self._capture_image_with_ai(filepath),
                lambda: self._capture_image_basic(filepath),
                lambda: self._capture_image_minimal(filepath)
            ]
            
            for i, method in enumerate(capture_methods):
                try:
                    self.logger.debug(f"Trying image capture method {i+1}/3")
                    if method():
                        self.logger.info(f"📸 IMX500 image captured: {filepath}")
                        return filepath
                    else:
                        self.logger.debug(f"Image capture method {i+1} failed")
                except Exception as e:
                    self.logger.debug(f"Image capture method {i+1} exception: {e}")
                    continue
            
            self.logger.error("All image capture methods failed")
            return None
                
        except Exception as e:
            self.logger.error(f"Error in capture_image: {e}")
            return None
    
    def _capture_image_with_ai(self, filepath: str) -> bool:
        """Capture image with AI model if available"""
        try:
            cmd = [
                'libcamera-still',
                '--output', filepath,
                '--timeout', '3000',
                '--nopreview'
            ]
            
            # Add AI model if available
            ai_model_path = '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk'
            if os.path.exists(ai_model_path):
                cmd.extend(['--post-process-file', ai_model_path])
                self.logger.debug("🧠 Using AI model for image capture")
            
            self.logger.debug(f"Running AI capture: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            
            return result.returncode == 0 and os.path.exists(filepath)
            
        except Exception as e:
            self.logger.debug(f"AI capture failed: {e}")
            return False
    
    def _capture_image_basic(self, filepath: str) -> bool:
        """Basic image capture without AI"""
        try:
            cmd = [
                'libcamera-still',
                '--output', filepath,
                '--timeout', '2000',
                '--nopreview'
            ]
            
            self.logger.debug(f"Running basic capture: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            return result.returncode == 0 and os.path.exists(filepath)
            
        except Exception as e:
            self.logger.debug(f"Basic capture failed: {e}")
            return False
    
    def _capture_image_minimal(self, filepath: str) -> bool:
        """Minimal image capture with shortest parameters"""
        try:
            cmd = ['libcamera-still', '-o', filepath]
            
            self.logger.debug(f"Running minimal capture: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            return result.returncode == 0 and os.path.exists(filepath)
            
        except Exception as e:
            self.logger.debug(f"Minimal capture failed: {e}")
            return False
    
    def detect_objects(self, frame: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """
        Get AI object detection results from IMX500
        Note: This requires the AI model to be loaded and running
        """
        if not self.ai_enabled or not self.ai_model_loaded:
            return []
        
        # For now, return empty list as AI results need to be parsed from libcamera output
        # This would need to be implemented based on the specific AI model output format
        return []
    
    def show_preview(self, duration: int = 5) -> bool:
        """Show camera preview using libcamera-hello"""
        if not self.is_opened:
            return False
            
        try:
            self.logger.info(f"🖥️ Starting IMX500 preview for {duration} seconds...")
            
            # Use simpler command for better compatibility
            cmd = [
                'libcamera-hello',
                '--timeout', str(duration * 1000)  # Convert to milliseconds
            ]
            
            # Add AI model if available (optional)
            ai_model_path = '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk'
            if os.path.exists(ai_model_path):
                cmd.extend(['--post-process-file', ai_model_path])
                self.logger.info("🧠 Preview with AI overlay enabled")
            else:
                self.logger.info("📷 Preview without AI overlay")
            
            self.logger.debug(f"🖥️ Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, timeout=duration + 10)
            
            if result.returncode == 0:
                self.logger.info("✅ Preview completed successfully")
                return True
            else:
                error_msg = result.stderr.decode() if result.stderr else "Unknown error"
                self.logger.error(f"Preview failed (code {result.returncode}): {error_msg}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.warning("Preview timeout - this is normal")
            return True  # Timeout is expected for preview
        except Exception as e:
            self.logger.error(f"Error showing preview: {e}")
            return False
    
    def get_ai_status(self) -> Dict[str, Any]:
        """Get current AI processing status"""
        return {
            'ai_enabled': self.ai_enabled,
            'ai_model_loaded': self.ai_model_loaded,
            'camera_available': self.is_opened,
            'streaming': self.is_streaming,
            'resolution': f"{self.width}x{self.height}",
            'framerate': self.framerate
        }
    
    def is_camera_available(self) -> bool:
        """Check if IMX500 camera is available"""
        return self.is_opened
    
    def release(self):
        """Release camera resources"""
        try:
            self.stop_streaming()
            
            # Clean up temp files
            if self.stream_file and os.path.exists(self.stream_file.name):
                os.unlink(self.stream_file.name)
            
            self.is_opened = False
            self.logger.info("📷 IMX500 Camera released")
            
        except Exception as e:
            self.logger.error(f"Error releasing camera: {e}")
    
    def __del__(self):
        """Destructor - ensure camera is released"""
        try:
            self.release()
        except:
            pass 