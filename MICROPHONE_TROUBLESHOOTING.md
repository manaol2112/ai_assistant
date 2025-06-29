# 🎤 Microphone Troubleshooting Guide for Raspberry Pi 5

## Overview

This guide helps you diagnose and fix microphone issues with your AI Assistant on Raspberry Pi 5. The most common problem is that the microphone works fine on macOS but doesn't work when deployed to Raspberry Pi.

## 🔧 Quick Fix (Recommended)

### Step 1: Run the Diagnostic Tool
```bash
# Copy these files to your Raspberry Pi 5
# Then run the diagnostic script
python3 diagnose_audio_pi.py
```

### Step 2: Run the Automatic Fix Script
```bash
# This will automatically fix most common issues
./fix_audio_pi.sh
```

### Step 3: Reboot and Test
```bash
sudo reboot
# After reboot, test your AI Assistant
python3 main.py
```

## 🔍 Common Issues and Solutions

### Issue 1: No ALSA Recording Devices
**Symptoms:** 
- "No ALSA recording devices found" error
- Application can't detect microphone

**Solution:**
```bash
# Install audio system packages
sudo apt update
sudo apt install -y alsa-utils pulseaudio portaudio19-dev

# Add user to audio group
sudo usermod -a -G audio,pulse,pulse-access $USER

# Reboot required
sudo reboot
```

### Issue 2: Audio Not Enabled in Raspberry Pi Config
**Symptoms:**
- System doesn't recognize audio hardware
- No audio devices available

**Solution:**
```bash
# Enable audio in config.txt
echo 'dtparam=audio=on' | sudo tee -a /boot/config.txt
echo 'audio_pwm_mode=2' | sudo tee -a /boot/config.txt

# Reboot required
sudo reboot
```

### Issue 3: PyAudio Not Working
**Symptoms:**
- PyAudio import errors
- "No input devices found" error

**Solution:**
```bash
# Install system PyAudio package
sudo apt install -y python3-pyaudio

# Or install from pip in virtual environment
source ai_assistant_env/bin/activate
pip install pyaudio
```

### Issue 4: USB Microphone Not Detected
**Symptoms:**
- USB microphone connected but not recognized
- No microphones listed in speech recognition

**Solution:**
```bash
# Check if USB microphone is detected
lsusb
arecord -l

# Set proper permissions
sudo usermod -a -G audio $USER

# Create udev rules (done automatically by fix script)
sudo tee /etc/udev/rules.d/99-usb-microphone.rules << EOF
SUBSYSTEM=="sound", GROUP="audio", MODE="0664"
SUBSYSTEM=="usb", ATTRS{bInterfaceClass}=="01", ATTRS{bInterfaceSubClass}=="01", GROUP="audio", MODE="0664"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger
```

## 🔧 Manual Troubleshooting Steps

### Step 1: Check Audio Devices
```bash
# List playback devices
aplay -l

# List recording devices
arecord -l

# Check PulseAudio sources
pactl list sources short
```

### Step 2: Test Basic Recording
```bash
# Record 5 seconds of audio
arecord -D hw:1,0 -f cd -t wav -d 5 test.wav

# Play back the recording
aplay test.wav
```

### Step 3: Check Python Libraries
```bash
# Test in Python
python3 -c "
import pyaudio
import speech_recognition as sr

# Test PyAudio
p = pyaudio.PyAudio()
print(f'PyAudio devices: {p.get_device_count()}')
p.terminate()

# Test SpeechRecognition
r = sr.Recognizer()
mics = sr.Microphone.list_microphone_names()
print(f'Microphones: {len(mics)}')
for i, mic in enumerate(mics):
    print(f'  {i}: {mic}')
"
```

### Step 4: Check User Permissions
```bash
# Check current user groups
groups

# Should include: audio, pulse, pulse-access
# If not, add them:
sudo usermod -a -G audio,pulse,pulse-access $USER

# Logout and login again for changes to take effect
```

## 🎯 Specific Raspberry Pi 5 Considerations

### Hardware Limitations
- **No 3.5mm microphone input**: Pi 5 doesn't have a microphone input jack
- **Use USB microphone**: Recommended for reliable audio input
- **USB sound card**: Alternative option for better audio quality

### Recommended USB Microphones
- **Blue Yeti Nano** - Excellent quality, plug-and-play
- **Audio-Technica ATR2100x-USB** - Professional quality
- **Generic USB microphones** - Usually work out of the box

### Pi 5 Audio Configuration
```bash
# Pi 5 specific config.txt settings
dtparam=audio=on
audio_pwm_mode=2
dtoverlay=vc4-kms-v3d
gpu_mem=128
```

## 🚨 Troubleshooting Script Details

### diagnose_audio_pi.py
- Comprehensive audio system diagnosis
- Tests all audio components
- Provides specific error messages
- Safe to run multiple times

### fix_audio_pi.sh
- Automatically fixes common issues
- Installs required packages
- Configures system settings
- Requires reboot to complete

## 🔄 Testing Your Fix

After running the fix script and rebooting:

1. **Test basic recording:**
   ```bash
   arecord -l  # Should show recording devices
   ```

2. **Test Python libraries:**
   ```bash
   python3 diagnose_audio_pi.py
   ```

3. **Test AI Assistant:**
   ```bash
   python3 main.py
   # Try speaking wake words: "Miley", "Dino", "Assistant"
   ```

## 🐛 Still Having Issues?

### Check System Logs
```bash
# Check system audio logs
journalctl -u pulseaudio --since "1 hour ago"

# Check ALSA errors
dmesg | grep -i audio
```

### Verify Hardware
```bash
# Check USB devices
lsusb

# Check audio hardware
cat /proc/asound/cards

# Test with different microphone
# Try different USB ports
```

### Reset Audio System
```bash
# Kill PulseAudio and restart
pulseaudio --kill
pulseaudio --start

# Restart ALSA
sudo systemctl restart alsa-state
```

## 📋 Checklist for Working Microphone

- [ ] USB microphone connected and detected (`lsusb`)
- [ ] ALSA shows recording devices (`arecord -l`)
- [ ] User in audio group (`groups | grep audio`)
- [ ] Audio enabled in config.txt (`grep audio /boot/config.txt`)
- [ ] PyAudio installed and working
- [ ] SpeechRecognition finds microphones
- [ ] PulseAudio running (`pulseaudio --check`)
- [ ] Basic recording works (`arecord test.wav`)
- [ ] AI Assistant responds to voice commands

## 💡 Prevention Tips

1. **Always use USB microphones** on Raspberry Pi 5
2. **Keep audio packages updated** with `sudo apt update`
3. **Use virtual environments** for Python packages
4. **Backup working configuration** before changes
5. **Test after system updates** to ensure compatibility

## 🆘 Need More Help?

If you're still experiencing issues:

1. Run the diagnostic script and share the output
2. Check if the microphone works on other devices
3. Try a different USB microphone
4. Verify your Raspberry Pi 5 is properly powered
5. Check for hardware defects

The diagnostic script will provide detailed information about what's working and what needs to be fixed. 