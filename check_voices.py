#!/usr/bin/env python3
"""
Check and set English voice for text-to-speech
"""

import pyttsx3

def check_voices():
    """Check available voices and find English ones."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("🗣️  Available Text-to-Speech Voices:")
    print("=" * 50)
    
    english_voices = []
    
    for i, voice in enumerate(voices):
        name = voice.name if hasattr(voice, 'name') else 'Unknown'
        lang = voice.languages[0] if hasattr(voice, 'languages') and voice.languages else 'Unknown'
        
        is_english = 'en' in lang.lower() if lang != 'Unknown' else 'english' in name.lower()
        
        status = "✅ ENGLISH" if is_english else "🌐 OTHER"
        print(f"{i:2d}. {status} - {name} ({lang})")
        
        if is_english:
            english_voices.append((i, voice, name))
    
    print(f"\n📊 Found {len(english_voices)} English voices out of {len(voices)} total")
    
    # Test with a preferred English voice
    if english_voices:
        print(f"\n🎯 Testing English voices:")
        
        for i, (idx, voice, name) in enumerate(english_voices[:3]):  # Test first 3
            print(f"\nTesting voice {idx}: {name}")
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
            test_text = f"Hello! This is voice {name}. I am speaking in English."
            print(f"Speaking: {test_text}")
            engine.say(test_text)
            engine.runAndWait()
            
            response = input("Did this sound like English? (y/n): ").lower().strip()
            if response == 'y':
                print(f"✅ Great! Voice {idx} ({name}) works well.")
                print(f"Voice ID: {voice.id}")
                break
        else:
            print("⚠️  Please check your system's text-to-speech settings.")
    
    engine.stop()
    return english_voices

if __name__ == "__main__":
    check_voices() 