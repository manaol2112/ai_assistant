#!/bin/bash

# Raspberry Pi 5 Audio Fix Script for AI Assistant
# Automatically fixes common microphone and audio issues

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}🔊 $1${NC}"
    echo -e "${BLUE}============================================${NC}"
}

print_status() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_fix() {
    echo -e "${GREEN}🔧 $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should NOT be run as root. Run as regular user."
        exit 1
    fi
}

# Check if running on Raspberry Pi
check_raspberry_pi() {
    if [[ ! -f /proc/device-tree/model ]] || ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
        print_warning "This script is designed for Raspberry Pi. Some fixes may not apply."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        PI_MODEL=$(cat /proc/device-tree/model)
        print_success "Running on: $PI_MODEL"
    fi
}

# Update system packages
update_system() {
    print_header "UPDATING SYSTEM PACKAGES"
    print_status "Updating package lists..."
    sudo apt update
    
    print_status "Upgrading system packages..."
    sudo apt upgrade -y
    
    print_success "System packages updated!"
}

# Install audio system dependencies
install_audio_deps() {
    print_header "INSTALLING AUDIO DEPENDENCIES"
    
    print_status "Installing ALSA and PulseAudio..."
    sudo apt install -y \
        alsa-utils \
        pulseaudio \
        pulseaudio-utils \
        pavucontrol \
        portaudio19-dev \
        libasound2-dev \
        libportaudio2 \
        libportaudiocpp0 \
        espeak \
        espeak-data \
        flac \
        sox \
        libsox-fmt-all
    
    print_success "Audio dependencies installed!"
}

# Install Python audio libraries
install_python_audio() {
    print_header "INSTALLING PYTHON AUDIO LIBRARIES"
    
    # Check if we're in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        print_status "Using virtual environment: $VIRTUAL_ENV"
    else
        print_warning "No virtual environment detected. Consider using one."
        if [[ -d "ai_assistant_env" ]]; then
            print_status "Found ai_assistant_env directory. Activating..."
            source ai_assistant_env/bin/activate
        fi
    fi
    
    print_status "Installing system Python audio packages..."
    sudo apt install -y python3-pyaudio python3-pygame
    
    print_status "Installing pip audio packages..."
    pip install --upgrade pip
    pip install pyaudio pygame sounddevice soundfile speech_recognition
    
    print_success "Python audio libraries installed!"
}

# Configure user permissions
fix_permissions() {
    print_header "FIXING AUDIO PERMISSIONS"
    
    print_status "Adding user to audio groups..."
    sudo usermod -a -G audio,pulse,pulse-access $USER
    
    print_status "Checking current groups..."
    groups $USER
    
    print_success "User permissions updated!"
    print_warning "You may need to logout and login again for group changes to take effect."
}

# Configure Raspberry Pi audio
configure_pi_audio() {
    print_header "CONFIGURING RASPBERRY PI AUDIO"
    
    # Determine config file location
    if [[ -f /boot/firmware/config.txt ]]; then
        CONFIG_FILE="/boot/firmware/config.txt"
    elif [[ -f /boot/config.txt ]]; then
        CONFIG_FILE="/boot/config.txt"
    else
        print_error "Cannot find config.txt file!"
        return 1
    fi
    
    print_status "Using config file: $CONFIG_FILE"
    
    # Backup config file
    sudo cp $CONFIG_FILE ${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)
    print_status "Config file backed up"
    
    # Check if audio is already enabled
    if grep -q "dtparam=audio=on" $CONFIG_FILE; then
        print_status "Audio already enabled in config"
    else
        print_status "Enabling audio in config..."
        echo "dtparam=audio=on" | sudo tee -a $CONFIG_FILE
    fi
    
    # Set audio PWM mode
    if grep -q "audio_pwm_mode" $CONFIG_FILE; then
        print_status "Audio PWM mode already configured"
    else
        print_status "Setting audio PWM mode..."
        echo "audio_pwm_mode=2" | sudo tee -a $CONFIG_FILE
    fi
    
    # Enable I2C and SPI (often needed for audio devices)
    if ! grep -q "dtparam=i2c_arm=on" $CONFIG_FILE; then
        echo "dtparam=i2c_arm=on" | sudo tee -a $CONFIG_FILE
    fi
    
    if ! grep -q "dtparam=spi=on" $CONFIG_FILE; then
        echo "dtparam=spi=on" | sudo tee -a $CONFIG_FILE
    fi
    
    print_success "Raspberry Pi audio configuration updated!"
}

# Start and configure PulseAudio
setup_pulseaudio() {
    print_header "SETTING UP PULSEAUDIO"
    
    # Kill any existing PulseAudio processes
    print_status "Stopping existing PulseAudio processes..."
    pulseaudio --kill 2>/dev/null || true
    
    # Start PulseAudio
    print_status "Starting PulseAudio..."
    pulseaudio --start --log-target=syslog
    
    # Wait a moment for PulseAudio to initialize
    sleep 2
    
    # Check if PulseAudio is running
    if pulseaudio --check; then
        print_success "PulseAudio is running!"
    else
        print_error "PulseAudio failed to start"
        return 1
    fi
    
    # List audio sources
    print_status "Available audio sources:"
    pactl list sources short 2>/dev/null || print_warning "No audio sources found"
}

# Test microphone
test_microphone() {
    print_header "TESTING MICROPHONE"
    
    print_status "Checking ALSA recording devices..."
    if arecord -l | grep -q "card"; then
        print_success "ALSA recording devices found:"
        arecord -l
    else
        print_error "No ALSA recording devices found!"
        print_warning "Make sure a USB microphone is connected"
        return 1
    fi
    
    print_status "Testing microphone recording (5 seconds)..."
    print_warning "Please speak into your microphone now..."
    
    # Record a test file
    TEST_FILE="/tmp/test_recording.wav"
    if arecord -D hw:1,0 -f cd -t wav -d 5 $TEST_FILE 2>/dev/null; then
        print_success "Recording successful!"
        
        # Play back the recording
        print_status "Playing back recording..."
        aplay $TEST_FILE 2>/dev/null || print_warning "Playback failed (speakers may not be connected)"
        
        # Clean up
        rm -f $TEST_FILE
    else
        print_error "Recording failed!"
        print_warning "Try: arecord -l to see available devices"
        print_warning "Then: arecord -D hw:X,0 -f cd -t wav -d 5 test.wav (where X is your card number)"
    fi
}

# Test Python audio libraries
test_python_audio() {
    print_header "TESTING PYTHON AUDIO LIBRARIES"
    
    # Create a simple test script
    cat > /tmp/test_audio.py << 'EOF'
#!/usr/bin/env python3
import sys

def test_library(library_name, import_name):
    try:
        __import__(import_name)
        print(f"✅ {library_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {library_name} - FAILED: {e}")
        return False

def test_pyaudio():
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        input_devices = 0
        
        for i in range(device_count):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices += 1
        
        p.terminate()
        print(f"✅ PyAudio - Found {input_devices} input device(s)")
        return input_devices > 0
    except Exception as e:
        print(f"❌ PyAudio - FAILED: {e}")
        return False

def test_speech_recognition():
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mics = sr.Microphone.list_microphone_names()
        print(f"✅ SpeechRecognition - Found {len(mics)} microphone(s)")
        return len(mics) > 0
    except Exception as e:
        print(f"❌ SpeechRecognition - FAILED: {e}")
        return False

if __name__ == "__main__":
    print("Testing Python audio libraries...")
    
    libraries = [
        ("NumPy", "numpy"),
        ("Pygame", "pygame"),
        ("SoundDevice", "sounddevice"),
        ("SoundFile", "soundfile")
    ]
    
    for lib_name, import_name in libraries:
        test_library(lib_name, import_name)
    
    test_pyaudio()
    test_speech_recognition()
EOF

    # Run the test
    python3 /tmp/test_audio.py
    
    # Clean up
    rm -f /tmp/test_audio.py
}

# Create udev rules for USB microphones
create_udev_rules() {
    print_header "CREATING UDEV RULES FOR USB MICROPHONES"
    
    UDEV_RULE_FILE="/etc/udev/rules.d/99-usb-microphone.rules"
    
    print_status "Creating udev rules for USB microphones..."
    sudo tee $UDEV_RULE_FILE > /dev/null << 'EOF'
# USB Microphone udev rules
# Allow access to USB audio devices for audio group
SUBSYSTEM=="sound", GROUP="audio", MODE="0664"
SUBSYSTEM=="usb", ATTRS{bInterfaceClass}=="01", ATTRS{bInterfaceSubClass}=="01", GROUP="audio", MODE="0664"
SUBSYSTEM=="usb", ATTRS{bInterfaceClass}=="01", ATTRS{bInterfaceSubClass}=="02", GROUP="audio", MODE="0664"
EOF
    
    print_status "Reloading udev rules..."
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    
    print_success "USB microphone udev rules created!"
}

# Main execution
main() {
    print_header "RASPBERRY PI 5 AUDIO FIX SCRIPT"
    echo "This script will automatically fix common microphone issues"
    echo "for your AI Assistant on Raspberry Pi 5"
    echo ""
    
    # Checks
    check_root
    check_raspberry_pi
    
    # Ask for confirmation
    echo "This script will:"
    echo "  1. Update system packages"
    echo "  2. Install audio dependencies"
    echo "  3. Install Python audio libraries"
    echo "  4. Fix user permissions"
    echo "  5. Configure Raspberry Pi audio"
    echo "  6. Setup PulseAudio"
    echo "  7. Test microphone functionality"
    echo ""
    
    read -p "Continue with the fix? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Fix cancelled by user"
        exit 0
    fi
    
    # Execute fixes
    update_system
    install_audio_deps
    install_python_audio
    fix_permissions
    configure_pi_audio
    create_udev_rules
    setup_pulseaudio
    test_microphone
    test_python_audio
    
    print_header "FIX COMPLETE"
    print_success "Audio fix script completed!"
    print_warning "IMPORTANT: You may need to reboot your Raspberry Pi for all changes to take effect."
    print_warning "After reboot, test your AI Assistant microphone functionality."
    
    echo ""
    read -p "Reboot now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Rebooting..."
        sudo reboot
    else
        print_warning "Remember to reboot later to ensure all changes take effect!"
    fi
}

# Run main function
main "$@" 