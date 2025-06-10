#!/usr/bin/env python3
"""
Integration Example for Visual Feedback in Main AI Assistant
Shows exactly how to add visual feedback to the existing main.py
"""

import sys
import os
import threading
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visual_feedback import create_visual_feedback
from visual_config import get_config_for_environment


class AIAssistantWithVisualFeedback:
    """
    Example showing how to integrate visual feedback into the main AI Assistant.
    This demonstrates the exact changes needed for main.py
    """
    
    def __init__(self):
        """Initialize AI Assistant with visual feedback."""
        
        # Get configuration for current environment
        self.config = get_config_for_environment()
        display_config = self.config.get_display_config()
        
        # Initialize visual feedback system
        self.visual = create_visual_feedback(use_gui=display_config['use_gui'])
        
        # Other AI initialization...
        self.running = False
        self.ai_speaking = False
        self.wake_word_detected = False
        
        print(f"🤖 AI Assistant initialized with visual feedback")
        print(f"   Display: {display_config['width']}x{display_config['height']}")
        print(f"   GUI Mode: {display_config['use_gui']}")
        print(f"   Hardware: {'Raspberry Pi' if self.config.RASPBERRY_PI else 'Desktop'}")
    
    def start(self):
        """Start the AI Assistant with visual feedback."""
        print("🚀 Starting AI Assistant with Visual Feedback...")
        
        self.running = True
        
        # Start visual feedback first
        if hasattr(self.visual, 'start'):
            self.visual.start()
        
        # Show startup sequence
        self.visual.show_standby("Starting AI Assistant...")
        time.sleep(1)
        
        self.visual.show_thinking("Loading models and services...")
        time.sleep(2)
        
        self.visual.show_happy("AI Assistant ready!")
        time.sleep(1)
        
        # Show ready state
        self.visual.show_standby("Ready to help! Say 'Miley' or 'Dino'")
        
        print("✅ AI Assistant started successfully!")
        
        # Start main AI loop in background if GUI is used
        if hasattr(self.visual, 'run_gui'):
            # Start AI operations in background thread
            ai_thread = threading.Thread(target=self._run_ai_operations, daemon=True)
            ai_thread.start()
            
            # Run GUI on main thread
            try:
                self.visual.run_gui()
            except KeyboardInterrupt:
                self.stop()
        else:
            # Run AI operations on main thread for non-GUI
            self._run_ai_operations()
    
    def _run_ai_operations(self):
        """Main AI operations loop."""
        while self.running:
            try:
                # Simulate AI operations
                self._simulate_wake_word_detection()
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error in AI operations: {e}")
                self.visual.show_error("System error occurred")
                time.sleep(5)
    
    def _simulate_wake_word_detection(self):
        """Simulate wake word detection and conversation."""
        
        # Simulate wake word detection every 10 seconds
        if not self.wake_word_detected:
            time.sleep(10)
            self.wake_word_detected = True
            
            # Show wake word detected
            self.visual.show_happy("Wake word detected!")
            time.sleep(1)
            
            # Start listening
            self.start_listening()
            
            # Simulate user interaction
            time.sleep(3)
            self.process_user_input("What's the weather like?")
            
            # Reset for next cycle
            self.wake_word_detected = False
    
    def start_listening(self):
        """Start listening for user input."""
        self.visual.show_listening("I'm listening! What can I help you with?")
        print("🎧 Listening for user input...")
    
    def process_user_input(self, user_input: str):
        """Process user input with visual feedback."""
        print(f"👤 User said: {user_input}")
        
        # Show thinking
        self.visual.show_thinking("Let me think about that...")
        time.sleep(2)
        
        # Simulate processing different types of requests
        if "weather" in user_input.lower():
            self.handle_weather_request()
        elif "game" in user_input.lower():
            self.handle_game_request()
        elif "camera" in user_input.lower():
            self.handle_camera_request()
        else:
            self.handle_general_request(user_input)
    
    def handle_weather_request(self):
        """Handle weather request with visual feedback."""
        self.visual.show_speaking("Let me check the weather for you...")
        self.ai_speaking = True
        
        time.sleep(2)
        
        self.visual.show_happy("It's sunny and 75°F today! Perfect weather!")
        time.sleep(3)
        
        self.ai_speaking = False
        self.visual.show_standby("Ready for your next question!")
    
    def handle_game_request(self):
        """Handle educational game request."""
        self.visual.show_happy("Let's play a learning game!")
        time.sleep(2)
        
        # Spelling game simulation
        self.visual.show_speaking("Can you spell the word 'CAT'?")
        time.sleep(3)
        
        self.visual.show_listening("I'm listening for your spelling...")
        time.sleep(4)
        
        self.visual.show_thinking("Let me check your spelling...")
        time.sleep(2)
        
        self.visual.show_happy("Perfect! C-A-T is correct! Great job!")
        time.sleep(3)
        
        self.visual.show_standby("Ready for more learning!")
    
    def handle_camera_request(self):
        """Handle camera/object identification request."""
        self.visual.show_thinking("Starting camera...")
        time.sleep(1)
        
        self.visual.show_listening("Show me what you want me to identify!")
        time.sleep(3)
        
        self.visual.show_thinking("Analyzing image...")
        time.sleep(2)
        
        self.visual.show_speaking("I can see a red apple! Apples are healthy fruits!")
        time.sleep(3)
        
        self.visual.show_standby("Ready to identify more objects!")
    
    def handle_general_request(self, user_input: str):
        """Handle general requests."""
        self.visual.show_speaking(f"You asked about: {user_input[:30]}...")
        time.sleep(3)
        
        self.visual.show_happy("I hope that helps!")
        time.sleep(2)
        
        self.visual.show_standby("What else can I help you with?")
    
    def handle_error(self, error_message: str):
        """Handle errors with visual feedback."""
        print(f"❌ Error: {error_message}")
        
        self.visual.show_error(f"Oops! {error_message}")
        time.sleep(3)
        
        self.visual.show_thinking("Let me try to fix that...")
        time.sleep(2)
        
        self.visual.show_standby("Back to normal! How can I help?")
    
    def stop(self):
        """Stop the AI Assistant."""
        print("🛑 Stopping AI Assistant...")
        
        self.running = False
        
        # Show shutdown sequence
        self.visual.show_sleeping("Goodbye! See you next time!")
        time.sleep(2)
        
        # Stop visual feedback
        if hasattr(self.visual, 'stop'):
            self.visual.stop()
        
        print("✅ AI Assistant stopped.")


def show_integration_guide():
    """Show step-by-step integration guide."""
    
    guide = """
🤖 VISUAL FEEDBACK INTEGRATION GUIDE
==================================

📋 Step 1: Add Imports to main.py
---------------------------------
Add these imports at the top of main.py:

```python
from visual_feedback import create_visual_feedback
from visual_config import get_config_for_environment
```

📋 Step 2: Initialize in AIAssistant.__init__()
----------------------------------------------
Add this to the __init__ method:

```python
def __init__(self):
    # ... existing initialization ...
    
    # Initialize visual feedback
    self.config = get_config_for_environment()
    display_config = self.config.get_display_config()
    self.visual = create_visual_feedback(use_gui=display_config['use_gui'])
    
    # ... rest of initialization ...
```

📋 Step 3: Update the run() method
---------------------------------
Modify the run method to handle GUI vs non-GUI:

```python
def run(self):
    self.running = True
    
    # Start visual feedback
    if hasattr(self.visual, 'start'):
        self.visual.start()
    
    self.visual.show_standby("AI Assistant starting...")
    
    # Initialize all systems...
    
    self.visual.show_happy("AI Assistant ready!")
    
    if hasattr(self.visual, 'run_gui'):
        # GUI mode: run AI operations in background
        ai_thread = threading.Thread(target=self._run_main_loop, daemon=True)
        ai_thread.start()
        
        try:
            self.visual.run_gui()  # Run GUI on main thread
        except KeyboardInterrupt:
            self.stop()
    else:
        # Non-GUI mode: run normally
        self._run_main_loop()

def _run_main_loop(self):
    # Move existing run() logic here
    while self.running:
        # ... existing main loop ...
```

📋 Step 4: Add State Changes Throughout Code
-------------------------------------------
Add visual feedback calls at key points:

```python
# When listening for wake word
self.visual.show_listening("Listening for wake word...")

# When wake word detected
self.visual.show_happy("Wake word detected!")

# When listening for user input
self.visual.show_listening("I'm listening...")

# When processing with OpenAI
self.visual.show_thinking("Let me think about that...")

# When speaking/responding
self.visual.show_speaking("Here's what I found...")

# When user gets something right in games
self.visual.show_happy("Great job!")

# When there's an error
self.visual.show_error("Oops! Let me try again.")

# Back to standby
self.visual.show_standby("Ready for next question!")
```

📋 Step 5: Update speak() method
-------------------------------
Integrate with existing speech:

```python
def speak(self, text: str, user: Optional[str] = None):
    # Show speaking state
    self.visual.show_speaking("Speaking...")
    
    # ... existing speech logic ...
    
    # Back to standby when done
    if not self.ai_speaking:
        self.visual.show_standby("Ready to help!")
```

📋 Step 6: Update Educational Games
----------------------------------
Add visual feedback to games:

```python
# In spelling game
def start_spelling_game(self, user: str) -> str:
    self.visual.show_happy("Let's play a spelling game!")
    # ... existing logic ...

def check_spelling_answer(self, user: str) -> str:
    self.visual.show_thinking("Checking your spelling...")
    # ... check logic ...
    
    if correct:
        self.visual.show_happy("Perfect! Great spelling!")
    else:
        self.visual.show_error("Not quite right. Let's try again!")
```

📋 Step 7: Update stop() method
------------------------------
Clean shutdown:

```python
def stop(self):
    self.visual.show_sleeping("Goodbye!")
    
    # ... existing cleanup ...
    
    if hasattr(self.visual, 'stop'):
        self.visual.stop()
```

🔧 Environment Variables for Raspberry Pi
========================================
Set these in your .bashrc or startup script:

```bash
export ROBOT_TYPE=pi_7inch          # or pi_5inch, desktop, minimal
export ROBOT_DISPLAY_WIDTH=800      # Display width
export ROBOT_DISPLAY_HEIGHT=480     # Display height  
export ROBOT_FULLSCREEN=true        # Full screen mode
export ROBOT_USE_GUI=true           # Enable GUI
export ROBOT_ANIMATIONS=true        # Enable animations
```

📱 Hardware Recommendations
==========================
- 7-inch touchscreen: 800x480 resolution
- 5-inch display: 800x480 resolution  
- HDMI displays: 1024x768 or higher
- Memory: At least 2GB RAM for smooth animations
- GPU: Hardware acceleration recommended

🎨 Customization Options
=======================
- Colors: Edit visual_config.py or use environment variables
- Face size: Adjust ROBOT_FACE_SIZE
- Messages: Customize default messages
- Animations: Enable/disable or adjust FPS
- Layout: Modify visual_feedback.py for custom layouts

✅ Testing
=========
Run the tests to verify integration:

```bash
cd tests
python test_visual_integration.py
python test_visual_feedback.py
```

🚀 Deployment
============
1. Copy visual_feedback.py and visual_config.py to your robot
2. Update main.py with the integration code above
3. Set environment variables for your display
4. Test with minimal mode first, then enable GUI
5. For production: set ROBOT_FULLSCREEN=true

That's it! Your robot will now have cute visual feedback! 🤖✨
"""
    
    print(guide)


def main():
    """Main demo function."""
    print("🤖 Visual Feedback Integration Example")
    print("=" * 45)
    
    while True:
        print("\nChoose an option:")
        print("1. Run Integration Demo (Full AI Simulation)")
        print("2. Show Integration Guide (Step-by-step)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\n🚀 Starting Full AI Assistant Simulation with Visual Feedback...")
            print("This demonstrates exactly how the visual feedback integrates!")
            
            ai = AIAssistantWithVisualFeedback()
            try:
                ai.start()
            except KeyboardInterrupt:
                ai.stop()
                
        elif choice == '2':
            show_integration_guide()
            
        elif choice == '3':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 