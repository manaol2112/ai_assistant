#!/usr/bin/env python3
"""
🔧 MOTOR DIRECTION FIX TOOL
Diagnose and fix motor direction and wiring issues for smooth movement

Based on user feedback:
- Forward → goes left (motor imbalance)  
- Backward → goes right + jerky
- Left → backs up instead of turning left
- Right → not smooth
"""

import time
from motor_control import MotorController

def diagnose_motor_directions():
    """Test each motor individually to identify wiring issues"""
    print("🔍 MOTOR DIRECTION DIAGNOSIS")
    print("=" * 35)
    
    motor = MotorController()
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    print("We'll test each motor individually to identify the problems...")
    print()
    
    # Test individual motors
    motor_tests = [
        ("A", "Front Left", "Should move front-left wheel forward"),
        ("B", "Front Right", "Should move front-right wheel forward"), 
        ("C", "Back Left", "Should move back-left wheel forward"),
        ("D", "Back Right", "Should move back-right wheel forward")
    ]
    
    motor_directions = {}
    
    for motor_id, position, expected in motor_tests:
        print(f"🔧 Testing Motor {motor_id} ({position})")
        print(f"Expected: {expected}")
        
        # Send individual motor command
        print("Starting motor forward...")
        motor._send_arduino_command(f"MOTOR_{motor_id}_FORWARD")
        time.sleep(2)
        motor._send_arduino_command(f"MOTOR_{motor_id}_STOP")
        
        actual = input(f"What happened? (f=forward, b=backward, n=nothing): ").lower()
        motor_directions[motor_id] = actual
        
        print()
    
    # Analyze results
    print("📊 MOTOR DIRECTION ANALYSIS:")
    print("=" * 35)
    
    issues = []
    
    for motor_id, actual in motor_directions.items():
        motor_names = {"A": "Front Left", "B": "Front Right", "C": "Back Left", "D": "Back Right"}
        if actual == 'f':
            print(f"✅ Motor {motor_id} ({motor_names[motor_id]}): CORRECT")
        elif actual == 'b':
            print(f"❌ Motor {motor_id} ({motor_names[motor_id]}): REVERSED")
            issues.append(f"Motor {motor_id} wiring reversed")
        else:
            print(f"❌ Motor {motor_id} ({motor_names[motor_id]}): NOT WORKING")
            issues.append(f"Motor {motor_id} connection problem")
    
    return motor_directions, issues

def create_motor_fix_recommendations(motor_directions):
    """Create specific fix recommendations based on test results"""
    print("\n🛠️ MOTOR FIX RECOMMENDATIONS:")
    print("=" * 35)
    
    # Check for reversed motors
    reversed_motors = [m for m, direction in motor_directions.items() if direction == 'b']
    
    if reversed_motors:
        print("🔄 WIRING FIXES NEEDED:")
        for motor_id in reversed_motors:
            motor_pins = {
                "A": "pins 2 and 4", 
                "B": "pins 6 and 7",
                "C": "pins 8 and 10", 
                "D": "pins 12 and 13"
            }
            print(f"   Motor {motor_id}: Swap {motor_pins[motor_id]} connections")
    
    # Create corrected motor mapping for Arduino
    print(f"\n📝 CORRECTED ARDUINO CODE:")
    print("Add this to your Arduino code to fix directions in software:")
    print()
    
    corrections = []
    for motor_id, direction in motor_directions.items():
        if direction == 'b':  # Reversed
            corrections.append(motor_id)
    
    if corrections:
        print("// SOFTWARE FIX - Reverse these motors in code:")
        for motor_id in corrections:
            if motor_id == 'A':
                print("// Motor A - Reverse pin1 and pin2 in software")
                print("// Change: digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW);")
                print("// To:     digitalWrite(motorA1, LOW); digitalWrite(motorA2, HIGH);")
            elif motor_id == 'B':
                print("// Motor B - Reverse pin1 and pin2 in software") 
                print("// Change: digitalWrite(motorB1, HIGH); digitalWrite(motorB2, LOW);")
                print("// To:     digitalWrite(motorB1, LOW); digitalWrite(motorB2, HIGH);")
            elif motor_id == 'C':
                print("// Motor C - Reverse pin1 and pin2 in software")
                print("// Change: digitalWrite(motorC1, HIGH); digitalWrite(motorC2, LOW);")
                print("// To:     digitalWrite(motorC1, LOW); digitalWrite(motorC2, HIGH);")
            elif motor_id == 'D':
                print("// Motor D - Reverse pin1 and pin2 in software")
                print("// Change: digitalWrite(motorD1, HIGH); digitalWrite(motorD2, LOW);")
                print("// To:     digitalWrite(motorD1, LOW); digitalWrite(motorD2, HIGH);")

def test_corrected_movements():
    """Test movements after applying fixes"""
    print("\n🎯 TESTING CORRECTED MOVEMENTS:")
    print("=" * 35)
    
    motor = MotorController()
    
    movements = [
        ("forward", "Should move straight forward"),
        ("backward", "Should move straight backward"),
        ("left", "Should turn left in place"),
        ("right", "Should turn right in place")
    ]
    
    results = {}
    
    for direction, expected in movements:
        print(f"\n🔄 Testing {direction} movement...")
        print(f"Expected: {expected}")
        
        if direction == "forward":
            motor.forward(1.5)
        elif direction == "backward":
            motor.backward(1.5)
        elif direction == "left":
            motor.left(1.0)
        elif direction == "right":
            motor.right(1.0)
        
        time.sleep(2.0)
        
        feedback = input("Result (good/bad): ").lower()
        results[direction] = feedback == 'good'
        
        if results[direction]:
            print("✅ Movement fixed!")
        else:
            print("❌ Still needs adjustment")
    
    return results

def create_speed_calibration():
    """Create speed calibration for straight movement"""
    print("\n⚙️ SPEED CALIBRATION FOR STRAIGHT MOVEMENT:")
    print("=" * 45)
    
    print("Based on your robot's behavior:")
    print("- Forward goes LEFT → Right motors (B,D) are too fast")
    print("- Backward goes RIGHT → Left motors (A,C) are too fast in reverse")
    print()
    
    # Recommended calibration
    calibration = {
        'A': 190,  # Front Left - reduced from 200
        'B': 200,  # Front Right - keep standard
        'C': 190,  # Back Left - reduced from 200  
        'D': 200   # Back Right - keep standard
    }
    
    print("🎯 RECOMMENDED SPEED CALIBRATION:")
    for motor, speed in calibration.items():
        motor_names = {'A': 'Front Left', 'B': 'Front Right', 'C': 'Back Left', 'D': 'Back Right'}
        print(f"   Motor {motor} ({motor_names[motor]}): {speed}")
    
    print(f"\n📝 Python code to apply this calibration:")
    print("motor.calibrate_motor_speeds(")
    print(f"    front_left={calibration['A']},")
    print(f"    front_right={calibration['B']},") 
    print(f"    back_left={calibration['C']},")
    print(f"    back_right={calibration['D']}")
    print(")")
    
    return calibration

def main():
    """Main motor direction fix process"""
    print("🚀 MOTOR DIRECTION & MOVEMENT FIX TOOL")
    print("=" * 45)
    print("This tool will:")
    print("1. Test each motor individually")
    print("2. Identify wiring/direction issues") 
    print("3. Provide specific fix recommendations")
    print("4. Create speed calibration for straight movement")
    print()
    
    if input("Ready to start diagnosis? (y/n): ").lower() != 'y':
        print("Diagnosis cancelled.")
        return
    
    # Step 1: Individual motor diagnosis
    motor_directions, issues = diagnose_motor_directions()
    
    # Step 2: Create fix recommendations
    create_motor_fix_recommendations(motor_directions)
    
    # Step 3: Speed calibration
    calibration = create_speed_calibration()
    
    # Step 4: Apply calibration and test
    print(f"\n🔧 APPLYING RECOMMENDED CALIBRATION...")
    motor = MotorController()
    if motor.enabled:
        motor.calibrate_motor_speeds(
            front_left=calibration['A'],
            front_right=calibration['B'],
            back_left=calibration['C'], 
            back_right=calibration['D']
        )
        
        print("Calibration applied! Test movements now:")
        test_corrected_movements()
        
        motor.cleanup()
    
    print(f"\n📋 SUMMARY:")
    print("=" * 15)
    print("1. ✅ Upload arduino_code_anti_jerk_integrated.ino")
    print("2. 🔧 Fix motor wiring issues identified above")  
    print("3. ⚙️ Apply speed calibration")
    print("4. 🧪 Test movements")
    print()
    print("This should eliminate:")
    print("• Jerky movement")
    print("• Circular movement")  
    print("• Wrong turning directions")
    print("• Movement delays")

if __name__ == "__main__":
    main() 