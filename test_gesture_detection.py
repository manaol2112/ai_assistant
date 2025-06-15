#!/usr/bin/env python3
"""
test_gesture_detection.py
Comprehensive Gesture Detection Test for Raspberry Pi
Tests both MediaPipe and OpenCV gesture recognition
"""

import sys
import time
import platform
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    missing_deps = []
    
    # Check OpenCV
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} installed")
    except ImportError:
        print("❌ OpenCV not installed")
        missing_deps.append("opencv-python")
    
    # Check NumPy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} installed")
    except ImportError:
        print("❌ NumPy not installed")
        missing_deps.append("numpy")
    
    # Check MediaPipe
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe {mp.__version__} installed")
        mediapipe_available = True
    except ImportError:
        print("⚠️ MediaPipe not installed (will use OpenCV fallback)")
        missing_deps.append("mediapipe")
        mediapipe_available = False
    
    if missing_deps:
        print(f"\n📦 Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install " + " ".join(missing_deps))
        return False, mediapipe_available
    
    return True, mediapipe_available

def check_camera():
    """Check if camera is available using CameraHandler (Sony IMX500 AI Camera support)"""
    print("\n📷 Checking camera availability...")
    
    try:
        # First try CameraHandler (supports Sony IMX500 AI Camera)
        try:
            from camera_handler import CameraHandler
            print("🤖 Testing CameraHandler (Sony IMX500 AI Camera support)...")
            
            camera_handler = CameraHandler(camera_index=0, prefer_imx500=True)
            
            if camera_handler.is_camera_available():
                # Test reading a frame
                ret, frame = camera_handler.read()
                if ret and frame is not None:
                    camera_type = "Sony IMX500 AI" if camera_handler.using_imx500 else "USB"
                    print(f"✅ {camera_type} Camera working via CameraHandler - Resolution: {frame.shape[1]}x{frame.shape[0]}")
                    
                    # Get AI status if available
                    ai_status = camera_handler.get_ai_status()
                    if ai_status.get('ai_enabled', False):
                        print("🎯 AI features available")
                    
                    camera_handler.release()
                    return 0  # Return 0 as camera index for compatibility
                else:
                    print("⚠️ CameraHandler opened but no frame")
            else:
                print("❌ CameraHandler failed to initialize")
                
        except ImportError:
            print("⚠️ CameraHandler not available, trying direct OpenCV access...")
        
        # Fallback to direct OpenCV camera access
        import cv2
        print("📷 Testing direct OpenCV camera access...")
        
        # Try different camera indices
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"✅ OpenCV Camera {i} working - Resolution: {frame.shape[1]}x{frame.shape[0]}")
                    cap.release()
                    return i
                else:
                    print(f"⚠️ OpenCV Camera {i} opened but no frame")
            cap.release()
        
        print("❌ No working camera found")
        return None
        
    except Exception as e:
        print(f"❌ Camera check failed: {e}")
        return None

def test_basic_gesture_detection():
    """Test basic gesture detection functionality"""
    print("\n🧪 Testing basic gesture detection...")
    
    try:
        from gesture_control import HandGestureController
        
        # Test with debug mode enabled
        controller = HandGestureController(show_debug=True)
        
        if not controller.enabled:
            print("❌ Gesture controller failed to initialize")
            return False
        
        print(f"✅ Gesture controller initialized: {controller.get_status()}")
        
        # Run test detection
        print("\n🎯 Starting gesture detection test...")
        print("Show these gestures to test:")
        print("🖐️ Open hand (5 fingers) → FORWARD")
        print("✊ Closed fist (0 fingers) → BACKWARD")
        print("✌️ Peace sign (2 fingers) → LEFT")
        print("🤟 Three fingers → RIGHT")
        print("☝️ One finger → STOP")
        
        success = controller.test_detection(duration=30)
        controller.release()
        
        return success
        
    except Exception as e:
        print(f"❌ Gesture detection test failed: {e}")
        return False

def test_motor_integration():
    """Test gesture detection with motor control integration"""
    print("\n🤖 Testing motor integration...")
    
    try:
        from main import AIAssistant
        
        # Initialize AI Assistant
        assistant = AIAssistant()
        
        print("✅ AI Assistant initialized")
        
        # Test voice-triggered gesture control
        print("\n🎤 Testing voice-triggered gesture control...")
        print("Testing with simulated voice command...")
        
        # Simulate voice command for testing with required target_user parameter
        response = assistant.start_voice_triggered_gesture_control("TestUser")
        print(f"Response: {response}")
        
        # Test if gesture controller is working
        if hasattr(assistant, 'gesture_controller') and assistant.gesture_controller:
            print("✅ Gesture controller integrated successfully")
            return True
        else:
            print("⚠️ Gesture controller not found in assistant")
            return False
        
    except Exception as e:
        print(f"❌ Motor integration test failed: {e}")
        return False

def run_performance_test():
    """Test gesture detection performance"""
    print("\n⚡ Running performance test...")
    
    try:
        from gesture_control import HandGestureController
        import time
        
        controller = HandGestureController()
        
        if not controller.enabled:
            print("❌ Controller not available for performance test")
            return False
        
        print("📊 Testing detection speed (10 seconds)...")
        
        start_time = time.time()
        frame_count = 0
        detection_count = 0
        
        while time.time() - start_time < 10:
            gesture = controller.get_gesture()
            frame_count += 1
            
            if gesture:
                detection_count += 1
                print(f"🖐️ Detected: {gesture}")
        
        elapsed = time.time() - start_time
        fps = frame_count / elapsed
        detection_rate = (detection_count / frame_count) * 100 if frame_count > 0 else 0
        
        print(f"📈 Performance Results:")
        print(f"   Frames processed: {frame_count}")
        print(f"   Average FPS: {fps:.1f}")
        print(f"   Gestures detected: {detection_count}")
        print(f"   Detection rate: {detection_rate:.1f}%")
        
        controller.release()
        
        # Adjust expectations for high-resolution AI cameras
        if fps >= 5:
            print("✅ Performance: Excellent (≥5 FPS)")
            return True
        elif fps >= 2:
            print("✅ Performance: Good (≥2 FPS) - Acceptable for AI camera")
            return True
        elif fps >= 1:
            print("⚠️ Performance: Fair (≥1 FPS) - Usable but slow")
            return True
        else:
            print("❌ Performance: Poor (<1 FPS)")
            return False
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def install_missing_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing missing dependencies...")
    
    try:
        # Update pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install required packages
        packages = ["opencv-python", "numpy", "mediapipe"]
        
        for package in packages:
            print(f"Installing {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}: {result.stderr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 AI Robot Gesture Detection Test Suite")
    print("=" * 50)
    
    # System info
    print(f"🖥️ System: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working directory: {sys.path[0]}")
    
    # Check dependencies
    deps_ok, mediapipe_available = check_dependencies()
    
    if not deps_ok:
        install_choice = input("\n❓ Install missing dependencies? (y/n): ").lower()
        if install_choice == 'y':
            if install_missing_dependencies():
                print("✅ Dependencies installed. Please restart the test.")
                return
            else:
                print("❌ Failed to install dependencies")
                return
        else:
            print("❌ Cannot proceed without dependencies")
            return
    
    # Check camera
    camera_index = check_camera()
    if camera_index is None:
        print("❌ Cannot proceed without camera")
        return
    
    # Run tests
    tests = [
        ("Basic Gesture Detection", test_basic_gesture_detection),
        ("Performance Test", run_performance_test),
        ("Motor Integration", test_motor_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            result = test_func()
            results[test_name] = result
            
            if result:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                
        except KeyboardInterrupt:
            print(f"\n🛑 {test_name} interrupted by user")
            results[test_name] = False
            break
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*20} TEST SUMMARY {'='*20}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gesture detection is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    # Recommendations
    print(f"\n{'='*20} RECOMMENDATIONS {'='*20}")
    
    if not mediapipe_available:
        print("📝 Install MediaPipe for better gesture accuracy:")
        print("   pip install mediapipe")
    
    if camera_index != 0:
        print(f"📝 Camera found at index {camera_index}, not 0")
        print("   Update camera_index in your code if needed")
    
    print("📝 For best results:")
    print("   - Ensure good lighting")
    print("   - Keep hand clearly visible")
    print("   - Use distinct finger positions")
    print("   - Avoid background clutter")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Test suite interrupted")
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        import traceback
        traceback.print_exc() 