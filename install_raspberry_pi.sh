#!/bin/bash

# ============================================================================
# AI ASSISTANT - RASPBERRY PI INSTALLATION SCRIPT
# Automated setup for easy Raspberry Pi deployment
# ============================================================================

set -e  # Exit on any error

echo "🤖 AI ASSISTANT - RASPBERRY PI SETUP"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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
}

# Check if running on Raspberry Pi
check_raspberry_pi() {
    print_status "Checking if running on Raspberry Pi..."
    if [[ -f /proc/device-tree/model ]] && grep -q "Raspberry Pi" /proc/device-tree/model; then
        print_success "Raspberry Pi detected!"
        PI_MODEL=$(cat /proc/device-tree/model)
        print_status "Model: $PI_MODEL"
    else
        print_warning "Not running on Raspberry Pi, but continuing anyway..."
    fi
}

# Update system packages
update_system() {
    print_status "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    print_success "System packages updated!"
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    # Core development tools
    sudo apt install -y \
        python3-pip \
        python3-dev \
        python3-venv \
        python3-setuptools \
        python3-wheel \
        build-essential \
        cmake \
        pkg-config \
        git
    
    # Audio dependencies
    sudo apt install -y \
        portaudio19-dev \
        libasound2-dev \
        pulseaudio \
        alsa-utils
    
    # Math and science libraries
    sudo apt install -y \
        libatlas-base-dev \
        libopenblas-dev \
        liblapack-dev \
        gfortran
    
    # Computer vision dependencies
    sudo apt install -y \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libgtk2.0-dev \
        libjpeg-dev \
        libtiff5-dev \
        libpng-dev \
        libv4l-dev \
        v4l-utils
    
    # HDF5 for data handling
    sudo apt install -y \
        libhdf5-dev \
        libhdf5-serial-dev
    
    print_success "System dependencies installed!"
}

# Setup Python virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ -d "ai_assistant_env" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf ai_assistant_env
    fi
    
    python3 -m venv ai_assistant_env
    source ai_assistant_env/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    print_success "Virtual environment created and activated!"
}

# Install Python packages with optimizations
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Ensure we're in the virtual environment
    source ai_assistant_env/bin/activate
    
    # Set compilation flags for Raspberry Pi
    export MAKEFLAGS="-j1"  # Single thread to avoid memory issues
    export CFLAGS="-O2"
    
    # Install packages in order of dependency
    print_status "Installing core dependencies..."
    pip install --no-cache-dir numpy>=1.21.0
    pip install --no-cache-dir scipy>=1.7.0
    
    print_status "Installing OpenAI and environment..."
    pip install --no-cache-dir openai>=1.0.0
    pip install --no-cache-dir python-dotenv>=0.19.0
    
    print_status "Installing audio processing..."
    pip install --no-cache-dir pyaudio>=0.2.13
    pip install --no-cache-dir SpeechRecognition>=3.10.0
    pip install --no-cache-dir pyttsx3>=2.90
    pip install --no-cache-dir pygame>=2.1.0
    
    print_status "Installing computer vision..."
    pip install --no-cache-dir Pillow>=9.0.0
    pip install --no-cache-dir opencv-python-headless>=4.8.0  # Headless for better Pi performance
    
    print_status "Installing face recognition (this may take a while)..."
    pip install --no-cache-dir dlib>=19.24.0
    pip install --no-cache-dir face-recognition>=1.3.0
    
    print_status "Installing PyTorch (CPU version for Raspberry Pi)..."
    pip install --no-cache-dir torch>=2.0.0 torchvision>=0.15.0 --extra-index-url https://download.pytorch.org/whl/cpu
    
    print_status "Installing YOLO object detection..."
    pip install --no-cache-dir ultralytics>=8.0.0
    
    print_status "Installing system utilities..."
    pip install --no-cache-dir psutil>=5.9.0
    pip install --no-cache-dir requests>=2.28.0
    
    # Raspberry Pi GPIO (only on Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_status "Installing Raspberry Pi GPIO..."
        pip install --no-cache-dir RPi.GPIO>=0.7.1
    fi
    
    # Optional: Wake word detection (requires Picovoice account)
    print_status "Installing wake word detection (optional)..."
    pip install --no-cache-dir pvporcupine>=3.0.0 || print_warning "Wake word detection installation failed (optional)"
    
    print_success "Python dependencies installed!"
}

# Setup camera permissions
setup_camera() {
    print_status "Setting up camera permissions..."
    
    # Add user to video group
    sudo usermod -a -G video $USER
    
    # Enable camera interface
    if command -v raspi-config &> /dev/null; then
        print_status "Enabling camera interface..."
        sudo raspi-config nonint do_camera 0
    fi
    
    print_success "Camera permissions configured!"
    print_warning "You may need to logout and login again for camera permissions to take effect."
}

# Create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    
    if [ ! -f ".env" ]; then
        cp env_example.txt .env
        print_success "Environment file created from template!"
        print_warning "Please edit .env file and add your OpenAI API key and other settings."
    else
        print_warning ".env file already exists, skipping creation."
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    source ai_assistant_env/bin/activate
    
    # Test Python imports
    python3 -c "
import sys
print(f'Python version: {sys.version}')

try:
    import openai
    print('✓ OpenAI imported successfully')
except ImportError as e:
    print(f'✗ OpenAI import failed: {e}')

try:
    import speech_recognition
    print('✓ Speech Recognition imported successfully')
except ImportError as e:
    print(f'✗ Speech Recognition import failed: {e}')

try:
    import cv2
    print('✓ OpenCV imported successfully')
except ImportError as e:
    print(f'✗ OpenCV import failed: {e}')

try:
    import face_recognition
    print('✓ Face Recognition imported successfully')
except ImportError as e:
    print(f'✗ Face Recognition import failed: {e}')

try:
    import ultralytics
    print('✓ Ultralytics imported successfully')
except ImportError as e:
    print(f'✗ Ultralytics import failed: {e}')

try:
    import pygame
    print('✓ Pygame imported successfully')
except ImportError as e:
    print(f'✗ Pygame import failed: {e}')
"
    
    print_success "Installation test completed!"
}

# Main installation process
main() {
    echo "Starting AI Assistant installation for Raspberry Pi..."
    echo "This process may take 30-60 minutes depending on your Pi model."
    echo ""
    
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    
    check_raspberry_pi
    update_system
    install_system_deps
    setup_venv
    install_python_deps
    setup_camera
    create_env_file
    test_installation
    
    echo ""
    print_success "🎉 AI Assistant installation completed!"
    echo ""
    echo "Next steps:"
    echo "1. Edit the .env file and add your OpenAI API key"
    echo "2. Logout and login again for camera permissions"
    echo "3. Activate the virtual environment: source ai_assistant_env/bin/activate"
    echo "4. Run the assistant: python main.py"
    echo ""
    echo "For troubleshooting, check the comments in requirements.txt"
}

# Run main function
main "$@" 