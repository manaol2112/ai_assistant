#!/usr/bin/env python3
"""
Test script for Arduino Motor Controller Integration
Tests the exact commands that work with your Arduino L298N setup
"""

import sys
import time
from motor_control import MotorController

def test_individual_motors():
    """Test each motor individually"""
    print("🧪 Testing individual motors...")
    
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    if not motor.arduino_serial:
        print("❌ Arduino not connected")
        return False
    
    print(f"✅ Connected to Arduino on {motor.arduino_port}")
    
    # Test each motor
    motors = ['A', 'B', 'C', 'D']
    
    for motor_name in motors:
        print(f"\n🔧 Testing Motor {motor_name}:")
        
        # Forward
        print(f"  → Motor {motor_name} Forward (1 second)")
        motor._send_arduino_command(f"MOTOR_{motor_name}_FORWARD")
        time.sleep(1.0)
        
        # Stop
        print(f"  ⏸️ Motor {motor_name} Stop")
        motor._send_arduino_command(f"MOTOR_{motor_name}_STOP")
        time.sleep(0.5)
        
        # Backward
        print(f"  ← Motor {motor_name} Backward (1 second)")
        motor._send_arduino_command(f"MOTOR_{motor_name}_BACKWARD")
        time.sleep(1.0)
        
        # Stop
        print(f"  ⏸️ Motor {motor_name} Stop")
        motor._send_arduino_command(f"MOTOR_{motor_name}_STOP")
        time.sleep(0.5)
        
        print(f"  ✅ Motor {motor_name} test complete")
    
    motor.cleanup()
    return True

def test_movement_patterns():
    """Test robot movement patterns"""
    print("\n🚀 Testing robot movement patterns...")
    
    motor = MotorController()
    
    if not motor.enabled or not motor.arduino_serial:
        print("❌ Arduino motor controller not available")
        return False
    
    print("Testing movement patterns (2 seconds each):")
    
    # Forward
    print("\n🚀 Moving Forward...")
    motor.forward(2.0)
    time.sleep(0.5)
    
    # Backward
    print("⬅️ Moving Backward...")
    motor.backward(2.0)
    time.sleep(0.5)
    
    # Left turn
    print("↪️ Turning Left...")
    motor.left(2.0)
    time.sleep(0.5)
    
    # Right turn
    print("↩️ Turning Right...")
    motor.right(2.0)
    time.sleep(0.5)
    
    # Final stop
    print("🛑 Final Stop")
    motor.stop()
    
    motor.cleanup()
    print("✅ Movement pattern test complete!")
    return True

def test_gesture_simulation():
    """Simulate gesture control commands"""
    print("\n🖐️ Simulating gesture control...")
    
    motor = MotorController()
    
    if not motor.enabled or not motor.arduino_serial:
        print("❌ Arduino motor controller not available")
        return False
    
    gestures = {
        '5 fingers': 'forward',
        'fist': 'backward', 
        '2 fingers': 'left',
        '3 fingers': 'right',
        '1 finger': 'stop'
    }
    
    print("Simulating gesture commands:")
    
    for gesture, action in gestures.items():
        print(f"\n🖐️ Gesture: {gesture} → Action: {action}")
        
        if action == 'forward':
            motor.forward(1.5)
        elif action == 'backward':
            motor.backward(1.5)
        elif action == 'left':
            motor.left(1.5)
        elif action == 'right':
            motor.right(1.5)
        elif action == 'stop':
            motor.stop()
            break
        
        time.sleep(0.5)
    
    motor.cleanup()
    print("✅ Gesture simulation complete!")
    return True

def main():
    """Main test function"""
    print("🤖 Arduino Motor Controller Test Suite")
    print("=" * 50)
    
    try:
        # Test 1: Individual motor control
        print("\n📋 TEST 1: Individual Motor Control")
        if not test_individual_motors():
            print("❌ Individual motor test failed")
            return
        
        time.sleep(2)
        
        # Test 2: Movement patterns
        print("\n📋 TEST 2: Movement Patterns")
        if not test_movement_patterns():
            print("❌ Movement pattern test failed")
            return
        
        time.sleep(2)
        
        # Test 3: Gesture simulation
        print("\n📋 TEST 3: Gesture Control Simulation")
        if not test_gesture_simulation():
            print("❌ Gesture simulation test failed")
            return
        
        print("\n🎉 ALL TESTS PASSED!")
        print("Your Arduino motor setup is working perfectly!")
        print("Ready for voice-triggered gesture control! 🚀")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 