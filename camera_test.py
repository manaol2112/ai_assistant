# Enhanced camera_test.py with V4L2 fixes
#!/usr/bin/env python3
"""
Enhanced Camera Diagnostic for Raspberry Pi with V4L2 Backend Fixes
Tests multiple camera backends and indices with specific V4L2 troubleshooting
"""

import cv2
import os
import subprocess
import sys
import time

def check_v4l2_devices():
    """Check V4L2 devices specifically"""
    print("\n🔧 V4L2 DEVICE ANALYSIS:")
    
    # Check v4l2-ctl availability
    try:
        result = subprocess.run(['which', 'v4l2-ctl'], capture_output=True, text=True)
        if result.returncode != 0:
            print("  ⚠️ v4l2-ctl not found. Install with: sudo apt install v4l-utils")
            return []
        
        print("  ✅ v4l2-ctl found")
        
        # List all video devices with v4l2-ctl
        devices = []
        for i in range(10):
            device_path = f"/dev/video{i}"
            if os.path.exists(device_path):
                try:
                    result = subprocess.run(['v4l2-ctl', '--device', device_path, '--info'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"  📹 {device_path}:")
                        # Parse device info
                        for line in result.stdout.split('\n'):
                            if 'Card type' in line or 'Bus info' in line or 'Driver name' in line:
                                print(f"      {line.strip()}")
                        devices.append(i)
                    else:
                        print(f"  ❌ {device_path}: Cannot query device")
                except subprocess.TimeoutExpired:
                    print(f"  ⏱️ {device_path}: Query timeout")
                except Exception as e:
                    print(f"  ❌ {device_path}: Error - {e}")
        
        return devices
        
    except Exception as e:
        print(f"  ❌ V4L2 check failed: {e}")
        return []

def test_camera_with_backend_fallback(camera_index):
    """Test camera with multiple backend fallbacks"""
    print(f"\n🎯 Testing Camera {camera_index} with Backend Fallback:")
    
    # Define backends in order of preference for Raspberry Pi
    backends = [
        (cv2.CAP_GSTREAMER, "GStreamer"),  # Often works better on Pi
        (cv2.CAP_V4L2, "V4L2"),            # Linux standard
        (cv2.CAP_FFMPEG, "FFmpeg"),        # Alternative
        (cv2.CAP_ANY, "Any")               # Let OpenCV decide
    ]
    
    working_backends = []
    
    for backend_id, backend_name in backends:
        try:
            print(f"  🔧 Trying {backend_name}...")
            
            # Initialize with specific backend
            cap = cv2.VideoCapture(camera_index, backend_id)
            
            if cap.isOpened():
                # Set properties before testing
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS for stability
                
                # Wait a moment for camera to initialize
                time.sleep(0.5)
                
                # Try to read multiple frames
                success_count = 0
                for attempt in range(3):
                    ret, frame = cap.read()
                    if ret and frame is not None and frame.size > 0:
                        success_count += 1
                
                if success_count >= 2:  # At least 2 successful reads
                    print(f"    ✅ {backend_name}: Working! Frame shape: {frame.shape}")
                    working_backends.append((backend_id, backend_name))
                else:
                    print(f"    ⚠️ {backend_name}: Opens but unreliable frame capture")
                
                cap.release()
            else:
                print(f"    ❌ {backend_name}: Cannot open")
                
        except Exception as e:
            print(f"    ❌ {backend_name}: Error - {e}")
    
    return working_backends

def create_robust_camera_class():
    """Create a robust camera class that handles V4L2 issues"""
    camera_class_code = '''
import cv2
import time
import logging

class RobustCameraCapture:
    """
    Robust camera capture class that handles V4L2 backend issues
    """
    
    def __init__(self, camera_index=0, preferred_backend=None):
        self.camera_index = camera_index
        self.cap = None
        self.backend = None
        self.logger = logging.getLogger(__name__)
        
        # Backend preference order for Raspberry Pi
        self.backends = [
            (cv2.CAP_GSTREAMER, "GStreamer"),
            (cv2.CAP_V4L2, "V4L2"), 
            (cv2.CAP_FFMPEG, "FFmpeg"),
            (cv2.CAP_ANY, "Any")
        ]
        
        if preferred_backend:
            # Move preferred backend to front
            self.backends = [b for b in self.backends if b[1] == preferred_backend] + [b for b in self.backends if b[1] != preferred_backend]
    
    def initialize_camera(self):
        """Initialize camera with backend fallback"""
        for backend_id, backend_name in self.backends:
            try:
                self.logger.info(f"Trying {backend_name} backend...")
                
                self.cap = cv2.VideoCapture(self.camera_index, backend_id)
                
                if self.cap.isOpened():
                    # Set camera properties
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    self.cap.set(cv2.CAP_PROP_FPS, 15)
                    
                    # Test frame capture
                    time.sleep(0.5)  # Allow camera to initialize
                    ret, frame = self.cap.read()
                    
                    if ret and frame is not None and frame.size > 0:
                        self.backend = backend_name
                        self.logger.info(f"✅ Camera initialized with {backend_name}")
                        return True
                    else:
                        self.cap.release()
                        self.logger.warning(f"⚠️ {backend_name} opens but no frame")
                else:
                    self.logger.warning(f"❌ {backend_name} cannot open camera")
                    
            except Exception as e:
                self.logger.error(f"❌ {backend_name} error: {e}")
                if self.cap:
                    self.cap.release()
        
        self.logger.error("Failed to initialize camera with any backend")
        return False
    
    def read(self):
        """Read frame with error handling"""
        if not self.cap or not self.cap.isOpened():
            return False, None
            
        try:
            ret, frame = self.cap.read()
            return ret, frame
        except Exception as e:
            self.logger.error(f"Error reading frame: {e}")
            return False, None
    
    def release(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
            self.logger.info("Camera released")
    
    def __del__(self):
        """Destructor"""
        self.release()

# Usage example:
# camera = RobustCameraCapture(camera_index=0)
# if camera.initialize_camera():
#     ret, frame = camera.read()
#     if ret:
#         print(f"Frame captured: {frame.shape}")
# camera.release()
'''
    
    return camera_class_code

def main():
    """Enhanced main diagnostic function with V4L2 fixes"""
    print("🔍 ENHANCED CAMERA DIAGNOSTIC WITH V4L2 FIXES")
    print("=" * 60)
    
    # Check system info
    try:
        with open('/proc/device-tree/model', 'r') as f:
            pi_model = f.read().strip()
        print(f"📱 Pi Model: {pi_model}")
    except:
        print("📱 Pi Model: Unknown")
    
    # Check V4L2 devices
    v4l2_devices = check_v4l2_devices()
    
    # Check video devices
    print("\n📹 Video Device Analysis:")
    video_devices = []
    for i in range(10):
        device_path = f"/dev/video{i}"
        if os.path.exists(device_path):
            video_devices.append(i)
            print(f"  ✅ {device_path} exists")
    
    if not video_devices:
        print("  ❌ No video devices found")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Check camera connection")
        print("2. Enable camera: sudo raspi-config")
        print("3. Add user to video group: sudo usermod -a -G video $USER")
        print("4. Reboot system")
        return False
    
    # Test each video device with backend fallback
    working_configs = []
    for device_index in video_devices:
        backends = test_camera_with_backend_fallback(device_index)
        if backends:
            for backend_id, backend_name in backends:
                working_configs.append((device_index, backend_id, backend_name))
    
    # Results and recommendations
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC RESULTS")
    print("=" * 60)
    
    if working_configs:
        print("✅ Working camera configurations:")
        for device_index, backend_id, backend_name in working_configs:
            print(f"  • Camera {device_index} with {backend_name} backend")
        
        # Recommend best configuration
        best_config = working_configs[0]
        print(f"\n💡 RECOMMENDED CONFIGURATION:")
        print(f"   Camera Index: {best_config[0]}")
        print(f"   Backend: {best_config[2]}")
        print(f"   Backend ID: {best_config[1]}")
        
        # Generate code snippets
        print(f"\n🔧 CODE SNIPPET:")
        print(f"   cap = cv2.VideoCapture({best_config[0]}, {best_config[1]})")
        
        # Create robust camera class file
        print(f"\n📁 Creating robust_camera.py...")
        with open('robust_camera.py', 'w') as f:
            f.write(create_robust_camera_class())
        print("   ✅ robust_camera.py created with fallback handling")
        
        return True
    else:
        print("❌ No working camera configurations found!")
        print("\n🔧 SPECIFIC V4L2 TROUBLESHOOTING:")
        print("1. Install V4L utilities: sudo apt install v4l-utils")
        print("2. Check camera permissions: ls -la /dev/video*")
        print("3. Try different camera index: 1, 2, 3 instead of 0")
        print("4. Use GStreamer backend instead of V4L2")
        print("5. For Pi 5: Consider using libcamera instead")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)