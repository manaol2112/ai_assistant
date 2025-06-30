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
    
    def __init__(self, arduino_port: str = '/dev/ttyUSB0', camera_index: int = 0):
        """Initialize enhanced face tracking integration with real-time optimizations"""
        self.logger = logging.getLogger(__name__)
        self.arduino_port = arduino_port
        self.camera_index = camera_index
        
        # Initialize optimized intelligent tracker
        self.tracker = IntelligentFaceTracker(arduino_port, camera_index)
        
        # Integration state
        self.active = False
        self.conversation_mode_active = False
        
        # Performance tracking
        self.command_response_times = []
        self.last_command_time = 0
        
        # Enhanced voice commands with faster response
        self.voice_commands = {
            # Primary tracking commands - fastest response
            'look at me': self._start_tracking,
            'track my face': self._start_tracking,
            'follow me': self._start_tracking,
            
            # Stop commands - immediate response
            'stop looking': self._stop_tracking,
            'stop tracking': self._stop_tracking,
            'stop following': self._stop_tracking,
            
            # Status commands - instant feedback
            'who are you looking at': self._get_tracking_status,
            'tracking status': self._get_tracking_status,
            
            # Search commands - fast activation
            'search for faces': self._search_for_faces,
            'find faces': self._search_for_faces,
            'look for people': self._search_for_faces,
            
            # Manual control - responsive movement
            'look left': lambda: self._manual_control('left'),
            'look right': lambda: self._manual_control('right'),
            'look up': lambda: self._manual_control('up'),
            'look down': lambda: self._manual_control('down'),
            'center your eyes': self._center_view,
            'look at center': self._center_view,
        }

    def initialize(self) -> bool:
        """Initialize the optimized face tracking system"""
        try:
            self.logger.info("⚡ Initializing Enhanced Face Tracking Integration with real-time optimizations...")
            
            # Initialize with performance optimizations
            if not self.tracker.initialize():
                self.logger.error("❌ Failed to initialize optimized tracker")
                return False
            
            self.active = True
            self.logger.info("✅ Enhanced Face Tracking Integration ready for real-time operation!")
            
            # Log optimized features
            self.logger.info("🚀 Real-time features enabled:")
            self.logger.info("  • 30 FPS tracking with frame skipping")
            self.logger.info("  • Sub-second voice command response")
            self.logger.info("  • Predictive face tracking")
            self.logger.info("  • Priority tracking for Sophia and Eladriel")
            self.logger.info("  • Optimized search patterns")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Integration initialization failed: {e}")
            return False

    def process_voice_command(self, command: str) -> str:
        """Process voice commands with optimized response times"""
        if not self.active:
            return "❌ Face tracking system not active"
        
        command_start = time.time()
        command = command.lower().strip()
        
        # Fast command lookup
        for cmd_phrase, cmd_function in self.voice_commands.items():
            if cmd_phrase in command:
                try:
                    response = cmd_function()
                    
                    # Track response time for performance monitoring
                    response_time = time.time() - command_start
                    self.command_response_times.append(response_time)
                    self.last_command_time = time.time()
                    
                    if len(self.command_response_times) > 50:  # Keep last 50 measurements
                        self.command_response_times.pop(0)
                    
                    # Log performance for very fast commands
                    if response_time < 0.1:
                        self.logger.debug(f"⚡ Ultra-fast command response: {response_time:.3f}s")
                    
                    return response
                    
                except Exception as e:
                    self.logger.error(f"❌ Command execution error: {e}")
                    return f"❌ Error executing command: {str(e)}"
        
        return f"❓ Unknown face tracking command: {command}"

    def _start_tracking(self) -> str:
        """Start optimized real-time face tracking"""
        try:
            if self.tracker.start_tracking():
                self.logger.info("🎯 Real-time face tracking activated!")
                return "✅ Real-time face tracking started! I'm now tracking faces with optimized performance."
            else:
                return "❌ Failed to start tracking"
        except Exception as e:
            self.logger.error(f"❌ Error starting tracking: {e}")
            return f"❌ Error starting tracking: {str(e)}"

    def _stop_tracking(self) -> str:
        """Stop face tracking with quick response"""
        try:
            if self.tracker.stop_tracking():
                self.logger.info("🛑 Face tracking stopped")
                return "✅ Face tracking stopped. Returning to center position."
            else:
                return "❌ Failed to stop tracking"
        except Exception as e:
            self.logger.error(f"❌ Error stopping tracking: {e}")
            return f"❌ Error stopping tracking: {str(e)}"

    def enable_conversation_mode(self, target_user: str = None) -> bool:
        """Enable optimized conversation mode tracking"""
        try:
            self.logger.info(f"💬 Enabling optimized conversation mode for {target_user or 'detected user'}")
            
            # Set conversation mode with priority user
            self.tracker.set_conversation_mode(True, target_user)
            
            # Start tracking with priority if not already active
            if not self.tracker.tracking_active:
                priority_user = target_user if target_user in ['sophia', 'eladriel'] else None
                self.tracker.start_tracking(priority_user)
            
            self.conversation_mode_active = True
            self.logger.info("✅ Optimized conversation mode tracking activated")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error enabling conversation mode: {e}")
            return False

    def disable_conversation_mode(self) -> bool:
        """Disable conversation mode tracking"""
        try:
            self.logger.info("💬 Disabling conversation mode tracking")
            
            self.tracker.set_conversation_mode(False)
            self.conversation_mode_active = False
            
            self.logger.info("✅ Conversation mode tracking disabled")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error disabling conversation mode: {e}")
            return False

    def get_performance_stats(self) -> dict:
        """Get real-time performance statistics"""
        if not self.command_response_times:
            return {"status": "No performance data available"}
        
        avg_response = sum(self.command_response_times) / len(self.command_response_times)
        max_response = max(self.command_response_times)
        min_response = min(self.command_response_times)
        
        return {
            "average_response_time": f"{avg_response:.3f}s",
            "fastest_response": f"{min_response:.3f}s",
            "slowest_response": f"{max_response:.3f}s",
            "total_commands": len(self.command_response_times),
            "tracking_active": self.tracker.tracking_active,
            "conversation_mode": self.conversation_mode_active,
            "target_fps": 30,
            "optimization_level": "Real-time"
        }

    def _center_view(self) -> Dict:
        """Center view and pause tracking"""
        if not self.tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            # Stop tracking and center
            self.tracker.stop_tracking()
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
            
    def _search_for_faces(self) -> Dict:
        """Start search behavior manually"""
        if not self.tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            # Start tracking which will activate search if no faces
            conversation_mode = False
            if self.tracker.conversation_mode:
                conversation_mode = True
                
            self.tracker.start_tracking(conversation_mode=conversation_mode)
            
            # Force search behavior by resetting last detection time
            self.tracker.last_detection_time = 0
            
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
        if not self.tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            status = self.tracker.get_tracking_status()
            
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
            
    def _manual_control(self, direction: str) -> Dict:
        """Manual look command with intelligent tracking pause"""
        if not self.tracker:
            return {
                'status': 'error',
                'message': 'Intelligent tracker not initialized',
                'response': "My tracking system isn't available right now."
            }
            
        try:
            # Temporarily pause tracking for manual control
            was_tracking = self.tracker.is_tracking
            if was_tracking:
                self.tracker.stop_tracking()
            
            # Execute manual movement
            self.tracker.manual_look(direction, amount=25)
            
            # Resume tracking if it was active
            if was_tracking:
                time.sleep(0.5)  # Brief pause
                conversation_mode = False
                if self.tracker.conversation_mode:
                    conversation_mode = True
                self.tracker.start_tracking(conversation_mode=conversation_mode)
            
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

# Integration function for main AI system
def integrate_enhanced_face_tracking(main_ai_instance):
    """
    Enhanced integration function for main AI system
    Replaces the old face tracking with intelligent tracking
    """
    print("🎯 Integrating Enhanced Face Tracking with AI Assistant...")
    
    # Create enhanced face tracking integration
    enhanced_integration = EnhancedFaceTrackingIntegration()
    
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
        integration = EnhancedFaceTrackingIntegration(args.arduino_port, args.camera_index)
        
        if integration.initialize():
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
                print(f"   ✅ {result}")
            else:
                print(f"   ❌ Command not recognized")
            time.sleep(2)
        
        print("\n✅ All tests completed!")
        print("🎯 Performance statistics:")
        print(integration.get_performance_stats())
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 