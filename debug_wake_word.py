#!/usr/bin/env python3
"""
Comprehensive Wake Word Debugging Script for Raspberry Pi 5
This script will help diagnose wake word detection issues step by step.
"""

import sys
import os
import time
import logging
from typing import Optional

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from config import Config
from audio_utils import AudioManager
from wake_word_detector import WakeWordDetector

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('wake_word_debug.log')
    ]
)
logger = logging.getLogger(__name__)

class WakeWordDebugger:
    def __init__(self):
        self.config = Config()
        self.audio_manager = None
        self.wake_word_detector = None
        
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "="*60)
        print(f"🔍 {title}")
        print("="*60)
        
    def test_audio_manager(self):
        """Test AudioManager initialization and basic functionality."""
        self.print_header("STEP 1: Testing AudioManager")
        
        try:
            self.audio_manager = AudioManager()
            print(f"✅ AudioManager initialized successfully")
            print(f"   📊 Sample Rate: {self.audio_manager.sample_rate}Hz")
            print(f"   📊 Chunk Size: {self.audio_manager.chunk_size}")
            print(f"   📊 Energy Threshold: {self.audio_manager.energy_threshold}")
            
            # Test microphone
            print("\n🎤 Testing microphone...")
            if self.audio_manager.test_microphone():
                print("✅ Microphone test passed")
            else:
                print("❌ Microphone test failed")
                return False
                
            # Get microphone info
            mic_info = self.audio_manager.get_microphone_info()
            print(f"🎤 Microphone Info: {mic_info}")
            
            return True
            
        except Exception as e:
            print(f"❌ AudioManager initialization failed: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def test_audio_calibration(self):
        """Test audio calibration."""
        self.print_header("STEP 2: Testing Audio Calibration")
        
        try:
            print("🔧 Calibrating audio for ambient noise...")
            print("   Please stay quiet for 3 seconds...")
            
            self.audio_manager.calibrate_audio(duration=3)
            print(f"✅ Audio calibrated")
            print(f"   📊 New Energy Threshold: {self.audio_manager.energy_threshold}")
            
            return True
            
        except Exception as e:
            print(f"❌ Audio calibration failed: {e}")
            return False
    
    def test_basic_speech_recognition(self):
        """Test basic speech recognition."""
        self.print_header("STEP 3: Testing Basic Speech Recognition")
        
        try:
            print("🎤 Testing basic speech recognition...")
            print("   Please say something (you have 5 seconds)...")
            
            audio_data = self.audio_manager.listen_for_audio(timeout=5, phrase_time_limit=3)
            
            if audio_data:
                print("✅ Audio captured successfully")
                
                # Convert to text
                text = self.audio_manager.audio_to_text(audio_data)
                
                if text:
                    print(f"✅ Speech recognized: '{text}'")
                    return True
                else:
                    print("❌ Speech recognition failed - no text returned")
                    return False
            else:
                print("❌ No audio captured")
                return False
                
        except Exception as e:
            print(f"❌ Speech recognition test failed: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def test_wake_word_detector_init(self):
        """Test WakeWordDetector initialization."""
        self.print_header("STEP 4: Testing WakeWordDetector Initialization")
        
        try:
            self.wake_word_detector = WakeWordDetector(self.config)
            print("✅ WakeWordDetector initialized successfully")
            
            # Get detection stats
            stats = self.wake_word_detector.get_detection_stats()
            print(f"📊 Detection Stats:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            return True
            
        except Exception as e:
            print(f"❌ WakeWordDetector initialization failed: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def test_wake_word_detection_single(self):
        """Test single wake word detection."""
        self.print_header("STEP 5: Testing Single Wake Word Detection")
        
        try:
            print("🎤 Testing single wake word detection...")
            print("   Say one of these wake words:")
            print("   • 'Hey Miley' or 'Miley' (for Sophia)")
            print("   • 'Hey Dino' or 'Dino' (for Eladriel)")
            print("   You have 10 seconds...")
            
            detected_user = self.wake_word_detector.listen_for_wake_word(timeout=10)
            
            if detected_user:
                print(f"✅ Wake word detected for: {detected_user}")
                return True
            else:
                print("❌ No wake word detected")
                return False
                
        except Exception as e:
            print(f"❌ Wake word detection failed: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def test_continuous_wake_word_detection(self):
        """Test continuous wake word detection."""
        self.print_header("STEP 6: Testing Continuous Wake Word Detection")
        
        try:
            print("🎤 Testing continuous wake word detection...")
            print("   This will run for 30 seconds")
            print("   Try saying wake words multiple times:")
            print("   • 'Hey Miley' or 'Miley' (for Sophia)")
            print("   • 'Hey Dino' or 'Dino' (for Eladriel)")
            print("   Starting in 3 seconds...")
            
            time.sleep(3)
            
            start_time = time.time()
            detection_count = 0
            attempt_count = 0
            
            while time.time() - start_time < 30:
                attempt_count += 1
                print(f"   Attempt #{attempt_count}...", end="", flush=True)
                
                detected_user = self.wake_word_detector.listen_for_wake_word(timeout=1)
                
                if detected_user:
                    detection_count += 1
                    print(f" ✅ DETECTED: {detected_user}")
                else:
                    print(" ❌")
                
                time.sleep(0.1)
            
            print(f"\n📊 Results:")
            print(f"   Total attempts: {attempt_count}")
            print(f"   Successful detections: {detection_count}")
            print(f"   Success rate: {(detection_count/attempt_count)*100:.1f}%")
            
            return detection_count > 0
            
        except Exception as e:
            print(f"❌ Continuous wake word detection failed: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests in sequence."""
        self.print_header("COMPREHENSIVE WAKE WORD DEBUGGING")
        
        print("🚀 Starting comprehensive wake word debugging...")
        print("   This will test all components step by step")
        
        tests = [
            ("AudioManager", self.test_audio_manager),
            ("Audio Calibration", self.test_audio_calibration),
            ("Basic Speech Recognition", self.test_basic_speech_recognition),
            ("WakeWordDetector Init", self.test_wake_word_detector_init),
            ("Single Wake Word Detection", self.test_wake_word_detection_single),
            ("Continuous Wake Word Detection", self.test_continuous_wake_word_detection)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running {test_name}...")
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results[test_name] = False
        
        # Print final results
        self.print_header("FINAL RESULTS")
        
        passed = 0
        total = len(tests)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        print(f"\n📊 Overall Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Wake word detection should work perfectly!")
        elif passed >= total * 0.8:
            print("⚠️  Most tests passed. There may be minor issues.")
        else:
            print("❌ Major issues detected. Wake word detection needs fixing.")
        
        return passed, total

def main():
    """Main function to run the debugging."""
    print("🔍 Wake Word Detection Debugging Script")
    print("   This script will help diagnose wake word detection issues")
    print("   Make sure you're in a quiet environment for best results")
    
    debugger = WakeWordDebugger()
    
    try:
        passed, total = debugger.run_comprehensive_test()
        
        print(f"\n📋 Debug log saved to: wake_word_debug.log")
        print(f"📊 Final Score: {passed}/{total} tests passed")
        
        if passed < total:
            print("\n💡 Troubleshooting Tips:")
            print("   1. Check microphone connections")
            print("   2. Verify audio levels (not too loud/quiet)")
            print("   3. Ensure minimal background noise")
            print("   4. Try speaking clearly and at normal volume")
            print("   5. Check the debug log for detailed error messages")
        
    except KeyboardInterrupt:
        print("\n🛑 Debugging interrupted by user")
    except Exception as e:
        print(f"\n💥 Debugging crashed: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main() 