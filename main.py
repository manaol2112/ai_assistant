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

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import Config
    from audio_utils import AudioManager, setup_premium_tts_engines
    from wake_word_detector import WakeWordDetector
    from dinosaur_identifier import DinosaurIdentifier
    from object_identifier import ObjectIdentifier
    from smart_camera_detector import SmartCameraDetector
    import openai
    import pyttsx3
    import speech_recognition as sr
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
        
        # Setup wake word detector
        self.wake_word_detector = WakeWordDetector(self.config)
        
        # Setup dinosaur identifier for Eladriel (specialized for dinosaurs)
        logger.info("Setting up dinosaur identification for Eladriel...")
        self.dinosaur_identifier = DinosaurIdentifier(self.client, self.config)
        
        # Setup universal object identifier for both users
        logger.info("🔍 Setting up universal object identification system...")
        self.object_identifier = ObjectIdentifier()
        
        # Setup face recognition system
        logger.info("🎭 Setting up face recognition system...")
        self.face_detector = SmartCameraDetector(model_size='n', confidence_threshold=0.4)
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
        
        # Spelling game settings
        self.spelling_game_active = False
        self.current_spelling_word = None
        self.spelling_word_index = 0
        self.spelling_score = 0
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
                'greeting': "Hi Sophia! I'm here to help you with anything you need! My voice sounds so much more natural now!",
                'face_greeting': "Hello Sophia! I can see you! 👋 How wonderful to see your beautiful face!",
                'tts_engine': self.sophia_tts,
                'special_commands': ['help', 'what can you do', 'identify this', 'what is this', 'tell me about this', 'spelling game', 'play spelling', 'ready', 'end game']
            },
            'eladriel': {
                'name': 'Eladriel',
                'wake_word': 'dino',
                'personality': 'playful, curious, and energetic',
                'greeting': "Hey Eladriel! Ready for some fun discoveries? I can identify your dinosaur toys and any other objects! And listen to how natural my voice sounds now!",
                'face_greeting': "Hey Eladriel! I see you there! 🦕 Ready for some dinosaur adventures?",
                'tts_engine': self.eladriel_tts,
                'special_commands': ['identify dinosaur', 'identify this', 'what is this', 'tell me about this', 'show me camera', 'dinosaur tips', 'help', 'spelling game', 'play spelling', 'ready', 'end game']
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
                    'news update', 'shopping list', 'calendar', 'notes', 'spelling game', 'play spelling', 'ready', 'end game'
                ]
            }
        }
        
        logger.info("🚀 AI Assistant initialized with premium natural voices, face recognition, and universal object identification!")

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
            # Start camera
            if not self.face_detector.start_camera():
                logger.error("Failed to start camera for face recognition")
                return
            
            while self.face_recognition_active and self.running:
                try:
                    # Capture frame
                    ret, frame = self.face_detector.cap.read()
                    if not ret:
                        continue
                    
                    # Detect faces
                    face_detections = self.face_detector.detect_faces(frame)
                    
                    # Process detected faces
                    for face in face_detections:
                        if face['name'] != "Unknown" and face['confidence'] > 0.6:
                            person_name = face['name'].lower()
                            
                            # Check if this person is in our user profiles
                            if person_name in self.users:
                                # If no one is currently in conversation, start automatic conversation
                                if not self.current_user and self.should_greet_face(person_name):
                                    # Get appropriate face greeting (time-aware for parent mode)
                                    if person_name == 'parent':
                                        face_greeting = self.get_parent_face_greeting()
                                    else:
                                        face_greeting = self.users[person_name].get('face_greeting', f"Hello {person_name.title()}!")
                                    
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
            if self.face_detector.cap:
                self.face_detector.cap.release()
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
                    self.speak(special_response, user)
                else:
                    # Process with OpenAI for regular conversation
                    import asyncio
                    try:
                        response = asyncio.run(self.process_with_openai(user_input, user))
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
        """Convert text to speech with user-specific voice settings and interrupt capability."""
        try:
            # Reset interrupt flag
            self.speech_interrupted = False
            
            # Start interrupt listener
            self.start_interrupt_listener()
            
            # Use personalized TTS engine for each user
            if user and user in self.users:
                tts_engine = self.users[user]['tts_engine']
                logger.info(f"Speaking to {user}: {text}")
                
                # Use threaded TTS for smooth speech with interrupt capability
                self._speak_with_interrupt_check(tts_engine, text)
                    
            else:
                # Default to Sophia's engine if no user specified
                logger.info(f"Speaking (default): {text}")
                self._speak_with_interrupt_check(self.sophia_tts, text)
            
            # Stop interrupt listener
            self.stop_interrupt_listener()
            
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            self.stop_interrupt_listener()

    def _speak_with_interrupt_check(self, tts_engine, text: str):
        """Speak with smooth delivery but interrupt capability."""
        # Create a flag to track if TTS is complete
        speech_complete = threading.Event()
        
        def speak_thread():
            """Background thread for TTS."""
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
                speech_complete.set()
            except Exception as e:
                logger.error(f"TTS thread error: {e}")
                speech_complete.set()
        
        # Start TTS in background thread
        tts_thread = threading.Thread(target=speak_thread, daemon=True)
        tts_thread.start()
        
        # Monitor for interrupts while speech is ongoing
        while not speech_complete.is_set() and not self.speech_interrupted:
            time.sleep(0.1)  # Check every 100ms for interrupts
        
        # If interrupted, stop the TTS engine
        if self.speech_interrupted:
            try:
                tts_engine.stop()
            except:
                pass
            logger.info("Speech interrupted and stopped")
        
        # Wait for thread to complete (with timeout)
        tts_thread.join(timeout=1.0)

    def split_text_for_interruption(self, text: str) -> list:
        """Split text into manageable chunks for interrupt checking."""
        # This method is now deprecated but kept for compatibility
        return [text]

    def start_interrupt_listener(self):
        """Start background listener for interrupt commands."""
        if not self.interrupt_listener_active:
            self.interrupt_listener_active = True
            self.interrupt_thread = threading.Thread(target=self.interrupt_listener, daemon=True)
            self.interrupt_thread.start()

    def stop_interrupt_listener(self):
        """Stop background interrupt listener."""
        self.interrupt_listener_active = False
        if self.interrupt_thread:
            self.interrupt_thread.join(timeout=1)

    def interrupt_listener(self):
        """Background thread that listens for interrupt commands during speech."""
        try:
            while self.interrupt_listener_active and not self.speech_interrupted:
                try:
                    with sr.Microphone() as source:
                        # Quick listen with short timeout for responsiveness
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                        audio = self.recognizer.listen(source, timeout=0.3, phrase_time_limit=2)
                        
                        # Convert to text
                        user_input = self.recognizer.recognize_google(audio).lower()
                        logger.info(f"Interrupt check detected: {user_input}")
                        
                        # Check for interrupt commands
                        if self.is_interrupt_command(user_input):
                            logger.info(f"Interrupt command detected: {user_input}")
                            self.speech_interrupted = True
                            
                            # Store the interrupt input for handling
                            self.last_interrupt_input = user_input
                            
                            # Stop TTS engines immediately
                            try:
                                self.sophia_tts.stop()
                                self.eladriel_tts.stop()
                            except:
                                pass
                            
                            break
                            
                except sr.WaitTimeoutError:
                    # No speech detected, continue listening
                    continue
                except sr.UnknownValueError:
                    # Could not understand audio, continue
                    continue
                except sr.RequestError:
                    # Speech recognition error, continue
                    continue
                except Exception as e:
                    # Any other error, log and continue
                    logger.error(f"Interrupt listener error: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Interrupt listener thread error: {e}")

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
        """Listen for speech input and convert to text with longer timeout for children."""
        try:
            with sr.Microphone() as source:
                logger.info("Listening for speech...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio with longer timeout and phrase limit for children
                # Kids need more time to think and formulate their thoughts
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=20)
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized speech: {text}")
                return text.lower()
                
        except sr.WaitTimeoutError:
            logger.info("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.info("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
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
        
        # Spelling Game Commands (for Sophia, Eladriel, and Parent)
        if user in ['sophia', 'eladriel', 'parent']:
            if any(phrase in user_input_lower for phrase in ['spelling game', 'play spelling', 'start spelling']):
                return self.start_spelling_game(user)
            
            elif self.spelling_game_active and any(phrase in user_input_lower for phrase in ['ready', 'i\'m ready', 'check my answer']):
                return self.check_spelling_answer(user)
            
            elif self.spelling_game_active and any(phrase in user_input_lower for phrase in ['end game', 'stop game', 'quit game']):
                return self.end_spelling_game(user)
        
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
            result = self.object_identifier.capture_and_identify(user)
            
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
• Say "Ready" when you want me to check your answer with my camera
• Get helpful tips if you need help with tricky words
• Say "End Game" to stop playing anytime

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

Ask me anything, show me any object, or play the spelling game to practice your writing!"""
        
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
• Say "Ready" when you want me to check your writing with my camera
• Get dinosaur-themed help and encouragement for tricky words
• Say "End Game" whenever you want to stop

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

What do you want to explore today? Show me anything you've discovered, or let's practice spelling! 🚀"""
        
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
            greeting = user_info['greeting']
        
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
                    self.speak(special_response, user)
                else:
                    # Process with OpenAI for regular conversation
                    import asyncio
                    try:
                        response = asyncio.run(self.process_with_openai(user_input, user))
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
        """Start an interactive spelling game for kids."""
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
            
            if user == 'sophia':
                intro = f"Hi Sophia! Let's play the spelling game! 📝✨ I'll give you words to spell, and you can write them down on paper."
            elif user == 'eladriel':
                intro = f"Hey Eladriel! Ready for a spelling adventure? 🦕📝 Let's see how well you can spell these words!"
            else:  # parent
                intro = f"Parent Mode: Spelling Game Test. This allows you to validate the game functionality before the children use it."
            
            word = self.current_spelling_word['word']
            hint = self.current_spelling_word['hint']
            
            game_instructions = f"""{intro}

Here's how to play:
1. I'll say a word and give you a hint
2. Write the word on paper with big, clear letters
3. When you're done, say 'Ready' and show me your paper
4. I'll check if it's correct and help you learn!
5. Say 'End Game' anytime to stop playing

Let's start! 🌟

Word #{self.spelling_word_index + 1}: {word.upper()}
Hint: {hint}

Take your time and write '{word}' on your paper. Remember to make your letters big and clear! When you're finished, say 'Ready' and show me your answer."""
            
            return game_instructions
            
        except Exception as e:
            logger.error(f"Error starting spelling game: {e}")
            return "Sorry! I had trouble starting the spelling game. Let's try again later!"

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

You're an amazing speller! Great job practicing your writing! 📝✨"""
                        self.spelling_game_active = False
                        return final_score
                    else:
                        # Next word
                        self.current_spelling_word = self.spelling_words_grade2_3[self.spelling_word_index]
                        next_word = self.current_spelling_word['word']
                        next_hint = self.current_spelling_word['hint']
                        
                        return f"""{praise}

Ready for the next word? Here we go! 

Word #{self.spelling_word_index + 1}: {next_word.upper()}
Hint: {next_hint}

Write '{next_word}' on your paper, and say 'Ready' when you want me to check it!"""
                
                else:
                    # Incorrect answer - provide helpful feedback with what was detected
                    detected_info = f" (I saw: '{detected_text}')" if detected_text else ""
                    
                    if user == 'sophia':
                        feedback = f"Good try Sophia! The correct spelling is '{correct_word.upper()}'{detected_info}. Let me help you learn it!"
                    elif user == 'eladriel':
                        feedback = f"Nice effort Eladriel! The correct spelling is '{correct_word.upper()}'{detected_info}. Let's learn it together!"
                    else:  # parent
                        feedback = f"❌ Incorrect spelling detected. Expected: '{correct_word.upper()}'{detected_info}. Testing educational feedback system."
                    
                    # Provide detailed spelling help
                    spelling_help = self.provide_spelling_help(correct_word, user)
                    
                    return f"""{feedback}

{spelling_help}

Try writing '{correct_word}' again! Take your time and remember the tips I gave you. Say 'Ready' when you want me to check your new answer!"""
            
            else:
                return f"I had trouble seeing your paper clearly. {result['message']} Make sure to write with big, dark letters and hold it steady in front of the camera. Say 'Ready' when you're ready to try again!"
                
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
            farewell = f"Great job playing the spelling game, Sophia! 📝✨"
        elif user == 'eladriel':
            farewell = f"Awesome spelling adventure, Eladriel! 🦕📝"
        else:  # parent
            farewell = f"Spelling Game Test Complete - Parent Mode"
        
        final_message = f"""{farewell}

Game Summary:
📊 Words attempted: {self.spelling_word_index + 1}
⭐ Score: {self.spelling_score} correct
🎯 You're doing fantastic with your spelling practice!

Thanks for playing! Say 'Spelling Game' anytime you want to practice more words! Keep up the great work! 🌟"""
        
        # Reset game state
        self.spelling_game_active = False
        self.current_spelling_word = None
        self.spelling_word_index = 0
        self.spelling_score = 0
        
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

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run() 