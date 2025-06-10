#!/usr/bin/env python3
"""
Display Manager for AI Assistant Robot
Shows visual feedback for different AI states on a screen display.
Perfect for Raspberry Pi robots with small screens.
"""

import pygame
import threading
import time
import math
import logging
import platform
import os
from typing import Optional, Tuple, Dict, Any
from enum import Enum
import queue
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class AIState(Enum):
    """AI states for visual display."""
    STANDBY = "standby"
    LISTENING = "listening"
    SPEAKING = "speaking"
    PROCESSING = "processing"
    GAME_ACTIVE = "game_active"
    ERROR = "error"

class DisplayManager:
    """Manages visual display for AI Assistant states."""
    
    def __init__(self, screen_width: int = 480, screen_height: int = 320, fullscreen: bool = False):
        """Initialize the display manager."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fullscreen = fullscreen
        self.current_state = AIState.STANDBY
        self.current_user = None
        self.current_message = ""
        self.animation_time = 0
        self.running = False
        self.display_thread = None
        self.state_queue = queue.Queue()
        
        # Platform detection
        self.is_macos = platform.system() == "Darwin"
        self.is_raspberry_pi = self._detect_raspberry_pi()
        self.headless_mode = self._detect_headless_mode()
        
        # Colors (RGB)
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'blue': (0, 120, 255),
            'green': (0, 200, 100),
            'red': (255, 50, 50),
            'orange': (255, 150, 0),
            'purple': (150, 50, 255),
            'cyan': (0, 200, 255),
            'yellow': (255, 255, 0),
            'gray': (128, 128, 128),
            'dark_gray': (64, 64, 64),
            'light_gray': (192, 192, 192)
        }
        
        # State configurations
        self.state_config = {
            AIState.STANDBY: {
                'color': self.colors['blue'],
                'bg_color': self.colors['black'],
                'text': 'AI Assistant Ready',
                'subtitle': 'Say "Hello" to start',
                'icon': '🤖',
                'animation': 'pulse'
            },
            AIState.LISTENING: {
                'color': self.colors['green'],
                'bg_color': (0, 20, 0),
                'text': 'Listening...',
                'subtitle': 'Speak now',
                'icon': '🎤',
                'animation': 'wave'
            },
            AIState.SPEAKING: {
                'color': self.colors['orange'],
                'bg_color': (20, 10, 0),
                'text': 'Speaking',
                'subtitle': 'AI is talking',
                'icon': '🗣️',
                'animation': 'bounce'
            },
            AIState.PROCESSING: {
                'color': self.colors['purple'],
                'bg_color': (15, 0, 20),
                'text': 'Thinking...',
                'subtitle': 'Processing your request',
                'icon': '🧠',
                'animation': 'spin'
            },
            AIState.GAME_ACTIVE: {
                'color': self.colors['cyan'],
                'bg_color': (0, 15, 20),
                'text': 'Game Active',
                'subtitle': 'Playing together!',
                'icon': '🎮',
                'animation': 'rainbow'
            },
            AIState.ERROR: {
                'color': self.colors['red'],
                'bg_color': (20, 0, 0),
                'text': 'Error',
                'subtitle': 'Something went wrong',
                'icon': '⚠️',
                'animation': 'flash'
            }
        }
        
        # Initialize pygame (but don't create screen yet)
        self.screen = None
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        
        # Log platform info
        logger.info(f"DisplayManager initialized - Platform: {platform.system()}, "
                   f"RPi: {self.is_raspberry_pi}, Headless: {self.headless_mode}")
    
    def _detect_raspberry_pi(self) -> bool:
        """Detect if running on Raspberry Pi."""
        try:
            with open('/proc/device-tree/model', 'r') as f:
                return 'raspberry pi' in f.read().lower()
        except:
            return False
    
    def _detect_headless_mode(self) -> bool:
        """Detect if running in headless mode."""
        # Check for SSH connection or no display
        # On macOS, DISPLAY might not be set even in GUI mode
        if self.is_macos:
            # On macOS, if we're not in SSH, we're likely in GUI mode
            return (os.environ.get('SSH_CLIENT') is not None or 
                    os.environ.get('SSH_TTY') is not None)
        else:
            # On Linux/Pi, check for DISPLAY environment variable
            return (os.environ.get('SSH_CLIENT') is not None or 
                    os.environ.get('SSH_TTY') is not None or
                    os.environ.get('DISPLAY') is None)
    
    def start_display(self):
        """Start the display in a separate thread."""
        if self.running:
            logger.warning("Display is already running")
            return
        
        # Handle different platforms
        if self.headless_mode:
            logger.info("Headless mode detected - Display manager running in simulation mode")
            self.running = True
            return
        
        if self.is_macos:
            logger.info("macOS detected - Display will run in compatibility mode")
            # On macOS, we'll use a simpler approach to avoid threading issues
            self._setup_macos_display()
        else:
            logger.info("Linux/Pi detected - Starting threaded display")
            self.running = True
            self.display_thread = threading.Thread(target=self._display_loop, daemon=True)
            self.display_thread.start()
        
        logger.info("Display system started")
    
    def _setup_macos_display(self):
        """Setup display for macOS with main thread compatibility."""
        try:
            # Set SDL to use a compatible video driver on macOS
            if 'SDL_VIDEODRIVER' not in os.environ:
                os.environ['SDL_VIDEODRIVER'] = 'cocoa'
            
            # Initialize pygame on main thread
            pygame.init()
            
            # Create a smaller window for testing on macOS
            test_width = min(self.screen_width, 800)
            test_height = min(self.screen_height, 600)
            
            self.screen = pygame.display.set_mode((test_width, test_height))
            pygame.display.set_caption("AI Assistant Display (macOS Test Mode)")
            
            # Initialize fonts
            try:
                self.font_large = pygame.font.Font(None, 36)
                self.font_medium = pygame.font.Font(None, 24)
                self.font_small = pygame.font.Font(None, 18)
            except:
                self.font_large = pygame.font.Font(None, 36)
                self.font_medium = pygame.font.Font(None, 24)
                self.font_small = pygame.font.Font(None, 18)
            
            self.running = True
            logger.info(f"macOS display initialized: {test_width}x{test_height}")
            
        except Exception as e:
            logger.warning(f"Could not initialize display on macOS: {e}")
            logger.info("Running in headless simulation mode")
            self.running = True
    
    def stop_display(self):
        """Stop the display."""
        self.running = False
        if self.display_thread:
            self.display_thread.join(timeout=2)
        
        try:
            if self.screen:
                pygame.quit()
        except:
            pass  # Ignore cleanup errors
        
        logger.info("Display stopped")
    
    def set_state(self, state: AIState, user: Optional[str] = None, message: str = ""):
        """Set the current AI state for display."""
        try:
            # Always update internal state
            self.current_state = state
            self.current_user = user
            self.current_message = message
            
            # Queue state for display thread if running
            if self.running and not self.headless_mode:
                try:
                    self.state_queue.put({
                        'state': state,
                        'user': user,
                        'message': message,
                        'timestamp': time.time()
                    }, block=False)
                except queue.Full:
                    logger.warning("State queue is full, dropping state update")
            
            # Log state changes for debugging
            logger.debug(f"Display state: {state.value} | User: {user} | Message: {message}")
            
            # On macOS, try to update display if screen exists
            if self.is_macos and self.screen and not self.headless_mode:
                try:
                    self._render_state()
                    pygame.display.flip()
                except Exception as e:
                    logger.debug(f"macOS display update failed: {e}")
        
        except Exception as e:
            logger.warning(f"Error setting display state: {e}")
    
    def _display_loop(self):
        """Main display loop running in separate thread (Linux/Pi only)."""
        try:
            # Initialize pygame
            pygame.init()
            
            # Set up display
            if self.fullscreen:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            
            pygame.display.set_caption("AI Assistant Display")
            
            # Initialize fonts
            try:
                self.font_large = pygame.font.Font(None, 48)
                self.font_medium = pygame.font.Font(None, 32)
                self.font_small = pygame.font.Font(None, 24)
            except:
                # Fallback to default font
                self.font_large = pygame.font.Font(None, 48)
                self.font_medium = pygame.font.Font(None, 32)
                self.font_small = pygame.font.Font(None, 24)
            
            clock = pygame.time.Clock()
            
            logger.info(f"Display initialized: {self.screen_width}x{self.screen_height}")
            
            while self.running:
                # Handle pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                
                # Process state updates
                try:
                    while True:
                        state_update = self.state_queue.get_nowait()
                        self.current_state = state_update['state']
                        self.current_user = state_update['user']
                        self.current_message = state_update['message']
                        self.animation_time = 0  # Reset animation
                except queue.Empty:
                    pass
                
                # Update animation time
                self.animation_time += 1
                
                # Render current state
                self._render_state()
                
                # Update display
                pygame.display.flip()
                clock.tick(60)  # 60 FPS
        
        except Exception as e:
            logger.error(f"Error in display loop: {e}")
        finally:
            try:
                if self.screen:
                    pygame.quit()
            except:
                pass  # Ignore cleanup errors
    
    def _render_state(self):
        """Render the current AI state on screen."""
        if not self.screen:
            return
        
        config = self.state_config[self.current_state]
        
        # Clear screen with background color
        bg_color = self._animate_color(config['bg_color'], config['animation'])
        self.screen.fill(bg_color)
        
        # Get center positions
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Draw animated background effect
        self._draw_background_effect(config)
        
        # Draw main icon with animation
        icon_y = center_y - 60
        self._draw_animated_icon(config['icon'], center_x, icon_y, config)
        
        # Draw main text
        main_color = self._animate_color(config['color'], config['animation'])
        text_surface = self.font_large.render(config['text'], True, main_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)
        
        # Draw subtitle
        subtitle_color = self._lighten_color(main_color, 0.7)
        subtitle_surface = self.font_medium.render(config['subtitle'], True, subtitle_color)
        subtitle_rect = subtitle_surface.get_rect(center=(center_x, center_y + 40))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw user info if available
        if self.current_user:
            user_text = f"User: {self.current_user.title()}"
            user_surface = self.font_small.render(user_text, True, self.colors['light_gray'])
            self.screen.blit(user_surface, (10, 10))
        
        # Draw custom message if available
        if self.current_message:
            message_lines = self._wrap_text(self.current_message, self.font_small, self.screen_width - 40)
            y_offset = self.screen_height - 60
            for line in message_lines[-2:]:  # Show last 2 lines
                message_surface = self.font_small.render(line, True, self.colors['white'])
                self.screen.blit(message_surface, (20, y_offset))
                y_offset += 25
        
        # Draw timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        time_surface = self.font_small.render(timestamp, True, self.colors['gray'])
        time_rect = time_surface.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(time_surface, time_rect)
        
        # Draw state indicator
        state_text = self.current_state.value.upper()
        state_surface = self.font_small.render(state_text, True, main_color)
        state_rect = state_surface.get_rect(bottomright=(self.screen_width - 10, self.screen_height - 10))
        self.screen.blit(state_surface, state_rect)
    
    def _draw_background_effect(self, config):
        """Draw animated background effects."""
        animation = config['animation']
        
        if animation == 'pulse':
            # Pulsing circles
            for i in range(3):
                radius = 50 + (self.animation_time + i * 20) % 100
                alpha = max(0, 255 - radius * 2)
                color = (*config['color'], alpha)
                self._draw_circle_with_alpha(self.screen_width // 2, self.screen_height // 2, radius, color)
        
        elif animation == 'wave':
            # Wave pattern
            for x in range(0, self.screen_width, 20):
                wave_height = math.sin((x + self.animation_time * 5) * 0.02) * 20
                y = self.screen_height // 2 + wave_height
                pygame.draw.circle(self.screen, config['color'], (x, int(y)), 3)
        
        elif animation == 'rainbow':
            # Rainbow gradient
            for i in range(self.screen_width):
                hue = (i + self.animation_time * 2) % 360
                color = self._hsv_to_rgb(hue, 0.5, 0.3)
                pygame.draw.line(self.screen, color, (i, 0), (i, self.screen_height))
    
    def _draw_animated_icon(self, icon: str, x: int, y: int, config):
        """Draw animated icon (simplified for basic pygame)."""
        animation = config['animation']
        color = config['color']
        
        # For simplicity, draw geometric shapes instead of emoji
        if animation == 'bounce':
            bounce = math.sin(self.animation_time * 0.2) * 10
            y += int(bounce)
        elif animation == 'spin':
            # Draw spinning circle
            angle = (self.animation_time * 5) % 360
            for i in range(8):
                spoke_angle = math.radians(angle + i * 45)
                end_x = x + math.cos(spoke_angle) * 20
                end_y = y + math.sin(spoke_angle) * 20
                pygame.draw.line(self.screen, color, (x, y), (int(end_x), int(end_y)), 3)
        
        # Draw main icon shape
        pygame.draw.circle(self.screen, color, (x, y), 25, 3)
        pygame.draw.circle(self.screen, self._lighten_color(color, 0.5), (x, y), 15)
    
    def _animate_color(self, base_color: Tuple[int, int, int], animation: str) -> Tuple[int, int, int]:
        """Animate color based on animation type."""
        if animation == 'flash':
            # Flashing effect
            intensity = (math.sin(self.animation_time * 0.3) + 1) / 2
            return tuple(int(c * intensity) for c in base_color)
        elif animation == 'pulse':
            # Pulsing effect
            intensity = (math.sin(self.animation_time * 0.1) + 1) / 2 * 0.5 + 0.5
            return tuple(int(c * intensity) for c in base_color)
        else:
            return base_color
    
    def _lighten_color(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Lighten a color by a factor."""
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color)
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB."""
        h = h / 360.0
        i = int(h * 6.)
        f = (h * 6.) - i
        p, q, t = v * (1. - s), v * (1. - s * f), v * (1. - s * (1. - f))
        i %= 6
        if i == 0: r, g, b = v, t, p
        elif i == 1: r, g, b = q, v, p
        elif i == 2: r, g, b = p, v, t
        elif i == 3: r, g, b = p, q, v
        elif i == 4: r, g, b = t, p, v
        elif i == 5: r, g, b = v, p, q
        return int(r * 255), int(g * 255), int(b * 255)
    
    def _draw_circle_with_alpha(self, x: int, y: int, radius: int, color: Tuple[int, int, int, int]):
        """Draw circle with alpha (simplified)."""
        # Simplified alpha blending for basic pygame
        alpha = color[3] / 255.0
        base_color = color[:3]
        blended_color = tuple(int(c * alpha) for c in base_color)
        if radius > 0:
            pygame.draw.circle(self.screen, blended_color, (x, y), radius, 2)
    
    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """Wrap text to fit within max width."""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def update_game_status(self, game_name: str, status: str):
        """Update display for game-specific status."""
        self.set_state(AIState.GAME_ACTIVE, message=f"{game_name}: {status}")
    
    def show_error(self, error_message: str):
        """Show error state with message."""
        self.set_state(AIState.ERROR, message=error_message)
    
    def get_display_info(self) -> Dict[str, Any]:
        """Get current display information."""
        return {
            'current_state': self.current_state.value,
            'current_user': self.current_user,
            'current_message': self.current_message,
            'screen_size': (self.screen_width, self.screen_height),
            'is_running': self.running
        }

# Example usage and testing
if __name__ == "__main__":
    import signal
    import sys
    
    def signal_handler(sig, frame):
        print("\nShutting down display...")
        display.stop_display()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start display
    print("Starting AI Assistant Display...")
    print("Press Ctrl+C to exit")
    
    display = DisplayManager(screen_width=800, screen_height=600, fullscreen=False)
    display.start_display()
    
    # Demo sequence
    states = [
        (AIState.STANDBY, None, ""),
        (AIState.LISTENING, "Sophia", "Waiting for voice input"),
        (AIState.PROCESSING, "Sophia", "Analyzing speech"),
        (AIState.SPEAKING, "Sophia", "Responding to question"),
        (AIState.GAME_ACTIVE, "Sophia", "Letter Word Game: Guess the word!"),
        (AIState.STANDBY, None, ""),
    ]
    
    try:
        for i, (state, user, message) in enumerate(states * 5):  # Repeat demo
            display.set_state(state, user, message)
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        display.stop_display() 