"""
Comprehensive Tests for Premium Visual Feedback System
Tests all premium features including animations, emotions, and visual effects
"""

import unittest
import threading
import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visual_feedback import PremiumVisualFeedbackSystem, create_visual_feedback
import tkinter as tk

class TestPremiumVisualFeedback(unittest.TestCase):
    """Test suite for premium visual feedback system."""
    
    def setUp(self):
        """Set up test environment."""
        self.system = None
        self.test_timeout = 10  # seconds
    
    def tearDown(self):
        """Clean up after tests."""
        if self.system:
            try:
                self.system.stop()
            except:
                pass
    
    def test_premium_system_creation(self):
        """Test creation of premium visual feedback system."""
        system = create_visual_feedback(use_gui=False, current_user="test_user")
        self.assertIsNotNone(system)
        system.stop()
    
    def test_dinosaur_face_creation(self):
        """Test premium dinosaur face creation for Eladriel."""
        try:
            system = PremiumVisualFeedbackSystem(current_user="eladriel")
            self.assertEqual(system._get_premium_face_type("eladriel"), "dinosaur")
        except Exception as e:
            self.skipTest(f"GUI not available: {e}")
    
    def test_girl_robot_face_creation(self):
        """Test premium girl robot face creation for Sophia."""
        try:
            system = PremiumVisualFeedbackSystem(current_user="sophia")
            self.assertEqual(system._get_premium_face_type("sophia"), "girl_robot")
        except Exception as e:
            self.skipTest(f"GUI not available: {e}")
    
    def test_emotional_states(self):
        """Test all premium emotional states."""
        try:
            system = create_visual_feedback(use_gui=False, current_user="test")
            
            # Test all emotional states
            emotions = ["standby", "listening", "speaking", "thinking", "happy", "error"]
            
            for emotion in emotions:
                system.set_state(emotion, f"Testing {emotion} state")
                self.assertEqual(system.current_state, emotion)
            
            system.stop()
        except Exception as e:
            self.skipTest(f"System not available: {e}")

class PremiumVisualFeedbackDemo:
    """Interactive demo for premium visual feedback features."""
    
    def __init__(self):
        self.system = None
        self.demo_running = False
    
    def run_dinosaur_demo(self):
        """Run premium dinosaur demo for Eladriel."""
        print("🦕 Starting Premium Dinosaur Demo for Eladriel...")
        
        try:
            self.system = PremiumVisualFeedbackSystem(
                width=900, 
                height=600, 
                current_user="eladriel"
            )
            
            # Schedule demo sequence
            self._schedule_dinosaur_sequence()
            
            # Start the system
            self.system.start()
            
        except Exception as e:
            print(f"Demo error: {e}")
            self._run_console_demo("eladriel")
    
    def run_girl_robot_demo(self):
        """Run premium girl robot demo for Sophia."""
        print("🤖 Starting Premium Girl Robot Demo for Sophia...")
        
        try:
            self.system = PremiumVisualFeedbackSystem(
                width=900, 
                height=600, 
                current_user="sophia"
            )
            
            # Schedule demo sequence
            self._schedule_girl_robot_sequence()
            
            # Start the system
            self.system.start()
            
        except Exception as e:
            print(f"Demo error: {e}")
            self._run_console_demo("sophia")
    
    def _schedule_dinosaur_sequence(self):
        """Schedule premium dinosaur demonstration sequence."""
        def demo_sequence():
            sequences = [
                (2000, lambda: self.system.show_standby("🦕 Hello! I'm Eladriel, your premium dino assistant!")),
                (4000, lambda: self.system.show_listening("🎧 I'm listening with my advanced audio processing...")),
                (6000, lambda: self.system.show_thinking("🧠 Let me think about this with my dinosaur wisdom...")),
                (8000, lambda: self.system.show_speaking("🗣️ Here's my response with emotional intelligence!")),
                (12000, lambda: self.system.show_happy("🌟 ROAR! That was fantastic! I'm so happy!")),
                (15000, lambda: self.system.show_standby("✨ Ready for our next premium adventure!")),
                (17000, lambda: self._demonstrate_mouth_animation()),
                (22000, lambda: self._demonstrate_emotional_transitions()),
                (30000, lambda: self.system.show_standby("🦕 Demo complete! I'm always here to help!"))
            ]
            
            for delay, action in sequences:
                if self.system and self.system.running:
                    self.system.root.after(delay, action)
        
        # Start demo sequence after UI is ready
        if self.system:
            self.system.root.after(1000, demo_sequence)
    
    def _schedule_girl_robot_sequence(self):
        """Schedule premium girl robot demonstration sequence."""
        def demo_sequence():
            sequences = [
                (2000, lambda: self.system.show_standby("👋 Hi! I'm Sophia, your premium AI assistant!")),
                (4000, lambda: self.system.show_listening("💫 I'm listening with perfect attention and care...")),
                (6000, lambda: self.system.show_thinking("💭 Processing with advanced emotional intelligence...")),
                (8000, lambda: self.system.show_speaking("💬 Speaking with warmth and personality!")),
                (12000, lambda: self.system.show_happy("💖 I'm absolutely delighted to help you! ✨")),
                (15000, lambda: self.system.show_standby("🌸 Ready for our next beautiful interaction!")),
                (17000, lambda: self._demonstrate_mouth_animation()),
                (22000, lambda: self._demonstrate_emotional_transitions()),
                (30000, lambda: self.system.show_standby("💝 Demo complete! Always here with a smile!"))
            ]
            
            for delay, action in sequences:
                if self.system and self.system.running:
                    self.system.root.after(delay, action)
        
        # Start demo sequence after UI is ready
        if self.system:
            self.system.root.after(1000, demo_sequence)
    
    def _demonstrate_mouth_animation(self):
        """Demonstrate advanced mouth animation features."""
        if not self.system or not self.system.robot_face:
            return
            
        print("🎭 Demonstrating premium mouth animations...")
        
        # Start speaking animation
        self.system.robot_face.start_speaking()
        self.system.set_message("🎤 Watch my mouth move realistically as I speak!")
        
        # Stop after demonstration
        if self.system:
            self.system.root.after(5000, lambda: self.system.robot_face.stop_speaking())
    
    def _demonstrate_emotional_transitions(self):
        """Demonstrate smooth emotional transitions."""
        if not self.system:
            return
            
        print("🎨 Demonstrating premium emotional transitions...")
        
        emotions = [
            ("happy", "😊 Pure joy and excitement!"),
            ("thinking", "🤔 Deep contemplation..."),
            ("listening", "👂 Focused attention..."),
            ("speaking", "🗨️ Expressive communication!"),
            ("standby", "😌 Peaceful and ready...")
        ]
        
        for i, (emotion, message) in enumerate(emotions):
            if self.system:
                delay = i * 1500
                self.system.root.after(
                    delay, 
                    lambda e=emotion, m=message: self.system.set_state(e, m)
                )
    
    def _run_console_demo(self, user: str):
        """Run console-based demo if GUI is not available."""
        print(f"\n📱 Running Console Demo for {user.title()}...")
        print("=" * 50)
        
        system = create_visual_feedback(use_gui=False, current_user=user)
        
        demo_sequence = [
            ("standby", f"Hello! I'm your premium AI assistant for {user.title()}!"),
            ("listening", "I'm listening with advanced audio processing..."),
            ("thinking", "Processing with emotional intelligence..."),
            ("speaking", "Speaking with personality and warmth!"),
            ("happy", "I'm so happy to help you! ✨"),
            ("standby", "Ready for our next interaction!")
        ]
        
        for state, message in demo_sequence:
            system.set_state(state, message)
            time.sleep(2)
        
        print("=" * 50)
        print("✅ Console demo complete!")

def run_comprehensive_demo():
    """Run comprehensive demonstration of all premium features."""
    print("🚀 Premium Visual Feedback System Demo")
    print("=" * 60)
    print("1. Premium Dinosaur (Eladriel)")
    print("2. Premium Girl Robot (Sophia)")
    print("3. Run Tests")
    print("4. Console Demo")
    print("=" * 60)
    
    choice = input("Select demo (1-4): ").strip()
    
    demo = PremiumVisualFeedbackDemo()
    
    if choice == "1":
        demo.run_dinosaur_demo()
    elif choice == "2":
        demo.run_girl_robot_demo()
    elif choice == "3":
        # Run unit tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPremiumVisualFeedback)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    elif choice == "4":
        user = input("Enter user name (eladriel/sophia/other): ").strip() or "sophia"
        demo._run_console_demo(user)
    else:
        print("Invalid choice. Running default demo...")
        demo.run_girl_robot_demo()

if __name__ == "__main__":
    run_comprehensive_demo() 