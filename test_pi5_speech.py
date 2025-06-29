#!/usr/bin/env python3
"""
Raspberry Pi 5 Speech Recognition Test
Tests the platform-specific optimizations for speech recognition on Pi 5
"""

import sys
import os
import logging
import time
import platform
from typing import Optional

# Add current directory to path for imports
sys.path.append('.')

try:
    import speech_recognition as sr
    from voice_activity_detector import VoiceActivityDetector
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the AI Assistant directory and have activated the virtual environment:")
    print("  source ai_assistant_env/bin/activate")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🔊 {text}")
    print('='*60)

def print_status(text):
    print(f"📋 {text}")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def detect_platform():
    """Detect current platform and show detection results."""
    print_header("PLATFORM DETECTION TEST")
    
    print_status("System information:")
    print(f"  System: {platform.system()}")
    print(f"  Machine: {platform.machine()}")
    print(f"  Platform: {platform.platform()}")
    
    # Check Raspberry Pi detection
    if os.path.exists('/proc/device-tree/model'):
        try:
            with open('/proc/device-tree/model', 'r') as f:
                model_info = f.read().strip()
                print(f"  Device Model: {model_info}")
                
                if 'raspberry pi' in model_info.lower():
                    print_success("Raspberry Pi detected!")
                    if 'pi 5' in model_info.lower():
                        print_success("This is a Raspberry Pi 5!")
                    else:
                        print_warning("This is an older Raspberry Pi model")
                else:
                    print_warning("Not a Raspberry Pi")
        except Exception as e:
            print_error(f"Could not read device model: {e}")
    else:
        print_warning("Not running on Raspberry Pi (no device tree)")

def test_voice_detector_initialization():
    """Test voice activity detector initialization and platform settings."""
    print_header("VOICE DETECTOR INITIALIZATION TEST")
    
    try:
        # Initialize speech recognizer
        recognizer = sr.Recognizer()
        print_success("Speech recognizer initialized")
        
        # Initialize voice activity detector
        voice_detector = VoiceActivityDetector(recognizer)
        print_success("Voice activity detector initialized")
        
        # Show platform information
        platform_info = voice_detector.platform_info
        print_status("Platform-specific settings:")
        print(f"  Platform Name: {platform_info['name']}")
        print(f"  Platform Type: {platform_info['type']}")
        print(f"  Base Energy Threshold: {platform_info['base_energy_threshold']}")
        print(f"  Calibration Duration: {platform_info['calibration_duration']}s")
        print(f"  Chunk Duration Multiplier: {platform_info['chunk_duration_multiplier']}")
        print(f"  Silence Tolerance Multiplier: {platform_info['silence_tolerance_multiplier']}")
        
        print_status("Energy thresholds for different modes:")
        for mode in ['normal', 'spelling', 'filipino', 'interrupt']:
            settings = voice_detector._get_optimal_thresholds(mode)
            print(f"  {mode.title()}: {settings['energy_threshold']}")
        
        return voice_detector
        
    except Exception as e:
        print_error(f"Voice detector initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_microphone_access():
    """Test basic microphone access."""
    print_header("MICROPHONE ACCESS TEST")
    
    try:
        # Test microphone listing
        mics = sr.Microphone.list_microphone_names()
        if mics:
            print_success(f"Found {len(mics)} microphone(s):")
            for i, mic in enumerate(mics):
                print(f"  {i}: {mic}")
        else:
            print_error("No microphones found!")
            return False
        
        # Test microphone access
        with sr.Microphone() as source:
            print_success("Successfully accessed default microphone")
            
            recognizer = sr.Recognizer()
            print_status("Testing ambient noise calibration...")
            recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print_success(f"Calibration complete. Energy threshold: {recognizer.energy_threshold}")
            
        return True
        
    except Exception as e:
        print_error(f"Microphone access failed: {e}")
        return False

def test_platform_optimized_speech(voice_detector):
    """Test speech recognition with platform optimizations."""
    print_header("PLATFORM-OPTIMIZED SPEECH RECOGNITION TEST")
    
    if not voice_detector:
        print_error("Voice detector not available")
        return
    
    print_status(f"Testing speech recognition optimized for {voice_detector.platform_info['name']}")
    print_warning("Please speak clearly when prompted...")
    
    test_modes = ['normal', 'spelling']  # Test key modes
    
    for mode in test_modes:
        print(f"\n🎤 Testing {mode} mode...")
        print_status("Say something now (you have 10 seconds)...")
        
        try:
            result = voice_detector.listen_with_speaker_detection(
                timeout=10,
                silence_threshold=2.0,
                max_total_time=15,
                game_mode=mode if mode != 'normal' else None
            )
            
            if result:
                print_success(f"{mode.title()} mode result: '{result}'")
            else:
                print_warning(f"{mode.title()} mode: No speech detected")
                
        except Exception as e:
            print_error(f"{mode.title()} mode test failed: {e}")
        
        time.sleep(1)  # Brief pause between tests

def main():
    """Main test function."""
    print("🔊 RASPBERRY PI 5 SPEECH RECOGNITION TEST")
    print("This script tests platform-specific speech recognition optimizations")
    print()
    
    try:
        # Run tests
        detect_platform()
        
        if not test_microphone_access():
            print_error("Microphone test failed. Please check your microphone connection.")
            return
        
        voice_detector = test_voice_detector_initialization()
        if voice_detector:
            test_platform_optimized_speech(voice_detector)
        
        print_header("TEST COMPLETE")
        
        if voice_detector and voice_detector.platform_info['type'] == 'raspberry_pi_5':
            print_success("✅ Raspberry Pi 5 optimizations are active!")
            print_status("Your AI Assistant should now work properly with speech recognition.")
            print_status("Energy thresholds have been optimized for Pi 5 USB microphones.")
        else:
            print_warning("⚠️  Not running on Raspberry Pi 5, but platform optimizations are still applied.")
        
        print()
        print("🚀 Ready to test your AI Assistant!")
        print("Run: python3 main.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
    except Exception as e:
        print_error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 