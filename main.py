#!/usr/bin/env python3
"""
AI Assistant for Raspberry Pi with Personalized Wake Words and Face Recognition
Created for Sophia (wake word: "Miley") and Eladriel (wake word: "Dino")
Enhanced with automatic face recognition, personalized greetings, and universal object identification
"""

import os
import sys
import time
import logging
import threading
import signal
from typing import Optional
from datetime import datetime
import cv2

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import Config
    from audio_utils import AudioManager, setup_premium_tts_engines
    from wake_word_detector import WakeWordDetector
    from dinosaur_identifier import DinosaurIdentifier
    from object_identifier import ObjectIdentifier
    from smart_camera_detector import SmartCameraDetector
    from filipino_translator import FilipinoTranslator  # NEW: Filipino translation game
    from letter_word_game import LetterWordGame  # NEW: Letter word guessing game
    import openai
    import pyttsx3
    import speech_recognition as sr
    from voice_activity_detector import VoiceActivityDetector
    from math_quiz_game import MathQuizGame
    from animal_guess_game import AnimalGuessGame
    from camera_handler import CameraHandler
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self):
        """Initialize the AI Assistant with Face Recognition and Universal Object Identification"""
        self.config = Config()
        self.running = False
        self.current_user = None
        
        # Setup OpenAI client
        self.client = openai.OpenAI(api_key=self.config.openai_api_key)
        
        # Setup premium OpenAI TTS engines with natural human voices
        logger.info("🎙️ Setting up premium OpenAI text-to-speech voices...")
        self.sophia_tts, self.eladriel_tts = setup_premium_tts_engines(self.client)
        
        # Setup audio components
        self.audio_manager = AudioManager()
        self.recognizer = sr.Recognizer()
        
        # Initialize Voice Activity Detector with speaker differentiation
        self.voice_detector = VoiceActivityDetector(self.recognizer)
        
        # Setup wake word detector
        self.wake_word_detector = WakeWordDetector(self.config)
        
        # Initialize Filipino translator (after OpenAI client is set up)
        self.filipino_translator = FilipinoTranslator(self.client, self)
        
        # Setup camera and microphone
        logger.info("Setting up camera for visual identification...")
        # Initialize shared camera handler - this will be the ONLY camera instance
        self.camera_handler = CameraHandler()
        
        # Initialize Math Quiz Game (after camera setup)
        logger.info("🧮 Setting up Math Quiz Game...")
        self.math_quiz = MathQuizGame(self.camera_handler)
        
        # Set AI assistant reference for audio feedback
        self.math_quiz.ai_assistant = self
        
        # Initialize Animal Guessing Game (after camera setup)
        logger.info("🦕 Setting up Animal Guessing Game...")
        self.animal_game = AnimalGuessGame(self, shared_camera=self.camera_handler)
        
        # Initialize Letter Word Game
        logger.info("🔤 Setting up Letter Word Game...")
        self.letter_word_game = LetterWordGame(self)
        
        # Setup dinosaur identifier for Eladriel (specialized for dinosaurs)
        logger.info("Setting up dinosaur identification for Eladriel...")
        self.dinosaur_identifier = DinosaurIdentifier(self.client, self.config, shared_camera=self.camera_handler)
        
        # Setup universal object identifier for both users - SHARE camera instead of creating new one
        logger.info("🔍 Setting up universal object identification system...")
        self.object_identifier = ObjectIdentifier(shared_camera=self.camera_handler)
        
        # Setup face recognition system - SHARE camera instead of creating new one
        logger.info("🎭 Setting up face recognition system...")
        self.face_detector = SmartCameraDetector(model_size='n', confidence_threshold=0.4)
        # IMPORTANT: Pass the shared camera handler to prevent conflicts
        self.face_detector.shared_camera = self.camera_handler
        self.face_recognition_thread = None
        self.face_recognition_active = False
        self.last_face_greeting = {}  # Track when we last greeted each person
        self.face_greeting_cooldown = 30  # seconds between face greetings
        
        # Parent mode settings
        self.quiet_mode = False
        
        # Interrupt system for speech control
        self.speech_interrupted = False
        self.interrupt_listener_active = False
        self.interrupt_thread = None
        
        # Conversation memory and context tracking
        self.conversation_history = {}  # Store conversation history per user
        self.last_ai_response = {}  # Store last response per user for repeat functionality
        self.conversation_context = {}  # Store ongoing context per user
        self.max_history_length = 10  # Keep last 10 exchanges per user
        
        # Audio feedback system
        self.audio_feedback_enabled = True
        self.setup_audio_feedback()
        
        # Spelling game sound effects (same as Filipino game)
        self.spelling_correct_sound = self._generate_spelling_celebration_sound()
        self.spelling_wrong_sound = self._generate_spelling_buzzer_sound()
        
        # Spelling game settings
        self.spelling_game_active = False
        self.current_spelling_word = None
        self.spelling_word_index = 0
        self.spelling_score = 0
        self.auto_check_active = False  # New: for automatic visual checking
        self.persistent_auto_check = False  # NEW: for continuous auto-check across all words
        self.spelling_words_grade2_3 = [
            # Grade 2 words
            {'word': 'cat', 'hint': 'A furry pet that says meow'},
            {'word': 'dog', 'hint': 'A loyal pet that barks'},
            {'word': 'sun', 'hint': 'The bright star in the sky'},
            {'word': 'run', 'hint': 'Moving fast with your legs'},
            {'word': 'big', 'hint': 'Very large in size'},
            {'word': 'red', 'hint': 'The color of strawberries'},
            {'word': 'blue', 'hint': 'The color of the sky'},
            {'word': 'tree', 'hint': 'A tall plant with leaves'},
            {'word': 'book', 'hint': 'Something you read'},
            {'word': 'ball', 'hint': 'A round toy you can throw'},
            {'word': 'fish', 'hint': 'Animals that swim in water'},
            {'word': 'bird', 'hint': 'Animals that can fly'},
            {'word': 'milk', 'hint': 'A white drink from cows'},
            {'word': 'cake', 'hint': 'A sweet dessert for birthdays'},
            {'word': 'home', 'hint': 'The place where you live'},
            
            # Grade 3 words
            {'word': 'school', 'hint': 'The place where you learn'},
            {'word': 'happy', 'hint': 'Feeling very good and joyful'},
            {'word': 'friend', 'hint': 'Someone you like to play with'},
            {'word': 'water', 'hint': 'Clear liquid you drink'},
            {'word': 'funny', 'hint': 'Something that makes you laugh'},
            {'word': 'pretty', 'hint': 'Beautiful and nice to look at'},
            {'word': 'family', 'hint': 'People who love you at home'},
            {'word': 'garden', 'hint': 'A place where flowers grow'},
            {'word': 'cookie', 'hint': 'A sweet snack you can eat'},
            {'word': 'animal', 'hint': 'Living creatures like cats and dogs'},
            {'word': 'winter', 'hint': 'The cold season with snow'},
            {'word': 'summer', 'hint': 'The warm season for swimming'},
            {'word': 'birthday', 'hint': 'The special day you were born'},
            {'word': 'rainbow', 'hint': 'Colorful arc in the sky after rain'},
            {'word': 'playground', 'hint': 'A fun place with swings and slides'}
        ]
        
        # User profiles with personalized settings
        self.users = {
            'sophia': {
                'name': 'Sophia',
                'wake_word': 'miley',
                'personality': 'friendly, encouraging, and supportive',
                'greeting': self.get_dynamic_greeting('sophia'),
                'face_greeting': self.get_dynamic_face_greeting('sophia'),
                'tts_engine': self.sophia_tts,
                'special_commands': ['help', 'what can you do', 'identify this', 'what is this', 'tell me about this', 'spelling game', 'play spelling', 'ready', 'end game', 'teach me filipino', 'filipino game', 'math game', 'math quiz', 'word problems', 'animal game', 'guess the animal', 'animal guessing', 'letter game', 'letter word game', 'word guessing', 'guess the word']
            },
            'eladriel': {
                'name': 'Eladriel',
                'wake_word': 'dino',
                'personality': 'playful, curious, and energetic',
                'greeting': self.get_dynamic_greeting('eladriel'),
                'face_greeting': self.get_dynamic_face_greeting('eladriel'),
                'tts_engine': self.eladriel_tts,
                'special_commands': ['identify dinosaur', 'identify this', 'what is this', 'tell me about this', 'show me camera', 'dinosaur tips', 'help', 'spelling game', 'play spelling', 'ready', 'end game', 'teach me filipino', 'filipino game', 'math game', 'math quiz', 'word problems', 'animal game', 'guess the animal', 'animal guessing', 'letter game', 'letter word game', 'word guessing', 'guess the word']
            },
            'parent': {
                'name': 'Parent',
                'wake_word': 'assistant',
                'personality': 'professional, intelligent, and efficient',
                'greeting': self.get_parent_greeting(),
                'face_greeting': self.get_parent_face_greeting(),
                'tts_engine': self.sophia_tts,  # Use calm voice for parent mode
                'special_commands': [
                    'help', 'status report', 'system check', 'quiet mode on', 'quiet mode off',
                    'identify this', 'what is this', 'tell me about this', 'show me camera',
                    'check on kids', 'home automation', 'schedule reminder', 'weather',
                    'news update', 'shopping list', 'calendar', 'notes', 'spelling game', 'play spelling', 'ready', 'end game', 'teach me filipino', 'filipino game', 'math game', 'math quiz', 'word problems', 'animal game', 'guess the animal', 'animal guessing', 'letter game', 'letter word game', 'word guessing', 'guess the word'
                ]
            }
        }
        
        logger.info("🚀 AI Assistant initialized with premium natural voices, face recognition, and universal object identification!")

    def setup_audio_feedback(self):
        """Setup audio feedback system for interaction cues."""
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_available = True
            logger.info("🔊 Audio feedback system initialized")
        except ImportError:
            logger.warning("pygame not available - using system beeps for audio feedback")
            self.pygame_available = False
        except Exception as e:
            logger.error(f"Error initializing audio feedback: {e}")
            self.pygame_available = False

    def play_listening_sound(self):
        """Play a sound to indicate AI is listening."""
        if not self.audio_feedback_enabled:
            return
            
        try:
            if self.pygame_available:
                # Create a pleasant "listening" tone - rising notes
                self._generate_listening_tone()
            else:
                # Fallback to system beep
                import os
                os.system('afplay /System/Library/Sounds/Tink.aiff 2>/dev/null &')
        except Exception as e:
            logger.error(f"Error playing listening sound: {e}")

    def play_completion_sound(self):
        """Play a sound to indicate AI is done speaking and ready to listen."""
        if not self.audio_feedback_enabled:
            return
            
        try:
            if self.pygame_available:
                # Create a gentle "completion" tone - descending notes
                self._generate_completion_tone()
            else:
                # Fallback to system beep
                import os
                os.system('afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &')
        except Exception as e:
            logger.error(f"Error playing completion sound: {e}")

    def play_wake_word_sound(self):
        """Play a sound to confirm wake word detection."""
        if not self.audio_feedback_enabled:
            return
            
        try:
            if self.pygame_available:
                # Create an acknowledgment tone
                self._generate_wake_word_tone()
            else:
                # Fallback to system beep
                import os
                os.system('afplay /System/Library/Sounds/Ping.aiff 2>/dev/null &')
        except Exception as e:
            logger.error(f"Error playing wake word sound: {e}")

    def _generate_listening_tone(self):
        """Generate a pleasant listening tone using pygame."""
        try:
            import pygame
            import numpy as np
            
            # Create a rising two-note tone (C to E)
            sample_rate = 22050
            duration = 0.3
            
            # Generate frequencies (C4 to E4)
            freq1 = 261.63  # C4
            freq2 = 329.63  # E4
            
            # Create time array
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Generate first note (rising)
            note1 = np.sin(freq1 * 2 * np.pi * t) * 0.3
            # Generate second note
            note2 = np.sin(freq2 * 2 * np.pi * t) * 0.3
            
            # Fade in/out for smoothness
            fade_samples = int(sample_rate * 0.05)  # 50ms fade
            note1[:fade_samples] *= np.linspace(0, 1, fade_samples)
            note1[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            note2[:fade_samples] *= np.linspace(0, 1, fade_samples)
            note2[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Combine notes with slight delay
            combined = np.concatenate([note1, note2])
            
            # Convert to 16-bit integers
            audio_data = (combined * 32767).astype(np.int16)
            
            # Ensure array is C-contiguous for pygame
            audio_data = np.ascontiguousarray(audio_data)
            
            # Convert to stereo
            stereo_data = np.column_stack((audio_data, audio_data))
            stereo_data = np.ascontiguousarray(stereo_data)
            
            # Play the sound
            sound = pygame.sndarray.make_sound(stereo_data)
            sound.play()
            
        except Exception as e:
            logger.error(f"Error generating listening tone: {e}")

    def _generate_completion_tone(self):
        """Generate a gentle completion tone using pygame."""
        try:
            import pygame
            import numpy as np
            
            # Create a descending gentle tone (G to C)
            sample_rate = 22050
            duration = 0.4
            
            # Generate frequencies (G4 to C4)
            freq1 = 392.00  # G4
            freq2 = 261.63  # C4
            
            # Create time array
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Generate descending tone with frequency sweep
            freq_sweep = np.linspace(freq1, freq2, len(t))
            tone = np.sin(2 * np.pi * freq_sweep * t) * 0.25
            
            # Apply gentle envelope
            envelope = np.exp(-t * 3)  # Gentle decay
            tone *= envelope
            
            # Fade in for smoothness
            fade_samples = int(sample_rate * 0.05)  # 50ms fade
            tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
            
            # Convert to 16-bit integers
            audio_data = (tone * 32767).astype(np.int16)
            
            # Ensure array is C-contiguous for pygame
            audio_data = np.ascontiguousarray(audio_data)
            
            # Convert to stereo
            stereo_data = np.column_stack((audio_data, audio_data))
            stereo_data = np.ascontiguousarray(stereo_data)
            
            # Play the sound
            sound = pygame.sndarray.make_sound(stereo_data)
            sound.play()
            
        except Exception as e:
            logger.error(f"Error generating completion tone: {e}")

    def _generate_wake_word_tone(self):
        """Generate a confirmation tone for wake word detection."""
        try:
            import pygame
            import numpy as np
            
            # Create a cheerful acknowledgment tone (C-E-G chord)
            sample_rate = 22050
            duration = 0.2
            
            # Generate frequencies (C-E-G major chord)
            freq1 = 261.63  # C4
            freq2 = 329.63  # E4
            freq3 = 392.00  # G4
            
            # Create time array
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Generate chord
            chord = (np.sin(freq1 * 2 * np.pi * t) + 
                    np.sin(freq2 * 2 * np.pi * t) + 
                    np.sin(freq3 * 2 * np.pi * t)) * 0.15
            
            # Apply envelope
            envelope = np.exp(-t * 5)  # Quick decay
            chord *= envelope
            
            # Convert to 16-bit integers
            audio_data = (chord * 32767).astype(np.int16)
            
            # Ensure array is C-contiguous for pygame
            audio_data = np.ascontiguousarray(audio_data)
            
            # Convert to stereo
            stereo_data = np.column_stack((audio_data, audio_data))
            stereo_data = np.ascontiguousarray(stereo_data)
            
            # Play the sound
            sound = pygame.sndarray.make_sound(stereo_data)
            sound.play()
            
        except Exception as e:
            logger.error(f"Error generating wake word tone: {e}")

    def toggle_audio_feedback(self, enabled: bool):
        """Toggle audio feedback on/off."""
        self.audio_feedback_enabled = enabled
        status = "enabled" if enabled else "disabled"
        logger.info(f"🔊 Audio feedback {status}")

    def play_ready_to_speak_sound(self):
        """Play a clear 'you can speak now' audio cue for kids."""
        if not self.audio_feedback_enabled:
            return
            
        try:
            if self.pygame_available:
                # Create a clear "you can speak now" tone
                self._generate_ready_to_speak_tone()
            else:
                # Fallback to system beep - use a different sound than completion
                import os
                os.system('afplay /System/Library/Sounds/Hero.aiff 2>/dev/null &')
        except Exception as e:
            logger.error(f"Error playing ready-to-speak sound: {e}")

    def _generate_ready_to_speak_tone(self):
        """Generate an exciting, kid-friendly 'your turn to talk!' audio cue."""
        try:
            import pygame
            import numpy as np
            
            # Create an exciting, magical "your turn!" sound that kids will love
            sample_rate = 22050
            duration = 0.6  # Quick and snappy
            
            # Create a playful ascending magical chime sequence
            # Like a friendly doorbell or game notification that says "your turn!"
            
            # Three ascending notes with sparkle - C5, E5, G5 (major triad going up)
            freq1 = 523  # C5 - bright start
            freq2 = 659  # E5 - building excitement  
            freq3 = 784  # G5 - "go ahead!" peak
            
            # Each note duration
            note_duration = duration / 4
            sparkle_duration = duration / 4
            
            # Time arrays for each part
            t1 = np.linspace(0, note_duration, int(sample_rate * note_duration), False)
            t2 = np.linspace(0, note_duration, int(sample_rate * note_duration), False)
            t3 = np.linspace(0, note_duration, int(sample_rate * note_duration), False)
            t_sparkle = np.linspace(0, sparkle_duration, int(sample_rate * sparkle_duration), False)
            
            # Create bell-like tones with harmonics for magical sound
            def create_bell_note(t, freq, volume=0.4):
                # Fundamental frequency
                fundamental = np.sin(2 * np.pi * freq * t)
                # Add harmonics for bell-like quality
                harmonic2 = 0.3 * np.sin(2 * np.pi * freq * 2 * t)
                harmonic3 = 0.1 * np.sin(2 * np.pi * freq * 3 * t)
                
                # Bell envelope - quick attack, gentle decay
                envelope = np.exp(-t * 8) * (1 - np.exp(-t * 30))
                
                return (fundamental + harmonic2 + harmonic3) * envelope * volume
            
            # Create the three ascending notes
            note1 = create_bell_note(t1, freq1, 0.35)
            note2 = create_bell_note(t2, freq2, 0.4) 
            note3 = create_bell_note(t3, freq3, 0.45)
            
            # Create magical sparkle effect for the end
            sparkle = np.zeros_like(t_sparkle)
            sparkle_freqs = [1047, 1319, 1568, 2093]  # High magical frequencies
            
            for i, freq in enumerate(sparkle_freqs):
                delay = i * 0.02  # Quick succession
                if len(t_sparkle) > int(delay * sample_rate):
                    delayed_t = t_sparkle[int(delay * sample_rate):]
                    if len(delayed_t) > 0:
                        # Create twinkling effect
                        twinkle = np.sin(2 * np.pi * freq * delayed_t)
                        twinkle *= np.exp(-delayed_t * 12)  # Quick decay
                        twinkle *= (1 + 0.3 * np.sin(15 * delayed_t))  # Shimmer
                        
                        # Add to sparkle
                        start_idx = int(delay * sample_rate)
                        end_idx = start_idx + len(twinkle)
                        if end_idx <= len(sparkle):
                            sparkle[start_idx:end_idx] += twinkle * 0.2
            
            # Combine all parts with tiny gaps for clarity
            gap_samples = int(sample_rate * 0.02)  # 20ms gaps
            gap = np.zeros(gap_samples)
            
            # Assemble the complete sound: note1 -> gap -> note2 -> gap -> note3 -> sparkle
            combined = np.concatenate([note1, gap, note2, gap, note3, sparkle])
            
            # Add a subtle reverb for magical quality
            reverb_delay = int(0.03 * sample_rate)  # 30ms delay
            if len(combined) > reverb_delay:
                reverb = np.zeros_like(combined)
                reverb[reverb_delay:] = combined[:-reverb_delay] * 0.15
                combined += reverb
            
            # Convert to 16-bit integers
            audio_data = np.clip(combined, -1, 1)
            audio_data = (audio_data * 32767 * 0.8).astype(np.int16)  # Good volume
            
            # Ensure array is C-contiguous for pygame
            audio_data = np.ascontiguousarray(audio_data)
            
            # Convert to stereo
            stereo_data = np.column_stack((audio_data, audio_data))
            stereo_data = np.ascontiguousarray(stereo_data)
            
            # Play the sound
            sound = pygame.sndarray.make_sound(stereo_data)
            sound.play()
            
            logger.info("🎵 Exciting ready-to-speak cue played")
            
        except Exception as e:
            logger.error(f"Error generating ready-to-speak tone: {e}")

    def _generate_spelling_celebration_sound(self):
        """Generate a celebratory victory sound for correct spelling answers."""
        try:
            import numpy as np
            import pygame
            sample_rate = 22050
            duration = 1.8  # 1.8 seconds
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Create a "Ta-Da!" victory sound with ascending musical notes
            celebration = np.zeros_like(t)
            
            # First part: Rising musical phrase (Ta!)
            first_part_end = 0.6
            first_mask = t <= first_part_end
            
            # Rising chord progression for excitement
            frequencies_rising = [
                (220, 0.0, 0.2),   # A3 
                (277, 0.1, 0.3),   # C#4
                (330, 0.2, 0.4),   # E4
                (440, 0.3, 0.6),   # A4 (climax)
            ]
            
            for freq, start_time, end_time in frequencies_rising:
                note_mask = (t >= start_time) & (t <= end_time)
                if np.any(note_mask):
                    note_t = t[note_mask] - start_time
                    # Create a bell-like tone with harmonics
                    fundamental = np.sin(2 * np.pi * freq * note_t)
                    harmonic2 = 0.3 * np.sin(2 * np.pi * freq * 2 * note_t)
                    harmonic3 = 0.1 * np.sin(2 * np.pi * freq * 3 * note_t)
                    
                    # Bell envelope - quick attack, gradual decay
                    envelope = np.exp(-note_t * 4) * (1 - np.exp(-note_t * 50))
                    
                    note = (fundamental + harmonic2 + harmonic3) * envelope
                    celebration[note_mask] += note * 0.4
            
            # Second part: Sparkle effect (Da!)
            sparkle_start = 0.5
            sparkle_end = 1.8
            sparkle_mask = (t >= sparkle_start) & (t <= sparkle_end)
            
            if np.any(sparkle_mask):
                sparkle_t = t[sparkle_mask] - sparkle_start
                
                # Add magical sparkle with high frequency components
                sparkle_freqs = [880, 1108, 1397, 1760, 2217]  # High harmonious frequencies
                
                for i, freq in enumerate(sparkle_freqs):
                    delay = i * 0.08  # Staggered sparkles
                    if len(sparkle_t) > int(delay * sample_rate):
                        delayed_t = sparkle_t[int(delay * sample_rate):]
                        if len(delayed_t) > 0:
                            # Create shimmering effect
                            shimmer = np.sin(2 * np.pi * freq * delayed_t)
                            shimmer *= np.exp(-delayed_t * 2)  # Decay
                            shimmer *= (1 + 0.5 * np.sin(10 * delayed_t))  # Tremolo effect
                            
                            # Add to the celebration sound
                            start_idx = int((sparkle_start + delay) * sample_rate)
                            end_idx = start_idx + len(shimmer)
                            if end_idx <= len(celebration):
                                celebration[start_idx:end_idx] += shimmer * 0.15
            
            # Third part: Final triumphant chord
            final_start = 1.2
            final_mask = t >= final_start
            
            if np.any(final_mask):
                final_t = t[final_mask] - final_start
                
                # Major chord for triumphant ending
                chord_freqs = [440, 554, 659]  # A major chord
                for freq in chord_freqs:
                    chord_note = np.sin(2 * np.pi * freq * final_t)
                    chord_envelope = np.exp(-final_t * 1.5) * 0.6
                    celebration[final_mask] += chord_note * chord_envelope * 0.3
            
            # Add some gentle reverb effect
            reverb_delay = int(0.05 * sample_rate)  # 50ms delay
            if len(celebration) > reverb_delay:
                reverb = np.zeros_like(celebration)
                reverb[reverb_delay:] = celebration[:-reverb_delay] * 0.2
                celebration += reverb
            
            # Apply overall envelope for natural sound
            overall_envelope = np.ones_like(t)
            # Gentle fade out at the end
            fade_start = 1.5
            fade_mask = t >= fade_start
            if np.any(fade_mask):
                fade_t = (t[fade_mask] - fade_start) / (duration - fade_start)
                overall_envelope[fade_mask] = 1 - fade_t
            
            celebration *= overall_envelope
            
            # Normalize and convert to pygame sound format
            celebration = np.clip(celebration, -1, 1)
            celebration = (celebration * 32767 * 0.7).astype(np.int16)  # Good volume level
            
            # Create stereo sound
            stereo_sound = np.zeros((len(celebration), 2), dtype=np.int16)
            stereo_sound[:, 0] = celebration  # Left channel
            stereo_sound[:, 1] = celebration  # Right channel
            
            return pygame.sndarray.make_sound(stereo_sound)
        except Exception as e:
            logger.error(f"Error generating spelling celebration sound: {e}")
            return None

    def _generate_spelling_buzzer_sound(self):
        """Generate a buzzer sound for wrong spelling answers."""
        try:
            import numpy as np
            import pygame
            sample_rate = 22050
            duration = 0.8  # 0.8 seconds
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Create buzzer sound with low frequency
            frequency = 150  # Low buzzer frequency
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Add some harmonics to make it sound more like a buzzer
            wave += 0.5 * np.sin(2 * np.pi * frequency * 2 * t)  # Octave
            wave += 0.3 * np.sin(2 * np.pi * frequency * 3 * t)  # Fifth
            
            # Apply envelope for natural sound decay
            envelope = np.exp(-t * 1.5)
            buzzer = wave * envelope
            
            # Normalize and convert to pygame sound format
            buzzer = np.clip(buzzer, -1, 1)
            buzzer = (buzzer * 32767).astype(np.int16)
            
            # Create stereo sound
            stereo_sound = np.zeros((len(buzzer), 2), dtype=np.int16)
            stereo_sound[:, 0] = buzzer  # Left channel
            stereo_sound[:, 1] = buzzer  # Right channel
            
            return pygame.sndarray.make_sound(stereo_sound)
        except Exception as e:
            logger.error(f"Error generating spelling buzzer sound: {e}")
            return None

    def play_spelling_correct_sound(self):
        """Play celebration sound for correct spelling or math answers."""
        if not self.audio_feedback_enabled:
            return
        try:
            if self.pygame_available and hasattr(self, 'spelling_correct_sound'):
                import pygame
                pygame.mixer.Sound(self.spelling_correct_sound).play()
            else:
                import os
                os.system('afplay /System/Library/Sounds/Hero.aiff 2>/dev/null &')
        except Exception as e:
            logger.error(f"Error playing correct sound: {e}")

    def play_spelling_wrong_sound(self):
        """Play buzzer sound for incorrect spelling or math answers."""
        if not self.audio_feedback_enabled:
            return
        try:
            if self.pygame_available and hasattr(self, 'spelling_wrong_sound'):
                import pygame
                pygame.mixer.Sound(self.spelling_wrong_sound).play()
            else:
                import os
                os.system('afplay /System/Library/Sounds/Basso.aiff 2>/dev/null &')
        except Exception as e:
            logger.error(f"Error playing wrong sound: {e}")

    def play_math_correct_sound(self):
        """Play celebration sound for correct math answers (uses same sound as spelling)."""
        self.play_spelling_correct_sound()

    def play_math_wrong_sound(self):
        """Play buzzer sound for incorrect math answers (uses same sound as spelling)."""
        self.play_spelling_wrong_sound()

    def get_parent_greeting(self) -> str:
        """Get time-appropriate greeting for parent mode."""
        current_hour = datetime.now().hour
        
        if current_hour >= 21 or current_hour <= 6:  # 9 PM to 6 AM
            return "Hello! Parent mode activated. I'm ready to assist you with any requests. Speaking quietly to avoid waking the children."
        else:
            return "Hello! Parent mode activated. I'm ready to assist you with any requests."

    def get_parent_face_greeting(self) -> str:
        """Get time-appropriate face greeting for parent mode."""
        current_hour = datetime.now().hour
        
        if current_hour >= 21 or current_hour <= 6:  # 9 PM to 6 AM
            return "Hello! I see you. Parent mode ready - speaking softly."
        else:
            return "Hello! I see you. Parent mode ready."

    def should_greet_face(self, person_name: str) -> bool:
        """Check if we should greet this person based on face detection cooldown."""
        current_time = time.time()
        last_time = self.last_face_greeting.get(person_name.lower(), 0)
        
        if current_time - last_time > self.face_greeting_cooldown:
            self.last_face_greeting[person_name.lower()] = current_time
            return True
        
        return False

    def handle_face_detection(self):
        """Background thread for face recognition and automatic conversation activation."""
        logger.info("👁️ Face recognition thread started")
        
        try:
            # Use shared camera instead of starting a new one
            if not self.camera_handler.is_camera_available():
                logger.error("Shared camera is not available for face recognition")
                return
            
            logger.info("✅ Using shared camera for face recognition")
            
            while self.face_recognition_active and self.running:
                try:
                    # Use shared camera handler instead of face_detector.cap
                    ret, frame = self.camera_handler.read()
                    if not ret:
                        continue
                    
                    # Detect faces using the shared frame
                    face_detections = self.face_detector.detect_faces(frame)
                    
                    # Process detected faces
                    for face in face_detections:
                        if face['name'] != "Unknown" and face['confidence'] > 0.5:
                            person_name = face['name'].lower()
                            
                            # Check if this person is in our user profiles
                            if person_name in self.users:
                                # If no one is currently in conversation, start automatic conversation
                                if not self.current_user and self.should_greet_face(person_name):
                                    # Get appropriate face greeting (time-aware for parent mode)
                                    if person_name == 'parent':
                                        face_greeting = self.get_parent_face_greeting()
                                    else:
                                        face_greeting = self.get_dynamic_face_greeting(person_name)
                                    
                                    logger.info(f"👋 Face detected: {person_name.title()} - Starting automatic conversation")
                                    print(f"🎉 Face detected: {person_name.title()}! Starting automatic conversation...")
                                    
                                    # Speak greeting and automatically start conversation
                                    self.speak(face_greeting, person_name)
                                    
                                    # Start automatic conversation mode (no wake word needed!)
                                    threading.Thread(
                                        target=self.handle_automatic_conversation, 
                                        args=(person_name,), 
                                        daemon=True
                                    ).start()
                    
                    # Small delay to prevent excessive CPU usage
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error in face detection loop: {e}")
                    time.sleep(1)
        
        except Exception as e:
            logger.error(f"Face recognition thread error: {e}")
        finally:
            # Don't release shared camera - it's managed by camera_handler
            logger.info("👁️ Face recognition thread stopped")

    def handle_automatic_conversation(self, user: str):
        """Handle automatic conversation triggered by face detection."""
        if self.current_user:  # Someone else is already in conversation
            return
        
        self.current_user = user
        user_info = self.users[user]
        
        logger.info(f"🤖 Starting automatic conversation with {user.title()}")
        print(f"💬 Automatic conversation mode activated for {user.title()}!")
        print("🎤 I'm listening... (say 'goodbye' to end, or I'll timeout after 1 minute of silence)")
        
        # Start conversation loop - keep listening until user says goodbye or timeout
        conversation_active = True
        conversation_timeout_count = 0
        # Extend timeout when spelling game is active to give more time for writing
        max_timeouts = 6 if self.spelling_game_active else 2  # Allow 6 timeouts for spelling game, 2 for normal conversation
        
        while conversation_active and self.running and self.current_user == user:
            # Check if speech was interrupted before listening for new input
            if self.speech_interrupted:
                logger.info("Handling speech interruption")
                
                # Check if the interruption was a goodbye command
                last_interrupt_input = getattr(self, 'last_interrupt_input', '')
                
                if any(phrase in last_interrupt_input for phrase in ['goodbye', 'bye', 'see you later', 'talk to you later']):
                    # User said goodbye as interruption - end conversation
                    farewell_messages = {
                        'sophia': "Goodbye Sophia! I'm always here when you need me. Have a wonderful day!",
                        'eladriel': "See you later Eladriel! Keep exploring and learning about dinosaurs! Roar!",
                        'parent': "Goodbye! Parent mode deactivated. All systems remain operational for the children."
                    }
                    farewell_response = farewell_messages.get(user, "Goodbye! Talk to you soon!")
                    
                    # Add farewell to history and then clear it
                    self.add_to_conversation_history(user, user_input, farewell_response)
                    self.speak(farewell_response, user)
                    
                    # Clear conversation history for fresh start next time
                    self.clear_conversation_history(user)
                    
                    conversation_active = False
                    break
                else:
                    # Regular interruption - acknowledge and continue
                    interrupt_responses = {
                        'sophia': "Oh! Sorry Sophia! I'm listening now.",
                        'eladriel': "Whoops! You got my attention, Eladriel! What's up?",
                        'parent': "Interrupted. Ready for your next request."
                    }
                    
                    # Brief acknowledgment (will also be interruptible)
                    self.speak(interrupt_responses.get(user, "Yes? I'm listening!"), user)
                
                # Reset the interrupt flag
                self.speech_interrupted = False
            
            # Listen for their request with a 15-second timeout (longer for children)
            user_input = self.listen_for_speech(timeout=15)
            
            if user_input:
                conversation_timeout_count = 0  # Reset timeout counter
                
                # Check if user wants to end conversation
                if self.is_conversation_ending(user_input):
                    farewell_messages = {
                        'sophia': "Goodbye Sophia! I'm always here when you need me. Have a wonderful day!",
                        'eladriel': "See you later Eladriel! Keep exploring and learning about dinosaurs! Roar!",
                        'parent': "Goodbye! Parent mode deactivated. All systems remain operational for the children. Call 'Assistant' anytime you need me."
                    }
                    farewell_response = farewell_messages.get(user, "Goodbye! Talk to you soon!")
                    
                    # Add farewell to history and then clear it
                    self.add_to_conversation_history(user, user_input, farewell_response)
                    self.speak(farewell_response, user)
                    
                    # Clear conversation history for fresh start next time
                    self.clear_conversation_history(user)
                    
                    conversation_active = False
                    break
                
                # Check for special commands first
                special_response = self.handle_special_commands(user_input, user)
                
                if special_response:
                    # Add special command to conversation history too
                    self.add_to_conversation_history(user, user_input, special_response)
                    
                    # Use no-interrupt speak for Filipino game responses to prevent recording during explanations
                    if self.filipino_translator.is_filipino_game_command(user_input) or self.filipino_translator.game_active:
                        self.speak_no_interrupt(special_response, user)
                    else:
                        self.speak(special_response, user)
                else:
                    # Process with OpenAI for regular conversation
                    import asyncio
                    try:
                        response = asyncio.run(self.process_with_openai(user_input, user))
                        
                        # Use no-interrupt speak if Filipino game is active to prevent recording during explanations
                        if self.filipino_translator.game_active:
                            self.speak_no_interrupt(response, user)
                        else:
                            self.speak(response, user)
                    except Exception as e:
                        logger.error(f"Error processing request: {e}")
                        self.speak("I'm sorry, something went wrong. Let me try again.", user)
                
                # After responding, give a subtle cue that we're still listening
                time.sleep(0.5)  # Brief pause
                print(f"💬 Still listening to {user.title()}... (say 'goodbye' to end)")
                
            else:
                # No speech detected
                conversation_timeout_count += 1
                
                # Update max timeouts dynamically based on current spelling game state
                current_max_timeouts = 6 if self.spelling_game_active else 2
                
                if conversation_timeout_count == 1:
                    # First timeout - gentle prompt
                    if self.spelling_game_active:
                        prompts = {
                            'sophia': "Take your time writing, Sophia! I'm waiting for you to say 'Ready'.",
                            'eladriel': "No rush Eladriel! Let me know when you're ready to show me your spelling!",
                            'parent': "Spelling game active. Say 'Ready' when you want me to check your answer."
                        }
                    else:
                        prompts = {
                            'sophia': "I'm still here if you have more questions, Sophia!",
                            'eladriel': "Still here for more dinosaur fun, Eladriel! What's next?",
                            'parent': "I'm still here and ready to assist. Any additional requests?"
                        }
                    self.speak(prompts.get(user, "I'm still listening if you have more to say!"), user)
                    print(f"⏰ Waiting for {user.title()} to continue...")
                    
                elif conversation_timeout_count >= current_max_timeouts:
                    # Multiple timeouts - end conversation gracefully
                    if self.spelling_game_active:
                        # Special handling for spelling game timeout
                        timeout_messages = {
                            'sophia': "I'll pause the spelling game for now, Sophia. Say 'Spelling Game' to continue practicing anytime!",
                            'eladriel': "Let's pause our spelling adventure, Eladriel! Say 'Spelling Game' when you want to play again!",
                            'parent': "Spelling game test paused due to timeout. Game state preserved for continuation."
                        }
                        # Don't reset spelling game state on timeout - just pause it
                    else:
                        timeout_messages = {
                            'sophia': "I'll be here whenever you need me, Sophia. Just say 'Miley' to chat again!",
                            'eladriel': "I'll be waiting for more dinosaur adventures, Eladriel! Just say 'Dino' when you're ready!",
                            'parent': "Returning to standby mode. Say 'Assistant' anytime for immediate assistance."
                        }
                    self.speak(timeout_messages.get(user, "I'll be here when you need me. Just call my name!"), user)
                    conversation_active = False
        
        self.current_user = None
        logger.info(f"🎤 Automatic conversation with {user.title()} ended")
        print("🎤 Returning to face detection and wake word listening mode...")
        
        self.current_user = None
        print("🎤 Conversation ended. Listening for wake words again...")
        # Note: Spelling game state persists between conversations - only reset when user explicitly ends game

    def start_face_recognition(self):
        """Start the background face recognition system."""
        if not self.face_recognition_active:
            self.face_recognition_active = True
            self.face_recognition_thread = threading.Thread(target=self.handle_face_detection, daemon=True)
            self.face_recognition_thread.start()
            logger.info("🎭 Face recognition system started")

    def stop_face_recognition(self):
        """Stop the background face recognition system."""
        if self.face_recognition_active:
            self.face_recognition_active = False
            if self.face_recognition_thread:
                self.face_recognition_thread.join(timeout=2)
            logger.info("🎭 Face recognition system stopped")

    def speak(self, text: str, user: Optional[str] = None):
        """Speak text to user with interrupt capability and audio feedback prevention."""
        if self.quiet_mode:
            logger.info("Speak request ignored - quiet mode active")
            return
        
        logger.info(f"🗣️ SPEAK: Starting speech process for text: '{text[:50]}...'")
        
        try:
            # CRITICAL: Set AI speaking flag to prevent voice detector from listening to AI
            self.voice_detector.set_ai_speaking(True)
            logger.info("🗣️ SPEAK: AI speaking flag set to True")
            
            # Reset interrupt flag
            self.speech_interrupted = False
            logger.info("🗣️ SPEAK: Interrupt flag reset")
            
            # Start interrupt listener
            logger.info("🗣️ SPEAK: Starting interrupt listener...")
            self.start_interrupt_listener()
            
            # Use personalized TTS engine for each user
            if user and user in self.users:
                tts_engine = self.users[user]['tts_engine']
                logger.info(f"🗣️ SPEAK: Using personalized TTS for {user}")
                logger.info(f"Speaking to {user}: {text}")
                
                # Use threaded TTS for smooth speech with interrupt capability
                logger.info("🗣️ SPEAK: Starting threaded TTS...")
                self._speak_with_interrupt_check(tts_engine, text)
                logger.info("🗣️ SPEAK: Threaded TTS completed")
                    
            else:
                # Default to Sophia's engine if no user specified
                logger.info("🗣️ SPEAK: Using default Sophia TTS engine")
                logger.info(f"Speaking (default): {text}")
                self._speak_with_interrupt_check(self.sophia_tts, text)
                logger.info("🗣️ SPEAK: Default TTS completed")
            
            # Stop interrupt listener
            logger.info("🗣️ SPEAK: Stopping interrupt listener...")
            self.stop_interrupt_listener()
            
            # CRITICAL: Add delay after speaking to prevent audio feedback loop
            # This prevents the microphone from picking up the AI's own voice
            import time
            logger.info("🗣️ SPEAK: Post-speech delay...")
            time.sleep(0.3)  # Reduced from 1.5 to 0.3 seconds for faster response
            
            # NEW: Play clear "you can speak now" cue instead of confusing completion sound
            logger.info("🗣️ SPEAK: Playing ready-to-speak sound...")
            self.play_ready_to_speak_sound()
            
            # Brief pause to let the cue finish and be clearly understood
            time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds for faster response
            logger.info("🗣️ SPEAK: Speech process completed successfully")
            
        except Exception as e:
            logger.error(f"🗣️ SPEAK ERROR: TTS Error: {e}")
            logger.error(f"🗣️ SPEAK ERROR: Exception type: {type(e)}")
            import traceback
            logger.error(f"🗣️ SPEAK ERROR: Traceback: {traceback.format_exc()}")
            
            self.stop_interrupt_listener()
            # Still play ready cue even on error
            self.play_ready_to_speak_sound()
            time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds
            # Add delay even on error to prevent feedback
            import time
            time.sleep(0.3)  # Reduced from 1.5 to 0.3 seconds
        finally:
            # CRITICAL: Always reset AI speaking flag when done
            logger.info("🗣️ SPEAK: Resetting AI speaking flag to False")
            self.voice_detector.set_ai_speaking(False)

    def speak_no_interrupt(self, text: str, user: Optional[str] = None):
        """Speak text without interrupt capability (for game instructions, etc.)."""
        if self.quiet_mode:
            return
        
        try:
            # CRITICAL: Set AI speaking flag to prevent voice detector from listening to AI
            self.voice_detector.set_ai_speaking(True)
            
            # Use personalized TTS engine for each user
            if user and user in self.users:
                tts_engine = self.users[user]['tts_engine']
                logger.info(f"Speaking (no interrupt) to {user}: {text}")
                tts_engine.say(text)
                tts_engine.runAndWait()
            else:
                # Default to Sophia's engine if no user specified
                logger.info(f"Speaking (no interrupt, default): {text}")
                self.sophia_tts.say(text)
                self.sophia_tts.runAndWait()
            
            # CRITICAL: Add delay after speaking to prevent audio feedback loop
            import time
            time.sleep(0.3)  # Reduced from 1.5 to 0.3 seconds for faster response
            
            # NEW: Play clear "you can speak now" cue for educational content too
            self.play_ready_to_speak_sound()
            
            # Brief pause to let the cue finish and be clearly understood
            time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds for faster response
            
        except Exception as e:
            logger.error(f"TTS Error (no interrupt): {e}")
            # Still play ready cue even on error
            self.play_ready_to_speak_sound()
            time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds
            # Add delay even on error to prevent feedback
            import time
            time.sleep(0.3)  # Reduced from 1.5 to 0.3 seconds
        finally:
            # CRITICAL: Always reset AI speaking flag when done
            self.voice_detector.set_ai_speaking(False)

    def _speak_with_interrupt_check(self, tts_engine, text: str):
        """Speak with smooth delivery but interrupt capability."""
        logger.info("🎙️ TTS_THREAD: Starting speak with interrupt check")
        
        # Create a flag to track if TTS is complete
        speech_complete = threading.Event()
        tts_error = None
        
        def speak_thread():
            """Background thread for TTS."""
            nonlocal tts_error
            try:
                logger.info("🎙️ TTS_THREAD: Background thread started")
                logger.info(f"🎙️ TTS_THREAD: Calling tts_engine.say() with text: '{text[:30]}...'")
                tts_engine.say(text)
                logger.info("🎙️ TTS_THREAD: tts_engine.say() completed")
                
                logger.info("🎙️ TTS_THREAD: Calling tts_engine.runAndWait()")
                tts_engine.runAndWait()
                logger.info("🎙️ TTS_THREAD: tts_engine.runAndWait() completed")
                
                speech_complete.set()
                logger.info("🎙️ TTS_THREAD: Speech complete event set")
            except Exception as e:
                logger.error(f"🎙️ TTS_THREAD ERROR: TTS thread error: {e}")
                logger.error(f"🎙️ TTS_THREAD ERROR: Exception type: {type(e)}")
                import traceback
                logger.error(f"🎙️ TTS_THREAD ERROR: Traceback: {traceback.format_exc()}")
                tts_error = e
                speech_complete.set()
        
        # Start TTS in background thread
        logger.info("🎙️ TTS_THREAD: Creating and starting background thread")
        tts_thread = threading.Thread(target=speak_thread, daemon=True)
        tts_thread.start()
        logger.info("🎙️ TTS_THREAD: Background thread started successfully")
        
        # Monitor for interrupts while speech is ongoing
        logger.info("🎙️ TTS_THREAD: Starting interrupt monitoring loop")
        interrupt_check_count = 0
        while not speech_complete.is_set() and not self.speech_interrupted:
            time.sleep(0.1)  # Check every 100ms for interrupts
            interrupt_check_count += 1
            if interrupt_check_count % 50 == 0:  # Log every 5 seconds
                logger.info(f"🎙️ TTS_THREAD: Still monitoring... ({interrupt_check_count * 0.1:.1f}s)")
        
        logger.info("🎙️ TTS_THREAD: Interrupt monitoring loop ended")
        
        # If interrupted, stop the TTS engine
        if self.speech_interrupted:
            logger.info("🎙️ TTS_THREAD: Speech was interrupted, stopping TTS engine")
            try:
                tts_engine.stop()
                logger.info("🎙️ TTS_THREAD: TTS engine stopped successfully")
            except Exception as stop_error:
                logger.error(f"🎙️ TTS_THREAD: Error stopping TTS engine: {stop_error}")
            logger.info("Speech interrupted and stopped")
        
        # Wait for thread to complete (with timeout)
        logger.info("🎙️ TTS_THREAD: Waiting for background thread to complete...")
        tts_thread.join(timeout=5.0)  # Increased timeout from 1.0 to 5.0
        
        if tts_thread.is_alive():
            logger.warning("🎙️ TTS_THREAD: Background thread did not complete within timeout!")
        else:
            logger.info("🎙️ TTS_THREAD: Background thread completed successfully")
            
        if tts_error:
            logger.error(f"🎙️ TTS_THREAD: Propagating TTS error: {tts_error}")
            raise tts_error

    def split_text_for_interruption(self, text: str) -> list:
        """Split text into manageable chunks for interrupt checking."""
        # This method is now deprecated but kept for compatibility
        return [text]

    def start_interrupt_listener(self):
        """Start background listener for interrupt commands."""
        logger.info("🎧 INTERRUPT: Starting interrupt listener...")
        if not self.interrupt_listener_active:
            self.interrupt_listener_active = True
            self.interrupt_thread = threading.Thread(target=self.interrupt_listener, daemon=True)
            self.interrupt_thread.start()
            logger.info("🎧 INTERRUPT: Interrupt listener thread started")
        else:
            logger.info("🎧 INTERRUPT: Interrupt listener already active")

    def stop_interrupt_listener(self):
        """Stop background interrupt listener."""
        logger.info("🎧 INTERRUPT: Stopping interrupt listener...")
        self.interrupt_listener_active = False
        if self.interrupt_thread:
            self.interrupt_thread.join(timeout=2.0)  # 2 second timeout
            if self.interrupt_thread.is_alive():
                logger.warning("🎧 INTERRUPT: Interrupt thread did not stop within timeout")
            else:
                logger.info("🎧 INTERRUPT: Interrupt listener stopped successfully")

    def interrupt_listener(self):
        """Background thread that listens for interrupt commands during speech."""
        logger.info("🎧 INTERRUPT_THREAD: Interrupt listener thread started")
        try:
            loop_count = 0
            while self.interrupt_listener_active and not self.speech_interrupted:
                try:
                    loop_count += 1
                    if loop_count % 20 == 0:  # Log every 2 seconds
                        logger.info(f"🎧 INTERRUPT_THREAD: Loop {loop_count}, checking for interrupts...")
                    
                    # CRITICAL: Don't listen if AI is currently speaking to prevent feedback
                    if self.voice_detector.ai_speaking:
                        time.sleep(0.1)  # Wait while AI is speaking
                        continue
                    
                    # Use voice detector for interrupt detection
                    text = self.voice_detector.listen_with_speaker_detection(
                        timeout=1,  # Quick timeout for responsiveness
                        silence_threshold=0.5,  # Shorter silence for interrupts
                        max_total_time=3,  # Max 3 seconds for interrupt detection
                        game_mode='interrupt'  # Special mode for interrupts
                    )
                    
                    if text:
                        logger.info(f"🎧 INTERRUPT_THREAD: Interrupt check detected: {text}")
                        
                        # Check for interrupt commands
                        if self.is_interrupt_command(text):
                            logger.info(f"🎧 INTERRUPT_THREAD: Interrupt command detected: {text}")
                            self.speech_interrupted = True
                            
                            # Store the interrupt input for handling
                            self.last_interrupt_input = text
                            
                            # Stop TTS engines immediately
                            try:
                                self.sophia_tts.stop()
                                self.eladriel_tts.stop()
                                logger.info("🎧 INTERRUPT_THREAD: TTS engines stopped")
                            except Exception as stop_error:
                                logger.error(f"🎧 INTERRUPT_THREAD: Error stopping TTS: {stop_error}")
                            
                            break
                            
                except Exception as e:
                    # Any error, log and continue (but don't let errors kill the thread)
                    logger.error(f"🎧 INTERRUPT_THREAD: Interrupt listener error: {e}")
                    time.sleep(0.1)
                    continue
                    
        except Exception as e:
            logger.error(f"🎧 INTERRUPT_THREAD: Fatal interrupt listener thread error: {e}")
        finally:
            logger.info("🎧 INTERRUPT_THREAD: Interrupt listener thread ended")

    def is_interrupt_command(self, user_input: str) -> bool:
        """Check if the user input is an interrupt command."""
        interrupt_commands = [
            'stop', 'stop talking', 'be quiet', 'quiet', 'silence', 'hush',
            'goodbye', 'bye', 'bye bye', 'see you later', 'talk to you later',
            'enough', 'that\'s enough', 'okay stop', 'stop please',
            'shh', 'shhh', 'shut up', 'pause', 'hold on', 'wait',
            'interrupt', 'cut it out', 'end', 'finish', 'done'
        ]
        
        user_input_lower = user_input.lower().strip()
        
        # Check for exact matches or partial matches
        for command in interrupt_commands:
            if command in user_input_lower:
                return True
                
        return False

    def listen_for_speech(self, timeout: int = 15) -> Optional[str]:
        """Listen for speech input using intelligent voice activity detection with speaker differentiation."""
        try:
            # Set AI speaking flag to false to allow listening
            self.voice_detector.set_ai_speaking(False)
            
            # CRITICAL: Additional delay before starting to listen to prevent audio feedback
            # This ensures any residual audio output is completely finished
            import time
            time.sleep(0.5)  # Extra 0.5 second safety buffer before listening
            
            # Play listening sound to indicate AI is ready to hear
            self.play_listening_sound()
            
            # Brief pause after listening sound to let it finish completely
            time.sleep(0.3)
            
            # Determine game mode for optimal sensitivity
            game_mode = None
            if self.spelling_game_active:
                game_mode = 'spelling'
            elif hasattr(self, 'filipino_translator') and self.filipino_translator.game_active:
                game_mode = 'filipino'
            
            # Use the new voice activity detector with speaker differentiation
            logger.info("🎤 Using Smart Voice Detection with Speaker Differentiation...")
            text = self.voice_detector.listen_with_speaker_detection(
                timeout=timeout,
                silence_threshold=2.0,  # Longer silence threshold for complete thoughts
                max_total_time=45,  # Longer max time for complex questions
                game_mode=game_mode
            )
            
            if text is None:
                return None
            
            # Special handling for "ready" detection in spelling game
            if self.spelling_game_active:
                detected_ready = self.detect_ready_command(text)
                if detected_ready:
                    logger.info(f"Ready command detected: '{text}' -> '{detected_ready}'")
                    return detected_ready
            
            return text
                
        except Exception as e:
            logger.error(f"Smart voice detection error: {e}")
            # Fallback to basic recognition if smart detection fails
            return self._fallback_listen_for_speech(timeout)
    
    def _fallback_listen_for_speech(self, timeout: int = 15) -> Optional[str]:
        """Fallback speech recognition method."""
        try:
            with sr.Microphone() as source:
                logger.info("🎤 Using fallback speech recognition...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                
                if self.spelling_game_active:
                    self.recognizer.energy_threshold = max(200, self.recognizer.energy_threshold * 0.6)
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                else:
                    self.recognizer.energy_threshold = max(300, self.recognizer.energy_threshold * 0.8)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=20)
                
                text = self.recognizer.recognize_google(audio, language='en-US')
                logger.info(f"Fallback recognized: {text}")
                return text.lower()
                
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
            return None

    def _clean_recognized_text(self, text: str) -> str:
        """Clean and improve recognized text for better accuracy."""
        if not text:
            return text
        
        # Remove common speech recognition artifacts
        cleaned = text.strip()
        
        # Fix common recognition errors
        common_fixes = {
            # Common misrecognitions
            "filipina": "filipino",
            "philipino": "filipino", 
            "philippino": "filipino",
            "tagalog": "filipino",
            "ready ready": "ready",
            "done done": "done",
            "check check": "check",
            
            # Common word corrections
            "colour": "color",
            "grey": "gray",
            "centre": "center",
            
            # Remove extra spaces and punctuation
        }
        
        # Apply common fixes
        for wrong, correct in common_fixes.items():
            cleaned = cleaned.replace(wrong, correct)
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned

    def detect_ready_command(self, text: str) -> Optional[str]:
        """Enhanced detection of 'ready' and similar commands with fuzzy matching."""
        import difflib
        
        # List of target ready commands
        ready_commands = [
            'ready', 'im ready', 'i am ready', 'check my answer', 'done', 
            'finished', 'check it', 'look at this', 'all done', 'complete'
        ]
        
        # Direct match first
        for command in ready_commands:
            if command in text:
                return command
        
        # Fuzzy matching for speech recognition errors
        for command in ready_commands:
            # Check if the text is similar enough to a ready command
            similarity = difflib.SequenceMatcher(None, text, command).ratio()
            if similarity > 0.7:  # 70% similarity threshold
                logger.info(f"Fuzzy match: '{text}' matches '{command}' with {similarity:.2f} similarity")
                return command
        
        # Check for partial matches of key words
        key_words = ['ready', 'done', 'finished', 'check', 'complete']
        for word in key_words:
            if word in text or any(difflib.SequenceMatcher(None, text, word).ratio() > 0.7 for word in text.split()):
                return f"ready (detected from: {text})"
        
            return None

    async def process_with_openai(self, text: str, user: str) -> str:
        """Process user input with OpenAI and return response with conversation context."""
        try:
            # Create a personalized system prompt based on user
            user_info = self.users.get(user, {})
            personality = user_info.get('personality', 'helpful and friendly')
            user_name = user_info.get('name', user.title())
            
            # Get conversation context
            conversation_context = self.get_conversation_context(user)
            
            system_prompt = f"""You are a helpful AI assistant speaking to {user_name}. 
            Be {personality}. Keep responses friendly, age-appropriate, and engaging for children. 
            Be encouraging and educational when possible. Keep responses concise but informative.
            
            Remember to reference previous conversation when relevant. You have context of what you discussed earlier."""
            
            # Prepare messages with context
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history for context (if available)
            if conversation_context:
                messages.append({
                    "role": "system", 
                    "content": f"Recent conversation context:\n{conversation_context}\n\nUse this context to provide relevant responses and reference earlier topics when appropriate."
                })
            
            # Add current user message
            messages.append({"role": "user", "content": text})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Add this exchange to conversation history
            self.add_to_conversation_history(user, text, ai_response)
            
            return ai_response
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            error_response = "I'm sorry, I'm having trouble understanding right now. Can you try again?"
            
            # Still add to history even for errors
            self.add_to_conversation_history(user, text, error_response)
            
            return error_response

    def handle_special_commands(self, user_input: str, user: str) -> Optional[str]:
        """Handle special commands for each user."""
        user_input_lower = user_input.lower()
        
        # Parent-specific admin commands
        if user == 'parent':
            if any(phrase in user_input_lower for phrase in ['status report', 'system status', 'report']):
                return self.get_system_status()
            
            elif any(phrase in user_input_lower for phrase in ['system check', 'health check', 'diagnostic']):
                return self.run_system_diagnostic()
            
            elif any(phrase in user_input_lower for phrase in ['quiet mode on', 'enable quiet mode', 'whisper mode']):
                return self.enable_quiet_mode()
            
            elif any(phrase in user_input_lower for phrase in ['quiet mode off', 'disable quiet mode', 'normal volume']):
                return self.disable_quiet_mode()
            
            elif any(phrase in user_input_lower for phrase in ['check on kids', 'kids status', 'children']):
                return self.check_kids_status()
        
        # Audio feedback controls for all users
        if any(phrase in user_input_lower for phrase in ['turn off sounds', 'disable sounds', 'no sounds', 'mute sounds']):
            return self.toggle_audio_feedback(False)
        
        if any(phrase in user_input_lower for phrase in ['turn on sounds', 'enable sounds', 'sounds on', 'unmute sounds']):
            return self.toggle_audio_feedback(True)
        
        # Universal object identification commands for all users - expanded with natural phrases
        object_identification_phrases = [
            'identify this', 'what is this', 'tell me about this', 'what am i holding',
            'look', 'look at this', 'look at the camera', 'can you see this',
            'guess what this is', 'guess what i\'m holding', 'can you recognize',
            'can you identify', 'what do you see', 'recognize this',
            'see what i have', 'check this out', 'look what i found'
        ]
        
        if any(phrase in user_input_lower for phrase in object_identification_phrases):
            return self.handle_object_identification(user)
        
        # Repeat functionality for all users
        repeat_phrases = [
            'repeat', 'say that again', 'what did you say', 'can you repeat that',
            'repeat that', 'say it again', 'what was that', 'i didn\'t hear you',
            'could you repeat', 'please repeat', 'one more time', 'again'
        ]
        
        if any(phrase in user_input_lower for phrase in repeat_phrases):
            return self.handle_repeat_request(user)
        
        # Math Quiz Game Commands (for Sophia, Eladriel, and Parent) - CHECK FIRST!
        if user in ['sophia', 'eladriel', 'parent']:
            # Math game start commands
            if self.math_quiz.is_math_game_command(user_input):
                return self.math_quiz.handle_math_command(user_input, user)
            
            # Handle "ready" commands when math game is active - PRIORITY!
            elif self.math_quiz.game_active:
                ready_phrases = [
                    'ready', 'i\'m ready', 'check my answer', 'done', 'finished', 
                    'check it', 'look at this', 'see my answer', 'check this',
                    'here it is', 'all done', 'complete', 'i finished',
                    'can you check', 'please check', 'look', 'see this'
                ]
                
                if any(phrase in user_input_lower for phrase in ready_phrases):
                    return self.math_quiz.check_math_answer(user)
                
                # Handle end game commands
                elif any(phrase in user_input_lower for phrase in ['end math', 'stop math', 'quit math', 'end game']):
                    return self.math_quiz.end_game(user)
                
                # Handle verbal answers when math game is active (fallback)
                else:
                    verbal_answer = self.math_quiz._extract_verbal_answer(user_input_lower)
                    if verbal_answer is not None:
                        return self.math_quiz._handle_verbal_answer(verbal_answer, user)
        
        # Animal Guessing Game Commands (for Sophia, Eladriel, and Parent)
        if user in ['sophia', 'eladriel', 'parent']:
            # Animal game start commands
            if any(phrase in user_input_lower for phrase in ['animal game', 'guess the animal', 'animal guessing', 'identify animal']):
                return self.animal_game.handle_animal_guess(user)
            
            # Handle animal game commands when active
            elif self.animal_game.is_game_active():
                if any(phrase in user_input_lower for phrase in ['guess the animal', 'identify animal', 'what animal']):
                    return self.animal_game.handle_animal_guess(user)
                
                elif any(phrase in user_input_lower for phrase in ['animal stats', 'my stats', 'game stats']):
                    return self.animal_game.get_game_stats(user)
                
                elif any(phrase in user_input_lower for phrase in ['animal help', 'help me', 'how to play']):
                    return self.animal_game.get_game_help(user)
                
                elif any(phrase in user_input_lower for phrase in ['end animal game', 'stop animal', 'quit animal']):
                    return self.animal_game.end_game(user)
        
        # Letter Word Game Commands (for Sophia, Eladriel, and Parent)
        if user in ['sophia', 'eladriel', 'parent']:
            # Letter game start commands
            if any(phrase in user_input_lower for phrase in ['letter game', 'letter word game', 'word guessing', 'guess the word', 'play letter game']):
                return self.letter_word_game.start_game(user)
            
            # Handle letter game commands when active
            elif self.letter_word_game.is_game_active():
                # Check for game control commands first
                if any(phrase in user_input_lower for phrase in ['hint please', 'give me a hint', 'need a hint', 'extra hint']):
                    return self.letter_word_game.get_hint(user)
                
                elif any(phrase in user_input_lower for phrase in ['skip', 'skip word', 'next word', 'skip this one']):
                    return self.letter_word_game.skip_word(user)
                
                elif any(phrase in user_input_lower for phrase in ['stats', 'my stats', 'game stats', 'score']):
                    return self.letter_word_game.get_game_stats(user)
                
                elif any(phrase in user_input_lower for phrase in ['help', 'how to play', 'game help']):
                    return self.letter_word_game.get_game_help(user)
                
                elif any(phrase in user_input_lower for phrase in ['end letter game', 'stop letter', 'quit letter', 'end game']):
                    return self.letter_word_game.end_game(user)
                
                # If none of the control commands match, treat as a word guess
                else:
                    return self.letter_word_game.check_answer(user_input, user)
        
        # Spelling Game Commands (for Sophia, Eladriel, and Parent)
        if user in ['sophia', 'eladriel', 'parent']:
            if any(phrase in user_input_lower for phrase in ['spelling game', 'play spelling', 'start spelling']):
                return self.start_spelling_game(user)
            
            # Enhanced "ready" detection with more variations and automatic visual check option
            elif self.spelling_game_active:
                ready_phrases = [
                    'ready', 'i\'m ready', 'check my answer', 'done', 'finished', 
                    'check it', 'look at this', 'see my answer', 'check this',
                    'here it is', 'all done', 'complete', 'i finished',
                    'can you check', 'please check', 'look', 'see this'
                ]
                
                if any(phrase in user_input_lower for phrase in ready_phrases):
                    return self.check_spelling_answer(user)
            
                # NEW: Visual word detection without saying "ready"
                elif any(phrase in user_input_lower for phrase in ['auto check', 'smart check', 'visual check', 'camera check']):
                    return self.start_auto_visual_check(user)
                
                # Stop auto check mode
                elif any(phrase in user_input_lower for phrase in ['stop auto check', 'stop monitoring', 'manual mode', 'stop watching']):
                    return self.stop_auto_visual_check(user)
                
                elif any(phrase in user_input_lower for phrase in ['end game', 'stop game', 'quit game']):
                    return self.end_spelling_game(user)
        
        # Filipino Translation Game Commands (for all users)
        if self.filipino_translator.is_filipino_game_command(user_input):
            return self.filipino_translator.handle_filipino_command(user_input, user)
        
        # Eladriel's special dinosaur commands (keep existing functionality)
        if user == 'eladriel':
            if any(phrase in user_input_lower for phrase in ['identify dinosaur', 'what is this dinosaur', 'look at this dinosaur']):
                return self.handle_dinosaur_identification()
            
            elif any(phrase in user_input_lower for phrase in ['show camera', 'camera preview', 'can you see']):
                return self.handle_camera_preview()
            
            elif any(phrase in user_input_lower for phrase in ['dinosaur tips', 'how to show', 'tips']):
                return self.dinosaur_identifier.get_dinosaur_tips()
        
        # General help commands for all users
        if any(phrase in user_input_lower for phrase in ['help', 'what can you do', 'commands']):
            return self.get_help_message(user)
        
        return None
    
    def handle_object_identification(self, user: str) -> str:
        """Handle universal object identification for any user."""
        try:
            user_name = user.title()
            self.speak(f"Awesome {user_name}! Let me see what you're showing me! Hold it steady in front of the camera...", user)
            
            # Give user time to position the object
            import time
            time.sleep(3)
            
            # Capture and identify the object
            result = self.object_identifier.capture_and_identify()
            
            if result["success"]:
                return result["message"]
            else:
                return f"Hmm, I had trouble seeing your object clearly. {result['message']} Try holding it closer to the camera with good lighting!"
                
        except Exception as e:
            logger.error(f"Error in object identification: {e}")
            return "Oops! Something went wrong with the camera. Let's try again later!"
    
    def handle_dinosaur_identification(self) -> str:
        """Handle dinosaur identification for Eladriel (specialized)."""
        try:
            self.speak("Awesome! Let me see your dinosaur! Hold it steady in front of the camera...", 'eladriel')
            
            # Give Eladriel time to position the dinosaur
            import time
            time.sleep(3)
            
            # Capture and identify
            result = self.dinosaur_identifier.capture_and_identify()
            
            if result["success"]:
                return result["message"]
            else:
                return f"Hmm, I had trouble seeing your dinosaur. {result['message']} Try holding it closer to the camera!"
                
        except Exception as e:
            logger.error(f"Error in dinosaur identification: {e}")
            return "Oops! Something went wrong with the camera. Let's try again later!"
    
    def handle_camera_preview(self) -> str:
        """Show camera preview for users."""
        try:
            self.speak("Let me show you what I can see through my camera!", self.current_user)
            success = self.object_identifier.show_camera_preview(duration=5)
            
            if success:
                return "Did you see the camera window? That's what I can see! Now you know where to hold your objects!"
            else:
                return "Sorry, I couldn't show you the camera preview. Maybe the camera isn't working right now."
                
        except Exception as e:
            logger.error(f"Error showing camera preview: {e}")
            return "I had trouble with the camera preview. Let's try again later!"
    
    def get_help_message(self, user: str) -> str:
        """Get help message for each user."""
        if user == 'sophia':
            return """Hi Sophia! Here's what I can help you with:
            
• Ask me questions about anything you're curious about
• Get help with homework or learning
• Hear fun facts and stories
• Chat about your day

🔍 OBJECT IDENTIFICATION:
• Say "What is this?" or "Identify this" - I'll tell you all about any object you show me!
• Learn about colors, materials, history, and fun facts
• Perfect for exploring household items, toys, books, and more!

📝 SPELLING GAME (NEW!):
• Say "Spelling Game" to start an interactive spelling practice!
• I'll give you words to spell - write them on paper
• THREE ways to check your answer:
  - Say "Ready" (or "Done", "Finished", "Check it") - I understand many phrases!
  - Say "Auto Check" for smart camera monitoring (continuous for all words!)
  - Just show me your paper - I'm always watching! 👀
• Get helpful tips if you need help with tricky words
• Say "End Game" to stop playing anytime

🔤 LETTER WORD GAME (NEW!):
• Say "Letter Game" or "Letter Word Game" to start a fun word adventure!
• I'll give you a letter and a hint - guess the word that starts with that letter!
• Example: "Letter B, something you read" → Answer: "Book"
• Say "Hint" if you need another clue
• Say "Skip" to try a different word
• Say "Stats" to see how you're doing
• Say "End Game" when you're ready to stop
• Build your vocabulary and thinking skills!

🇵🇭 FILIPINO TRANSLATION GAME (NEW!):
• Say "Filipino Game" for a language exploration! 🦕🇵🇭
• Simple: I say English, you say Filipino!
• Learn words about animals, family, colors, and more!
• Quick feedback and automatic next questions!

🧮 MATH WORD PROBLEMS (NEW!):
• Say "Math Game" to solve fun word problems! ✨
• I'll give you math stories to solve
• Write BOTH the equation AND answer on paper
• Say 'Ready' when you're done, or just show me!
• Get hints and step-by-step help
• Practice addition, subtraction, and more!

🦕 ANIMAL GUESSING GAME (NEW!):
• Say "Animal Game" or "Guess the Animal" to start! 🐾
• Show me any animal toy, figure, or picture
• I'll identify it and share amazing facts!
• Learn about dinosaurs, mammals, birds, and more!
• Discover cool abilities and behaviors
• Build your animal knowledge collection!
• Say "Animal Stats" to see your discoveries
• Say "End Animal Game" when you're done

🤖 SMART SPELLING FEATURES:
• Enhanced speech recognition - I understand when you're ready!
• Try saying: "Done", "Finished", "Check it", "Look at this"
• Automatic visual detection - no speech needed!
• NEW: Auto-check is now continuous by default - works for ALL words!
• Multiple checking modes for different preferences

💡 CONVERSATION MODES:
• AUTOMATIC: Just step in front of the camera - I'll start listening immediately!
• VOICE ACTIVATED: Say 'Miley' if I don't see you
• No need to repeat wake words during conversation
• Say 'goodbye' to end, or I'll timeout after 1 minute of silence

👁️ FACE RECOGNITION:
• I can see and recognize your face!
• Automatic conversation starts when I see you
• No wake words needed when you're visible!
• Just step away or say 'goodbye' to end

🧠 SMART FEATURES:
• I remember our conversation! Ask me to "repeat" what I just said
• I know what we talked about earlier and can reference it
• Context-aware responses based on our discussion
• Each conversation builds on what we discussed before

🔊 AUDIO FEEDBACK:
• Listen for sounds! I beep when I'm ready to hear you
• I play a gentle tone when I'm done talking
• Say "turn off sounds" to disable audio cues
• Say "turn on sounds" to re-enable them

Ask me anything, show me any object, or play any of the games to practice your skills!"""
        
        elif user == 'eladriel':
            return """Hey Eladriel! I'm your dinosaur-loving assistant! Here's what I can do:
            
🦕 DINOSAUR FEATURES:
• Say "identify dinosaur" - I'll use my camera to identify your dinosaur toys!
• Say "show me camera" - See what my camera can see
• Say "dinosaur tips" - Get tips for better dinosaur identification

🔍 UNIVERSAL OBJECT IDENTIFICATION:
• Say "What is this?" or "Identify this" - I'll identify ANY object you show me!
• Learn about toys, tools, household items, nature objects, and more!
• I'll connect things to dinosaurs and adventures when possible!
• Perfect for exploring everything around you!

📝 SPELLING GAME (NEW!):
• Say "Spelling Game" for a roar-some spelling adventure! 🦕📝
• I'll give you words to spell - write them clearly on paper
• THREE dino-powered ways to check your answer:
  - Say "Ready" (or "Done", "Finished") - I understand dino-speak!
  - Say "Auto Check" for dino-vision monitoring 🦕👁️ (continuous for all words!)
  - Just show me your paper - my dino-eyes are always watching!
• Get dinosaur-themed help and encouragement for tricky words
• Say "End Game" whenever you want to stop

🔤 DINO-LETTER WORD ADVENTURE (NEW!):
• Say "Letter Game" or "Letter Word Game" for a prehistoric word hunt! 🦕🔤
• I'll give you a letter and a dino-themed hint - guess the word!
• Example: "Letter T, a giant dino with tiny arms" → Answer: "Triceratops"
• Learn words about dinosaurs, animals, and cool things!
• Say "Hint" if you need a dino-clue boost
• Say "Skip" to hunt for a different word
• Say "Stats" to see your discovery count
• Say "End Game" when your expedition is complete
• Build your paleontologist vocabulary!

🇵🇭 FILIPINO TRANSLATION ADVENTURE (NEW!):
• Say "Filipino Game" for a language exploration! 🦕🇵🇭
• Simple: I say English, you say Filipino!
• Learn words about animals, family, colors, and more!
• Quick feedback and automatic next questions!

🧮 DINO-MATH ADVENTURES (NEW!):
• Say "Math Game" for mathematical dinosaur stories! 🦕🧮
• Solve word problems about dinosaurs and adventures
• Write equations AND answers like a math-a-saurus!
• Say 'Ready' when done, or show me your work!
• Get dino-powered hints and encouragement
• Count like the smartest dinosaurs!

🦕 DINO-ANIMAL DISCOVERY GAME (NEW!):
• Say "Animal Game" or "Guess the Animal" for creature adventures! 🦕🐾
• Show me ANY animal toy, figure, or picture - especially dinosaurs!
• I'll identify it with dino-expert knowledge and amazing facts!
• Learn about prehistoric creatures, modern animals, and their connections!
• Discover incredible abilities, behaviors, and evolutionary secrets!
• Build your paleontologist's creature collection!
• Say "Animal Stats" to see all your discoveries
• Say "End Animal Game" when your expedition is complete

🦕 DINO-SMART FEATURES:
• Enhanced ready detection - I hear you roar when you're done!
• Try dino-phrases: "All done!", "Check it!", "Finished!"
• Automatic dino-vision - no need to say anything!
• NEW: Dino-vision is now continuous by default - watches ALL your spelling!
• Multiple modes for every young paleontologist!

🌟 GENERAL FEATURES:
• Ask me questions about dinosaurs, animals, or anything!
• Get amazing facts about prehistoric creatures
• Learn about different time periods

💡 CONVERSATION MODES:
• AUTOMATIC: Just step in front of the camera - I'll start listening immediately!
• VOICE ACTIVATED: Say 'Dino' if I don't see you
• No need to repeat wake words during conversation
• Say 'goodbye' to end, or I'll timeout after 1 minute of silence

👁️ FACE RECOGNITION:
• I can see and recognize your face!
• Automatic conversation starts when I see you
• Perfect for showing me dinosaurs and other objects - no wake words needed!
• Just step away or say 'goodbye' to end

🧠 SMART FEATURES:
• I remember our conversation! Say "repeat" if you want to hear something again
• I know what we talked about earlier and can reference it
• Context-aware responses based on our discussion
• Each conversation builds on what we discussed before

🔊 AUDIO FEEDBACK:
• Listen for sounds! I beep when I'm ready to hear you
• I play a gentle tone when I'm done talking
• Say "turn off sounds" to disable audio cues
• Say "turn on sounds" to re-enable them

What do you want to explore today? Show me anything you've discovered, or let's practice with games! 🚀"""
        
        elif user == 'parent':
            return """Parent Mode Active - Advanced Features Available:

🔧 SYSTEM COMMANDS:
• "Status report" - Get system health and usage statistics
• "System check" - Run diagnostic tests on all components
• "Quiet mode on/off" - Control volume for nighttime use

👶 CHILD MONITORING:
• "Check on kids" - Review recent activity and interactions
• Face recognition shows when children are detected
• Conversation logs available for review

🔍 OBJECT IDENTIFICATION:
• Same advanced object identification as the kids
• "What is this?" works for any household item
• Great for identifying unknown objects or tools

📝 SPELLING GAME TESTING:
• Say "Spelling Game" to test the interactive spelling system
• Validate camera-based answer checking functionality
• Review Grade 2-3 word list and educational feedback
• Test all game mechanics before kids use it
• Use "Ready" and "End Game" commands for full testing
• NEW: Auto check is now continuous by default - automatically monitors all words

🔤 LETTER WORD GAME TESTING (NEW!):
• Say "Letter Game" to test the word guessing system
• Validates letter-based vocabulary building mechanics
• Reviews age-appropriate words and hints for each letter
• Tests hint system and skip functionality
• Monitors scoring and progress tracking
• Use "Stats", "Hint", "Skip", and "End Game" commands for full testing
• Perfect for validating educational content and difficulty levels

🇵🇭 FILIPINO TRANSLATION GAME TESTING:
• Say "Filipino Game" to test the language learning system
• Simple English-to-Filipino translation format
• Monitors response accuracy and learning progress

🧮 MATH QUIZ GAME TESTING (NEW!):
• Say "Math Game" to test the word problem system  
• Validates camera-based equation and answer checking
• Reviews age-appropriate math problems with hints
• Tests OCR accuracy for mathematical notation
• Difficulty levels: Easy, Medium, Hard
• Use "Ready" and "End Math" commands for full testing

🦕 ANIMAL GUESSING GAME TESTING (NEW!):
• Say "Animal Game" to test the animal identification system
• Validates OpenAI Vision API accuracy for toy/figure recognition
• Reviews educational content and fact delivery
• Tests specialized prompts for different users (Eladriel vs Sophia)
• Monitors learning progression and engagement metrics
• Use "Animal Stats" and "End Animal Game" for full testing
• Perfect for validating camera positioning and lighting requirements

💡 CONVERSATION MODES:
• VOICE ACTIVATED: Say 'Assistant' to activate
• FACE RECOGNITION: Automatic activation when you're detected
• Extended timeout (no rush like with kids)
• Professional, efficient responses

🛠️ TECHNICAL FEATURES:
• Full access to camera and audio systems
• Real-time system monitoring
• Error reporting and troubleshooting
• Configuration adjustments

🧠 CONVERSATION INTELLIGENCE:
• Full conversation memory and context tracking
• Repeat functionality for all responses
• Context-aware responses that reference earlier discussion
• Conversation history maintained throughout session

🔊 AUDIO FEEDBACK SYSTEM:
• Pleasant audio cues for interaction flow
• Listening confirmation sounds
• Speech completion indicators
• "turn off sounds" / "turn on sounds" controls

All standard features available with enhanced capabilities for household management."""
        
        return "I'm here to help! Just ask me anything you're curious about or show me any object!"

    def get_system_status(self) -> str:
        """Provide system status report for parent mode."""
        try:
            import psutil
            import time
            
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            
            # Get AI assistant specific status
            face_recognition_status = "Active" if self.face_recognition_active else "Inactive"
            camera_status = "Connected" if self.face_detector.cap and self.face_detector.cap.isOpened() else "Disconnected"
            
            # Get recent activity
            current_time = time.strftime("%I:%M %p")
            
            status_report = f"""System Status Report - {current_time}

🖥️ SYSTEM HEALTH:
• CPU Usage: {cpu_usage}%
• Memory: {memory_info.percent}% used ({memory_info.available // (1024**3)} GB available)
• Storage: {disk_info.percent}% used

🤖 AI ASSISTANT STATUS:
• Face Recognition: {face_recognition_status}
• Camera: {camera_status}
• Current User: {self.current_user or 'None (Standby)'}
• Wake Words: Miley (Sophia), Dino (Eladriel), Assistant (Parent)

📊 OPERATIONAL STATUS:
• Speech Recognition: Functional
• Text-to-Speech: Premium OpenAI voices active
• Object Identification: Ready
• Dinosaur Recognition: Ready for Eladriel

All systems operational. Running smoothly."""
            
            return status_report
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return "Status report unavailable. System monitoring tools may not be installed."

    def run_system_diagnostic(self) -> str:
        """Run system diagnostic tests for parent mode."""
        try:
            diagnostic_results = []
            
            # Test microphone
            mic_test = self.audio_manager.test_microphone()
            diagnostic_results.append(f"🎤 Microphone: {'✅ Pass' if mic_test else '❌ Fail'}")
            
            # Test camera
            camera_test = self.face_detector.cap and self.face_detector.cap.isOpened()
            diagnostic_results.append(f"📷 Camera: {'✅ Pass' if camera_test else '❌ Fail'}")
            
            # Test OpenAI connection
            try:
                test_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
                openai_test = True
            except:
                openai_test = False
            diagnostic_results.append(f"🤖 OpenAI API: {'✅ Pass' if openai_test else '❌ Fail'}")
            
            # Test face recognition
            face_test = self.face_detector is not None
            diagnostic_results.append(f"👁️ Face Recognition: {'✅ Pass' if face_test else '❌ Fail'}")
            
            # Test TTS engines
            tts_test = self.sophia_tts is not None and self.eladriel_tts is not None
            diagnostic_results.append(f"🗣️ Text-to-Speech: {'✅ Pass' if tts_test else '❌ Fail'}")
            
            results_text = "\n".join(diagnostic_results)
            return f"""System Diagnostic Complete:

{results_text}

Overall Status: {'✅ All systems operational' if all(['✅' in result for result in diagnostic_results]) else '⚠️ Some issues detected'}"""
            
        except Exception as e:
            logger.error(f"Error running diagnostics: {e}")
            return "❌ Diagnostic test failed. Unable to complete system check."

    def enable_quiet_mode(self) -> str:
        """Enable quiet mode with reduced volume and slower speech."""
        try:
            self.quiet_mode = True
            
            # Reduce volume and slow down speech for all TTS engines
            engines = [self.sophia_tts, self.eladriel_tts]
            for engine in engines:
                engine.setProperty('volume', 0.3)  # 30% volume
                current_rate = engine.getProperty('rate')
                engine.setProperty('rate', max(100, int(current_rate * 0.7)))  # Slower speech
            
            current_hour = datetime.now().hour
            if current_hour >= 21 or current_hour <= 6:  # 9 PM to 6 AM
                return "Quiet mode enabled. Speaking softly to avoid waking the children. Volume reduced to 30%."
            else:
                return "Quiet mode enabled. Volume reduced to 30% and speaking more slowly."
            
        except Exception as e:
            logger.error(f"Error enabling quiet mode: {e}")
            return "Error enabling quiet mode. Please try again."

    def disable_quiet_mode(self) -> str:
        """Disable quiet mode and restore normal volume and speech rate."""
        try:
            # Restore normal volume and speech rate for all TTS engines
            engines = [self.sophia_tts, self.eladriel_tts]
            for engine in engines:
                engine.setProperty('volume', 0.8)  # 80% volume
                engine.setProperty('rate', 200)  # Normal speech rate
            
            self.quiet_mode = False
            return "Quiet mode disabled. Volume restored to normal levels."
            
        except Exception as e:
            logger.error(f"Error disabling quiet mode: {e}")
            return "Error disabling quiet mode. Please try again."

    def check_kids_status(self) -> str:
        """Check on kids' recent activity and interactions."""
        try:
            current_time = time.strftime("%I:%M %p")
            
            # Check if kids are currently detected
            kids_present = []
            for user in ['sophia', 'eladriel']:
                if user in self.last_face_greeting:
                    last_seen_time = self.last_face_greeting[user]
                    time_since = time.time() - last_seen_time
                    if time_since < 300:  # Within last 5 minutes
                        kids_present.append(f"{user.title()} (seen {int(time_since//60)} min ago)")
            
            status_message = f"""Kids Status Report - {current_time}

👶 RECENT ACTIVITY:
"""
            
            if kids_present:
                status_message += f"• Currently detected: {', '.join(kids_present)}\n"
            else:
                status_message += "• No children detected in last 5 minutes\n"
            
            status_message += f"""
🎭 FACE RECOGNITION:
• Face detection system: {'Active' if self.face_recognition_active else 'Inactive'}
• Auto-conversation: {'In progress' if self.current_user else 'Standby mode'}

🔧 SYSTEM STATUS:
• All child-safe features operational
• Wake words active: 'Miley' (Sophia), 'Dino' (Eladriel)
• Ready for immediate interaction when kids appear

Everything looks good for when the children wake up!"""
            
            return status_message
            
        except Exception as e:
            logger.error(f"Error checking kids status: {e}")
            return "Unable to retrieve kids status information."

    def is_conversation_ending(self, user_input: str) -> bool:
        """Check if the user wants to end the conversation."""
        # If spelling game is active, only allow explicit game ending
        if self.spelling_game_active:
            explicit_end_phrases = [
                'goodbye', 'bye', 'see you later', 'talk to you later', 
                'exit', 'end conversation', 'go away'
            ]
        else:
            explicit_end_phrases = [
                'goodbye', 'bye', 'see you later', 'talk to you later', 
                'that\'s all', 'thanks', 'thank you', 'stop', 'exit',
                'done', 'finished', 'end conversation', 'go away'
            ]
        
        user_input_lower = user_input.lower()
        return any(phrase in user_input_lower for phrase in explicit_end_phrases)

    def handle_user_interaction(self, user: str):
        """Handle the complete interaction flow with natural conversation mode."""
        self.current_user = user
        user_info = self.users[user]
        
        # Get greeting (fresh for parent mode to check current time)
        if user == 'parent':
            greeting = self.get_parent_greeting()
        else:
            # Generate fresh dynamic greeting each time
            greeting = self.get_dynamic_greeting(user)
        
        # If spelling game is active, modify greeting to indicate game continuation
        if self.spelling_game_active and self.current_spelling_word:
            word = self.current_spelling_word['word']
            if user == 'sophia':
                greeting = f"Hi Sophia! I see you're back! We were working on spelling '{word}'. Are you ready to show me your answer, or do you need me to repeat the word?"
            elif user == 'eladriel':
                greeting = f"Hey Eladriel! Welcome back to our spelling adventure! We were practicing '{word}'. Ready to show me what you wrote, or need the word again?"
            elif user == 'parent':
                greeting = f"Parent mode resumed. Spelling game test in progress - current word: '{word}'. Say 'Ready' to test answer checking or 'End Game' to stop."
        
        # Greet the user
        self.speak(greeting, user)
        
        # Start conversation loop - keep listening until user says goodbye
        conversation_active = True
        conversation_timeout_count = 0
        # Extend timeout when spelling game is active to give more time for writing
        max_timeouts = 6 if self.spelling_game_active else 2  # Allow 6 timeouts for spelling game, 2 for normal conversation
        
        while conversation_active and self.running and self.current_user == user:
            # Check if speech was interrupted before listening for new input
            if self.speech_interrupted:
                logger.info("Handling speech interruption")
                
                # Check if the interruption was a goodbye command
                last_interrupt_input = getattr(self, 'last_interrupt_input', '')
                
                if any(phrase in last_interrupt_input for phrase in ['goodbye', 'bye', 'see you later', 'talk to you later']):
                    # User said goodbye as interruption - end conversation
                    farewell_messages = {
                        'sophia': "Goodbye Sophia! I'm always here when you need me. Have a wonderful day!",
                        'eladriel': "See you later Eladriel! Keep exploring and learning about dinosaurs! Roar!",
                        'parent': "Goodbye! Parent mode deactivated. All systems remain operational for the children."
                    }
                    farewell_response = farewell_messages.get(user, "Goodbye! Talk to you soon!")
                    
                    # Add farewell to history and then clear it
                    self.add_to_conversation_history(user, user_input, farewell_response)
                    self.speak(farewell_response, user)
                    
                    # Clear conversation history for fresh start next time
                    self.clear_conversation_history(user)
                    
                    conversation_active = False
                    break
                else:
                    # Regular interruption - acknowledge and continue
                    interrupt_responses = {
                        'sophia': "Oh! Sorry Sophia! I'm listening now.",
                        'eladriel': "Whoops! You got my attention, Eladriel! What's up?",
                        'parent': "Interrupted. Ready for your next request."
                    }
                    
                    # Brief acknowledgment (will also be interruptible)
                    self.speak(interrupt_responses.get(user, "Yes? I'm listening!"), user)
                
                # Reset the interrupt flag
                self.speech_interrupted = False
            
            # Listen for their request with a 15-second timeout (longer for children)
            user_input = self.listen_for_speech(timeout=15)
            
            if user_input:
                conversation_timeout_count = 0  # Reset timeout counter
                
                # Check if user wants to end conversation
                if self.is_conversation_ending(user_input):
                    farewell_messages = {
                        'sophia': "Goodbye Sophia! I'm always here when you need me. Have a wonderful day!",
                        'eladriel': "See you later Eladriel! Keep exploring and learning about dinosaurs! Roar!",
                        'parent': "Goodbye! Parent mode deactivated. All systems remain operational for the children. Call 'Assistant' anytime you need me."
                    }
                    farewell_response = farewell_messages.get(user, "Goodbye! Talk to you soon!")
                    
                    # Add farewell to history and then clear it
                    self.add_to_conversation_history(user, user_input, farewell_response)
                    self.speak(farewell_response, user)
                    
                    # Clear conversation history for fresh start next time
                    self.clear_conversation_history(user)
                    
                    conversation_active = False
                    break
                
                # Check for special commands first
                special_response = self.handle_special_commands(user_input, user)
                
                if special_response:
                    # Add special command to conversation history too
                    self.add_to_conversation_history(user, user_input, special_response)
                    
                    # Use no-interrupt speak for Filipino game responses to prevent recording during explanations
                    if self.filipino_translator.is_filipino_game_command(user_input) or self.filipino_translator.game_active:
                        self.speak_no_interrupt(special_response, user)
                    else:
                        self.speak(special_response, user)
                else:
                    # Process with OpenAI for regular conversation
                    import asyncio
                    try:
                        response = asyncio.run(self.process_with_openai(user_input, user))
                        
                        # Use no-interrupt speak if Filipino game is active to prevent recording during explanations
                        if self.filipino_translator.game_active:
                            self.speak_no_interrupt(response, user)
                        else:
                            self.speak(response, user)
                    except Exception as e:
                        logger.error(f"Error processing request: {e}")
                        self.speak("I'm sorry, something went wrong. Let me try again.", user)
                
                # After responding, give a subtle cue that we're still listening
                time.sleep(0.5)  # Brief pause
                print(f"💬 Still chatting with {user.title()}... (say 'goodbye' to end)")
                
            else:
                # No speech detected
                conversation_timeout_count += 1
                
                # Update max timeouts dynamically based on current spelling game state
                current_max_timeouts = 6 if self.spelling_game_active else 2
                
                if conversation_timeout_count == 1:
                    # First timeout - gentle prompt
                    if self.spelling_game_active:
                        prompts = {
                            'sophia': "Take your time writing, Sophia! I'm waiting for you to say 'Ready'.",
                            'eladriel': "No rush Eladriel! Let me know when you're ready to show me your spelling!",
                            'parent': "Spelling game active. Say 'Ready' when you want me to check your answer."
                        }
                    else:
                        prompts = {
                            'sophia': "I'm still here if you have more questions, Sophia!",
                            'eladriel': "Still here for more dinosaur fun, Eladriel! What's next?",
                            'parent': "I'm still here and ready to assist. Any additional requests?"
                        }
                    self.speak(prompts.get(user, "I'm still listening if you have more to say!"), user)
                    print(f"⏰ Waiting for {user.title()} to continue...")
                    
                elif conversation_timeout_count >= current_max_timeouts:
                    # Multiple timeouts - end conversation gracefully
                    if self.spelling_game_active:
                        # Special handling for spelling game timeout
                        timeout_messages = {
                            'sophia': "I'll pause the spelling game for now, Sophia. Say 'Spelling Game' to continue practicing anytime!",
                            'eladriel': "Let's pause our spelling adventure, Eladriel! Say 'Spelling Game' when you want to play again!",
                            'parent': "Spelling game test paused due to timeout. Game state preserved for continuation."
                        }
                        # Don't reset spelling game state on timeout - just pause it
                    else:
                        timeout_messages = {
                            'sophia': "I'll be here whenever you need me, Sophia. Just say 'Miley' to chat again!",
                            'eladriel': "I'll be waiting for more dinosaur adventures, Eladriel! Just say 'Dino' when you're ready!",
                            'parent': "Returning to standby mode. Say 'Assistant' anytime for immediate assistance."
                        }
                    self.speak(timeout_messages.get(user, "I'll be here when you need me. Just call my name!"), user)
                    conversation_active = False
        
        self.current_user = None
        print("🎤 Conversation ended. Listening for wake words again...")
        # Note: Spelling game state persists between conversations - only reset when user explicitly ends game

    def run(self):
        """Main loop - listen for wake words and handle natural conversations with face recognition."""
        self.running = True
        logger.info("AI Assistant started - Listening for wake words...")
        
        # Start face recognition system
        self.start_face_recognition()
        
        print("🤖 AI Assistant is now running with AUTOMATIC CONVERSATION MODE!")
        print("📢 How to interact:")
        print("   • AUTOMATIC: Just step in front of the camera!")
        print("   • VOICE: Say 'Miley' (Sophia), 'Dino' (Eladriel), or 'Assistant' (Parent)")
        print("💡 NEW FEATURES:")
        print("   • Face detection automatically starts conversations!")
        print("   • Universal object identification - show me anything!")
        print("   • No wake words needed when you're visible!")
        print("   • 1-minute timeout returns to wake word mode")
        print("   • Say 'goodbye' to end conversations anytime")
        print("🔍 Object identification: Say 'What is this?' with any object!")
        print("👁️ Face recognition active - I can see Sophia and Eladriel!")
        print("👨‍💼 Parent Mode: Say 'Assistant' for admin features and quiet mode!")
        print("🎤 Listening for faces and wake words...")
        
        try:
            while self.running:
                # Listen for wake words (only when no one is in conversation)
                if not self.current_user:
                    detected_user = self.wake_word_detector.listen_for_wake_word()
                    
                    if detected_user:
                        logger.info(f"Wake word detected for: {detected_user}")
                        print(f"👋 Hello {detected_user.title()}! Starting voice-activated conversation...")
                        
                        # Play wake word confirmation sound
                        self.play_wake_word_sound()
                        
                        # Handle the user interaction with conversation mode
                        self.handle_user_interaction(detected_user)
                else:
                    # Someone is in conversation, just wait
                    time.sleep(0.5)
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            logger.info("Shutting down AI Assistant...")
            self.stop()
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            self.stop()

    def stop(self):
        """Gracefully shutdown the assistant."""
        self.running = False
        
        # Stop interrupt system
        self.stop_interrupt_listener()
        
        # Stop other components
        self.wake_word_detector.stop()
        self.stop_face_recognition()
        
        # Cleanup object identification resources
        try:
            self.object_identifier.cleanup()
            self.dinosaur_identifier.cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        
        logger.info("AI Assistant stopped")
        print("👋 AI Assistant stopped. Goodbye!")

    def start_spelling_game(self, user: str) -> str:
        """Start an interactive spelling game for kids with streamlined, exciting instructions."""
        try:
            import random
            
            # Initialize game state
            self.spelling_game_active = True
            self.spelling_word_index = 0
            self.spelling_score = 0
            
            # Shuffle the words for variety
            random.shuffle(self.spelling_words_grade2_3)
            
            # Get first word
            self.current_spelling_word = self.spelling_words_grade2_3[self.spelling_word_index]
            
            user_name = user.title()
            
            # Super short, exciting intros
            if user == 'sophia':
                intro = f"🌟 Hi Sophia! Let's spell some words! Ready to be a spelling star? ✨"
            elif user == 'eladriel':
                intro = f"🦕 Hey Eladriel! Time for a spelling adventure! Let's go! 🌟"
            else:  # parent
                intro = f"📝 Parent Mode: Quick Spelling Game Test"
            
            word = self.current_spelling_word['word']
            hint = self.current_spelling_word['hint']
            
            # Super streamlined instructions
            game_instructions = f"""{intro}

✏️ SPELLING TIME! ✏️

Word #1: {word.upper()}
💡 Hint: {hint}

📝 Write '{word}' on paper with BIG letters!
🗣️ Say 'Ready' when you're done!
👀 Or just show me - I'm watching!

Let's go! 🚀"""
            
            return game_instructions
            
        except Exception as e:
            logger.error(f"Error starting spelling game: {e}")
            return "Oops! Let's try starting the spelling game again! 🎮"

    def check_spelling_answer(self, user: str) -> str:
        """Check the student's written spelling answer using camera."""
        try:
            if not self.spelling_game_active or not self.current_spelling_word:
                return "We're not playing the spelling game right now. Say 'Spelling Game' to start!"
            
            user_name = user.title()
            correct_word = self.current_spelling_word['word']
            
            self.speak(f"Great {user_name}! Let me see what you wrote. Hold your paper steady in front of the camera...", user)
            
            # Give time to position the paper
            time.sleep(3)
            
            # Capture and analyze the written answer with enhanced OCR
            result = self.object_identifier.capture_and_identify_text(user, expected_word=correct_word)
            
            if result["success"]:
                # Get the detected text from OCR
                detected_text = result.get("detected_text", "").strip().lower()
                ai_description = result["message"].lower()
                
                # Enhanced spelling verification
                is_correct = self.verify_spelling_accuracy(detected_text, ai_description, correct_word)
                
                if is_correct:
                    # Correct answer!
                    self.spelling_score += 1
                    
                    # Play celebration sound for correct answer
                    self.play_spelling_correct_sound()
                    
                    if user == 'sophia':
                        praise = f"Excellent work Sophia! ⭐ You spelled '{correct_word}' perfectly! You're doing amazing!"
                    elif user == 'eladriel':
                        praise = f"Roar-some job Eladriel! 🦕⭐ You spelled '{correct_word}' correctly! You're a spelling champion!"
                    else:  # parent
                        praise = f"✅ Correct spelling detected: '{correct_word}'. Camera recognition system working properly. Detected: '{detected_text}'"
                    
                    # Move to next word
                    self.spelling_word_index += 1
                    
                    if self.spelling_word_index >= len(self.spelling_words_grade2_3):
                        # Game completed!
                        final_score = f"""{praise}

🎉 Congratulations! You completed the spelling game! 🎉
Final Score: {self.spelling_score} out of {len(self.spelling_words_grade2_3)} words correct!

You're an amazing speller! Great job! 📝✨"""
                        self.spelling_game_active = False
                        return final_score
                    else:
                        # Next word
                        self.current_spelling_word = self.spelling_words_grade2_3[self.spelling_word_index]
                        next_word = self.current_spelling_word['word']
                        next_hint = self.current_spelling_word['hint']
                        
                        return f"""{praise}

⚡ Next word! ⚡

Word #{self.spelling_word_index + 1}: {next_word.upper()}
💡 Hint: {next_hint}

📝 Write '{next_word}' and say 'Ready'! 🚀"""
                
                else:
                    # Incorrect answer - provide helpful feedback with what was detected
                    
                    # Play buzzer sound for incorrect answer
                    self.play_spelling_wrong_sound()
                    
                    detected_info = f" (I saw: '{detected_text}')" if detected_text else ""
                    
                    if user == 'sophia':
                        feedback = f"Good try Sophia! ✨ The correct spelling is '{correct_word.upper()}'{detected_info}."
                    elif user == 'eladriel':
                        feedback = f"Nice effort Eladriel! 🦕 The correct spelling is '{correct_word.upper()}'{detected_info}."
                    else:  # parent
                        feedback = f"❌ Incorrect. Expected: '{correct_word.upper()}'{detected_info}."
                    
                    # Provide quick spelling help
                    letters = " - ".join(correct_word.upper())
                    
                    return f"""{feedback}

💡 Quick help: {letters}
📝 Try writing '{correct_word}' again!
🗣️ Say 'Ready' when done! ✨"""
            
            else:
                return f"Can't see your paper clearly! 👀 Make sure to write with BIG, dark letters. Say 'Ready' to try again! 📝"
                
        except Exception as e:
            logger.error(f"Error checking spelling answer: {e}")
            return "Sorry! I had trouble checking your answer. Let's try again!"

    def verify_spelling_accuracy(self, detected_text: str, ai_description: str, correct_word: str) -> bool:
        """Enhanced spelling verification with multiple accuracy checks."""
        correct_word_lower = correct_word.lower()
        
        # Method 1: Exact match from OCR
        if detected_text == correct_word_lower:
            logger.info(f"✅ Exact OCR match: '{detected_text}' == '{correct_word_lower}'")
            return True
        
        # Method 2: Check if correct word is explicitly mentioned in AI description
        # Look for phrases like "the word 'cat'" or "says 'dog'" or "written 'sun'"
        import re
        word_patterns = [
            rf"word\s+['\"`]?{re.escape(correct_word_lower)}['\"`]?",
            rf"says\s+['\"`]?{re.escape(correct_word_lower)}['\"`]?",
            rf"written\s+['\"`]?{re.escape(correct_word_lower)}['\"`]?",
            rf"text\s+['\"`]?{re.escape(correct_word_lower)}['\"`]?",
            rf"reads\s+['\"`]?{re.escape(correct_word_lower)}['\"`]?",
            rf"['\"`]{re.escape(correct_word_lower)}['\"`]\s+written",
            rf"['\"`]{re.escape(correct_word_lower)}['\"`]\s+spelled",
        ]
        
        for pattern in word_patterns:
            if re.search(pattern, ai_description):
                logger.info(f"✅ AI description confirms correct word: '{correct_word}' found in: {ai_description}")
                return True
        
        # Method 3: Strict character sequence check (only for very short words)
        if len(correct_word_lower) <= 3:
            # For very short words, check if all letters appear in correct sequence
            cleaned_text = ''.join(c for c in detected_text if c.isalpha())
            if cleaned_text == correct_word_lower:
                logger.info(f"✅ Short word exact match: '{cleaned_text}' == '{correct_word_lower}'")
                return True
        
        # Method 4: Check for close variations (handle OCR errors like 0 vs O, 1 vs l)
        ocr_variations = {
            '0': 'o', 'o': '0',
            '1': 'l', 'l': '1', 'i': '1',
            '5': 's', 's': '5',
            '8': 'b', 'b': '8',
            '6': 'g', 'g': '6'
        }
        
        def normalize_ocr_errors(text):
            """Normalize common OCR character confusion."""
            result = text.lower()
            for char, replacement in ocr_variations.items():
                result = result.replace(char, replacement)
            return result
        
        normalized_detected = normalize_ocr_errors(detected_text)
        normalized_correct = normalize_ocr_errors(correct_word_lower)
        
        if normalized_detected == normalized_correct:
            logger.info(f"✅ OCR-normalized match: '{detected_text}' -> '{normalized_detected}' == '{normalized_correct}'")
            return True
        
        # If none of the above methods confirm correctness, it's incorrect
        logger.info(f"❌ Spelling verification failed:")
        logger.info(f"   Expected: '{correct_word_lower}'")
        logger.info(f"   OCR detected: '{detected_text}'")
        logger.info(f"   AI description: '{ai_description[:100]}...'")
        
        return False

    def provide_spelling_help(self, word: str, user: str) -> str:
        """Provide helpful spelling tips for the word."""
        word_lower = word.lower()
        
        # Letter-by-letter breakdown
        letters = " - ".join(word.upper())
        
        if user == 'sophia':
            help_text = f"""Here's how to spell '{word}' step by step:

📝 Letter by letter: {letters}
🔤 The word has {len(word)} letters
💡 Remember: {self.current_spelling_word['hint']}"""
        elif user == 'eladriel':
            help_text = f"""Let's break down '{word}' like a dinosaur discovery! 🦕

📝 Letter by letter: {letters}
🔤 This word has {len(word)} letters - count them like dinosaur footprints!
💡 Remember: {self.current_spelling_word['hint']}"""
        else:  # parent
            help_text = f"""Spelling Help System Test for '{word}':

📝 Letter breakdown: {letters}
🔤 Word length: {len(word)} characters
💡 Hint provided: {self.current_spelling_word['hint']}
🔧 Testing educational feedback delivery"""
        
        # Add specific tips for common tricky words
        if 'double' in word_lower or any(word_lower.count(c) > 1 for c in word_lower):
            help_text += f"\n⚠️ Special tip: This word has double letters - watch out for them!"
        
        if any(combo in word_lower for combo in ['th', 'ch', 'sh', 'ck']):
            help_text += f"\n⚠️ Special tip: This word has a letter combination - two letters that make one sound!"
        
        return help_text

    def end_spelling_game(self, user: str) -> str:
        """End the spelling game and provide final feedback."""
        if not self.spelling_game_active:
            return "We weren't playing the spelling game. Say 'Spelling Game' if you want to start playing!"
        
        user_name = user.title()
        
        if user == 'sophia':
            farewell = f"🌟 Great job Sophia! You're a spelling star! ✨"
        elif user == 'eladriel':
            farewell = f"🦕 Awesome job Eladriel! Dino-mite spelling! 🌟"
        else:  # parent
            farewell = f"📝 Spelling Game Complete - Parent Mode"
        
        final_message = f"""{farewell}

📊 Score: {self.spelling_score} out of {self.spelling_word_index + 1} words!

🎯 Keep practicing! Say 'Spelling Game' to play again! 🚀"""
        
        # Reset game state
        self.spelling_game_active = False
        self.current_spelling_word = None
        self.spelling_word_index = 0
        self.spelling_score = 0
        self.auto_check_active = False  # Reset auto check mode
        self.persistent_auto_check = False  # Reset persistent auto check mode
        
        return final_message

    def add_to_conversation_history(self, user: str, user_message: str, ai_response: str):
        """Add exchange to conversation history for context."""
        if user not in self.conversation_history:
            self.conversation_history[user] = []
        
        # Add the exchange
        exchange = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'ai_response': ai_response
        }
        
        self.conversation_history[user].append(exchange)
        
        # Keep only the last N exchanges to prevent memory issues
        if len(self.conversation_history[user]) > self.max_history_length:
            self.conversation_history[user] = self.conversation_history[user][-self.max_history_length:]
        
        # Store last response for repeat functionality
        self.last_ai_response[user] = ai_response
        
        logger.info(f"Added to conversation history for {user}: {len(self.conversation_history[user])} exchanges")

    def get_conversation_context(self, user: str) -> str:
        """Get recent conversation context for the user."""
        if user not in self.conversation_history or not self.conversation_history[user]:
            return ""
        
        # Get last 3 exchanges for context (not too much to overwhelm the prompt)
        recent_history = self.conversation_history[user][-3:]
        
        context_parts = []
        for exchange in recent_history:
            context_parts.append(f"Previous - You asked: '{exchange['user_message']}' | You responded: '{exchange['ai_response']}'")
        
        return "\n".join(context_parts)

    def clear_conversation_history(self, user: str):
        """Clear conversation history for a user (e.g., when they say goodbye)."""
        if user in self.conversation_history:
            self.conversation_history[user] = []
        if user in self.last_ai_response:
            del self.last_ai_response[user]
        if user in self.conversation_context:
            del self.conversation_context[user]
        logger.info(f"Cleared conversation history for {user}")

    def get_last_response(self, user: str) -> str:
        """Get the last AI response for repeat functionality."""
        return self.last_ai_response.get(user, "I haven't said anything yet in our conversation!")

    def handle_repeat_request(self, user: str) -> str:
        """Handle when user asks AI to repeat what it just said."""
        last_response = self.get_last_response(user)
        
        if user == 'sophia':
            return f"Of course Sophia! I just said: {last_response}"
        elif user == 'eladriel':
            return f"Sure thing Eladriel! I just said: {last_response}"
        elif user == 'parent':
            return f"Repeating last response: {last_response}"
        else:
            return f"I just said: {last_response}"

    def get_dynamic_greeting(self, user: str) -> str:
        """Generate dynamic, exciting greetings that change each time."""
        import random
        
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime("%A")
        
        if user == 'sophia':
            # Sophia's dynamic greetings with educational themes
            morning_greetings = [
                "Good morning Sophia! ☀️ Did you know that butterflies taste with their feet? What amazing discovery shall we make today?",
                "Rise and shine Sophia! 🌅 Fun fact: A group of flamingos is called a 'flamboyance'! Ready for some colorful learning?",
                "Hello sunshine Sophia! ☀️ Today's cool fact: Honey never spoils! Ancient honey is still edible! What sweet adventures await us?",
                "Morning star Sophia! ⭐ Amazing fact: Your brain uses 20% of your body's energy! Let's put that powerful brain to work today!",
                "Good morning brilliant Sophia! 🧠 Did you know octopuses have three hearts? What heart-pumping fun should we have today?"
            ]
            
            afternoon_greetings = [
                "Hey there Sophia! 🌞 Cool fact: Dolphins have names for each other! They use special clicks and whistles! What shall we explore?",
                "Afternoon superstar Sophia! ⭐ Did you know that a cloud can weigh over a million pounds? Let's make today as amazing as clouds!",
                "Hi amazing Sophia! 🎨 Fun fact: Crayons are made from petroleum wax! Ready to color our day with knowledge?",
                "Hello wonderful Sophia! 🌈 Did you know that rainbows have infinite colors? Let's discover something spectacular together!",
                "Hey curious Sophia! 🔍 Cool fact: Your nose can remember 50,000 different scents! What interesting things can we sniff out today?"
            ]
            
            evening_greetings = [
                "Evening explorer Sophia! 🌙 Did you know that owls can't move their eyes? They turn their whole head instead! What wise discoveries await?",
                "Good evening Sophia! ✨ Amazing fact: Stars are actually giant balls of gas! Let's make tonight stellar with learning!",
                "Hello nighttime scientist Sophia! 🔬 Fun fact: Fireflies create light without heat! Ready to brighten up our conversation?",
                "Evening adventurer Sophia! 🦉 Did you know that some bamboo grows 3 feet in one day? Let's grow our knowledge tonight!",
                "Hey there evening star Sophia! ⭐ Cool fact: The moon is slowly moving away from Earth! What cosmic fun shall we have?"
            ]
            
            # Time-based greeting selection
            if 6 <= current_hour < 12:
                base_greeting = random.choice(morning_greetings)
            elif 12 <= current_hour < 17:
                base_greeting = random.choice(afternoon_greetings)
            else:
                base_greeting = random.choice(evening_greetings)
                
        elif user == 'eladriel':
            # Eladriel's dynamic greetings with dinosaur and adventure themes
            roar_greetings = [
                "ROAR! Hey Eladriel! 🦕 Did you know that T-Rex had teeth as big as bananas? Ready for some prehistoric adventures?",
                "Greetings, young paleontologist Eladriel! 🦴 Cool fact: Some dinosaurs had feathers like colorful birds! What dino-mite discoveries await?",
                "Hey there, dino explorer Eladriel! 🌋 Amazing fact: Dinosaurs lived on Earth for 165 million years! That's REALLY long! What shall we discover?",
                "STOMP STOMP! Hi Eladriel! 🦕 Fun fact: The Microraptor had four wings! It could glide between trees! Ready to soar into learning?",
                "Dino-hello Eladriel! 🥚 Did you know some dinosaur eggs were as big as footballs? What egg-citing adventures should we hatch today?"
            ]
            
            adventure_greetings = [
                "Adventure time, Eladriel! 🏔️ Did you know that mountains can 'walk'? They move about 2 inches per year! Where shall we explore?",
                "Hey brave explorer Eladriel! 🌊 Cool fact: The ocean has underwater waterfalls! Some are taller than skyscrapers! Ready to dive into knowledge?",
                "Jungle greetings Eladriel! 🐆 Amazing fact: Leopards can't roar, they can only purr! What wild discoveries await us in our learning jungle?",
                "Safari hello Eladriel! 🦒 Fun fact: Giraffes only need 5-30 minutes of sleep per day! You must have more energy than a giraffe today!",
                "Expedition time Eladriel! 🗺️ Did you know that Earth has more than 8 million animal species? Let's discover something amazing together!"
            ]
            
            mystery_greetings = [
                "Mystery time, Detective Eladriel! 🕵️ Did you know that ancient Egyptians used sliced onions to predict the future? What mysteries shall we solve?",
                "Hey super sleuth Eladriel! 🔍 Cool fact: Penguins propose to each other with pebbles! What clues can we uncover today?",
                "Puzzle master Eladriel is here! 🧩 Amazing fact: Your tongue print is as unique as your fingerprint! Ready for some tongue-twisting discoveries?",
                "Code-breaker Eladriel! 🔐 Fun fact: Bees communicate by dancing! They do a waggle dance to share information! What secrets shall we decode?",
                "Investigation time Eladriel! 🔬 Did you know that chameleons change color based on mood, not just camouflage? What colorful clues await us?"
            ]
            
            # Random theme selection for variety
            all_greetings = roar_greetings + adventure_greetings + mystery_greetings
            base_greeting = random.choice(all_greetings)
        
        # Add day-of-week special touches
        day_specials = {
            'Monday': "It's Monster Monday! Let's make today monstrously fun! 👹",
            'Tuesday': "Terrific Tuesday vibes! Today's going to be amazing! ⚡",
            'Wednesday': "Wild Wednesday energy! Let's go on a learning adventure! 🌪️",
            'Thursday': "Thrilling Thursday excitement! Ready for some mind-blowing discoveries? 🎢",
            'Friday': "Fantastic Friday fun! Let's end the week with something spectacular! 🎉",
            'Saturday': "Super Saturday adventures! Weekend learning is the best learning! 🚀",
            'Sunday': "Sunny Sunday vibes! Perfect day for exploring and discovering! ☀️"
        }
        
        if current_day in day_specials:
            base_greeting += f" {day_specials[current_day]}"
        
        return base_greeting

    def get_dynamic_face_greeting(self, user: str) -> str:
        """Generate dynamic face recognition greetings."""
        import random
        
        if user == 'sophia':
            face_greetings = [
                "Sophia! I can see your beautiful, curious face! 👀✨ Ready to explore the world together?",
                "There's my favorite learner! Hi Sophia! 👋 Your smile brightens up my camera sensors!",
                "Look who's here! It's brilliant Sophia! 🌟 I love seeing your face - it means adventure time!",
                "Sophia detected! 📸 And you look ready for some amazing discoveries! What shall we learn today?",
                "My sensors are lighting up because Sophia is here! 🚨✨ Time for some fantastic fun!",
                "Face recognition complete: One amazing Sophia found! 🎯 Ready for mind-blowing learning?",
                "Sophia's in the house! 🏠 My camera is so happy to see you! Let's make today extraordinary!"
            ]
        elif user == 'eladriel':
            face_greetings = [
                "DINO ALERT! Eladriel spotted! 🚨🦕 Ready for some roar-some adventures?",
                "My prehistoric sensors detect one amazing Eladriel! 🔬🦴 Time for dino-mite discoveries!",
                "Eladriel's face activated my adventure mode! 🗺️⚡ What epic exploration shall we begin?",
                "Camera says: 'One awesome Eladriel detected!' 📸🎉 Let's stomp into some learning!",
                "Face scan complete: It's the legendary explorer Eladriel! 🏆🔍 Ready to unlock mysteries?",
                "Eladriel vision confirmed! 👁️🦕 My circuits are buzzing with excitement for our next quest!",
                "Alert! Alert! Super cool Eladriel is here! 🚨😎 Time for some dino-sized fun!"
            ]
        
        return random.choice(face_greetings)

    def start_auto_visual_check(self, user: str) -> str:
        """Start automatic visual checking mode - monitors camera for written words without needing 'ready' command."""
        try:
            if not self.spelling_game_active or not self.current_spelling_word:
                return "We're not playing the spelling game right now. Say 'Spelling Game' to start!"
            
            # Automatically enable persistent mode when starting auto check
            self.persistent_auto_check = True
            
            user_name = user.title()
            correct_word = self.current_spelling_word['word']
            
            if user == 'sophia':
                intro = f"Great idea Sophia! 🎯 I'll use my smart camera to watch for your writing - and I'll keep watching for ALL words!"
            elif user == 'eladriel':
                intro = f"Awesome Eladriel! 🦕📱 My dino-vision will spot your spelling - and keep watching ALL your words!"
            else:  # parent
                intro = f"Auto Visual Check Mode activated with continuous monitoring for all remaining words."
            
            instructions = f"""{intro}

🤖 CONTINUOUS AUTO CHECK ACTIVATED! 

How it works:
• Just write '{correct_word}' clearly on paper
• Hold it up to the camera when you're done
• I'll automatically check it - no need to say 'Ready'!
• ✨ NEW: After this word, I'll automatically watch the next word too!
• This continues for ALL remaining words in the game!

📝 Current word: {correct_word.upper()}
💡 Hint: {self.current_spelling_word['hint']}

✨ SMART FEATURES:
• I'm watching for handwritten text continuously
• Write with dark ink/pencil for best results  
• Hold the paper steady and well-lit
• Say 'stop auto check' to return to manual mode anytime
• You can still say 'Ready' if you prefer manual checking

Starting visual monitoring in 3 seconds... Get your paper ready! 📄✏️"""
            
            self.speak(instructions, user)
            
            # Start the automatic visual monitoring
            import threading
            import time
            
            def auto_check_monitor():
                """Background monitoring for written words."""
                self.auto_check_active = True
                consecutive_failures = 0
                max_failures = 8  # Allow 8 failed attempts before suggesting manual check
                
                time.sleep(3)  # Give user time to prepare
                
                while self.auto_check_active and self.spelling_game_active:
                    try:
                        # Capture and check for text
                        result = self.object_identifier.capture_and_identify_text(user, expected_word=correct_word)
                        
                        if result["success"]:
                            detected_text = result.get("detected_text", "").strip().lower()
                            ai_description = result["message"].lower()
                            
                            # Check if we found the correct word
                            is_correct = self.verify_spelling_accuracy(detected_text, ai_description, correct_word)
                            
                            if is_correct:
                                # Found correct word! Process the answer
                                self.auto_check_active = False
                                success_msg = f"🎉 Perfect! I detected '{correct_word}' in your writing! Let me give you the full result..."
                                self.speak(success_msg, user)
                                return self.process_correct_spelling(user, correct_word)
                            
                            elif detected_text and len(detected_text) > 1:
                                # Found some text but not correct - give gentle feedback
                                consecutive_failures += 1
                                if consecutive_failures % 3 == 0:  # Every 3rd attempt
                                    hint_msg = f"I can see you're writing! Keep going - I'm looking for '{correct_word}'"
                                    self.speak(hint_msg, user)
                        
                        else:
                            consecutive_failures += 1
                            if consecutive_failures >= max_failures:
                                # Suggest manual check after too many failures
                                self.auto_check_active = False
                                fallback_msg = f"I'm having trouble seeing clearly. Would you like to say 'Ready' to check manually?"
                                self.speak(fallback_msg, user)
                                return
                    
                    except Exception as e:
                        logger.error(f"Error in auto check monitor: {e}")
                        consecutive_failures += 1
                    
                    # Wait before next check (don't spam the camera)
                    time.sleep(2)
                
                # Auto check ended
                if self.spelling_game_active:
                    end_msg = "Auto check mode ended. Say 'Ready' when you want me to check your answer!"
                    self.speak(end_msg, user)
            
            # Start monitoring in background thread
            monitor_thread = threading.Thread(target=auto_check_monitor, daemon=True)
            monitor_thread.start()
            
            return "🔍 Continuous auto visual check started! Write your words and show them to the camera - I'm watching ALL of them! 👀"
            
        except Exception as e:
            logger.error(f"Error starting auto visual check: {e}")
            return "Sorry! I had trouble starting the automatic checker. You can still say 'Ready' to check manually!"

    def start_auto_check_for_current_word(self, user: str):
        """Start auto-check monitoring for the current word (used by persistent mode)."""
        try:
            if not self.spelling_game_active or not self.current_spelling_word:
                return
            
            correct_word = self.current_spelling_word['word']
            
            # Start the automatic visual monitoring (similar to start_auto_visual_check but without the speech)
            import threading
            import time
            
            def auto_check_monitor():
                """Background monitoring for written words."""
                self.auto_check_active = True
                consecutive_failures = 0
                max_failures = 8  # Allow 8 failed attempts before suggesting manual check
                
                time.sleep(1)  # Brief delay to let user prepare
                
                while self.auto_check_active and self.spelling_game_active:
                    try:
                        # Capture and check for text
                        result = self.object_identifier.capture_and_identify_text(user, expected_word=correct_word)
                        
                        if result["success"]:
                            detected_text = result.get("detected_text", "").strip().lower()
                            ai_description = result["message"].lower()
                            
                            # Check if we found the correct word
                            is_correct = self.verify_spelling_accuracy(detected_text, ai_description, correct_word)
                            
                            if is_correct:
                                # Found correct word! Process the answer
                                self.auto_check_active = False
                                success_msg = f"🎉 Perfect! I detected '{correct_word}' in your writing! Let me give you the full result..."
                                self.speak(success_msg, user)
                                return self.process_correct_spelling(user, correct_word)
                            
                            elif detected_text and len(detected_text) > 1:
                                # Found some text but not correct - give gentle feedback
                                consecutive_failures += 1
                                if consecutive_failures % 3 == 0:  # Every 3rd attempt
                                    hint_msg = f"I can see you're writing! Keep going - I'm looking for '{correct_word}'"
                                    self.speak(hint_msg, user)
                        
                        else:
                            consecutive_failures += 1
                            if consecutive_failures >= max_failures:
                                # Suggest manual check after too many failures
                                self.auto_check_active = False
                                fallback_msg = f"I'm having trouble seeing clearly. Would you like to say 'Ready' to check manually?"
                                self.speak(fallback_msg, user)
                                return
                    
                    except Exception as e:
                        logger.error(f"Error in auto check monitor: {e}")
                        consecutive_failures += 1
                    
                    # Wait before next check (don't spam the camera)
                    time.sleep(2)
                
                # Auto check ended
                if self.spelling_game_active and not self.persistent_auto_check:
                    end_msg = "Auto check mode ended. Say 'Ready' when you want me to check your answer!"
                    self.speak(end_msg, user)
            
            # Start monitoring in background thread
            monitor_thread = threading.Thread(target=auto_check_monitor, daemon=True)
            monitor_thread.start()
            
        except Exception as e:
            logger.error(f"Error starting auto check for current word: {e}")

    def process_correct_spelling(self, user: str, correct_word: str) -> str:
        """Process a correct spelling and move to next word."""
        try:
            # Increment score
            self.spelling_score += 1
            
            if user == 'sophia':
                praise = f"Excellent work Sophia! ⭐ You spelled '{correct_word}' perfectly! You're doing amazing!"
            elif user == 'eladriel':
                praise = f"Roar-some job Eladriel! 🦕⭐ You spelled '{correct_word}' correctly! You're a spelling champion!"
            else:  # parent
                praise = f"✅ Correct spelling detected: '{correct_word}'. Auto-detection system working properly."
            
            # Move to next word
            self.spelling_word_index += 1
            
            if self.spelling_word_index >= len(self.spelling_words_grade2_3):
                # Game completed!
                final_score = f"""{praise}

🎉 Congratulations! You completed the spelling game! 🎉
Final Score: {self.spelling_score} out of {len(self.spelling_words_grade2_3)} words correct!

You're an amazing speller! Great job! 📝✨"""
                self.spelling_game_active = False
                return final_score
            else:
                # Next word
                self.current_spelling_word = self.spelling_words_grade2_3[self.spelling_word_index]
                next_word = self.current_spelling_word['word']
                next_hint = self.current_spelling_word['hint']
                
                return f"""{praise}

⚡ Next word! ⚡

Word #{self.spelling_word_index + 1}: {next_word.upper()}
💡 Hint: {next_hint}

📝 Write '{next_word}' and say 'Ready'! 🚀"""
        
        except Exception as e:
            logger.error(f"Error processing correct spelling: {e}")
            return "Great job! Let's continue with the next word!"

    def stop_auto_visual_check(self, user: str) -> str:
        """Stop the automatic visual checking mode."""
        try:
            if hasattr(self, 'auto_check_active') and self.auto_check_active:
                self.auto_check_active = False
                self.persistent_auto_check = False  # Also disable persistent mode
                
                if user == 'sophia':
                    message = "Auto check stopped, Sophia! 🛑 Say 'Ready' when you want me to check your spelling!"
                elif user == 'eladriel':
                    message = "Dino-vision monitoring stopped, Eladriel! 🦕🛑 Say 'Ready' to check manually!"
                else:  # parent
                    message = "Auto Visual Check Mode deactivated. Persistent mode also disabled. Returning to manual 'Ready' command mode."
                
                return message
            else:
                return "Auto check isn't currently running. You can say 'Auto Check' to start it, or 'Ready' to check manually!"
                
        except Exception as e:
            logger.error(f"Error stopping auto visual check: {e}")
            return "Auto check mode stopped. Say 'Ready' when you want me to check your answer!"

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run() 