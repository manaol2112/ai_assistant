#!/usr/bin/env python3
"""
Simple Camera Test Script
Tests the IMX500 camera handler in isolation to debug libcamera-still issues
"""

import logging
import sys
import os

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_camera_handler():
    """Test the IMX500 camera handler step by step"""
    print("🤖 Simple IMX500 Camera Test")
    print("=" * 40)
    
    try:
        # Import the camera handler
        from imx500_camera_handler import IMX500CameraHandler
        print("✅ IMX500CameraHandler imported successfully")
        
        # Initialize the camera
        print("\n📷 Initializing camera...")
        camera = IMX500CameraHandler(width=640, height=480, framerate=15)
        
        # Check if camera is available
        if not camera.is_camera_available():
            print("❌ Camera not available")
            return False
        
        print("✅ Camera initialized and available")
        
        # Test frame capture
        print("\n📸 Testing frame capture...")
        success, frame = camera.read()
        
        if success and frame is not None:
            print(f"✅ Frame captured successfully: {frame.shape}")
        else:
            print("❌ Frame capture failed")
            return False
        
        # Test image capture
        print("\n🖼️ Testing image capture...")
        image_path = camera.capture_image("test_simple.jpg")
        
        if image_path and os.path.exists(image_path):
            print(f"✅ Image captured successfully: {image_path}")
        else:
            print("❌ Image capture failed")
            return False
        
        # Test AI status
        print("\n🧠 Testing AI status...")
        ai_status = camera.get_ai_status()
        print(f"AI Status: {ai_status}")
        
        # Clean up
        camera.release()
        print("\n✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_libcamera():
    """Test libcamera commands directly"""
    print("\n🔧 Testing libcamera commands directly...")
    
    import subprocess
    import tempfile
    
    # Test 1: List cameras
    try:
        result = subprocess.run(['libcamera-hello', '--list-cameras'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ libcamera-hello --list-cameras works")
            print(f"Output: {result.stdout[:200]}...")
        else:
            print(f"❌ libcamera-hello failed: {result.stderr}")
    except Exception as e:
        print(f"❌ libcamera-hello error: {e}")
    
    # Test 2: Simple capture
    try:
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        result = subprocess.run(['libcamera-still', '-o', temp_path], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and os.path.exists(temp_path):
            print("✅ Direct libcamera-still works")
            os.unlink(temp_path)
        else:
            print(f"❌ Direct libcamera-still failed: {result.stderr}")
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"❌ Direct libcamera-still error: {e}")

if __name__ == "__main__":
    print("🚀 Starting simple camera tests...\n")
    
    # Test direct libcamera first
    test_direct_libcamera()
    
    # Then test our handler
    success = test_camera_handler()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Tests failed - check the logs above")
        sys.exit(1) 