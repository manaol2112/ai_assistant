#!/usr/bin/env python3
"""
Display Integration Demo
Shows how the AI Assistant uses the display manager for visual feedback
"""

import time
import signal
import sys
from main import AIAssistant
from display_manager import AIState

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\n🛑 Demo stopped by user")
    sys.exit(0)

def main():
    """Demonstrate display integration with AI Assistant."""
    print("\n" + "="*60)
    print("🤖 AI ASSISTANT DISPLAY INTEGRATION DEMO")
    print("📺 Watch the console for visual state feedback")
    print("⚡ This simulates what would appear on your robot's screen")
    print("="*60)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Initialize AI Assistant (this includes display manager)
        print("\n🔄 Initializing AI Assistant with display...")
        ai = AIAssistant()
        
        # Start the display manager
        print("📺 Starting display manager...")
        ai.display_manager.start_display()
        
        print("\n🎬 Starting demo sequence...")
        print("   (In real usage, these states change automatically)")
        
        # Demo sequence showing different states
        demos = [
            (AIState.STANDBY, None, "AI ready for interaction"),
            (AIState.LISTENING, "Sophia", "Waiting for voice input..."),
            (AIState.PROCESSING, "Sophia", "Analyzing: 'What's 5 plus 3?'"),
            (AIState.SPEAKING, "Sophia", "5 plus 3 equals 8! Great question!"),
            (AIState.GAME_ACTIVE, "Eladriel", "Playing Letter Word Game"),
            (AIState.LISTENING, "Eladriel", "Your turn to guess the word"),
            (AIState.PROCESSING, "Eladriel", "Checking answer: 'elephant'"),
            (AIState.SPEAKING, "Eladriel", "Excellent! That's correct!"),
            (AIState.ERROR, None, "Microphone connection lost"),
            (AIState.STANDBY, None, "Error resolved - ready again"),
        ]
        
        for i, (state, user, message) in enumerate(demos, 1):
            print(f"\n[{i}/{len(demos)}] Setting state: {state.value.upper()}")
            ai.display_manager.set_state(state, user, message)
            time.sleep(2)  # Pause to see each state
        
        print("\n✅ Demo completed!")
        print("\n📝 INTEGRATION FEATURES:")
        print("   🔄 Real-time state updates")
        print("   👤 User-specific information display")
        print("   🎮 Game mode indicators")
        print("   ⚠️  Error state handling")
        print("   🎨 Color-coded visual feedback")
        print("   📱 Cross-platform compatibility")
        
        print("\n🚀 READY FOR RASPBERRY PI:")
        print("   • Copy this project to your Pi")
        print("   • Install: pip install -r requirements_display.txt")
        print("   • Run: python3 main.py")
        print("   • Enjoy visual feedback on your robot's screen!")
        
        # Stop display
        print("\n🛑 Stopping display manager...")
        ai.display_manager.stop_display()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
    finally:
        print("🔚 Demo finished")

if __name__ == "__main__":
    main() 