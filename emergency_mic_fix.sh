#!/bin/bash

# 🚨 EMERGENCY PI 5 MICROPHONE FIX
# This will diagnose and fix the exact hardware issue

echo "🚨 EMERGENCY PI 5 MICROPHONE DIAGNOSTIC & FIX"
echo "🔧 Finding and fixing the exact hardware issue..."
echo "============================================================"

# Function to check hardware detection
check_hardware() {
    echo "🔍 HARDWARE DETECTION"
    echo "=================================================="
    
    echo "🎤 USB devices:"
    lsusb | grep -i audio || echo "❌ No USB audio devices found"
    
    echo ""
    echo "🎤 Sound cards:"
    cat /proc/asound/cards || echo "❌ No sound cards found"
    
    echo ""
    echo "🎤 Audio devices:"
    ls -la /dev/snd/ 2>/dev/null || echo "❌ No /dev/snd devices"
    
    echo ""
    echo "🎤 ALSA cards:"
    aplay -l 2>/dev/null || echo "❌ No playback devices"
    arecord -l 2>/dev/null || echo "❌ No recording devices"
}

# Function to test each available microphone
test_all_microphones() {
    echo ""
    echo "🎤 TESTING ALL AVAILABLE MICROPHONES"
    echo "=================================================="
    
    # Get list of cards
    cards=$(arecord -l 2>/dev/null | grep "^card" | cut -d: -f1 | cut -d' ' -f2 | sort -u)
    
    if [ -z "$cards" ]; then
        echo "❌ No recording cards found"
        return 1
    fi
    
    for card in $cards; do
        echo "🎤 Testing card $card..."
        
        # Test different devices on this card
        for device in 0 1 2; do
            echo "  📱 Testing hw:$card,$device..."
            
            # Quick 2-second test
            if timeout 3 arecord -D hw:$card,$device -f cd -t wav -d 2 /tmp/test_$card_$device.wav 2>/dev/null; then
                if [ -s /tmp/test_$card_$device.wav ]; then
                    echo "  ✅ hw:$card,$device WORKS!"
                    echo "  📊 File size: $(wc -c < /tmp/test_$card_$device.wav) bytes"
                    
                    # Test with Python
                    python3 -c "
import speech_recognition as sr
try:
    r = sr.Recognizer()
    with sr.Microphone(device_index=$card) as source:
        r.energy_threshold = 50
        print('  🐍 Python can access this microphone')
        audio = r.listen(source, timeout=1, phrase_time_limit=1)
        print('  ✅ Python audio capture works!')
except Exception as e:
    print(f'  ❌ Python error: {e}')
"
                    
                    # This is our working microphone!
                    echo "  🎉 FOUND WORKING MICROPHONE: hw:$card,$device"
                    echo "hw:$card,$device" > /tmp/working_mic.txt
                    rm -f /tmp/test_$card_$device.wav
                    return 0
                else
                    echo "  ❌ hw:$card,$device - empty recording"
                fi
            else
                echo "  ❌ hw:$card,$device - failed to record"
            fi
            
            rm -f /tmp/test_$card_$device.wav
        done
    done
    
    echo "❌ No working microphones found"
    return 1
}

# Function to create working ALSA config
create_working_asoundrc() {
    local working_mic="$1"
    
    echo ""
    echo "🔧 CREATING WORKING ALSA CONFIG"
    echo "=================================================="
    
    # Extract card and device
    card=$(echo $working_mic | cut -d: -f2 | cut -d, -f1)
    device=$(echo $working_mic | cut -d: -f2 | cut -d, -f2)
    
    echo "📝 Creating .asoundrc for $working_mic (card=$card, device=$device)..."
    
    cat > ~/.asoundrc << EOF
# Working configuration for Pi 5 microphone: $working_mic
pcm.!default {
    type asym
    playback.pcm "dmix"
    capture.pcm "working_mic"
}

pcm.working_mic {
    type hw
    card $card
    device $device
    channels 1
    rate 44100
    format S16_LE
}

pcm.dmix {
    type dmix
    ipc_key 1024
    slave {
        pcm "hw:0,0"
        channels 2
    }
}

ctl.!default {
    type hw
    card 0
}
EOF
    
    echo "✅ Created working .asoundrc"
}

# Function to create Python test with working microphone
create_working_python_test() {
    local working_mic="$1"
    
    echo ""
    echo "🔧 CREATING PYTHON TEST FOR WORKING MIC"
    echo "=================================================="
    
    # Extract card number
    card=$(echo $working_mic | cut -d: -f2 | cut -d, -f1)
    
    cat > test_working_mic.py << EOF
#!/usr/bin/env python3
"""
Test script using the working microphone: $working_mic
"""

import speech_recognition as sr
import logging

logging.basicConfig(level=logging.INFO)

def test_working_microphone():
    print("🎤 TESTING WORKING MICROPHONE: $working_mic")
    print("=" * 50)
    
    try:
        recognizer = sr.Recognizer()
        
        # Use the specific working microphone
        with sr.Microphone(device_index=$card) as source:
            print("✅ Using working microphone: $working_mic")
            
            # Very low energy threshold
            recognizer.energy_threshold = 30
            print(f"🎚️ Energy threshold: {recognizer.energy_threshold}")
            
            # Quick calibration
            print("🎯 Quick calibration...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Override with very low threshold
            recognizer.energy_threshold = 30
            print(f"🎚️ Final energy threshold: {recognizer.energy_threshold}")
            
            # Test speech recognition
            print("📢 Say 'hello' NOW (you have 5 seconds)...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                print("✅ Audio captured!")
                
                # Try to recognize
                text = recognizer.recognize_google(audio)
                print(f"🎉 SUCCESS! Recognized: '{text}'")
                return True
                
            except sr.WaitTimeoutError:
                print("⏰ Still no speech detected")
                print("💡 Try speaking louder or closer to microphone")
                return False
            except sr.UnknownValueError:
                print("❓ Audio captured but speech not understood")
                print("💡 This is progress! Try speaking more clearly")
                return False
            except Exception as e:
                print(f"❌ Recognition error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return False

if __name__ == "__main__":
    success = test_working_microphone()
    if success:
        print("\n🎉 MICROPHONE IS WORKING!")
        print("✅ You can now run: python3 main.py")
    else:
        print("\n🔧 Still troubleshooting needed")
        print("💡 Try adjusting microphone position or volume")
EOF
    
    chmod +x test_working_mic.py
    echo "✅ Created working microphone test"
}

# Function to fix permissions aggressively
fix_permissions_aggressive() {
    echo ""
    echo "🔧 AGGRESSIVE PERMISSION FIX"
    echo "=================================================="
    
    # Add to audio group
    sudo usermod -a -G audio $USER
    
    # Fix all audio device permissions
    sudo chmod 666 /dev/snd/* 2>/dev/null
    sudo chown $USER:audio /dev/snd/* 2>/dev/null
    
    # Fix ALSA state
    sudo chmod 666 /var/lib/alsa/asound.state 2>/dev/null
    
    echo "✅ Permissions fixed aggressively"
}

# Main execution
main() {
    echo "🚨 Starting emergency microphone fix..."
    
    check_hardware
    fix_permissions_aggressive
    
    echo ""
    echo "🔍 SEARCHING FOR WORKING MICROPHONE..."
    echo "=================================================="
    
    if test_all_microphones; then
        working_mic=$(cat /tmp/working_mic.txt)
        echo "🎉 FOUND WORKING MICROPHONE: $working_mic"
        
        create_working_asoundrc "$working_mic"
        create_working_python_test "$working_mic"
        
        echo ""
        echo "🎉 EMERGENCY FIX COMPLETE!"
        echo "============================================================"
        echo "✅ Working microphone: $working_mic"
        echo "✅ ALSA config updated"
        echo "✅ Python test created"
        echo ""
        echo "🚀 TEST NOW:"
        echo "python3 test_working_mic.py"
        echo ""
        
    else
        echo ""
        echo "❌ EMERGENCY FIX FAILED"
        echo "============================================================"
        echo "🔧 POSSIBLE ISSUES:"
        echo "1. USB microphone not connected"
        echo "2. USB microphone not recognized"
        echo "3. Hardware failure"
        echo "4. Driver issues"
        echo ""
        echo "💡 NEXT STEPS:"
        echo "1. Check USB connection"
        echo "2. Try different USB port"
        echo "3. Reboot Pi: sudo reboot"
        echo "4. Check if microphone works on other devices"
    fi
}

# Run the main function
main 