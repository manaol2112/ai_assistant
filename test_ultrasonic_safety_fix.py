#!/usr/bin/env python3
"""
🔧 ULTRASONIC SAFETY DIAGNOSTIC & FIX TOOL
Diagnose why forward movement is blocked and provide solutions

The issue: Forward movement is blocked by ultrasonic sensor safety system
"""

import time
from motor_control import MotorController

def test_ultrasonic_sensor_readings():
    """Test the ultrasonic sensor to see what it's detecting"""
    print("🔍 ULTRASONIC SENSOR DIAGNOSTIC")
    print("=" * 35)
    
    motor = MotorController()
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    print("Testing ultrasonic sensor readings...")
    print("(Looking for false obstacle detections)")
    print()
    
    # Take 10 readings
    for i in range(10):
        motor._send_arduino_command("READ_ULTRASONIC")
        time.sleep(0.2)
        
        # Try to read the response
        if motor.arduino_serial and motor.arduino_serial.in_waiting > 0:
            response = motor.arduino_serial.readline().decode().strip()
            if "ULTRASONIC_DISTANCE:" in response:
                distance = response.split(":")[1]
                print(f"Reading {i+1}: {distance} cm")
                
                try:
                    dist_val = int(distance)
                    if dist_val < 15 and dist_val > 0:
                        print(f"  ⚠️ OBSTACLE DETECTED: {dist_val}cm (blocking forward movement)")
                    elif dist_val < 0:
                        print(f"  ❌ SENSOR ERROR: {dist_val} (invalid reading)")
                    else:
                        print(f"  ✅ CLEAR: {dist_val}cm (safe to move)")
                except:
                    print(f"  ❓ UNKNOWN READING: {distance}")
            else:
                print(f"Reading {i+1}: No response or {response}")
        else:
            print(f"Reading {i+1}: No response from Arduino")
        
        time.sleep(0.5)
    
    motor.cleanup()
    return True

def disable_safety_and_test_forward():
    """Temporarily disable safety to test forward movement"""
    print("\n🛡️ DISABLING SAFETY TEMPORARILY")
    print("=" * 35)
    print("This will turn OFF collision avoidance to test forward movement")
    print("⚠️ WARNING: Make sure there are no obstacles in front!")
    print()
    
    proceed = input("Continue? Clear the path and type 'yes': ").lower()
    if proceed != 'yes':
        print("Safety test cancelled.")
        return False
    
    motor = MotorController()
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    print("🔧 Sending SAFETY_OFF command...")
    motor._send_arduino_command("SAFETY_OFF")
    time.sleep(0.5)
    
    print("🚀 Testing forward movement with safety disabled...")
    motor.forward(2.0)
    time.sleep(3.0)
    
    # Check if it worked
    result = input("Did the robot move forward? (y/n): ").lower()
    
    print("🔧 Re-enabling safety...")
    motor._send_arduino_command("SAFETY_ON")
    
    motor.cleanup()
    
    if result == 'y':
        print("✅ DIAGNOSIS CONFIRMED: Ultrasonic sensor was blocking movement")
        return True
    else:
        print("❌ Issue is NOT the ultrasonic sensor - deeper problem exists")
        return False

def apply_permanent_fix():
    """Apply permanent fix by adjusting the safety distance"""
    print("\n🔧 APPLYING PERMANENT FIX")
    print("=" * 25)
    print("Recommendations:")
    print("1. 🎯 PREFERRED: Adjust SAFE_DISTANCE in Arduino code")
    print("2. 🔧 ALTERNATIVE: Disable safety permanently")
    print("3. 🔍 HARDWARE: Check ultrasonic sensor wiring")
    print()
    
    print("📝 ARDUINO CODE FIXES:")
    print("=" * 20)
    print("Open your arduino_code_anti_jerk_integrated.ino file and:")
    print()
    print("OPTION 1 - Reduce safe distance:")
    print("   Change: const int SAFE_DISTANCE = 15;")
    print("   To:     const int SAFE_DISTANCE = 5;   // 5cm instead of 15cm")
    print()
    print("OPTION 2 - Disable safety by default:")
    print("   Change: bool safety_enabled = true;")
    print("   To:     bool safety_enabled = false;  // Disable collision avoidance")
    print()
    print("OPTION 3 - Add distance check:")
    print("   In is_safe_to_move_forward() function, change:")
    print("   if (distance > 0 && distance < SAFE_DISTANCE) {")
    print("   To:")
    print("   if (distance > 2 && distance < SAFE_DISTANCE) {  // Ignore readings below 2cm")
    print()
    
    choice = input("Which fix do you want to apply? (1/2/3): ")
    
    if choice == "1":
        print("✅ Recommended: Change SAFE_DISTANCE = 15 to SAFE_DISTANCE = 5")
    elif choice == "2":
        print("✅ Alternative: Change safety_enabled = true to safety_enabled = false")
    elif choice == "3":
        print("✅ Hardware fix: Add minimum distance check to ignore false readings")
    else:
        print("ℹ️ Manual fix required - edit the Arduino code as shown above")

def test_ir_sensors():
    """Test IR sensors for false detections"""
    print("\n👁️ TESTING IR SENSORS")
    print("=" * 20)
    
    motor = MotorController()
    if not motor.enabled:
        print("❌ Motor controller not available")
        return False
    
    print("Checking IR sensor readings...")
    
    # Test left IR
    motor._send_arduino_command("READ_IR_LEFT")
    time.sleep(0.2)
    
    # Test right IR  
    motor._send_arduino_command("READ_IR_RIGHT")
    time.sleep(0.2)
    
    # Test both IR
    motor._send_arduino_command("READ_IR_BOTH")
    time.sleep(0.2)
    
    print("IR sensor values shown above")
    print("Note: 0 = obstacle detected, 1 = clear path")
    
    motor.cleanup()
    return True

def main():
    """Main diagnostic process"""
    print("🚨 FORWARD MOVEMENT BLOCKED - DIAGNOSTIC TOOL")
    print("=" * 50)
    print("Issue: Forward movement not working after uploading anti-jerk code")
    print("Cause: Ultrasonic sensor safety system blocking movement")
    print()
    print("This tool will:")
    print("1. Test ultrasonic sensor readings")
    print("2. Test IR sensor readings") 
    print("3. Temporarily disable safety to confirm diagnosis")
    print("4. Provide permanent fix options")
    print()
    
    if input("Start diagnosis? (y/n): ").lower() != 'y':
        print("Diagnosis cancelled.")
        return
    
    # Step 1: Test ultrasonic sensor
    print("\n" + "="*50)
    print("STEP 1: ULTRASONIC SENSOR TEST")
    print("="*50)
    test_ultrasonic_sensor_readings()
    
    # Step 2: Test IR sensors
    print("\n" + "="*50)
    print("STEP 2: IR SENSOR TEST")
    print("="*50)
    test_ir_sensors()
    
    # Step 3: Safety disable test
    print("\n" + "="*50)
    print("STEP 3: SAFETY DISABLE TEST")
    print("="*50)
    if disable_safety_and_test_forward():
        # Step 4: Apply fix
        print("\n" + "="*50)
        print("STEP 4: PERMANENT FIX")
        print("="*50)
        apply_permanent_fix()
    
    print("\n🎯 QUICK TEMPORARY FIX:")
    print("Run this command to disable safety right now:")
    print("python3 -c \"from motor_control import MotorController; m=MotorController(); m._send_arduino_command('SAFETY_OFF'); m.cleanup()\"")
    print()
    print("Then test: python3 fix_motor_directions.py")

if __name__ == "__main__":
    main() 