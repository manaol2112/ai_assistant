"""
Visual Feedback Configuration
Settings for different robot displays and environments
"""

import os
from typing import Dict, Any


class VisualConfig:
    """Configuration settings for visual feedback system."""
    
    # Display Settings
    DISPLAY_WIDTH = int(os.getenv('ROBOT_DISPLAY_WIDTH', '800'))
    DISPLAY_HEIGHT = int(os.getenv('ROBOT_DISPLAY_HEIGHT', '480'))
    FULLSCREEN = os.getenv('ROBOT_FULLSCREEN', 'False').lower() == 'true'
    
    # Visual Feedback Mode
    USE_GUI = os.getenv('ROBOT_USE_GUI', 'True').lower() == 'true'
    
    # Animation Settings
    ANIMATION_FPS = int(os.getenv('ROBOT_ANIMATION_FPS', '10'))
    ENABLE_ANIMATIONS = os.getenv('ROBOT_ANIMATIONS', 'True').lower() == 'true'
    
    # Face Customization
    FACE_SIZE = int(os.getenv('ROBOT_FACE_SIZE', '120'))
    
    # Colors for different states (can be overridden via environment)
    COLORS = {
        'standby': {
            'face': os.getenv('ROBOT_COLOR_STANDBY_FACE', '#E8F4FD'),
            'eyes': os.getenv('ROBOT_COLOR_STANDBY_EYES', '#4A90E2'),
            'mouth': os.getenv('ROBOT_COLOR_STANDBY_MOUTH', '#666666')
        },
        'listening': {
            'face': os.getenv('ROBOT_COLOR_LISTENING_FACE', '#E8F8F5'),
            'eyes': os.getenv('ROBOT_COLOR_LISTENING_EYES', '#00C853'),
            'mouth': os.getenv('ROBOT_COLOR_LISTENING_MOUTH', '#4CAF50')
        },
        'speaking': {
            'face': os.getenv('ROBOT_COLOR_SPEAKING_FACE', '#FFF3E0'),
            'eyes': os.getenv('ROBOT_COLOR_SPEAKING_EYES', '#FF9800'),
            'mouth': os.getenv('ROBOT_COLOR_SPEAKING_MOUTH', '#F57C00')
        },
        'thinking': {
            'face': os.getenv('ROBOT_COLOR_THINKING_FACE', '#F3E5F5'),
            'eyes': os.getenv('ROBOT_COLOR_THINKING_EYES', '#9C27B0'),
            'mouth': os.getenv('ROBOT_COLOR_THINKING_MOUTH', '#7B1FA2')
        },
        'happy': {
            'face': os.getenv('ROBOT_COLOR_HAPPY_FACE', '#E8F5E8'),
            'eyes': os.getenv('ROBOT_COLOR_HAPPY_EYES', '#4CAF50'),
            'mouth': os.getenv('ROBOT_COLOR_HAPPY_MOUTH', '#2E7D32')
        },
        'error': {
            'face': os.getenv('ROBOT_COLOR_ERROR_FACE', '#FFEBEE'),
            'eyes': os.getenv('ROBOT_COLOR_ERROR_EYES', '#F44336'),
            'mouth': os.getenv('ROBOT_COLOR_ERROR_MOUTH', '#C62828')
        },
        'sleeping': {
            'face': os.getenv('ROBOT_COLOR_SLEEPING_FACE', '#F5F5F5'),
            'eyes': os.getenv('ROBOT_COLOR_SLEEPING_EYES', '#9E9E9E'),
            'mouth': os.getenv('ROBOT_COLOR_SLEEPING_MOUTH', '#757575')
        }
    }
    
    # Status Messages
    MESSAGES = {
        'standby': os.getenv('ROBOT_MSG_STANDBY', 'Ready to help!'),
        'listening': os.getenv('ROBOT_MSG_LISTENING', "I'm listening..."),
        'speaking': os.getenv('ROBOT_MSG_SPEAKING', 'Speaking...'),
        'thinking': os.getenv('ROBOT_MSG_THINKING', 'Let me think...'),
        'happy': os.getenv('ROBOT_MSG_HAPPY', 'Great job!'),
        'error': os.getenv('ROBOT_MSG_ERROR', 'Oops! Something went wrong.'),
        'sleeping': os.getenv('ROBOT_MSG_SLEEPING', 'Sleeping...')
    }
    
    # Hardware specific settings
    RASPBERRY_PI = os.getenv('ROBOT_IS_PI', 'False').lower() == 'true'
    TOUCHSCREEN = os.getenv('ROBOT_HAS_TOUCH', 'False').lower() == 'true'
    
    @classmethod
    def get_display_config(cls) -> Dict[str, Any]:
        """Get display configuration."""
        return {
            'width': cls.DISPLAY_WIDTH,
            'height': cls.DISPLAY_HEIGHT,
            'fullscreen': cls.FULLSCREEN,
            'use_gui': cls.USE_GUI,
            'face_size': cls.FACE_SIZE
        }
    
    @classmethod
    def get_animation_config(cls) -> Dict[str, Any]:
        """Get animation configuration."""
        return {
            'fps': cls.ANIMATION_FPS,
            'enabled': cls.ENABLE_ANIMATIONS
        }
    
    @classmethod
    def get_hardware_config(cls) -> Dict[str, Any]:
        """Get hardware configuration."""
        return {
            'is_pi': cls.RASPBERRY_PI,
            'has_touch': cls.TOUCHSCREEN
        }


# Preset configurations for different robot setups

class RaspberryPi7InchConfig(VisualConfig):
    """Configuration for Raspberry Pi with 7-inch touchscreen."""
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480
    FULLSCREEN = True
    RASPBERRY_PI = True
    TOUCHSCREEN = True
    FACE_SIZE = 100


class RaspberryPi5InchConfig(VisualConfig):
    """Configuration for Raspberry Pi with 5-inch display."""
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 480
    FULLSCREEN = True
    RASPBERRY_PI = True
    TOUCHSCREEN = False
    FACE_SIZE = 80


class DesktopDevelopmentConfig(VisualConfig):
    """Configuration for desktop development."""
    DISPLAY_WIDTH = 1024
    DISPLAY_HEIGHT = 768
    FULLSCREEN = False
    RASPBERRY_PI = False
    TOUCHSCREEN = False
    FACE_SIZE = 150


class MinimalConfig(VisualConfig):
    """Configuration for minimal/headless setup."""
    USE_GUI = False
    ENABLE_ANIMATIONS = False


def get_config_for_environment() -> VisualConfig:
    """Automatically detect and return appropriate configuration."""
    
    # Check for specific environment variables
    robot_type = os.getenv('ROBOT_TYPE', '').lower()
    
    if robot_type == 'pi_7inch':
        return RaspberryPi7InchConfig
    elif robot_type == 'pi_5inch':
        return RaspberryPi5InchConfig
    elif robot_type == 'desktop':
        return DesktopDevelopmentConfig
    elif robot_type == 'minimal':
        return MinimalConfig
    
    # Auto-detect based on system
    try:
        import platform
        
        # Check if running on Raspberry Pi
        if platform.machine().startswith('arm') or os.path.exists('/opt/vc/bin/vcgencmd'):
            # Check display size if possible
            try:
                import subprocess
                result = subprocess.run(['xrandr'], capture_output=True, text=True)
                if '800x480' in result.stdout:
                    return RaspberryPi7InchConfig
                else:
                    return RaspberryPi5InchConfig
            except:
                return RaspberryPi7InchConfig
        
        # Desktop/development environment
        else:
            # Check if GUI is available
            try:
                import tkinter
                return DesktopDevelopmentConfig
            except ImportError:
                return MinimalConfig
    
    except Exception:
        # Fallback to minimal config
        return MinimalConfig
    
    # Default fallback
    return VisualConfig 