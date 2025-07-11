"""
Smart Camera Detection with Face Recognition
Enhanced YOLOv8 + Face Recognition for Sophia
Natural conversation flow with personalized greetings
"""

import cv2
import time
import numpy as np
import os
import logging
from typing import Optional, List, Dict, Any
from ultralytics import YOLO

# Try to import face recognition
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️ Face recognition not available. Install with: pip install face-recognition")

class SmartCameraDetector:
    def __init__(self, model_size='n', confidence_threshold=0.5, headless=False):
        """
        Initialize smart camera detector with YOLOv8 and face recognition
        Enhanced for AITRIOS AI Camera support
        
        Args:
            model_size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (extra large)
            confidence_threshold: Minimum confidence for detections
            headless: Hide camera display when True
        """
        self.logger = logging.getLogger(__name__)
        
        # Check for AITRIOS camera availability
        try:
            from aitrios_camera_handler import AITRIOSCameraHandler
            self.aitrios_available = True
            self.logger.info("🤖 AITRIOS AI Camera support detected")
        except ImportError:
            self.aitrios_available = False
            self.logger.info("📷 Using standard camera detection")
        
        # Load YOLOv8 model for non-AITRIOS cameras
        self.model_size = model_size
        self.confidence_threshold = confidence_threshold
        self.headless = headless  # Hide camera display when True
        self.model = None
        self.device = 'cpu'  # Default to CPU for compatibility
        self.model_path = f'yolov8{model_size}.pt'
        print(f"🤖 Loading YOLOv8 model: {self.model_path}")
        self.model = YOLO(self.model_path)
        
        # Face recognition setup
        self.face_recognition_enabled = FACE_RECOGNITION_AVAILABLE
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_detection_threshold = 0.6
        
        # Greeting system
        self.last_greeting_time = {}
        self.greeting_cooldown = 10  # seconds between greetings for same person
        
        # Enhanced target classes for better detection
        self.target_classes = {
            # Animals that could be dinosaur-like
            'bird': 14, 'cat': 15, 'dog': 16, 'horse': 17, 'sheep': 18,
            'bear': 21, 'zebra': 22, 'giraffe': 24, 'elephant': 25,
            # Objects that could be toys
            'teddy bear': 77, 'book': 73, 'vase': 75,
            # People
            'person': 0
        }
        
        # Camera management - support both standalone and shared modes
        self.cap = None
        self.shared_camera = None  # NEW: for shared camera mode
        self.is_running = False
        
        # Performance tracking
        self.detection_count = 0
        self.last_fps_time = time.time()
        
        # Load known faces
        if self.face_recognition_enabled:
            self.load_known_faces()
        
    def load_known_faces(self):
        """Load known faces from the people directory."""
        if not self.face_recognition_enabled:
            return
        
        people_dir = "people"
        if not os.path.exists(people_dir):
            print(f"⚠️ People directory '{people_dir}' not found")
            return
        
        print("👤 Loading known faces...")
        
        for person_name in os.listdir(people_dir):
            person_path = os.path.join(people_dir, person_name)
            if not os.path.isdir(person_path):
                continue
            
            print(f"   Loading faces for {person_name.title()}...")
            person_encodings = []
            
            # Load all images for this person
            for image_file in os.listdir(person_path):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(person_path, image_file)
                    
                    try:
                        # Load image
                        image = face_recognition.load_image_file(image_path)
                        
                        # Get face encodings
                        encodings = face_recognition.face_encodings(image)
                        
                        if encodings:
                            person_encodings.extend(encodings)
                            print(f"     ✅ Loaded {len(encodings)} face(s) from {image_file}")
                        else:
                            print(f"     ⚠️ No face found in {image_file}")
                    
                    except Exception as e:
                        print(f"     ❌ Error loading {image_file}: {e}")
            
            # Add all encodings for this person
            if person_encodings:
                self.known_face_encodings.extend(person_encodings)
                self.known_face_names.extend([person_name] * len(person_encodings))
                print(f"   ✅ Total {len(person_encodings)} face encodings loaded for {person_name.title()}")
        
        print(f"🎉 Face recognition ready! Loaded {len(self.known_face_names)} face encodings for {len(set(self.known_face_names))} people")

    def detect_faces(self, frame):
        """Detect and recognize faces - enhanced with AITRIOS AI when available"""
        if not self.face_recognition_enabled:
            return []
        
        try:
            # Check if we're using AITRIOS camera with AI face detection
            if (hasattr(self.shared_camera, 'using_aitrios') and 
                self.shared_camera.using_aitrios and 
                hasattr(self.shared_camera, 'aitrios_handler')):
                
                # Use AITRIOS AI face detection
                ai_faces = self.shared_camera.aitrios_handler.detect_faces()
                
                # Convert to our format and add greeting logic
                face_detections = []
                for face in ai_faces:
                    name = face.get('name', 'Unknown')
                    confidence = face.get('confidence', 0)
                    bbox = face.get('bbox', [0, 0, 0, 0])
                    
                    face_detections.append({
                        'name': name,
                        'confidence': confidence,
                        'bbox': bbox,
                        'location': face.get('location', bbox),
                        'source': 'AITRIOS_AI'
                    })
                
                self.logger.debug(f"🤖 AITRIOS detected {len(face_detections)} faces")
                return face_detections
            
            # Fallback to standard face recognition
            # Resize frame for faster face recognition
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find faces
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            face_detections = []
            
            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=self.face_detection_threshold)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                
                name = "Unknown"
                confidence = 0.0
                
                if any(matches):
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1.0 - face_distances[best_match_index]
                
                # Scale back up face locations
                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                face_detections.append({
                    'name': name,
                    'confidence': confidence,
                    'bbox': (left, top, right, bottom),
                    'location': (top, right, bottom, left),
                    'source': 'face_recognition'
                })
            
            return face_detections
            
        except Exception as e:
            self.logger.error(f"Error in face detection: {e}")
            return []

    def should_greet(self, person_name: str) -> bool:
        """Check if we should greet this person (based on cooldown)."""
        current_time = time.time()
        last_time = self.last_greeting_time.get(person_name, 0)
        
        if current_time - last_time > self.greeting_cooldown:
            self.last_greeting_time[person_name] = current_time
            return True
        
        return False

    def generate_greeting(self, person_name: str) -> str:
        """Generate a personalized greeting."""
        greetings = {
            'sophia': [
                "Hello Sophia! I see you! 👋",
                "Hi there, Sophia! How are you today?",
                "Sophia! Welcome back! 😊",
                "Hey Sophia! Great to see you again!",
                "Hello beautiful Sophia! ✨"
            ],
            'eladriel': [
                "Hey Eladriel! I see you! 👋",
                "Hi Eladriel! How's it going?",
                "Eladriel! Welcome back! 😊",
                "Hey there, Eladriel! Good to see you!"
            ]
        }
        
        person_greetings = greetings.get(person_name.lower(), [f"Hello {person_name.title()}! I see you!"])
        return np.random.choice(person_greetings)

    def start_camera(self, camera_index=0):
        """Start camera capture - enhanced for AITRIOS support"""
        # Check if we have a shared camera first
        if self.shared_camera and self.shared_camera.is_camera_available():
            self.logger.info("🤖 Using shared camera for smart detection")
            
            # Check if shared camera has AI capabilities
            if hasattr(self.shared_camera, 'using_aitrios') and self.shared_camera.using_aitrios:
                self.logger.info("✨ AITRIOS AI features available for enhanced detection")
            
            self.cap = self.shared_camera
            return True
        
        # Otherwise initialize our own camera
        self.logger.info(f"📷 Starting camera {camera_index} for detection")
        self.cap = cv2.VideoCapture(camera_index)
        
        if not self.cap.isOpened():
            self.logger.error(f"❌ Failed to open camera {camera_index}")
            return False
        
        # Set properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.logger.info("✅ Camera started successfully")
        return True

    def detect_objects(self, frame):
        """Detect objects - enhanced with AITRIOS AI when available"""
        object_detections = []
        
        try:
            # Check if we're using AITRIOS camera with AI capabilities
            if (hasattr(self.shared_camera, 'using_aitrios') and 
                self.shared_camera.using_aitrios and 
                hasattr(self.shared_camera, 'aitrios_handler')):
                
                # Use AITRIOS AI object detection
                ai_objects = self.shared_camera.aitrios_handler.detect_objects()
                
                for obj in ai_objects:
                    # Convert AITRIOS format to our format
                    class_name = obj.get('class', 'unknown')
                    confidence = obj.get('confidence', 0)
                    bbox = obj.get('bbox', [0, 0, 0, 0])
                    
                    if confidence > self.confidence_threshold:
                        object_detections.append({
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': bbox,
                            'source': 'AITRIOS_AI'
                        })
                
                self.logger.debug(f"🤖 AITRIOS detected {len(object_detections)} objects")
                return object_detections
            
            # Fallback to YOLOv8 detection for standard cameras
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for i, box in enumerate(boxes):
                        # Extract detection info
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        xyxy = box.xyxy[0].cpu().numpy()
                        
                        # Get class name
                        class_name = self.model.names[cls] if cls < len(self.model.names) else 'unknown'
                        
                        # Check if it's a target class or high confidence
                        if class_name in self.target_classes or conf > 0.7:
                            object_detections.append({
                                'class': class_name,
                                'confidence': conf,
                                'bbox': xyxy.tolist(),
                                'source': 'YOLOv8'
                            })
            
            return object_detections
            
        except Exception as e:
            self.logger.error(f"Error in object detection: {e}")
            return []

    def draw_detections(self, frame, object_detections, face_detections):
        """Draw bounding boxes and labels on frame"""
        # Draw object detections
        for detection in object_detections:
            bbox = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class']
            
            x1, y1, x2, y2 = bbox
            
            # Choose color based on class
            color = (0, 255, 0) if class_name.lower() in [k.lower() for k in self.target_classes.keys()] else (255, 0, 0)
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Create label
            label = f"{class_name}: {confidence:.2f}"
            
            # Get text size for background
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            
            # Draw label background
            cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
            
            # Draw label text
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Draw face detections with special styling
        for face in face_detections:
            left, top, right, bottom = face['bbox']
            name = face['name']
            confidence = face['confidence']
            
            # Choose color based on recognition
            if name != "Unknown":
                color = (0, 255, 255)  # Yellow for known faces
                thickness = 3
            else:
                color = (0, 0, 255)    # Red for unknown faces
                thickness = 2
            
            # Draw face rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)
            
            # Create face label
            if name != "Unknown":
                face_label = f"{name.title()}: {confidence:.2f}"
            else:
                face_label = "Unknown Person"
            
            # Get text size for background
            (text_width, text_height), _ = cv2.getTextSize(face_label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom + 5), (left + text_width, bottom + text_height + 15), color, -1)
            
            # Draw label text
            cv2.putText(frame, face_label, (left, bottom + text_height + 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame

    def run_detection(self, show_fps=True, save_video=False, output_path='smart_detection_output.mp4'):
        """Run real-time detection with face recognition"""
        # Check camera availability - prefer shared camera
        camera_available = False
        if self.shared_camera and self.shared_camera.is_camera_available():
            print("🎥 Using shared camera for detection")
            camera_available = True
        elif self.start_camera():
            print("🎥 Using standalone camera for detection")
            camera_available = True
        
        if not camera_available:
            print("❌ No camera available for detection")
            return False
        
        self.is_running = True
        fps_counter = 0
        start_time = time.time()
        
        # Video writer setup if saving
        video_writer = None
        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))
        
        print("\n🦕🤖 SMART DETECTOR ACTIVE 🤖🦕")
        print("Features:")
        print("  • YOLOv8 Object Detection")
        if self.face_recognition_enabled:
            print("  • Face Recognition for Sophia & Others")
            print("  • Personalized Greetings")
        print("\nControls:")
        print("  • Press 'q' to quit")
        print("  • Press 's' to save screenshot")
        print("  • Press 'g' to force greet detected people")
        
        try:
            while self.is_running:
                # Read from shared camera or standalone camera
                if self.shared_camera and self.shared_camera.is_camera_available():
                    ret, frame = self.shared_camera.read()
                else:
                    ret, frame = self.cap.read()
                
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Run detections
                object_detections = self.detect_objects(frame)
                face_detections = self.detect_faces(frame) if self.face_recognition_enabled else []
                
                # Process face detections for greetings
                for face in face_detections:
                    if face['name'] != "Unknown" and face['confidence'] > self.face_detection_threshold:
                        if self.should_greet(face['name']):
                            greeting = self.generate_greeting(face['name'])
                            print(f"\n🎉 {greeting}")
                
                # Draw all detections
                annotated_frame = self.draw_detections(frame.copy(), object_detections, face_detections)
                
                # Add status overlay
                if show_fps:
                    fps_counter += 1
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 1.0:
                        fps = fps_counter / elapsed_time
                        fps_counter = 0
                        start_time = time.time()
                        
                        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Add detection counts
                cv2.putText(annotated_frame, f"Objects: {len(object_detections)}", (10, 70), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                if self.face_recognition_enabled:
                    known_faces = len([f for f in face_detections if f['name'] != "Unknown"])
                    cv2.putText(annotated_frame, f"Known Faces: {known_faces}", (10, 110), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Show interesting detections
                target_detections = [d for d in object_detections if d['class'].lower() in [k.lower() for k in self.target_classes.keys()]]
                if target_detections:
                    objects = [d['class'] for d in target_detections]
                    print(f"🎯 Objects: {objects}")
                
                # Save video frame if enabled
                if save_video and video_writer:
                    video_writer.write(annotated_frame)
                
                # Display frame only if not in headless mode
                if not self.headless:
                    cv2.imshow('Smart Camera Detector', annotated_frame)
                
                # Handle key presses only if not in headless mode
                if not self.headless:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        timestamp = int(time.time())
                        screenshot_name = f"smart_detection_screenshot_{timestamp}.jpg"
                        cv2.imwrite(screenshot_name, annotated_frame)
                        print(f"📸 Screenshot saved: {screenshot_name}")
                    elif key == ord('g'):
                        # Force greet all detected known faces
                        for face in face_detections:
                            if face['name'] != "Unknown":
                                greeting = self.generate_greeting(face['name'])
                                print(f"👋 {greeting}")
                else:
                    # In headless mode, just add a small delay
                    time.sleep(0.03)  # ~30 FPS timing
        
        except KeyboardInterrupt:
            print("\n⚠️ Detection stopped by user")
        
        finally:
            self.cleanup()
            if video_writer:
                video_writer.release()
            print("🏁 Smart detection stopped")

    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        # Only release camera if we're using standalone mode
        if self.cap and not self.shared_camera:
            self.cap.release()
            print("📷 Standalone camera released")
        elif self.shared_camera:
            print("📷 Shared camera remains active")
        cv2.destroyAllWindows()

def main():
    """Main function to run smart camera detection"""
    print("🦕🤖 Smart Camera Detection System 🤖🦕")
    print("Enhanced with Face Recognition & Natural Greetings")
    
    # Create detector
    detector = SmartCameraDetector(model_size='n', confidence_threshold=0.4)
    
    print(f"\n📊 System Status:")
    print(f"  • YOLOv8: ✅ Ready")
    print(f"  • Face Recognition: {'✅ Ready' if detector.face_recognition_enabled else '❌ Not Available'}")
    print(f"  • Known People: {len(set(detector.known_face_names))}")
    
    # Run detection
    try:
        detector.run_detection(show_fps=True, save_video=False)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        detector.cleanup()

if __name__ == "__main__":
    main() 