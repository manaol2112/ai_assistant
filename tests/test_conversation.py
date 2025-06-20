#!/usr/bin/env python3
"""
Quick Conversation Test for AI Assistant
Test the assistant's responses without requiring wake word detection
"""

import os
import sys
import pyttsx3
import openai
from dotenv import load_dotenv
from config import Config

def test_conversation():
    """Test a quick conversation with the AI assistant."""
    
    print("🤖 AI Assistant Conversation Test")
    print("=" * 40)
    
    try:
        # Load configuration
        config = Config()
        print("✅ Configuration loaded")
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=config.openai_api_key)
        print("✅ OpenAI client ready")
        
        # Initialize text-to-speech
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', config.tts_rate)
        tts_engine.setProperty('volume', config.tts_volume)
        print("✅ Text-to-speech ready")
        
        # Test different user modes
        users = {
            'sophia': {
                'wake_word': 'Miley',
                'greeting': 'Hi Sophia! I\'m your AI assistant. How can I help you today?',
                'personality': 'friendly and encouraging, perfect for a child named Sophia'
            },
            'eladriel': {
                'wake_word': 'Dino',
                'greeting': 'Hey Eladriel! I\'m your AI assistant. What would you like to know?',
                'personality': 'playful and curious, perfect for a child named Eladriel'
            }
        }
        
        def get_ai_response(user_name, message):
            """Get AI response for a specific user."""
            user_info = users[user_name]
            
            system_prompt = f"""You are a helpful AI assistant for {user_name.title()}. 
Your personality should be {user_info['personality']}. 
Keep responses brief, child-friendly, and engaging. 
Always respond in a warm, caring tone appropriate for a young person."""
            
            response = client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=config.openai_max_tokens,
                temperature=config.openai_temperature
            )
            
            return response.choices[0].message.content.strip()
        
        def speak_text(text):
            """Convert text to speech."""
            print(f"🗣️  Speaking: {text}")
            tts_engine.say(text)
            tts_engine.runAndWait()
        
        # Test for each user
        for user_name, user_info in users.items():
            print(f"\n🎭 Testing {user_name.title()} mode (wake word: '{user_info['wake_word']}')")
            print("-" * 30)
            
            # Greeting
            greeting = user_info['greeting']
            print(f"AI: {greeting}")
            speak_text(greeting)
            
            # Test questions
            test_questions = [
                "What's your favorite color?",
                "Tell me a fun fact!",
                "How are you today?"
            ]
            
            for question in test_questions:
                print(f"\nUser: {question}")
                try:
                    response = get_ai_response(user_name, question)
                    print(f"AI: {response}")
                    speak_text(response)
                except Exception as e:
                    print(f"❌ Error getting AI response: {e}")
                
                input("Press Enter to continue...")
        
        print("\n✅ Conversation test completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python main.py' for full voice control")
        print("2. Say 'Miley' or 'Dino' to activate the assistant")
        print("3. Speak your questions naturally")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversation test: {e}")
        return False

def main():
    """Run the conversation test."""
    print("Starting AI Assistant conversation test...")
    print("This will test text-to-speech and AI responses.")
    print("Make sure your speakers/headphones are on!\n")
    
    input("Press Enter to start the test...")
    
    success = test_conversation()
    
    if success:
        print("\n🎉 All tests passed! Your AI assistant is ready!")
    else:
        print("\n⚠️  Some issues detected. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 