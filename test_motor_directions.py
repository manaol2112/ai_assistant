#!/usr/bin/env python3
"""
Motor Direction Diagnostic Script
Tests each motor individually to identify backward movement issues
"""

import sys
import time
from motor_control import MotorController

def test_individual_motor_directions():
    """Test each motor in both directions individually"""
    print("🔧 MOTOR DIRECTION DIAGNOSTIC TEST")
    print("=" * 50)
    
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    if not motor.arduino_serial:
        print("❌ Arduino not connected")
        return False
    
    print(f"✅ Connected to Arduino on {motor.arduino_port}")
    print("\n🧪 Testing each motor individually...")
    
    # Test each motor
    motors = ['A', 'B', 'C', 'D']
    
    for motor_name in motors:
        print(f"\n🔧 TESTING MOTOR {motor_name}:")
        print("-" * 30)
        
        # Forward test
        print(f"  🚀 Motor {motor_name} FORWARD (2 seconds)")
        motor._send_arduino_command(f"MOTOR_{motor_name}_FORWARD")
        time.sleep(2.0)
        
        # Stop
        print(f"  ⏸️ Motor {motor_name} STOP")
        motor._send_arduino_command(f"MOTOR_{motor_name}_STOP")
        time.sleep(1.0)
        
        # Backward test
        print(f"  ⬅️ Motor {motor_name} BACKWARD (2 seconds)")
        motor._send_arduino_command(f"MOTOR_{motor_name}_BACKWARD")
        time.sleep(2.0)
        
        # Stop
        print(f"  ⏸️ Motor {motor_name} STOP")
        motor._send_arduino_command(f"MOTOR_{motor_name}_STOP")
        time.sleep(1.0)
        
        # Ask user for feedback
        response = input(f"  ❓ Did Motor {motor_name} move BACKWARD correctly? (y/n): ").lower().strip()
        if response == 'y':
            print(f"  ✅ Motor {motor_name} backward: WORKING")
        else:
            print(f"  ❌ Motor {motor_name} backward: PROBLEM DETECTED")
            print(f"     🔍 Check wiring for Motor {motor_name}")
            print(f"     🔍 Verify Arduino code handles MOTOR_{motor_name}_BACKWARD")
    
    motor.cleanup()
    return True

def test_all_motors_backward():
    """Test all motors backward simultaneously"""
    print("\n🔧 TESTING ALL MOTORS BACKWARD TOGETHER")
    print("=" * 50)
    
    motor = MotorController()
    
    if not motor.enabled or not motor.arduino_serial:
        print("❌ Motor controller not available")
        return False
    
    print("🚀 All motors FORWARD (2 seconds)")
    motor.forward(2.0)
    time.sleep(1.0)
    
    print("⬅️ All motors BACKWARD (2 seconds)")
    motor.backward(2.0)
    time.sleep(1.0)
    
    response = input("❓ Did ALL motors move backward correctly? (y/n): ").lower().strip()
    if response == 'y':
        print("✅ All motors backward: WORKING")
    else:
        print("❌ All motors backward: PROBLEM DETECTED")
        print("🔍 Some motors may have wiring issues")
    
    motor.cleanup()
    return True

def test_arduino_commands():
    """Test raw Arduino commands"""
    print("\n🔧 TESTING RAW ARDUINO COMMANDS")
    print("=" * 50)
    
    motor = MotorController()
    
    if not motor.enabled or not motor.arduino_serial:
        print("❌ Motor controller not available")
        return False
    
    commands_to_test = [
        "MOTOR_A_FORWARD",
        "MOTOR_A_BACKWARD", 
        "MOTOR_A_STOP",
        "MOTOR_B_FORWARD",
        "MOTOR_B_BACKWARD",
        "MOTOR_B_STOP"
    ]
    
    for command in commands_to_test:
        print(f"📤 Sending: {command}")
        success = motor._send_arduino_command(command)
        if success:
            print(f"✅ Command sent successfully")
        else:
            print(f"❌ Command failed")
        time.sleep(1.0)
    
    motor.cleanup()
    return True

def diagnose_backward_issue():
    """Main diagnostic function"""
    print("🤖 MOTOR BACKWARD MOVEMENT DIAGNOSTIC")
    print("=" * 60)
    print("This script will help identify why backward movement isn't working")
    print("=" * 60)
    
    # Test 1: Individual motor directions
    print("\n📋 TEST 1: Individual Motor Direction Testing")
    test_individual_motor_directions()
    
    # Test 2: All motors backward
    print("\n📋 TEST 2: All Motors Backward Testing")
    test_all_motors_backward()
    
    # Test 3: Raw Arduino commands
    print("\n📋 TEST 3: Raw Arduino Command Testing")
    test_arduino_commands()
    
    print("\n🔍 DIAGNOSTIC COMPLETE")
    print("=" * 60)
    print("COMMON ISSUES AND SOLUTIONS:")
    print("1. ⚡ Motor wiring: Check if motor wires are connected correctly")
    print("2. 🔌 Power supply: Ensure adequate power for all motors")
    print("3. 💻 Arduino code: Verify MOTOR_X_BACKWARD commands are implemented")
    print("4. 🔄 Motor direction: Some motors may need wire polarity reversed")
    print("5. 📡 Serial communication: Check if commands are being received")
    print("=" * 60)

if __name__ == "__main__":
    try:
        diagnose_backward_issue()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}") 