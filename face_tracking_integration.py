#!/usr/bin/env python3
"""
Face Tracking Integration for AI Assistant
Integrates the face tracking servo controller with the main AI assistant system.

Voice Commands:
- "look at me" / "track my face" - Start face tracking
- "stop looking" / "stop tracking" - Stop face tracking  
- "look left/right/up/down" - Manual servo control
- "center your eyes" / "look forward" - Center servos
- "who are you looking at" - Get current tracking status
"""

from face_tracking_servo_controller import PremiumFaceTracker
import threading
import time
import logging
from typing import Dict, Optional

class FaceTrackingIntegration:
    """
    Integration class for face tracking with AI Assistant
    Handles voice commands and system integration
    """
    
    def __init__(self, main_ai_assistant=None):
        self.ai_assistant = main_ai_assistant
        self.face_tracker = None
        self.is_initialized = False
        
        # Setup logging
        self.logger = logging.getLogger('FaceTrackingIntegration')
        
        # Voice command mappings
        self.voice_commands = {
            # Start tracking commands
            'start_tracking': [
                'look at me', 'track my face', 'follow me', 'watch me',
                'start face tracking', 'begin tracking', 'look for me'
            ],
            
            # Stop tracking commands  
            'stop_tracking': [
                'stop looking', 'stop tracking', 'stop following',
                'stop face tracking', 'look away', 'stop watching'
            ],
            
            # Manual control commands
            'look_left': ['look left', 'turn left', 'look to your left'],
            'look_right': ['look right', 'turn right', 'look to your right'], 
            'look_up': ['look up', 'look upward'],
            'look_down': ['look down', 'look downward'],
            
            # Center commands
            'center_view': [
                'center your eyes', 'look forward', 'look straight',
                'center view', 'look ahead', 'face forward'
            ],
            
            # Status commands
            'tracking_status': [
                'who are you looking at', 'who are you tracking',
                'what are you looking at', 'tracking status'
            ]
        }
        
    def initialize(self, arduino_port='/dev/ttyUSB0', camera_index=0):
        """Initialize the face tracking system"""
        try:
            self.logger.info("🔄 Initializing face tracking integration...")
            
            # Initialize face tracker
            self.face_tracker = PremiumFaceTracker(
                arduino_port=arduino_port,
                camera_index=camera_index
            )
            
            # Initialize camera and Arduino
            camera_ok = self.face_tracker.initialize_camera()
            arduino_ok = self.face_tracker.initialize_arduino()
            
            if not arduino_ok:
                self.logger.error("❌ Arduino not connected")
                return False
                
            if not camera_ok:
                self.logger.error("❌ Camera not available") 
                return False
                
            # Check face encodings
            if len(self.face_tracker.known_face_names) == 0:
                self.logger.warning("⚠️ No face encodings loaded - will track any face")
                
            self.is_initialized = True
            self.logger.info("✅ Face tracking integration initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Face tracking initialization failed: {e}")
            return False
            
    def process_voice_command(self, command_text: str) -> Optional[Dict]:
        """Process voice commands related to face tracking"""
        if not self.is_initialized:
            return None
            
        command_text = command_text.lower().strip()
        
        # Check each command category
        for command_type, phrases in self.voice_commands.items():
            for phrase in phrases:
                if phrase in command_text:
                    return self._execute_command(command_type, command_text)
                    
        return None
        
    def _execute_command(self, command_type: str, original_text: str) -> Dict:
        """Execute the identified command"""
        try:
            if command_type == 'start_tracking':
                return self._start_tracking()
                
            elif command_type == 'stop_tracking':
                return self._stop_tracking()
                
            elif command_type == 'look_left':
                return self._manual_look('left')
                
            elif command_type == 'look_right':
                return self._manual_look('right')
                
            elif command_type == 'look_up':
                return self._manual_look('up')
                
            elif command_type == 'look_down':
                return self._manual_look('down')
                
            elif command_type == 'center_view':
                return self._center_view()
                
            elif command_type == 'tracking_status':
                return self._get_tracking_status()
                
        except Exception as e:
            self.logger.error(f"❌ Command execution failed: {e}")
            return {
                'status': 'error',
                'message': f"Sorry, I couldn't execute that command: {str(e)}",
                'response': "I encountered an error while trying to move my eyes."
            }
            
    def _start_tracking(self) -> Dict:
        """Start face tracking"""
        if not self.face_tracker:
            return {
                'status': 'error', 
                'message': 'Face tracker not initialized',
                'response': "I'm sorry, my face tracking system isn't ready yet."
            }
            
        try:
            self.face_tracker.tracking_active = True
            self.logger.info("👁️ Face tracking started via voice command")
            
            return {
                'status': 'success',
                'message': 'Face tracking started',
                'response': "I'm now looking for familiar faces to follow. I'll track Sophia or Eladriel when I see them!"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to start tracking: {e}',
                'response': "I had trouble starting my face tracking. Let me try to fix that."
            }
            
    def _stop_tracking(self) -> Dict:
        """Stop face tracking"""
        if not self.face_tracker:
            return {
                'status': 'error',
                'message': 'Face tracker not initialized', 
                'response': "My face tracking system isn't available right now."
            }
            
        try:
            self.face_tracker.tracking_active = False
            # Center servos when stopping
            self.face_tracker.move_servos(
                self.face_tracker.servo1_center, 
                self.face_tracker.servo2_center
            )
            self.logger.info("🛑 Face tracking stopped via voice command")
            
            return {
                'status': 'success',
                'message': 'Face tracking stopped',
                'response': "I've stopped tracking faces and returned to center position."
            }
            
        except Exception as e:
            return {
                'status': 'error', 
                'message': f'Failed to stop tracking: {e}',
                'response': "I had trouble stopping the face tracking."
            }
            
    def _manual_look(self, direction: str) -> Dict:
        """Manual servo control for looking in specific directions"""
        if not self.face_tracker:
            return {
                'status': 'error',
                'message': 'Face tracker not initialized',
                'response': "My servo control system isn't available right now."
            }
            
        try:
            # Temporarily stop tracking for manual control
            was_tracking = self.face_tracker.tracking_active
            self.face_tracker.tracking_active = False
            
            # Get current positions
            current_pan = self.face_tracker.servo1_current
            current_tilt = self.face_tracker.servo2_current
            
            # Calculate new positions based on direction
            movement_step = 30  # degrees
            
            if direction == 'left':
                new_pan = max(self.face_tracker.servo_min, current_pan - movement_step)
                new_tilt = current_tilt
                response = "Looking left now."
                
            elif direction == 'right':
                new_pan = min(self.face_tracker.servo_max, current_pan + movement_step)
                new_tilt = current_tilt
                response = "Looking right now."
                
            elif direction == 'up':
                new_pan = current_pan
                new_tilt = max(self.face_tracker.servo_min, current_tilt - movement_step)
                response = "Looking up now."
                
            elif direction == 'down':
                new_pan = current_pan
                new_tilt = min(self.face_tracker.servo_max, current_tilt + movement_step)
                response = "Looking down now."
                
            else:
                return {
                    'status': 'error',
                    'message': f'Invalid direction: {direction}',
                    'response': "I don't understand that direction."
                }
                
            # Move servos
            self.face_tracker.move_servos(new_pan, new_tilt)
            
            # Brief pause, then restore tracking state
            time.sleep(0.5)
            self.face_tracker.tracking_active = was_tracking
            
            self.logger.info(f"👁️ Manual look command: {direction}")
            
            return {
                'status': 'success',
                'message': f'Looked {direction}',
                'response': response
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to look {direction}: {e}',
                'response': f"I had trouble looking {direction}."
            }
            
    def _center_view(self) -> Dict:
        """Center the servo positions"""
        if not self.face_tracker:
            return {
                'status': 'error',
                'message': 'Face tracker not initialized',
                'response': "My servo control system isn't available right now."
            }
            
        try:
            # Center servos
            self.face_tracker.move_servos(
                self.face_tracker.servo1_center,
                self.face_tracker.servo2_center
            )
            
            self.logger.info("🎯 Servos centered via voice command")
            
            return {
                'status': 'success', 
                'message': 'View centered',
                'response': "I'm now looking straight ahead."
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to center view: {e}',
                'response': "I had trouble centering my view."
            }
            
    def _get_tracking_status(self) -> Dict:
        """Get current tracking status"""
        if not self.face_tracker:
            return {
                'status': 'error',
                'message': 'Face tracker not initialized',
                'response': "My face tracking system isn't available right now."
            }
            
        try:
            tracking_active = self.face_tracker.tracking_active
            current_target = getattr(self.face_tracker, 'target_person', None)
            known_faces = self.face_tracker.known_face_names
            
            # Build status response
            if not tracking_active:
                response = "I'm not currently tracking any faces. I'm looking straight ahead."
            elif current_target:
                response = f"I'm actively tracking {current_target}."
            elif known_faces:
                response = f"I'm looking for familiar faces. I can recognize: {', '.join(known_faces)}."
            else:
                response = "I'm looking for any faces to track."
                
            return {
                'status': 'success',
                'message': 'Status retrieved',
                'response': response,
                'details': {
                    'tracking_active': tracking_active,
                    'current_target': current_target,
                    'known_faces': known_faces,
                    'servo_positions': {
                        'pan': self.face_tracker.servo1_current,
                        'tilt': self.face_tracker.servo2_current
                    }
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get status: {e}',
                'response': "I had trouble checking my tracking status."
            }
            
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        if not self.is_initialized or not self.face_tracker:
            return {
                'initialized': False,
                'camera_available': False,
                'arduino_connected': False,
                'tracking_active': False,
                'face_encodings_loaded': 0,
                'error': 'System not initialized'
            }
            
        try:
            return {
                'initialized': True,
                'camera_available': self.face_tracker.camera is not None or self.face_tracker.camera_handler is not None,
                'arduino_connected': self.face_tracker.arduino is not None,
                'tracking_active': self.face_tracker.tracking_active,
                'face_encodings_loaded': len(self.face_tracker.known_face_names),
                'known_faces': self.face_tracker.known_face_names,
                'current_target': getattr(self.face_tracker, 'target_person', None),
                'servo_positions': {
                    'pan': self.face_tracker.servo1_current,
                    'tilt': self.face_tracker.servo2_current
                },
                'using_imx500': getattr(self.face_tracker, 'using_imx500', False)
            }
            
        except Exception as e:
            return {
                'initialized': True,
                'error': f'Status check failed: {e}'
            }
            
    def cleanup(self):
        """Clean up face tracking resources"""
        if self.face_tracker:
            try:
                self.face_tracker.cleanup()
            except:
                pass
            self.face_tracker = None
        self.is_initialized = False

# Example integration with main AI assistant
def integrate_with_main_ai(main_ai_instance):
    """
    Example function showing how to integrate with the main AI assistant
    This should be called from your main.py file
    """
    
    # Initialize face tracking integration
    face_integration = FaceTrackingIntegration(main_ai_instance)
    
    if not face_integration.initialize():
        print("⚠️ Face tracking integration failed to initialize")
        return None
        
    # Add to AI assistant's command processors
    def enhanced_command_processor(text):
        """Enhanced command processor that includes face tracking"""
        
        # First try face tracking commands
        face_result = face_integration.process_voice_command(text)
        if face_result:
            return face_result['response']
            
        # Fall back to original AI processing
        return main_ai_instance.original_process_command(text)
    
    # Replace or enhance the main AI's command processing
    main_ai_instance.face_tracking = face_integration
    main_ai_instance.enhanced_process_command = enhanced_command_processor
    
    print("✅ Face tracking integration completed!")
    return face_integration

if __name__ == "__main__":
    # Standalone testing
    print("🤖 Face Tracking Integration Test")
    print("=" * 40)
    
    integration = FaceTrackingIntegration()
    
    if integration.initialize():
        print("✅ Integration initialized successfully!")
        
        # Test voice commands
        test_commands = [
            "look at me",
            "look left", 
            "center your eyes",
            "who are you looking at",
            "stop tracking"
        ]
        
        for cmd in test_commands:
            print(f"\n🗣️ Testing command: '{cmd}'")
            result = integration.process_voice_command(cmd)
            if result:
                print(f"📝 Response: {result['response']}")
            else:
                print("❓ Command not recognized")
            time.sleep(2)
            
    else:
        print("❌ Integration failed to initialize")
        
    integration.cleanup() 