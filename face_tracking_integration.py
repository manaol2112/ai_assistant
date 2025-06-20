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

from face_tracking_servo_controller import FaceTrackingServoController
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
            self.face_tracker = FaceTrackingServoController(
                arduino_port=arduino_port,
                camera_index=camera_index,
                tracking_smoothness=0.2,  # Smooth tracking
                face_confidence_threshold=0.5  # More lenient for better tracking
            )
            
            # Check if initialization was successful
            status = self.face_tracker.get_status()
            if not status['arduino_connected']:
                self.logger.error("❌ Arduino not connected")
                return False
                
            if not status['camera_available']:
                self.logger.error("❌ Camera not available") 
                return False
                
            if status['face_encodings_loaded'] == 0:
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
            self.face_tracker.start_tracking()
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
            self.face_tracker.stop_tracking()
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
        """Manual servo control for looking in directions"""
        if not self.face_tracker:
            return {
                'status': 'error',
                'message': 'Face tracker not initialized',
                'response': "I can't move my eyes right now."
            }
            
        try:
            # Stop tracking first for manual control
            was_tracking = self.face_tracker.is_tracking
            if was_tracking:
                self.face_tracker.stop_tracking()
                time.sleep(0.5)
            
            # Calculate servo positions based on direction
            servo1_angle = self.face_tracker.servo1_current
            servo2_angle = self.face_tracker.servo2_current
            
            if direction == 'left':
                servo1_angle = 45  # Look left
                response = "Looking to my left."
            elif direction == 'right':
                servo1_angle = 135  # Look right
                response = "Looking to my right."
            elif direction == 'up':
                servo2_angle = 60   # Look up
                response = "Looking up."
            elif direction == 'down':
                servo2_angle = 120  # Look down  
                response = "Looking down."
            else:
                response = "I'm not sure which direction you meant."
                
            # Send command
            self.face_tracker.manual_servo_control(servo1_angle, servo2_angle)
            self.logger.info(f"👁️ Manual look command: {direction}")
            
            return {
                'status': 'success',
                'message': f'Looking {direction}',
                'response': response
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to look {direction}: {e}',
                'response': f"I had trouble looking {direction}."
            }
            
    def _center_view(self) -> Dict:
        """Center the servo view"""
        if not self.face_tracker:
            return {
                'status': 'error',
                'message': 'Face tracker not initialized',
                'response': "I can't center my view right now."
            }
            
        try:
            # Stop tracking for manual control
            was_tracking = self.face_tracker.is_tracking
            if was_tracking:
                self.face_tracker.stop_tracking()
                time.sleep(0.5)
                
            # Center servos
            self.face_tracker.manual_servo_control(90, 90)
            self.logger.info("🎯 Centered view via voice command")
            
            return {
                'status': 'success',
                'message': 'View centered',
                'response': "I'm now looking straight ahead with my eyes centered."
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
                'response': "My face tracking system isn't available."
            }
            
        try:
            status = self.face_tracker.get_status()
            
            if status['is_tracking']:
                if status['current_target']:
                    response = f"I'm currently tracking {status['current_target']}'s face."
                else:
                    response = "I'm looking for familiar faces but don't see anyone I recognize right now."
            else:
                response = "I'm not currently tracking any faces. My eyes are in manual mode."
                
            servo_pos = f"My eyes are positioned at ({status['servo1_position']}, {status['servo2_position']})"
            
            return {
                'status': 'success',
                'message': f"Tracking: {status['is_tracking']}, Target: {status['current_target']}",
                'response': f"{response} {servo_pos}."
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get status: {e}',
                'response': "I can't check my tracking status right now."
            }
            
    def get_system_status(self) -> Dict:
        """Get overall system status"""
        if not self.is_initialized or not self.face_tracker:
            return {
                'initialized': False,
                'available': False,
                'message': 'Face tracking not initialized'
            }
            
        status = self.face_tracker.get_status()
        return {
            'initialized': True,
            'available': status['arduino_connected'] and status['camera_available'],
            'tracking_active': status['is_tracking'],
            'current_target': status['current_target'],
            'face_encodings': status['face_encodings_loaded'],
            'servo_position': (status['servo1_position'], status['servo2_position']),
            'target_people': status['target_people']
        }
        
    def cleanup(self):
        """Cleanup face tracking resources"""
        if self.face_tracker:
            self.face_tracker.cleanup()
            self.logger.info("🧹 Face tracking integration cleanup completed")

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