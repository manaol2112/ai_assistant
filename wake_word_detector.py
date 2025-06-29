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
    
    def __init__(self, config, audio_manager=None):
        """Initialize wake word detector with shared AudioManager to prevent resource conflicts."""
        self.config = config
        self.current_user = None
        self.conversation_active = False
        
        # Use shared AudioManager or create new one if none provided
        if audio_manager:
            self.audio_manager = audio_manager
            self.logger.info("WakeWordDetector: Using shared AudioManager (prevents resource conflicts)")
        else:
            # Fallback for backward compatibility
            self.audio_manager = AudioManager()
            self.logger.info("WakeWordDetector: Created new AudioManager instance")
        
        self.logger = logging.getLogger(__name__)
        
        # Try to initialize Porcupine (if available)
        self.porcupine = None
        try:
            import pvporcupine
            self.porcupine = pvporcupine.create(
                keywords=["hey google", "alexa", "computer"]  # Generic wake words
            )
            self.logger.info("Porcupine wake word engine initialized")
        except ImportError:
            self.logger.info("Porcupine not available, using speech recognition fallback")
        except Exception as e:
            self.logger.warning(f"Porcupine initialization failed: {e}, using speech recognition fallback")
        
        # Wake word patterns for speech recognition fallback
        self.wake_patterns = {
            'sophia': ['miley', 'hey miley', 'hi miley', 'miley cyrus', 'miley help'],
            'eladriel': ['dino', 'hey dino', 'hi dino', 'dinosaur', 'dino help'],
            'parent': ['assistant', 'hey assistant', 'hi assistant', 'computer', 'ai assistant']
        }
        
        # More natural wake word variations
        self.wake_word_variations = {
            'miley': ['miley', 'hey miley', 'hi miley', 'hello miley', 'miley cyrus', 'mily', 'mailey'],
            'dino': ['dino', 'hey dino', 'hi dino', 'hello dino', 'dinosaur', 'deeno', 'dinah'],
            'assistant': ['assistant', 'hey assistant', 'hi assistant', 'hello assistant', 'ai assistant', 'hey ai', 'computer']
        }
        
        # Conversation state management
        self.last_interaction_time = 0
        self.conversation_timeout = 30  # 30 seconds of inactivity ends conversation
        
        self.is_listening = False
        
        self.logger.info("WakeWordDetector initialized with natural conversation flow")

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
        self.logger.info(f"🔍 WAKE WORD DEBUG: Analyzing text: '{text}'")
        
        # If we're in a conversation, any speech continues it (no wake word needed)
        if self.is_conversation_active():
            self.logger.info("🔍 WAKE WORD DEBUG: Conversation is active, continuing with current user")
            self.continue_conversation()
            return self.current_user
        
        self.logger.info("🔍 WAKE WORD DEBUG: No active conversation, checking for wake words...")
        
        # Look for wake words to start new conversation
        for user, wake_word_list in self.wake_patterns.items():
            self.logger.info(f"🔍 WAKE WORD DEBUG: Checking wake words for user '{user}': {wake_word_list}")
            
            # Check each wake word pattern for this user
            for wake_word in wake_word_list:
                if wake_word in text:
                    self.logger.info(f"🎉 WAKE WORD DEBUG: Match found! '{wake_word}' detected for {user}")
                    self.start_conversation(user)
                    return user
        
        self.logger.info("🔍 WAKE WORD DEBUG: No wake words found in text")
        return None

    def listen_for_wake_word(self, timeout: int = 1) -> Optional[str]:
        """Listen for wake words and return detected user."""
        try:
            # DEBUG: Show that we're actively listening
            self.logger.info(f"🎤 WAKE WORD DEBUG: Starting listen cycle (timeout={timeout}s)")
            
            # Use speech recognition to continuously listen
            audio_data = self.audio_manager.listen_for_audio(timeout=timeout, phrase_time_limit=3)
            
            if audio_data:
                self.logger.info("🎤 WAKE WORD DEBUG: Audio data captured, converting to text...")
                
                # Convert audio to text
                text = self.audio_manager.audio_to_text(audio_data)
                
                if text:
                    self.logger.info(f"🎤 WAKE WORD DEBUG: Recognized text: '{text}'")
                    
                    # Check if any wake word was detected or conversation continues
                    detected_user = self._detect_wake_word_in_text(text)
                    
                    if detected_user:
                        self.logger.info(f"🎉 WAKE WORD DEBUG: User detected: {detected_user}")
                    else:
                        self.logger.info(f"🎤 WAKE WORD DEBUG: No wake word found in: '{text}'")
                    
                    return detected_user
                else:
                    self.logger.info("🎤 WAKE WORD DEBUG: Audio captured but no text recognized")
            else:
                self.logger.debug("🎤 WAKE WORD DEBUG: No audio data captured (timeout/silence)")
            
            return None
            
        except Exception as e:
            self.logger.error(f"🎤 WAKE WORD DEBUG: Error during wake word detection: {e}")
            import traceback
            self.logger.error(f"🎤 WAKE WORD DEBUG: Traceback: {traceback.format_exc()}")
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
            "wake_words_supported": list(self.wake_patterns.keys()),
            "users_supported": list(self.wake_patterns.keys()),
            "porcupine_available": PORCUPINE_AVAILABLE,
            "using_advanced_detection": self.porcupine is not None,
            "microphone_info": mic_info,
            "audio_sample_rate": self.audio_manager.sample_rate,
            "audio_chunk_size": self.audio_manager.chunk_size,
            "wake_word_sensitivity": getattr(self.config, 'wake_word_sensitivity', 'default'),
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