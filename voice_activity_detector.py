"""
Voice Activity Detection Module with Speaker Differentiation
Prevents AI from recognizing its own voice during listening sessions.
"""

import speech_recognition as sr
import logging
import time
import threading
from typing import Optional, List, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

class VoiceActivityDetector:
    """Smart voice activity detection that can differentiate between AI and human speech."""
    
    def __init__(self, recognizer: sr.Recognizer):
        self.recognizer = recognizer
        self.ai_speaking = False  # Flag to track when AI is speaking
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
                logger.info("🎤 Smart Voice Detection: Listening for human speech only...")
                
                # Enhanced microphone calibration
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                
                # Configure sensitivity based on game mode
                if game_mode == 'spelling':
                    self.recognizer.energy_threshold = max(200, self.recognizer.energy_threshold * 0.6)
                    chunk_duration = 0.8  # Longer chunks for better word capture
                    min_silence_gap = 0.3  # Shorter silence gap tolerance
                elif game_mode == 'filipino':
                    self.recognizer.energy_threshold = max(250, self.recognizer.energy_threshold * 0.7)
                    chunk_duration = 1.0  # Longer chunks for Filipino phrases
                    min_silence_gap = 0.4
                elif game_mode == 'interrupt':
                    self.recognizer.energy_threshold = max(400, self.recognizer.energy_threshold * 0.9)
                    chunk_duration = 0.2  # Very short chunks for quick interrupts
                    min_silence_gap = 0.1
                else:
                    self.recognizer.energy_threshold = max(300, self.recognizer.energy_threshold * 0.8)
                    chunk_duration = 1.2  # Much longer chunks for complete sentences
                    min_silence_gap = 0.5  # Allow brief pauses in natural speech
                
                self.recognizer.dynamic_energy_threshold = True
                
                # Voice activity detection with improved continuous speech handling
                audio_chunks = []
                total_listening_time = 0
                consecutive_silence_time = 0
                human_speech_detected = False
                recent_ai_speech = False
                last_speech_time = 0
                
                logger.info(f"👂 Listening for human speech (max {max_total_time}s)...")
                
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
                            phrase_time_limit=min(8.0, chunk_duration * 3)  # Allow much longer phrases
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