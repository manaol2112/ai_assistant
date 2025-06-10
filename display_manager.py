#!/usr/bin/env python3
"""
Display Manager for AI Assistant
Provides visual feedback for different AI states on a small screen (e.g., Raspberry Pi)
Supports both real display and console simulation mode for development
"""

import os
import sys
import queue
import time
import logging
import threading
import platform
import math
from enum import Enum
from typing import Optional, Dict, Tuple, Any
from datetime import datetime

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("pygame not available - running in simulation mode")

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
            logger.info("macOS detected - Attempting display initialization...")
            # Try to setup macOS display, but don't fail if it doesn't work
            success = self._setup_macos_display()
            if not success:
                logger.info("macOS display failed - Running in console simulation mode")
                self._setup_console_simulation()
        else:
            logger.info("Linux/Pi detected - Starting threaded display")
            self.running = True
            self.display_thread = threading.Thread(target=self._display_loop, daemon=True)
            self.display_thread.start()
        
        logger.info("Display system started")
    
    def _setup_macos_display(self) -> bool:
        """Setup display for macOS with main thread compatibility. Returns True if successful."""
        try:
            # Test if pygame display is available
            pygame.init()
            
            # Try to get display info first
            try:
                info = pygame.display.Info()
                if info.w == 0 or info.h == 0:
                    logger.warning("Display info shows 0x0 dimensions - display not available")
                    return False
            except Exception as display_info_error:
                logger.warning(f"Cannot get display info: {display_info_error}")
                return False
            
            # Set SDL to use a compatible video driver on macOS
            os.environ['SDL_VIDEODRIVER'] = 'cocoa'
            
            # Set window position to center
            os.environ['SDL_WINDOWID'] = ''
            os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'
            
            # Ensure minimum dimensions for macOS
            test_width = max(min(self.screen_width, 800), 320)  # Minimum 320px
            test_height = max(min(self.screen_height, 600), 240)  # Minimum 240px
            
            logger.info(f"Creating macOS display with dimensions: {test_width}x{test_height}")
            
            # Create window with proper flags for visibility
            self.screen = pygame.display.set_mode((test_width, test_height), pygame.SHOWN | pygame.RESIZABLE)
            pygame.display.set_caption("AI Assistant Display (macOS Test Mode)")
            
            # Initialize fonts with error checking
            try:
                self.font_large = pygame.font.Font(None, max(36, test_height // 15))
                self.font_medium = pygame.font.Font(None, max(24, test_height // 20))
                self.font_small = pygame.font.Font(None, max(18, test_height // 25))
            except Exception as font_error:
                logger.warning(f"Font initialization error: {font_error}")
                # Use system default
                self.font_large = pygame.font.Font(None, 36)
                self.font_medium = pygame.font.Font(None, 24)
                self.font_small = pygame.font.Font(None, 18)
            
            # Verify screen was created successfully
            if self.screen is None:
                raise Exception("Failed to create pygame screen")
            
            # Check actual screen dimensions
            actual_size = self.screen.get_size()
            if actual_size[0] == 0 or actual_size[1] == 0:
                raise Exception(f"Invalid screen dimensions: {actual_size}")
            
            self.running = True
            
            # Initial render to make window visible with a bright test pattern
            self.screen.fill((50, 50, 200))  # Blue background for visibility
            
            # Draw a test pattern to ensure visibility
            pygame.draw.circle(self.screen, (255, 255, 0), (test_width//2, test_height//2), 50)  # Yellow circle
            pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, 100, 50))  # Red rectangle
            
            # Add text to confirm it's working
            if self.font_large:
                text = self.font_large.render("AI Assistant Display", True, (255, 255, 255))
                text_rect = text.get_rect(center=(test_width//2, test_height//2 + 80))
                self.screen.blit(text, text_rect)
            
            # Force display update
            pygame.display.flip()
            
            logger.info(f"macOS display initialized successfully: {actual_size[0]}x{actual_size[1]}")
            return True
            
        except Exception as e:
            logger.warning(f"macOS display initialization failed: {e}")
            try:
                pygame.quit()
            except:
                pass
            self.screen = None
            return False
    
    def _setup_console_simulation(self):
        """Setup console-based display simulation for development."""
        self.running = True
        self.screen = None  # No actual screen
        logger.info("Console display simulation active - State changes will be logged")
        
        # Print a visual indicator
        print("\n" + "="*60)
        print("🖥️  AI ASSISTANT DISPLAY SIMULATOR")
        print("📺 Visual feedback will be shown in console")
        print("="*60)
    
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
            
            # Handle different display modes
            if not self.running:
                return
            
            if self.headless_mode or (self.is_macos and self.screen is None):
                # Console simulation mode
                self._display_console_state(state, user, message)
            elif self.screen:
                # Real display mode
                try:
                    if self.is_macos:
                        # Direct update for macOS
                        self._render_state()
                        pygame.display.flip()
                    else:
                        # Queue for threaded display
                        self.state_queue.put({
                            'state': state,
                            'user': user,
                            'message': message,
                            'timestamp': time.time()
                        }, block=False)
                except Exception as e:
                    logger.debug(f"Display update failed: {e}")
            
            # Log state changes for debugging
            logger.debug(f"Display state: {state.value} | User: {user} | Message: {message}")
        
        except Exception as e:
            logger.warning(f"Error setting display state: {e}")
    
    def _display_console_state(self, state: AIState, user: Optional[str], message: str):
        """Display state in console for simulation mode."""
        # Get state info
        config = self.state_config[state]
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Create a visual representation
        state_symbols = {
            AIState.STANDBY: "🔵",
            AIState.LISTENING: "🟢",
            AIState.SPEAKING: "🟠", 
            AIState.PROCESSING: "🟣",
            AIState.GAME_ACTIVE: "🔵",
            AIState.ERROR: "🔴"
        }
        
        symbol = state_symbols.get(state, "⚪")
        user_info = f" | User: {user.title()}" if user else ""
        message_info = f" | {message}" if message else ""
        
        # Print the state update
        print(f"\n📺 [{timestamp}] {symbol} {config['text'].upper()}{user_info}{message_info}")
        
        # Add visual separator for important states
        if state in [AIState.LISTENING, AIState.SPEAKING]:
            print("   " + "━" * 50)
    
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