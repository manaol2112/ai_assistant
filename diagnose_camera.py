#!/usr/bin/env python3
"""
Diagnostic script for Raspberry Pi 5 + Sony AITRIOS AI Camera issues
This script helps identify why picamera2 might not be working
"""

import os
import sys
import platform
import subprocess
import importlib.util

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def check_system_info():
    """Check basic system information"""
    print_header("SYSTEM INFORMATION")
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print(f"System: {platform.system()}")
    
    # Check if we're on Raspberry Pi
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
            print(f"Device model: {model}")
    except FileNotFoundError:
        print("Device model: Not a Raspberry Pi or /proc/device-tree/model not found")
    except Exception as e:
        print(f"Device model: Error reading - {e}")
    
    # Check OS version
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read()
            for line in os_info.split('\n'):
                if line.startswith('PRETTY_NAME='):
                    print(f"OS: {line.split('=')[1].strip('\"')}")
                    break
    except:
        print("OS: Unknown")

def check_camera_hardware():
    """Check camera hardware detection"""
    print_header("CAMERA HARDWARE DETECTION")
    
    # Check for camera devices
    video_devices = []
    for i in range(10):
        device_path = f"/dev/video{i}"
        if os.path.exists(device_path):
            video_devices.append(device_path)
    
    if video_devices:
        print(f"✅ Found video devices: {', '.join(video_devices)}")
    else:
        print("❌ No video devices found in /dev/")
    
    # Check camera detection via vcgencmd
    try:
        result = subprocess.run(['vcgencmd', 'get_camera'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ vcgencmd get_camera: {result.stdout.strip()}")
        else:
            print(f"❌ vcgencmd get_camera failed: {result.stderr.strip()}")
    except FileNotFoundError:
        print("⚠️ vcgencmd not found (not on Raspberry Pi?)")
    except subprocess.TimeoutExpired:
        print("⚠️ vcgencmd timeout")
    except Exception as e:
        print(f"❌ vcgencmd error: {e}")
    
    # Check libcamera detection
    try:
        result = subprocess.run(['libcamera-hello', '--list-cameras'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ libcamera-hello --list-cameras:")
            print(result.stdout)
        else:
            print(f"❌ libcamera-hello failed: {result.stderr.strip()}")
    except FileNotFoundError:
        print("⚠️ libcamera-hello not found")
    except subprocess.TimeoutExpired:
        print("⚠️ libcamera-hello timeout")
    except Exception as e:
        print(f"❌ libcamera-hello error: {e}")

def check_permissions():
    """Check camera permissions"""
    print_header("PERMISSIONS & GROUPS")
    
    import pwd
    import grp
    
    # Get current user
    current_user = pwd.getpwuid(os.getuid()).pw_name
    print(f"Current user: {current_user}")
    
    # Check groups
    try:
        user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
        print(f"User groups: {', '.join(user_groups)}")
        
        important_groups = ['video', 'camera', 'gpio']
        for group in important_groups:
            if group in user_groups:
                print(f"✅ User is in {group} group")
            else:
                print(f"❌ User is NOT in {group} group")
    except Exception as e:
        print(f"Error checking groups: {e}")
    
    # Check video device permissions
    for device in ['/dev/video0', '/dev/video1']:
        if os.path.exists(device):
            stat = os.stat(device)
            print(f"{device} permissions: {oct(stat.st_mode)[-3:]}")

def check_python_packages():
    """Check Python package installations"""
    print_header("PYTHON PACKAGES")
    
    packages_to_check = [
        'picamera2',
        'libcamera',
        'cv2',
        'numpy',
        'PIL',
        'face_recognition'
    ]
    
    for package in packages_to_check:
        try:
            if package == 'cv2':
                import cv2
                print(f"✅ OpenCV: {cv2.__version__}")
            elif package == 'PIL':
                from PIL import Image
                print(f"✅ PIL/Pillow: {Image.__version__}")
            else:
                spec = importlib.util.find_spec(package)
                if spec is not None:
                    module = importlib.import_module(package)
                    version = getattr(module, '__version__', 'unknown')
                    print(f"✅ {package}: {version}")
                else:
                    print(f"❌ {package}: Not found")
        except ImportError as e:
            print(f"❌ {package}: Import error - {e}")
        except Exception as e:
            print(f"⚠️ {package}: Error - {e}")

def check_picamera2_specific():
    """Check picamera2 specific issues"""
    print_header("PICAMERA2 SPECIFIC CHECKS")
    
    try:
        from picamera2 import Picamera2
        print("✅ picamera2 import successful")
        
        # Try to create Picamera2 object
        try:
            picam2 = Picamera2()
            print("✅ Picamera2 object created")
            
            # Check available cameras
            try:
                cameras = Picamera2.global_camera_info()
                print(f"✅ Available cameras: {len(cameras)}")
                for i, camera in enumerate(cameras):
                    print(f"   Camera {i}: {camera}")
            except Exception as e:
                print(f"❌ Error getting camera info: {e}")
            
            # Try to get sensor modes
            try:
                modes = picam2.sensor_modes
                print(f"✅ Sensor modes available: {len(modes)}")
            except Exception as e:
                print(f"❌ Error getting sensor modes: {e}")
            
            picam2.close()
            
        except Exception as e:
            print(f"❌ Error creating Picamera2 object: {e}")
            
    except ImportError as e:
        print(f"❌ picamera2 import failed: {e}")
        
        # Suggest installation methods
        print("\n💡 Installation suggestions:")
        print("1. System package: sudo apt install python3-picamera2")
        print("2. Pip install: pip3 install picamera2")
        print("3. With break-system-packages: pip3 install --break-system-packages picamera2")

def check_config_files():
    """Check important configuration files"""
    print_header("CONFIGURATION FILES")
    
    config_files = [
        '/boot/config.txt',
        '/boot/firmware/config.txt'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"\n📄 Checking {config_file}:")
            try:
                with open(config_file, 'r') as f:
                    lines = f.readlines()
                
                camera_related = []
                for line in lines:
                    line = line.strip()
                    if any(keyword in line.lower() for keyword in ['camera', 'gpu_mem', 'dtoverlay']):
                        camera_related.append(line)
                
                if camera_related:
                    for line in camera_related:
                        print(f"   {line}")
                else:
                    print("   No camera-related configuration found")
                    
            except Exception as e:
                print(f"   Error reading file: {e}")

def main():
    """Main diagnostic function"""
    print("🤖 Raspberry Pi 5 + Sony AITRIOS AI Camera Diagnostic Tool")
    print("This tool will help identify why picamera2 might not be working")
    
    check_system_info()
    check_camera_hardware()
    check_permissions()
    check_python_packages()
    check_picamera2_specific()
    check_config_files()
    
    print_header("SUMMARY & RECOMMENDATIONS")
    print("📋 Based on the diagnostic results above:")
    print("1. If no video devices found: Check camera cable connection")
    print("2. If permission errors: Add user to video group: sudo usermod -a -G video $USER")
    print("3. If picamera2 not found: Run the setup script: bash setup_raspberry_pi_camera.sh")
    print("4. If camera not detected: Enable camera in raspi-config: sudo raspi-config")
    print("5. After changes: Reboot the system: sudo reboot")
    
    print("\n🔧 Quick fixes to try:")
    print("sudo raspi-config nonint do_camera 0")
    print("sudo usermod -a -G video $USER")
    print("sudo apt update && sudo apt install python3-picamera2")
    print("sudo reboot")

if __name__ == "__main__":
    main() 