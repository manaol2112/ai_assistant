#!/bin/bash

# Raspberry Pi 5 + Sony AITRIOS AI Camera Setup Script
# This script installs all required dependencies for the AI camera system

echo "🤖 Setting up Raspberry Pi 5 with Sony AITRIOS AI Camera..."
echo "=================================================="

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "❌ This script must be run on a Raspberry Pi"
    exit 1
fi

echo "✅ Detected Raspberry Pi system"

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies for camera
echo "📷 Installing camera system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    python3-numpy \
    python3-opencv \
    libcamera-dev \
    libcamera-tools \
    libcamera-apps \
    python3-libcamera \
    python3-kms++ \
    python3-prctl \
    libatlas-base-dev \
    libjpeg-dev \
    libtiff5-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libfontconfig1-dev \
    libcairo2-dev \
    libgdk-pixbuf2.0-dev \
    libpango1.0-dev \
    libgtk2.0-dev \
    libgtk-3-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    libqt5gui5 \
    libqt5webkit5 \
    libqt5test5 \
    python3-pyqt5

# Install picamera2 and related packages
echo "🎥 Installing picamera2..."
sudo apt install -y python3-picamera2

# Alternative installation methods if the above fails
if ! python3 -c "import picamera2" 2>/dev/null; then
    echo "⚠️ System picamera2 not working, trying pip installation..."
    
    # Install via pip
    pip3 install --upgrade pip
    pip3 install picamera2
    
    # If still failing, try with --break-system-packages (for newer Pi OS)
    if ! python3 -c "import picamera2" 2>/dev/null; then
        echo "🔧 Trying pip with --break-system-packages..."
        pip3 install --break-system-packages picamera2
    fi
fi

# Install Sony IMX500 specific packages (if available)
echo "🧠 Installing Sony IMX500 AI packages..."
sudo apt install -y \
    imx500-all \
    rpi-camera-assets \
    python3-tflite-runtime

# Install face recognition dependencies
echo "👤 Installing face recognition dependencies..."
sudo apt install -y \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev

# Install face recognition
pip3 install --break-system-packages \
    face-recognition \
    dlib \
    opencv-python

# Enable camera interface
echo "🔧 Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Enable I2C (needed for some camera modules)
sudo raspi-config nonint do_i2c 0

# Add user to video group
echo "👥 Adding user to video group..."
sudo usermod -a -G video $USER

# Create camera test script
echo "📝 Creating camera test script..."
cat > test_camera.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for Raspberry Pi 5 + Sony AITRIOS AI Camera
"""

import sys
import platform

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
    
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
    
    try:
        from picamera2 import Picamera2
        print("✅ Picamera2: Available")
        return True
    except ImportError as e:
        print(f"❌ Picamera2: {e}")
        return False
    
    try:
        import face_recognition
        print("✅ Face Recognition: Available")
    except ImportError as e:
        print(f"❌ Face Recognition: {e}")

def test_camera():
    """Test camera functionality"""
    print("\n📷 Testing camera...")
    
    try:
        from picamera2 import Picamera2
        
        picam2 = Picamera2()
        print("✅ Camera object created")
        
        # Get camera info
        camera_info = picam2.sensor_modes
        print(f"✅ Available sensor modes: {len(camera_info)}")
        
        # Test configuration
        config = picam2.create_preview_configuration()
        picam2.configure(config)
        print("✅ Camera configured")
        
        # Test start/stop
        picam2.start()
        print("✅ Camera started")
        
        # Capture a test frame
        frame = picam2.capture_array()
        print(f"✅ Frame captured: {frame.shape}")
        
        picam2.stop()
        picam2.close()
        print("✅ Camera stopped and closed")
        
        return True
        
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def main():
    print("🤖 Raspberry Pi 5 + Sony AITRIOS AI Camera Test")
    print("=" * 50)
    print(f"System: {platform.system()} {platform.machine()}")
    print(f"Platform: {platform.platform()}")
    
    # Check if we're on Raspberry Pi
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
            print(f"Device: {model}")
    except:
        print("Device: Unknown")
    
    print()
    
    # Test imports
    picamera2_available = test_imports()
    
    if picamera2_available:
        # Test camera
        camera_working = test_camera()
        
        if camera_working:
            print("\n🎉 All tests passed! Camera is ready.")
        else:
            print("\n⚠️ Camera hardware test failed.")
    else:
        print("\n❌ Picamera2 not available. Check installation.")

if __name__ == "__main__":
    main()
EOF

chmod +x test_camera.py

# Test the installation
echo ""
echo "🧪 Testing installation..."
python3 test_camera.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. After reboot, test the camera: python3 test_camera.py"
echo "3. Run your AI assistant with: python3 your_main_script.py"
echo ""
echo "💡 If you still have issues:"
echo "- Check camera cable connection"
echo "- Ensure camera is enabled in raspi-config"
echo "- Check camera permissions: ls -l /dev/video*"
echo "- Try: sudo usermod -a -G video $USER && newgrp video" 