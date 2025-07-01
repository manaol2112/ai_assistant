#!/usr/bin/env python3
"""
Advanced Motor Calibration Tool for AI Assistant Robot
Interactive tool to diagnose and fix circular movement issues
"""

import time
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from motor_control import MotorController

class MotorCalibrationTool:
    """Interactive tool for motor calibration and movement analysis"""
    
    def __init__(self):
        """Initialize the calibration tool"""
        print("🔧 AI ROBOT MOTOR CALIBRATION TOOL")
        print("=" * 50)
        print("This tool will help fix circular movement issues")
        print("and ensure your robot moves straight and turns properly.")
        print()
        
        # Initialize motor controller
        print("Initializing motor controller...")
        self.motor = MotorController()
        
        if not self.motor.enabled:
            print("❌ ERROR: Motor controller not available!")
            print("Please check:")
            print("  - Arduino is connected")
            print("  - USB port is correct (/dev/ttyUSB0)")
            print("  - Robot is powered on")
            sys.exit(1)
        
        print("✅ Motor controller initialized successfully!")
        print()

    def main_menu(self):
        """Display main calibration menu"""
        while True:
            print("\n🎯 MOTOR CALIBRATION MENU")
            print("=" * 30)
            print("1. Quick Movement Test")
            print("2. Individual Motor Test")
            print("3. Straight Line Calibration")
            print("4. Advanced Speed Adjustment")
            print("5. Movement Pattern Analysis")
            print("6. Save Calibration Settings")
            print("7. Reset to Default Settings")
            print("8. Exit")
            print()
            
            choice = input("Select option (1-8): ").strip()
            
            if choice == '1':
                self.quick_movement_test()
            elif choice == '2':
                self.individual_motor_test()
            elif choice == '3':
                self.straight_line_calibration()
            elif choice == '4':
                self.advanced_speed_adjustment()
            elif choice == '5':
                self.movement_pattern_analysis()
            elif choice == '6':
                self.save_calibration()
            elif choice == '7':
                self.reset_to_defaults()
            elif choice == '8':
                print("👋 Exiting calibration tool...")
                self.motor.cleanup()
                break
            else:
                print("❌ Invalid choice. Please select 1-8.")

    def quick_movement_test(self):
        """Quick test to identify movement issues"""
        print("\n🚀 QUICK MOVEMENT TEST")
        print("=" * 25)
        print("This test will show basic movement patterns.")
        print("Watch carefully and note any issues:")
        print("  - Does robot go straight forward/backward?")
        print("  - Does robot turn in place or move in arcs?")
        print()
        
        input("Press Enter to start test...")
        
        movements = [
            ("Forward", lambda: self.motor.forward(2.0)),
            ("Backward", lambda: self.motor.backward(2.0)),
            ("Left Turn", lambda: self.motor.left(1.5)),
            ("Right Turn", lambda: self.motor.right(1.5))
        ]
        
        for name, movement_func in movements:
            print(f"\n🎯 Testing: {name}")
            print("Get ready...")
            time.sleep(1)
            
            movement_func()
            time.sleep(3)  # Wait for movement to complete
            
            result = input(f"Did {name} work correctly? (y/n/s to skip): ").lower()
            if result == 'n':
                if 'forward' in name.lower() or 'backward' in name.lower():
                    print("💡 Issue detected: Robot not moving straight")
                    print("   This suggests motor speed imbalance")
                    if input("Run straight line calibration now? (y/n): ").lower() == 'y':
                        self.straight_line_calibration()
                        return
                elif 'turn' in name.lower():
                    print("💡 Issue detected: Turning problem")
                    print("   Check individual motors")
            elif result == 's':
                break
        
        print("\n✅ Quick test completed!")

    def individual_motor_test(self):
        """Test each motor individually"""
        print("\n🔧 INDIVIDUAL MOTOR TEST")
        print("=" * 25)
        print("Testing each motor separately to identify wiring issues.")
        print()
        
        if not self.motor.arduino_serial:
            print("❌ Individual motor testing requires Arduino connection")
            return
        
        motors = [
            ('A', 'Front Left'),
            ('B', 'Front Right'),
            ('C', 'Back Left'),
            ('D', 'Back Right')
        ]
        
        motor_status = {}
        
        for motor_id, position in motors:
            print(f"\n🔍 Testing Motor {motor_id} ({position})")
            print("-" * 30)
            
            # Forward test
            print("  ➡️ Forward direction (2 seconds)")
            input("    Press Enter to start...")
            self.motor._send_arduino_command(f"MOTOR_{motor_id}_FORWARD")
            time.sleep(2.0)
            self.motor._send_arduino_command(f"MOTOR_{motor_id}_STOP")
            
            forward_ok = input("    Did motor spin correctly forward? (y/n): ").lower() == 'y'
            
            # Backward test
            print("  ⬅️ Backward direction (2 seconds)")
            input("    Press Enter to start...")
            self.motor._send_arduino_command(f"MOTOR_{motor_id}_BACKWARD")
            time.sleep(2.0)
            self.motor._send_arduino_command(f"MOTOR_{motor_id}_STOP")
            
            backward_ok = input("    Did motor spin correctly backward? (y/n): ").lower() == 'y'
            
            motor_status[motor_id] = {
                'position': position,
                'forward': forward_ok,
                'backward': backward_ok
            }
        
        # Summary
        print("\n📊 MOTOR TEST SUMMARY")
        print("=" * 25)
        all_good = True
        for motor_id, status in motor_status.items():
            status_icon = "✅" if status['forward'] and status['backward'] else "❌"
            print(f"{status_icon} Motor {motor_id} ({status['position']}): "
                  f"Forward {'✅' if status['forward'] else '❌'}, "
                  f"Backward {'✅' if status['backward'] else '❌'}")
            if not (status['forward'] and status['backward']):
                all_good = False
        
        if not all_good:
            print("\n💡 TROUBLESHOOTING TIPS:")
            print("  - Check motor connections to Arduino")
            print("  - Verify power supply is adequate")
            print("  - Ensure motors are not mechanically stuck")
        else:
            print("\n🎉 All motors working correctly!")

    def straight_line_calibration(self):
        """Interactive calibration for straight line movement"""
        print("\n📐 STRAIGHT LINE CALIBRATION")
        print("=" * 30)
        print("This will help fix circular movement during forward/backward.")
        print()
        print("Current motor speeds:")
        self.display_current_speeds()
        print()
        
        # Test current settings
        print("Step 1: Testing current forward movement...")
        input("Place robot in open space and press Enter...")
        
        print("Moving forward for 3 seconds - watch direction carefully!")
        time.sleep(1)
        self.motor.forward(3.0)
        time.sleep(4)
        
        # Get user feedback
        direction = None
        while direction not in ['straight', 'left', 'right']:
            direction = input("\nDid robot go: straight/left/right? ").lower()
            if direction not in ['straight', 'left', 'right']:
                print("Please enter 'straight', 'left', or 'right'")
        
        if direction == 'straight':
            print("🎉 Robot already moving straight! Testing backward...")
            
            print("Moving backward for 3 seconds...")
            time.sleep(1)
            self.motor.backward(3.0)
            time.sleep(4)
            
            back_direction = None
            while back_direction not in ['straight', 'left', 'right']:
                back_direction = input("Backward movement: straight/left/right? ").lower()
            
            if back_direction == 'straight':
                print("✅ Perfect! Robot moves straight in both directions.")
                return
            else:
                direction = back_direction
        
        # Calculate speed adjustments
        if direction == 'right':
            print("\n🔧 Robot turns RIGHT - reducing RIGHT side motor speeds")
            adjustment = self.get_adjustment_amount()
            new_speeds = self.motor.motor_speeds.copy()
            new_speeds['B'] = max(50, new_speeds['B'] - adjustment)  # Front right
            new_speeds['D'] = max(50, new_speeds['D'] - adjustment)  # Back right
            
        elif direction == 'left':
            print("\n🔧 Robot turns LEFT - reducing LEFT side motor speeds")
            adjustment = self.get_adjustment_amount()
            new_speeds = self.motor.motor_speeds.copy()
            new_speeds['A'] = max(50, new_speeds['A'] - adjustment)  # Front left
            new_speeds['C'] = max(50, new_speeds['C'] - adjustment)  # Back left
        
        # Apply and test new speeds
        print(f"\nApplying adjustment (-{adjustment} to appropriate motors)...")
        self.motor.calibrate_motor_speeds(
            front_left=new_speeds['A'],
            front_right=new_speeds['B'],
            back_left=new_speeds['C'],
            back_right=new_speeds['D']
        )
        
        # Test adjustment
        print("\nTesting adjusted movement...")
        time.sleep(1)
        self.motor.forward(3.0)
        time.sleep(4)
        
        result = input("Better? (y/n/worse): ").lower()
        if result == 'y':
            print("✅ Improvement confirmed!")
            if input("Run another fine-tuning round? (y/n): ").lower() == 'y':
                self.straight_line_calibration()
        elif result == 'worse':
            print("⚠️ Movement got worse. Reducing adjustment...")
            # Reduce the adjustment by half
            half_adj = adjustment // 2
            if direction == 'right':
                new_speeds['B'] = min(255, self.motor.motor_speeds['B'] + half_adj)
                new_speeds['D'] = min(255, self.motor.motor_speeds['D'] + half_adj)
            else:
                new_speeds['A'] = min(255, self.motor.motor_speeds['A'] + half_adj)
                new_speeds['C'] = min(255, self.motor.motor_speeds['C'] + half_adj)
            
            self.motor.calibrate_motor_speeds(
                front_left=new_speeds['A'],
                front_right=new_speeds['B'],
                back_left=new_speeds['C'],
                back_right=new_speeds['D']
            )
        else:
            print("🔄 No change detected. Try larger adjustment or check for mechanical issues.")

    def get_adjustment_amount(self):
        """Get speed adjustment amount from user"""
        while True:
            try:
                adjustment = int(input("Enter adjustment amount (10-50, recommended 20): "))
                if 5 <= adjustment <= 100:
                    return adjustment
                else:
                    print("Please enter a value between 5 and 100")
            except ValueError:
                print("Please enter a valid number")

    def advanced_speed_adjustment(self):
        """Manual speed adjustment for each motor"""
        print("\n⚙️ ADVANCED SPEED ADJUSTMENT")
        print("=" * 30)
        print("Manually adjust individual motor speeds")
        print("Valid range: 50-255 (higher = faster)")
        print()
        
        self.display_current_speeds()
        print()
        
        motors = [
            ('A', 'Front Left'),
            ('B', 'Front Right'), 
            ('C', 'Back Left'),
            ('D', 'Back Right')
        ]
        
        new_speeds = self.motor.motor_speeds.copy()
        
        for motor_id, position in motors:
            current = new_speeds[motor_id]
            while True:
                try:
                    new_speed = input(f"{position} (Motor {motor_id}) [{current}]: ").strip()
                    if new_speed == '':
                        break  # Keep current value
                    
                    new_speed = int(new_speed)
                    if 50 <= new_speed <= 255:
                        new_speeds[motor_id] = new_speed
                        break
                    else:
                        print("Speed must be between 50 and 255")
                except ValueError:
                    print("Please enter a valid number or press Enter to keep current")
        
        # Apply new speeds
        self.motor.calibrate_motor_speeds(
            front_left=new_speeds['A'],
            front_right=new_speeds['B'],
            back_left=new_speeds['C'],
            back_right=new_speeds['D']
        )
        
        # Test new settings
        if input("\nTest new settings? (y/n): ").lower() == 'y':
            self.quick_movement_test()

    def movement_pattern_analysis(self):
        """Comprehensive movement analysis"""
        print("\n📊 MOVEMENT PATTERN ANALYSIS")
        print("=" * 35)
        print("This performs detailed movement testing with timing analysis")
        print()
        
        test_duration = 2.0
        patterns = [
            ("Forward", lambda: self.motor.forward(test_duration)),
            ("Backward", lambda: self.motor.backward(test_duration)),
            ("Left Turn", lambda: self.motor.left(test_duration)),
            ("Right Turn", lambda: self.motor.right(test_duration))
        ]
        
        results = {}
        
        for pattern_name, pattern_func in patterns:
            print(f"\n🎯 Analyzing {pattern_name}...")
            print("Place robot in center of test area")
            input("Press Enter when ready...")
            
            # Mark starting position
            print("Note starting position, then movement begins in 3...")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            
            start_time = time.time()
            pattern_func()
            time.sleep(test_duration + 0.5)  # Wait for completion
            end_time = time.time()
            
            # Get feedback
            print(f"\nMovement completed in {end_time - start_time:.1f} seconds")
            
            quality = None
            while quality not in ['excellent', 'good', 'poor']:
                quality = input("Rate movement quality (excellent/good/poor): ").lower()
            
            deviation = None
            while deviation not in ['none', 'slight', 'major']:
                deviation = input("Path deviation (none/slight/major): ").lower()
            
            results[pattern_name] = {
                'quality': quality,
                'deviation': deviation,
                'duration': end_time - start_time
            }
        
        # Analysis summary
        print("\n📈 ANALYSIS SUMMARY")
        print("=" * 20)
        
        issues_found = []
        for pattern, data in results.items():
            status = "✅" if data['quality'] == 'excellent' and data['deviation'] == 'none' else "⚠️"
            print(f"{status} {pattern}: {data['quality']} quality, {data['deviation']} deviation")
            
            if data['quality'] != 'excellent' or data['deviation'] != 'none':
                issues_found.append(pattern)
        
        if issues_found:
            print(f"\n💡 RECOMMENDATIONS:")
            if any('Forward' in issue or 'Backward' in issue for issue in issues_found):
                print("  - Run straight line calibration for forward/backward issues")
            if any('Turn' in issue for issue in issues_found):
                print("  - Check individual motors for turning issues")
            print("  - Consider mechanical inspection if multiple issues persist")
        else:
            print("\n🎉 All movement patterns working excellently!")

    def display_current_speeds(self):
        """Display current motor speed settings"""
        speeds = self.motor.motor_speeds
        print("Motor Speeds:")
        print(f"  Front Left  (A): {speeds['A']}")
        print(f"  Front Right (B): {speeds['B']}")
        print(f"  Back Left   (C): {speeds['C']}")
        print(f"  Back Right  (D): {speeds['D']}")

    def save_calibration(self):
        """Save calibration settings to file"""
        print("\n💾 SAVE CALIBRATION SETTINGS")
        print("=" * 30)
        
        filename = input("Enter filename (default: motor_calibration.txt): ").strip()
        if not filename:
            filename = "motor_calibration.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("# AI Robot Motor Calibration Settings\n")
                f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("Motor Speeds:\n")
                for motor, speed in self.motor.motor_speeds.items():
                    f.write(f"Motor_{motor} = {speed}\n")
                f.write("\n# To apply these settings:\n")
                f.write("# motor.calibrate_motor_speeds(\n")
                f.write(f"#     front_left={self.motor.motor_speeds['A']},\n")
                f.write(f"#     front_right={self.motor.motor_speeds['B']},\n")
                f.write(f"#     back_left={self.motor.motor_speeds['C']},\n")
                f.write(f"#     back_right={self.motor.motor_speeds['D']}\n")
                f.write("# )\n")
            
            print(f"✅ Calibration saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving calibration: {e}")

    def reset_to_defaults(self):
        """Reset motor speeds to default values"""
        print("\n🔄 RESET TO DEFAULT SETTINGS")
        print("=" * 30)
        
        if input("Reset all motor speeds to 200? (y/n): ").lower() == 'y':
            self.motor.calibrate_motor_speeds(
                front_left=200,
                front_right=200,
                back_left=200,
                back_right=200
            )
            print("✅ Reset to default speeds (200 for all motors)")
        else:
            print("Reset cancelled")

def main():
    """Main function"""
    try:
        calibrator = MotorCalibrationTool()
        calibrator.main_menu()
    except KeyboardInterrupt:
        print("\n\n🛑 Calibration interrupted by user")
    except Exception as e:
        print(f"\n❌ Calibration error: {e}")
        print("Please check your robot setup and try again")

if __name__ == "__main__":
    main() 