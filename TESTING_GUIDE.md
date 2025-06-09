# 🧪 AI Assistant Testing Guide

## Quick Setup and Testing on Mac

Your AI assistant is ready for testing! Here's how to test it step by step:

### 1. Environment Check
```bash
# Make sure you're in the virtual environment
source ai_assistant_env/bin/activate

# Verify all components work
python test_mac.py
```

### 2. Test Core Functionality (Without Voice)
```bash
# Test AI responses and text-to-speech
python test_conversation.py
```
This will:
- Test personalized greetings for Sophia and Eladriel
- Demonstrate AI responses with different personalities
- Use text-to-speech to speak responses
- Show how wake words work ("Miley" for Sophia, "Dino" for Eladriel)

### 3. Test Full Voice System
```bash
# Run the complete AI assistant
python main.py
```

Then:
1. **Say "Miley"** to activate Sophia mode
2. **Say "Dino"** to activate Eladriel mode
3. **Ask questions** like:
   - "What's the weather like?"
   - "Tell me a joke"
   - "What's 2 + 2?"
   - "How are you today?"

### 📱 Personalized Features

#### For Sophia (Wake word: "Miley")
- Friendly and encouraging personality
- Child-appropriate responses
- Warm, caring tone

#### For Eladriel (Wake word: "Dino")
- Playful and curious personality
- Educational and fun responses
- Engaging, dinosaur-themed personality

### 🔧 Configuration

All settings are in `.env` file:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-3.5-turbo
TTS_RATE=180
AUDIO_SAMPLE_RATE=16000
```

### 🎯 Testing Scenarios

#### Quick Tests
1. **Component Test**: `python test_mac.py`
2. **Conversation Test**: `python test_conversation.py`
3. **Full System**: `python main.py`

#### Audio Tests
- Test microphone: Say wake words clearly
- Test speakers: Listen for TTS responses
- Test wake word detection: "Miley" or "Dino"

### 🚀 Deployment to Raspberry Pi

When ready to deploy:
```bash
# Copy to Raspberry Pi
scp -r . pi@raspberrypi.local:~/ai_assistant/

# On Raspberry Pi
./setup_raspberry_pi.sh
```

### 🛠️ Troubleshooting

#### Audio Issues
- **No microphone**: Check `python test_mac.py` for microphone detection
- **No sound**: Verify speakers/headphones work
- **PyAudio errors**: `brew install portaudio && pip install pyaudio`

#### OpenAI Issues
- Check API key in `.env` file
- Verify internet connection
- Check OpenAI account credits

#### Wake Word Issues
- Speak clearly and loudly
- Use exact wake words: "Miley" or "Dino"
- Check microphone permissions in System Preferences

### 📊 System Status

Current configuration:
- ✅ Python 3.12+ environment
- ✅ OpenAI GPT integration
- ✅ Text-to-speech (48 voices available)
- ✅ Speech recognition
- ✅ Wake word detection
- ✅ Personalized responses
- ✅ Raspberry Pi ready

### 🎵 Voice Commands Examples

**General Commands:**
- "What time is it?"
- "Tell me about space"
- "What's the capital of France?"
- "Help me with my homework"

**For Sophia (after saying "Miley"):**
- "What's your favorite color?"
- "Tell me about animals"
- "How do I learn math?"

**For Eladriel (after saying "Dino"):**
- "Tell me about dinosaurs"
- "What's a fun fact?"
- "How do rockets work?"

---

## 🎉 Ready to Use!

Your AI assistant is now fully configured and tested. Enjoy exploring the personalized experience for both Sophia and Eladriel!

For issues or questions, check the logs in `ai_assistant.log` or run the test scripts. 