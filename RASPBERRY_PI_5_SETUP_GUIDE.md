# 🤖 AI Assistant Setup Guide for Raspberry Pi 5

## Overview
This guide will help you deploy your AI Assistant on Raspberry Pi 5 with fully working wake word detection. The main issue was that the energy threshold for speech recognition was hardcoded for macOS (300) but needs to be much lower for Pi 5 USB microphones (150).

## ✅ What We Fixed

### 1. **Platform-Aware Energy Thresholds**
- **macOS**: Energy threshold = 300 (higher for built-in mics)
- **Pi 5**: Energy threshold = 150 (lower for USB mics)
- **Pi 4**: Energy threshold = 120 (even lower for older hardware)

### 2. **Automatic Platform Detection**
The `AudioManager` now automatically detects your platform and sets the optimal energy threshold.

## 🚀 Quick Setup (Recommended)

### Step 1: Copy Updated Files to Pi 5
```bash
# Copy these updated files to your Pi 5:
# - audio_utils.py (with platform-aware energy thresholds)
# - test_platform_audio.py (for testing)
```

### Step 2: Test the Configuration
```bash
# On your Raspberry Pi 5, run:
cd /path/to/your/ai_assistant
python3 test_platform_audio.py
```

**Expected Output on Pi 5:**
```
Detected Platform: Raspberry Pi 5
Energy Threshold: 150
Status: ✅ CORRECT
```

### Step 3: Test Wake Word Detection
```bash
# Run your AI Assistant:
python3 main.py

# Try saying the wake words:
# - "Miley" (for Sophia)
# - "Dino" (for Eladriel)
# - "Assistant" (for general use)
```

## 🔧 Detailed Setup (If Issues Persist)

### Step 1: System Audio Setup
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install audio system dependencies
sudo apt install -y \
    alsa-utils \
    pulseaudio \
    pulseaudio-utils \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    espeak-data \
    flac \
    sox \
    libsox-fmt-all

# Add user to audio groups
sudo usermod -a -G audio,pulse,pulse-access $USER

# Reboot to apply group changes
sudo reboot
```

### Step 2: Enable Audio in Pi 5 Config
```bash
# Enable audio in config.txt
echo 'dtparam=audio=on' | sudo tee -a /boot/firmware/config.txt
echo 'audio_pwm_mode=2' | sudo tee -a /boot/firmware/config.txt

# Reboot to apply changes
sudo reboot
```

### Step 3: Configure PulseAudio
```bash
# Start PulseAudio
pulseaudio --start

# Check if running
pulseaudio --check && echo "PulseAudio is running" || echo "PulseAudio failed"

# List audio sources
pactl list sources short
```

### Step 4: Test USB Microphone
```bash
# Check if USB microphone is detected
lsusb | grep -i audio
arecord -l

# Test recording (5 seconds)
arecord -D hw:1,0 -f cd -t wav -d 5 test.wav

# Play back the recording
aplay test.wav
```

## 🔍 Troubleshooting

### Issue: "No wake word detected"
**Likely Cause**: Energy threshold too high
**Solution**: The updated code should fix this automatically

### Issue: "No microphones detected"
**Likely Cause**: USB microphone not properly configured
**Solution**:
```bash
# Check USB devices
lsusb

# Restart audio services
sudo systemctl restart alsa-state
pulseaudio --kill && pulseaudio --start
```

### Issue: "Microphone works but no speech recognition"
**Likely Cause**: Internet connectivity for Google Speech Recognition
**Solution**:
```bash
# Test internet connectivity
ping google.com

# Check if you can access Google's speech API
curl -I https://speech.googleapis.com
```

## 📊 Energy Threshold Comparison

| Platform | Energy Threshold | Reason |
|----------|------------------|--------|
| macOS | 300 | Built-in microphones are less sensitive |
| Pi 5 | 150 | USB microphones are more sensitive |
| Pi 4 | 120 | Older hardware needs lower threshold |
| Linux | 200 | General purpose middle ground |
| Windows | 250 | Conservative default |

## 🎯 Optimal USB Microphones for Pi 5

### Recommended Options:
1. **Blue Yeti Nano** - Excellent quality, plug-and-play
2. **Audio-Technica ATR2100x-USB** - Professional quality
3. **Samson Go Mic** - Compact and affordable
4. **Generic USB microphones** - Usually work out of the box

### Avoid:
- 3.5mm microphones (Pi 5 has no mic input)
- Bluetooth microphones (latency issues)
- USB-C microphones without proper drivers

## 🧪 Testing Your Setup

### 1. Run Platform Test
```bash
python3 test_platform_audio.py
```

### 2. Test Wake Word Detection
```bash
# Start the assistant
python3 main.py

# Say wake words clearly:
# - "Hey Miley" or just "Miley"
# - "Hey Dino" or just "Dino"
# - "Assistant"
```

### 3. Debug Audio Issues
```bash
# Check audio devices
arecord -l
aplay -l

# Check microphone levels
alsamixer

# Test recording with different devices
arecord -D hw:0,0 -f cd -t wav -d 3 test0.wav
arecord -D hw:1,0 -f cd -t wav -d 3 test1.wav
```

## 💡 Pro Tips

### 1. **Microphone Positioning**
- Place USB microphone 1-2 feet from speaker
- Avoid reflective surfaces
- Test different positions

### 2. **Environment Optimization**
- Reduce background noise
- Speak clearly and at normal volume
- Wait for the "listening" indicator

### 3. **Performance Optimization**
- Use a good quality USB microphone
- Ensure stable power supply for Pi 5
- Close unnecessary applications

## 🔄 Automatic Setup Script

If you want to automate the setup process, you can run:
```bash
# Make the script executable
chmod +x fix_audio_pi.sh

# Run the automatic fix script
./fix_audio_pi.sh
```

This script will:
- Install all required packages
- Configure audio settings
- Set up proper permissions
- Test microphone functionality

## 📋 Verification Checklist

- [ ] Pi 5 detects USB microphone (`lsusb`)
- [ ] ALSA shows recording devices (`arecord -l`)
- [ ] User in audio group (`groups | grep audio`)
- [ ] Audio enabled in config.txt
- [ ] PulseAudio running (`pulseaudio --check`)
- [ ] Platform test passes (`python3 test_platform_audio.py`)
- [ ] Energy threshold = 150 on Pi 5
- [ ] Wake words detected: "Miley", "Dino", "Assistant"

## 🎉 Success Indicators

When everything is working correctly, you should see:
```
✅ AudioManager initialized with energy_threshold=150 for Raspberry Pi 5
✅ Wake word 'miley' detected for sophia
👋 Hello Sophia! Starting voice-activated conversation...
```

## 🆘 Need Help?

If you're still having issues:
1. Run `python3 diagnose_audio_pi.py` on your Pi 5
2. Check the logs in `ai_assistant.log`
3. Verify your USB microphone works with other applications
4. Ensure your Pi 5 has adequate power supply

The key fix was making the energy threshold platform-aware. Your Pi 5 should now detect wake words much more reliably! 