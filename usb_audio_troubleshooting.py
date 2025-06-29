#!/usr/bin/env python3
"""
USB Audio Troubleshooting Tool for Raspberry Pi 5
Helps diagnose and fix USB microphone and speaker issues
"""

import sys
import os
import subprocess
import time
import logging
from typing import Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class USBAudioTroubleshooter:
    """USB audio troubleshooting tool for Raspberry Pi 5."""
    
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        self.usb_devices = {}
        
    def print_header(self, text: str):
        print(f"\n{'='*70}")
        print(f"🔌 {text}")
        print('='*70)
        
    def print_status(self, text: str):
        print(f"📋 {text}")
        
    def print_error(self, text: str):
        print(f"❌ ERROR: {text}")
        self.issues_found.append(text)
        
    def print_success(self, text: str):
        print(f"✅ SUCCESS: {text}")
        
    def print_warning(self, text: str):
        print(f"⚠️  WARNING: {text}")
        
    def print_fix(self, text: str):
        print(f"🔧 FIX: {text}")
        self.fixes_applied.append(text)

    def run_command(self, command: str, description: str = "") -> Tuple[bool, str, str]:
        """Run a system command and return results."""
        try:
            if description:
                self.print_status(description)
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.print_error(f"Command timed out: {command}")
            return False, "", "Command timed out"
        except Exception as e:
            self.print_error(f"Command failed: {command} - {e}")
            return False, "", str(e)

    def detect_raspberry_pi_model(self) -> Dict[str, str]:
        """Detect Raspberry Pi model and USB configuration."""
        self.print_header("RASPBERRY PI MODEL DETECTION")
        
        pi_info = {"model": "Unknown", "usb_config": "Unknown"}
        
        if os.path.exists('/proc/device-tree/model'):
            try:
                with open('/proc/device-tree/model', 'r') as f:
                    model_info = f.read().strip()
                    pi_info["model"] = model_info
                    self.print_success(f"Detected: {model_info}")
                    
                    if 'pi 5' in model_info.lower():
                        pi_info["usb_config"] = "Pi 5 - 2x USB 3.0 + 2x USB 2.0"
                        self.print_status("USB Configuration: 2x USB 3.0 ports + 2x USB 2.0 ports")
                        self.print_status("USB 3.0 ports are blue, USB 2.0 ports are black")
                    elif 'pi 4' in model_info.lower():
                        pi_info["usb_config"] = "Pi 4 - 2x USB 3.0 + 2x USB 2.0"
                    else:
                        pi_info["usb_config"] = "Older Pi - USB 2.0 only"
                        
            except Exception as e:
                self.print_error(f"Could not read Pi model: {e}")
        else:
            self.print_warning("Not running on Raspberry Pi")
            
        return pi_info

    def scan_usb_devices(self) -> Dict[str, List[Dict]]:
        """Scan for USB devices and categorize them."""
        self.print_header("USB DEVICE SCAN")
        
        # Get USB device list
        success, output, _ = self.run_command("lsusb", "Scanning USB devices")
        
        usb_devices = {
            "audio": [],
            "other": [],
            "hubs": []
        }
        
        if success and output:
            lines = output.strip().split('\n')
            for line in lines:
                if line.strip():
                    # Parse lsusb output: Bus 001 Device 002: ID 1234:5678 Device Name
                    parts = line.split()
                    if len(parts) >= 6:
                        bus = parts[1]
                        device = parts[3].rstrip(':')
                        device_id = parts[5]
                        device_name = ' '.join(parts[6:])
                        
                        device_info = {
                            "bus": bus,
                            "device": device,
                            "id": device_id,
                            "name": device_name,
                            "line": line
                        }
                        
                        # Categorize devices
                        if any(keyword in device_name.lower() for keyword in 
                               ['audio', 'microphone', 'mic', 'speaker', 'sound', 'usb audio']):
                            usb_devices["audio"].append(device_info)
                        elif 'hub' in device_name.lower():
                            usb_devices["hubs"].append(device_info)
                        else:
                            usb_devices["other"].append(device_info)
            
            # Display results
            if usb_devices["audio"]:
                self.print_success(f"Found {len(usb_devices['audio'])} USB audio device(s):")
                for device in usb_devices["audio"]:
                    print(f"  📱 {device['name']} (Bus {device['bus']}, Device {device['device']})")
            else:
                self.print_error("No USB audio devices detected!")
                self.print_warning("Make sure your USB microphone/speaker is connected")
                
            if usb_devices["other"]:
                self.print_status(f"Other USB devices ({len(usb_devices['other'])}):")
                for device in usb_devices["other"]:
                    print(f"  🔌 {device['name']}")
                    
        else:
            self.print_error("Failed to scan USB devices")
            
        self.usb_devices = usb_devices
        return usb_devices

    def check_usb_audio_detection(self):
        """Check if USB audio devices are properly detected by the audio system."""
        self.print_header("USB AUDIO SYSTEM DETECTION")
        
        # Check ALSA detection
        success, output, _ = self.run_command("arecord -l", "Checking ALSA recording devices")
        if success and output.strip():
            self.print_success("ALSA detected recording devices:")
            print(output)
            
            # Parse ALSA output to map to USB devices
            if "USB Audio" in output or "card" in output:
                self.print_success("USB audio devices are recognized by ALSA")
            else:
                self.print_warning("ALSA may not be detecting USB audio properly")
        else:
            self.print_error("No ALSA recording devices found")
            
        # Check PulseAudio detection
        success, output, _ = self.run_command("pactl list sources short", "Checking PulseAudio sources")
        if success and output.strip():
            self.print_success("PulseAudio sources found:")
            print(output)
        else:
            self.print_warning("No PulseAudio sources detected")

    def test_usb_port_recommendations(self):
        """Provide USB port recommendations for Pi 5."""
        self.print_header("USB PORT RECOMMENDATIONS FOR RASPBERRY PI 5")
        
        print("🔌 OPTIMAL USB PORT CONFIGURATION:")
        print()
        print("   Pi 5 USB Layout (looking at the Pi from the side with USB ports):")
        print("   ┌─────────────────────────────────────┐")
        print("   │  [USB3] [USB3] [USB2] [USB2]       │")
        print("   │   Blue   Blue   Black  Black       │")
        print("   └─────────────────────────────────────┘")
        print()
        
        self.print_success("RECOMMENDED SETUP:")
        print("  🎤 USB Microphone    → USB 2.0 port (black) - More stable for audio")
        print("  🔊 USB Speaker       → USB 2.0 port (black) - Consistent power")
        print("  📱 Other devices     → USB 3.0 ports (blue) - High bandwidth devices")
        print()
        
        self.print_warning("AVOID THESE CONFIGURATIONS:")
        print("  ❌ Microphone + Speaker on same USB 3.0 ports")
        print("  ❌ All audio devices on USB 3.0 (can cause interference)")
        print("  ❌ Using USB hubs for critical audio devices")
        print("  ❌ Connecting audio devices to the same physical USB controller")
        print()
        
        self.print_fix("TRY THESE STEPS:")
        print("  1. Move microphone to a USB 2.0 port (black)")
        print("  2. Move speaker to the other USB 2.0 port (black)")
        print("  3. Disconnect other USB devices temporarily to test")
        print("  4. Reboot after moving devices")
        print("  5. Test each USB port individually")

    def test_individual_usb_ports(self):
        """Guide user through testing individual USB ports."""
        self.print_header("USB PORT TESTING GUIDE")
        
        print("📋 MANUAL USB PORT TESTING PROCEDURE:")
        print()
        print("Follow these steps to find the best USB port for your microphone:")
        print()
        
        for port_num in range(1, 5):
            port_type = "USB 3.0 (blue)" if port_num <= 2 else "USB 2.0 (black)"
            print(f"🔌 STEP {port_num}: Test USB Port {port_num} ({port_type})")
            print(f"  1. Connect ONLY your microphone to USB port {port_num}")
            print(f"  2. Disconnect all other USB devices")
            print(f"  3. Run: lsusb | grep -i audio")
            print(f"  4. Run: arecord -l")
            print(f"  5. Test: arecord -f cd -d 3 test_port{port_num}.wav")
            print(f"  6. Listen: aplay test_port{port_num}.wav")
            print()
            
        self.print_success("RECOMMENDED TESTING ORDER:")
        print("  1st: USB 2.0 Port 1 (rightmost black port)")
        print("  2nd: USB 2.0 Port 2 (leftmost black port)")  
        print("  3rd: USB 3.0 Port 1 (rightmost blue port)")
        print("  4th: USB 3.0 Port 2 (leftmost blue port)")

    def check_usb_power_issues(self):
        """Check for USB power-related issues."""
        self.print_header("USB POWER DIAGNOSTICS")
        
        # Check USB power configuration
        success, output, _ = self.run_command("cat /sys/kernel/debug/usb/devices 2>/dev/null || echo 'Debug info not available'")
        
        # Check dmesg for USB issues
        success, output, _ = self.run_command("dmesg | grep -i usb | tail -20", "Checking recent USB messages")
        if success and output:
            self.print_status("Recent USB system messages:")
            print(output)
            
            # Look for common USB issues
            if "over-current" in output.lower():
                self.print_error("USB over-current detected - power supply issue!")
            if "device not accepting address" in output.lower():
                self.print_warning("USB device enumeration issues detected")
            if "reset" in output.lower():
                self.print_warning("USB device resets detected")
                
        # Check power supply recommendations
        self.print_status("Power Supply Recommendations:")
        print("  • Use official Raspberry Pi 5 power supply (5V/5A)")
        print("  • Avoid using computer USB ports to power the Pi")
        print("  • Use powered USB hub if connecting many devices")
        print("  • Check power supply cable quality")

    def run_automated_fix_sequence(self):
        """Run automated fixes for common USB audio issues."""
        self.print_header("AUTOMATED USB AUDIO FIXES")
        
        fixes = [
            ("Restarting PulseAudio", "pulseaudio --kill && sleep 2 && pulseaudio --start"),
            ("Reloading ALSA", "sudo alsactl restore"),
            ("Refreshing USB subsystem", "sudo udevadm control --reload-rules && sudo udevadm trigger"),
            ("Checking audio groups", "groups | grep audio"),
        ]
        
        for description, command in fixes:
            self.print_status(f"Applying fix: {description}")
            success, output, error = self.run_command(command)
            if success:
                self.print_success(f"✅ {description} - Success")
                if output.strip():
                    print(f"   Output: {output.strip()}")
            else:
                self.print_warning(f"⚠️  {description} - Failed: {error}")
                
        self.print_fix("Applied automated fixes. Test your microphone now!")

    def provide_troubleshooting_summary(self):
        """Provide a summary of issues and recommended actions."""
        self.print_header("TROUBLESHOOTING SUMMARY")
        
        if self.usb_devices["audio"]:
            self.print_success("✅ USB audio devices detected")
        else:
            self.print_error("❌ No USB audio devices found")
            print("  🔧 Try different USB ports")
            print("  🔧 Check device connections")
            print("  🔧 Test with different USB cables")
            
        print()
        self.print_status("RECOMMENDED NEXT STEPS:")
        print("1. 🔌 Move microphone to USB 2.0 port (black)")
        print("2. 🔄 Reboot your Raspberry Pi")
        print("3. 🧪 Run: python3 diagnose_audio_pi.py")
        print("4. 🎤 Test: python3 main.py")
        print("5. 🆘 If still not working, try different USB ports systematically")
        
    def run_complete_usb_diagnosis(self):
        """Run the complete USB audio diagnosis."""
        print("🔌 USB AUDIO TROUBLESHOOTING TOOL FOR RASPBERRY PI 5")
        print("This tool helps diagnose and fix USB microphone/speaker issues")
        print()
        
        try:
            # Run all diagnostic steps
            pi_info = self.detect_raspberry_pi_model()
            usb_devices = self.scan_usb_devices()
            self.check_usb_audio_detection()
            self.test_usb_port_recommendations()
            self.check_usb_power_issues()
            
            # Ask if user wants to run automated fixes
            print("\n" + "="*50)
            response = input("🔧 Run automated fixes? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                self.run_automated_fix_sequence()
                
            # Ask if user wants USB port testing guide
            print("\n" + "="*50)
            response = input("📋 Show detailed USB port testing guide? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                self.test_individual_usb_ports()
                
            self.provide_troubleshooting_summary()
            
        except KeyboardInterrupt:
            print("\n\n🛑 USB diagnosis interrupted by user")
        except Exception as e:
            self.print_error(f"USB diagnosis failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Starting USB Audio Troubleshooting...")
    troubleshooter = USBAudioTroubleshooter()
    troubleshooter.run_complete_usb_diagnosis() 