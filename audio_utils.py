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
import platform


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
    
    def __init__(self, sample_rate: int = None, chunk_size: int = None):
        """Initialize audio manager with platform-optimized settings."""
        # Get platform-optimized settings
        platform_settings = self._get_platform_audio_settings()
        
        self.sample_rate = sample_rate or platform_settings['sample_rate']
        self.chunk_size = chunk_size or platform_settings['chunk_size']
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Store platform info for later use
        self.platform_info = {
            'name': platform_settings['platform_name'],
            'sample_rate': self.sample_rate,
            'chunk_size': self.chunk_size
        }
        
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        
        # Initialize pygame mixer for sound effects
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Configure recognizer with platform-optimized settings
        self.energy_threshold = platform_settings['energy_threshold']
        self.recognizer.dynamic_energy_threshold = platform_settings['dynamic_energy_threshold']
        self.recognizer.pause_threshold = platform_settings['pause_threshold']
        self.recognizer.operation_timeout = None
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"AudioManager initialized with sample_rate={self.sample_rate}Hz, energy_threshold={self.energy_threshold} for {self._get_platform_name()}")

    def _get_platform_audio_settings(self) -> dict:
        """Get platform-optimized audio settings including sample rate and thresholds."""
        system = platform.system().lower()
        
        # Check if running on Raspberry Pi
        is_raspberry_pi = False
        pi_version = None
        
        if os.path.exists('/proc/device-tree/model'):
            try:
                with open('/proc/device-tree/model', 'r') as f:
                    model_info = f.read().strip()
                    if 'raspberry pi' in model_info.lower():
                        is_raspberry_pi = True
                        if 'pi 5' in model_info.lower() or '5 model' in model_info.lower():
                            pi_version = 5
                        elif 'pi 4' in model_info.lower() or '4 model' in model_info.lower():
                            pi_version = 4
                        else:
                            pi_version = 3
            except:
                pass
        
        # Return platform-specific settings
        if is_raspberry_pi and pi_version == 5:
            # Waveshare USB Audio optimized settings for Pi 5
            return {
                'sample_rate': 44100,  # Waveshare supports 44100Hz perfectly
                'chunk_size': 4096,    # Large buffer for stability
                'energy_threshold': 200,  # Higher threshold for quality USB mics
                'dynamic_energy_threshold': False,  # Disable for consistent performance
                'pause_threshold': 0.8,
                'platform_name': 'Raspberry Pi 5 (Waveshare USB Audio)'
            }
        elif is_raspberry_pi:
            # Other Pi models
            return {
                'sample_rate': 16000,
                'chunk_size': 2048,
                'energy_threshold': 120,
                'dynamic_energy_threshold': True,
                'pause_threshold': 0.8,
                'platform_name': f'Raspberry Pi {pi_version or "Unknown"}'
            }
        elif system == 'darwin':  # macOS
            return {
                'sample_rate': 16000,
                'chunk_size': 1024,
                'energy_threshold': 300,
                'dynamic_energy_threshold': True,
                'pause_threshold': 0.8,
                'platform_name': 'macOS'
            }
        else:  # Linux, Windows, other
            return {
                'sample_rate': 16000,
                'chunk_size': 1024,
                'energy_threshold': 250,
                'dynamic_energy_threshold': True,
                'pause_threshold': 0.8,
                'platform_name': system.title()
            }

    def _get_platform_name(self) -> str:
        """Get platform name for logging."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Check if running on Raspberry Pi
        if os.path.exists('/proc/device-tree/model'):
            try:
                with open('/proc/device-tree/model', 'r') as f:
                    model_info = f.read().strip()
                    if 'raspberry pi' in model_info.lower():
                        if 'pi 5' in model_info.lower() or '5 model' in model_info.lower():
                            return 'Raspberry Pi 5'
                        elif 'pi 4' in model_info.lower() or '4 model' in model_info.lower():
                            return 'Raspberry Pi 4'
                        else:
                            return 'Raspberry Pi (older)'
            except:
                pass
        
        if system == 'darwin':
            return 'macOS'
        elif system == 'linux':
            return 'Linux'
        elif system == 'windows':
            return 'Windows'
        else:
            return system.title()
    
    @property
    def energy_threshold(self) -> float:
        """Get the current energy threshold."""
        return getattr(self, '_energy_threshold', self.recognizer.energy_threshold)
    
    @energy_threshold.setter
    def energy_threshold(self, value: float):
        """Set the energy threshold for both internal tracking and recognizer."""
        self._energy_threshold = value
        self.recognizer.energy_threshold = value

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
            # Get the best microphone device for this platform
            mic_device_index = self._get_best_microphone_device()
            
            # Use platform-optimized microphone settings with specific device
            with sr.Microphone(
                device_index=mic_device_index,
                sample_rate=self.sample_rate, 
                chunk_size=self.chunk_size
            ) as source:
                self.logger.info(f"Testing microphone (device index: {mic_device_index})...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.logger.info("Microphone test successful")
                return True
        except Exception as e:
            self.logger.error(f"Microphone test failed: {e}")
            return False

    def _get_best_microphone_device(self) -> Optional[int]:
        """Get the best microphone device for the current platform with ALSA error handling."""
        try:
            # Get all microphones with error handling
            try:
                mic_list = sr.Microphone.list_microphone_names()
                self.logger.info(f"🎤 Available microphones: {mic_list}")
            except Exception as list_error:
                self.logger.error(f"🎤 Failed to list microphones: {list_error}")
                return None
            
            # Raspberry Pi specific: Handle ALSA errors gracefully
            if 'Raspberry Pi' in self.platform_info['name']:
                self.logger.info("🍓 Raspberry Pi detected - using ALSA-compatible audio settings")
                
                # Try USB audio devices first (more reliable on Pi)
                for i, name in enumerate(mic_list):
                    if any(usb_indicator in name.lower() for usb_indicator in ['usb', 'webcam', 'logitech', 'creative', 'blue']):
                        # Test if this device actually works
                        if self._test_microphone_device(i):
                            self.logger.info(f"🎤 Selected USB microphone: {name} (index {i})")
                            return i
                
                # If no USB device works, try built-in audio with special handling
                for i, name in enumerate(mic_list):
                    if any(builtin_indicator in name.lower() for builtin_indicator in ['bcm', 'alsa', 'default', 'pulse']):
                        if self._test_microphone_device(i):
                            self.logger.info(f"🎤 Selected built-in microphone: {name} (index {i})")
                            return i
                
                # Last resort: return None to use basic microphone
                self.logger.warning("🍓 No working microphone devices found on Raspberry Pi")
                return None
            
            # For other platforms, use existing logic
            for i, name in enumerate(mic_list):
                if any(usb_indicator in name.lower() for usb_indicator in ['usb', 'webcam', 'logitech', 'creative', 'blue']):
                    self.logger.info(f"🎤 Selected USB microphone: {name} (index {i})")
                    return i
            
            # Default to first available microphone
            if mic_list:
                self.logger.info(f"🎤 Using default microphone: {mic_list[0]} (index 0)")
                return 0
            
            return None
            
        except Exception as e:
            self.logger.error(f"🎤 Error detecting microphones: {e}")
            return None

    def _test_microphone_device(self, device_index: int) -> bool:
        """Test if a specific microphone device actually works."""
        try:
            # Quick test to see if device can be opened
            test_mic = sr.Microphone(device_index=device_index)
            with test_mic as source:
                # If we can open it, it's probably working
                if hasattr(source, 'stream') and source.stream is not None:
                    return True
            return False
        except Exception as e:
            self.logger.debug(f"🎤 Device {device_index} test failed: {e}")
            return False

    def calibrate_audio(self, duration: float = 2.0):
        """Calibrate audio settings for ambient noise with robust error handling and threshold management."""
        mic_source = None
        try:
            # Get the best microphone device for this platform
            mic_device_index = self._get_best_microphone_device()
            
            # Try with specific device first
            try:
                mic_source = sr.Microphone(
                    device_index=mic_device_index,
                    sample_rate=self.sample_rate, 
                    chunk_size=self.chunk_size
                )
                self.logger.info(f"Calibration: Microphone initialized with device {mic_device_index}")
            except Exception as device_error:
                self.logger.warning(f"Calibration: Failed to initialize with device {mic_device_index}: {device_error}")
                # Fallback to default device
                try:
                    mic_source = sr.Microphone(
                        sample_rate=self.sample_rate, 
                        chunk_size=self.chunk_size
                    )
                    self.logger.info("Calibration: Microphone initialized with default device")
                except Exception as default_error:
                    self.logger.error(f"Calibration: Failed to initialize default microphone: {default_error}")
                    # Last resort - basic microphone
                    mic_source = sr.Microphone()
                    self.logger.info("Calibration: Microphone initialized with basic settings")
            
            # Use platform-optimized microphone settings with specific device
            with mic_source as source:
                try:
                    self.logger.info(f"Calibrating for ambient noise ({duration}s)...")
                    
                    # Store the original threshold for comparison
                    original_threshold = getattr(self, '_energy_threshold', self.recognizer.energy_threshold)
                    
                    self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                    new_threshold = self.recognizer.energy_threshold
                    
                    # Implement smart threshold management to prevent runaway values
                    platform_max_threshold = 1000 if 'Raspberry Pi' in self.platform_info['name'] else 800
                    platform_min_threshold = 100 if 'Raspberry Pi' in self.platform_info['name'] else 150
                    
                    # If the new threshold is too high, use a reasonable maximum
                    if new_threshold > platform_max_threshold:
                        self.logger.warning(f"Calibrated threshold {new_threshold:.2f} exceeds platform maximum {platform_max_threshold}")
                        self.recognizer.energy_threshold = platform_max_threshold
                        self.energy_threshold = platform_max_threshold
                        self.logger.info(f"Using platform maximum threshold: {platform_max_threshold}")
                    # If the new threshold is too low, use a reasonable minimum
                    elif new_threshold < platform_min_threshold:
                        self.logger.warning(f"Calibrated threshold {new_threshold:.2f} below platform minimum {platform_min_threshold}")
                        self.recognizer.energy_threshold = platform_min_threshold
                        self.energy_threshold = platform_min_threshold
                        self.logger.info(f"Using platform minimum threshold: {platform_min_threshold}")
                    else:
                        # Use the calibrated threshold
                        self.energy_threshold = new_threshold
                        self.logger.info(f"Audio calibrated. Energy threshold: {new_threshold:.2f}")
                    
                    # Log the threshold change for debugging
                    final_threshold = self.energy_threshold
                    self.logger.info(f"🔧 THRESHOLD MANAGEMENT: {original_threshold:.2f} → {final_threshold:.2f}")
                    
                except Exception as calibration_error:
                    self.logger.warning(f"Ambient noise calibration failed: {calibration_error}")
                    # Use platform-specific default energy threshold
                    if 'Raspberry Pi' in self.platform_info['name']:
                        default_threshold = 200  # Good for Pi with USB audio
                    else:
                        default_threshold = 300  # Good for other platforms
                    
                    self.recognizer.energy_threshold = default_threshold
                    self.energy_threshold = default_threshold
                    self.logger.info(f"Using platform default energy threshold: {default_threshold}")
        except Exception as e:
            self.logger.error(f"Audio calibration failed: {e}")
            # Set platform-specific fallback values
            if 'Raspberry Pi' in self.platform_info['name']:
                fallback_threshold = 200
            else:
                fallback_threshold = 300
            
            self.recognizer.energy_threshold = fallback_threshold
            self.energy_threshold = fallback_threshold
            self.logger.info(f"Using fallback energy threshold: {fallback_threshold}")

    def listen_for_audio(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[sr.AudioData]:
        """Listen for audio input with improved error handling for Raspberry Pi."""
        mic_source = None
        try:
            self.logger.info(f"🎤 AUDIO DEBUG: Starting audio capture (timeout={timeout}s, phrase_limit={phrase_time_limit}s)")
            
            # Try to get the best microphone with proper error handling
            best_device_index = self._get_best_microphone_device()
            
            # Initialize microphone with robust error handling
            if best_device_index is not None:
                try:
                    mic_source = sr.Microphone(device_index=best_device_index, sample_rate=self.sample_rate, chunk_size=self.chunk_size)
                    self.logger.info(f"🎤 AUDIO DEBUG: Using microphone device {best_device_index}")
                except Exception as device_error:
                    self.logger.warning(f"🎤 AUDIO DEBUG: Failed to use device {best_device_index}: {device_error}")
                    mic_source = None
            
            # Fallback to default microphone if specific device failed
            if mic_source is None:
                try:
                    mic_source = sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size)
                    self.logger.info("🎤 AUDIO DEBUG: Using default microphone with custom settings")
                except Exception as default_error:
                    self.logger.error(f"🎤 AUDIO DEBUG: Failed to initialize default microphone: {default_error}")
                    # Last resort - basic microphone
                    try:
                        mic_source = sr.Microphone()
                        self.logger.info("🎤 AUDIO DEBUG: Using basic microphone settings")
                    except Exception as basic_error:
                        self.logger.error(f"🎤 AUDIO DEBUG: Failed to initialize any microphone: {basic_error}")
                        return None
            
            # Test if microphone can be opened before using it
            try:
                with mic_source as source:
                    # Test if the stream actually opened
                    if not hasattr(source, 'stream') or source.stream is None:
                        self.logger.error("🎤 AUDIO DEBUG: Microphone stream failed to initialize")
                        return None
                    
                    self.logger.info("🎤 AUDIO DEBUG: Microphone opened successfully")
                    
                    # Quick ambient noise adjustment with error handling
                    try:
                        self.logger.info("🎤 AUDIO DEBUG: Adjusting for ambient noise...")
                        # Only do full calibration if threshold seems way off, otherwise use quick adjustment
                        current_threshold = getattr(self, '_energy_threshold', self.recognizer.energy_threshold)
                        
                        # Quick calibration (0.5s) to avoid excessive threshold climbing
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                        new_threshold = self.recognizer.energy_threshold
                        
                        # Apply the same threshold management as in calibrate_audio
                        platform_max_threshold = 1000 if 'Raspberry Pi' in self.platform_info['name'] else 800
                        platform_min_threshold = 100 if 'Raspberry Pi' in self.platform_info['name'] else 150
                        
                        # Prevent runaway threshold climbing during conversation
                        if new_threshold > platform_max_threshold:
                            self.logger.warning(f"🎤 AUDIO DEBUG: Threshold {new_threshold:.2f} capped at {platform_max_threshold}")
                            self.recognizer.energy_threshold = platform_max_threshold
                            self.energy_threshold = platform_max_threshold
                        elif new_threshold < platform_min_threshold:
                            self.logger.warning(f"🎤 AUDIO DEBUG: Threshold {new_threshold:.2f} raised to {platform_min_threshold}")
                            self.recognizer.energy_threshold = platform_min_threshold
                            self.energy_threshold = platform_min_threshold
                        else:
                            self.energy_threshold = new_threshold
                        
                        self.logger.info(f"🎤 AUDIO DEBUG: Energy threshold: {current_threshold:.2f} → {self.energy_threshold:.2f}")
                    except Exception as calibration_error:
                        self.logger.warning(f"🎤 AUDIO DEBUG: Ambient noise calibration failed: {calibration_error}")
                        # Use lower energy threshold for Pi to detect quieter speech
                        if 'Raspberry Pi' in self.platform_info['name']:
                            self.recognizer.energy_threshold = 200  # Stable threshold for Pi
                            self.energy_threshold = 200
                            self.logger.info("🎤 AUDIO DEBUG: Using Pi-optimized energy threshold: 200")
                        else:
                            self.recognizer.energy_threshold = 300
                            self.energy_threshold = 300
                            self.logger.info("🎤 AUDIO DEBUG: Using default energy threshold: 300")
                    
                    # Listen for audio with improved settings
                    self.logger.info("🎤 AUDIO DEBUG: Listening for speech...")
                    
                    # Adjust timeout and phrase limit for better detection
                    actual_timeout = max(timeout, 2)  # Minimum 2 seconds
                    actual_phrase_limit = max(phrase_time_limit, 5)  # Minimum 5 seconds
                    
                    self.logger.info(f"🎤 AUDIO DEBUG: Using timeout={actual_timeout}s, phrase_limit={actual_phrase_limit}s")
                    
                    audio = self.recognizer.listen(
                        source, 
                        timeout=actual_timeout, 
                        phrase_time_limit=actual_phrase_limit
                    )
                    self.logger.info("🎤 AUDIO DEBUG: Audio captured successfully!")
                    return audio
                    
            except Exception as stream_error:
                # Handle timeout errors separately from other errors
                if isinstance(stream_error, sr.WaitTimeoutError):
                    self.logger.debug("🎤 AUDIO DEBUG: Listening timeout - no speech detected (this is normal)")
                    return None
                else:
                    self.logger.error(f"🎤 AUDIO DEBUG: Error with microphone stream: {stream_error}")
                    import traceback
                    self.logger.error(f"🎤 AUDIO DEBUG: Stream error traceback: {traceback.format_exc()}")
                    return None
                
        except sr.WaitTimeoutError:
            self.logger.debug("🎤 AUDIO DEBUG: Audio listening timeout - no speech detected (this is normal)")
            return None
        except Exception as e:
            self.logger.error(f"🎤 AUDIO DEBUG: Error listening for audio: {e}")
            import traceback
            self.logger.error(f"🎤 AUDIO DEBUG: Traceback: {traceback.format_exc()}")
            return None

    def audio_to_text(self, audio_data: sr.AudioData) -> Optional[str]:
        """Convert audio data to text using Google Speech Recognition."""
        try:
            self.logger.info("🧠 RECOGNITION DEBUG: Starting speech recognition...")
            text = self.recognizer.recognize_google(audio_data)
            self.logger.info(f"🧠 RECOGNITION DEBUG: Speech recognized successfully: '{text}'")
            return text.lower()
        except sr.UnknownValueError:
            self.logger.info("🧠 RECOGNITION DEBUG: Could not understand audio - speech was unclear")
            return None
        except sr.RequestError as e:
            self.logger.error(f"🧠 RECOGNITION DEBUG: Speech recognition service error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"🧠 RECOGNITION DEBUG: Unexpected recognition error: {e}")
            import traceback
            self.logger.error(f"🧠 RECOGNITION DEBUG: Traceback: {traceback.format_exc()}")
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