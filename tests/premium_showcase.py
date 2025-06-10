#!/usr/bin/env python3
"""
Premium Visual Feedback Showcase
Demonstrates the billion-dollar quality robot faces with advanced animations
"""

import sys
import os
import time
import threading

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visual_feedback import create_visual_feedback, PremiumVisualFeedbackSystem

def showcase_premium_dinosaur():
    """Showcase the premium dinosaur (Eladriel) with all features."""
    print("🦕 PREMIUM DINOSAUR SHOWCASE")
    print("=" * 50)
    print("Features:")
    print("✨ Crystalline horns with metallic effects")
    print("👁️ Expressive eyes with depth and life")
    print("💬 Advanced mouth animation system")
    print("🎭 Emotional intelligence with smooth transitions")
    print("🌟 Premium particle effects and celebrations")
    print("💫 Ambient effects and sound visualization")
    print("=" * 50)
    
    try:
        # Create premium dinosaur system
        system = PremiumVisualFeedbackSystem(
            width=1000,
            height=700,
            current_user="eladriel"
        )
        
        print("\n🎬 Starting Eladriel Premium Experience...")
        
        # Schedule premium demonstration
        def premium_demo():
            time.sleep(1)
            system.show_standby("🦕 Greetings! I'm Eladriel, your premium dinosaur assistant!")
            
            time.sleep(4)
            system.show_listening("🎧 My advanced sensors are picking up your voice perfectly...")
            
            time.sleep(4)
            system.show_thinking("🧠 Processing with millions of years of dinosaur wisdom...")
            
            time.sleep(4)
            system.show_speaking("🗣️ Watch my mouth move naturally as I communicate!")
            
            time.sleep(5)
            system.show_happy("🌟 ROAR! I'm absolutely thrilled to demonstrate my capabilities!")
            
            time.sleep(4)
            print("\n🎭 Demonstrating emotional transitions...")
            
            # Cycle through emotions
            emotions = [
                ("thinking", "🤔 Deep contemplation..."),
                ("listening", "👂 Focused attention..."),
                ("speaking", "💬 Expressive communication!"),
                ("happy", "😊 Pure dinosaur joy!"),
                ("standby", "✨ Ready for adventure!")
            ]
            
            for emotion, message in emotions:
                time.sleep(2)
                system.set_state(emotion, message)
            
            time.sleep(3)
            system.show_standby("🦕 Premium dinosaur experience complete! ROAR! 🌟")
        
        # Run demo in background
        demo_thread = threading.Thread(target=premium_demo, daemon=True)
        demo_thread.start()
        
        # Start the GUI
        system.start()
        
    except Exception as e:
        print(f"Error running premium demo: {e}")
        print("Running console fallback...")
        run_console_showcase("eladriel")

def showcase_premium_girl_robot():
    """Showcase the premium girl robot (Sophia) with all features."""
    print("🤖 PREMIUM GIRL ROBOT SHOWCASE")
    print("=" * 50)
    print("Features:")
    print("✨ Elegant bow with sparkle effects")
    print("👁️ Beautiful eyes with multiple highlights")
    print("💄 Gorgeous eyelashes and rosy cheeks")
    print("💬 Advanced emotional mouth animations")
    print("🎨 Sophisticated color schemes and gradients")
    print("💖 Premium celebration and particle effects")
    print("🌸 Graceful transitions and micro-expressions")
    print("=" * 50)
    
    try:
        # Create premium girl robot system
        system = PremiumVisualFeedbackSystem(
            width=1000,
            height=700,
            current_user="sophia"
        )
        
        print("\n💖 Starting Sophia Premium Experience...")
        
        # Schedule premium demonstration
        def premium_demo():
            time.sleep(1)
            system.show_standby("👋 Hello beautiful! I'm Sophia, your premium AI companion!")
            
            time.sleep(4)
            system.show_listening("💫 I'm listening with perfect attention and emotional intelligence...")
            
            time.sleep(4)
            system.show_thinking("💭 Processing with grace, wisdom, and advanced AI reasoning...")
            
            time.sleep(4)
            system.show_speaking("💬 Notice how my mouth moves naturally with emotional expression!")
            
            time.sleep(5)
            system.show_happy("💖 I'm absolutely delighted! Watch the celebration effects! ✨")
            
            time.sleep(4)
            print("\n🎨 Demonstrating emotional sophistication...")
            
            # Sophisticated emotional demonstration
            emotions = [
                ("thinking", "💭 Contemplating with elegance..."),
                ("listening", "👂 Attentive and caring..."),
                ("speaking", "💬 Communicating with warmth!"),
                ("happy", "😊 Radiating joy and positivity!"),
                ("standby", "🌸 Gracefully ready to assist!")
            ]
            
            for emotion, message in emotions:
                time.sleep(2)
                system.set_state(emotion, message)
            
            time.sleep(3)
            system.show_standby("💝 Premium experience complete! Always here with love! 💖")
        
        # Run demo in background
        demo_thread = threading.Thread(target=premium_demo, daemon=True)
        demo_thread.start()
        
        # Start the GUI
        system.start()
        
    except Exception as e:
        print(f"Error running premium demo: {e}")
        print("Running console fallback...")
        run_console_showcase("sophia")

def run_console_showcase(user: str):
    """Run console-based showcase if GUI is not available."""
    print(f"\n📱 CONSOLE SHOWCASE FOR {user.upper()}")
    print("=" * 50)
    
    system = create_visual_feedback(use_gui=False, current_user=user)
    
    if user == "eladriel":
        sequences = [
            ("standby", "🦕 Greetings! Premium dinosaur assistant ready!"),
            ("listening", "🎧 Advanced audio sensors active..."),
            ("thinking", "🧠 Dinosaur wisdom processing..."),
            ("speaking", "🗣️ Premium vocal communication!"),
            ("happy", "🌟 ROAR! Dinosaur celebration mode!"),
            ("standby", "✨ Premium dino experience complete!")
        ]
    else:  # sophia
        sequences = [
            ("standby", "👋 Hello! Premium AI companion ready!"),
            ("listening", "💫 Listening with emotional intelligence..."),
            ("thinking", "💭 Processing with grace and wisdom..."),
            ("speaking", "💬 Communicating with warmth!"),
            ("happy", "💖 Absolutely delighted to help!"),
            ("standby", "🌸 Premium experience complete!")
        ]
    
    for state, message in sequences:
        system.set_state(state, message)
        time.sleep(3)
    
    print("=" * 50)
    print("✅ Console showcase complete!")

def main():
    """Main showcase selector."""
    print("🚀 PREMIUM VISUAL FEEDBACK SHOWCASE")
    print("=" * 60)
    print("Experience billion-dollar quality robot assistants!")
    print()
    print("1. 🦕 Premium Dinosaur (Eladriel)")
    print("   - Crystalline horns, expressive eyes")
    print("   - Advanced mouth animations")
    print("   - Emotional intelligence")
    print()
    print("2. 🤖 Premium Girl Robot (Sophia)")
    print("   - Elegant bow with sparkles")
    print("   - Beautiful eyelashes and highlights")
    print("   - Sophisticated emotional expressions")
    print()
    print("3. 🎭 Compare Both (Console Demo)")
    print("=" * 60)
    
    try:
        choice = input("Select showcase (1-3): ").strip()
        
        if choice == "1":
            showcase_premium_dinosaur()
        elif choice == "2":
            showcase_premium_girl_robot()
        elif choice == "3":
            print("\n🎭 COMPARING BOTH PREMIUM ASSISTANTS")
            print("=" * 50)
            print("Eladriel (Dinosaur):")
            run_console_showcase("eladriel")
            print("\nSophia (Girl Robot):")
            run_console_showcase("sophia")
        else:
            print("Invalid choice. Running default Sophia showcase...")
            showcase_premium_girl_robot()
            
    except KeyboardInterrupt:
        print("\n\n👋 Showcase ended. Thank you for experiencing premium quality!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Running safe console demo...")
        run_console_showcase("sophia")

if __name__ == "__main__":
    main() 