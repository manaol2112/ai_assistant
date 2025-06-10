"""
Simple camera test to verify OpenCV camera access
"""

import cv2
import sys

def test_camera():
    print("🎥 Testing camera access...")
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot access camera")
        print("💡 On macOS, you may need to:")
        print("   1. Go to System Preferences > Security & Privacy > Camera")
        print("   2. Allow Terminal or your IDE to access the camera")
        print("   3. Restart Terminal/IDE after granting permission")
        return False
    
    print("✅ Camera opened successfully")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame captured: {frame.shape}")
        
        # Show camera for 5 seconds
        print("📹 Showing camera feed for 5 seconds...")
        print("Press 'q' to quit early")
        
        start_time = cv2.getTickCount()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Add text overlay
            cv2.putText(frame, "Camera Test - Press 'q' to quit", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Camera Test', frame)
            
            # Check for quit or timeout
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if elapsed > 5:
                break
        
        cv2.destroyAllWindows()
        print("✅ Camera test completed successfully")
        cap.release()
        return True
    else:
        print("❌ Cannot read from camera")
        cap.release()
        return False

if __name__ == "__main__":
    if test_camera():
        print("\n🎉 Camera is working! You can now run the smart camera detector:")
        print("python smart_camera_detector.py")
    else:
        print("\n🚫 Camera test failed. Please check permissions and try again.")
        sys.exit(1) 