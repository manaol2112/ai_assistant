#!/usr/bin/env python3
"""
Pi 5 Audio Debug Script
Tests current audio settings to debug speech recognition issues.
"""

import sys
import logging
import speech_recognition as sr
from audio_utils import AudioManager
from config import Config
from voice_activity_detector import VoiceActivityDetector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_audio():
    """Test basic audio functionality."""
    print("\n🎤 TESTING BASIC AUDIO FUNCTIONALITY")
    print("=" * 50)
    
    try:
        config = Config()
        audio_manager = AudioManager(config.audio_sample_rate, config.audio_chunk_size)
        
        print(f"✅ Platform: {audio_manager._get_platform_name()}")
        print(f"✅ Energy Threshold: {audio_manager.recognizer.energy_threshold}")
        
        # Test microphone
        mic_working = audio_manager.test_microphone()
        print(f"✅ Microphone Test: {'PASSED' if mic_working else 'FAILED'}")
        
        # Get microphone info
        mic_info = audio_manager.get_microphone_info()
        print(f"✅ Default Microphone: {mic_info['default_mic']['name'] if mic_info['default_mic'] else 'None'}")
        print(f"✅ Available Microphones: {len(mic_info['available_mics'])}")
        
        return audio_manager
        
    except Exception as e:
        print(f"❌ Basic audio test failed: {e}")
        return None

def test_speech_recognition(audio_manager):
    """Test speech recognition with current settings."""
    print("\n🎤 TESTING SPEECH RECOGNITION")
    print("=" * 50)
    
    try:
        print("📢 Say something now (you have 10 seconds)...")
        
        with sr.Microphone() as source:
            print("🎯 Calibrating for ambient noise...")
            audio_manager.recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"🎚️ Energy threshold after calibration: {audio_manager.recognizer.energy_threshold}")
            
            print("👂 Listening for speech...")
            audio = audio_manager.recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            print("🔄 Processing speech...")
            text = audio_manager.recognizer.recognize_google(audio, language='en-US')
            print(f"✅ Recognized: '{text}'")
            return True
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected within timeout")
        return False
    except sr.UnknownValueError:
        print("❓ Could not understand the speech")
        return False
    except Exception as e:
        print(f"❌ Speech recognition failed: {e}")
        return False

def test_voice_activity_detector(audio_manager):
    """Test the voice activity detector."""
    print("\n🎤 TESTING VOICE ACTIVITY DETECTOR")
    print("=" * 50)
    
    try:
        vad = VoiceActivityDetector(audio_manager.recognizer)
        
        print(f"✅ Platform Info: {vad.platform_info}")
        
        # Get optimal thresholds
        settings = vad._get_optimal_thresholds()
        print(f"✅ Optimal Settings: {settings}")
        
        print("📢 Say something now (you have 15 seconds)...")
        print("💡 The voice activity detector will try to detect your speech...")
        
        text = vad.listen_with_speaker_detection(
            timeout=15,
            silence_threshold=2.0,
            max_total_time=30
        )
        
        if text:
            print(f"✅ Voice Activity Detector Result: '{text}'")
            return True
        else:
            print("❌ Voice Activity Detector: No speech detected")
            return False
            
    except Exception as e:
        print(f"❌ Voice Activity Detector failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_energy_threshold_sensitivity():
    """Test different energy threshold values."""
    print("\n🎤 TESTING ENERGY THRESHOLD SENSITIVITY")
    print("=" * 50)
    
    thresholds_to_test = [50, 100, 150, 200, 300]
    
    for threshold in thresholds_to_test:
        print(f"\n🎚️ Testing threshold: {threshold}")
        try:
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = threshold
            
            with sr.Microphone() as source:
                print(f"📢 Say 'hello' (threshold={threshold})...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    text = recognizer.recognize_google(audio, language='en-US')
                    print(f"✅ Threshold {threshold}: '{text}'")
                except sr.WaitTimeoutError:
                    print(f"⏰ Threshold {threshold}: Timeout (too high?)")
                except sr.UnknownValueError:
                    print(f"❓ Threshold {threshold}: Could not understand")
                    
        except Exception as e:
            print(f"❌ Threshold {threshold}: Error - {e}")

def main():
    """Main diagnostic function."""
    print("🤖 PI 5 AUDIO DIAGNOSTIC TOOL")
    print("🔧 This will help debug speech recognition issues")
    print("=" * 60)
    
    # Test 1: Basic Audio
    audio_manager = test_basic_audio()
    if not audio_manager:
        print("\n❌ CRITICAL: Basic audio setup failed!")
        return
    
    # Test 2: Simple Speech Recognition
    print("\n" + "=" * 60)
    speech_working = test_speech_recognition(audio_manager)
    
    # Test 3: Voice Activity Detector
    print("\n" + "=" * 60)
    vad_working = test_voice_activity_detector(audio_manager)
    
    # Test 4: Energy Threshold Sensitivity
    print("\n" + "=" * 60)
    test_energy_threshold_sensitivity()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"✅ Basic Audio: {'WORKING' if audio_manager else 'FAILED'}")
    print(f"✅ Speech Recognition: {'WORKING' if speech_working else 'FAILED'}")
    print(f"✅ Voice Activity Detector: {'WORKING' if vad_working else 'FAILED'}")
    
    if not speech_working:
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Check microphone connection")
        print("2. Try lower energy threshold (50-100)")
        print("3. Verify microphone permissions")
        print("4. Test with different USB ports")
    
    if not vad_working:
        print("\n🔧 VOICE ACTIVITY DETECTOR ISSUES:")
        print("1. May be too sensitive to AI speech filtering")
        print("2. Try speaking more clearly/loudly")
        print("3. Check for background noise")

if __name__ == "__main__":
    main() 