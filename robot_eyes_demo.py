#!/usr/bin/env python3
"""
Simple Robot Eyes Demo - Inspired by Loona Pet AI
Black and white expressive robot eyes that react to speech, listening, and standby states
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_feedback import create_visual_feedback
import time
import threading

def main():
    print("🤖 SIMPLE ROBOT EYES DEMO")
    print("=" * 50)
    print("✨ Inspired by Loona Pet AI")
    print("👀 Simple black and white expressive eyes")
    print("🎭 Emotional reactions to different states")
    print("=" * 50)
    
    # Create the simple robot eyes system
    visual = create_visual_feedback(use_gui=True)
    
    # Start the visual system
    print("\n🚀 Starting robot eyes...")
    visual.start()
    print("✅ Robot eyes activated!")
    
    def demo_sequence():
        """Demonstrate the robot eyes in action."""
        time.sleep(2)
        
        print("\n🎭 ROBOT EYES EMOTIONAL SHOWCASE:")
        print("-" * 40)
        
        states = [
            ("standby", "💤 STANDBY - Calm and ready", "Hello! I'm ready to help you."),
            ("listening", "👂 LISTENING - Attentive and alert", "I'm listening carefully..."),
            ("thinking", "🤔 THINKING - Looking up thoughtfully", "Hmm, let me think about that..."),
            ("speaking", "💬 SPEAKING - Animated blinking", "I'm speaking to you right now!"),
            ("happy", "😊 HAPPY - Sparkles and joy", "Wonderful! I'm so happy to help! ✨"),
            ("error", "😕 ERROR - Looking down sadly", "Oops, something went wrong..."),
            ("standby", "💤 BACK TO STANDBY - Ready again", "Ready for the next interaction!")
        ]
        
        for state, description, message in states:
            print(f"\n{description}")
            visual.set_state(state, message)
            time.sleep(3)
        
        print("\n🎨 SPECIAL ANIMATIONS:")
        print("-" * 25)
        
        # Test speaking animation
        print("💬 Testing speaking animation...")
        visual.start_speaking()
        visual.set_message("Watch my eyes blink and move while I speak!")
        time.sleep(4)
        visual.stop_speaking()
        
        # Test listening animation
        print("👂 Testing listening animation...")
        visual.show_listening("I'm pulsing gently while listening...")
        time.sleep(3)
        
        # Test happy sparkles
        print("✨ Testing happy sparkles...")
        visual.show_happy("Look at the sparkles! ✨🎉✨")
        time.sleep(3)
        
        print("\n🎯 Demo complete! The robot eyes are ready for real use.")
        print("🔧 Integration: Use create_visual_feedback() in your main app")
        print("📱 Close the window when you're done exploring!")
        
        visual.show_standby("Demo complete! Close window to exit.")
    
    # Start demo in background
    demo_thread = threading.Thread(target=demo_sequence, daemon=True)
    demo_thread.start()
    
    # Run GUI
    try:
        visual.run_gui()
    except KeyboardInterrupt:
        visual.stop()

if __name__ == "__main__":
    main() 