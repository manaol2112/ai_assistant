#!/usr/bin/env python3
"""
Enhanced Face Tracking Integration for AI Assistant
Integrates the intelligent face tracking system with priority recognition
for Sophia and Eladriel, automatic conversation mode tracking, and search behavior.

Voice Commands:
- "look at me" / "track my face" - Start intelligent face tracking
- "stop looking" / "stop tracking" - Stop face tracking  
- "look left/right/up/down" - Manual servo control
- "center your eyes" / "look forward" - Center servos
- "who are you looking at" - Get current tracking status
- "search for faces" - Start search behavior when no faces detected
"""

from intelligent_face_tracker import IntelligentFaceTracker, TrackingPriority
import threading
import time
import logging
from typing import Dict, Optional

class EnhancedFaceTrackingIntegration:
    """
    Enhanced integration class for intelligent face tracking with AI Assistant
    Handles voice commands, conversation mode integration, and priority tracking
    """
    
    def __init__(self, main_ai_assistant=None):
        self.ai_assistant = main_ai_assistant
        self.intelligent_tracker = None
        self.is_initialized = False
        
        # Setup logging
        self.logger = logging.getLogger('EnhancedFaceTrackingIntegration')
        
        # Voice command mappings
        self.voice_commands = {
            # Start tracking commands
            'start_tracking': [
                'look at me', 'track my face', 'follow me', 'watch me',
                'start face tracking', 'begin tracking', 'look for me',
                'track faces', 'start intelligent tracking'
            ],
            
            # Stop tracking commands  
            'stop_tracking': [
                'stop looking', 'stop tracking', 'stop following',
                'stop face tracking', 'look away', 'stop watching',
                'stop intelligent tracking'
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
            
            # Search commands
            'search_faces': [
                'search for faces', 'look for people', 'find faces',
                'scan for faces', 'search around'
            ],
            
            # Status commands
            'tracking_status': [
                'who are you looking at', 'who are you tracking',
                'what are you looking at', 'tracking status',
                'where are you looking'
            ]
        }
        
    def initialize(self, arduino_port='/dev/ttyUSB0', camera_index=0):
        """Initialize the enhanced face tracking system"""
        try:
            self.logger.info("🎯 Initializing Enhanced Face Tracking Integration...")
            
            # Initialize intelligent face tracker
            self.intelligent_tracker = IntelligentFaceTracker(
                arduino_port=arduino_port,
                camera_index=camera_index
            )
            
            # Initialize the tracker
            if not self.intelligent_tracker.initialize():
                self.logger.error("❌ Intelligent tracker initialization failed")
                return False
            
            self.is_initialized = True
            self.logger.info("✅ Enhanced Face Tracking Integration initialized successfully!")
            self.logger.info("🎯 Priority users: Sophia and Eladriel")
            self.logger.info("🔍 Intelligent search behavior enabled")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Enhanced face tracking initialization failed: {e}")
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
                
            elif command_type == 'search_faces':
                return self._start_search()
                
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
        """Start intelligent face tracking"""
        if not self.intelligent_tracker:
            return {
                'status': 'error', 
                'message': 'Intelligent tracker not initialized',
                'response': "I'm sorry, my intelligent tracking system isn't ready yet."
            }
            
        try:
            # Determine if we're in conversation mode
            conversation_mode = False
            if self.ai_assistant and hasattr(self.ai_assistant, 'current_user') and self.ai_assistant.current_user:
                conversation_mode = True
                
            self.intelligent_tracker.start_tracking(conversation_mode=conversation_mode)
            self.logger.info("🎯 Intelligent face tracking started via voice command")
            
            mode_text = "conversation mode" if conversation_mode else "general mode"
            return {
                'status': 'success',
                'message': f'Intelligent face tracking started in {mode_text}',
                'response': f"I'm now using my intelligent tracking system in {mode_text}! I'll prioritize Sophia and Eladriel, and search for faces when I don't see anyone."
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to start tracking: {e}',
                'response': "I had trouble starting my intelligent tracking system. Let me try to fix that."
            }
            
    def _stop_tracking(self) -> Dict:
        """Stop intelligent face tracking"""
        if not self.intelligent_tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized', 
                'response': "My intelligent tracking system isn't available right now."
            }
            
        try:
            self.intelligent_tracker.stop_tracking()
            self.logger.info("🛑 Intelligent face tracking stopped via voice command")
            
            return {
                'status': 'success',
                'message': 'Intelligent face tracking stopped',
                'response': "I've stopped intelligent tracking and returned to center position."
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to stop tracking: {e}',
                'response': "I had trouble stopping the intelligent tracking."
            }
            
    def _manual_look(self, direction: str) -> Dict:
        """Manual look command with intelligent tracking pause"""
        if not self.intelligent_tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            # Temporarily pause tracking for manual control
            was_tracking = self.intelligent_tracker.is_tracking
            if was_tracking:
                self.intelligent_tracker.stop_tracking()
            
            # Execute manual movement
            self.intelligent_tracker.manual_look(direction, amount=25)
            
            # Resume tracking if it was active
            if was_tracking:
                time.sleep(0.5)  # Brief pause
                conversation_mode = False
                if self.ai_assistant and hasattr(self.ai_assistant, 'current_user') and self.ai_assistant.current_user:
                    conversation_mode = True
                self.intelligent_tracker.start_tracking(conversation_mode=conversation_mode)
            
            self.logger.info(f"👁️ Manual look {direction} executed")
            
            return {
                'status': 'success',
                'message': f'Looked {direction}',
                'response': f"I'm now looking {direction}."
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Manual look failed: {e}',
                'response': f"I had trouble looking {direction}."
            }
            
    def _center_view(self) -> Dict:
        """Center view and pause tracking"""
        if not self.intelligent_tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            # Stop tracking and center
            self.intelligent_tracker.stop_tracking()
            self.logger.info("👁️ View centered via voice command")
            
            return {
                'status': 'success',
                'message': 'View centered',
                'response': "I'm now looking straight ahead in center position."
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Center view failed: {e}',
                'response': "I had trouble centering my view."
            }
            
    def _start_search(self) -> Dict:
        """Start search behavior manually"""
        if not self.intelligent_tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            # Start tracking which will activate search if no faces
            conversation_mode = False
            if self.ai_assistant and hasattr(self.ai_assistant, 'current_user') and self.ai_assistant.current_user:
                conversation_mode = True
                
            self.intelligent_tracker.start_tracking(conversation_mode=conversation_mode)
            
            # Force search behavior by resetting last detection time
            self.intelligent_tracker.last_detection_time = 0
            
            self.logger.info("🔍 Manual search behavior activated")
            
            return {
                'status': 'success',
                'message': 'Search behavior started',
                'response': "I'm now searching for faces by looking left, right, and up. I'll track anyone I find!"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Search start failed: {e}',
                'response': "I had trouble starting my search behavior."
            }
            
    def _get_tracking_status(self) -> Dict:
        """Get current tracking status"""
        if not self.intelligent_tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            status = self.intelligent_tracker.get_tracking_status()
            
            if not status['tracking_active']:
                response = "I'm not currently tracking any faces. I'm looking straight ahead."
            elif status['search_active']:
                response = "I'm searching for faces by looking around slowly."
            elif status['conversation_mode'] and status['current_target']:
                response = f"I'm in conversation mode, prioritizing {status['current_target'].title()}."
            else:
                response = "I'm tracking faces with priority for Sophia and Eladriel."
            
            return {
                'status': 'success',
                'message': 'Status retrieved',
                'response': response,
                'data': status
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Status check failed: {e}',
                'response': "I had trouble checking my tracking status."
            }
    
    def enable_conversation_mode(self, user: str):
        """Enable conversation mode tracking for specific user"""
        if not self.is_initialized or not self.intelligent_tracker:
            return
            
        try:
            # Set conversation mode with the specific user
            self.intelligent_tracker.set_conversation_mode(True, user)
            
            # Start tracking if not already active
            if not self.intelligent_tracker.is_tracking:
                self.intelligent_tracker.start_tracking(conversation_mode=True)
                
            self.logger.info(f"💬 Conversation mode enabled for {user}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to enable conversation mode: {e}")
    
    def disable_conversation_mode(self):
        """Disable conversation mode tracking"""
        if not self.is_initialized or not self.intelligent_tracker:
            return
            
        try:
            self.intelligent_tracker.set_conversation_mode(False)
            self.logger.info("💬 Conversation mode disabled")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to disable conversation mode: {e}")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        if not self.is_initialized:
            return {
                'initialized': False,
                'error': 'System not initialized'
            }
            
        try:
            tracker_status = self.intelligent_tracker.get_tracking_status()
            
            return {
                'initialized': True,
                'intelligent_tracking': tracker_status,
                'voice_commands_available': len(sum(self.voice_commands.values(), [])),
                'priority_users': ['sophia', 'eladriel'],
                'features': [
                    'Priority face tracking',
                    'Conversation mode integration', 
                    'Intelligent search behavior',
                    'Smooth servo movements',
                    'Voice command control'
                ]
            }
            
        except Exception as e:
            return {
                'initialized': True,
                'error': f'Status error: {e}'
            }
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.intelligent_tracker:
                self.intelligent_tracker.cleanup()
            self.is_initialized = False
            self.logger.info("🧹 Enhanced Face Tracking Integration cleaned up")
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup error: {e}")

# Integration function for main AI system
def integrate_enhanced_face_tracking(main_ai_instance):
    """
    Enhanced integration function for main AI system
    Replaces the old face tracking with intelligent tracking
    """
    print("🎯 Integrating Enhanced Face Tracking with AI Assistant...")
    
    # Create enhanced face tracking integration
    enhanced_integration = EnhancedFaceTrackingIntegration(main_ai_instance)
    
    # Initialize the system
    if enhanced_integration.initialize():
        print("✅ Enhanced Face Tracking integrated successfully!")
        
        # Add to main AI system
        main_ai_instance.enhanced_face_tracking = enhanced_integration
        
        # Hook into conversation mode
        original_handle_automatic_conversation = main_ai_instance.handle_automatic_conversation
        
        def enhanced_handle_automatic_conversation(user: str):
            """Enhanced conversation handler with intelligent tracking"""
            # Enable conversation mode tracking
            enhanced_integration.enable_conversation_mode(user)
            
            try:
                # Call original conversation handler
                result = original_handle_automatic_conversation(user)
                return result
            finally:
                # Disable conversation mode when done
                enhanced_integration.disable_conversation_mode()
        
        # Replace the method
        main_ai_instance.handle_automatic_conversation = enhanced_handle_automatic_conversation
        
        # Enhanced command processor that includes face tracking
        original_command_processor = getattr(main_ai_instance, 'handle_special_commands', None)
        
        def enhanced_command_processor(text, user):
            """Enhanced command processor with face tracking commands"""
            # First check for face tracking commands
            face_tracking_result = enhanced_integration.process_voice_command(text)
            
            if face_tracking_result:
                return face_tracking_result.get('response', 'Face tracking command processed.')
            
            # Fall back to original command processor
            if original_command_processor:
                return original_command_processor(text, user)
            
            return None
        
        # Add enhanced command processor
        main_ai_instance.enhanced_command_processor = enhanced_command_processor
        
        print("🎯 Enhanced face tracking commands available:")
        print("   • 'Look at me' - Start intelligent tracking")
        print("   • 'Stop looking' - Stop tracking") 
        print("   • 'Search for faces' - Start search behavior")
        print("   • 'Who are you looking at?' - Get status")
        print("   • Manual direction commands: left, right, up, down")
        print("🎭 Features enabled:")
        print("   • Priority tracking for Sophia and Eladriel")
        print("   • Automatic conversation mode tracking")
        print("   • Intelligent search when no faces detected")
        print("   • Smooth servo movements with prediction")
        
        return enhanced_integration
        
    else:
        print("❌ Enhanced Face Tracking integration failed")
        return None

if __name__ == "__main__":
    # Test the enhanced integration
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Face Tracking Integration Test')
    parser.add_argument('--arduino-port', default='/dev/ttyUSB0', help='Arduino port')
    parser.add_argument('--camera-index', type=int, default=0, help='Camera index')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    print("🎯 ENHANCED FACE TRACKING INTEGRATION TEST")
    print("=" * 60)
    
    try:
        integration = EnhancedFaceTrackingIntegration()
        
        if integration.initialize(args.arduino_port, args.camera_index):
            print("✅ Integration initialized successfully!")
            
            # Test voice commands
            test_commands = [
                "look at me",
                "who are you looking at",
                "search for faces", 
                "look left",
                "center your eyes",
                "stop tracking"
            ]
            
            for command in test_commands:
                print(f"\n🎤 Testing command: '{command}'")
                result = integration.process_voice_command(command)
                if result:
                    print(f"   ✅ {result.get('response', 'Command processed')}")
                else:
                    print(f"   ❌ Command not recognized")
                time.sleep(2)
            
            print("\n✅ All tests completed!")
            integration.cleanup()
            
        else:
            print("❌ Integration initialization failed")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 