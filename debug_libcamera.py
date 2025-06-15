#!/usr/bin/env python3
"""
Debug script for libcamera and Sony IMX500 camera
Tests libcamera commands step by step to identify issues
"""

import subprocess
import os
import time
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, timeout=10, description=""):
    """Run a command and return result with detailed logging"""
    print(f"\n🧪 Testing: {description}")
    print(f"📝 Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        
        print(f"📊 Return code: {result.returncode}")
        
        if result.stdout:
            print(f"✅ STDOUT:\n{result.stdout}")
        
        if result.stderr:
            print(f"⚠️ STDERR:\n{result.stderr}")
        
        return result.returncode == 0, result
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Command timed out after {timeout} seconds")
        return False, None
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False, None
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False, None

def main():
    """Main diagnostic function"""
    print("🤖 Sony IMX500 / libcamera Diagnostic Tool")
    print("=" * 50)
    
    # Test 1: Check if libcamera commands exist
    print("\n📋 STEP 1: Checking libcamera installation")
    commands_to_check = ['libcamera-hello', 'libcamera-still', 'libcamera-vid']
    
    for cmd in commands_to_check:
        success, _ = run_command(['which', cmd], description=f"Finding {cmd}")
        if not success:
            print(f"❌ {cmd} not found - install with: sudo apt install libcamera-apps")
    
    # Test 2: List cameras
    print("\n📋 STEP 2: Camera detection")
    success, result = run_command(['libcamera-hello', '--list-cameras'], 
                                timeout=15, description="Listing available cameras")
    
    if not success:
        print("❌ Camera detection failed - check camera connection")
        return
    
    # Test 3: Simple preview test (very short)
    print("\n📋 STEP 3: Quick preview test")
    success, result = run_command(['libcamera-hello', '--timeout', '1000', '--nopreview'], 
                                timeout=10, description="Quick preview test (1 second)")
    
    # Test 4: Simple image capture
    print("\n📋 STEP 4: Basic image capture")
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        success, result = run_command(['libcamera-still', '--output', temp_path, 
                                     '--timeout', '2000', '--nopreview'], 
                                    timeout=15, description="Basic image capture")
        
        if success and os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            print(f"✅ Image captured successfully: {temp_path} ({file_size} bytes)")
            
            # Try to read with OpenCV
            try:
                import cv2
                img = cv2.imread(temp_path)
                if img is not None:
                    print(f"✅ OpenCV can read image: {img.shape}")
                else:
                    print("❌ OpenCV cannot read the captured image")
            except ImportError:
                print("⚠️ OpenCV not available for image verification")
        else:
            print("❌ Image capture failed")
    
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    # Test 5: Check for AI models
    print("\n📋 STEP 5: AI model detection")
    ai_model_paths = [
        '/usr/share/imx500-models/',
        '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk',
        '/opt/imx500-models/',
        '/home/pi/imx500-models/'
    ]
    
    for path in ai_model_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path}")
            if os.path.isdir(path):
                try:
                    files = os.listdir(path)
                    print(f"   📁 Contains {len(files)} files: {files[:5]}...")
                except:
                    print("   📁 Directory exists but cannot list contents")
        else:
            print(f"❌ Not found: {path}")
    
    # Test 6: Test with AI model (if available)
    ai_model_path = '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk'
    if os.path.exists(ai_model_path):
        print("\n📋 STEP 6: AI model test")
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            success, result = run_command(['libcamera-still', '--output', temp_path, 
                                         '--timeout', '3000', '--nopreview',
                                         '--post-process-file', ai_model_path], 
                                        timeout=20, description="Image capture with AI model")
            
            if success and os.path.exists(temp_path):
                file_size = os.path.getsize(temp_path)
                print(f"✅ AI-enhanced image captured: {temp_path} ({file_size} bytes)")
            else:
                print("❌ AI-enhanced capture failed")
        
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    else:
        print("\n📋 STEP 6: Skipped (no AI model found)")
    
    # Test 7: System information
    print("\n📋 STEP 7: System information")
    
    # Check video devices
    success, result = run_command(['ls', '-la', '/dev/video*'], 
                                description="Video devices")
    
    # Check camera group membership
    success, result = run_command(['groups'], 
                                description="User groups")
    
    # Check libcamera version
    success, result = run_command(['libcamera-hello', '--version'], 
                                description="libcamera version")
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSTIC COMPLETE")
    print("=" * 50)
    print("\n💡 If tests failed:")
    print("1. Install libcamera: sudo apt install libcamera-apps")
    print("2. Add user to video group: sudo usermod -a -G video $USER")
    print("3. Reboot: sudo reboot")
    print("4. Check camera connection")
    print("5. Try manual test: libcamera-hello --list-cameras")

if __name__ == "__main__":
    main() 