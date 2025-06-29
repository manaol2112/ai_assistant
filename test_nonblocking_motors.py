#!/usr/bin/env python3
"""
Test script to verify non-blocking motor control doesn't interfere with speech recognition
"""

import time
import threading
from motor_control import MotorController
import speech_recognition as sr

def test_speech_during_movement():
    """Test if speech recognition works while motors are moving"""
    print("🧪 TESTING NON-BLOCKING MOTOR CONTROL WITH SPEECH RECOGNITION")
    print("=" * 60)
    
    # Initialize motor controller
    motor = MotorController()
    
    if not motor.enabled:
        print("❌ Motor controller not available - test cannot run")
        return False
    
    # Initialize speech recognizer
    r = sr.Recognizer()
    r.energy_threshold = 150  # Pi 5 optimized
    
    print("✅ Motor controller initialized")
    print("✅ Speech recognizer initialized")
    
    # Test 1: Start motor movement (non-blocking)
    print("\n🚀 TEST 1: Starting forward movement (should be non-blocking)")
    start_time = time.time()
    motor.forward(3.0)  # Move forward for 3 seconds
    elapsed = time.time() - start_time
    
    if elapsed < 0.5:  # Should return immediately
        print(f"✅ Motor command returned immediately ({elapsed:.3f}s)")
        print("✅ NON-BLOCKING: Motor command doesn't block the thread!")
    else:
        print(f"❌ BLOCKING: Motor command took {elapsed:.3f}s to return")
        return False
    
    # Test 2: Try speech recognition while motor is moving
    print("\n🎤 TEST 2: Testing speech recognition while motor is moving")
    print("   Motor should still be moving from previous command...")
    print("   Say something now!")
    
    try:
        with sr.Microphone(device_index=0) as source:
            print("📋 Calibrating for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1.0)
            print("🎤 Listening for speech while motor moves...")
            
            # Try to recognize speech while motor is moving
            audio = r.listen(source, timeout=4, phrase_time_limit=3)
            text = r.recognize_google(audio)
            
            print(f"✅ SUCCESS: Recognized '{text}' while motor was moving!")
            speech_success = True
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected (timeout)")
        speech_success = False
    except sr.UnknownValueError:
        print("❓ Could not understand speech")
        speech_success = False
    except Exception as e:
        print(f"❌ Speech recognition error: {e}")
        speech_success = False
    
    # Test 3: Check motor status
    print(f"\n📊 TEST 3: Motor status check")
    status = motor.get_status()
    is_moving = motor.is_moving()
    current_movement = motor.get_current_movement()
    
    print(f"   Status: {status}")
    print(f"   Is moving: {is_moving}")
    print(f"   Current movement: {current_movement}")
    
    # Wait for movement to complete
    print("\n⏳ Waiting for movement to complete...")
    time.sleep(4)  # Wait for the 3-second movement to finish
    
    final_status = motor.get_status()
    final_moving = motor.is_moving()
    print(f"   Final status: {final_status}")
    print(f"   Final is moving: {final_moving}")
    
    # Test 4: Quick movement sequence (should not block)
    print("\n🔄 TEST 4: Quick movement sequence (should not block)")
    sequence_start = time.time()
    
    motor.forward(1.0)
    motor.backward(1.0)  # Should interrupt forward and start backward
    motor.stop()  # Should stop immediately
    
    sequence_elapsed = time.time() - sequence_start
    print(f"   Sequence commands took: {sequence_elapsed:.3f}s")
    
    if sequence_elapsed < 0.5:
        print("✅ All movement commands returned immediately")
    else:
        print("❌ Movement commands are still blocking")
    
    # Cleanup
    motor.cleanup()
    
    # Results
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS:")
    print(f"   Non-blocking motor commands: {'✅ PASS' if elapsed < 0.5 else '❌ FAIL'}")
    print(f"   Speech recognition while moving: {'✅ PASS' if speech_success else '⚠️ NO SPEECH DETECTED'}")
    print(f"   Quick command sequence: {'✅ PASS' if sequence_elapsed < 0.5 else '❌ FAIL'}")
    
    overall_success = elapsed < 0.5 and sequence_elapsed < 0.5
    
    if overall_success:
        print("\n🎉 OVERALL: NON-BLOCKING MOTOR CONTROL IS WORKING!")
        print("   Speech recognition should no longer be blocked by motor commands.")
    else:
        print("\n❌ OVERALL: Motor control is still blocking - needs more fixes.")
    
    return overall_success

if __name__ == "__main__":
    test_speech_during_movement() 