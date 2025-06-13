import unittest
from unittest.mock import MagicMock
import cv2
import numpy as np

class MockHandGestureController:
    """Mock gesture controller for testing on Mac"""
    def __init__(self):
        self.enabled = True
        self.gesture_count = 0
        
    def get_gesture(self):
        """Simulate gesture detection - returns different gestures on each call"""
        self.gesture_count += 1
        if self.gesture_count == 1:
            print("[MOCK] No gesture detected")
            return None
        elif self.gesture_count == 2:
            print("[MOCK] Forward gesture detected (5 fingers)")
            return 'forward'
        elif self.gesture_count == 3:
            print("[MOCK] Backward gesture detected (fist)")
            return 'backward'
        else:
            return 'stop'
    
    def release(self):
        print("[MOCK] Camera released")

class MockMotorController:
    """Mock motor controller for testing on Mac"""
    def __init__(self):
        self.last_action = None
        self.actions_performed = []
        
    def move_forward(self):
        self.last_action = 'forward'
        self.actions_performed.append('forward')
        print("[MOCK] Motors moving forward")
        
    def move_backward(self):
        self.last_action = 'backward'
        self.actions_performed.append('backward')
        print("[MOCK] Motors moving backward")
        
    def turn_left(self):
        self.last_action = 'left'
        self.actions_performed.append('left')
        print("[MOCK] Motors turning left")
        
    def turn_right(self):
        self.last_action = 'right'
        self.actions_performed.append('right')
        print("[MOCK] Motors turning right")
        
    def stop(self):
        self.last_action = 'stop'
        self.actions_performed.append('stop')
        print("[MOCK] Motors stopped")

class DummyAssistant:
    def __init__(self):
        self.gesture_mode_started = False
        self.motor_controller = MockMotorController()
    
    def start_gesture_motor_control(self):
        print("[TEST] start_gesture_motor_control called!")
        self.gesture_mode_started = True
        
        # Create a new gesture controller for the control loop
        control_gesture_controller = MockHandGestureController()
        
        # Simulate the gesture control loop
        for i in range(3):
            gesture = control_gesture_controller.get_gesture()
            if gesture:
                print(f"[TEST] Processing gesture: {gesture}")
                if gesture == 'forward':
                    self.motor_controller.move_forward()
                elif gesture == 'backward':
                    self.motor_controller.move_backward()
                elif gesture == 'left':
                    self.motor_controller.turn_left()
                elif gesture == 'right':
                    self.motor_controller.turn_right()
                elif gesture == 'stop':
                    self.motor_controller.stop()
        
        control_gesture_controller.release()

class TestAutoGestureTrigger(unittest.TestCase):
    
    def test_auto_gesture_trigger_on_face_detection(self):
        """Test that gesture control starts when Sophia/Eladriel is detected with hand gesture"""
        print("\n=== Testing Auto Gesture Trigger ===")
        
        assistant = DummyAssistant()
        person_name = 'sophia'
        
        # Simulate face detection
        print(f"[TEST] Face detected: {person_name}")
        
        # Create gesture controller for initial detection
        detection_gesture_controller = MockHandGestureController()
        
        # Check for gesture
        gesture_detected = None
        for attempt in range(2):
            gesture = detection_gesture_controller.get_gesture()
            if gesture:
                gesture_detected = gesture
                break
        
        detection_gesture_controller.release()
        
        # If gesture detected, start gesture control
        if gesture_detected:
            print(f"[TEST] Hand gesture '{gesture_detected}' detected for {person_name}. Starting gesture control mode.")
            assistant.start_gesture_motor_control()
        
        # Assertions
        self.assertTrue(assistant.gesture_mode_started)
        self.assertIn('forward', assistant.motor_controller.actions_performed)
        self.assertIn('backward', assistant.motor_controller.actions_performed)
        print("[TEST] ✅ Auto gesture trigger test passed!")
        print(f"[TEST] Actions performed: {assistant.motor_controller.actions_performed}")
    
    def test_no_gesture_no_trigger(self):
        """Test that gesture control doesn't start if no gesture is detected"""
        print("\n=== Testing No Gesture Scenario ===")
        
        assistant = DummyAssistant()
        person_name = 'eladriel'
        print(f"[TEST] Face detected: {person_name}")
        
        # Create gesture controller for detection (simulate no gesture)
        detection_gesture_controller = MockHandGestureController()
        detection_gesture_controller.gesture_count = 10  # Will return 'stop'
        
        # Check for gesture (simulate no gesture detected)
        gesture_detected = None
        gesture = detection_gesture_controller.get_gesture()
        if gesture and gesture != 'stop':
            gesture_detected = gesture
        
        detection_gesture_controller.release()
        
        if not gesture_detected:
            print("[TEST] No hand gesture detected. Gesture control not started.")
        
        # Assertions
        self.assertFalse(assistant.gesture_mode_started)
        self.assertEqual(len(assistant.motor_controller.actions_performed), 0)
        print("[TEST] ✅ No gesture scenario test passed!")

if __name__ == '__main__':
    print("🤖 Testing Gesture Control on Mac (Hardware-Free)")
    print("=" * 50)
    unittest.main(verbosity=2) 