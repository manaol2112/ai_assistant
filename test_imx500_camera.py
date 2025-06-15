#!/usr/bin/env python3
"""
Test script for Sony IMX500 AI Camera using libcamera system
This script tests the camera functionality without picamera2 dependency
"""

import sys
import logging
from camera_handler import CameraHandler

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_camera_initialization():
    """Test camera initialization"""
    print("🧪 Testing Sony IMX500 Camera Initialization...")
    
    try:
        camera = CameraHandler(prefer_imx500=True)
        
        if camera.is_camera_available():
            print("✅ Camera initialized successfully!")
            
            # Get AI status
            ai_status = camera.get_ai_status()
            print(f"📊 AI Status: {ai_status}")
            
            return camera
        else:
            print("❌ Camera initialization failed")
            return None
            
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        return None

def test_frame_capture(camera):
    """Test single frame capture"""
    print("\n🖼️ Testing Frame Capture...")
    
    try:
        ret, frame = camera.read()
        
        if ret and frame is not None:
            print(f"✅ Frame captured successfully! Shape: {frame.shape}")
            return True
        else:
            print("❌ Failed to capture frame")
            return False
            
    except Exception as e:
        print(f"❌ Error capturing frame: {e}")
        return False

def test_image_capture(camera):
    """Test high-resolution image capture"""
    print("\n📸 Testing Image Capture...")
    
    try:
        filepath = camera.capture_image("test_imx500.jpg")
        
        if filepath:
            print(f"✅ Image captured successfully: {filepath}")
            return True
        else:
            print("❌ Failed to capture image")
            return False
            
    except Exception as e:
        print(f"❌ Error capturing image: {e}")
        return False

def test_preview(camera):
    """Test camera preview"""
    print("\n🖥️ Testing Camera Preview...")
    
    try:
        print("Starting 5-second preview...")
        success = camera.show_preview(duration=5)
        
        if success:
            print("✅ Preview completed successfully")
            return True
        else:
            print("❌ Preview failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during preview: {e}")
        return False

def test_ai_features(camera):
    """Test AI object detection features"""
    print("\n🤖 Testing AI Features...")
    
    try:
        # Test object detection
        objects = camera.detect_objects()
        print(f"🎯 Object detection results: {len(objects)} objects detected")
        
        for i, obj in enumerate(objects):
            print(f"   Object {i+1}: {obj}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI features: {e}")
        return False

def main():
    """Main test function"""
    print("🤖 Sony IMX500 AI Camera Test Suite")
    print("=" * 50)
    
    # Test 1: Camera Initialization
    camera = test_camera_initialization()
    if not camera:
        print("\n❌ Camera initialization failed. Exiting.")
        sys.exit(1)
    
    try:
        # Test 2: Frame Capture
        frame_success = test_frame_capture(camera)
        
        # Test 3: Image Capture
        image_success = test_image_capture(camera)
        
        # Test 4: Preview (optional - comment out if running headless)
        preview_success = test_preview(camera)
        
        # Test 5: AI Features
        ai_success = test_ai_features(camera)
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY")
        print("=" * 50)
        print(f"Camera Initialization: {'✅' if camera else '❌'}")
        print(f"Frame Capture: {'✅' if frame_success else '❌'}")
        print(f"Image Capture: {'✅' if image_success else '❌'}")
        print(f"Preview: {'✅' if preview_success else '❌'}")
        print(f"AI Features: {'✅' if ai_success else '❌'}")
        
        all_passed = all([camera, frame_success, image_success, preview_success, ai_success])
        
        if all_passed:
            print("\n🎉 All tests passed! Sony IMX500 camera is working perfectly!")
        else:
            print("\n⚠️ Some tests failed. Check the output above for details.")
        
    finally:
        # Clean up
        if camera:
            camera.release()
            print("\n🧹 Camera resources released")

if __name__ == "__main__":
    main() 