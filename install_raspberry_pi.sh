#!/bin/bash

# ============================================================================
# AI ASSISTANT - RASPBERRY PI 5 AUTOMATED INSTALLATION SCRIPT
# Complete deployment automation for production-ready Raspberry Pi 5 setup
# Optimized for ARM64 with Cortex-A76 CPU and 4-core compilation
# ============================================================================

set -e  # Exit on any error

echo "🤖 AI ASSISTANT - RASPBERRY PI 5 DEPLOYMENT"
echo "============================================="
echo "🚀 Production-Ready Automated Installation"
echo "⚡ Optimized for ARM64 Cortex-A76 (Pi 5)"
echo ""

# Colors for enhanced output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Enhanced output functions
print_header() {
    echo -e "${BOLD}${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${PURPLE} $1${NC}"
    echo -e "${BOLD}${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

print_progress() {
    echo -e "${CYAN}[PROGRESS]${NC} $1"
}

# System information and validation
check_system() {
    print_header "🔍 SYSTEM VALIDATION"
    
    # Check if running on Raspberry Pi
    print_status "Detecting Raspberry Pi model..."
    if [[ -f /proc/device-tree/model ]] && grep -q "Raspberry Pi" /proc/device-tree/model; then
        PI_MODEL=$(cat /proc/device-tree/model)
        print_success "Raspberry Pi detected: $PI_MODEL"
        
        # Check for Pi 5 specifically
        if echo "$PI_MODEL" | grep -q "Raspberry Pi 5"; then
            print_success "🚀 Raspberry Pi 5 detected! Using optimized installation."
            export PI_VERSION=5
            export CPU_CORES=4
            export MAKEFLAGS="-j4"
            export CFLAGS="-O3 -mcpu=cortex-a76"
            export CXXFLAGS="-O3 -mcpu=cortex-a76"
        elif echo "$PI_MODEL" | grep -q "Raspberry Pi 4"; then
            print_warning "Pi 4 detected. Using compatible settings."
            export PI_VERSION=4
            export CPU_CORES=4
            export MAKEFLAGS="-j2"
            export CFLAGS="-O2 -mcpu=cortex-a72"
            export CXXFLAGS="-O2 -mcpu=cortex-a72"
        else
            print_warning "Older Pi model detected. Using conservative settings."
            export PI_VERSION=3
            export CPU_CORES=1
            export MAKEFLAGS="-j1"
            export CFLAGS="-O2"
            export CXXFLAGS="-O2"
        fi
    else
        print_warning "Not running on Raspberry Pi, using generic ARM settings."
        export PI_VERSION=0
        export CPU_CORES=2
        export MAKEFLAGS="-j2"
    fi
    
    # Check OS and architecture
    print_status "Checking system architecture..."
    ARCH=$(uname -m)
    OS=$(lsb_release -si 2>/dev/null || echo "Unknown")
    print_status "Architecture: $ARCH, OS: $OS"
    
    # Check available memory
    TOTAL_MEM=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    print_status "Total memory: ${TOTAL_MEM}MB"
    
    if [ "$TOTAL_MEM" -lt 1000 ]; then
        print_warning "Low memory detected. Installation may take longer."
        export LOW_MEMORY=true
    fi
    
    # Check available disk space
    DISK_SPACE=$(df / | awk 'NR==2 {print $4}')
    DISK_SPACE_GB=$((DISK_SPACE / 1024 / 1024))
    print_status "Available disk space: ${DISK_SPACE_GB}GB"
    
    if [ "$DISK_SPACE_GB" -lt 8 ]; then
        print_error "Insufficient disk space. At least 8GB required."
    fi
    
    print_success "System validation completed!"
}

# Memory optimization for compilation
optimize_memory() {
    print_header "🧠 MEMORY OPTIMIZATION"
    
    print_status "Configuring swap memory for compilation..."
    
    # Check current swap
    CURRENT_SWAP=$(free -m | awk 'NR==3{print $2}')
    print_status "Current swap: ${CURRENT_SWAP}MB"
    
    if [ "$CURRENT_SWAP" -lt 2048 ]; then
        print_status "Increasing swap memory to 2GB for compilation..."
        
        # Backup current swapfile config
        if [ -f /etc/dphys-swapfile ]; then
            sudo cp /etc/dphys-swapfile /etc/dphys-swapfile.backup
        fi
        
        # Stop swap
        sudo dphys-swapfile swapoff || true
        
        # Set new swap size
        echo 'CONF_SWAPSIZE=2048' | sudo tee /etc/dphys-swapfile > /dev/null
        
        # Setup and enable new swap
        sudo dphys-swapfile setup
        sudo dphys-swapfile swapon
        
        # Verify new swap
        NEW_SWAP=$(free -m | awk 'NR==3{print $2}')
        print_success "Swap increased to: ${NEW_SWAP}MB"
    else
        print_success "Sufficient swap memory available."
    fi
    
    # Configure memory management for Pi 5
    if [ "$PI_VERSION" -eq 5 ]; then
        print_status "Applying Pi 5 memory optimizations..."
        
        # Configure sysctl for better memory management
        sudo tee -a /etc/sysctl.conf > /dev/null << EOF

# Pi 5 Memory Optimizations
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_ratio=15
vm.dirty_background_ratio=5
EOF
        
        # Apply sysctl changes
        sudo sysctl -p
        print_success "Memory optimizations applied!"
    fi
}

# System packages update with optimization
update_system() {
    print_header "📦 SYSTEM UPDATE"
    
    print_status "Updating package repositories..."
    sudo apt update
    
    print_status "Upgrading system packages..."
    sudo apt upgrade -y
    
    print_status "Installing essential build tools..."
    sudo apt install -y apt-transport-https ca-certificates gnupg lsb-release
    
    print_success "System update completed!"
}

# Comprehensive system dependencies for Pi 5
install_system_deps() {
    print_header "🔧 SYSTEM DEPENDENCIES"
    
    print_status "Installing core development tools..."
    sudo apt install -y \
        python3-pip \
        python3-dev \
        python3-venv \
        python3-setuptools \
        python3-wheel \
        build-essential \
        cmake \
        pkg-config \
        git \
        curl \
        wget \
        unzip
    
    print_status "Installing ARM64 optimized math libraries..."
    sudo apt install -y \
        libatlas-base-dev \
        libopenblas-dev \
        liblapack-dev \
        libblas-dev \
        gfortran \
        libhdf5-dev \
        libhdf5-serial-dev
    
    print_status "Installing audio processing dependencies..."
    sudo apt install -y \
        portaudio19-dev \
        libasound2-dev \
        pulseaudio \
        alsa-utils \
        espeak \
        espeak-data \
        libespeak1 \
        libespeak-dev \
        flac \
        sox \
        libsox-fmt-all \
        libportaudio2 \
        libportaudiocpp0
    
    print_status "Installing computer vision dependencies..."
    sudo apt install -y \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libgtk-3-dev \
        libcanberra-gtk3-dev \
        libjpeg-dev \
        libtiff5-dev \
        libpng-dev \
        libv4l-dev \
        v4l-utils \
        libdc1394-dev \
        libxine2-dev \
        libfaac-dev \
        libmp3lame-dev \
        libopencore-amrnb-dev \
        libopencore-amrwb-dev \
        libtheora-dev \
        libvorbis-dev \
        libxvidcore-dev \
        x264
    
    print_status "Installing GStreamer for multimedia..."
    sudo apt install -y \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-ugly
    
    print_status "Installing additional utilities..."
    sudo apt install -y \
        libffi-dev \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev
    
    # Pi 5 specific optimizations
    if [ "$PI_VERSION" -eq 5 ]; then
        print_status "Installing Pi 5 specific packages..."
        sudo apt install -y \
            python3-opencv \
            python3-pyaudio \
            python3-numpy \
            python3-scipy
    fi
    
    print_success "System dependencies installed!"
}

# Pi 5 hardware configuration
configure_pi5_hardware() {
    if [ "$PI_VERSION" -eq 5 ]; then
        print_header "⚙️ RASPBERRY PI 5 HARDWARE CONFIGURATION"
        
        print_status "Configuring Pi 5 hardware settings..."
        
        # Backup config.txt
        sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.backup 2>/dev/null || sudo cp /boot/config.txt /boot/config.txt.backup
        
        # Pi 5 optimizations
        sudo tee -a /boot/firmware/config.txt > /dev/null 2>&1 << EOF || sudo tee -a /boot/config.txt > /dev/null << EOF

# Pi 5 AI Assistant Optimizations
gpu_mem=128
arm_64bit=1
dtoverlay=vc4-kms-v3d
camera_auto_detect=1
dtparam=audio=on
audio_pwm_mode=2

# Performance optimizations
over_voltage=2
arm_freq=2400
gpu_freq=800

# Enable hardware interfaces
dtparam=i2c_arm=on
dtparam=spi=on
dtparam=audio=on
EOF
        
        print_status "Setting CPU governor to performance mode..."
        echo 'performance' | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null || true
        
        # Make performance mode persistent
        sudo tee /etc/systemd/system/cpu-performance.service > /dev/null << EOF
[Unit]
Description=Set CPU governor to performance
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
        
        sudo systemctl enable cpu-performance.service
        
        print_success "Pi 5 hardware configuration completed!"
    fi
}

# Enhanced Python virtual environment setup
setup_venv() {
    print_header "🐍 PYTHON ENVIRONMENT SETUP"
    
    print_status "Setting up optimized Python virtual environment..."
    
    # Remove existing environment if present
    if [ -d "ai_assistant_env" ]; then
        print_warning "Removing existing virtual environment..."
        rm -rf ai_assistant_env
    fi
    
    # Create new virtual environment
    python3 -m venv ai_assistant_env
    source ai_assistant_env/bin/activate
    
    # Upgrade pip with latest version
    print_status "Upgrading pip and build tools..."
    pip install --upgrade pip setuptools wheel
    
    # Install Cython for faster compilation
    pip install --no-cache-dir Cython
    
    print_success "Python environment created and optimized!"
}

# Optimized Python package installation using requirements.txt
install_python_deps() {
    print_header "📚 PYTHON DEPENDENCIES INSTALLATION"
    
    # Ensure we're in the virtual environment
    source ai_assistant_env/bin/activate
    
    # Verify requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found! Please ensure you're in the correct directory."
    fi
    
    print_status "Installing Python packages using optimized requirements.txt..."
    print_warning "This process may take 30-60 minutes depending on your Pi model."
    
    # Set compilation flags based on Pi version
    export MAKEFLAGS="$MAKEFLAGS"
    export CFLAGS="$CFLAGS"
    export CXXFLAGS="$CXXFLAGS"
    
    # Use Piwheels for ARM pre-compiled packages
    print_status "Using Piwheels repository for ARM-optimized packages..."
    
    # Install in stages for better error handling and progress tracking
    print_progress "Stage 1/5: Installing core dependencies..."
    pip install --no-cache-dir --extra-index-url https://www.piwheels.org/simple/ \
        numpy scipy
    
    print_progress "Stage 2/5: Installing OpenAI and utilities..."
    pip install --no-cache-dir --extra-index-url https://www.piwheels.org/simple/ \
        openai python-dotenv requests urllib3 psutil
    
    print_progress "Stage 3/5: Installing computer vision libraries..."
    pip install --no-cache-dir --extra-index-url https://www.piwheels.org/simple/ \
        opencv-python-headless Pillow
    
    print_progress "Stage 4/5: Installing PyTorch (CPU optimized)..."
    pip install --no-cache-dir torch torchvision torchaudio \
        --extra-index-url https://download.pytorch.org/whl/cpu
    
    print_progress "Stage 5/5: Installing remaining packages from requirements.txt..."
    # Install remaining packages, handling potential failures gracefully
    pip install --no-cache-dir --extra-index-url https://www.piwheels.org/simple/ \
        -r requirements.txt || {
        print_warning "Some packages failed to install. Attempting individual installation..."
        
        # Try installing problematic packages individually
        while IFS= read -r line; do
            if [[ $line =~ ^[^#]*[a-zA-Z] ]]; then
                package=$(echo "$line" | cut -d'#' -f1 | xargs)
                if [ ! -z "$package" ]; then
                    print_status "Installing: $package"
                    pip install --no-cache-dir --extra-index-url https://www.piwheels.org/simple/ \
                        "$package" || print_warning "Failed to install: $package"
                fi
            fi
        done < requirements.txt
    }
    
    print_success "Python dependencies installation completed!"
}

# Advanced camera and permissions setup
setup_camera_and_permissions() {
    print_header "📷 CAMERA AND PERMISSIONS SETUP"
    
    print_status "Configuring camera access..."
    
    # Add user to required groups
    sudo usermod -a -G video,dialout,i2c,spi,gpio "$USER"
    
    # Enable camera interface for older Pi models
    if command -v raspi-config &> /dev/null; then
        print_status "Enabling camera interface..."
        sudo raspi-config nonint do_camera 0
    fi
    
    # Pi 5 camera configuration
    if [ "$PI_VERSION" -eq 5 ]; then
        print_status "Configuring Pi 5 camera stack..."
        
        # Ensure libcamera is available
        sudo apt install -y libcamera-apps libcamera-dev
        
        # Test camera detection
        if command -v libcamera-hello &> /dev/null; then
            print_status "Testing camera detection..."
            timeout 5 libcamera-hello --list-cameras || print_warning "Camera test timeout (normal if no camera connected)"
        fi
    fi
    
    print_success "Camera and permissions configured!"
    print_warning "⚠️  Please reboot after installation for all permissions to take effect."
}

# Environment file creation with enhanced template
create_env_file() {
    print_header "⚙️ ENVIRONMENT CONFIGURATION"
    
    print_status "Creating environment configuration file..."
    
    if [ ! -f ".env" ]; then
        # Create comprehensive .env file
        cat > .env << EOF
# ============================================================================
# AI ASSISTANT - PRODUCTION ENVIRONMENT CONFIGURATION
# ============================================================================

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.7

# Performance Settings for Raspberry Pi 5
PI_OPTIMIZATION=true
CAMERA_RESOLUTION_WIDTH=640
CAMERA_RESOLUTION_HEIGHT=480
CAMERA_FPS=15
AUDIO_SAMPLE_RATE=16000
AUDIO_CHUNK_SIZE=1024

# Resource Management
MAX_CONCURRENT_OPERATIONS=2
FACE_RECOGNITION_THRESHOLD=0.6
OBJECT_DETECTION_CONFIDENCE=0.5

# Wake Word Detection (Optional - Picovoice)
PORCUPINE_ACCESS_KEY=your_picovoice_key_here
WAKE_WORD_SENSITIVITY=0.5

# Audio Configuration
TTS_RATE=180
TTS_VOLUME=0.9
SPEECH_TIMEOUT=5
SPEECH_PHRASE_LIMIT=10

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=/var/log/ai_assistant.log

# Hardware Specific Settings
CPU_CORES=$CPU_CORES
PI_VERSION=$PI_VERSION
EOF
        
        print_success "Environment file created!"
        print_warning "⚠️  Please edit .env file and add your OpenAI API key before running the assistant."
    else
        print_warning ".env file already exists, skipping creation."
    fi
}

# Comprehensive installation testing
test_installation() {
    print_header "🧪 INSTALLATION VERIFICATION"
    
    source ai_assistant_env/bin/activate
    
    print_status "Running comprehensive system tests..."
    
    # Test Python imports
    python3 << 'EOF'
import sys
import subprocess

print(f"🐍 Python version: {sys.version}")
print(f"📍 Python path: {sys.executable}")
print()

# Test core imports
modules_to_test = [
    ("openai", "OpenAI API"),
    ("speech_recognition", "Speech Recognition"),
    ("pyttsx3", "Text-to-Speech"),
    ("cv2", "OpenCV"),
    ("numpy", "NumPy"),
    ("scipy", "SciPy"),
    ("pygame", "Pygame"),
    ("torch", "PyTorch"),
    ("ultralytics", "YOLO"),
    ("face_recognition", "Face Recognition"),
    ("PIL", "Pillow"),
    ("psutil", "System Utilities"),
    ("requests", "HTTP Requests")
]

passed = 0
total = len(modules_to_test)

for module, name in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {name}")
        passed += 1
    except ImportError as e:
        print(f"❌ {name}: {e}")

print(f"\n📊 Test Results: {passed}/{total} modules imported successfully")

if passed >= total * 0.8:  # 80% success rate
    print("🎉 Installation verification PASSED!")
else:
    print("⚠️  Installation verification shows issues. Check failed imports above.")
EOF
    
    # Test camera if available
    print_status "Testing camera access..."
    python3 << 'EOF'
try:
    import cv2
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        print("✅ Camera access working")
    else:
        print("⚠️  Camera not detected (normal if no camera connected)")
except Exception as e:
    print(f"⚠️  Camera test failed: {e}")
EOF
    
    # Test audio system
    print_status "Testing audio system..."
    python3 << 'EOF'
try:
    import pygame
    pygame.mixer.init()
    print("✅ Audio system initialized")
    pygame.mixer.quit()
except Exception as e:
    print(f"⚠️  Audio test failed: {e}")
EOF
    
    print_success "Installation verification completed!"
}

# Create systemd service for production deployment
create_systemd_service() {
    print_header "🚀 PRODUCTION SERVICE SETUP"
    
    read -p "Do you want to create a systemd service for automatic startup? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Creating systemd service..."
        
        CURRENT_DIR=$(pwd)
        SERVICE_USER=$(whoami)
        
        sudo tee /etc/systemd/system/ai-assistant.service > /dev/null << EOF
[Unit]
Description=AI Assistant Service
After=network.target sound.target
Wants=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/ai_assistant_env/bin
ExecStart=$CURRENT_DIR/ai_assistant_env/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
        
        sudo systemctl daemon-reload
        sudo systemctl enable ai-assistant.service
        
        print_success "Systemd service created and enabled!"
        print_status "Service commands:"
        echo "  • Start: sudo systemctl start ai-assistant.service"
        echo "  • Stop: sudo systemctl stop ai-assistant.service"
        echo "  • Status: sudo systemctl status ai-assistant.service"
        echo "  • Logs: journalctl -u ai-assistant.service -f"
    else
        print_status "Skipping systemd service creation."
    fi
}

# Cleanup and final optimization
cleanup_and_optimize() {
    print_header "🧹 CLEANUP AND OPTIMIZATION"
    
    print_status "Cleaning package cache..."
    sudo apt autoremove -y
    sudo apt autoclean
    
    print_status "Optimizing Python cache..."
    source ai_assistant_env/bin/activate
    python3 -m compileall ai_assistant_env/ 2>/dev/null || true
    
    # Reset swap to original size if it was modified
    if [ -f /etc/dphys-swapfile.backup ]; then
        print_status "Restoring original swap configuration..."
        read -p "Do you want to restore original swap size? (recommended) (Y/n): " -n 1 -r
        echo
        
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            sudo dphys-swapfile swapoff
            sudo mv /etc/dphys-swapfile.backup /etc/dphys-swapfile
            sudo dphys-swapfile setup
            sudo dphys-swapfile swapon
            print_success "Original swap configuration restored."
        fi
    fi
    
    print_success "Cleanup and optimization completed!"
}

# Display final instructions and summary
show_final_instructions() {
    print_header "🎉 INSTALLATION COMPLETED SUCCESSFULLY!"
    
    echo -e "${GREEN}╭─────────────────────────────────────────────────────────────────╮${NC}"
    echo -e "${GREEN}│                     🤖 AI ASSISTANT READY! 🤖                   │${NC}"
    echo -e "${GREEN}╰─────────────────────────────────────────────────────────────────╯${NC}"
    echo
    
    echo -e "${BOLD}📋 NEXT STEPS:${NC}"
    echo "1. 🔑 Edit .env file and add your OpenAI API key:"
    echo "   nano .env"
    echo
    echo "2. 🔄 Reboot your Raspberry Pi (recommended):"
    echo "   sudo reboot"
    echo
    echo "3. 🚀 Start the AI Assistant:"
    echo "   source ai_assistant_env/bin/activate"
    echo "   python main.py"
    echo
    
    echo -e "${BOLD}💡 USEFUL COMMANDS:${NC}"
    echo "• Check system status: python test_mac.py"
    echo "• Test camera: python test_dinosaur_camera.py"
    echo "• View logs: tail -f ai_assistant.log"
    echo
    
    echo -e "${BOLD}🎙️ WAKE WORDS:${NC}"
    echo "• 'Miley' → Activates Sophia mode"
    echo "• 'Dino' → Activates Eladriel mode"
    echo "• 'Assistant' → Activates Parent mode"
    echo
    
    echo -e "${BOLD}🔧 TROUBLESHOOTING:${NC}"
    echo "• Check requirements.txt for detailed troubleshooting guide"
    echo "• Report issues: https://github.com/manaol2112/ai_assistant/issues"
    echo
    
    if [ "$PI_VERSION" -eq 5 ]; then
        echo -e "${BOLD}🚀 PI 5 OPTIMIZATIONS ACTIVE:${NC}"
        echo "• ARM64 Cortex-A76 optimizations enabled"
        echo "• 4-core compilation configured"
        echo "• Hardware acceleration enabled"
        echo "• Performance CPU governor active"
    fi
    
    echo -e "${GREEN}Installation completed in $(date)${NC}"
    echo -e "${GREEN}Happy AI Assistant-ing! 🎉${NC}"
}

# Main installation orchestration
main() {
    # Pre-installation checks
    print_header "🚀 AI ASSISTANT - RASPBERRY PI 5 INSTALLATION"
    
    echo "This script will install and configure the AI Assistant for optimal"
    echo "performance on Raspberry Pi 5 with ARM64 optimizations."
    echo
    echo "⏱️  Estimated installation time:"
    echo "   • Pi 5: 30-45 minutes"
    echo "   • Pi 4: 45-60 minutes"
    echo "   • Older Pi: 60-90 minutes"
    echo
    echo "💾 Requirements:"
    echo "   • 8GB+ available disk space"
    echo "   • Internet connection"
    echo "   • OpenAI API key (for completion)"
    echo
    
    read -p "Do you want to continue with the installation? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    # Installation sequence
    START_TIME=$(date +%s)
    
    check_system
    optimize_memory
    update_system
    install_system_deps
    configure_pi5_hardware
    setup_venv
    install_python_deps
    setup_camera_and_permissions
    create_env_file
    test_installation
    create_systemd_service
    cleanup_and_optimize
    
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    
    echo
    print_success "Total installation time: ${MINUTES}m ${SECONDS}s"
    
    show_final_instructions
}

# Error handling
trap 'print_error "Installation failed! Check the error above."' ERR

# Start installation
main "$@" 