#!/bin/bash
# Minimal setup script for Sony IMX500 AI Camera on Raspberry Pi 5
# Only installs essential packages that are guaranteed to exist

set -e

echo "🤖 Minimal Sony IMX500 setup - Essential packages only..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update

# Install only the essential libcamera packages
echo "📷 Installing essential libcamera packages..."
sudo apt install -y libcamera-apps

# Install v4l-utils for camera debugging
echo "🔧 Installing video utilities..."
sudo apt install -y v4l-utils

# Try to install python3-libcamera if available
echo "🐍 Installing Python libcamera support..."
sudo apt install -y python3-libcamera || echo "⚠️ python3-libcamera not available on this system"

# Test libcamera installation
echo "🧪 Testing libcamera..."
if command -v libcamera-hello &> /dev/null; then
    echo "✅ libcamera-hello found"
    
    # Quick camera test
    echo "🔍 Quick camera test..."
    timeout 5 libcamera-hello --list-cameras || echo "⚠️ No camera detected or timeout"
else
    echo "❌ libcamera-hello not found - installation may have failed"
    exit 1
fi

# Set camera permissions
echo "🔐 Adding user to video group..."
sudo usermod -a -G video $USER

echo ""
echo "✅ Minimal setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Reboot: sudo reboot"
echo "2. Test: libcamera-hello --list-cameras"
echo "3. Run: python3 test_imx500_camera.py"
echo ""
echo "💡 If you need more features, run the full setup script later" 