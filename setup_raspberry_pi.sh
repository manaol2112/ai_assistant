#!/bin/bash

# AI Assistant Setup Script for Raspberry Pi
# This script installs all necessary dependencies and configures the system

set -e  # Exit on any error

echo "🤖 Setting up AI Assistant for Raspberry Pi..."
echo "=================================================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies for audio
echo "🔊 Installing audio system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    portaudio19-dev \
    python3-pyaudio \
    alsa-utils \
    pulseaudio \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    flac \
    sox \
    libsox-fmt-all

# Install build dependencies
echo "🔧 Installing build dependencies..."
sudo apt install -y \
    build-essential \
    cmake \
    pkg-config \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    libav-tools \
    libavcodec-extra

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv ai_assistant_env
source ai_assistant_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Configure audio for Raspberry Pi
echo "🎵 Configuring audio for Raspberry Pi..."

# Set up ALSA configuration
sudo tee /etc/asound.conf > /dev/null <<EOF
pcm.!default {
    type pulse
}
ctl.!default {
    type pulse
}
EOF

# Add user to audio group
sudo usermod -a -G audio $USER

# Configure PulseAudio for better performance
mkdir -p ~/.config/pulse
tee ~/.config/pulse/client.conf > /dev/null <<EOF
autospawn = yes
daemon-binary = /usr/bin/pulseaudio
extra-arguments = --log-target=syslog
EOF

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env configuration file..."
    cp env_example.txt .env
    echo "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key!"
fi

# Create systemd service for auto-start (optional)
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/ai-assistant.service > /dev/null <<EOF
[Unit]
Description=AI Assistant for Sophia and Eladriel
After=network.target sound.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
Environment=PATH=$PWD/ai_assistant_env/bin
ExecStart=$PWD/ai_assistant_env/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Make scripts executable
chmod +x *.sh
chmod +x main.py

# Configure GPIO and permissions (if needed)
echo "🔐 Configuring permissions..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G i2c $USER
sudo usermod -a -G spi $USER

# Test audio system
echo "🧪 Testing audio system..."
if command -v speaker-test &> /dev/null; then
    echo "Running quick audio test (2 seconds)..."
    timeout 2 speaker-test -t sine -f 1000 -l 1 || echo "Audio test completed"
fi

# Performance optimizations for Raspberry Pi
echo "⚡ Applying Raspberry Pi optimizations..."

# Increase GPU memory split for better audio performance
if grep -q "gpu_mem=" /boot/config.txt; then
    sudo sed -i 's/gpu_mem=.*/gpu_mem=128/' /boot/config.txt
else
    echo "gpu_mem=128" | sudo tee -a /boot/config.txt
fi

# Enable audio
if ! grep -q "dtparam=audio=on" /boot/config.txt; then
    echo "dtparam=audio=on" | sudo tee -a /boot/config.txt
fi

# Create test script
echo "📝 Creating test script..."
tee test_assistant.py > /dev/null <<'EOF'
#!/usr/bin/env python3
"""Test script for AI Assistant"""

import sys
sys.path.append('.')

from wake_word_detector import WakeWordDetector
from config import Config
from audio_utils import AudioManager

def test_components():
    print("🧪 Testing AI Assistant Components")
    print("=" * 40)
    
    try:
        # Test configuration
        print("1. Testing configuration...")
        config = Config()
        config.validate()
        
        # Test audio
        print("2. Testing audio system...")
        audio_manager = AudioManager()
        mic_info = audio_manager.get_microphone_info()
        print(f"   Default microphone: {mic_info['default_mic']['name'] if mic_info['default_mic'] else 'None'}")
        
        # Test wake word detector
        print("3. Testing wake word detector...")
        wake_detector = WakeWordDetector(config)
        stats = wake_detector.get_detection_stats()
        print(f"   Wake words supported: {stats['wake_words_supported']}")
        print(f"   Users supported: {stats['users_supported']}")
        
        print("\n✅ All components initialized successfully!")
        print("\n🎤 You can now run: python main.py")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_components()
EOF

chmod +x test_assistant.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: source ai_assistant_env/bin/activate"
echo "3. Test: python test_assistant.py"
echo "4. Start: python main.py"
echo ""
echo "Optional: Enable auto-start service:"
echo "  sudo systemctl enable ai-assistant.service"
echo "  sudo systemctl start ai-assistant.service"
echo ""
echo "⚠️  You may need to reboot for audio changes to take effect"

# Deactivate virtual environment
deactivate 2>/dev/null || true

echo "Setup script completed! 🚀" 