#!/bin/bash
# Setup script for Sony IMX500 AI Camera dependencies on Raspberry Pi 5
# This installs the system packages needed for libcamera support

set -e

echo "🤖 Setting up Sony IMX500 AI Camera dependencies..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update

# Install libcamera system packages
echo "📷 Installing libcamera system packages..."
sudo apt install -y \
    libcamera-apps \
    libcamera-dev \
    libcamera-tools \
    python3-libcamera \
    python3-kms++ \
    python3-prctl

# Install additional camera and video tools
echo "🔧 Installing additional camera tools..."
sudo apt install -y \
    v4l-utils \
    libcamera0

# Optional: Install additional development tools if available
echo "🔧 Installing optional development tools..."
sudo apt install -y \
    cmake \
    build-essential \
    pkg-config || echo "⚠️ Some development tools not available"

# Check if libcamera is working
echo "🧪 Testing libcamera installation..."
if command -v libcamera-hello &> /dev/null; then
    echo "✅ libcamera-hello found"
    
    # Test camera detection (with timeout)
    echo "🔍 Testing camera detection..."
    timeout 10 libcamera-hello --list-cameras || echo "⚠️ Camera test timeout (normal if no camera connected)"
else
    echo "❌ libcamera-hello not found"
    exit 1
fi

# Check for IMX500 specific files
echo "🔍 Checking for IMX500 AI models..."
if [ -d "/usr/share/imx500-models" ]; then
    echo "✅ IMX500 models directory found"
    ls -la /usr/share/imx500-models/ || true
else
    echo "⚠️ IMX500 models directory not found"
    echo "   You may need to install Sony AITRIOS SDK for AI models"
fi

# Check for camera devices
echo "🔍 Checking camera devices..."
if [ -e "/dev/video0" ]; then
    echo "✅ Camera device /dev/video0 found"
else
    echo "⚠️ No camera device found at /dev/video0"
fi

# Set proper permissions
echo "🔐 Setting camera permissions..."
sudo usermod -a -G video $USER

echo ""
echo "✅ Sony IMX500 dependencies setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. Test the camera: python3 test_imx500_camera.py"
echo "3. Run the AI assistant: python3 main.py"
echo ""
echo "🔧 If you need AI models, install Sony AITRIOS SDK:"
echo "   Follow Sony's official documentation for IMX500 AI models" 