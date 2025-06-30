#!/usr/bin/env python3
"""
REAL-TIME Enhanced Face Tracking Integration for AI Assistant
Ultra-responsive integration with continuous conversation tracking

Features:
- Real-time face tracking (60+ FPS) with sub-second response times
- Continuous tracking during all conversation stages (listening, processing, responding)
- Priority tracking for Sophia and Eladriel
- Voice command integration with enhanced responsiveness
- Conversation stage awareness for optimal tracking
- Performance-optimized detection pipeline
"""

import logging
import time
from typing import Optional, Dict
import threading

# Import the real-time intelligent tracker
from intelligent_face_tracker import RealTimeIntelligentFaceTracker, ConversationStage

class RealTimeEnhancedFaceTrackingIntegration:
    """REAL-TIME Enhanced face tracking integration with conversation stage management"""
    
    def __init__(self, arduino_port: str = '/dev/ttyUSB0', camera_index: int = 0):
        self.logger = logging.getLogger('RealTimeEnhancedFaceTrackingIntegration')
        
        # Initialize real-time intelligent tracker in headless mode (no camera display)
        self.intelligent_tracker = RealTimeIntelligentFaceTracker(arduino_port, camera_index, headless=True)
        
        # Integration state
        self.is_integrated = False
        self.conversation_active = False
        self.current_user = None
        self.last_command_time = 0
        
        # Performance monitoring
        self.command_response_times = []
        
        # Priority users for enhanced tracking
        self.priority_users = {'sophia', 'eladriel'}
        
    def initialize(self) -> bool:
        """Initialize the real-time face tracking integration"""
        try:
            self.logger.info("🚀 Initializing REAL-TIME Enhanced Face Tracking Integration...")
            
            # Initialize the intelligent tracker
            if not self.intelligent_tracker.initialize():
                self.logger.error("❌ Failed to initialize real-time intelligent tracker")
                return False
                
            self.is_integrated = True
            
            self.logger.info("✅ REAL-TIME Enhanced Face Tracking Integration initialized!")
            self.logger.info("🎯 Available Commands:")
            self.logger.info("   - 'look at me' / 'track my face'")
            self.logger.info("   - 'stop looking' / 'stop tracking'") 
            self.logger.info("   - 'who are you looking at'")
            self.logger.info("   - 'search for faces'")
            self.logger.info("   - 'look left/right/up/down'")
            self.logger.info("   - 'center your eyes'")
            self.logger.info("🌟 FEATURES ENABLED:")
            self.logger.info("   ⚡ Real-time tracking (60+ FPS)")
            self.logger.info("   🎯 Priority tracking for Sophia and Eladriel")
            self.logger.info("   💬 Continuous conversation mode tracking")
            self.logger.info("   🔍 Intelligent search behavior")
            self.logger.info("   📊 Performance monitoring")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Integration initialization failed: {e}")
            return False
            
    def process_voice_command(self, command: str, user_name: str = None) -> str:
        """Process voice commands with enhanced real-time response"""
        start_time = time.time()
        
        if not self.is_integrated:
            return "Face tracking system not initialized."
        
        try:
            # Store user context for conversation mode
            if user_name:
                self.current_user = user_name.lower()
            
            # Process command with real-time tracker
            response = self.intelligent_tracker.process_voice_command(command)
            
            # Enhanced responses for priority users
            if self.current_user in self.priority_users:
                if 'look at me' in command.lower():
                    response = f"Of course, {user_name}! I'm now tracking you with priority."
                elif 'who are you looking at' in command.lower():
                    response = f"I'm looking at you, {user_name}! You have my full attention."
            
            # Track response time for performance monitoring
            response_time = time.time() - start_time
            self.command_response_times.append(response_time)
            
            # Keep only last 10 response times
            if len(self.command_response_times) > 10:
                self.command_response_times.pop(0)
            
            # Log performance for fast responses
            if response_time < 0.2:
                self.logger.debug(f"⚡ ULTRA-FAST response: {response_time:.3f}s")
            elif response_time < 0.5:
                self.logger.debug(f"✅ Fast response: {response_time:.3f}s")
            else:
                self.logger.warning(f"⚠️ Slow response: {response_time:.3f}s")
            
            self.last_command_time = time.time()
            return response
                
        except Exception as e:
            self.logger.error(f"❌ Error processing voice command: {e}")
            return "Sorry, I couldn't process that face tracking command."
    
    def enable_conversation_mode(self, user_name: str = None) -> bool:
        """Enable continuous conversation mode with real-time tracking"""
        try:
            if not self.is_integrated:
                self.logger.warning("⚠️ Integration not initialized - cannot enable conversation mode")
                return False
            
            self.conversation_active = True
            self.current_user = user_name.lower() if user_name else None
            
            # Start real-time conversation tracking
            self.intelligent_tracker.set_conversation_mode(True, self.current_user)
            
            if not self.intelligent_tracker.is_tracking:
                self.intelligent_tracker.start_tracking(conversation_mode=True)
            
            # Set initial conversation stage
            self.intelligent_tracker.set_conversation_stage(ConversationStage.LISTENING)
            
            user_info = f" for {user_name}" if user_name else ""
            self.logger.info(f"💬 REAL-TIME conversation mode enabled{user_info}")
            self.logger.info("🎯 Continuous tracking active during all conversation stages")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error enabling conversation mode: {e}")
            return False
    
    def disable_conversation_mode(self) -> bool:
        """Disable conversation mode while maintaining tracking"""
        try:
            self.conversation_active = False
            
            # Disable conversation mode in tracker
            self.intelligent_tracker.set_conversation_mode(False)
            self.intelligent_tracker.set_conversation_stage(ConversationStage.IDLE)
            
            self.logger.info("💬 REAL-TIME conversation mode disabled")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error disabling conversation mode: {e}")
            return False
    
    def set_conversation_stage(self, stage: str) -> bool:
        """Update conversation stage for continuous tracking optimization"""
        try:
            # Map string stages to enum
            stage_mapping = {
                'listening': ConversationStage.LISTENING,
                'processing': ConversationStage.PROCESSING,
                'responding': ConversationStage.RESPONDING,
                'idle': ConversationStage.IDLE
            }
            
            conversation_stage = stage_mapping.get(stage.lower())
            if conversation_stage:
                self.intelligent_tracker.set_conversation_stage(conversation_stage)
                
                # Enhanced logging for stage transitions
                stage_emojis = {
                    'listening': '👂',
                    'processing': '🧠',
                    'responding': '🗣️',
                    'idle': '😴'
                }
                emoji = stage_emojis.get(stage.lower(), '🎯')
                self.logger.debug(f"{emoji} Conversation stage: {stage}")
                
                return True
            else:
                self.logger.warning(f"⚠️ Unknown conversation stage: {stage}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error setting conversation stage: {e}")
            return False
    
    def start_tracking(self, conversation_mode: bool = False) -> bool:
        """Start real-time intelligent face tracking"""
        try:
            if not self.is_integrated:
                return False
            
            self.intelligent_tracker.start_tracking(conversation_mode)
            self.logger.info("🚀 REAL-TIME face tracking started")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error starting tracking: {e}")
            return False
    
    def stop_tracking(self) -> bool:
        """Stop face tracking"""
        try:
            self.intelligent_tracker.stop_tracking()
            self.conversation_active = False
            self.logger.info("🛑 REAL-TIME face tracking stopped")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping tracking: {e}")
            return False
    
    def get_tracking_status(self) -> Dict:
        """Get comprehensive tracking status with performance metrics"""
        try:
            base_status = self.intelligent_tracker.get_status()
            
            # Add integration-specific information
            integration_status = {
                'integration_active': self.is_integrated,
                'conversation_active': self.conversation_active,
                'current_user': self.current_user,
                'priority_users': list(self.priority_users),
                'last_command_time': self.last_command_time,
                'performance': {
                    'avg_response_time': sum(self.command_response_times) / len(self.command_response_times) if self.command_response_times else 0,
                    'min_response_time': min(self.command_response_times) if self.command_response_times else 0,
                    'max_response_time': max(self.command_response_times) if self.command_response_times else 0,
                    'ultra_fast_responses': len([t for t in self.command_response_times if t < 0.2]),
                    'fast_responses': len([t for t in self.command_response_times if 0.2 <= t < 0.5]),
                    'slow_responses': len([t for t in self.command_response_times if t >= 0.5])
                }
            }
            
            # Merge statuses
            full_status = {**base_status, **integration_status}
            
            return full_status
            
        except Exception as e:
            self.logger.error(f"❌ Error getting tracking status: {e}")
            return {'error': str(e)}
    
    def get_performance_metrics(self) -> Dict:
        """Get detailed performance metrics"""
        if not self.command_response_times:
            return {'message': 'No performance data available yet'}
        
        total_responses = len(self.command_response_times)
        avg_time = sum(self.command_response_times) / total_responses
        ultra_fast = len([t for t in self.command_response_times if t < 0.2])
        fast = len([t for t in self.command_response_times if 0.2 <= t < 0.5])
        slow = len([t for t in self.command_response_times if t >= 0.5])
        
        return {
            'total_commands': total_responses,
            'average_response_time': f"{avg_time:.3f}s",
            'ultra_fast_responses': f"{ultra_fast} ({ultra_fast/total_responses*100:.1f}%)",
            'fast_responses': f"{fast} ({fast/total_responses*100:.1f}%)",
            'slow_responses': f"{slow} ({slow/total_responses*100:.1f}%)",
            'performance_rating': '⚡ EXCELLENT' if avg_time < 0.2 else '✅ GOOD' if avg_time < 0.5 else '⚠️ NEEDS OPTIMIZATION'
        }
            
    def cleanup(self):
        """Clean up integration resources"""
        try:
            self.logger.info("🧹 Cleaning up REAL-TIME Enhanced Face Tracking Integration...")
            
            self.conversation_active = False
            self.is_integrated = False

            # Clean up intelligent tracker
            if self.intelligent_tracker:
                self.intelligent_tracker.cleanup()
            
            self.logger.info("🧹 REAL-TIME integration cleanup completed")
            
        except Exception as e:
            self.logger.error(f"❌ Error during cleanup: {e}")

# Convenience function for main AI integration
def create_enhanced_face_tracking_integration(arduino_port='/dev/ttyUSB0', camera_index=0) -> RealTimeEnhancedFaceTrackingIntegration:
    """Create and initialize the real-time enhanced face tracking integration"""
    integration = RealTimeEnhancedFaceTrackingIntegration(arduino_port, camera_index)
    
    if integration.initialize():
        return integration
    else:
        raise Exception("Failed to initialize REAL-TIME Enhanced Face Tracking Integration")
        
# Integration function for main AI system
def integrate_enhanced_face_tracking(ai_assistant, arduino_port='/dev/ttyUSB0', camera_index=0):
    """Integrate enhanced face tracking with the main AI assistant"""
    try:
        # Create the enhanced face tracking integration
        integration = RealTimeEnhancedFaceTrackingIntegration(arduino_port, camera_index)
        
        if integration.initialize():
            # Add to AI assistant
            ai_assistant.enhanced_face_tracking = integration
            
            # Enable conversation mode hooks
            def enable_tracking_conversation_mode(user_name):
                if ai_assistant.enhanced_face_tracking:
                    ai_assistant.enhanced_face_tracking.enable_conversation_mode(user_name)
            
            def disable_tracking_conversation_mode():
                if ai_assistant.enhanced_face_tracking:
                    ai_assistant.enhanced_face_tracking.disable_conversation_mode()
            
            def set_tracking_conversation_stage(stage):
                if ai_assistant.enhanced_face_tracking:
                    ai_assistant.enhanced_face_tracking.set_conversation_stage(stage)
            
            # Add methods to AI assistant
            ai_assistant.enable_face_tracking_conversation = enable_tracking_conversation_mode
            ai_assistant.disable_face_tracking_conversation = disable_tracking_conversation_mode
            ai_assistant.set_face_tracking_stage = set_tracking_conversation_stage
            
            print("✅ Enhanced Face Tracking integrated with AI Assistant")
            print("🎯 Features enabled: Priority tracking, conversation mode, real-time performance")
            
            return integration
        else:
            print("❌ Failed to initialize enhanced face tracking")
            return None
            
    except Exception as e:
        print(f"❌ Integration error: {e}")
        return None

if __name__ == "__main__":
    # Test the real-time enhanced integration
    import argparse
    
    parser = argparse.ArgumentParser(description='REAL-TIME Enhanced Face Tracking Integration Test')
    parser.add_argument('--arduino-port', default='/dev/ttyUSB0', help='Arduino port')
    parser.add_argument('--camera-index', type=int, default=0, help='Camera index')
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 REAL-TIME Enhanced Face Tracking Integration Test")
    print("=" * 60)
    
    try:
        # Initialize integration
        integration = RealTimeEnhancedFaceTrackingIntegration(args.arduino_port, args.camera_index)
    
        if not integration.initialize():
            print("❌ Failed to initialize integration")
            exit(1)
        
        print("✅ REAL-TIME integration initialized successfully!")
        
        # Test voice commands with performance monitoring
        test_commands = [
            ("look at me", "Sophia"),
            ("who are you looking at", "Sophia"),
            ("search for faces", None),
            ("look left", "Eladriel"),
            ("center your eyes", "Eladriel"),
            ("stop tracking", None)
        ]
        
        print("\n🎤 Testing voice commands with performance monitoring:")
        for command, user in test_commands:
            start_time = time.time()
            response = integration.process_voice_command(command, user)
            response_time = time.time() - start_time
            
            status = "⚡" if response_time < 0.2 else "✅" if response_time < 0.5 else "⚠️"
            print(f"{status} [{response_time:.3f}s] User: {user or 'None'}, Command: '{command}' -> '{response}'")
            
            time.sleep(0.5)
        
        # Test conversation mode with stage management
        print("\n💬 Testing conversation mode with continuous tracking:")
        integration.enable_conversation_mode("Sophia")
        
        # Simulate conversation stages
        conversation_stages = ['listening', 'processing', 'responding', 'idle']
        
        for stage in conversation_stages:
            print(f"Setting conversation stage: {stage}")
            integration.set_conversation_stage(stage)
            time.sleep(1)
        
        # Get performance metrics
        print("\n📊 Performance Metrics:")
        metrics = integration.get_performance_metrics()
        for key, value in metrics.items():
            print(f"   {key}: {value}")
        
        # Get full status
        print("\n📈 Full Status:")
        status = integration.get_tracking_status()
        for key, value in status.items():
            if key != 'performance':
                print(f"   {key}: {value}")
        
        print("\n⚡ Real-time tracking test for 5 seconds...")
        time.sleep(5)
        
        print("✅ REAL-TIME Enhanced Integration Test Completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'integration' in locals():
            integration.cleanup() 
        print("🧹 Test cleanup completed")