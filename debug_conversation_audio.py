#!/usr/bin/env python3
"""
Debug script for conversation mode audio issues
Tests the exact same audio flow that happens during conversation
"""

import sys
import os
import logging
import time
import speech_recognition as sr

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio_utils import AudioManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_conversation_audio_flow():
    """Test the exact audio flow that happens during conversation mode."""
    print("🎤 CONVERSATION AUDIO DEBUG TEST")
    print("=" * 50)
    
    try:
        # Initialize AudioManager exactly like in main.py
        print("1. Initializing AudioManager...")
        audio_manager = AudioManager()
        
        print(f"   ✅ Sample Rate: {audio_manager.sample_rate}Hz")
        print(f"   ✅ Chunk Size: {audio_manager.chunk_size}")
        print(f"   ✅ Energy Threshold: {audio_manager.energy_threshold}")
        print(f"   ✅ Platform: {audio_manager.platform_info}")
        
        # Test microphone
        print("\n2. Testing microphone...")
        if audio_manager.test_microphone():
            print("   ✅ Microphone test passed")
        else:
            print("   ❌ Microphone test failed")
            return False
        
        # Get microphone info
        print("\n3. Microphone information:")
        mic_info = audio_manager.get_microphone_info()
        print(f"   Default mic: {mic_info.get('default_mic', {}).get('name', 'Unknown')}")
        print(f"   Available mics: {len(mic_info.get('available_mics', []))}")
        
        # Test calibration
        print("\n4. Testing audio calibration...")
        audio_manager.calibrate_audio(duration=1.0)
        print(f"   ✅ Calibrated energy threshold: {audio_manager.energy_threshold}")
        
        # Now test the exact conversation flow
        print("\n5. CONVERSATION MODE SIMULATION")
        print("   This simulates what happens after wake word detection...")
        
        for test_round in range(3):
            print(f"\n   TEST ROUND {test_round + 1}/3")
            print("   Say something now (you have 10 seconds)...")
            
            # Use the exact same settings as in listen_for_speech method
            conversation_timeout = 10  # Shorter for testing
            phrase_limit = 8
            
            print(f"   🎤 Listening with timeout={conversation_timeout}s, phrase_limit={phrase_limit}s")
            
            # Show current audio settings (like in main.py)
            print(f"   🔧 Current Settings:")
            print(f"      Sample Rate: {audio_manager.sample_rate}Hz")
            print(f"      Energy Threshold: {audio_manager.energy_threshold}")
            print(f"      Recognizer Energy: {audio_manager.recognizer.energy_threshold}")
            
            # Listen for audio (exact same call as in main.py)
            start_time = time.time()
            audio_data = audio_manager.listen_for_audio(
                timeout=conversation_timeout, 
                phrase_time_limit=phrase_limit
            )
            end_time = time.time()
            
            print(f"   ⏱️ Listening took {end_time - start_time:.2f} seconds")
            
            if audio_data:
                print("   ✅ Audio captured! Converting to text...")
                
                # Convert to text (exact same call as in main.py)
                text = audio_manager.audio_to_text(audio_data)
                
                if text:
                    print(f"   🎯 SUCCESS! Recognized: '{text}'")
                else:
                    print("   ⚠️ Audio captured but no text recognized")
            else:
                print("   ❌ No audio captured (timeout or silence)")
            
            print("   " + "-" * 40)
        
        print("\n6. FINAL AUDIO LEVEL TEST")
        print("   Testing ambient audio levels...")
        
        for i in range(5):
            level = audio_manager.get_audio_level(duration=0.2)
            print(f"   Audio level {i+1}: {level:.2f}")
            time.sleep(0.3)
        
        print("\n✅ Conversation audio debug test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during conversation audio test: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False
    
    finally:
        try:
            audio_manager.cleanup()
        except:
            pass

def test_simple_recognition():
    """Test basic speech recognition without AudioManager wrapper."""
    print("\n🔍 SIMPLE RECOGNITION TEST")
    print("=" * 30)
    
    try:
        recognizer = sr.Recognizer()
        
        print("Testing basic speech recognition (5 seconds)...")
        print("Say something now...")
        
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"Energy threshold: {recognizer.energy_threshold}")
            
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("Converting to text...")
            text = recognizer.recognize_google(audio)
            print(f"✅ Recognized: '{text}'")
            return True
            
    except sr.WaitTimeoutError:
        print("❌ Timeout - no speech detected")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Conversation Audio Debug")
    print("This will test the exact audio flow used in conversation mode")
    print("Make sure you're in a quiet environment and speak clearly")
    print()
    
    # Test conversation audio flow
    success1 = test_conversation_audio_flow()
    
    print("\n" + "=" * 60)
    
    # Test simple recognition as comparison
    success2 = test_simple_recognition()
    
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS:")
    print(f"   Conversation mode test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"   Simple recognition test: {'✅ PASSED' if success2 else '❌ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 Both tests passed! Audio should work in conversation mode.")
    elif success2 and not success1:
        print("\n⚠️ Simple recognition works but conversation mode fails.")
        print("   This indicates an issue with the AudioManager or conversation flow.")
    elif not success2:
        print("\n❌ Basic speech recognition is not working.")
        print("   Check microphone hardware and permissions.")
    
    print("\nRun this script on your Raspberry Pi to diagnose the conversation mode issue!") 