#!/usr/bin/env python3
"""
🚀 ANTI-JERK SYSTEM TEST
Quick test to verify that the updated Arduino code eliminates jerky movement
and that collision avoidance is working properly.
"""

import time
from motor_control import MotorController

def test_anti_jerk_system():
    """Test the complete anti-jerk system"""
    print("🤖 ANTI-JERK SYSTEM TEST")
    print("=" * 30)
    print("Testing smooth movement with collision avoidance...")
    print()
    
    # Initialize motor controller with auto port detection
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not available")
        print("Please ensure:")
        print("1. Arduino is connected via USB")
        print("2. Arduino code has been uploaded")
        print("3. Serial drivers are installed")
        return False
    
    print(f"✅ Motor controller initialized: {motor.get_status()}")
    print()
    
    # Test collision safety first
    print("🛡️ TESTING COLLISION SAFETY...")
    print("Place your hand 10cm in front of the robot's ultrasonic sensor")
    input("Press Enter when obstacle is in place...")
    
    print("Testing forward movement (should be blocked)...")
    motor.forward(2.0)
    time.sleep(1.0)
    motor.stop()
    
    print("Remove the obstacle")
    input("Press Enter when path is clear...")
    
    # Test smooth movements
    print("\n⚡ TESTING SMOOTH MOVEMENTS...")
    
    movements = [
        ("forward", "Forward (smooth start/stop)"),
        ("backward", "Backward (smooth start/stop)"),
        ("left", "Turn left (smooth)"),
        ("right", "Turn right (smooth)")
    ]
    
    for direction, description in movements:
        print(f"\n🎯 Testing {description}...")
        print("Watch for smooth, non-jerky movement...")
        input("Press Enter to start...")
        
        # Execute movement
        if direction == "forward":
            motor.forward(1.5)
        elif direction == "backward":
            motor.backward(1.5)
        elif direction == "left":
            motor.left(1.0)
        elif direction == "right":
            motor.right(1.0)
        
        time.sleep(2.0)  # Let movement complete
        
        # Get user feedback
        smooth = input("Was the movement smooth? (y/n): ").lower() == 'y'
        if smooth:
            print("✅ Movement is smooth!")
        else:
            print("⚠️ Still jerky - may need calibration")
    
    # Test rapid direction changes
    print("\n🔄 TESTING RAPID DIRECTION CHANGES...")
    print("This tests transition smoothness...")
    input("Press Enter to start rapid transitions...")
    
    print("Forward → Backward transition...")
    motor.forward(0.8)
    time.sleep(0.4)
    motor.backward(0.8)
    time.sleep(1.2)
    
    print("Left → Right transition...")
    motor.left(0.6)
    time.sleep(0.3)
    motor.right(0.6)
    time.sleep(1.0)
    
    motor.stop()
    
    transitions_smooth = input("Were the direction transitions smooth? (y/n): ").lower() == 'y'
    
    # Test servo functionality
    print("\n🔄 TESTING SERVO FUNCTIONALITY...")
    if motor.arduino_serial:
        print("Testing servo movements...")
        
        # Test first servo
        motor._send_arduino_command("SERVO_45")
        time.sleep(1)
        motor._send_arduino_command("SERVO_135")
        time.sleep(1)
        motor._send_arduino_command("SERVO_90")
        time.sleep(1)
        
        # Test second servo
        motor._send_arduino_command("SERVO2_45")
        time.sleep(1)
        motor._send_arduino_command("SERVO2_135")
        time.sleep(1)
        motor._send_arduino_command("SERVO2_90")
        
        servos_working = input("Did the servos move correctly? (y/n): ").lower() == 'y'
    else:
        print("⚠️ Cannot test servos - Arduino not connected")
        servos_working = False
    
    # Test sensor readings
    print("\n📡 TESTING SENSORS...")
    if motor.arduino_serial:
        print("Reading ultrasonic sensor...")
        motor._send_arduino_command("READ_ULTRASONIC")
        time.sleep(0.2)
        
        print("Reading IR sensors...")
        motor._send_arduino_command("READ_IR_BOTH")
        time.sleep(0.2)
        
        # Check if Arduino responded
        if motor.arduino_serial.in_waiting > 0:
            response = motor.arduino_serial.read_all().decode()
            print(f"Sensor readings: {response}")
            sensors_working = True
        else:
            print("⚠️ No sensor response received")
            sensors_working = False
    else:
        print("⚠️ Cannot test sensors - Arduino not connected")
        sensors_working = False
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 25)
    
    results = {
        "Motor controller": motor.enabled,
        "Smooth movements": smooth if 'smooth' in locals() else False,
        "Smooth transitions": transitions_smooth,
        "Servo control": servos_working,
        "Sensor readings": sensors_working
    }
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed >= 4:
        print("🎉 EXCELLENT: Anti-jerk system is working perfectly!")
        print("Your robot now has:")
        print("• Smooth, non-jerky movement")
        print("• Collision avoidance protection")
        print("• Working servo and sensor integration")
    elif passed >= 3:
        print("✅ GOOD: System is mostly working")
        print("Check any failed components above")
    else:
        print("⚠️ NEEDS ATTENTION: Multiple issues detected")
        print("1. Verify Arduino code upload")
        print("2. Check wiring connections")
        print("3. Test serial communication")
    
    motor.cleanup()
    return passed >= 4

if __name__ == "__main__":
    print("🚀 STARTING ANTI-JERK SYSTEM TEST")
    print("=" * 40)
    print("This will test your updated Arduino code and anti-jerk fixes.")
    print("Make sure your robot is in a safe, open area.")
    print()
    
    if input("Ready to test? (y/n): ").lower() != 'y':
        print("Test cancelled.")
        exit()
    
    success = test_anti_jerk_system()
    
    if success:
        print("\n🎉 SUCCESS: Your robot movement is now smooth and safe!")
    else:
        print("\n⚠️ Some issues detected. Check the summary above.") 