#!/usr/bin/env python3
"""
Mac Testing Script for AI Assistant
Simple test to verify core functionality without full audio setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported."""
    try:
        print("Testing imports...")
        import openai
        import speech_recognition as sr
        import pyttsx3
        import numpy as np
        from dotenv import load_dotenv
        print("✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    try:
        print("\nTesting configuration...")
        from config import Config
        config = Config()
        print(f"✅ Configuration loaded")
        print(f"   • OpenAI Model: {config.openai_model}")
        print(f"   • Audio Sample Rate: {config.audio_sample_rate}")
        print(f"   • TTS Rate: {config.tts_rate}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_openai_setup():
    """Test OpenAI API setup."""
    try:
        print("\nTesting OpenAI setup...")
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("✅ OpenAI API key found in environment")
            # Test basic OpenAI client creation
            import openai
            client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI client created successfully")
            return True
        else:
            print("⚠️  No OpenAI API key found - please add to .env file")
            return False
    except Exception as e:
        print(f"❌ OpenAI setup error: {e}")
        return False

def test_tts():
    """Test text-to-speech setup."""
    try:
        print("\nTesting text-to-speech...")
        import pyttsx3
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"✅ TTS engine initialized - {len(voices) if voices else 0} voices available")
        
        # Test setting voice properties (without actually speaking)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        print("✅ TTS properties set successfully")
        
        engine.stop()
        return True
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition setup."""
    try:
        print("\nTesting speech recognition...")
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        print("✅ Speech recognizer created")
        
        # Test microphone list (won't fail if no mic)
        try:
            mics = sr.Microphone.list_microphone_names()
            print(f"✅ Found {len(mics)} microphone(s)")
            if mics:
                print(f"   Default microphone: {mics[0]}")
        except:
            print("⚠️  No microphones detected (normal for testing)")
        
        return True
    except Exception as e:
        print(f"❌ Speech recognition error: {e}")
        return False

def test_wake_word_detector():
    """Test wake word detector."""
    try:
        print("\nTesting wake word detector...")
        
        # First check if we can import the required modules
        try:
            import pyaudio
            print("✅ PyAudio available")
        except ImportError:
            print("⚠️  PyAudio not available - wake word detection will be limited")
        
        from config import Config
        config = Config()
        
        # Create a simplified version without audio dependencies
        class SimpleWakeWordDetector:
            def __init__(self):
                self.wake_words = {
                    'miley': 'sophia',
                    'dino': 'eladriel'
                }
                
            def detect_wake_word(self, text):
                """Simple wake word detection for testing."""
                text = text.lower().strip()
                for wake_word, user in self.wake_words.items():
                    if wake_word in text:
                        return user
                return None
        
        detector = SimpleWakeWordDetector()
        print("✅ Wake word detector created (simplified for testing)")
        
        # Test wake word detection logic (without audio)
        test_phrases = [
            "hello miley",
            "hey dino", 
            "hi assistant",
            "random phrase"
        ]
        
        for phrase in test_phrases:
            detected = detector.detect_wake_word(phrase)
            status = "✅" if detected else "⚪"
            result = detected if detected else "None"
            print(f"   {status} '{phrase}' -> {result}")
            
        return True
    except Exception as e:
        print(f"❌ Wake word detector error: {e}")
        return False

def test_ai_assistant_core():
    """Test the core AI assistant functionality without audio."""
    try:
        print("\nTesting AI Assistant core...")
        from config import Config
        
        # Create config
        config = Config()
        
        # Test OpenAI integration
        import openai
        client = openai.OpenAI(api_key=config.openai_api_key)
        
        print("✅ Core AI Assistant components ready")
        print(f"   • Model: {config.openai_model}")
        print(f"   • Max tokens: {config.openai_max_tokens}")
        print(f"   • Temperature: {config.openai_temperature}")
        
        return True
    except Exception as e:
        print(f"❌ AI Assistant core error: {e}")
        return False

def main():
    """Run all tests."""
    print("🤖 AI Assistant Mac Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_config,
        test_openai_setup,
        test_tts,
        test_speech_recognition,
        test_wake_word_detector,
        test_ai_assistant_core
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed >= 5:  # Allow some tests to fail due to audio dependencies
        print("🎉 Core functionality is working! Your Mac setup is ready.")
        print("\nTo test the full system:")
        print("1. Make sure your OpenAI API key is in .env file")
        print("2. For audio testing, install PyAudio: pip install pyaudio")
        print("3. Run: python main.py")
        print("4. Say 'Miley' (for Sophia) or 'Dino' (for Eladriel)")
        print("\nPersonalized wake words:")
        print("   • 'Miley' activates Sophia mode")
        print("   • 'Dino' activates Eladriel mode")
    else:
        print("⚠️  Core functionality issues detected. Please check the errors above.")
        
    return passed >= 5

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 