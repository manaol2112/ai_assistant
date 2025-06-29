#!/usr/bin/env python3
"""
Test script for conversation audio debugging
"""

import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio_utils import AudioManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_conversation_audio():
    """Test conversation audio settings."""
    print("🎤 Testing Conversation Audio Settings")
    print("=" * 50)
    
    try:
        # Initialize AudioManager
        print("1. Initializing AudioManager...")
        audio_manager = AudioManager()
        
        # Show current settings
        print(f"✅ AudioManager initialized")
        print(f"   Sample Rate: {audio_manager.sample_rate}Hz")
        print(f"   Chunk Size: {audio_manager.chunk_size}")
        print(f"   Energy Threshold: {audio_manager.energy_threshold}")
        print(f"   Recognizer Energy Threshold: {audio_manager.recognizer.energy_threshold}")
        print()
        
        # Test microphone
        print("2. Testing microphone...")
        mic_test = audio_manager.test_microphone()
        if mic_test:
            print("✅ Microphone test passed")
        else:
            print("❌ Microphone test failed")
            return False
        print()
        
        # Calibrate audio
        print("3. Calibrating audio...")
        audio_manager.calibrate_audio(duration=2.0)
        print(f"✅ Audio calibrated")
        print(f"   New Energy Threshold: {audio_manager.energy_threshold}")
        print()
        
        # Test conversation-style listening
        print("4. Testing conversation listening...")
        print("🎤 Say something now (you have 10 seconds)...")
        
        audio_data = audio_manager.listen_for_audio(timeout=10, phrase_time_limit=8)
        
        if audio_data:
            print("✅ Audio captured successfully!")
            
            # Convert to text
            print("5. Converting audio to text...")
            text = audio_manager.audio_to_text(audio_data)
            
            if text:
                print(f"✅ Speech recognized: '{text}'")
                return True
            else:
                print("❌ Audio captured but no text recognized")
                return False
        else:
            print("❌ No audio captured")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            audio_manager.cleanup()
        except:
            pass

if __name__ == "__main__":
    print("🤖 Conversation Audio Debug Test")
    print("This will test the same audio settings used in conversation mode")
    print()
    
    success = test_conversation_audio()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 Test completed successfully!")
        print("The conversation audio should work properly.")
    else:
        print("⚠️ Test failed!")
        print("There may be issues with conversation audio.")
    
    print("Press Enter to exit...")
    input() 