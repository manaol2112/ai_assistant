"""
Audio utilities for AI Assistant
Handles speech recognition and audio processing with premium OpenAI TTS
"""

import pyaudio
import speech_recognition as sr
import logging
from typing import Optional, Tuple
import numpy as np
import pyttsx3
import openai
import io
import pygame
import tempfile
import os
from pathlib import Path
import threading
import time


class OpenAITTSEngine:
    """Premium OpenAI Text-to-Speech Engine with natural human-like voices."""
    
    def __init__(self, openai_client: openai.OpenAI, voice: str = "nova", model: str = "tts-1-hd"):
        """
        Initialize OpenAI TTS Engine
        
        Args:
            openai_client: OpenAI client instance
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: TTS model (tts-1 for speed, tts-1-hd for quality)
        """
        self.client = openai_client
        self.voice = voice
        self.model = model
        self.rate = 1.0  # Speech rate (0.25 to 4.0)
        self.volume = 1.0
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"OpenAI TTS Engine initialized with voice: {voice}")
    
    def say(self, text: str):
        """Convert text to speech and play it with retry logic."""
        max_retries = 2
        base_timeout = 15.0
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    self.logger.info(f"OpenAI TTS: Retry attempt {attempt + 1}/{max_retries}")
                
                self.logger.info(f"OpenAI TTS: Starting to process text: '{text[:50]}...'")
                
                # Generate speech using OpenAI TTS with progressive timeout
                self.logger.info("OpenAI TTS: Calling API...")
                
                # Progressive timeout: 15s, then 25s
                current_timeout = base_timeout + (attempt * 10)
                
                # Add timeout to the OpenAI API call
                response = None
                api_error = None
                
                def api_call():
                    nonlocal response, api_error
                    try:
                        response = self.client.audio.speech.create(
                            model=self.model,
                            voice=self.voice,
                            input=text,
                            speed=self.rate
                        )
                    except Exception as e:
                        api_error = e
                
                # Start API call in separate thread with timeout
                api_thread = threading.Thread(target=api_call)
                api_thread.daemon = True
                api_thread.start()
                
                # Wait for API call to complete with progressive timeout
                api_thread.join(timeout=current_timeout)
                
                if api_thread.is_alive():
                    self.logger.error(f"OpenAI TTS: API call timed out after {current_timeout} seconds (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        self.logger.info("OpenAI TTS: Retrying with longer timeout...")
                        time.sleep(1)  # Brief pause before retry
                        continue
                    else:
                        self.logger.error(f"OpenAI TTS: All retry attempts failed for text: '{text[:50]}...'")
                        print(f"🔇 TTS TIMEOUT - Message was: {text}")
                        return
                
                if api_error:
                    self.logger.error(f"OpenAI TTS: API call failed: {api_error} (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        self.logger.info("OpenAI TTS: Retrying after API error...")
                        time.sleep(2)  # Longer pause after API error
                        continue
                    else:
                        self.logger.error(f"OpenAI TTS: All retry attempts failed for text: '{text[:50]}...'")
                        print(f"🔇 TTS FAILED - Message was: {text}")
                        return
                
                if not response:
                    self.logger.error(f"OpenAI TTS: API call returned no response (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        self.logger.info("OpenAI TTS: Retrying after no response...")
                        time.sleep(1)
                        continue
                    else:
                        self.logger.error(f"OpenAI TTS: All retry attempts failed for text: '{text[:50]}...'")
                        print(f"🔇 TTS NO RESPONSE - Message was: {text}")
                        return
                    
                # Success! Process the audio
                self.logger.info(f"OpenAI TTS: API call successful on attempt {attempt + 1}, processing audio...")
                break  # Exit retry loop on success
                
            except Exception as e:
                self.logger.error(f"OpenAI TTS error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    self.logger.info("OpenAI TTS: Retrying after exception...")
                    time.sleep(1)
                    continue
                else:
                    self.logger.error(f"OpenAI TTS: All retry attempts failed for text: '{text[:50]}...'")
                    print(f"🔇 TTS ERROR - Message was: {text}")
                    return
        
        # Process the successful audio response
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            
            self.logger.info(f"OpenAI TTS: Audio file created: {temp_file_path}")
            
            try:
                # Play the audio using pygame
                self.logger.info("OpenAI TTS: Loading audio into pygame...")
                pygame.mixer.music.load(temp_file_path)
                pygame.mixer.music.set_volume(self.volume)
                
                self.logger.info("OpenAI TTS: Starting audio playback...")
                pygame.mixer.music.play()
                
                # Wait for playback to complete with timeout
                timeout_counter = 0
                max_timeout = 45  # Increased max timeout for longer messages
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                    timeout_counter += 0.1
                    if timeout_counter > max_timeout:
                        self.logger.warning("OpenAI TTS: Playback timeout, stopping...")
                        pygame.mixer.music.stop()
                        break
                
                self.logger.info("OpenAI TTS: Playback completed successfully")
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                    self.logger.info("OpenAI TTS: Temporary file cleaned up")
                except Exception as cleanup_error:
                    self.logger.warning(f"OpenAI TTS: Could not clean up temp file: {cleanup_error}")
                    
        except Exception as audio_error:
            self.logger.error(f"OpenAI TTS: Audio processing error: {audio_error}")
            print(f"🔇 TTS AUDIO ERROR - Message was: {text}")
    
    def runAndWait(self):
        """Compatibility method for pyttsx3 interface."""
        pass  # Audio is played synchronously in say() method
    
    def setProperty(self, name: str, value):
        """Set TTS properties."""
        if name == 'rate':
            # Convert pyttsx3 rate (words per minute) to OpenAI speed (0.25-4.0)
            self.rate = max(0.25, min(4.0, value / 200.0))
        elif name == 'volume':
            self.volume = max(0.0, min(1.0, value))
        elif name == 'voice':
            # Map to OpenAI voice names
            voice_mapping = {
                'alloy': 'alloy',
                'echo': 'echo', 
                'fable': 'fable',
                'onyx': 'onyx',
                'nova': 'nova',
                'shimmer': 'shimmer'
            }
            if value.lower() in voice_mapping:
                self.voice = voice_mapping[value.lower()]
    
    def stop(self):
        """Stop current speech."""
        try:
            pygame.mixer.music.stop()
        except:
            pass


class AudioManager:
    """Manages audio input/output operations for the AI Assistant."""
    
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        """Initialize audio manager with specified parameters."""
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        self.channels = 1
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Configure recognizer for better performance
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.operation_timeout = None
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("AudioManager initialized")

    def get_microphone_info(self) -> dict:
        """Get information about available microphones."""
        info = {"default_mic": None, "available_mics": []}
        
        try:
            # Get default input device
            default_info = self.audio.get_default_input_device_info()
            info["default_mic"] = {
                "name": default_info["name"],
                "index": default_info["index"],
                "channels": default_info["maxInputChannels"],
                "sample_rate": default_info["defaultSampleRate"]
            }
            
            # Get all available microphones
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info["maxInputChannels"] > 0:
                    info["available_mics"].append({
                        "name": device_info["name"],
                        "index": i,
                        "channels": device_info["maxInputChannels"],
                        "sample_rate": device_info["defaultSampleRate"]
                    })
        except Exception as e:
            self.logger.error(f"Error getting microphone info: {e}")
        
        return info

    def test_microphone(self) -> bool:
        """Test if microphone is working properly."""
        try:
            with sr.Microphone() as source:
                self.logger.info("Testing microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.logger.info("Microphone test successful")
                return True
        except Exception as e:
            self.logger.error(f"Microphone test failed: {e}")
            return False

    def calibrate_audio(self, duration: float = 2.0):
        """Calibrate audio settings for ambient noise."""
        try:
            with sr.Microphone() as source:
                self.logger.info(f"Calibrating for ambient noise ({duration}s)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                self.logger.info(f"Audio calibrated. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            self.logger.error(f"Audio calibration failed: {e}")

    def listen_for_audio(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[sr.AudioData]:
        """Listen for audio input from microphone."""
        try:
            with sr.Microphone() as source:
                # Quick ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                return audio
        except sr.WaitTimeoutError:
            self.logger.debug("Audio listening timeout")
            return None
        except Exception as e:
            self.logger.error(f"Error listening for audio: {e}")
            return None

    def audio_to_text(self, audio_data: sr.AudioData) -> Optional[str]:
        """Convert audio data to text using Google Speech Recognition."""
        try:
            text = self.recognizer.recognize_google(audio_data)
            self.logger.info(f"Speech recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Speech recognition error: {e}")
            return None

    def get_audio_level(self, duration: float = 0.1) -> float:
        """Get current audio input level for wake word detection."""
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            frames_to_record = int(self.sample_rate * duration / self.chunk_size)
            audio_data = []
            
            for _ in range(frames_to_record):
                data = stream.read(self.chunk_size)
                audio_data.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Convert to numpy array and calculate RMS
            audio_np = np.frombuffer(b''.join(audio_data), dtype=np.int16)
            rms = np.sqrt(np.mean(audio_np.astype(np.float64)**2))
            
            return rms
        except Exception as e:
            self.logger.error(f"Error getting audio level: {e}")
            return 0.0

    def cleanup(self):
        """Clean up audio resources."""
        try:
            self.audio.terminate()
            pygame.mixer.quit()
            self.logger.info("Audio resources cleaned up")
        except Exception as e:
            self.logger.error(f"Error cleaning up audio resources: {e}")

    def __del__(self):
        """Destructor to ensure cleanup."""
        self.cleanup()


def setup_premium_tts_engines(client):
    """Setup premium OpenAI TTS engines with natural human voices for each user."""
    
    logger = logging.getLogger(__name__)
    
    # Sophia's voice - soft, encouraging, and supportive (feminine)
    sophia_tts = OpenAITTSEngine(client, voice="nova")  # Nova: reliable and friendly
    logger.info("✨ Sophia's premium voice (Nova) initialized - soft and encouraging")
    
    # Eladriel's voice - energetic, playful, and adventurous (masculine for a boy)
    eladriel_tts = OpenAITTSEngine(client, voice="alloy")  # Alloy: reliable and energetic
    logger.info("🦕 Eladriel's premium voice (Alloy) initialized - energetic and reliable")
    
    return sophia_tts, eladriel_tts


def setup_tts_engines() -> tuple[pyttsx3.Engine, pyttsx3.Engine]:
    """
    Legacy function for backward compatibility.
    This will be replaced by setup_premium_tts_engines in main.py
    """
    # Sophia's engine (friendly, warm voice)
    sophia_engine = pyttsx3.init()
    
    # Get all voices and find English ones
    voices = sophia_engine.getProperty('voices')
    english_voices = []
    
    for voice in voices:
        # Check for English voices
        if 'en' in voice.id.lower() or 'english' in voice.name.lower():
            english_voices.append(voice)
    
    # Set kid-friendly voice for Sophia (prefer voices that sound younger/warmer)
    preferred_sophia_voices = ['karen', 'victoria', 'samantha', 'alice', 'susan']
    sophia_voice = None
    
    for preferred in preferred_sophia_voices:
        for voice in english_voices:
            if preferred.lower() in voice.name.lower():
                sophia_voice = voice
                break
        if sophia_voice:
            break
    
    # Fallback to first English voice if preferred not found
    if not sophia_voice and english_voices:
        sophia_voice = english_voices[0]
    
    if sophia_voice:
        sophia_engine.setProperty('voice', sophia_voice.id)
        logging.info(f"Sophia voice set to: {sophia_voice.name} (kid-friendly)")
    
    # Configure Sophia's voice properties for kids
    sophia_engine.setProperty('rate', 175)  # Slightly slower for clarity
    sophia_engine.setProperty('volume', 0.95)
    
    # Eladriel's engine (playful, energetic voice)
    eladriel_engine = pyttsx3.init()
    
    # Set kid-friendly voice for Eladriel (prefer different, more playful voices)
    preferred_eladriel_voices = ['fiona', 'alex', 'fred', 'daniel', 'tom']
    eladriel_voice = None
    
    for preferred in preferred_eladriel_voices:
        for voice in english_voices:
            if preferred.lower() in voice.name.lower():
                eladriel_voice = voice
                break
        if eladriel_voice:
            break
    
    # Fallback to second English voice if preferred not found
    if not eladriel_voice and len(english_voices) > 1:
        eladriel_voice = english_voices[1]
    elif not eladriel_voice and english_voices:
        eladriel_voice = english_voices[0]
    
    if eladriel_voice:
        eladriel_engine.setProperty('voice', eladriel_voice.id)
        logging.info(f"Eladriel voice set to: {eladriel_voice.name} (kid-friendly)")
    
    # Configure Eladriel's voice properties for kids
    eladriel_engine.setProperty('rate', 185)  # Slightly faster, more energetic
    eladriel_engine.setProperty('volume', 0.95)
    
    return sophia_engine, eladriel_engine 