#!/usr/bin/env python3
"""
Test kid-friendly voices for the AI Assistant
"""

import pyttsx3
import time

def test_kid_friendly_voices():
    """Test voices that might sound more kid-friendly."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Kid-friendly voices to test (these tend to sound younger/more playful)
    kid_friendly_candidates = [
        'karen',      # Australian - often sounds younger
        'victoria',   # US female - clear and friendly
        'samantha',   # US female - warm and friendly  
        'fiona',      # Scottish - unique and playful
        'alex',       # US male - clear and friendly
        'daniel',     # British male - polite and clear
        'fred'        # US male - sometimes sounds younger
    ]
    
    print("🎯 Testing Kid-Friendly Voices")
    print("=" * 50)
    
    # Find available kid-friendly voices
    available_kid_voices = []
    for voice in voices:
        voice_name = voice.name.lower()
        for candidate in kid_friendly_candidates:
            if candidate in voice_name:
                available_kid_voices.append((voice, candidate))
                break
    
    if not available_kid_voices:
        print("❌ No kid-friendly voices found from preferred list")
        return
    
    print(f"Found {len(available_kid_voices)} kid-friendly voices to test:\n")
    
    # Test each voice with kid-friendly content
    test_phrases = [
        "Hi! I'm your AI friend! Ready to learn something cool?",
        "Wow, that's an awesome question! Let me help you with that!",
        "Did you know that octopuses have three hearts? That's so cool!"
    ]
    
    for i, (voice, name) in enumerate(available_kid_voices):
        print(f"🎤 Testing Voice {i+1}: {voice.name}")
        print(f"   Language: {voice.languages[0] if voice.languages else 'Unknown'}")
        
        # Configure voice
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 190)  # Slightly faster for kids
        engine.setProperty('volume', 0.95)
        
        # Test with kid-friendly phrase
        phrase = test_phrases[i % len(test_phrases)]
        print(f"   Speaking: '{phrase}'")
        
        engine.say(phrase)
        engine.runAndWait()
        
        # Get user feedback
        while True:
            response = input(f"   Rate this voice (1-5, 5=best for kids): ").strip()
            if response.isdigit() and 1 <= int(response) <= 5:
                rating = int(response)
                break
            print("   Please enter a number from 1 to 5")
        
        if rating >= 4:
            print(f"   ✅ Great choice! Voice ID: {voice.id}")
            print(f"   Recommended for: {'Sophia' if i % 2 == 0 else 'Eladriel'}")
        else:
            print(f"   📝 Noted (rating: {rating})")
        
        print()
        time.sleep(1)
    
    engine.stop()
    
    print("\n" + "=" * 50)
    print("🍓 RASPBERRY PI COMPATIBILITY INFO:")
    print("=" * 50)
    print("✅ The AI assistant will work on Raspberry Pi!")
    print("However, voice availability may differ:")
    print()
    print("📋 Raspberry Pi Voice Notes:")
    print("• Default voices: Usually has 'espeak' voices")
    print("• May have fewer high-quality voices than Mac")
    print("• Can install additional voices with:")
    print("  sudo apt-get install espeak-data")
    print("  sudo apt-get install festival speechd-festival")
    print()
    print("🔧 For best results on Raspberry Pi:")
    print("• Test voices after setup with: python check_voices.py")
    print("• The system will automatically select best available English voice")
    print("• Voice quality may be different but still kid-friendly")
    print()
    print("🚀 To deploy to Raspberry Pi:")
    print("• Copy all files: scp -r . pi@raspberrypi.local:~/ai_assistant/")
    print("• Run setup: ./setup_raspberry_pi.sh")
    print("• Test voices: python check_voices.py")

if __name__ == "__main__":
    test_kid_friendly_voices() 