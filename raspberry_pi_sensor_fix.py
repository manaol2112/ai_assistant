#!/usr/bin/env python3
"""
🔧 RASPBERRY PI SENSOR INTERFERENCE FIX
Diagnose and fix ultrasonic/IR sensor interference with forward movement
while keeping sensors fully functional.

This tool works on Raspberry Pi with Arduino connected.
"""

import time
import serial
import subprocess
import sys
from motor_control import MotorController

class RaspberryPiSensorFix:
    def __init__(self):
        self.motor = None
        self.arduino_port = None
        self.sensor_readings = []
        
    def detect_arduino_connection(self):
        """Detect Arduino connection on Raspberry Pi"""
        print("🔍 DETECTING ARDUINO CONNECTION")
        print("=" * 35)
        
        # Common Arduino ports on Raspberry Pi
        possible_ports = [
            '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2',
            '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2',
            '/dev/serial0', '/dev/serial1'
        ]
        
        for port in possible_ports:
            try:
                # Try to open the port
                test_serial = serial.Serial(port, 9600, timeout=2)
                test_serial.write(b'READ_ULTRASONIC\n')
                time.sleep(0.5)
                
                if test_serial.in_waiting > 0:
                    response = test_serial.readline().decode().strip()
                    test_serial.close()
                    
                    print(f"✅ Arduino found on {port}")
                    print(f"   Response: {response}")
                    self.arduino_port = port
                    return True
                    
                test_serial.close()
                
            except Exception as e:
                continue
        
        print("❌ No Arduino detected on common ports")
        return False
    
    def test_sensor_readings(self):
        """Test all sensor readings to identify interference"""
        print("\n🔍 TESTING SENSOR READINGS")
        print("=" * 30)
        
        if not self.arduino_port:
            print("❌ Arduino not connected")
            return False
        
        try:
            arduino = serial.Serial(self.arduino_port, 9600, timeout=2)
            time.sleep(2)  # Wait for Arduino to initialize
            
            print("📊 Taking 15 sensor readings...")
            
            ultrasonic_readings = []
            ir_left_readings = []
            ir_right_readings = []
            
            for i in range(15):
                print(f"Reading {i+1}/15...")
                
                # Test ultrasonic
                arduino.write(b'READ_ULTRASONIC\n')
                time.sleep(0.3)
                if arduino.in_waiting > 0:
                    response = arduino.readline().decode().strip()
                    if "ULTRASONIC_DISTANCE:" in response:
                        distance = response.split(":")[1].strip()
                        try:
                            dist_val = int(distance)
                            ultrasonic_readings.append(dist_val)
                            print(f"  Ultrasonic: {dist_val}cm", end="")
                            
                            if dist_val < 2:
                                print(" ⚠️ FALSE READING")
                            elif dist_val < 15:
                                print(" 🚫 BLOCKING MOVEMENT")
                            else:
                                print(" ✅ CLEAR")
                        except:
                            ultrasonic_readings.append(-999)
                            print(f"  Ultrasonic: ERROR ({distance})")
                
                # Test IR sensors
                arduino.write(b'READ_IR_BOTH\n')
                time.sleep(0.3)
                if arduino.in_waiting > 0:
                    response = arduino.readline().decode().strip()
                    if "IR_BOTH:" in response:
                        ir_values = response.split(":")[1].strip()
                        try:
                            left, right = ir_values.split(",")
                            ir_left_readings.append(int(left))
                            ir_right_readings.append(int(right))
                            print(f"  IR Left: {left}, Right: {right}")
                        except:
                            print(f"  IR: ERROR ({ir_values})")
                
                time.sleep(0.5)
            
            arduino.close()
            
            # Analyze readings
            self.analyze_sensor_readings(ultrasonic_readings, ir_left_readings, ir_right_readings)
            return True
            
        except Exception as e:
            print(f"❌ Sensor test failed: {e}")
            return False
    
    def analyze_sensor_readings(self, ultrasonic, ir_left, ir_right):
        """Analyze sensor readings to identify issues"""
        print("\n📊 SENSOR ANALYSIS RESULTS")
        print("=" * 28)
        
        # Ultrasonic analysis
        false_readings = [r for r in ultrasonic if 0 <= r < 2]
        blocking_readings = [r for r in ultrasonic if 2 <= r < 15]
        clear_readings = [r for r in ultrasonic if r >= 15]
        error_readings = [r for r in ultrasonic if r < 0]
        
        print(f"🔊 ULTRASONIC SENSOR:")
        print(f"   False readings (0-2cm): {len(false_readings)} times")
        print(f"   Blocking readings (2-15cm): {len(blocking_readings)} times")
        print(f"   Clear readings (15+cm): {len(clear_readings)} times")
        print(f"   Error readings: {len(error_readings)} times")
        
        if len(false_readings) > 5:
            print("   ⚠️ HIGH FALSE READING COUNT - Sensor interference detected!")
        
        if len(blocking_readings) > 10:
            print("   🚫 FREQUENT BLOCKING - May prevent forward movement")
        
        # IR analysis
        ir_left_blocking = ir_left.count(0)
        ir_right_blocking = ir_right.count(0)
        
        print(f"\n👁️ IR SENSORS:")
        print(f"   Left sensor blocking: {ir_left_blocking}/15 times")
        print(f"   Right sensor blocking: {ir_right_blocking}/15 times")
        
        if ir_left_blocking > 10 or ir_right_blocking > 10:
            print("   ⚠️ IR SENSORS FREQUENTLY BLOCKING MOVEMENT")
    
    def test_movement_with_safety_off(self):
        """Test forward movement with safety temporarily disabled"""
        print("\n🚀 TESTING FORWARD MOVEMENT")
        print("=" * 28)
        print("This will temporarily disable safety to test if sensors are the issue")
        print("⚠️ WARNING: Make sure the robot has clear space!")
        
        input("Press Enter when robot is in clear space...")
        
        try:
            arduino = serial.Serial(self.arduino_port, 9600, timeout=2)
            time.sleep(2)
            
            print("🔧 Disabling safety...")
            arduino.write(b'SAFETY_OFF\n')
            time.sleep(0.5)
            
            print("🚀 Testing forward movement...")
            arduino.write(b'MOVE_FORWARD\n')
            time.sleep(3)  # Move for 3 seconds
            
            print("🛑 Stopping movement...")
            arduino.write(b'STOP_ALL\n')
            time.sleep(0.5)
            
            print("🔧 Re-enabling safety...")
            arduino.write(b'SAFETY_ON\n')
            
            arduino.close()
            
            result = input("Did the robot move forward? (y/n): ").lower().strip()
            
            if result == 'y':
                print("✅ CONFIRMED: Sensors were blocking movement")
                return True
            else:
                print("❌ Issue is NOT sensors - deeper motor problem")
                return False
                
        except Exception as e:
            print(f"❌ Movement test failed: {e}")
            return False
    
    def apply_smart_sensor_fix(self):
        """Apply intelligent sensor filtering to prevent false blocking"""
        print("\n🧠 APPLYING SMART SENSOR FIX")
        print("=" * 30)
        
        print("Creating improved Arduino code with smart sensor filtering...")
        
        # Create improved Arduino code snippet
        improved_safety_code = '''
// IMPROVED SAFETY FUNCTION - Smart sensor filtering
bool is_safe_to_move_forward() {
  if (!safety_enabled) return true;
  
  // Take multiple readings to filter out noise
  int distances[3];
  int valid_readings = 0;
  
  for (int i = 0; i < 3; i++) {
    distances[i] = read_ultrasonic_distance();
    if (distances[i] > 0 && distances[i] < 400) {  // Valid range
      valid_readings++;
    }
    delay(10);  // Small delay between readings
  }
  
  // Only block if we have consistent readings
  if (valid_readings >= 2) {
    int avg_distance = 0;
    for (int i = 0; i < 3; i++) {
      if (distances[i] > 0 && distances[i] < 400) {
        avg_distance += distances[i];
      }
    }
    avg_distance /= valid_readings;
    
    // Block only if average distance is consistently low
    if (avg_distance > 3 && avg_distance < SAFE_DISTANCE) {
      Serial.print("SAFETY: Confirmed obstacle at ");
      Serial.print(avg_distance);
      Serial.println("cm (averaged)");
      return false;
    }
  }
  
  // Check IR sensors with filtering
  int ir_left_count = 0;
  int ir_right_count = 0;
  
  // Take 3 quick IR readings
  for (int i = 0; i < 3; i++) {
    if (digitalRead(irLeftPin) == 0) ir_left_count++;
    if (digitalRead(irRightPin) == 0) ir_right_count++;
    delay(5);
  }
  
  // Block only if IR consistently detects obstacle
  if (ir_left_count >= 2 || ir_right_count >= 2) {
    Serial.println("SAFETY: IR sensor consistently detected obstacle");
    return false;
  }
  
  return true;  // Safe to move
}
'''
        
        # Save the improved code to a file
        with open('/home/pi/improved_safety_function.txt', 'w') as f:
            f.write(improved_safety_code)
        
        print("✅ Improved safety function saved to /home/pi/improved_safety_function.txt")
        print("\n📝 MANUAL FIX INSTRUCTIONS:")
        print("1. Open Arduino IDE on your Raspberry Pi")
        print("2. Open arduino_code_anti_jerk_integrated.ino") 
        print("3. Replace the is_safe_to_move_forward() function with the code from:")
        print("   /home/pi/improved_safety_function.txt")
        print("4. Upload the updated code to Arduino")
        print("\nThis fix will:")
        print("✅ Take multiple sensor readings to filter noise")
        print("✅ Use average distance instead of single readings")
        print("✅ Ignore readings below 3cm (false readings)")
        print("✅ Require consistent IR sensor detections")
        print("✅ Keep your sensors working while preventing false blocking")
    
    def create_quick_safety_toggle(self):
        """Create a quick script to toggle safety on/off"""
        print("\n⚡ CREATING QUICK SAFETY TOGGLE")
        print("=" * 32)
        
        toggle_script = '''#!/usr/bin/env python3
"""
Quick safety toggle for testing
Usage: python3 safety_toggle.py [on|off]
"""
import sys
import serial
import time

def toggle_safety(mode):
    ports = ['/dev/ttyUSB0', '/dev/ttyACM0', '/dev/serial0']
    
    for port in ports:
        try:
            arduino = serial.Serial(port, 9600, timeout=2)
            time.sleep(1)
            
            if mode == 'off':
                arduino.write(b'SAFETY_OFF\\n')
                print("🔓 Safety DISABLED - Robot can move freely")
                print("⚠️ WARNING: No collision avoidance!")
            else:
                arduino.write(b'SAFETY_ON\\n')  
                print("🔒 Safety ENABLED - Collision avoidance active")
            
            arduino.close()
            return True
            
        except:
            continue
    
    print("❌ Could not connect to Arduino")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode in ['on', 'off']:
            toggle_safety(mode)
        else:
            print("Usage: python3 safety_toggle.py [on|off]")
    else:
        print("Usage: python3 safety_toggle.py [on|off]")
'''
        
        with open('/home/pi/safety_toggle.py', 'w') as f:
            f.write(toggle_script)
        
        # Make executable
        subprocess.run(['chmod', '+x', '/home/pi/safety_toggle.py'])
        
        print("✅ Safety toggle script created: /home/pi/safety_toggle.py")
        print("\n🎯 QUICK COMMANDS:")
        print("To disable safety:  python3 /home/pi/safety_toggle.py off")
        print("To enable safety:   python3 /home/pi/safety_toggle.py on")
    
    def run_full_diagnostic(self):
        """Run complete diagnostic and fix process"""
        print("🚀 RASPBERRY PI SENSOR INTERFERENCE DIAGNOSTIC")
        print("=" * 50)
        print("This tool will:")
        print("1. Detect Arduino connection")
        print("2. Test sensor readings for interference")
        print("3. Test movement with safety disabled") 
        print("4. Apply smart sensor filtering fix")
        print("5. Create safety toggle tools")
        print()
        
        # Step 1: Detect Arduino
        if not self.detect_arduino_connection():
            print("\n❌ Cannot proceed without Arduino connection")
            print("📝 Check:")
            print("  - USB cable connected")
            print("  - Arduino powered on")
            print("  - Correct drivers installed")
            return False
        
        # Step 2: Test sensors
        if not self.test_sensor_readings():
            print("\n⚠️ Sensor testing failed, but continuing...")
        
        # Step 3: Test movement
        if self.test_movement_with_safety_off():
            print("\n✅ DIAGNOSIS CONFIRMED: Sensors are blocking movement")
            
            # Step 4: Apply fixes
            self.apply_smart_sensor_fix()
            self.create_quick_safety_toggle()
            
            print("\n🎯 NEXT STEPS:")
            print("1. Apply the improved safety function to your Arduino code")
            print("2. OR use: python3 /home/pi/safety_toggle.py off")
            print("3. Test: python3 fix_motor_directions.py")
            
        else:
            print("\n❌ Issue is not sensor-related")
            print("📝 Check motor wiring and Arduino commands")
        
        return True

def main():
    """Main function for Raspberry Pi"""
    print("🤖 Starting Raspberry Pi sensor diagnostic...")
    
    # Check if running on Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            if 'Raspberry Pi' not in f.read():
                print("⚠️ This script is designed for Raspberry Pi")
                print("But continuing anyway...")
    except:
        pass
    
    fixer = RaspberryPiSensorFix()
    fixer.run_full_diagnostic()

if __name__ == "__main__":
    main() 