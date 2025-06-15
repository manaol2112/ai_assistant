#!/bin/bash

# =============================================================================
# AITRIOS AI Camera Setup Script for Raspberry Pi 5
# =============================================================================
# This script helps set up the Sony AITRIOS AI Camera on Raspberry Pi 5
# Run with: bash setup_aitrios.sh
#
# IMPORTANT: This script assumes you have:
# 1. Raspberry Pi 5 with Raspberry Pi OS Bookworm
# 2. Sony IMX500 AITRIOS AI Camera module connected
# 3. Internet connection for downloads
# =============================================================================

set -e  # Exit on any error

echo "🤖 Starting AITRIOS AI Camera Setup for Raspberry Pi 5..."
echo "============================================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# Check if running on Raspberry Pi
print_section "System Check"
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    print_error "This script is designed for Raspberry Pi only!"
    exit 1
fi

print_status "Detected Raspberry Pi system ✅"

# Check Raspberry Pi version
PI_MODEL=$(cat /proc/cpuinfo | grep "Model" | head -1 | cut -d: -f2 | xargs)
print_status "Pi Model: $PI_MODEL"

# Update system
print_section "System Update"
print_status "Updating package lists..."
sudo apt update -y

print_status "Upgrading system packages..."
sudo apt upgrade -y

# Install essential packages
print_section "Installing Essential Packages"
print_status "Installing camera and development packages..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-opencv \
    python3-numpy \
    python3-picamera \
    python3-picamera2 \
    python3-libcamera \
    python3-kms++ \
    cmake \
    pkg-config \
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
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    python3-pyqt5 \
    python3-h5py \
    git

# Enable camera interface
print_section "Camera Configuration"
print_status "Enabling camera interface..."
sudo raspi-config nonint do_camera 0
print_status "Camera interface enabled ✅"

# Add user to video group
print_status "Adding user to video group..."
sudo usermod -a -G video $USER

# Check for camera connection
print_section "Camera Detection"
print_status "Checking for connected cameras..."
if libcamera-hello --list-cameras 2>/dev/null | grep -q "Available cameras"; then
    print_status "Camera detected ✅"
    libcamera-hello --list-cameras
else
    print_warning "No camera detected. Please check your camera connection."
fi

# Create virtual environment
print_section "Python Environment Setup"
VENV_DIR="aitrios_venv"
if [ ! -d "$VENV_DIR" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv $VENV_DIR
fi

print_status "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python packages
print_status "Installing Python packages..."
pip install \
    opencv-python \
    numpy \
    pillow \
    picamera2 \
    ultralytics \
    torch \
    torchvision \
    face-recognition \
    mediapipe \
    imutils

# Create model directory
print_section "Model Setup"
MODEL_DIR="/usr/share/imx500-models"
if [ ! -d "$MODEL_DIR" ]; then
    print_status "Creating model directory..."
    sudo mkdir -p $MODEL_DIR
fi

# Download IMX500 models (if available)
print_status "Setting up IMX500 models..."
# Note: Actual model files should be downloaded from Sony's official sources
# This is a placeholder for the model setup process

# Create camera assets directory
ASSETS_DIR="/usr/share/rpi-camera-assets"
if [ ! -d "$ASSETS_DIR" ]; then
    print_status "Creating camera assets directory..."
    sudo mkdir -p $ASSETS_DIR
fi

# Create sample configuration files
print_section "Configuration Files"
print_status "Creating sample configuration files..."

# Camera configuration
cat > camera_config.json << EOF
{
    "camera_type": "aitrios",
    "resolution": {
        "width": 4056,
        "height": 3040
    },
    "ai_models": {
        "object_detection": "/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk",
        "pose_detection": "/usr/share/rpi-camera-assets/imx500_posenet.json",
        "mobilenet_ssd": "/usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json"
    },
    "settings": {
        "confidence_threshold": 0.5,
        "max_detections": 10,
        "enable_face_recognition": true,
        "enable_object_detection": true,
        "enable_pose_detection": true
    }
}
EOF

print_status "Camera configuration created: camera_config.json"

# Test script
print_section "Creating Test Script"
cat > test_aitrios_camera.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for AITRIOS AI Camera
"""
import cv2
import numpy as np
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_camera():
    """Test AITRIOS camera functionality"""
    print("🤖 Testing AITRIOS AI Camera...")
    
    try:
        # Try to import our AITRIOS handler
        try:
            from aitrios_camera_handler import AITRIOSCameraHandler
            print("✅ AITRIOS handler imported successfully")
            
            # Initialize camera
            camera = AITRIOSCameraHandler()
            
            if camera.is_camera_available():
                print("✅ AITRIOS camera is available")
                
                # Test frame capture
                ret, frame = camera.read()
                if ret and frame is not None:
                    print(f"✅ Frame captured successfully: {frame.shape}")
                    
                    # Test AI detection
                    objects = camera.detect_objects()
                    faces = camera.detect_faces()
                    
                    print(f"🤖 Objects detected: {len(objects)}")
                    print(f"🤖 Faces detected: {len(faces)}")
                    
                    # Test image capture
                    result = camera.capture_image_with_ai_metadata("test_capture.jpg")
                    if result['success']:
                        print("✅ Image capture with AI metadata successful")
                    
                    camera.release()
                    print("✅ All AITRIOS tests passed!")
                    return True
                else:
                    print("❌ Failed to capture frame")
                    
            else:
                print("❌ AITRIOS camera not available")
                
        except ImportError:
            print("⚠️ AITRIOS handler not found, testing with standard camera")
            
            # Fallback to standard camera test
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"✅ Standard camera working: {frame.shape}")
                    cap.release()
                    return True
                else:
                    print("❌ Failed to capture from standard camera")
            else:
                print("❌ No camera detected")
                
    except Exception as e:
        logger.error(f"Camera test failed: {e}")
        return False
    
    return False

if __name__ == "__main__":
    test_camera()
EOF

chmod +x test_aitrios_camera.py
print_status "Test script created: test_aitrios_camera.py"

# Create systemd service file
print_section "Service Configuration"
cat > ai-assistant-aitrios.service << EOF
[Unit]
Description=AI Assistant with AITRIOS Camera
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=/usr/bin:/usr/local/bin:$(pwd)/$VENV_DIR/bin
ExecStart=$(pwd)/$VENV_DIR/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_status "Systemd service file created: ai-assistant-aitrios.service"

# Final instructions
print_section "Setup Complete!"
echo
print_status "AITRIOS AI Camera setup completed successfully! 🎉"
echo
echo "Next steps:"
echo "1. Reboot your Raspberry Pi: ${YELLOW}sudo reboot${NC}"
echo "2. After reboot, test the camera: ${YELLOW}./test_aitrios_camera.py${NC}"
echo "3. If needed, install Sony AITRIOS SDK following their documentation"
echo "4. Run your AI assistant: ${YELLOW}source $VENV_DIR/bin/activate && python3 main.py${NC}"
echo
print_warning "Important notes:"
echo "- Ensure your IMX500 camera is properly connected"
echo "- Some features may require Sony's official AITRIOS SDK"
echo "- Check camera permissions if you encounter access issues"
echo "- The AI models may need to be downloaded separately from Sony"
echo
print_status "For service installation: ${YELLOW}sudo cp ai-assistant-aitrios.service /etc/systemd/system/${NC}"
print_status "Enable service: ${YELLOW}sudo systemctl enable ai-assistant-aitrios${NC}"
print_status "Start service: ${YELLOW}sudo systemctl start ai-assistant-aitrios${NC}"
echo
echo "🤖 Happy AI Camera programming! 📸" 