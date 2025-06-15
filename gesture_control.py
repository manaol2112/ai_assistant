"""
gesture_control.py
Premium Hand Gesture Recognition for Robot Control (MediaPipe + OpenCV)
Enhanced with visual feedback and robust finger counting
"""
import sys
import platform
import time

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None
    np = None

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    mp = None

class HandGestureController:
    """
    HandGestureController uses MediaPipe + OpenCV for robust hand gesture detection.
    Maps finger counts to robot actions:
    - 5 fingers (open hand) = forward
    - 0 fingers (fist) = backward  
    - 2 fingers (peace sign) = left
    - 3 fingers = right
    - 1 finger (pointing) = stop
    """
    
    def __init__(self, camera_index=0, use_mediapipe=True, show_debug=False):
        """
        Initialize gesture controller with MediaPipe or OpenCV fallback
        
        Args:
            camera_index: Camera device index (default 0)
            use_mediapipe: Use MediaPipe for better accuracy (default True)
            show_debug: Show debug window with hand detection (default False)
        """
        self.camera_index = camera_index
        self.use_mediapipe = use_mediapipe and MEDIAPIPE_AVAILABLE
        self.show_debug = show_debug
        self.enabled = False
        self.cap = None
        self.mp_hands = None
        self.hands = None
        self.mp_draw = None
        
        # Initialize camera
        if not CV2_AVAILABLE:
            print("[HandGestureController] ❌ OpenCV not available. Gesture control disabled.")
            return
            
        try:
            print(f"[HandGestureController] 📷 Initializing camera {camera_index}...")
            self.cap = cv2.VideoCapture(camera_index)
            
            if not self.cap.isOpened():
                print(f"[HandGestureController] ❌ Camera {camera_index} not available.")
                return
                
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.enabled = True
            print(f"[HandGestureController] ✅ Camera {camera_index} initialized")
            
        except Exception as e:
            print(f"[HandGestureController] ❌ Camera initialization failed: {e}")
            return
        
        # Initialize MediaPipe if available
        if self.use_mediapipe:
            try:
                print("[HandGestureController] 🤖 Initializing MediaPipe hands...")
                self.mp_hands = mp.solutions.hands
                self.hands = self.mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.5
                )
                self.mp_draw = mp.solutions.drawing_utils
                print("[HandGestureController] ✅ MediaPipe hands initialized")
                
            except Exception as e:
                print(f"[HandGestureController] ⚠️ MediaPipe initialization failed: {e}")
                print("[HandGestureController] Falling back to OpenCV detection...")
                self.use_mediapipe = False
        
        if not self.use_mediapipe:
            print("[HandGestureController] 📋 Using OpenCV-based gesture detection")

    def count_fingers_mediapipe(self, landmarks):
        """Count fingers using MediaPipe hand landmarks"""
        if not landmarks:
            return 0
            
        # Finger tip and pip landmark indices
        tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        pip_ids = [3, 6, 10, 14, 18]  # Corresponding PIP joints
        
        fingers = []
        
        # Thumb (special case - compare x coordinates)
        if landmarks[tip_ids[0]].x > landmarks[pip_ids[0]].x:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Other fingers (compare y coordinates)
        for i in range(1, 5):
            if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return sum(fingers)

    def count_fingers_opencv(self, frame):
        """Fallback finger counting using OpenCV contours"""
        try:
            # Convert to HSV for better skin detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Improved skin color range
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # Create mask
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Morphological operations to clean up the mask
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return 0
                
            # Get the largest contour (hand)
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
                        
                        # If angle is less than 90 degrees, count as finger
                        if angle <= np.pi/2:
                            finger_count += 1
                    
                    return finger_count + 1  # Add 1 for the thumb
            
            return 0
            
        except Exception as e:
            print(f"[HandGestureController] OpenCV finger counting error: {e}")
            return 0

    def get_gesture(self):
        """Get current gesture from camera feed"""
        if not self.enabled or not self.cap:
            return None
            
        try:
            ret, frame = self.cap.read()
            if not ret:
                return None
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            finger_count = 0
            
            if self.use_mediapipe:
                # MediaPipe detection
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Count fingers
                        finger_count = self.count_fingers_mediapipe(hand_landmarks.landmark)
                        
                        # Draw hand landmarks if debug mode
                        if self.show_debug:
                            self.mp_draw.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        break
            else:
                # OpenCV fallback detection
                finger_count = self.count_fingers_opencv(frame)
            
            # Show debug window if enabled
            if self.show_debug:
                # Add finger count text
                cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Add gesture action text
                action = self.map_fingers_to_action(finger_count)
                if action:
                    cv2.putText(frame, f"Action: {action}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                cv2.imshow('Hand Gesture Detection', frame)
                cv2.waitKey(1)
            
            return self.map_fingers_to_action(finger_count)
            
        except Exception as e:
            print(f"[HandGestureController] Gesture detection error: {e}")
            return None

    def map_fingers_to_action(self, finger_count):
        """Map finger count to robot action"""
        finger_map = {
            5: 'forward',    # Open hand = forward
            0: 'backward',   # Fist = backward
            2: 'left',       # Peace sign = left
            3: 'right',      # Three fingers = right
            1: 'stop'        # One finger = stop
        }
        
        return finger_map.get(finger_count, None)

    def test_detection(self, duration=30):
        """Test gesture detection with visual feedback"""
        if not self.enabled:
            print("❌ Gesture controller not enabled")
            return False
            
        print(f"🧪 Testing gesture detection for {duration} seconds...")
        print("📋 Gesture mapping:")
        print("   🖐️ 5 fingers (open hand) = FORWARD")
        print("   ✊ 0 fingers (fist) = BACKWARD") 
        print("   ✌️ 2 fingers (peace) = LEFT")
        print("   🤟 3 fingers = RIGHT")
        print("   ☝️ 1 finger (point) = STOP")
        print("\nPress 'q' to quit early")
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                frame = cv2.flip(frame, 1)
                finger_count = 0
                
                if self.use_mediapipe:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(rgb_frame)
                    
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            finger_count = self.count_fingers_mediapipe(hand_landmarks.landmark)
                            self.mp_draw.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                            break
                else:
                    finger_count = self.count_fingers_opencv(frame)
                
                # Add overlay information
                cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                action = self.map_fingers_to_action(finger_count)
                if action:
                    cv2.putText(frame, f"Action: {action.upper()}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    print(f"🖐️ Detected: {finger_count} fingers → {action.upper()}")
                
                # Add instructions
                cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.imshow('Gesture Detection Test', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted")
        finally:
            cv2.destroyAllWindows()
            
        print("✅ Gesture detection test completed")
        return True

    def release(self):
        """Release camera and cleanup resources"""
        try:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            print("[HandGestureController] 📷 Camera released")
        except Exception as e:
            print(f"[HandGestureController] Cleanup error: {e}")

    def get_status(self):
        """Get current status of gesture controller"""
        if not self.enabled:
            return "Gesture controller disabled"
        elif self.use_mediapipe:
            return "MediaPipe gesture detection active"
        else:
            return "OpenCV gesture detection active" 