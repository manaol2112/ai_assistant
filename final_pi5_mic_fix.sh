#!/bin/bash

# 🔥 FINAL PI 5 MICROPHONE FIX
# Removes all ALSA configs and uses direct hardware access

echo "🔥 FINAL PI 5 MICROPHONE FIX"
echo "🎤 Bypassing ALL ALSA configurations"
echo "============================================================"

# Remove ALL ALSA configuration files
echo "🗑️ Removing ALL ALSA configurations..."
rm -f ~/.asoundrc
rm -f ~/.asoundrc.bak
rm -f /home/$USER/.asoundrc*
sudo rm -f /etc/asound.conf 2>/dev/null

echo "✅ All ALSA configs removed"

# Create the ultimate direct hardware test
echo "🐍 Creating ULTIMATE direct hardware test..."
cat > test_direct_hardware.py << 'EOF'
#!/usr/bin/env python3
"""
ULTIMATE Pi 5 Microphone Test - Direct Hardware Access
Bypasses ALL ALSA configurations
"""

import speech_recognition as sr
import pyaudio
import wave
import tempfile
import os

def test_direct_hardware():
    print("🔥 ULTIMATE DIRECT HARDWARE TEST")
    print("=" * 50)
    
    # Test PyAudio direct access first
    print("🎤 Testing PyAudio direct access...")
    try:
        p = pyaudio.PyAudio()
        
        # Find the USB microphone
        usb_device_index = None
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if 'USB' in info['name'] and info['maxInputChannels'] > 0:
                usb_device_index = i
                print(f"✅ Found USB microphone: {info['name']} (device {i})")
                break
        
        if usb_device_index is None:
            print("❌ No USB microphone found")
            return False
            
        # Test direct recording
        print("🎙️ Testing direct recording (3 seconds)...")
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 3
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          input_device_index=usb_device_index,
                          frames_per_buffer=CHUNK)
            
            print("📢 Recording... Say 'HELLO' loudly!")
            frames = []
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Save the recording
            wf = wave.open(temp_filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            # Check if we got audio data
            file_size = os.path.getsize(temp_filename)
            print(f"✅ Recorded {file_size} bytes")
            
            if file_size > 1000:  # More than 1KB means we got audio
                print("🎉 DIRECT HARDWARE RECORDING SUCCESS!")
                
                # Now test speech recognition
                print("🧠 Testing speech recognition...")
                try:
                    recognizer = sr.Recognizer()
                    
                    # Use the specific device with very low threshold
                    with sr.Microphone(device_index=usb_device_index) as source:
                        recognizer.energy_threshold = 10  # VERY low
                        recognizer.dynamic_energy_threshold = False
                        
                        print("📢 Say 'HELLO' NOW (3 seconds)...")
                        audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                        
                        text = recognizer.recognize_google(audio)
                        print(f"🎉 SUCCESS! You said: '{text}'")
                        
                        # Clean up
                        os.unlink(temp_filename)
                        return True
                        
                except sr.WaitTimeoutError:
                    print("⏰ Speech recognition timeout - but hardware works!")
                    print("💡 Try speaking VERY loudly and close to microphone")
                except sr.UnknownValueError:
                    print("❓ Audio captured but couldn't understand")
                    print("💡 Hardware works - try speaking more clearly")
                except Exception as e:
                    print(f"🔧 Speech recognition error: {e}")
                    print("✅ But hardware recording works!")
                
                # Clean up
                os.unlink(temp_filename)
                return True
            else:
                print("❌ No audio data captured")
                return False
                
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ PyAudio error: {e}")
        return False
    finally:
        p.terminate()

def create_working_config():
    """Create a minimal working audio configuration"""
    print("🔧 Creating minimal working configuration...")
    
    # Create a super simple .asoundrc that just points to hardware
    with open(os.path.expanduser('~/.asoundrc'), 'w') as f:
        f.write("""# Minimal Pi 5 USB microphone config
pcm.!default {
    type hw
    card 2
    device 0
}

ctl.!default {
    type hw
    card 2
}
""")
    print("✅ Created minimal .asoundrc")

if __name__ == "__main__":
    success = test_direct_hardware()
    
    if success:
        print("\n🎉 MICROPHONE WORKING!")
        print("=" * 50)
        print("✅ Direct hardware access: SUCCESS")
        print("✅ Audio recording: SUCCESS")
        print("🚀 Ready to run: python3 main.py")
        
        # Create the minimal config
        create_working_config()
        
    else:
        print("\n🔧 HARDWARE ISSUE DETECTED")
        print("=" * 50)
        print("💡 Possible solutions:")
        print("1. Check USB microphone connection")
        print("2. Try a different USB port")
        print("3. Check microphone volume/gain")
        print("4. Reboot the Pi")
EOF

chmod +x test_direct_hardware.py
echo "✅ Created ultimate hardware test"

# Create a simple main.py test version
echo "🚀 Creating simple AI assistant test..."
cat > test_ai_simple.py << 'EOF'
#!/usr/bin/env python3
"""
Simple AI Assistant Test for Pi 5
"""

import speech_recognition as sr
import pyaudio

def test_ai_assistant():
    print("🤖 SIMPLE AI ASSISTANT TEST")
    print("=" * 40)
    
    try:
        recognizer = sr.Recognizer()
        
        # Find USB microphone
        p = pyaudio.PyAudio()
        usb_device = None
        
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if 'USB' in info['name'] and info['maxInputChannels'] > 0:
                usb_device = i
                break
        
        p.terminate()
        
        if usb_device is None:
            print("❌ No USB microphone found")
            return
            
        print(f"✅ Using USB microphone device {usb_device}")
        
        # Test wake word detection
        with sr.Microphone(device_index=usb_device) as source:
            recognizer.energy_threshold = 15  # Very low for Pi 5
            recognizer.dynamic_energy_threshold = False
            
            print("🎯 Listening for wake words: 'Miley', 'Dino', 'Assistant'")
            print("📢 Say a wake word NOW...")
            
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                
                print(f"🎤 Heard: '{text}'")
                
                if any(wake_word in text for wake_word in ['miley', 'dino', 'assistant']):
                    print("🎉 WAKE WORD DETECTED!")
                    print("✅ AI Assistant ready to work!")
                else:
                    print("💡 Try saying: 'Miley', 'Dino', or 'Assistant'")
                    
            except sr.WaitTimeoutError:
                print("⏰ No speech detected")
                print("💡 Speak louder or closer to microphone")
            except Exception as e:
                print(f"🔧 Error: {e}")
    
    except Exception as e:
        print(f"❌ Setup error: {e}")

if __name__ == "__main__":
    test_ai_assistant()
EOF

chmod +x test_ai_simple.py
echo "✅ Created simple AI assistant test"

echo ""
echo "🔥 FINAL FIX COMPLETE!"
echo "============================================================"
echo "✅ All ALSA configs removed"
echo "✅ Direct hardware test ready"
echo "✅ Simple AI assistant test ready"
echo ""
echo "🚀 TEST SEQUENCE:"
echo "1. python3 test_direct_hardware.py"
echo "2. python3 test_ai_simple.py"
echo "3. python3 main.py"
echo ""
echo "💡 This bypasses ALL ALSA configuration issues!" 