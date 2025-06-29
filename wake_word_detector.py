"""
Wake Word Detection for AI Assistant
Supports custom wake words: "Miley" for Sophia, "Dino" for Eladriel
Enhanced for natural conversation flow
"""

import time
import logging
import threading
from typing import Optional, Dict, Any
import speech_recognition as sr
import numpy as np

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False

from audio_utils import AudioManager


class WakeWordDetector:
    """Detects wake words for different users with natural conversation flow."""
    
    def __init__(self, config):
        """Initialize wake word detector with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # User wake word mappings - FIXED the confusion
        self.wake_words = {
            'miley': 'sophia',
            'dino': 'eladriel',
            'assistant': 'parent'
        }
        
        # More natural wake word variations
        self.wake_word_variations = {
            'miley': ['miley', 'hey miley', 'hi miley', 'hello miley', 'miley cyrus', 'mily', 'mailey'],
            'dino': ['dino', 'hey dino', 'hi dino', 'hello dino', 'dinosaur', 'deeno', 'dinah'],
            'assistant': ['assistant', 'hey assistant', 'hi assistant', 'hello assistant', 'ai assistant', 'hey ai', 'computer']
        }
        
        # Conversation state management
        self.current_user = None
        self.conversation_active = False
        self.last_interaction_time = 0
        self.conversation_timeout = 30  # 30 seconds of inactivity ends conversation
        
        # Use platform-optimized AudioManager (auto-detects Pi 5 + Waveshare settings)
        self.audio_manager = AudioManager()
        
        self.is_listening = False
        self.porcupine = None
        
        # Try to initialize Porcupine for advanced wake word detection
        if PORCUPINE_AVAILABLE and config.porcupine_access_key:
            self._init_porcupine()
        else:
            self.logger.info("Using fallback speech recognition for wake word detection")
        
        self.logger.info("WakeWordDetector initialized with natural conversation flow")

    def _init_porcupine(self):
        """Initialize Porcupine wake word engine if available."""
        try:
            # Note: This would require custom wake word files for "Miley" and "Dino"
            # For now, we'll use the fallback method
            self.logger.info("Porcupine available but using fallback method for custom wake words")
        except Exception as e:
            self.logger.error(f"Failed to initialize Porcupine: {e}")
            self.porcupine = None

    def is_conversation_active(self) -> bool:
        """Check if we're currently in an active conversation."""
        if not self.conversation_active:
            return False
        
        # Check if conversation has timed out
        time_since_last = time.time() - self.last_interaction_time
        if time_since_last > self.conversation_timeout:
            self.end_conversation()
            return False
        
        return True

    def start_conversation(self, user: str):
        """Start a conversation with a specific user."""
        self.current_user = user
        self.conversation_active = True
        self.last_interaction_time = time.time()
        self.logger.info(f"Started conversation with {user}")

    def continue_conversation(self):
        """Continue the current conversation (reset timeout)."""
        if self.conversation_active:
            self.last_interaction_time = time.time()

    def end_conversation(self):
        """End the current conversation."""
        if self.conversation_active:
            self.logger.info(f"Ended conversation with {self.current_user}")
        self.current_user = None
        self.conversation_active = False
        self.last_interaction_time = 0

    def _detect_wake_word_in_text(self, text: str) -> Optional[str]:
        """Detect wake words in recognized text."""
        text = text.lower().strip()
        
        # If we're in a conversation, any speech continues it (no wake word needed)
        if self.is_conversation_active():
            self.continue_conversation()
            return self.current_user
        
        # Look for wake words to start new conversation
        for wake_word, user in self.wake_words.items():
            # Check exact match
            if wake_word in text:
                self.logger.info(f"Wake word '{wake_word}' detected for {user}")
                self.start_conversation(user)
                return user
            
            # Check variations
            variations = self.wake_word_variations.get(wake_word, [])
            for variation in variations:
                if variation in text:
                    self.logger.info(f"Wake word variation '{variation}' detected for {user}")
                    self.start_conversation(user)
                    return user
        
        return None

    def listen_for_wake_word(self, timeout: int = 1) -> Optional[str]:
        """Listen for wake words and return detected user."""
        try:
            # Use speech recognition to continuously listen
            audio_data = self.audio_manager.listen_for_audio(timeout=timeout, phrase_time_limit=3)
            
            if audio_data:
                # Convert audio to text
                text = self.audio_manager.audio_to_text(audio_data)
                
                if text:
                    # Check if any wake word was detected or conversation continues
                    detected_user = self._detect_wake_word_in_text(text)
                    return detected_user
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error during wake word detection: {e}")
            return None

    def continuous_listen(self, callback_func):
        """Continuously listen for wake words in a separate thread."""
        def listen_loop():
            self.is_listening = True
            self.logger.info("Starting continuous wake word listening with natural conversation flow...")
            
            while self.is_listening:
                try:
                    detected_user = self.listen_for_wake_word(timeout=1)
                    if detected_user:
                        callback_func(detected_user)
                    
                    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                    
                except Exception as e:
                    self.logger.error(f"Error in continuous listening: {e}")
                    time.sleep(1)  # Longer delay on error
        
        listen_thread = threading.Thread(target=listen_loop, daemon=True)
        listen_thread.start()
        return listen_thread

    def test_wake_words(self):
        """Test wake word detection by asking user to say wake words."""
        print("\n🧪 Testing Enhanced Wake Word Detection")
        print("Say the following wake words to test detection:")
        print("   • 'Hey Miley' or 'Miley' (for Sophia)")
        print("   • 'Hey Dino' or 'Dino' (for Eladriel)")
        print("Once detected, continue talking naturally - no need to repeat wake words!")
        print("Conversation will timeout after 30 seconds of silence.")
        print("Listening for 60 seconds...")
        
        start_time = time.time()
        while time.time() - start_time < 60:
            detected_user = self.listen_for_wake_word(timeout=2)
            if detected_user:
                status = "continuing conversation" if self.is_conversation_active() else "new conversation"
                print(f"✅ Detected: {detected_user.title()} ({status})")
            else:
                print(".", end="", flush=True)
        
        print("\n🏁 Wake word test completed")

    def calibrate_sensitivity(self):
        """Calibrate wake word detection sensitivity."""
        print("\n📏 Calibrating wake word sensitivity...")
        
        # Calibrate audio for ambient noise
        self.audio_manager.calibrate_audio(duration=3)
        
        # Test microphone
        if not self.audio_manager.test_microphone():
            print("❌ Microphone test failed")
            return False
        
        print("✅ Wake word sensitivity calibrated")
        return True

    def get_detection_stats(self) -> Dict[str, Any]:
        """Get statistics about wake word detection."""
        mic_info = self.audio_manager.get_microphone_info()
        
        stats = {
            "wake_words_supported": list(self.wake_words.keys()),
            "users_supported": list(self.wake_words.values()),
            "porcupine_available": PORCUPINE_AVAILABLE,
            "using_advanced_detection": self.porcupine is not None,
            "microphone_info": mic_info,
            "audio_sample_rate": self.audio_manager.sample_rate,
            "audio_chunk_size": self.audio_manager.chunk_size,
            "wake_word_sensitivity": self.config.wake_word_sensitivity,
            "conversation_active": self.conversation_active,
            "current_user": self.current_user,
            "conversation_timeout": self.conversation_timeout
        }
        
        return stats

    def stop(self):
        """Stop wake word detection."""
        self.is_listening = False
        self.end_conversation()
        if hasattr(self, 'porcupine') and self.porcupine:
            self.porcupine.delete()
        if hasattr(self, 'audio_manager'):
            self.audio_manager.cleanup()
        self.logger.info("Wake word detector stopped")

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.stop()
        except Exception as e:
            # Ignore errors during cleanup
            pass 