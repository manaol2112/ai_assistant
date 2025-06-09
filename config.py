"""
Configuration management for AI Assistant
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for AI Assistant settings."""
    
    def __init__(self):
        """Initialize configuration with environment variables and defaults."""
        
        # OpenAI Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file")
        
        # Audio Configuration
        self.audio_sample_rate = int(os.getenv('AUDIO_SAMPLE_RATE', '16000'))
        self.audio_chunk_size = int(os.getenv('AUDIO_CHUNK_SIZE', '1024'))
        self.audio_channels = int(os.getenv('AUDIO_CHANNELS', '1'))
        
        # Wake Word Configuration
        self.wake_word_sensitivity = float(os.getenv('WAKE_WORD_SENSITIVITY', '0.5'))
        self.porcupine_access_key = os.getenv('PORCUPINE_ACCESS_KEY', '')
        
        # Speech Recognition Configuration
        self.speech_timeout = int(os.getenv('SPEECH_TIMEOUT', '5'))
        self.speech_phrase_limit = int(os.getenv('SPEECH_PHRASE_LIMIT', '10'))
        
        # Text-to-Speech Configuration
        self.tts_rate = int(os.getenv('TTS_RATE', '180'))
        self.tts_volume = float(os.getenv('TTS_VOLUME', '0.9'))
        
        # OpenAI Model Configuration
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.openai_max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '150'))
        self.openai_temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        
        # Logging Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'ai_assistant.log')
        
        # Raspberry Pi Optimization
        self.pi_optimization = os.getenv('PI_OPTIMIZATION', 'true').lower() == 'true'
        self.low_power_mode = os.getenv('LOW_POWER_MODE', 'false').lower() == 'true'

    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        required_fields = ['openai_api_key']
        
        for field in required_fields:
            if not getattr(self, field):
                print(f"❌ Missing required configuration: {field}")
                return False
        
        print("✅ Configuration validated successfully")
        return True
    
    def print_config(self):
        """Print current configuration (excluding sensitive data)."""
        print("🔧 Current Configuration:")
        print(f"   • OpenAI Model: {self.openai_model}")
        print(f"   • Audio Sample Rate: {self.audio_sample_rate}")
        print(f"   • Speech Timeout: {self.speech_timeout}s")
        print(f"   • TTS Rate: {self.tts_rate}")
        print(f"   • Wake Word Sensitivity: {self.wake_word_sensitivity}")
        print(f"   • Pi Optimization: {self.pi_optimization}")
        print(f"   • Low Power Mode: {self.low_power_mode}") 