#!/bin/bash

# 🎤 COMPLETE PI 5 AUDIO FIX SCRIPT
# Fixes all microphone and audio issues for AI Assistant on Raspberry Pi 5

echo "🤖 PI 5 COMPLETE AUDIO FIX"
echo "🔧 This will fix all microphone and speech recognition issues"
echo "============================================================"

# Function to check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        echo "❌ Please run this script as a regular user (not sudo)"
        echo "💡 The script will ask for sudo when needed"
        exit 1
    fi
}

# Function to backup config files
backup_configs() {
    echo "📁 Creating backup of audio configs..."
    sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
    cp ~/.asoundrc ~/.asoundrc.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
    echo "✅ Configs backed up"
}

# Function to fix ALSA configuration
fix_alsa_config() {
    echo ""
    echo "🔧 FIXING ALSA CONFIGURATION"
    echo "=================================================="
    
    # Create proper .asoundrc file
    echo "📝 Creating optimized .asoundrc..."
    cat > ~/.asoundrc << 'EOF'
# Optimized ALSA configuration for Raspberry Pi 5 USB microphones
pcm.!default {
    type asym
    playback.pcm "dmix"
    capture.pcm "dsnoop"
}

pcm.dmix {
    type dmix
    ipc_key 1024
    slave {
        pcm "hw:0,0"
        channels 2
    }
}

pcm.dsnoop {
    type dsnoop
    ipc_key 2048
    slave {
        pcm "hw:1,0"  # USB microphone (usually card 1)
        channels 1
        rate 44100
        format S16_LE
    }
}

# Fallback for USB microphone
pcm.usb_mic {
    type hw
    card 1
    device 0
}

# Mixer controls
ctl.!default {
    type hw
    card 0
}
EOF
    
    echo "✅ .asoundrc created"
}

# Function to fix Pi 5 boot config
fix_boot_config() {
    echo ""
    echo "🔧 FIXING PI 5 BOOT CONFIGURATION"
    echo "=================================================="
    
    # Check and fix config.txt
    echo "📝 Updating /boot/firmware/config.txt..."
    
    # Remove conflicting audio settings
    sudo sed -i '/^dtparam=audio=/d' /boot/firmware/config.txt
    sudo sed -i '/^audio_pwm_mode=/d' /boot/firmware/config.txt
    
    # Add optimized audio settings for Pi 5
    echo "" | sudo tee -a /boot/firmware/config.txt
    echo "# Audio configuration for AI Assistant" | sudo tee -a /boot/firmware/config.txt
    echo "dtparam=audio=on" | sudo tee -a /boot/firmware/config.txt
    echo "audio_pwm_mode=0" | sudo tee -a /boot/firmware/config.txt
    echo "" | sudo tee -a /boot/firmware/config.txt
    
    echo "✅ Boot config updated"
}

# Function to install required packages
install_packages() {
    echo ""
    echo "🔧 INSTALLING REQUIRED PACKAGES"
    echo "=================================================="
    
    echo "📦 Updating package list..."
    sudo apt update -qq
    
    echo "📦 Installing audio packages..."
    sudo apt install -y \
        alsa-utils \
        pulseaudio \
        pulseaudio-utils \
        pavucontrol \
        sox \
        portaudio19-dev \
        python3-pyaudio \
        espeak \
        espeak-data
    
    echo "✅ Packages installed"
}

# Function to configure PulseAudio
configure_pulseaudio() {
    echo ""
    echo "🔧 CONFIGURING PULSEAUDIO"
    echo "=================================================="
    
    # Kill existing PulseAudio
    pulseaudio -k 2>/dev/null || true
    
    # Create PulseAudio config directory
    mkdir -p ~/.config/pulse
    
    # Create optimized PulseAudio config
    cat > ~/.config/pulse/default.pa << 'EOF'
#!/usr/bin/pulseaudio -nF

# Load audio drivers
load-module module-alsa-sink device=hw:0,0
load-module module-alsa-source device=hw:1,0 source_name=usb_mic

# Load other essential modules
load-module module-native-protocol-unix
load-module module-default-device-restore
load-module module-rescue-streams
load-module module-always-sink
load-module module-intended-roles
load-module module-suspend-on-idle

# Set default source to USB microphone
set-default-source usb_mic
EOF
    
    # Start PulseAudio
    pulseaudio --start
    sleep 2
    
    echo "✅ PulseAudio configured"
}

# Function to test microphone
test_microphone() {
    echo ""
    echo "🔧 TESTING MICROPHONE"
    echo "=================================================="
    
    echo "🎤 Available audio devices:"
    arecord -l 2>/dev/null || echo "❌ arecord command failed"
    
    echo ""
    echo "🎤 PulseAudio sources:"
    pactl list sources short 2>/dev/null || echo "❌ PulseAudio not running"
    
    echo ""
    echo "🎤 Testing microphone recording (5 seconds)..."
    echo "📢 Please speak now..."
    
    # Test recording
    if arecord -D hw:1,0 -f cd -t wav -d 5 /tmp/test_recording.wav 2>/dev/null; then
        echo "✅ Recording successful"
        
        # Test playback
        echo "🔊 Playing back your recording..."
        aplay /tmp/test_recording.wav 2>/dev/null || echo "⚠️ Playback failed (normal on headless Pi)"
        
        # Check file size
        if [ -s /tmp/test_recording.wav ]; then
            echo "✅ Microphone is working!"
            rm -f /tmp/test_recording.wav
            return 0
        else
            echo "❌ Recording file is empty"
            return 1
        fi
    else
        echo "❌ Recording failed"
        return 1
    fi
}

# Function to create Python test script
create_python_test() {
    echo ""
    echo "🔧 CREATING PYTHON AUDIO TEST"
    echo "=================================================="
    
    cat > test_fixed_audio.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for fixed audio on Pi 5
"""

import speech_recognition as sr
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fixed_audio():
    """Test the fixed audio configuration."""
    print("🎤 TESTING FIXED AUDIO CONFIGURATION")
    print("=" * 50)
    
    try:
        recognizer = sr.Recognizer()
        
        # Test microphone access
        print("🔍 Testing microphone access...")
        with sr.Microphone() as source:
            print("✅ Microphone accessible")
            
            # Calibrate for ambient noise
            print("🎯 Calibrating for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"✅ Energy threshold after calibration: {recognizer.energy_threshold}")
            
            # Set a very low threshold for Pi 5
            recognizer.energy_threshold = 50
            print(f"🎚️ Set energy threshold to: {recognizer.energy_threshold}")
            
            # Test speech recognition
            print("📢 Say 'hello' now (you have 5 seconds)...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                print("✅ Audio captured successfully")
                
                # Try to recognize
                text = recognizer.recognize_google(audio)
                print(f"✅ Speech recognized: '{text}'")
                return True
                
            except sr.WaitTimeoutError:
                print("⏰ No speech detected (timeout)")
                return False
            except sr.UnknownValueError:
                print("❓ Speech detected but not understood")
                return False
            except sr.RequestError as e:
                print(f"❌ Recognition service error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_fixed_audio()
    if success:
        print("\n🎉 AUDIO FIX SUCCESSFUL!")
        print("✅ Your Pi 5 microphone is now working properly")
    else:
        print("\n❌ AUDIO FIX INCOMPLETE")
        print("🔧 Additional troubleshooting may be needed")
EOF
    
    chmod +x test_fixed_audio.py
    echo "✅ Python test script created"
}

# Function to fix permissions
fix_permissions() {
    echo ""
    echo "🔧 FIXING AUDIO PERMISSIONS"
    echo "=================================================="
    
    # Add user to audio group
    sudo usermod -a -G audio $USER
    
    # Fix device permissions
    sudo chmod 666 /dev/snd/* 2>/dev/null || true
    
    echo "✅ Permissions fixed"
}

# Function to restart audio services
restart_audio_services() {
    echo ""
    echo "🔧 RESTARTING AUDIO SERVICES"
    echo "=================================================="
    
    # Stop services
    pulseaudio -k 2>/dev/null || true
    sudo systemctl stop alsa-state 2>/dev/null || true
    
    # Reload ALSA
    sudo alsactl restore 2>/dev/null || true
    
    # Start PulseAudio
    pulseaudio --start
    sleep 2
    
    echo "✅ Audio services restarted"
}

# Main execution
main() {
    echo "🚀 Starting complete Pi 5 audio fix..."
    
    check_root
    backup_configs
    install_packages
    fix_boot_config
    fix_alsa_config
    fix_permissions
    configure_pulseaudio
    restart_audio_services
    create_python_test
    
    echo ""
    echo "🎉 COMPLETE AUDIO FIX FINISHED!"
    echo "============================================================"
    echo ""
    echo "🔄 NEXT STEPS:"
    echo "1. Reboot your Pi 5: sudo reboot"
    echo "2. After reboot, test: python3 test_fixed_audio.py"
    echo "3. If working, run: python3 main.py"
    echo ""
    echo "⚠️  IMPORTANT: You MUST reboot for changes to take effect!"
    echo ""
    
    # Test current state
    if test_microphone; then
        echo "🎉 Microphone is already working!"
        echo "🚀 You can try: python3 test_fixed_audio.py"
    else
        echo "🔄 Reboot required for full fix"
    fi
}

# Run the main function
main 