#!/usr/bin/env python3
"""
Test Face Tracking Setup
Comprehensive test script to verify Arduino connection, servo functionality, 
and face recognition setup before running the full face tracking system.
"""

import serial
import time
import cv2
import os
import face_recognition
from typing import List, Dict

class FaceTrackingSetupTester:
    """Premium setup tester for face tracking system"""
    
    def __init__(self):
        self.arduino_ports = ['/dev/ttyUSB0', '/dev/ttyACM0', '/dev/ttyUSB1']
        self.arduino_baud = 9600
        self.test_results = {}
        
    def test_arduino_connection(self) -> Dict:
        """Test Arduino serial connection"""
        print("🔌 Testing Arduino Connection...")
        print("-" * 40)
        
        for port in self.arduino_ports:
            try:
                print(f"  Trying {port}...")
                arduino = serial.Serial(port, self.arduino_baud, timeout=2)
                time.sleep(2)  # Wait for Arduino initialization
                
                # Test with a simple servo command
                arduino.write(b"SERVO_90\n")
                arduino.flush()
                time.sleep(0.5)
                
                arduino.write(b"SERVO2_90\n") 
                arduino.flush()
                time.sleep(0.5)
                
                arduino.close()
                
                print(f"  ✅ Successfully connected to Arduino on {port}")
                return {
                    'status': 'success',
                    'port': port,
                    'message': f'Arduino connected on {port}'
                }
                
            except Exception as e:
                print(f"  ❌ Failed to connect to {port}: {e}")
                continue
                
        return {
            'status': 'failed',
            'port': None,
            'message': 'No Arduino found on any port'
        }
        
    def test_servo_movement(self, arduino_port: str) -> Dict:
        """Test servo movement functionality"""
        print(f"\n🎯 Testing Servo Movement on {arduino_port}...")
        print("-" * 40)
        
        try:
            arduino = serial.Serial(arduino_port, self.arduino_baud, timeout=2)
            time.sleep(2)
            
            # Test sequence for both servos
            test_positions = [
                (90, 90, "Center position"),
                (45, 90, "Servo1 left"),
                (135, 90, "Servo1 right"), 
                (90, 60, "Servo2 up"),
                (90, 120, "Servo2 down"),
                (90, 90, "Return to center")
            ]
            
            print("  Starting servo movement test sequence...")
            
            for servo1, servo2, description in test_positions:
                print(f"  🎮 {description}: ({servo1}, {servo2})")
                
                # Send servo commands
                arduino.write(f"SERVO_{servo1}\n".encode())
                arduino.flush()
                time.sleep(0.2)
                
                arduino.write(f"SERVO2_{servo2}\n".encode())
                arduino.flush()
                time.sleep(1.5)  # Wait to see movement
                
            arduino.close()
            print("  ✅ Servo movement test completed successfully!")
            
            return {
                'status': 'success',
                'message': 'All servo movements executed'
            }
            
        except Exception as e:
            print(f"  ❌ Servo test failed: {e}")
            return {
                'status': 'failed', 
                'message': f'Servo test error: {e}'
            }
            
    def test_camera_access(self) -> Dict:
        """Test camera access using the existing CameraHandler system"""
        print("\n📸 Testing Camera Access...")
        print("-" * 40)
        
        # First try using the existing CameraHandler (supports Sony IMX500 AI Camera)
        try:
            print("  🤖 Testing with CameraHandler (Sony IMX500 AI Camera support)...")
            
            # Import the existing camera handler
            from camera_handler import CameraHandler
            
            # Initialize camera handler with IMX500 preference
            camera_handler = CameraHandler(camera_index=0, prefer_imx500=True)
            
            if camera_handler.is_camera_available():
                camera_type = "Sony IMX500 AI" if camera_handler.using_imx500 else "USB"
                print(f"  ✅ {camera_type} camera initialized successfully")
                
                # Test frame capture
                ret, frame = camera_handler.read()
                if ret and frame is not None:
                    height, width = frame.shape[:2]
                    print(f"  ✅ Camera capture working - Resolution: {width}x{height}")
                    
                    # Save test frame
                    cv2.imwrite('camera_test_working.jpg', frame)
                    print(f"  📸 Test image saved as camera_test_working.jpg")
                    
                    # Test AI capabilities if using IMX500
                    if camera_handler.using_imx500:
                        ai_status = camera_handler.get_ai_status()
                        print(f"  🤖 AI Status: {ai_status}")
                    
                    camera_handler.release()
                    
                    return {
                        'status': 'success',
                        'camera_type': camera_type,
                        'using_imx500': camera_handler.using_imx500,
                        'resolution': (width, height),
                        'message': f'{camera_type} camera working properly'
                    }
                else:
                    print(f"  ❌ Camera initialized but can't capture frames")
                    camera_handler.release()
            else:
                print(f"  ❌ CameraHandler reports camera not available")
                
        except Exception as e:
            print(f"  ❌ CameraHandler error: {e}")
            
        # Fallback to basic OpenCV test
        print("  🔄 Falling back to basic OpenCV camera test...")
        camera_indices = [0, 1, 2]
        
        for index in camera_indices:
            try:
                print(f"  Trying basic camera index {index}...")
                camera = cv2.VideoCapture(index)
                
                if not camera.isOpened():
                    print(f"  ❌ Camera {index} not accessible")
                    continue
                    
                # Test frame capture
                ret, frame = camera.read()
                if not ret:
                    print(f"  ❌ Camera {index} can't capture frames")
                    camera.release()
                    continue
                    
                height, width = frame.shape[:2]
                print(f"  ✅ Basic camera {index} working - Resolution: {width}x{height}")
                
                # Save test frame
                cv2.imwrite(f'camera_test_basic_{index}.jpg', frame)
                print(f"  📸 Test image saved as camera_test_basic_{index}.jpg")
                
                camera.release()
                
                return {
                    'status': 'success',
                    'camera_type': 'Basic USB',
                    'using_imx500': False,
                    'camera_index': index,
                    'resolution': (width, height),
                    'message': f'Basic camera {index} working properly'
                }
                
            except Exception as e:
                print(f"  ❌ Camera {index} error: {e}")
                continue
                
        return {
            'status': 'failed',
            'message': 'No working camera found with any method'
        }
        
    def test_face_recognition_setup(self) -> Dict:
        """Test face recognition and encodings"""
        print("\n👤 Testing Face Recognition Setup...")
        print("-" * 40)
        
        target_people = ['sophia', 'eladriel']
        total_encodings = 0
        people_found = []
        
        for person in target_people:
            person_dir = f"people/{person}"
            print(f"  Checking {person_dir}...")
            
            if not os.path.exists(person_dir):
                print(f"  ⚠️ Directory {person_dir} not found")
                continue
                
            image_files = [f for f in os.listdir(person_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not image_files:
                print(f"  ⚠️ No image files found in {person_dir}")
                continue
                
            print(f"  📁 Found {len(image_files)} images for {person}")
            
            person_encodings = 0
            for img_file in image_files:
                try:
                    img_path = os.path.join(person_dir, img_file)
                    image = face_recognition.load_image_file(img_path)
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        person_encodings += 1
                        print(f"    ✅ {img_file} - Face encoding extracted")
                    else:
                        print(f"    ⚠️ {img_file} - No face found")
                        
                except Exception as e:
                    print(f"    ❌ {img_file} - Error: {e}")
                    
            if person_encodings > 0:
                total_encodings += person_encodings
                people_found.append(person)
                print(f"  ✅ {person}: {person_encodings} valid encodings")
            else:
                print(f"  ❌ {person}: No valid face encodings")
                
        if total_encodings > 0:
            return {
                'status': 'success',
                'total_encodings': total_encodings,
                'people_found': people_found,
                'message': f'Face recognition ready with {total_encodings} encodings'
            }
        else:
            return {
                'status': 'warning',
                'total_encodings': 0,
                'people_found': [],
                'message': 'No face encodings found - system will track any face'
            }
            
    def test_dependencies(self) -> Dict:
        """Test required Python dependencies"""
        print("\n📦 Testing Dependencies...")
        print("-" * 40)
        
        required_modules = [
            ('cv2', 'OpenCV'),
            ('face_recognition', 'Face Recognition'),
            ('serial', 'PySerial'),
            ('numpy', 'NumPy')
        ]
        
        missing_modules = []
        
        for module_name, display_name in required_modules:
            try:
                __import__(module_name)
                print(f"  ✅ {display_name} - Available")
            except ImportError:
                print(f"  ❌ {display_name} - Missing")
                missing_modules.append(display_name)
                
        # Test camera handler availability
        try:
            from camera_handler import CameraHandler
            print(f"  ✅ CameraHandler - Available (Sony IMX500 AI support)")
        except ImportError:
            print(f"  ⚠️ CameraHandler - Not available (basic camera only)")
                
        if missing_modules:
            return {
                'status': 'failed',
                'missing': missing_modules,
                'message': f'Missing modules: {", ".join(missing_modules)}'
            }
        else:
            return {
                'status': 'success',
                'message': 'All dependencies available'
            }
            
    def run_comprehensive_test(self) -> Dict:
        """Run all tests and provide comprehensive report"""
        print("🤖 AI Assistant Face Tracking - Setup Test")
        print("=" * 50)
        
        results = {}
        
        # Test dependencies first
        results['dependencies'] = self.test_dependencies()
        if results['dependencies']['status'] == 'failed':
            print(f"\n❌ CRITICAL: Missing dependencies - {results['dependencies']['message']}")
            return results
            
        # Test Arduino connection
        results['arduino'] = self.test_arduino_connection()
        arduino_port = results['arduino'].get('port')
        
        # Test servo movement if Arduino connected
        if arduino_port:
            results['servos'] = self.test_servo_movement(arduino_port)
        else:
            results['servos'] = {'status': 'skipped', 'message': 'Arduino not connected'}
            
        # Test camera
        results['camera'] = self.test_camera_access()
        
        # Test face recognition
        results['face_recognition'] = self.test_face_recognition_setup()
        
        # Generate summary report
        self.print_summary_report(results)
        
        return results
        
    def print_summary_report(self, results: Dict):
        """Print comprehensive summary report"""
        print("\n" + "=" * 50)
        print("📊 SETUP TEST SUMMARY REPORT")
        print("=" * 50)
        
        # Overall status
        critical_failures = []
        warnings = []
        successes = []
        
        for test_name, result in results.items():
            status = result['status']
            message = result['message']
            
            if status == 'success':
                successes.append(f"✅ {test_name.title()}: {message}")
            elif status == 'failed':
                critical_failures.append(f"❌ {test_name.title()}: {message}")
            elif status == 'warning':
                warnings.append(f"⚠️ {test_name.title()}: {message}")
            else:
                warnings.append(f"⏭️ {test_name.title()}: {message}")
                
        # Print results
        if successes:
            print("\n🟢 WORKING COMPONENTS:")
            for success in successes:
                print(f"  {success}")
                
        if warnings:
            print("\n🟡 WARNINGS:")
            for warning in warnings:
                print(f"  {warning}")
                
        if critical_failures:
            print("\n🔴 CRITICAL ISSUES:")
            for failure in critical_failures:
                print(f"  {failure}")
                
        # Overall recommendation
        print("\n" + "=" * 50)
        if critical_failures:
            print("❌ RECOMMENDATION: Fix critical issues before proceeding")
            print("   • Check Arduino connections and serial ports")
            print("   • Install missing dependencies")
            print("   • Verify hardware connections")
        elif warnings:
            print("⚠️ RECOMMENDATION: System partially ready")
            print("   • Face tracking will work but may have limitations")
            print("   • Consider adding face encodings for better performance")
        else:
            print("✅ RECOMMENDATION: System fully ready!")
            print("   • All components tested successfully")
            print("   • Ready to run face tracking system")
            
        print("\n🚀 To start face tracking, run:")
        print("   python face_tracking_servo_controller.py")

def main():
    """Main test function"""
    tester = FaceTrackingSetupTester()
    results = tester.run_comprehensive_test()
    
    # Cleanup test images
    try:
        test_files = ['camera_test_working.jpg'] + [f'camera_test_basic_{i}.jpg' for i in range(3)]
        for test_file in test_files:
            if os.path.exists(test_file):
                os.remove(test_file)
    except:
        pass
        
    return results

if __name__ == "__main__":
    main() 