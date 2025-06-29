"""
Voice Activity Detection Module with Speaker Differentiation
Prevents AI from recognizing its own voice during listening sessions.
"""

import speech_recognition as sr
import logging
import time
import threading
import platform
import os
from typing import Optional, List, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

class VoiceActivityDetector:
    """Smart voice activity detection that can differentiate between AI and human speech."""
    
    def __init__(self, recognizer: sr.Recognizer):
        self.recognizer = recognizer
        self.ai_speaking = False  # Flag to track when AI is speaking
        self.platform_info = self._detect_platform()
        self.ai_speech_patterns = [
            # Common AI phrases that should be ignored
            "smile brightens up my camera sensors",
            "automatic conversation mode activated",
            "i'm listening",
            "say goodbye to end",
            "timeout after",
            "minute of silence",
            "camera sensors",
            "conversation mode",
            "listening for speech",
            "wonderful sophia",
            "hello sophia",
            "let me know",
            "i'm here to help",
            "just let me know",
            "here to help you",
            "what you're curious about",
            "have in mind",
            "you'd like to",
            "feel free to share",
            "dive into it together",
            "specific topic",
            "explore or learn",
            "how far is what",
            "sophia i'm here to help",
            "what you'd like to know",
            "distance of",
            "i'll do my best",
            "to assist you",
            "just let me know what",
            "assist you",
            "help you",
            "how far is what soph",
            "what sophia",
            "here to help just let me know what you",
            "brilliant sophia",
            "love seeing your face",
            "means adventure time",
            "look who's here",
            "it's brilliant sophia",
            "excellent work sophia",
            "you spelled",
            "perfectly",
            "you're doing amazing",
            "roar-some job",
            "correctly",
            "spelling champion",
            "great job",
            "try again",
            "wonderful",
            "fantastic",
            "keep going",
            "almost there",
        ]
        self.speaker_lock = threading.Lock()
        logger.info(f"🎤 Voice Activity Detector initialized for {self.platform_info['name']}")
    
    def _detect_platform(self) -> Dict[str, Any]:
        """Detect the current platform and return optimized settings."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Check if running on Raspberry Pi
        is_raspberry_pi = False
        pi_version = None
        
        try:
            if os.path.exists('/proc/device-tree/model'):
                with open('/proc/device-tree/model', 'r') as f:
                    model_info = f.read().strip()
                    if 'raspberry pi' in model_info.lower():
                        is_raspberry_pi = True
                        if 'pi 5' in model_info.lower() or '5 model' in model_info.lower():
                            pi_version = 5
                        elif 'pi 4' in model_info.lower() or '4 model' in model_info.lower():
                            pi_version = 4
                        else:
                            pi_version = 3  # Assume older Pi
        except:
            pass
        
        # Determine platform-specific settings
        if is_raspberry_pi:
            if pi_version == 5:
                return {
                    'name': f'Raspberry Pi {pi_version}',
                    'type': 'raspberry_pi_5',
                    'base_energy_threshold': 150,  # Lower for Pi 5 USB mics
                    'calibration_duration': 1.2,   # Longer calibration for Pi
                    'energy_multipliers': {
                        'normal': 1.0,      # 150 base
                        'spelling': 0.8,    # 120 - more sensitive for spelling
                        'filipino': 1.1,    # 165 - slightly higher for accents
                        'interrupt': 0.6    # 90 - very sensitive for interrupts
                    },
                    'chunk_duration_multiplier': 1.2,  # Slightly longer chunks for Pi
                    'silence_tolerance_multiplier': 1.3  # More forgiving silence
                }
            else:
                return {
                    'name': f'Raspberry Pi {pi_version or "Unknown"}',
                    'type': 'raspberry_pi_other',
                    'base_energy_threshold': 120,  # Even lower for older Pi
                    'calibration_duration': 1.0,
                    'energy_multipliers': {
                        'normal': 1.0,
                        'spelling': 0.7,
                        'filipino': 1.2,
                        'interrupt': 0.5
                    },
                    'chunk_duration_multiplier': 1.0,
                    'silence_tolerance_multiplier': 1.2
                }
        elif system == 'darwin':  # macOS
            return {
                'name': 'macOS',
                'type': 'macos',
                'base_energy_threshold': 300,  # Higher for macOS built-in mics
                'calibration_duration': 0.8,
                'energy_multipliers': {
                    'normal': 1.0,      # 300 base
                    'spelling': 0.83,   # 250
                    'filipino': 1.0,    # 300
                    'interrupt': 0.67   # 200
                },
                'chunk_duration_multiplier': 1.0,
                'silence_tolerance_multiplier': 1.0
            }
        elif system == 'linux':  # Generic Linux
            return {
                'name': 'Linux',
                'type': 'linux',
                'base_energy_threshold': 200,  # Middle ground
                'calibration_duration': 1.0,
                'energy_multipliers': {
                    'normal': 1.0,
                    'spelling': 0.75,
                    'filipino': 1.15,
                    'interrupt': 0.6
                },
                'chunk_duration_multiplier': 1.1,
                'silence_tolerance_multiplier': 1.1
            }
        else:  # Windows or other
            return {
                'name': system.title(),
                'type': 'other',
                'base_energy_threshold': 250,
                'calibration_duration': 0.8,
                'energy_multipliers': {
                    'normal': 1.0,
                    'spelling': 0.8,
                    'filipino': 1.1,
                    'interrupt': 0.65
                },
                'chunk_duration_multiplier': 1.0,
                'silence_tolerance_multiplier': 1.0
            }
    
    def _get_optimal_thresholds(self, game_mode: str = None) -> Dict[str, Any]:
        """Get platform-optimized energy thresholds and timing settings."""
        base_threshold = self.platform_info['base_energy_threshold']
        multipliers = self.platform_info['energy_multipliers']
        
        mode = game_mode or 'normal'
        multiplier = multipliers.get(mode, multipliers['normal'])
        
        optimal_threshold = int(base_threshold * multiplier)
        
        return {
            'energy_threshold': optimal_threshold,
            'calibration_duration': self.platform_info['calibration_duration'],
            'chunk_duration_base': 0.5 * self.platform_info['chunk_duration_multiplier'],
            'silence_tolerance_base': 1.0 * self.platform_info['silence_tolerance_multiplier']
        }

    def set_ai_speaking(self, speaking: bool):
        """Set the AI speaking flag to prevent self-recognition."""
        with self.speaker_lock:
            self.ai_speaking = speaking
            if speaking:
                logger.info("🔇 AI is speaking - voice detection paused")
            else:
                logger.info("🎤 AI finished speaking - voice detection active")
    
    def is_ai_speech(self, text: str) -> bool:
        """Check if the recognized text is likely from the AI itself."""
        if not text:
            return False
        
        text_lower = text.lower().strip()
        
        # Check against known AI speech patterns
        for pattern in self.ai_speech_patterns:
            if pattern in text_lower:
                logger.warning(f"🤖 Detected AI's own speech: '{text}' (matched: '{pattern}')")
                return True
        
        # Check for very long responses (typically AI)
        if len(text.split()) > 15:
            logger.warning(f"🤖 Detected long response (likely AI): '{text[:50]}...'")
            return True
        
        return False
    
    def listen_with_speaker_detection(self, 
                                    timeout: int = 15,
                                    silence_threshold: float = 1.0,
                                    max_total_time: int = 30,
                                    game_mode: str = None) -> Optional[str]:
        """
        Listen for human speech while ignoring AI's own voice.
        
        Args:
            timeout: Maximum time to wait for first speech
            silence_threshold: Seconds of silence to wait after speech ends
            max_total_time: Maximum total listening time
            game_mode: 'spelling', 'filipino', 'interrupt', or None for optimization
        
        Returns:
            Recognized human speech text or None
        """
        
        try:
            with sr.Microphone() as source:
                logger.info(f"🎤 Smart Voice Detection ({self.platform_info['name']}): Listening for human speech only...")
                
                # Get platform-optimized settings
                settings = self._get_optimal_thresholds(game_mode)
                
                # Enhanced microphone calibration with platform-specific duration
                calibration_duration = settings['calibration_duration']
                self.recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logger.info(f"🎯 Calibrated for {calibration_duration}s on {self.platform_info['name']}")
                
                # Set platform-optimized energy threshold
                optimal_threshold = settings['energy_threshold']
                self.recognizer.energy_threshold = max(optimal_threshold, self.recognizer.energy_threshold * 0.8)
                
                logger.info(f"🎚️ Energy threshold set to {self.recognizer.energy_threshold} (optimized for {self.platform_info['name']} {game_mode or 'normal'} mode)")
                
                # Configure timing based on game mode and platform
                if game_mode == 'spelling':
                    chunk_duration = settings['chunk_duration_base'] * 0.6  # Faster for spelling
                    min_silence_gap = 0.2
                elif game_mode == 'filipino':
                    chunk_duration = settings['chunk_duration_base'] * 0.8  # Medium speed
                    min_silence_gap = 0.3
                elif game_mode == 'interrupt':
                    chunk_duration = settings['chunk_duration_base'] * 0.2  # Ultra-fast
                    min_silence_gap = 0.1
                else:
                    # NORMAL MODE - OPTIMIZED FOR COMPLETE SPEECH CAPTURE
                    chunk_duration = settings['chunk_duration_base']
                    min_silence_gap = 0.4
                
                # Apply platform-specific silence tolerance
                silence_threshold = silence_threshold * settings['silence_tolerance_base']
                
                self.recognizer.dynamic_energy_threshold = True
                
                # Voice activity detection with improved continuous speech handling
                audio_chunks = []
                total_listening_time = 0
                consecutive_silence_time = 0
                human_speech_detected = False
                recent_ai_speech = False
                last_speech_time = 0
                
                logger.info(f"👂 Listening for human speech (max {max_total_time}s, silence tolerance: {silence_threshold:.1f}s)...")
                
                while total_listening_time < max_total_time:
                    # Check if AI started speaking (should stop listening)
                    if self.ai_speaking:
                        logger.info("🔇 AI started speaking - stopping voice detection")
                        break
                    
                    try:
                        # Listen for a chunk with longer phrase limit for complete thoughts
                        chunk_audio = self.recognizer.listen(
                            source, 
                            timeout=chunk_duration, 
                            phrase_time_limit=min(4.0, chunk_duration * 8)  # Allow longer phrases for complete thoughts
                        )
                        
                        # Quick speech test for this chunk
                        try:
                            test_text = self.recognizer.recognize_google(chunk_audio, language='en-US')
                            
                            if test_text.strip():
                                # Check if this is AI's own voice
                                if self.is_ai_speech(test_text):
                                    logger.info(f"🤖 Ignored AI speech: '{test_text[:30]}...'")
                                    consecutive_silence_time += chunk_duration
                                    recent_ai_speech = True
                                else:
                                    # This is human speech!
                                    current_time = total_listening_time
                                    
                                    # If this speech is close to previous speech, it's likely continuation
                                    if human_speech_detected and (current_time - last_speech_time) < (silence_threshold * 0.8):
                                        logger.info(f"👤 Continuing human speech: '{test_text[:30]}...'")
                                    else:
                                        logger.info(f"👤 Human speech detected: '{test_text[:30]}...'")
                                    
                                    audio_chunks.append(chunk_audio)
                                    consecutive_silence_time = 0
                                    human_speech_detected = True
                                    recent_ai_speech = False
                                    last_speech_time = current_time
                            else:
                                consecutive_silence_time += chunk_duration
                                
                        except (sr.UnknownValueError, sr.RequestError):
                            # No recognizable speech in this chunk
                            consecutive_silence_time += chunk_duration
                            if human_speech_detected and consecutive_silence_time >= min_silence_gap:
                                # Only log silence if we've detected speech and had a meaningful gap
                                if consecutive_silence_time % 0.6 == 0:  # Log every 0.6 seconds to avoid spam
                                    logger.info(f"🔇 Silence: {consecutive_silence_time:.1f}s of {silence_threshold}s")
                        
                        total_listening_time += chunk_duration
                        
                        # Stop if we have enough silence after detecting human speech
                        # But be more generous with silence tolerance for natural speech
                        if consecutive_silence_time >= silence_threshold and human_speech_detected:
                            # Check if the last detected speech seems incomplete
                            if audio_chunks:
                                try:
                                    # Quick check of the last chunk to see if sentence seems incomplete
                                    last_chunk = audio_chunks[-1]
                                    test_text = self.recognizer.recognize_google(last_chunk, language='en-US')
                                    
                                    # Common incomplete patterns
                                    incomplete_patterns = [
                                        "what is the", "how do you", "where is the", "when did the",
                                        "why do", "who is", "which one", "how far is", "what are the",
                                        "tell me about", "what about", "how about", "what if",
                                        "can you", "could you", "would you", "will you"
                                    ]
                                    
                                    test_lower = test_text.lower().strip()
                                    is_incomplete = any(test_lower.endswith(pattern) for pattern in incomplete_patterns)
                                    
                                    if is_incomplete and consecutive_silence_time < (silence_threshold * 2):
                                        logger.info(f"🔄 Detected incomplete sentence: '{test_text}' - waiting for completion...")
                                        consecutive_silence_time = 0  # Reset to wait for more speech
                                        continue
                                        
                                except (sr.UnknownValueError, sr.RequestError):
                                    pass  # Continue with normal processing
                            
                            logger.info(f"✅ Human finished speaking! Processing {len(audio_chunks)} chunks...")
                            break
                            
                    except sr.WaitTimeoutError:
                        # Silence in this chunk
                        consecutive_silence_time += chunk_duration
                        total_listening_time += chunk_duration
                        
                        # Only log meaningful silence periods
                        if human_speech_detected and consecutive_silence_time >= min_silence_gap:
                            if int(consecutive_silence_time * 10) % 6 == 0:  # Log every 0.6 seconds
                                logger.info(f"🔇 Silence: {consecutive_silence_time:.1f}s of {silence_threshold}s")
                        
                        # Stop if enough silence after human speech
                        if consecutive_silence_time >= silence_threshold and human_speech_detected:
                            logger.info("✅ Human finished speaking! Processing collected audio...")
                            break
                
                # Process collected human speech
                if not audio_chunks:
                    logger.info("👤 No human speech detected")
                    return None
                
                return self._process_audio_chunks(audio_chunks, game_mode)
                
        except Exception as e:
            logger.error(f"Voice detection error: {e}")
            return None
    
    def _process_audio_chunks(self, audio_chunks: List[sr.AudioData], game_mode: str = None) -> Optional[str]:
        """Process and combine audio chunks into final text with improved sentence reconstruction."""
        try:
            logger.info(f"🎵 Processing {len(audio_chunks)} human speech chunks...")
            
            # Strategy 1: Try to combine all chunks into one audio stream for complete recognition
            combined_audio_data = b''
            sample_rate = audio_chunks[0].sample_rate
            sample_width = audio_chunks[0].sample_width
            
            for chunk in audio_chunks:
                combined_audio_data += chunk.get_raw_data()
            
            # Create combined audio object
            combined_audio = sr.AudioData(combined_audio_data, sample_rate, sample_width)
            
            # Strategy 2: Also process chunks individually and combine text intelligently
            individual_texts = []
            
            # Try combined audio first (best for continuous speech)
            for attempt in range(3):
                try:
                    # Choose language based on game mode
                    if game_mode == 'filipino':
                        try:
                            combined_text = self.recognizer.recognize_google(combined_audio, language='fil-PH')
                            logger.info(f"✅ Combined human speech (Filipino, attempt {attempt + 1}): '{combined_text}'")
                            return self._clean_text(combined_text)
                        except (sr.UnknownValueError, sr.RequestError):
                            combined_text = self.recognizer.recognize_google(combined_audio, language='en-US')
                            logger.info(f"✅ Combined human speech (English fallback, attempt {attempt + 1}): '{combined_text}'")
                            return self._clean_text(combined_text)
                    else:
                        # English recognition with multiple dialect attempts
                        languages = ['en-US', 'en-GB', 'en-AU']
                        for lang in languages:
                            try:
                                combined_text = self.recognizer.recognize_google(combined_audio, language=lang)
                                logger.info(f"✅ Combined human speech ({lang}, attempt {attempt + 1}): '{combined_text}'")
                                return self._clean_text(combined_text)
                            except (sr.UnknownValueError, sr.RequestError):
                                continue
                        
                except Exception as e:
                    if attempt < 2:
                        logger.warning(f"Combined recognition attempt {attempt + 1} failed: {e}")
                        time.sleep(0.2)
                        continue
                    else:
                        logger.info("Combined audio recognition failed, trying individual chunks...")
                        break
            
            # Fallback: Process individual chunks and intelligently combine
            logger.info("🔗 Using individual chunk processing and smart combination...")
            
            for i, chunk in enumerate(audio_chunks):
                try:
                    chunk_text = self.recognizer.recognize_google(chunk, language='en-US')
                    if chunk_text.strip():
                        individual_texts.append(chunk_text.strip())
                        logger.info(f"📝 Chunk {i+1}: '{chunk_text}'")
                except (sr.UnknownValueError, sr.RequestError):
                    continue
            
            if individual_texts:
                # Intelligent text combination
                final_text = self._combine_text_chunks(individual_texts)
                logger.info(f"🎯 Final combined speech: '{final_text}'")
                return self._clean_text(final_text)
            
            logger.info("❌ Could not process any speech chunks")
            return None
                
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return None

    def _combine_text_chunks(self, texts: List[str]) -> str:
        """Intelligently combine text chunks into coherent sentences."""
        if not texts:
            return ""
        
        if len(texts) == 1:
            return texts[0]
        
        # Join chunks with spaces and clean up
        combined = " ".join(texts)
        
        # Clean up common issues from chunk combination
        combined = combined.replace("  ", " ")  # Remove double spaces
        combined = combined.strip()
        
        # Handle common speech recognition artifacts in multi-chunk scenarios
        word_fixes = {
            "between pampang and": "between pampanga and",
            "in australia": "and australia",
            "what is the distance": "what is the distance",
            "how far is": "how far is",
            "what's the": "what's the",
        }
        
        combined_lower = combined.lower()
        for wrong, correct in word_fixes.items():
            if wrong in combined_lower:
                # Preserve original case while fixing
                combined = combined.replace(wrong, correct)
                combined = combined.replace(wrong.title(), correct.title())
                combined = combined.replace(wrong.upper(), correct.upper())
        
        return combined
    
    def _clean_text(self, text: str) -> str:
        """Clean recognized text."""
        if not text:
            return text
        
        cleaned = text.strip()
        
        # Common fixes
        common_fixes = {
            "filipina": "filipino",
            "philipino": "filipino", 
            "philippino": "filipino",
            "tagalog": "filipino",
            "ready ready": "ready",
            "done done": "done",
        }
        
        for wrong, correct in common_fixes.items():
            cleaned = cleaned.replace(wrong, correct)
        
        return ' '.join(cleaned.split()) 