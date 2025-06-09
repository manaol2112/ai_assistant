#!/usr/bin/env python3
"""
Test script to showcase the premium OpenAI TTS voices
This demonstrates the incredible difference between robotic system voices and natural human-like OpenAI voices
"""

import os
import sys
import time
import openai
from config import Config
from audio_utils import setup_premium_tts_engines, setup_tts_engines

def test_voice_comparison():
    """Test and compare robotic vs premium natural voices."""
    
    print("🎙️ VOICE COMPARISON TEST")
    print("=" * 50)
    print("Let's compare the old robotic voices with the new premium natural voices!")
    print()
    
    # Setup config and OpenAI client
    config = Config()
    client = openai.OpenAI(api_key=config.openai_api_key)
    
    # Test messages
    test_messages = [
        "Hi! I'm your AI assistant and I'm here to help you!",
        "The difference in voice quality is absolutely incredible!",
        "I can now speak with natural human-like voices that sound completely real!"
    ]
    
    print("🤖 TESTING OLD ROBOTIC SYSTEM VOICES")
    print("-" * 40)
    
    try:
        # Test old robotic voices
        print("Setting up old robotic TTS engines...")
        old_sophia, old_eladriel = setup_tts_engines()
        
        for i, message in enumerate(test_messages, 1):
            print(f"🔊 Playing robotic message {i}: {message}")
            old_sophia.say(message)
            old_sophia.runAndWait()
            time.sleep(1)
            
        print("\n✅ Old robotic voices demo complete")
        
    except Exception as e:
        print(f"⚠️ Old voice system error: {e}")
    
    print("\n" + "="*50)
    print("✨ TESTING NEW PREMIUM OPENAI VOICES")
    print("-" * 40)
    
    try:
        # Test premium OpenAI voices
        print("Setting up premium OpenAI TTS engines...")
        premium_sophia, premium_eladriel = setup_premium_tts_engines(client)
        
        print("\n🎯 SOPHIA'S PREMIUM VOICE (Shimmer - Soft & Encouraging)")
        for i, message in enumerate(test_messages, 1):
            enhanced_message = f"Hi, this is Sophia speaking! {message}"
            print(f"🔊 Playing premium Sophia message {i}: {enhanced_message}")
            premium_sophia.say(enhanced_message)
            time.sleep(0.5)
        
        print("\n🦕 ELADRIEL'S PREMIUM VOICE (Nova - Young & Energetic)")
        for i, message in enumerate(test_messages, 1):
            enhanced_message = f"Hey, this is Eladriel! {message} Isn't this amazing?"
            print(f"🔊 Playing premium Eladriel message {i}: {enhanced_message}")
            premium_eladriel.say(enhanced_message)
            time.sleep(0.5)
            
        print("\n🎉 Premium voice demo complete!")
        
    except Exception as e:
        print(f"❌ Premium voice system error: {e}")
        print("Make sure your OpenAI API key is properly configured!")
    
    print("\n" + "="*50)
    print("🏆 VOICE COMPARISON RESULTS")
    print("-" * 40)
    print("✅ OLD SYSTEM: Robotic, mechanical, clearly artificial")
    print("🌟 NEW SYSTEM: Natural, human-like, warm and engaging")
    print("\nThe difference is absolutely incredible! The new voices sound")
    print("completely human and will make interactions so much more natural!")


def test_individual_voices():
    """Test each OpenAI voice individually to pick favorites."""
    
    print("\n🎨 TESTING ALL AVAILABLE OPENAI VOICES")
    print("=" * 50)
    
    config = Config()
    client = openai.OpenAI(api_key=config.openai_api_key)
    
    # All available OpenAI voices
    voices = {
        "alloy": "Balanced and natural",
        "echo": "Male, clear and articulate", 
        "fable": "British accent, warm and friendly",
        "onyx": "Deep and authoritative",
        "nova": "Young and energetic (perfect for kids!)",
        "shimmer": "Soft and gentle (very encouraging)"
    }
    
    test_message = "Hello! I'm testing this voice to see how natural and pleasant it sounds for our AI assistant!"
    
    for voice_name, description in voices.items():
        print(f"\n🎤 Testing {voice_name.upper()}: {description}")
        print("-" * 30)
        
        try:
            from audio_utils import OpenAITTSEngine
            engine = OpenAITTSEngine(client, voice=voice_name, model="tts-1-hd")
            
            voice_message = f"Hi! This is the {voice_name} voice. {test_message}"
            print(f"🔊 Playing: {voice_message}")
            engine.say(voice_message)
            
        except Exception as e:
            print(f"❌ Error with {voice_name}: {e}")
    
    print("\n🌟 Voice testing complete!")
    print("Current selections:")
    print("  • Sophia: Shimmer (soft, encouraging)")
    print("  • Eladriel: Nova (young, energetic)")


if __name__ == "__main__":
    print("🎙️ PREMIUM VOICE SYSTEM TEST")
    print("Testing the incredible new natural human-like voices!")
    print("This will demonstrate the massive improvement over robotic system voices.")
    print()
    
    try:
        # Main comparison test
        test_voice_comparison()
        
        # Individual voice testing
        response = input("\nWould you like to test all individual voices? (y/n): ").lower()
        if response == 'y':
            test_individual_voices()
            
        print("\n🎉 Voice testing complete!")
        print("Your AI assistant now has premium natural voices that sound completely human!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Voice test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Make sure your environment is properly set up and OpenAI API key is configured!") 