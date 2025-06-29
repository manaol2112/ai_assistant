#!/bin/bash

# 🔧 FIX ASOUNDRC SYNTAX ERROR
# Creates a working ALSA configuration for hw:2,0 microphone

echo "🔧 FIXING ASOUNDRC SYNTAX ERROR"
echo "🎤 Creating working config for hw:2,0 microphone"
echo "============================================================"

# Remove the corrupted .asoundrc
echo "🗑️ Removing corrupted .asoundrc..."
rm -f ~/.asoundrc

# Create a clean, working .asoundrc
echo "📝 Creating clean .asoundrc for hw:2,0..."
cat > ~/.asoundrc << 'EOF'
# Working ALSA configuration for Pi 5 USB microphone hw:2,0
pcm.!default {
    type asym
    playback.pcm "playback_dmix"
    capture.pcm "capture_hw"
}

pcm.playback_dmix {
    type dmix
    ipc_key 1024
    slave {
        pcm "hw:0,0"
        channels 2
        rate 44100
        format S16_LE
    }
}

pcm.capture_hw {
    type hw
    card 2
    device 0
    channels 1
    rate 44100
    format S16_LE
}

# Control interface
ctl.!default {
    type hw
    card 0
}
EOF

echo "✅ Created clean .asoundrc"

# Test the configuration
echo "🧪 Testing ALSA configuration..."
if arecord -D capture_hw -f cd -t wav -d 1 /tmp/alsa_test.wav 2>/dev/null; then
    echo "✅ ALSA config works!"
    rm -f /tmp/alsa_test.wav
else
    echo "❌ ALSA config still has issues"
fi

# Create a simple Python test
echo "🐍 Creating simple Python test..."
cat > test_simple_mic.py << 'EOF'
#!/usr/bin/env python3
"""
Simple microphone test for hw:2,0
"""

import speech_recognition as sr
import logging

def test_simple_microphone():
    print("🎤 SIMPLE MICROPHONE TEST")
    print("=" * 40)
    
    try:
        recognizer = sr.Recognizer()
        
        # Use the specific microphone device
        with sr.Microphone(device_index=2) as source:
            print("✅ Using microphone device 2 (hw:2,0)")
            
            # Very low energy threshold
            recognizer.energy_threshold = 25
            print(f"🎚️ Energy threshold: {recognizer.energy_threshold}")
            
            # Test speech recognition
            print("📢 Say 'hello' NOW (5 seconds)...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                print("✅ Audio captured successfully!")
                
                # Try to recognize
                text = recognizer.recognize_google(audio)
                print(f"🎉 SUCCESS! You said: '{text}'")
                return True
                
            except sr.WaitTimeoutError:
                print("⏰ No speech detected")
                print("💡 Try speaking louder or closer to the microphone")
                return False
            except sr.UnknownValueError:
                print("❓ Audio captured but couldn't understand speech")
                print("💡 Try speaking more clearly")
                return False
            except Exception as e:
                print(f"❌ Recognition error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Microphone access error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_microphone()
    if success:
        print("\n🎉 MICROPHONE WORKING PERFECTLY!")
        print("✅ Ready to run: python3 main.py")
    else:
        print("\n🔧 Need more troubleshooting")

EOF

chmod +x test_simple_mic.py
echo "✅ Created simple Python test"

echo ""
echo "🎉 SYNTAX FIX COMPLETE!"
echo "============================================================"
echo "✅ Corrupted .asoundrc removed"
echo "✅ Clean .asoundrc created for hw:2,0"
echo "✅ Simple Python test ready"
echo ""
echo "🚀 TEST NOW:"
echo "python3 test_simple_mic.py" 