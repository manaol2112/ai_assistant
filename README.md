# 🤖 AI Assistant for Sophia and Eladriel

A personalized AI assistant designed specifically for Sophia and Eladriel, with custom wake words and OpenAI integration. Optimized for easy deployment on Raspberry Pi.

## ✨ Features

- **Personalized Wake Words:**
  - "Miley" for Sophia - responds with "Hello Sophia, what can I do for you?"
  - "Dino" for Eladriel - responds with "Hello Eladriel, what can I do for you?"
- **OpenAI Integration:** Uses GPT-3.5-turbo for intelligent responses
- **Child-Friendly:** Age-appropriate and educational responses
- **Raspberry Pi Optimized:** Efficient performance on low-power devices
- **Easy Deployment:** One-click setup script for Raspberry Pi
- **Multi-User Support:** Different voice settings for each child
- **Continuous Listening:** Always ready to respond to wake words

## 🚀 Quick Start

### Prerequisites

- Raspberry Pi (3B+ or newer recommended)
- Microphone (USB or HAT)
- Speaker or headphones
- Internet connection
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai_assistant
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup_raspberry_pi.sh
   ./setup_raspberry_pi.sh
   ```

3. **Configure your API key:**
   ```bash
   nano .env
   # Add your OpenAI API key: OPENAI_API_KEY=your_key_here
   ```

4. **Activate the virtual environment:**
   ```bash
   source ai_assistant_env/bin/activate
   ```

5. **Test the installation:**
   ```bash
   python test_assistant.py
   ```

6. **Start the assistant:**
   ```bash
   python main.py
   ```

## 📖 Usage

### Wake Words

- **For Sophia:** Say "Miley" to activate
- **For Eladriel:** Say "Dino" to activate

### Example Interaction

1. Say "Miley" (wake word)
2. Assistant responds: "Hello Sophia, what can I do for you?"
3. Ask your question: "What's the weather like?"
4. Assistant provides an answer
5. Returns to listening for wake words

### Voice Commands

The assistant can help with:
- Answering questions
- Educational content
- Storytelling
- Math problems
- General conversation
- Fun facts

## ⚙️ Configuration

### Environment Variables (.env file)

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional Customization
OPENAI_MODEL=gpt-3.5-turbo
TTS_RATE=180
WAKE_WORD_SENSITIVITY=0.5
PI_OPTIMIZATION=true
```

### Audio Settings

The assistant automatically detects and configures your microphone. For manual configuration:

```bash
# Test microphone
arecord -l

# Test speaker
speaker-test -t sine -f 1000 -l 1
```

## 🔧 Advanced Setup

### Auto-Start on Boot

Enable the systemd service to start automatically:

```bash
sudo systemctl enable ai-assistant.service
sudo systemctl start ai-assistant.service
```

Check status:
```bash
sudo systemctl status ai-assistant.service
```

### Performance Tuning

For better performance on Raspberry Pi:

1. **Increase swap space:**
   ```bash
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Set CONF_SWAPSIZE=1024
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

2. **Optimize GPU memory:**
   ```bash
   sudo nano /boot/config.txt
   # Add: gpu_mem=128
   ```

## 🎵 Audio Configuration

### Microphone Issues

If the microphone isn't working:

```bash
# Check audio devices
arecord -l
alsamixer

# Test recording
arecord -d 5 test.wav
aplay test.wav
```

### Speaker Issues

If text-to-speech isn't working:

```bash
# Test espeak directly
espeak "Hello world"

# Check PulseAudio
pulseaudio --check -v
```

## 🧪 Testing

### Component Testing

```bash
python test_assistant.py
```

### Wake Word Testing

```bash
python -c "
from wake_word_detector import WakeWordDetector
from config import Config
detector = WakeWordDetector(Config())
detector.test_wake_words()
"
```

### Audio Testing

```bash
python -c "
from audio_utils import AudioManager
manager = AudioManager()
print(manager.get_microphone_info())
"
```

## 🛠️ Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'pyaudio'"**
   ```bash
   sudo apt install python3-pyaudio portaudio19-dev
   pip install pyaudio
   ```

2. **"OpenAI API key not found"**
   - Check your `.env` file
   - Ensure `OPENAI_API_KEY` is set correctly

3. **"No microphone detected"**
   ```bash
   # Check if microphone is recognized
   lsusb
   arecord -l
   ```

4. **"Permission denied for audio"**
   ```bash
   sudo usermod -a -G audio $USER
   # Logout and login again
   ```

5. **Wake words not detected**
   - Ensure microphone is working
   - Try speaking louder and clearer
   - Check background noise levels

### Log Files

Check logs for detailed error information:
```bash
tail -f ai_assistant.log
```

### Performance Issues

If the assistant is slow:
1. Reduce `OPENAI_MAX_TOKENS` in `.env`
2. Enable `LOW_POWER_MODE=true`
3. Close unnecessary applications

## 📁 Project Structure

```
ai_assistant/
├── main.py                 # Main application
├── config.py              # Configuration management
├── audio_utils.py         # Audio processing utilities
├── wake_word_detector.py  # Wake word detection
├── requirements.txt       # Python dependencies
├── setup_raspberry_pi.sh  # Setup script
├── test_assistant.py      # Test utilities
├── env_example.txt        # Environment configuration example
└── README.md             # This file
```

## 🔒 Security Notes

- Keep your OpenAI API key secure
- Don't share your `.env` file
- Monitor API usage to avoid unexpected charges
- The assistant processes audio locally except for OpenAI API calls

## 📊 Resource Usage

Typical resource usage on Raspberry Pi 4:
- **CPU:** 15-25% during active listening
- **RAM:** ~150MB
- **Storage:** ~500MB for all dependencies
- **Network:** Only for OpenAI API calls

## 🤝 Support

If you encounter issues:

1. Check the logs: `tail -f ai_assistant.log`
2. Run the test script: `python test_assistant.py`
3. Verify your configuration: Check `.env` file
4. Test individual components using the provided test functions

## 📝 License

This project is created for personal use. Please respect OpenAI's usage policies and terms of service.

## 🎉 Enjoy!

Your AI assistant is now ready to help Sophia and Eladriel with their questions and provide educational, fun interactions!

---

*"Miley, what's the capital of France?"* 🗼
*"Dino, tell me about dinosaurs!"* 🦕 