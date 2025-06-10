#!/usr/bin/env python3
"""
Visual Feedback Setup Script for AI Assistant
Automatically installs and configures visual feedback system
"""

import os
import sys
import shutil
import subprocess
import platform


def detect_environment():
    """Detect the current environment and hardware."""
    
    env_info = {
        'platform': platform.system(),
        'machine': platform.machine(),
        'raspberry_pi': False,
        'display_available': False,
        'gui_available': False
    }
    
    # Check if running on Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo:
                env_info['raspberry_pi'] = True
    except FileNotFoundError:
        pass
    
    # Check for display
    if 'DISPLAY' in os.environ or env_info['platform'] == 'Darwin':
        env_info['display_available'] = True
    
    # Check for GUI capabilities
    try:
        import tkinter
        env_info['gui_available'] = True
    except ImportError:
        pass
    
    return env_info


def install_dependencies():
    """Install required Python packages."""
    
    print("📦 Installing required packages...")
    
    required_packages = [
        'tkinter',  # For GUI
        'pillow',   # For image processing
    ]
    
    # Try to import packages, install if missing
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'pillow':
                from PIL import Image
                
            print(f"✅ {package} already installed")
            
        except ImportError:
            print(f"⚠️  {package} not found, attempting to install...")
            
            if package == 'tkinter':
                # On Ubuntu/Debian systems
                try:
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'python3-tk'], 
                                 check=True, capture_output=True)
                    print(f"✅ {package} installed via apt-get")
                except:
                    print(f"❌ Failed to install {package}. Please install manually:")
                    print(f"   sudo apt-get install python3-tk")
            else:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                 check=True, capture_output=True)
                    print(f"✅ {package} installed via pip")
                except:
                    print(f"❌ Failed to install {package}. Please install manually:")
                    print(f"   pip install {package}")


def setup_environment_variables(env_info):
    """Set up environment variables based on detected hardware."""
    
    print("🔧 Setting up environment variables...")
    
    # Default configuration
    if env_info['raspberry_pi']:
        if env_info['gui_available']:
            config = {
                'ROBOT_TYPE': 'pi_7inch',
                'ROBOT_DISPLAY_WIDTH': '800',
                'ROBOT_DISPLAY_HEIGHT': '480',
                'ROBOT_FULLSCREEN': 'true',
                'ROBOT_USE_GUI': 'true',
                'ROBOT_ANIMATIONS': 'true',
                'ROBOT_FACE_SIZE': '150'
            }
        else:
            config = {
                'ROBOT_TYPE': 'minimal',
                'ROBOT_USE_GUI': 'false',
                'ROBOT_ANIMATIONS': 'false'
            }
    else:
        # Desktop development
        config = {
            'ROBOT_TYPE': 'desktop',
            'ROBOT_DISPLAY_WIDTH': '1024',
            'ROBOT_DISPLAY_HEIGHT': '768',
            'ROBOT_FULLSCREEN': 'false',
            'ROBOT_USE_GUI': 'true',
            'ROBOT_ANIMATIONS': 'true',
            'ROBOT_FACE_SIZE': '200'
        }
    
    # Write environment variables to a script
    env_script = """#!/bin/bash
# AI Assistant Visual Feedback Environment Variables
# Source this file or add to your .bashrc

"""
    
    for key, value in config.items():
        env_script += f"export {key}={value}\n"
        # Also set for current session
        os.environ[key] = value
    
    # Save environment script
    with open('robot_env.sh', 'w') as f:
        f.write(env_script)
    
    # Make it executable
    os.chmod('robot_env.sh', 0o755)
    
    print("✅ Environment variables configured:")
    for key, value in config.items():
        print(f"   {key}={value}")
    
    print(f"\n💡 To make these permanent, add to your .bashrc:")
    print(f"   echo 'source {os.path.abspath('robot_env.sh')}' >> ~/.bashrc")


def create_startup_script():
    """Create a startup script for the AI Assistant with visual feedback."""
    
    startup_script = """#!/bin/bash
# AI Assistant Startup Script with Visual Feedback

# Source environment variables
source "$(dirname "$0")/robot_env.sh"

# Change to AI assistant directory
cd "$(dirname "$0")"

# Start the AI Assistant
echo "🤖 Starting AI Assistant with Visual Feedback..."
python3 main.py

# If that fails, try the integration example
if [ $? -ne 0 ]; then
    echo "⚠️  Main assistant failed, running integration example..."
    cd tests
    python3 integration_example.py
fi
"""

    with open('start_robot.sh', 'w') as f:
        f.write(startup_script)
    
    os.chmod('start_robot.sh', 0o755)
    
    print("✅ Startup script created: start_robot.sh")


def setup_systemd_service():
    """Set up systemd service for auto-start on Raspberry Pi."""
    
    service_content = f"""[Unit]
Description=AI Assistant with Visual Feedback
After=graphical-session.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
WorkingDirectory={os.getcwd()}
ExecStart={os.getcwd()}/start_robot.sh
Restart=always
RestartSec=10

[Install]
WantedBy=graphical-session.target
"""

    service_file = 'ai-assistant.service'
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"✅ Systemd service file created: {service_file}")
    print("📝 To enable auto-start on boot:")
    print(f"   sudo cp {service_file} /etc/systemd/system/")
    print("   sudo systemctl enable ai-assistant.service")
    print("   sudo systemctl start ai-assistant.service")


def test_visual_system():
    """Test the visual feedback system."""
    
    print("🧪 Testing visual feedback system...")
    
    try:
        # Test import
        from visual_feedback import create_visual_feedback
        from visual_config import get_config_for_environment
        
        print("✅ Visual feedback modules imported successfully")
        
        # Test configuration
        config = get_config_for_environment()
        display_config = config.get_display_config()
        
        print(f"✅ Configuration loaded:")
        print(f"   Display: {display_config['width']}x{display_config['height']}")
        print(f"   GUI Mode: {display_config['use_gui']}")
        
        # Test visual system creation
        visual = create_visual_feedback(use_gui=False)  # Test non-GUI first
        print("✅ Visual feedback system created successfully")
        
        # Test basic functionality
        visual.show_standby("Test message")
        print("✅ Basic visual feedback test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Visual system test failed: {e}")
        return False


def show_completion_message(env_info):
    """Show setup completion message with next steps."""
    
    message = f"""
🎉 VISUAL FEEDBACK SETUP COMPLETE! 🎉
{'=' * 50}

🔍 Environment Detected:
   Platform: {env_info['platform']}
   Raspberry Pi: {'Yes' if env_info['raspberry_pi'] else 'No'}
   Display Available: {'Yes' if env_info['display_available'] else 'No'}
   GUI Available: {'Yes' if env_info['gui_available'] else 'No'}

📁 Files Created:
   ✅ visual_feedback.py      - Main visual feedback system
   ✅ visual_config.py        - Configuration management
   ✅ robot_env.sh           - Environment variables
   ✅ start_robot.sh         - Startup script
   ✅ tests/                 - Test files and examples
   ✅ ai-assistant.service   - Systemd service file

🚀 Quick Start:
   1. Test the system:
      ./start_robot.sh
   
   2. Run specific tests:
      cd tests && python3 test_visual_feedback.py
   
   3. See integration example:
      cd tests && python3 integration_example.py

🔧 Raspberry Pi Setup:
   1. Enable environment variables:
      echo 'source {os.path.abspath("robot_env.sh")}' >> ~/.bashrc
   
   2. Enable auto-start (optional):
      sudo cp ai-assistant.service /etc/systemd/system/
      sudo systemctl enable ai-assistant.service
   
   3. For touchscreen setup:
      # Add to /boot/config.txt:
      hdmi_force_hotplug=1
      hdmi_cvt=800 480 60 6 0 0 0
      
⚙️  Integration with main.py:
   See tests/integration_example.py for complete example
   
   Key changes needed:
   1. Add imports:
      from visual_feedback import create_visual_feedback
      from visual_config import get_config_for_environment
   
   2. Initialize in __init__():
      self.config = get_config_for_environment()
      self.visual = create_visual_feedback(use_gui=config.get_display_config()['use_gui'])
   
   3. Add state changes throughout code:
      self.visual.show_listening("Listening...")
      self.visual.show_thinking("Processing...")
      self.visual.show_speaking("Responding...")
      self.visual.show_happy("Success!")
      self.visual.show_error("Error occurred")
      self.visual.show_standby("Ready to help!")

🎨 Customization:
   Edit visual_config.py or use environment variables:
   export ROBOT_FACE_SIZE=200
   export ROBOT_STANDBY_COLOR="#4CAF50"
   export ROBOT_LISTENING_COLOR="#2196F3"

📱 Hardware Recommendations:
   - Official Raspberry Pi 7" Touchscreen
   - HDMI displays (800x480 minimum)
   - At least 2GB RAM for smooth animations
   - Hardware GPU acceleration for best performance

🎯 Your robot now has cute visual feedback! 🤖✨

Need help? Check the tests directory for examples and documentation.
"""
    
    print(message)


def main():
    """Main setup function."""
    
    print("🤖 AI Assistant Visual Feedback Setup")
    print("=" * 40)
    
    # Detect environment
    env_info = detect_environment()
    
    print(f"\n🔍 Environment Detection:")
    print(f"   Platform: {env_info['platform']}")
    print(f"   Raspberry Pi: {'Yes' if env_info['raspberry_pi'] else 'No'}")
    print(f"   Display: {'Yes' if env_info['display_available'] else 'No'}")
    print(f"   GUI: {'Yes' if env_info['gui_available'] else 'No'}")
    
    # Ask for confirmation
    print(f"\n📋 Setup will configure visual feedback for your environment.")
    choice = input("Continue? (y/N): ").strip().lower()
    
    if choice != 'y':
        print("Setup cancelled.")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment_variables(env_info)
    
    # Create startup script
    create_startup_script()
    
    # Create systemd service for Raspberry Pi
    if env_info['raspberry_pi']:
        setup_systemd_service()
    
    # Test the system
    if test_visual_system():
        print("✅ Visual feedback system test passed!")
    else:
        print("⚠️  Visual feedback system test failed. Check dependencies.")
    
    # Show completion message
    show_completion_message(env_info)


if __name__ == "__main__":
    main() 