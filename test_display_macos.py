#!/usr/bin/env python3
"""
Test script for Display Manager on macOS
This script will open a visible window to test the display functionality.
"""

import time
import signal
import sys
from display_manager import DisplayManager, AIState

def signal_handler(sig, frame):
    print("\nShutting down display test...")
    if 'display' in globals():
        display.stop_display()
    sys.exit(0)

def main():
    print("🖥️  Starting AI Assistant Display Test for macOS")
    print("This will open a visible window to test the display functionality")
    print("Press Ctrl+C to exit")
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create display manager with a larger, more visible window
    display = DisplayManager(screen_width=600, screen_height=400, fullscreen=False)
    
    try:
        # Start display
        print("📺 Starting display...")
        display.start_display()
        
        # Give it a moment to initialize
        time.sleep(1)
        
        # Test different states with visible feedback
        states_to_test = [
            (AIState.STANDBY, None, "AI Assistant Ready - Testing macOS Display"),
            (AIState.LISTENING, "TestUser", "Microphone is listening for your voice"),
            (AIState.PROCESSING, "TestUser", "AI is thinking about your request"),
            (AIState.SPEAKING, "TestUser", "AI is speaking the response"),
            (AIState.GAME_ACTIVE, "TestUser", "Playing an educational game"),
            (AIState.ERROR, None, "Error state demonstration"),
        ]
        
        print("\n🎮 Testing display states...")
        for i, (state, user, message) in enumerate(states_to_test):
            print(f"   State {i+1}/{len(states_to_test)}: {state.value}")
            display.set_state(state, user, message)
            time.sleep(3)  # Show each state for 3 seconds
        
        print("\n✅ Display test completed successfully!")
        print("💡 If you can see the window changing states, the display is working correctly!")
        print("🔄 The test will continue cycling through states. Press Ctrl+C to stop.")
        
        # Continuous cycle for extended testing
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"\n🔄 Cycle {cycle_count} - Press Ctrl+C to stop")
            
            for state, user, message in states_to_test:
                display.set_state(state, user, f"Cycle {cycle_count}: {message}")
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during display test: {e}")
    finally:
        print("🔧 Cleaning up...")
        display.stop_display()
        print("✅ Display test completed")

if __name__ == "__main__":
    main() 