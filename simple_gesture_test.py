#!/usr/bin/env python3
"""
simple_gesture_test.py
Quick and simple gesture detection test
Perfect for debugging gesture recognition issues
"""

import sys
import time

def test_gesture_detection():
    """Simple gesture detection test"""
    print("🚀 Simple Gesture Detection Test")
    print("=" * 40)
    
    # Check if OpenCV is available
    try:
        import cv2
        import numpy as np
        print(f"✅ OpenCV {cv2.__version__} loaded")
    except ImportError:
        print("❌ OpenCV not installed. Install with: pip install opencv-python")
        return False
    
    # Check MediaPipe
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe {mp.__version__} loaded")
        use_mediapipe = True
    except ImportError:
        print("⚠️ MediaPipe not available, using OpenCV fallback")
        use_mediapipe = False
    
    # Initialize camera
    print("\n📷 Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Camera not available")
        return False
    
    print("✅ Camera initialized")
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Initialize MediaPipe if available
    if use_mediapipe:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        mp_draw = mp.solutions.drawing_utils
    
    print("\n🎯 Gesture Detection Started!")
    print("📋 Show these gestures:")
    print("   🖐️ 5 fingers (open hand) = FORWARD")
    print("   ✊ 0 fingers (fist) = BACKWARD")
    print("   ✌️ 2 fingers (peace) = LEFT") 
    print("   🤟 3 fingers = RIGHT")
    print("   ☝️ 1 finger = STOP")
    print("\nPress 'q' to quit")
    
    def count_fingers_mediapipe(landmarks):
        """Count fingers using MediaPipe"""
        if not landmarks:
            return 0
        
        # Finger tip and pip indices
        tip_ids = [4, 8, 12, 16, 20]
        pip_ids = [3, 6, 10, 14, 18]
        
        fingers = []
        
        # Thumb (x-coordinate comparison)
        if landmarks[tip_ids[0]].x > landmarks[pip_ids[0]].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers (y-coordinate comparison)
        for i in range(1, 5):
            if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)
    
    def count_fingers_opencv(frame):
        """Count fingers using OpenCV"""
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Skin color range
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Clean up mask
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return 0
            
            # Get largest contour
            hand_contour = max(contours, key=cv2.contourArea)
            
            # Calculate convex hull and defects
            hull = cv2.convexHull(hand_contour, returnPoints=False)
            
            if len(hull) > 3:
                defects = cv2.convexityDefects(hand_contour, hull)
                
                if defects is not None:
                    finger_count = 0
                    
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(hand_contour[s][0])
                        end = tuple(hand_contour[e][0])
                        far = tuple(hand_contour[f][0])
                        
                        # Calculate angle
                        a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                        b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                        c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                        
                        angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c + 1e-10))
                        
                        if angle <= np.pi/2:
                            finger_count += 1
                    
                    return finger_count + 1
            
            return 0
            
        except Exception as e:
            return 0
    
    def map_fingers_to_action(finger_count):
        """Map finger count to action"""
        finger_map = {
            5: 'FORWARD',
            0: 'BACKWARD', 
            2: 'LEFT',
            3: 'RIGHT',
            1: 'STOP'
        }
        return finger_map.get(finger_count, None)
    
    # Main detection loop
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            finger_count = 0
            
            if use_mediapipe:
                # MediaPipe detection
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        finger_count = count_fingers_mediapipe(hand_landmarks.landmark)
                        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        break
            else:
                # OpenCV detection
                finger_count = count_fingers_opencv(frame)
            
            # Add text overlay
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            action = map_fingers_to_action(finger_count)
            if action:
                cv2.putText(frame, f"Action: {action}", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print(f"🖐️ {finger_count} fingers → {action}")
            
            # Add instructions
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            cv2.imshow('Simple Gesture Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Test completed")
    
    return True

if __name__ == "__main__":
    try:
        test_gesture_detection()
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc() 