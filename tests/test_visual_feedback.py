#!/usr/bin/env python3
"""
Test Visual Feedback System
Demonstrates all the cute robot faces and animations
"""

import sys
import os
import time
import threading

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visual_feedback import VisualFeedbackSystem, MinimalVisualFeedback, create_visual_feedback


def test_full_visual_system():
    """Test the full GUI visual feedback system."""
    print("🤖 Testing Full Visual Feedback System with GUI")
    print("You should see a window with an animated robot face!")
    
    # Create visual feedback system
    visual = VisualFeedbackSystem(width=800, height=600)
    
    # Start the system (creates UI)
    visual.start()
    
    # Test different states with animations in a separate thread
    def state_demo():
        test_states = [
            ('standby', "Ready to help!", 3),
            ('listening', "I'm listening for your voice...", 4),
            ('thinking', "Let me think about that...", 3),
            ('speaking', "Here's what I found for you!", 4),
            ('happy', "Great job! You're amazing!", 3),
            ('error', "Oops! Let me try that again.", 2),
            ('sleeping', "Taking a quick nap...", 3),
            ('standby', "Back to normal!", 2)
        ]
        
        print("\n🎭 Demonstrating different robot states:")
        
        for state, message, duration in test_states:
            print(f"   {state.upper()}: {message}")
            visual.set_state(state, message)
            time.sleep(duration)
        
        print("\n✨ Demo complete! The robot should be back to standby.")
        print("Close the window to finish the test.")
    
    # Start demo in background thread
    demo_thread = threading.Thread(target=state_demo, daemon=True)
    demo_thread.start()
    
    # Run GUI on main thread (blocking)
    try:
        visual.run_gui()
    except KeyboardInterrupt:
        visual.stop()


def test_minimal_visual_system():
    """Test the minimal console-based visual feedback."""
    print("🤖 Testing Minimal Visual Feedback System (Console Only)")
    print("You should see emoji status indicators in the console.")
    
    # Create minimal visual feedback
    visual = MinimalVisualFeedback()
    visual.start()
    
    # Test different states
    test_states = [
        ('standby', "Ready to help!"),
        ('listening', "I'm listening for your voice..."),
        ('thinking', "Let me think about that..."),
        ('speaking', "Here's what I found for you!"),
        ('happy', "Great job! You're amazing!"),
        ('error', "Oops! Let me try that again."),
        ('sleeping', "Taking a quick nap..."),
        ('standby', "Back to normal!")
    ]
    
    print("\n🎭 Demonstrating different robot states:")
    
    for state, message in test_states:
        visual.set_state(state, message)
        time.sleep(2)
    
    visual.stop()
    print("✨ Minimal feedback demo complete!")


def test_animated_demo():
    """Test animated demo showing robot personality."""
    print("🤖 Testing Animated Robot Personality Demo")
    
    # Create visual feedback system
    visual = VisualFeedbackSystem(width=800, height=600)
    visual.start()
    
    # Simulate a conversation scenario
    def conversation_demo():
        conversation_flow = [
            ('standby', "Hi! I'm your AI robot assistant!", 2),
            ('listening', "Say something to me...", 3),
            ('thinking', "Hmm, that's interesting...", 2),
            ('speaking', "I think I understand!", 3),
            ('happy', "You're so smart!", 2),
            ('listening', "What else would you like to know?", 3),
            ('thinking', "Let me process that...", 2),
            ('speaking', "Here's what I think...", 3),
            ('happy', "I love helping you learn!", 2),
            ('sleeping', "Time for a quick rest...", 2),
            ('standby', "Ready for more adventures!", 1)
        ]
        
        print("\n🎬 Playing conversation simulation:")
        
        for state, message, duration in conversation_flow:
            print(f"   🤖 {state.upper()}: {message}")
            visual.set_state(state, message)
            time.sleep(duration)
        
        print("\n✨ Conversation demo complete!")
        print("Close the window to finish.")
    
    # Start demo in background
    demo_thread = threading.Thread(target=conversation_demo, daemon=True)
    demo_thread.start()
    
    # Run GUI
    try:
        visual.run_gui()
    except KeyboardInterrupt:
        visual.stop()


def test_game_states():
    """Test visual feedback during educational games."""
    print("🎮 Testing Visual Feedback for Educational Games")
    
    visual = VisualFeedbackSystem(width=800, height=600)
    visual.start()
    
    # Simulate a spelling game
    def game_demo():
        spelling_game = [
            ('standby', "Let's play a spelling game!", 2),
            ('speaking', "Can you spell the word 'CAT'?", 3),
            ('listening', "I'm listening for your answer...", 4),
            ('thinking', "Let me check your spelling...", 2),
            ('happy', "Perfect! C-A-T is correct!", 3),
            ('speaking', "Now try spelling 'DOG'!", 3),
            ('listening', "Take your time...", 4),
            ('thinking', "Checking your answer...", 2),
            ('happy', "Excellent work! You're a spelling star!", 3),
            ('standby', "Ready for the next challenge!", 2)
        ]
        
        print("\n📝 Simulating spelling game:")
        
        for state, message, duration in spelling_game:
            print(f"   📚 {message}")
            visual.set_state(state, message)
            time.sleep(duration)
        
        print("\n✨ Game simulation complete!")
        print("Close the window to finish.")
    
    # Start demo in background
    demo_thread = threading.Thread(target=game_demo, daemon=True)
    demo_thread.start()
    
    try:
        visual.run_gui()
    except KeyboardInterrupt:
        visual.stop()


def test_factory_function():
    """Test the factory function for creating visual feedback."""
    print("🏭 Testing Visual Feedback Factory Function")
    
    # Test GUI creation
    print("   Creating GUI version...")
    visual_gui = create_visual_feedback(use_gui=True)
    print(f"   Created: {type(visual_gui).__name__}")
    
    # Test minimal creation
    print("   Creating minimal version...")
    visual_minimal = create_visual_feedback(use_gui=False)
    print(f"   Created: {type(visual_minimal).__name__}")
    
    # Quick test of both
    print("\n   Testing both systems:")
    
    visual_minimal.show_standby("Minimal system ready!")
    time.sleep(1)
    
    if hasattr(visual_gui, 'start'):
        visual_gui.start()
        visual_gui.show_happy("GUI system ready!")
        
        def quick_demo():
            time.sleep(2)
            visual_gui.show_thinking("Testing factory...")
            time.sleep(2)
            visual_gui.show_standby("Factory test complete!")
            time.sleep(2)
            visual_gui.stop()
        
        demo_thread = threading.Thread(target=quick_demo, daemon=True)
        demo_thread.start()
        
        try:
            visual_gui.run_gui()
        except:
            pass
    
    print("✨ Factory function test complete!")


def main():
    """Main test function with menu."""
    print("🤖 AI Robot Visual Feedback System Tests")
    print("=" * 50)
    
    while True:
        print("\nChoose a test to run:")
        print("1. Full Visual System (GUI with animations)")
        print("2. Minimal Visual System (console only)")
        print("3. Animated Conversation Demo")
        print("4. Educational Game States Demo")
        print("5. Factory Function Test")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            test_full_visual_system()
        elif choice == '2':
            test_minimal_visual_system()
        elif choice == '3':
            test_animated_demo()
        elif choice == '4':
            test_game_states()
        elif choice == '5':
            test_factory_function()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 