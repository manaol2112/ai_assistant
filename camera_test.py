#!/usr/bin/env python3
"""
Enhanced Camera Diagnostic for Raspberry Pi
Tests multiple camera backends and indices
"""

import cv2
import os
import subprocess
import sys

def check_system_info():
    """Check system and camera information"""
    print("🔍 SYSTEM CAMERA DIAGNOSTIC")
    print("=" * 50)
    
    # Check Pi model
    try:
        with open('/proc/device-tree/model', 'r') as f:
            pi_model = f.read().strip()
        print(f"📱 Pi Model: {pi_model}")
    except:
        print("📱 Pi Model: Unknown")
    
    # Check video devices
    print("\n📹 Video Devices:")
    video_devices = []
    for i in range(10):
        device_path = f"/dev/video{i}"
        if os.path.exists(device_path):
            video_devices.append(i)
            print(f"  ✅ /dev/video{i} exists")
    
    if not video_devices:
        print("  ❌ No video devices found")
        return False
    
    # Check USB cameras
    print("\n🔌 USB Devices:")
    try:
        result = subprocess.run(['lsusb'], capture_output=True, text=True)
        usb_lines = result.stdout.split('\n')
        camera_found = False
        for line in usb_lines:
            if any(keyword in line.lower() for keyword in ['camera', 'webcam', 'video']):
                print(f"  📷 {line.strip()}")
                camera_found = True
        if not camera_found:
            print("  ⚠️ No USB cameras detected")
    except:
        print("  ❌ Cannot check USB devices")
    
    return True

def test_opencv_backends():
    """Test different OpenCV backends"""
    print("\n🔧 Testing OpenCV Backends:")
    
    backends = [
        (cv2.CAP_V4L2, "V4L2"),
        (cv2.CAP_GSTREAMER, "GStreamer"),
        (cv2.CAP_FFMPEG, "FFmpeg"),
        (cv2.CAP_ANY, "Any")
    ]
    
    working_configs = []
    
    for backend_id, backend_name in backends:
        print(f"\n  Testing {backend_name} backend...")
        
        for camera_index in range(4):
            try:
                cap = cv2.VideoCapture(camera_index, backend_id)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"    ✅ Camera {camera_index} with {backend_name}: {frame.shape}")
                        working_configs.append((camera_index, backend_id, backend_name))
                    else:
                        print(f"    ⚠️ Camera {camera_index} with {backend_name}: Opens but no frame")
                    cap.release()
                else:
                    print(f"    ❌ Camera {camera_index} with {backend_name}: Cannot open")
            except Exception as e:
                print(f"    ❌ Camera {camera_index} with {backend_name}: Error - {e}")
    
    return working_configs

def test_libcamera():
    """Test libcamera (Pi 5 specific)"""
    print("\n📷 Testing libcamera (Pi 5):")
    
    try:
        # Check if libcamera-hello exists
        result = subprocess.run(['which', 'libcamera-hello'], capture_output=True)
        if result.returncode == 0:
            print("  ✅ libcamera-hello found")
            
            # List cameras
            result = subprocess.run(['libcamera-hello', '--list-cameras'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("  📋 Available cameras:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print(f"    {line}")
                return True
            else:
                print(f"  ❌ libcamera-hello failed: {result.stderr}")
        else:
            print("  ⚠️ libcamera-hello not found (normal for older Pi models)")
    except Exception as e:
        print(f"  ❌ libcamera test error: {e}")
    
    return False

def main():
    """Main diagnostic function"""
    if not check_system_info():
        print("\n❌ No video devices found. Check camera connection.")
        return False
    
    # Test libcamera first (Pi 5)
    libcamera_works = test_libcamera()
    
    # Test OpenCV backends
    working_configs = test_opencv_backends()
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC RESULTS")
    print("=" * 50)
    
    if working_configs:
        print("✅ Working camera configurations found:")
        for camera_index, backend_id, backend_name in working_configs:
            print(f"  • Camera {camera_index} with {backend_name} backend")
        
        # Recommend best configuration
        best_config = working_configs[0]
        print(f"\n💡 RECOMMENDED CONFIGURATION:")
        print(f"   Camera Index: {best_config[0]}")
        print(f"   Backend: {best_config[2]}")
        
        # Generate code snippet
        print(f"\n🔧 Use this in your code:")
        print(f"   cap = cv2.VideoCapture({best_config[0]}, {best_config[1]})")
        
        return True
    else:
        print("❌ No working camera configurations found!")
        
        if libcamera_works:
            print("\n💡 SOLUTION: Use libcamera instead of OpenCV")
            print("   Try: libcamera-still -o test.jpg")
        else:
            print("\n🔧 TROUBLESHOOTING STEPS:")
            print("1. Check camera connection")
            print("2. Enable camera interface: sudo raspi-config")
            print("3. Add user to video group: sudo usermod -a -G video $USER")
            print("4. Reboot the system")
            print("5. Check /boot/config.txt for camera settings")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)