#!/usr/bin/env python3
"""
🚀 SMOOTH MOVEMENT TEST SCRIPT
Test the anti-jerk motor control fixes to ensure smooth robot movement

This script tests:
1. Movement timing analysis
2. Simultaneous motor command functionality
3. Transition smoothness between directions
4. Speed calibration effectiveness
"""

import time
import threading
from motor_control import MotorController

def test_movement_timing():
    """Test movement timing to identify jerk causes"""
    print("🔍 MOVEMENT TIMING ANALYSIS")
    print("=" * 35)
    
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not enabled - cannot test")
        return False
    
    print(f"Motor Controller Status: {motor.get_status()}")
    print()
    
    # Test timing for different movements
    movements = [
        ("forward", 1.0),
        ("backward", 1.0), 
        ("left", 0.8),
        ("right", 0.8)
    ]
    
    timing_results = {}
    
    for direction, duration in movements:
        print(f"🎯 Testing {direction} movement timing...")
        
        # Measure start time
        start_time = time.time()
        
        if direction == "forward":
            motor.forward(duration)
        elif direction == "backward":
            motor.backward(duration)
        elif direction == "left":
            motor.left(duration)
        elif direction == "right":
            motor.right(duration)
        
        # Measure command execution time
        command_time = time.time() - start_time
        
        # Wait for movement to complete
        time.sleep(duration + 0.5)
        
        # Measure stop time
        stop_start = time.time()
        motor.stop()
        stop_time = time.time() - stop_start
        
        timing_results[direction] = {
            'command_time': command_time,
            'stop_time': stop_time
        }
        
        print(f"   Command execution: {command_time:.3f}s")
        print(f"   Stop time: {stop_time:.3f}s")
        
        # Small delay between tests
        time.sleep(0.5)
    
    print("\n📊 TIMING ANALYSIS SUMMARY:")
    print("=" * 35)
    
    total_jerky_issues = 0
    
    for direction, times in timing_results.items():
        cmd_time = times['command_time']
        stop_time = times['stop_time']
        
        status = "✅ SMOOTH"
        issues = []
        
        if cmd_time > 0.05:
            issues.append(f"Slow start ({cmd_time:.3f}s)")
            total_jerky_issues += 1
            
        if stop_time > 0.05:
            issues.append(f"Slow stop ({stop_time:.3f}s)")
            total_jerky_issues += 1
        
        if issues:
            status = f"⚠️ JERKY: {', '.join(issues)}"
        
        print(f"{direction.ljust(8)}: {status}")
    
    print(f"\nTotal jerky issues detected: {total_jerky_issues}")
    
    motor.cleanup()
    return total_jerky_issues == 0

def test_direction_transitions():
    """Test smoothness of direction transitions"""
    print("\n🔄 DIRECTION TRANSITION TEST")
    print("=" * 35)
    
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not enabled - cannot test")
        return False
    
    # Test rapid direction changes
    transitions = [
        ("forward", "backward"),
        ("left", "right"),
        ("forward", "left"),
        ("backward", "right")
    ]
    
    transition_times = []
    
    for from_dir, to_dir in transitions:
        print(f"🔄 Testing {from_dir} → {to_dir} transition...")
        
        # Start first movement
        if from_dir == "forward":
            motor.forward(0.5)
        elif from_dir == "backward":
            motor.backward(0.5)
        elif from_dir == "left":
            motor.left(0.5)
        elif from_dir == "right":
            motor.right(0.5)
        
        time.sleep(0.3)  # Let first movement start
        
        # Measure transition time
        transition_start = time.time()
        
        # Start second movement (should trigger transition)
        if to_dir == "forward":
            motor.forward(0.5)
        elif to_dir == "backward":
            motor.backward(0.5)
        elif to_dir == "left":
            motor.left(0.5)
        elif to_dir == "right":
            motor.right(0.5)
        
        transition_time = time.time() - transition_start
        transition_times.append(transition_time)
        
        print(f"   Transition time: {transition_time:.3f}s")
        
        time.sleep(0.8)  # Let second movement complete
        motor.stop()
        time.sleep(0.3)  # Rest between tests
    
    # Analyze transition smoothness
    avg_transition = sum(transition_times) / len(transition_times)
    max_transition = max(transition_times)
    
    print(f"\n📈 TRANSITION ANALYSIS:")
    print(f"Average transition time: {avg_transition:.3f}s")
    print(f"Maximum transition time: {max_transition:.3f}s")
    
    if avg_transition < 0.1:
        print("✅ EXCELLENT: Transitions are very smooth")
        smooth_rating = "excellent"
    elif avg_transition < 0.2:
        print("✅ GOOD: Transitions are acceptable")
        smooth_rating = "good"
    else:
        print("⚠️ POOR: Transitions are too slow/jerky")
        smooth_rating = "poor"
    
    motor.cleanup()
    return smooth_rating in ["excellent", "good"]

def test_speed_calibration_effectiveness():
    """Test if speed calibration reduces circular movement"""
    print("\n⚙️ SPEED CALIBRATION TEST")
    print("=" * 35)
    
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not enabled - cannot test")
        return False
    
    print("Current motor speeds:")
    for motor_id, speed in motor.motor_speeds.items():
        motor_names = {'A': 'Front Left', 'B': 'Front Right', 'C': 'Back Left', 'D': 'Back Right'}
        print(f"  Motor {motor_id} ({motor_names[motor_id]}): {speed}")
    
    print("\n🎯 Testing speed calibration impact...")
    
    # Test default speeds
    print("1️⃣ Testing with current calibrated speeds...")
    print("   (Watch for straight movement)")
    
    motor.forward(2.0)
    time.sleep(3.0)
    
    user_feedback = input("Did robot move in a straight line? (y/n): ").lower()
    current_straight = user_feedback == 'y'
    
    # Test equal speeds (should show the original problem)
    print("\n2️⃣ Testing with equal speeds (200 for all motors)...")
    print("   (This should demonstrate the original circular movement)")
    
    motor.calibrate_motor_speeds(200, 200, 200, 200)
    
    motor.forward(2.0)
    time.sleep(3.0)
    
    user_feedback = input("Did robot move in a straight line with equal speeds? (y/n): ").lower()
    equal_straight = user_feedback == 'y'
    
    # Restore original calibration
    motor.calibrate_motor_speeds(
        front_left=motor.motor_speeds['A'],
        front_right=motor.motor_speeds['B'],
        back_left=motor.motor_speeds['C'],
        back_right=motor.motor_speeds['D']
    )
    
    print("\n📊 CALIBRATION EFFECTIVENESS:")
    
    if current_straight and not equal_straight:
        print("✅ EXCELLENT: Calibration is working - fixes circular movement")
        effectiveness = "excellent"
    elif current_straight and equal_straight:
        print("✅ GOOD: Both work well - no calibration needed")
        effectiveness = "good"
    elif not current_straight and not equal_straight:
        print("⚠️ POOR: Neither works - needs manual calibration")
        effectiveness = "poor"
    else:
        print("🤔 UNEXPECTED: Equal speeds work better than calibrated")
        effectiveness = "unexpected"
    
    motor.cleanup()
    return effectiveness in ["excellent", "good"]

def comprehensive_smooth_movement_test():
    """Run all movement smoothness tests"""
    print("🚀 COMPREHENSIVE SMOOTH MOVEMENT TEST")
    print("=" * 45)
    print("Testing all aspects of robot movement smoothness...")
    print()
    
    # Run all tests
    results = {}
    
    try:
        print("Phase 1: Movement Timing Analysis")
        results['timing'] = test_movement_timing()
        
        print("\nPhase 2: Direction Transition Smoothness")
        results['transitions'] = test_direction_transitions()
        
        print("\nPhase 3: Speed Calibration Effectiveness")
        results['calibration'] = test_speed_calibration_effectiveness()
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        return False
    
    # Overall assessment
    print("\n🎯 OVERALL SMOOTHNESS ASSESSMENT")
    print("=" * 40)
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.capitalize()}: {status}")
    
    print(f"\nTests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 EXCELLENT: Robot movement is smooth and optimized!")
        return True
    elif passed_tests >= total_tests * 0.7:
        print("✅ GOOD: Robot movement is acceptable with minor issues")
        return True
    else:
        print("⚠️ POOR: Robot movement needs further optimization")
        
        print("\n💡 RECOMMENDATIONS:")
        if not results.get('timing', True):
            print("- Update Arduino code to use simultaneous motor commands")
            print("- Check serial communication speed (baud rate)")
        if not results.get('transitions', True):
            print("- Reduce movement durations for testing")
            print("- Add small delays between direction changes")
        if not results.get('calibration', True):
            print("- Run motor calibration tool: python3 motor_calibration_tool.py")
            print("- Check individual motor functionality")
        
        return False

if __name__ == "__main__":
    print("🤖 SMOOTH MOVEMENT VERIFICATION")
    print("=" * 35)
    print("This script will test if the jerky movement fixes are working.")
    print("Make sure your robot is in a safe, open area before testing.")
    print()
    
    if input("Ready to start testing? (y/n): ").lower() != 'y':
        print("Test cancelled.")
        exit()
    
    # Run comprehensive test
    success = comprehensive_smooth_movement_test()
    
    if success:
        print("\n🎉 SUCCESS: Jerky movement fixes are working!")
        print("Your robot should now move smoothly in all directions.")
    else:
        print("\n⚠️ Further optimization needed.")
        print("Check the recommendations above and run calibration tools.") 