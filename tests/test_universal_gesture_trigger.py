import unittest
from unittest.mock import MagicMock
import time

class MockHandGestureController:
    """Mock gesture controller for testing universal gesture trigger"""
    def __init__(self):
        self.enabled = True
        self.gesture_sequence = ['forward', 'left', 'backward', 'right', 'stop']
        self.call_count = 0
        
    def get_gesture(self):
        """Return different gestures in sequence"""
        if self.call_count < len(self.gesture_sequence):
            gesture = self.gesture_sequence[self.call_count]
            self.call_count += 1
            print(f"[MOCK] Gesture detected: {gesture}")
            return gesture
        return 'stop'
    
    def release(self):
        print("[MOCK] Gesture controller released")

class MockMotorController:
    """Mock motor controller for testing"""
    def __init__(self):
        self.enabled = True
        self.actions_performed = []
        
    def move_forward(self):
        self.actions_performed.append('forward')
        print("[MOCK] Motors moving forward")
        
    def move_backward(self):
        self.actions_performed.append('backward')
        print("[MOCK] Motors moving backward")
        
    def turn_left(self):
        self.actions_performed.append('left')
        print("[MOCK] Motors turning left")
        
    def turn_right(self):
        self.actions_performed.append('right')
        print("[MOCK] Motors turning right")
        
    def stop(self):
        self.actions_performed.append('stop')
        print("[MOCK] Motors stopped")
        
    def cleanup(self):
        print("[MOCK] Motor controller cleanup")

class MockAssistant:
    """Mock assistant for testing universal gesture trigger"""
    def __init__(self):
        self.gesture_control_started = False
        self.visual = None
        
    def start_gesture_motor_control(self):
        """Simulate gesture motor control"""
        print("[TEST] start_gesture_motor_control called!")
        self.gesture_control_started = True
        
        # Simulate the gesture control process
        motor = MockMotorController()
        gesture = MockHandGestureController()
        
        print("🖐️ Hand gesture control started (TESTING MODE)")
        
        # Simulate a few gesture detections
        for i in range(3):
            action = gesture.get_gesture()
            if action and action != 'stop':
                print(f"Processing gesture: {action}")
                if action == 'forward':
                    motor.move_forward()
                elif action == 'backward':
                    motor.move_backward()
                elif action == 'left':
                    motor.turn_left()
                elif action == 'right':
                    motor.turn_right()
            else:
                motor.stop()
                break
        
        gesture.release()
        motor.cleanup()
        return "Gesture control completed"

def simulate_face_detection_with_gesture(person_name, confidence=0.8):
    """Simulate the face detection + gesture trigger logic"""
    print(f"\n=== Simulating Face Detection for {person_name} ===")
    
    assistant = MockAssistant()
    
    # Simulate face detection
    print(f"🎭 Face detected: {person_name} (confidence: {confidence:.2f})")
    
    if confidence < 0.45:
        print("❌ Confidence too low, skipping...")
        return False
    
    # Simulate gesture detection
    try:
        gesture_controller = MockHandGestureController()
        if gesture_controller.enabled:
            print(f"🖐️ Checking for hand gestures from {person_name}...")
            
            # Quick gesture detection (2 attempts)
            gesture_detected = None
            for attempt in range(2):
                print(f"   👁️ Gesture detection attempt {attempt + 1}/2...")
                gesture = gesture_controller.get_gesture()
                print(f"   📊 Raw gesture result: {gesture}")
                
                if gesture and gesture != 'stop':
                    gesture_detected = gesture
                    print(f"   ✅ Valid gesture detected: {gesture_detected}")
                    break
                elif gesture == 'stop':
                    print(f"   ⏹️ Stop gesture detected, ignoring for auto-trigger")
                else:
                    print(f"   ❌ No gesture detected on attempt {attempt + 1}")
                
                time.sleep(0.1)  # Brief pause
            
            gesture_controller.release()
            print(f"   🔄 Gesture controller released")
            
            if gesture_detected:
                print(f"🎮 GESTURE VALIDATION SUCCESS! Hand gesture '{gesture_detected}' detected from {person_name}!")
                print(f"🚀 Starting gesture control mode...")
                assistant.start_gesture_motor_control()
                return True
            else:
                print(f"❌ GESTURE VALIDATION FAILED: No valid gesture detected from {person_name} after 2 attempts")
                return False
        else:
            print(f"⚠️ Gesture controller not enabled for {person_name}")
            return False
    
    except Exception as e:
        print(f"⚠️ Error in gesture detection for {person_name}: {e}")
        return False

class TestUniversalGestureTrigger(unittest.TestCase):
    
    def test_sophia_gesture_trigger(self):
        """Test gesture trigger for Sophia"""
        print("\n🧪 Testing Sophia gesture trigger...")
        result = simulate_face_detection_with_gesture('sophia', 0.85)
        self.assertTrue(result, "Sophia should be able to trigger gesture control")
    
    def test_eladriel_gesture_trigger(self):
        """Test gesture trigger for Eladriel"""
        print("\n🧪 Testing Eladriel gesture trigger...")
        result = simulate_face_detection_with_gesture('eladriel', 0.90)
        self.assertTrue(result, "Eladriel should be able to trigger gesture control")
    
    def test_parent_gesture_trigger(self):
        """Test gesture trigger for Parent"""
        print("\n🧪 Testing Parent gesture trigger...")
        result = simulate_face_detection_with_gesture('parent', 0.75)
        self.assertTrue(result, "Parent should be able to trigger gesture control")
    
    def test_unknown_user_gesture_trigger(self):
        """Test gesture trigger for unknown user"""
        print("\n🧪 Testing Unknown user gesture trigger...")
        result = simulate_face_detection_with_gesture('john', 0.70)
        self.assertTrue(result, "Any user should be able to trigger gesture control in testing mode")
    
    def test_low_confidence_no_trigger(self):
        """Test that low confidence faces don't trigger gesture control"""
        print("\n🧪 Testing low confidence face...")
        result = simulate_face_detection_with_gesture('sophia', 0.30)
        self.assertFalse(result, "Low confidence faces should not trigger gesture control")
    
    def test_multiple_users_sequential(self):
        """Test multiple users can trigger gesture control"""
        print("\n🧪 Testing multiple users sequentially...")
        
        users = ['sophia', 'eladriel', 'parent', 'visitor', 'friend']
        results = []
        
        for user in users:
            result = simulate_face_detection_with_gesture(user, 0.80)
            results.append(result)
            print(f"✅ {user}: {'SUCCESS' if result else 'FAILED'}")
        
        # All users should be able to trigger gesture control
        self.assertTrue(all(results), "All users should be able to trigger gesture control")
        print(f"\n🎉 Universal gesture control test: {sum(results)}/{len(results)} users successful!")

if __name__ == '__main__':
    print("🤖 Testing Universal Gesture Control (Anyone Can Control!)")
    print("=" * 60)
    print("🎯 TESTING MODE: Any detected face can trigger gesture control")
    print("=" * 60)
    unittest.main(verbosity=2) 