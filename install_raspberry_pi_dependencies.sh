#!/bin/bash
# Install Raspberry Pi Dependencies for AI Assistant
# This script installs additional dependencies needed for Raspberry Pi 5

echo "🍓 Installing Raspberry Pi 5 Dependencies for AI Assistant"
echo "============================================================"

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install libcamera and related packages
echo "📷 Installing libcamera and camera dependencies..."
sudo apt install -y libcamera-dev libcamera-apps libcamera-tools

# Install picamera2 
echo "🐍 Installing picamera2 for Python..."
pip install picamera2

# Install additional camera libraries
echo "📸 Installing additional camera libraries..."
pip install v4l2-python3

# Install MediaPipe dependencies for ARM64
echo "🤖 Installing MediaPipe for ARM64..."
pip install mediapipe

# Install additional AI/ML libraries optimized for Raspberry Pi
echo "🧠 Installing AI/ML libraries..."
pip install --upgrade numpy opencv-python
pip install tensorflow-lite-runtime

# Install GPIO and hardware control libraries
echo "⚡ Installing hardware control libraries..."
sudo apt install -y python3-rpi.gpio
pip install gpiozero

# Install audio dependencies
echo "🔊 Installing audio dependencies..."
sudo apt install -y portaudio19-dev python3-pyaudio
pip install pyaudio

# Install additional system libraries
echo "📚 Installing system libraries..."
sudo apt install -y python3-dev python3-pip
sudo apt install -y cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libfontconfig1-dev libcairo2-dev
sudo apt install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt install -y libgtk2.0-dev libgtk-3-dev
sudo apt install -y libatlas-base-dev gfortran

# Enable camera interface
echo "📷 Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Set up camera permissions
echo "🔐 Setting up camera permissions..."
sudo usermod -a -G video $USER

# Install face recognition dependencies
echo "👤 Installing face recognition dependencies..."
pip install dlib
pip install face-recognition

# Install additional Python packages
echo "🐍 Installing additional Python packages..."
pip install imutils
pip install Pillow
pip install scipy

echo ""
echo "✅ Raspberry Pi 5 dependencies installation completed!"
echo ""
echo "📋 Installed components:"
echo "   • libcamera and libcamera-apps"
echo "   • picamera2 for Python camera interface"
echo "   • MediaPipe for gesture recognition"
echo "   • Face recognition libraries"
echo "   • Audio processing libraries"
echo "   • GPIO control libraries"
echo "   • AI/ML optimization libraries"
echo ""
echo "🔄 Please reboot your Raspberry Pi 5 for changes to take effect:"
echo "   sudo reboot"
echo ""
echo "🚀 After reboot, test your setup with:"
echo "   python3 test_face_tracking_setup.py"
echo "   python3 main.py" 