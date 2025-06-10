#!/usr/bin/env python3
"""
Test Visual Feedback Integration
Shows how to integrate visual feedback with the AI Assistant
"""

import sys
import os
import time
import threading

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visual_feedback import create_visual_feedback


class MockAIAssistant:
    """Mock AI Assistant to demonstrate visual feedback integration."""
    
    def __init__(self, use_visual_gui=True):
        """Initialize mock AI with visual feedback."""
        self.visual = create_visual_feedback(use_gui=use_visual_gui)
        self.running = False
        
        print(f"🤖 Mock AI Assistant initialized with {type(self.visual).__name__}")
    
    def start(self):
        """Start the AI assistant with visual feedback."""
        print("🚀 Starting AI Assistant with Visual Feedback...")
        
        self.running = True
        
        # Start visual feedback
        if hasattr(self.visual, 'start'):
            self.visual.start()
        
        # Show startup
        self.visual.show_standby("Starting up...")
        
        # For GUI systems, we need to handle the startup differently
        if hasattr(self.visual, 'run_gui'):
            # Start a demo in background thread
            def startup_demo():
                time.sleep(2)
                self.visual.show_happy("AI Assistant ready!")
                time.sleep(2)
                print("✅ AI Assistant started successfully!")
            
            demo_thread = threading.Thread(target=startup_demo, daemon=True)
            demo_thread.start()
        else:
            time.sleep(2)
            self.visual.show_happy("AI Assistant ready!")
            time.sleep(2)
            print("✅ AI Assistant started successfully!")
    
    def simulate_conversation(self):
        """Simulate a full conversation with visual feedback."""
        print("\n🗣️ Simulating conversation with visual feedback...")
        
        # Wake word detection
        self.visual.show_listening("Listening for wake word...")
        time.sleep(2)
        
        self.visual.show_happy("Wake word detected!")
        time.sleep(1)
        
        # User interaction
        self.visual.show_listening("I'm listening! What can I help you with?")
        time.sleep(3)
        
        # Processing user request
        self.visual.show_thinking("Let me think about that...")
        time.sleep(2)
        
        # Responding
        self.visual.show_speaking("Here's what I found for you! The weather today is sunny with a high of 75 degrees.")
        time.sleep(4)
        
        # Follow-up
        self.visual.show_listening("Is there anything else you'd like to know?")
        time.sleep(3)
        
        # End conversation
        self.visual.show_happy("Great chatting with you!")
        time.sleep(2)
        
        self.visual.show_standby("Ready for next interaction")
        
        print("✅ Conversation simulation complete!")
    
    def simulate_educational_game(self):
        """Simulate educational game with visual feedback."""
        print("\n🎮 Simulating educational game with visual feedback...")
        
        # Game start
        self.visual.show_happy("Let's play a learning game!")
        time.sleep(2)
        
        # Spelling game
        self.visual.show_speaking("I'm thinking of an animal that says 'meow'. Can you spell it?")
        time.sleep(4)
        
        self.visual.show_listening("Take your time spelling...")
        time.sleep(4)
        
        # Checking answer
        self.visual.show_thinking("Let me check your spelling...")
        time.sleep(2)
        
        # Correct answer
        self.visual.show_happy("Perfect! C-A-T is correct! Great job!")
        time.sleep(3)
        
        # Next question
        self.visual.show_speaking("Now let's try a math problem. What's 2 + 3?")
        time.sleep(3)
        
        self.visual.show_listening("I'm listening for your answer...")
        time.sleep(3)
        
        # Checking math
        self.visual.show_thinking("Calculating...")
        time.sleep(1)
        
        self.visual.show_happy("Excellent! 5 is correct! You're so smart!")
        time.sleep(3)
        
        # Game end
        self.visual.show_happy("You did amazing in our learning game!")
        time.sleep(2)
        
        self.visual.show_standby("Ready for more learning!")
        
        print("✅ Educational game simulation complete!")
    
    def simulate_error_handling(self):
        """Simulate error scenarios with visual feedback."""
        print("\n⚠️ Simulating error handling with visual feedback...")
        
        # Connection error
        self.visual.show_error("Oops! I lost my internet connection.")
        time.sleep(3)
        
        self.visual.show_thinking("Let me try to reconnect...")
        time.sleep(2)
        
        self.visual.show_happy("Connection restored! I'm back!")
        time.sleep(2)
        
        # Speech recognition error
        self.visual.show_error("Sorry, I didn't quite catch that.")
        time.sleep(2)
        
        self.visual.show_listening("Could you please repeat that?")
        time.sleep(3)
        
        self.visual.show_happy("Got it! Thanks for being patient!")
        time.sleep(2)
        
        # Camera error
        self.visual.show_error("My camera seems to be having trouble.")
        time.sleep(2)
        
        self.visual.show_thinking("Let me restart the camera...")
        time.sleep(2)
        
        self.visual.show_happy("Camera is working again!")
        time.sleep(2)
        
        self.visual.show_standby("Everything is back to normal!")
        
        print("✅ Error handling simulation complete!")
    
    def simulate_daily_interactions(self):
        """Simulate typical daily interactions."""
        print("\n📅 Simulating daily interactions with visual feedback...")
        
        interactions = [
            ("Morning greeting", [
                ('happy', "Good morning! Ready for a great day?", 3),
                ('listening', "What would you like to do first?", 3)
            ]),
            ("Homework help", [
                ('speaking', "Let's work on your homework together!", 3),
                ('listening', "What subject are we studying today?", 3),
                ('thinking', "Let me prepare some practice problems...", 2),
                ('happy', "I've got some fun exercises for you!", 3)
            ]),
            ("Story time", [
                ('speaking', "Would you like to hear a story?", 2),
                ('thinking', "Let me think of a good one...", 2),
                ('speaking', "Once upon a time, in a magical forest...", 4),
                ('happy', "Did you like that story?", 2)
            ]),
            ("Bedtime routine", [
                ('speaking', "It's getting late. Time to get ready for bed!", 3),
                ('happy', "You had such a wonderful day!", 3),
                ('speaking', "Sweet dreams! I'll see you tomorrow!", 3),
                ('sleeping', "Going to sleep mode...", 2)
            ])
        ]
        
        for interaction_name, steps in interactions:
            print(f"\n   📝 {interaction_name}:")
            for state, message, duration in steps:
                print(f"      {state.upper()}: {message}")
                self.visual.set_state(state, message)
                time.sleep(duration)
            time.sleep(1)
        
        print("✅ Daily interactions simulation complete!")
    
    def stop(self):
        """Stop the AI assistant."""
        print("\n🛑 Stopping AI Assistant...")
        
        self.visual.show_sleeping("Goodbye! See you later!")
        time.sleep(2)
        
        self.running = False
        
        if hasattr(self.visual, 'stop'):
            self.visual.stop()
        
        print("✅ AI Assistant stopped.")


def test_integration_gui():
    """Test integration with GUI."""
    print("🖥️ Testing Visual Feedback Integration (GUI)")
    
    ai = MockAIAssistant(use_visual_gui=True)
    ai.start()
    
    # If it's a GUI system, run all simulations in background
    if hasattr(ai.visual, 'run_gui'):
        def run_all_simulations():
            time.sleep(3)  # Wait for startup
            
            # Run all simulations
            ai.simulate_conversation()
            time.sleep(1)
            
            ai.simulate_educational_game()
            time.sleep(1)
            
            ai.simulate_error_handling()
            time.sleep(1)
            
            ai.simulate_daily_interactions()
            
            print("\n✨ All simulations complete!")
            print("Close the window to finish the test.")
        
        # Start simulations in background
        sim_thread = threading.Thread(target=run_all_simulations, daemon=True)
        sim_thread.start()
        
        # Run GUI on main thread
        try:
            ai.visual.run_gui()
        except KeyboardInterrupt:
            ai.stop()
    else:
        # For non-GUI systems, run normally
        try:
            # Run all simulations
            ai.simulate_conversation()
            time.sleep(1)
            
            ai.simulate_educational_game()
            time.sleep(1)
            
            ai.simulate_error_handling()
            time.sleep(1)
            
            ai.simulate_daily_interactions()
            
            print("\n✨ All simulations complete!")
                
        except KeyboardInterrupt:
            ai.stop()


def test_integration_minimal():
    """Test integration with minimal console output."""
    print("📝 Testing Visual Feedback Integration (Console)")
    
    ai = MockAIAssistant(use_visual_gui=False)
    ai.start()
    
    # Run quick simulations
    ai.simulate_conversation()
    ai.simulate_educational_game()
    ai.simulate_error_handling()
    
    ai.stop()


def demonstration_guide():
    """Show integration guide for developers."""
    guide = """
🤖 AI Assistant Visual Feedback Integration Guide
===============================================

1. 📦 Import the visual feedback system:
   ```python
   from visual_feedback import create_visual_feedback
   ```

2. 🚀 Initialize in your AI Assistant __init__:
   ```python
   def __init__(self):
       # Other initialization...
       self.visual = create_visual_feedback(use_gui=True)  # or False for minimal
   ```

3. 🏁 Start the visual system:
   ```python
   def start(self):
       self.visual.start()
       self.visual.show_standby("AI Assistant ready!")
   ```

4. 🎯 Use state changes throughout your code:
   ```python
   # When listening for wake word
   self.visual.show_listening("Listening for wake word...")
   
   # When processing user input
   self.visual.show_thinking("Processing your request...")
   
   # When speaking/responding
   self.visual.show_speaking("Here's what I found...")
   
   # When user gets something right
   self.visual.show_happy("Great job!")
   
   # When there's an error
   self.visual.show_error("Oops! Let me try again.")
   ```

5. 🛑 Clean shutdown:
   ```python
   def stop(self):
       self.visual.show_sleeping("Goodbye!")
       self.visual.stop()
   ```

📱 Raspberry Pi Setup:
=====================
- For full screen: Uncomment the fullscreen line in visual_feedback.py
- Recommended resolution: 800x480 (7-inch display) or 1024x600
- Touch screen compatible
- Automatically falls back to console mode if GUI fails

🎨 Available States:
==================
- standby: Ready/waiting state (blue)
- listening: Actively listening (green, pulsing)
- speaking: Talking/responding (orange, mouth animation)
- thinking: Processing (purple, eye movement)
- happy: Success/celebration (green)
- error: Problem occurred (red)
- sleeping: Inactive/shutdown (gray)

🔧 Customization:
================
- Colors: Edit the colors dictionary in RobotFace class
- Animations: Modify the animate_* methods
- Size: Change the size parameter when creating RobotFace
- Messages: Use set_message() to update text without changing state
"""
    
    print(guide)


def main():
    """Main test menu."""
    print("🤖 AI Assistant Visual Feedback Integration Tests")
    print("=" * 55)
    
    while True:
        print("\nChoose a test:")
        print("1. GUI Integration Demo (Full Visual)")
        print("2. Console Integration Demo (Minimal)")
        print("3. Integration Guide for Developers")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            test_integration_gui()
        elif choice == '2':
            test_integration_minimal()
        elif choice == '3':
            demonstration_guide()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 