#!/usr/bin/env python3
"""
Display Manager Demo for AI Assistant Robot
Demonstrates the visual feedback system for different AI states
Run this to see what the screen will look like on your Raspberry Pi
"""

import signal
import sys
import time
from display_manager import DisplayManager, AIState

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\nShutting down display demo...")
    display.stop_display()
    sys.exit(0)

def main():
    """Run the display demo."""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🤖 AI Assistant Display Demo")
    print("=" * 40)
    print("This demonstrates the visual feedback system")
    print("that will show on your Raspberry Pi screen.")
    print("Press Ctrl+C to exit")
    print()
    
    # Create display manager
    # For Raspberry Pi, use smaller resolution and fullscreen=True
    display = DisplayManager(
        screen_width=800,   # Use 800x600 for demo, 480x320 for Pi
        screen_height=600,  # Use 600 for demo, 320 for Pi
        fullscreen=False    # Set to True for fullscreen on Pi
    )
    
    # Start the display
    display.start_display()
    
    # Demo sequence showing different AI states
    demo_states = [
        # (state, user, message, duration)
        (AIState.STANDBY, None, "AI Assistant Ready - Say wake word or step in front of camera", 3),
        (AIState.LISTENING, "Sophia", "Waiting for voice input from Sophia", 2),
        (AIState.PROCESSING, "Sophia", "Processing: Hello, can you help me with math?", 2),
        (AIState.SPEAKING, "Sophia", "Speaking: Hi Sophia! I'd be happy to help you with math!", 3),
        (AIState.GAME_ACTIVE, "Sophia", "Letter Word Game: Guess the word that starts with 'B'!", 4),
        (AIState.LISTENING, "Sophia", "Listening for your answer...", 2),
        (AIState.SPEAKING, "Sophia", "Speaking: Great job! That's correct!", 2),
        (AIState.STANDBY, "Sophia", "Ready for next interaction", 2),
        
        # Switch to Eladriel
        (AIState.LISTENING, "Eladriel", "Dinosaur expert mode - Waiting for Eladriel", 2),
        (AIState.PROCESSING, "Eladriel", "Processing: What dinosaur is this?", 2),
        (AIState.SPEAKING, "Eladriel", "Speaking: That's a Triceratops! It has three horns!", 3),
        (AIState.GAME_ACTIVE, "Eladriel", "Animal Guessing Game: Show me your dinosaur!", 3),
        (AIState.STANDBY, "Eladriel", "Ready for more dinosaur fun!", 2),
        
        # Parent mode
        (AIState.PROCESSING, "Parent", "Processing parent command: system status", 2),
        (AIState.SPEAKING, "Parent", "Speaking: All systems operational. Kids are learning!", 3),
        (AIState.STANDBY, "Parent", "Parent mode - Quiet time active", 2),
        
        # Error demonstration
        (AIState.ERROR, None, "Microphone connection lost - reconnecting...", 3),
        (AIState.STANDBY, None, "System recovered - Ready for interaction", 2),
    ]
    
    print("🎬 Starting demo sequence...")
    print("You'll see different AI states on the display:")
    print("  • STANDBY (Blue) - Ready and waiting")
    print("  • LISTENING (Green) - Actively listening for speech")
    print("  • PROCESSING (Purple) - Thinking about your request")
    print("  • SPEAKING (Orange) - AI is talking")
    print("  • GAME_ACTIVE (Cyan) - Educational game in progress")
    print("  • ERROR (Red) - System issue detected")
    print()
    
    try:
        # Run through the demo sequence
        for i, (state, user, message, duration) in enumerate(demo_states):
            print(f"📺 Demo {i+1}/{len(demo_states)}: {state.value.upper()}", end="")
            if user:
                print(f" (User: {user})", end="")
            print(f" - {message[:50]}...")
            
            # Update display
            display.set_state(state, user, message)
            
            # Wait for the specified duration
            time.sleep(duration)
        
        print()
        print("🎯 Demo sequence completed!")
        print("The display will now cycle through states continuously...")
        print("This is what you'll see on your Raspberry Pi robot!")
        print()
        print("Integration features:")
        print("  ✅ Real-time state updates")
        print("  ✅ User-specific information display")
        print("  ✅ Game status tracking")
        print("  ✅ Error state visualization")
        print("  ✅ Animated visual effects")
        print("  ✅ Timestamp and current user info")
        print()
        print("Press Ctrl+C to stop the demo")
        
        # Continuous cycle for testing
        cycle_states = [
            (AIState.STANDBY, None, "Ready - Looking for interaction"),
            (AIState.LISTENING, "Sophia", "Listening for Sophia's voice"),
            (AIState.PROCESSING, "Sophia", "Understanding Sophia's request"),
            (AIState.SPEAKING, "Sophia", "Responding to Sophia"),
            (AIState.GAME_ACTIVE, "Sophia", "Letter Word Game active"),
        ]
        
        cycle_index = 0
        while True:
            state, user, message = cycle_states[cycle_index]
            display.set_state(state, user, message)
            cycle_index = (cycle_index + 1) % len(cycle_states)
            time.sleep(3)
    
    except KeyboardInterrupt:
        pass
    finally:
        display.stop_display()
        print("\n🏁 Display demo completed!")
        print("To use this on your Raspberry Pi:")
        print("1. Install pygame: pip install pygame")
        print("2. Set fullscreen=True in DisplayManager")
        print("3. Adjust screen_width and screen_height for your display")
        print("4. The display will automatically start with your AI assistant!")

if __name__ == "__main__":
    main() 