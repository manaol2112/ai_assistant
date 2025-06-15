#!/usr/bin/env python3
"""
Test Backward Command Routing
This script tests if backward commands are being sent to Arduino correctly
"""

import sys
import time
from motor_control import MotorController

def test_backward_command_routing():
    """Test if backward commands are being routed correctly"""
    print("🔍 TESTING BACKWARD COMMAND ROUTING")
    print("=" * 50)
    
    # Initialize motor controller
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    if not motor.arduino_serial:
        print("❌ Arduino not connected")
        return False
    
    print(f"✅ Connected to Arduino on {motor.arduino_port}")
    
    # Test 1: Direct Arduino command
    print("\n📋 TEST 1: Direct Arduino MOVE_BACKWARD Command")
    print("Sending MOVE_BACKWARD directly to Arduino...")
    success = motor._send_arduino_command("MOVE_BACKWARD")
    if success:
        print("✅ MOVE_BACKWARD command sent successfully")
    else:
        print("❌ MOVE_BACKWARD command failed to send")
    
    time.sleep(3)  # Let it run for 3 seconds
    
    # Stop motors
    print("Stopping motors...")
    motor._send_arduino_command("STOP_ALL")
    
    # Test 2: Python backward() method
    print("\n📋 TEST 2: Python backward() Method")
    print("Calling motor.backward(2.0)...")
    try:
        motor.backward(2.0)
        print("✅ Python backward() method executed")
    except Exception as e:
        print(f"❌ Python backward() method failed: {e}")
    
    # Test 3: Compare with forward command
    print("\n📋 TEST 3: Compare Forward vs Backward")
    
    print("Testing FORWARD command...")
    motor._send_arduino_command("MOVE_FORWARD")
    time.sleep(2)
    motor._send_arduino_command("STOP_ALL")
    time.sleep(1)
    
    print("Testing BACKWARD command...")
    motor._send_arduino_command("MOVE_BACKWARD")
    time.sleep(2)
    motor._send_arduino_command("STOP_ALL")
    
    # Ask user for feedback
    forward_works = input("❓ Did FORWARD movement work? (y/n): ").lower().strip() == 'y'
    backward_works = input("❓ Did BACKWARD movement work? (y/n): ").lower().strip() == 'y'
    
    print("\n🔍 DIAGNOSIS RESULTS:")
    print(f"Forward command: {'✅ WORKING' if forward_works else '❌ NOT WORKING'}")
    print(f"Backward command: {'✅ WORKING' if backward_works else '❌ NOT WORKING'}")
    
    if forward_works and not backward_works:
        print("\n🎯 ISSUE IDENTIFIED: Arduino MOVE_BACKWARD command not implemented!")
        print("📝 SOLUTION: Update your Arduino code with the template provided")
        print("   Make sure your Arduino has the move_backward() function")
        print("   and handles the 'MOVE_BACKWARD' command in the main loop")
    elif not forward_works and not backward_works:
        print("\n🎯 ISSUE IDENTIFIED: General motor/Arduino communication problem")
        print("📝 SOLUTION: Check Arduino connection, power supply, and wiring")
    elif forward_works and backward_works:
        print("\n✅ BOTH COMMANDS WORKING: Issue might be elsewhere")
        print("📝 Check voice command detection or timing issues")
    
    motor.cleanup()
    return True

def test_voice_command_detection():
    """Test if voice commands are being detected correctly"""
    print("\n🔍 TESTING VOICE COMMAND DETECTION")
    print("=" * 50)
    
    # Import the main AI assistant to test command detection
    try:
        from main import AIAssistant
        assistant = AIAssistant()
        
        # Test backward command detection
        test_phrases = [
            "hey robot go backward",
            "robot go backwards", 
            "go backward",
            "backward",
            "move backward"
        ]
        
        print("Testing backward command detection...")
        for phrase in test_phrases:
            result = assistant.handle_special_commands(phrase, 'parent')
            if result and 'backward' in result.lower():
                print(f"✅ '{phrase}' -> DETECTED as movement command")
            else:
                print(f"❌ '{phrase}' -> NOT detected as movement command")
                if result:
                    print(f"   Instead got: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ Voice command test failed: {e}")

if __name__ == "__main__":
    try:
        print("🤖 BACKWARD COMMAND DIAGNOSTIC TOOL")
        print("=" * 60)
        print("This will help identify why backward commands aren't working")
        print("=" * 60)
        
        # Test Arduino communication
        test_backward_command_routing()
        
        # Test voice command detection
        test_voice_command_detection()
        
        print("\n🏁 DIAGNOSTIC COMPLETE!")
        print("If backward still doesn't work, the issue is likely in your Arduino code.")
        print("Compare your Arduino code with the template provided (arduino_code_template.ino)")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 