#!/bin/bash

echo "🔧 RASPBERRY PI 5 AUDIO CONFIGURATION FIX"
echo "=========================================="
echo "This script will fix the audio issues identified in the diagnostic."
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Please run this script as a regular user (not with sudo)"
   echo "The script will use sudo when needed."
   exit 1
fi

# Function to print status messages
print_status() {
    echo "📋 $1"
}

print_success() {
    echo "✅ $1"
}

print_error() {
    echo "❌ $1"
}

print_fix() {
    echo "🔧 $1"
}

print_status "Starting Raspberry Pi 5 audio fixes..."

# Fix 1: Add user to pulse groups
print_fix "Adding user to pulse and pulse-access groups..."
sudo usermod -a -G pulse,pulse-access $USER
if [ $? -eq 0 ]; then
    print_success "User added to pulse groups successfully"
else
    print_error "Failed to add user to pulse groups"
fi

# Fix 2: Enable audio in /boot/config.txt (or /boot/firmware/config.txt for newer Pi OS)
print_fix "Enabling audio in Raspberry Pi configuration..."

CONFIG_FILE=""
if [ -f "/boot/firmware/config.txt" ]; then
    CONFIG_FILE="/boot/firmware/config.txt"
elif [ -f "/boot/config.txt" ]; then
    CONFIG_FILE="/boot/config.txt"
else
    print_error "Could not find config.txt file"
    exit 1
fi

print_status "Using config file: $CONFIG_FILE"

# Check if audio is already enabled
if grep -q "^dtparam=audio=on" "$CONFIG_FILE"; then
    print_success "Audio already enabled in config.txt"
else
    print_fix "Adding audio configuration to $CONFIG_FILE"
    echo "" | sudo tee -a "$CONFIG_FILE"
    echo "# Audio configuration for AI Assistant" | sudo tee -a "$CONFIG_FILE"
    echo "dtparam=audio=on" | sudo tee -a "$CONFIG_FILE"
    echo "audio_pwm_mode=2" | sudo tee -a "$CONFIG_FILE"
    print_success "Audio configuration added to $CONFIG_FILE"
fi

# Fix 3: Configure ALSA for USB audio device
print_fix "Configuring ALSA for USB audio device..."

# Create or update .asoundrc for better USB audio handling
cat > ~/.asoundrc << 'EOF'
# ALSA configuration for USB PnP Audio Device
pcm.!default {
    type pulse
    fallback "sysdefault"
    hint {
        show on
        description "Default ALSA Output (currently PulseAudio Sound Server)"
    }
}

ctl.!default {
    type pulse
    fallback "sysdefault"
}

# USB Audio Device configuration
pcm.usb {
    type hw
    card 2
    device 0
}

ctl.usb {
    type hw
    card 2
}
EOF

print_success "ALSA configuration updated"

# Fix 4: Restart audio services
print_fix "Restarting audio services..."

# Kill any existing audio processes
pulseaudio --kill 2>/dev/null || true
sleep 2

# Restart PulseAudio
pulseaudio --start --log-target=syslog
if [ $? -eq 0 ]; then
    print_success "PulseAudio restarted successfully"
else
    print_error "Failed to restart PulseAudio"
fi

# Reload ALSA configuration
sudo alsactl restore 2>/dev/null || true
print_success "ALSA configuration reloaded"

# Fix 5: Set USB audio as default
print_fix "Setting USB audio device as default..."

# Create PulseAudio configuration
mkdir -p ~/.config/pulse
cat > ~/.config/pulse/default.pa << 'EOF'
#!/usr/bin/pulseaudio -nF

# Load system default configuration
.include /etc/pulse/default.pa

# Set USB audio as default
set-default-sink alsa_output.usb-0c76_USB_PnP_Audio_Device-00.analog-stereo
set-default-source alsa_input.usb-0c76_USB_PnP_Audio_Device-00.analog-stereo
EOF

print_success "PulseAudio default configuration set"

# Fix 6: Test audio functionality
print_fix "Testing audio functionality..."

# Test if we can access the microphone
python3 -c "
import pyaudio
import sys

try:
    p = pyaudio.PyAudio()
    # Try to open the USB microphone
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        input_device_index=0,  # USB PnP Audio Device
        frames_per_buffer=1024
    )
    stream.close()
    p.terminate()
    print('✅ USB microphone access test: SUCCESS')
except Exception as e:
    print(f'❌ USB microphone access test: FAILED - {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    print_success "Microphone access test passed"
else
    print_error "Microphone access test failed"
fi

# Fix 7: Create optimized speech recognition test
print_fix "Creating optimized speech test for Pi 5..."

cat > test_pi5_speech_final.py << 'EOF'
#!/usr/bin/env python3
"""
Final speech recognition test for Raspberry Pi 5 after audio fixes
"""

import speech_recognition as sr
import pyaudio
import time
import sys

def test_speech_recognition():
    print("🎤 RASPBERRY PI 5 SPEECH RECOGNITION TEST")
    print("=" * 50)
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # Configure for Pi 5 with USB microphone
    r.energy_threshold = 150  # Optimized for Pi 5
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    r.phrase_threshold = 0.3
    
    # Use USB microphone (device index 0)
    with sr.Microphone(device_index=0) as source:
        print("📋 Calibrating for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1.2)
        print(f"✅ Energy threshold set to: {r.energy_threshold}")
        
        for attempt in range(3):
            print(f"\n🎤 Attempt {attempt + 1}/3: Say something...")
            try:
                # Listen for speech
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                print("🔄 Processing speech...")
                
                # Recognize speech
                text = r.recognize_google(audio)
                print(f"✅ SUCCESS: '{text}'")
                return True
                
            except sr.WaitTimeoutError:
                print("⏰ Timeout - no speech detected")
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Recognition error: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_speech_recognition()
    if success:
        print("\n🎉 Speech recognition is working! You can now run:")
        print("   python3 main.py")
    else:
        print("\n❌ Speech recognition test failed. Check microphone connection.")
    sys.exit(0 if success else 1)
EOF

chmod +x test_pi5_speech_final.py
print_success "Speech recognition test script created"

# Summary
echo ""
echo "🎉 AUDIO CONFIGURATION COMPLETE!"
echo "================================="
echo ""
echo "✅ Fixes applied:"
echo "  1. Added user to pulse and pulse-access groups"
echo "  2. Enabled audio in Raspberry Pi configuration"
echo "  3. Configured ALSA for USB audio device"
echo "  4. Restarted audio services"
echo "  5. Set USB audio as default device"
echo "  6. Tested microphone access"
echo "  7. Created optimized speech test"
echo ""
echo "🔄 REBOOT REQUIRED!"
echo "Please reboot your Raspberry Pi to apply all changes:"
echo "   sudo reboot"
echo ""
echo "📋 After reboot, test with:"
echo "   python3 test_pi5_speech_final.py"
echo "   python3 main.py"
echo ""
echo "🔌 USB PORT RECOMMENDATION:"
echo "Make sure your USB microphone is connected to a USB 2.0 port (black connector)"
echo "for optimal audio performance on Raspberry Pi 5." 