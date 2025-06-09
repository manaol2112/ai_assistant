# 🤖 AI Assistant - Smart Camera & Voice Assistant

A sophisticated AI-powered assistant that combines computer vision, speech recognition, and natural language processing to create an interactive experience for children and families.

## 🌟 Features

- **Face Recognition**: Personalized interactions for Sophia and Eladriel
- **Object Identification**: Advanced object detection with educational information
- **Dinosaur Recognition**: Specialized dinosaur identification for educational fun
- **Voice Interaction**: Natural speech recognition and text-to-speech
- **Smart Camera**: Real-time camera processing and image capture
- **Wake Word Detection**: Hands-free activation with "Miley" and "Dino"
- **Educational Content**: Age-appropriate learning materials and fun facts
- **Raspberry Pi Optimized**: Efficient performance on low-power devices

## 🚀 Quick Installation (Raspberry Pi)

For Raspberry Pi users, we provide an automated installation script:

```bash
# Clone the repository
git clone https://github.com/manaol2112/ai_assistant.git
cd ai_assistant

# Run the automated installer
./install_raspberry_pi.sh
```

The script will:
- Install all system dependencies
- Set up Python virtual environment
- Install all required packages with Pi optimizations
- Configure camera permissions
- Test the installation

## 📋 Manual Installation

### Prerequisites

- Python 3.8 or higher
- Camera (USB webcam or Raspberry Pi camera)
- Microphone and speakers
- OpenAI API key

### System Dependencies

**Ubuntu/Debian/Raspberry Pi OS:**
```bash
sudo apt update
sudo apt install -y python3-pip python3-dev python3-venv build-essential cmake pkg-config
sudo apt install -y portaudio19-dev libasound2-dev pulseaudio alsa-utils
sudo apt install -y libatlas-base-dev libopenblas-dev liblapack-dev gfortran
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libgtk2.0-dev
sudo apt install -y libjpeg-dev libtiff5-dev libpng-dev libv4l-dev v4l-utils
sudo apt install -y libhdf5-dev libhdf5-serial-dev
```

**macOS:**
```bash
brew install portaudio cmake pkg-config
```

### Python Setup

1. **Clone the repository:**
```bash
git clone https://github.com/manaol2112/ai_assistant.git
cd ai_assistant
```

2. **Create virtual environment:**
```bash
python3 -m venv ai_assistant_env
source ai_assistant_env/bin/activate  # On Windows: ai_assistant_env\Scripts\activate
```

3. **Install Python dependencies:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Configuration

1. **Create environment file:**
```bash
cp env_example.txt .env
```

2. **Edit `.env` file and add your settings:**
```env
OPENAI_API_KEY=your_openai_api_key_here
PICOVOICE_ACCESS_KEY=your_picovoice_key_here  # Optional for wake word
```

## 🎯 Usage

### Basic Usage

```bash
# Activate virtual environment
source ai_assistant_env/bin/activate

# Run the main assistant
python main.py
```

### Testing Components

```bash
# Test object identification
python test_object_identification.py

# Test face recognition
python test_face_recognition.py

# Test dinosaur identification
python test_dinosaur_camera.py

# Test camera functionality
python test_camera.py

# Test conversation mode
python test_conversation.py
```

## 🔧 Configuration Options

The assistant can be configured through the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PICOVOICE_ACCESS_KEY`: For wake word detection (optional)
- `CAMERA_INDEX`: Camera device index (default: 0)
- `AUDIO_DEVICE_INDEX`: Audio input device index (optional)

## 📁 Project Structure

```
ai_assistant/
├── main.py                     # Main application entry point
├── object_identifier.py        # Object identification system
├── dinosaur_identifier.py      # Dinosaur-specific identification
├── audio_utils.py             # Audio processing utilities
├── camera_utils.py            # Camera handling utilities
├── wake_word_detector.py      # Wake word detection
├── smart_camera_detector.py   # Smart camera processing
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── install_raspberry_pi.sh    # Automated Pi installer
├── people/                    # Face recognition data
│   ├── sophia/               # Sophia's face data
│   └── eladriel/            # Eladriel's face data
└── test_*.py                 # Various test scripts
```

## 🎮 Interactive Features

### Wake Words
- **"Miley"** for Sophia - responds with personalized greeting
- **"Dino"** for Eladriel - responds with personalized greeting

### For Sophia (Age-appropriate content):
- Simple object identification
- Basic educational facts
- Encouraging and supportive responses
- Visual learning emphasis

### For Eladriel (Advanced content):
- Detailed scientific explanations
- Historical context and trivia
- Complex vocabulary and concepts
- Critical thinking questions

### Dinosaur Mode:
- Specialized dinosaur identification
- Paleontological facts
- Prehistoric timeline information
- Interactive learning games

## 🛠️ Troubleshooting

### Common Issues

**Camera not working:**
```bash
# Check camera permissions
ls /dev/video*
# Add user to video group
sudo usermod -a -G video $USER
```

**Audio issues:**
```bash
# Test audio devices
python -c "import pyaudio; p=pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

**Memory issues on Raspberry Pi:**
```bash
# Increase swap space
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

**Package installation failures:**
```bash
# For face_recognition on Pi
sudo apt install -y libopenblas-dev liblapack-dev
pip install --no-cache-dir dlib
pip install --no-cache-dir face-recognition
```

### Performance Optimization

**For Raspberry Pi 4:**
- Use `opencv-python-headless` instead of `opencv-python`
- Enable GPU memory split: `sudo raspi-config` → Advanced → Memory Split → 128
- Use CPU-only PyTorch version

**For older Pi models:**
- Reduce camera resolution in `camera_utils.py`
- Increase processing delays
- Consider using lighter models

## 🔒 Privacy & Security

- All face recognition data is stored locally
- No personal data is sent to external services except OpenAI API calls
- Camera images are processed locally and not stored permanently
- Environment variables keep API keys secure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision API
- Ultralytics for YOLO object detection
- Face Recognition library by Adam Geitgey
- Raspberry Pi Foundation for amazing hardware

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test scripts for examples
3. Check the GitHub issues page
4. Ensure all dependencies are properly installed

---

**Happy Learning! 🎓🤖** 