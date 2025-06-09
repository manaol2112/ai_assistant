"""
Real-time Camera Object Detection using YOLOv8
Optimized for detecting dinosaur toys, figurines, and related objects
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO
import logging

class CameraDetector:
    def __init__(self, model_size='n', confidence_threshold=0.5):
        """
        Initialize camera detector with YOLOv8
        
        Args:
            model_size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (extra large)
            confidence_threshold: Minimum confidence for detections
        """
        self.logger = logging.getLogger(__name__)
        
        # Load YOLOv8 model
        model_path = f'yolov8{model_size}.pt'
        print(f"Loading YOLOv8 model: {model_path}")
        self.model = YOLO(model_path)
        
        self.confidence_threshold = confidence_threshold
        
        # Classes that might be dinosaur-related or interesting
        self.target_classes = {
            # Animals that could be dinosaur-like
            'bird': 14,
            'cat': 15,
            'dog': 16,
            'horse': 17,
            'sheep': 18,
            'bear': 21,
            'zebra': 22,
            'giraffe': 24,
            'elephant': 25,
            # Objects that could be toys
            'teddy bear': 77,
            'book': 73,
            'vase': 75,
            # Add any other relevant classes
        }
        
        # Initialize camera
        self.cap = None
        self.is_running = False
        
    def start_camera(self, camera_index=0):
        """Start camera capture"""
        self.cap = cv2.VideoCapture(camera_index)
        
        if not self.cap.isOpened():
            raise Exception(f"Cannot open camera {camera_index}")
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("✅ Camera started successfully")
        return True
    
    def detect_objects(self, frame):
        """Run YOLOv8 detection on frame"""
        # Run inference
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)
        
        detections = []
        
        # Process results
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    # Get class name
                    class_name = self.model.names[class_id]
                    
                    detections.append({
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': float(confidence),
                        'class_name': class_name,
                        'class_id': class_id
                    })
        
        return detections
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        for detection in detections:
            bbox = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            
            x1, y1, x2, y2 = bbox
            
            # Choose color based on class (green for target classes, blue for others)
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
        
        return frame
    
    def run_detection(self, show_fps=True, save_video=False, output_path='detection_output.mp4'):
        """Run real-time detection on camera stream"""
        if not self.start_camera():
            return False
        
        self.is_running = True
        fps_counter = 0
        start_time = time.time()
        
        # Video writer setup if saving
        video_writer = None
        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))
        
        print("\n🦕 DINOSAUR DETECTOR ACTIVE 🦕")
        print("Press 'q' to quit, 's' to save screenshot")
        print("Looking for dinosaur-like objects and toys...")
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Run detection
                detections = self.detect_objects(frame)
                
                # Draw detections
                annotated_frame = self.draw_detections(frame.copy(), detections)
                
                # Add FPS counter
                if show_fps:
                    fps_counter += 1
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 1.0:
                        fps = fps_counter / elapsed_time
                        fps_counter = 0
                        start_time = time.time()
                        
                        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Add detection count
                cv2.putText(annotated_frame, f"Objects: {len(detections)}", (10, 70), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Show interesting detections
                target_detections = [d for d in detections if d['class_name'].lower() in [k.lower() for k in self.target_classes.keys()]]
                if target_detections:
                    print(f"🎯 Found {len(target_detections)} interesting objects: {[d['class_name'] for d in target_detections]}")
                
                # Save video frame if enabled
                if save_video and video_writer:
                    video_writer.write(annotated_frame)
                
                # Display frame
                cv2.imshow('YOLOv8 Dinosaur Detector', annotated_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    screenshot_name = f"detection_screenshot_{int(time.time())}.jpg"
                    cv2.imwrite(screenshot_name, annotated_frame)
                    print(f"📸 Screenshot saved: {screenshot_name}")
        
        except KeyboardInterrupt:
            print("\n⚠️ Detection stopped by user")
        
        finally:
            self.cleanup()
            if video_writer:
                video_writer.release()
            print("🏁 Detection stopped")
    
    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def list_available_classes(self):
        """List all classes the model can detect"""
        print("\n📋 Available detection classes:")
        for i, class_name in self.model.names.items():
            print(f"  {i:2d}: {class_name}")
        
        print(f"\n🎯 Target classes for dinosaur-like detection:")
        for class_name in self.target_classes.keys():
            print(f"  - {class_name}")

def main():
    """Main function to run camera detection"""
    print("🦕 YOLOv8 Dinosaur Detection System 🦕")
    
    # Create detector (use 'n' for fastest, 's' for better accuracy)
    detector = CameraDetector(model_size='n', confidence_threshold=0.4)
    
    # Show available classes
    detector.list_available_classes()
    
    # Ask user for preferences
    print("\nStarting camera detection...")
    print("Note: Pre-trained YOLOv8 doesn't have 'dinosaur' class.")
    print("We'll detect animals and objects that could be dinosaur toys/figurines.")
    
    # Run detection
    try:
        detector.run_detection(show_fps=True, save_video=False)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        detector.cleanup()

if __name__ == "__main__":
    main() 