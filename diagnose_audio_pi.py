#!/usr/bin/env python3
"""
Raspberry Pi 5 Audio Diagnostic Tool
Comprehensive microphone testing and troubleshooting for AI Assistant
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AudioDiagnostics:
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"🔊 {text}")
        print('='*60)
        
    def print_status(self, text):
        print(f"📋 {text}")
        
    def print_error(self, text):
        print(f"❌ ERROR: {text}")
        self.issues_found.append(text)
        
    def print_success(self, text):
        print(f"✅ SUCCESS: {text}")
        
    def print_warning(self, text):
        print(f"⚠️  WARNING: {text}")
        
    def print_fix(self, text):
        print(f"🔧 FIX: {text}")
        self.fixes_applied.append(text)

    def run_command(self, command, description=""):
        """Run a system command and return output"""
        try:
            if description:
                self.print_status(f"{description}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.print_error(f"Command timed out: {command}")
            return False, "", "Command timed out"
        except Exception as e:
            self.print_error(f"Command failed: {command} - {e}")
            return False, "", str(e)

    def check_system_info(self):
        """Check basic system information"""
        self.print_header("SYSTEM INFORMATION")
        
        # Check if running on Raspberry Pi
        success, output, _ = self.run_command("cat /proc/device-tree/model 2>/dev/null || echo 'Not a Raspberry Pi'")
        if success and "Raspberry Pi" in output:
            self.print_success(f"Running on: {output.strip()}")
        else:
            self.print_warning("Not running on Raspberry Pi - some tests may not apply")
            
        # Check OS version
        success, output, _ = self.run_command("cat /etc/os-release | grep PRETTY_NAME")
        if success:
            self.print_status(f"OS: {output.strip()}")
            
        # Check kernel version
        success, output, _ = self.run_command("uname -r")
        if success:
            self.print_status(f"Kernel: {output.strip()}")

    def check_audio_devices(self):
        """Check available audio devices"""
        self.print_header("AUDIO DEVICES DETECTION")
        
        # Check ALSA devices
        success, output, stderr = self.run_command("aplay -l", "Checking ALSA playback devices")
        if success and output.strip():
            self.print_success("ALSA playback devices found:")
            print(output)
        else:
            self.print_error("No ALSA playback devices found")
            
        # Check ALSA recording devices
        success, output, stderr = self.run_command("arecord -l", "Checking ALSA recording devices")
        if success and output.strip():
            self.print_success("ALSA recording devices found:")
            print(output)
        else:
            self.print_error("No ALSA recording devices found - this is likely the main issue!")
            
        # Check PulseAudio
        success, output, stderr = self.run_command("pulseaudio --check", "Checking PulseAudio status")
        if success:
            self.print_success("PulseAudio is running")
        else:
            self.print_warning("PulseAudio not running")
            
        # List PulseAudio sources
        success, output, stderr = self.run_command("pactl list sources short", "Checking PulseAudio sources")
        if success and output.strip():
            self.print_success("PulseAudio sources found:")
            print(output)
        else:
            self.print_error("No PulseAudio sources found")

    def check_permissions(self):
        """Check audio permissions"""
        self.print_header("AUDIO PERMISSIONS")
        
        # Check user groups
        success, output, _ = self.run_command("groups", "Checking user groups")
        if success:
            groups = output.strip().split()
            audio_groups = ['audio', 'pulse', 'pulse-access']
            for group in audio_groups:
                if group in groups:
                    self.print_success(f"User is in '{group}' group")
                else:
                    self.print_error(f"User is NOT in '{group}' group")
                    
        # Check device permissions
        audio_devices = ['/dev/snd/', '/dev/dsp', '/dev/audio']
        for device in audio_devices:
            if os.path.exists(device):
                success, output, _ = self.run_command(f"ls -la {device}")
                if success:
                    self.print_status(f"Permissions for {device}:")
                    print(output)

    def check_python_audio_libraries(self):
        """Check Python audio library installations"""
        self.print_header("PYTHON AUDIO LIBRARIES")
        
        libraries = [
            ('pyaudio', 'PyAudio'),
            ('speech_recognition', 'SpeechRecognition'),
            ('pygame', 'Pygame'),
            ('sounddevice', 'SoundDevice'),
            ('numpy', 'NumPy')
        ]
        
        for module, name in libraries:
            try:
                __import__(module)
                self.print_success(f"{name} is installed")
            except ImportError:
                self.print_error(f"{name} is NOT installed")

    def test_pyaudio(self):
        """Test PyAudio functionality"""
        self.print_header("PYAUDIO FUNCTIONALITY TEST")
        
        try:
            import pyaudio
            
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            self.print_success("PyAudio initialized successfully")
            
            # List audio devices
            self.print_status("Available audio devices:")
            device_count = p.get_device_count()
            input_devices = []
            
            for i in range(device_count):
                info = p.get_device_info_by_index(i)
                device_type = "Input" if info['maxInputChannels'] > 0 else "Output"
                if info['maxInputChannels'] > 0:
                    input_devices.append((i, info))
                print(f"  {i}: {info['name']} ({device_type}) - {info['maxInputChannels']} input channels")
            
            if input_devices:
                self.print_success(f"Found {len(input_devices)} input device(s)")
                
                # Test default input device
                try:
                    default_input = p.get_default_input_device_info()
                    self.print_success(f"Default input device: {default_input['name']}")
                    
                    # Try to open an input stream
                    stream = p.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024
                    )
                    self.print_success("Successfully opened input stream")
                    stream.close()
                    
                except Exception as e:
                    self.print_error(f"Failed to open input stream: {e}")
                    
            else:
                self.print_error("No input devices found")
                
            p.terminate()
            
        except ImportError:
            self.print_error("PyAudio not installed")
        except Exception as e:
            self.print_error(f"PyAudio test failed: {e}")

    def test_speech_recognition(self):
        """Test speech recognition functionality"""
        self.print_header("SPEECH RECOGNITION TEST")
        
        try:
            import speech_recognition as sr
            
            # Initialize recognizer
            r = sr.Recognizer()
            self.print_success("Speech recognizer initialized")
            
            # List microphones
            mics = sr.Microphone.list_microphone_names()
            if mics:
                self.print_success(f"Found {len(mics)} microphone(s):")
                for i, mic in enumerate(mics):
                    print(f"  {i}: {mic}")
                    
                # Test microphone access
                try:
                    with sr.Microphone() as source:
                        self.print_success("Successfully accessed microphone")
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        self.print_success("Ambient noise calibration completed")
                        
                        # Quick recording test
                        print("🎤 Testing microphone recording (speak now)...")
                        try:
                            audio = r.listen(source, timeout=3, phrase_time_limit=2)
                            self.print_success("Successfully recorded audio")
                            
                            # Try to recognize (optional - may fail without internet)
                            try:
                                text = r.recognize_google(audio)
                                self.print_success(f"Recognition successful: '{text}'")
                            except:
                                self.print_warning("Audio recognition failed (likely no internet), but recording worked")
                                
                        except sr.WaitTimeoutError:
                            self.print_warning("No speech detected during test")
                        except Exception as e:
                            self.print_error(f"Recording test failed: {e}")
                            
                except Exception as e:
                    self.print_error(f"Microphone access failed: {e}")
                    
            else:
                self.print_error("No microphones detected")
                
        except ImportError:
            self.print_error("SpeechRecognition not installed")
        except Exception as e:
            self.print_error(f"Speech recognition test failed: {e}")

    def check_raspberry_pi_config(self):
        """Check Raspberry Pi specific audio configuration"""
        self.print_header("RASPBERRY PI AUDIO CONFIGURATION")
        
        config_files = ['/boot/config.txt', '/boot/firmware/config.txt']
        config_found = False
        
        for config_file in config_files:
            if os.path.exists(config_file):
                config_found = True
                self.print_status(f"Checking {config_file}")
                
                success, output, _ = self.run_command(f"grep -E 'dtparam=audio|audio_pwm_mode' {config_file}")
                if success and output.strip():
                    self.print_success("Audio configuration found:")
                    print(output)
                else:
                    self.print_error("Audio not enabled in config.txt")
                break
                
        if not config_found:
            self.print_error("Could not find config.txt file")

    def provide_fixes(self):
        """Provide specific fixes for common issues"""
        self.print_header("RECOMMENDED FIXES")
        
        if not self.issues_found:
            self.print_success("No major issues detected!")
            return
            
        print("Based on the diagnostic results, here are recommended fixes:\n")
        
        # Check for common issues and provide fixes
        issue_keywords = [
            "No ALSA recording devices",
            "No input devices found",
            "User is NOT in 'audio' group",
            "Audio not enabled in config.txt",
            "PyAudio not installed",
            "SpeechRecognition not installed"
        ]
        
        for issue in self.issues_found:
            if "No ALSA recording devices" in issue:
                print("🔧 FIX 1: Enable audio and install USB microphone support")
                print("   sudo apt update && sudo apt install -y alsa-utils pulseaudio")
                print("   sudo usermod -a -G audio $USER")
                print("   # Reboot required after adding user to audio group")
                print()
                
            if "User is NOT in 'audio' group" in issue:
                print("🔧 FIX 2: Add user to audio group")
                print("   sudo usermod -a -G audio,pulse,pulse-access $USER")
                print("   # Logout and login again (or reboot)")
                print()
                
            if "Audio not enabled in config.txt" in issue:
                print("🔧 FIX 3: Enable audio in Raspberry Pi config")
                print("   echo 'dtparam=audio=on' | sudo tee -a /boot/config.txt")
                print("   echo 'audio_pwm_mode=2' | sudo tee -a /boot/config.txt")
                print("   # Reboot required")
                print()
                
            if "PyAudio not installed" in issue:
                print("🔧 FIX 4: Install PyAudio")
                print("   sudo apt install -y python3-pyaudio portaudio19-dev")
                print("   pip install pyaudio")
                print()
                
            if "No microphones detected" in issue:
                print("🔧 FIX 5: Connect and configure microphone")
                print("   # For USB microphone:")
                print("   lsusb  # Check if USB mic is detected")
                print("   arecord -l  # List recording devices")
                print("   alsamixer  # Adjust microphone levels")
                print()
                print("   # For 3.5mm microphone on Pi 5:")
                print("   # Note: Pi 5 may not have 3.5mm microphone input")
                print("   # Use USB microphone or USB sound card")
                print()

    def run_complete_diagnosis(self):
        """Run complete audio diagnosis"""
        print("🔊 RASPBERRY PI 5 AUDIO DIAGNOSTIC TOOL")
        print("This tool will help diagnose microphone issues with your AI Assistant")
        print()
        
        try:
            self.check_system_info()
            self.check_audio_devices()
            self.check_permissions()
            self.check_python_audio_libraries()
            self.test_pyaudio()
            self.test_speech_recognition()
            self.check_raspberry_pi_config()
            
            # Summary
            self.print_header("DIAGNOSTIC SUMMARY")
            
            if self.issues_found:
                self.print_error(f"Found {len(self.issues_found)} issue(s):")
                for i, issue in enumerate(self.issues_found, 1):
                    print(f"  {i}. {issue}")
            else:
                self.print_success("No major issues detected!")
                
            self.provide_fixes()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Diagnostic interrupted by user")
        except Exception as e:
            self.print_error(f"Diagnostic failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Starting Raspberry Pi 5 Audio Diagnostics...")
    diagnostics = AudioDiagnostics()
    diagnostics.run_complete_diagnosis() 