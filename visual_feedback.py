"""
Premium Visual Feedback System for AI Assistant Robot
State-of-the-art animated faces with emotional intelligence and premium aesthetics
Designed for enterprise-grade user experience with advanced animations
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
import logging
from typing import Optional, Tuple, Dict, List
from datetime import datetime
import queue
import random
from dataclasses import dataclass

try:
    from visual_config import VisualConfig
except ImportError:
    # Create minimal config if module not available
    class VisualConfig:
        def __init__(self):
            self.WINDOW_WIDTH = 800
            self.WINDOW_HEIGHT = 480
            self.ROBOT_TYPE = "default"
            self.USE_GUI = True

@dataclass
class EmotionalState:
    """Advanced emotional state with intensity and duration"""
    emotion: str
    intensity: float  # 0.0 to 1.0
    duration: float   # seconds
    blend_with: Optional[str] = None  # emotion to blend with
    
class SimpleRobotEyes:
    """Large circular robot eyes with bluish-white color and expressive emotions."""
    
    def __init__(self, canvas: tk.Canvas, center_x: int, center_y: int, size: int = 120):
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.elements = {}
        self.animation_active = False
        self.current_state = "standby"
        self.speaking = False
        self.animation_frame = 0
        
        # Animation timers
        self.blink_timer = 0
        self.thinking_timer = 0
        self.speaking_timer = 0
        self.natural_blink_timer = 0
        self.mouth_timer = 0
        self.glow_timer = 0
        self.listening_timer = 0
        
        # Eye configuration - Large circular eyes
        self.eye_distance = size // 1.2        # Distance between eye centers
        self.eye_radius = size // 2.2          # Main eye radius (much larger)
        self.pupil_radius = size // 4.5        # Pupil radius
        self.iris_radius = size // 3.2         # Iris radius
        
        # Bluish-white color scheme
        self.eye_bg = '#f8fbff'                # Very light bluish-white background
        self.eye_border = '#d6e7ff'            # Light blue border
        self.iris_color = '#e6f3ff'            # Light bluish iris
        self.pupil_color = '#2c5aa0'           # Deep blue pupil
        self.glow_color = '#87ceeb'            # Sky blue glow
        self.highlight_color = '#ffffff'        # Pure white highlights
        
        # Expression colors (keeping emotional variety)
        self.expression_color = '#4a90e2'      # Medium blue for expressions
        self.happy_color = '#5cb85c'           # Green for happy
        self.error_color = '#d9534f'           # Red for error
        self.thinking_color = '#f0ad4e'        # Orange for thinking
        self.listening_color = '#5bc0de'       # Light blue for listening
        
        # Create the large circular eyes
        self.create_circular_eyes()
        
        # Start animations
        self.start_glow_animation()
        
    def create_circular_eyes(self):
        """Create large circular robot eyes with bluish-white design."""
        # Calculate eye positions
        left_x = self.center_x - self.eye_distance // 2
        right_x = self.center_x + self.eye_distance // 2
        eye_y = self.center_y
        
        # Create outer glow effect (much larger)
        glow_size = 25
        self.elements['left_glow'] = self.canvas.create_oval(
            left_x - self.eye_radius - glow_size, eye_y - self.eye_radius - glow_size,
            left_x + self.eye_radius + glow_size, eye_y + self.eye_radius + glow_size,
            fill=self.glow_color, outline='', stipple='gray25'
        )
        
        self.elements['right_glow'] = self.canvas.create_oval(
            right_x - self.eye_radius - glow_size, eye_y - self.eye_radius - glow_size,
            right_x + self.eye_radius + glow_size, eye_y + self.eye_radius + glow_size,
            fill=self.glow_color, outline='', stipple='gray25'
        )
        
        # Create main eye whites (large circles)
        self.elements['left_eye'] = self.canvas.create_oval(
            left_x - self.eye_radius, eye_y - self.eye_radius,
            left_x + self.eye_radius, eye_y + self.eye_radius,
            fill=self.eye_bg, outline=self.eye_border, width=3
        )
        
        self.elements['right_eye'] = self.canvas.create_oval(
            right_x - self.eye_radius, eye_y - self.eye_radius,
            right_x + self.eye_radius, eye_y + self.eye_radius,
            fill=self.eye_bg, outline=self.eye_border, width=3
        )
        
        # Create iris (colored part)
        self.elements['left_iris'] = self.canvas.create_oval(
            left_x - self.iris_radius, eye_y - self.iris_radius,
            left_x + self.iris_radius, eye_y + self.iris_radius,
            fill=self.iris_color, outline=self.expression_color, width=2
        )
        
        self.elements['right_iris'] = self.canvas.create_oval(
            right_x - self.iris_radius, eye_y - self.iris_radius,
            right_x + self.iris_radius, eye_y + self.iris_radius,
            fill=self.iris_color, outline=self.expression_color, width=2
        )
        
        # Create pupils (dark centers)
        self.elements['left_pupil'] = self.canvas.create_oval(
            left_x - self.pupil_radius, eye_y - self.pupil_radius,
            left_x + self.pupil_radius, eye_y + self.pupil_radius,
            fill=self.pupil_color, outline=''
        )
        
        self.elements['right_pupil'] = self.canvas.create_oval(
            right_x - self.pupil_radius, eye_y - self.pupil_radius,
            right_x + self.pupil_radius, eye_y + self.pupil_radius,
            fill=self.pupil_color, outline=''
        )
        
        # Create highlights for life-like appearance
        highlight_size = 8
        highlight_offset = self.pupil_radius // 2
        self.elements['left_highlight'] = self.canvas.create_oval(
            left_x - highlight_offset - highlight_size, eye_y - highlight_offset - highlight_size,
            left_x - highlight_offset + highlight_size, eye_y - highlight_offset + highlight_size,
            fill=self.highlight_color, outline=''
        )
        
        self.elements['right_highlight'] = self.canvas.create_oval(
            right_x - highlight_offset - highlight_size, eye_y - highlight_offset - highlight_size,
            right_x - highlight_offset + highlight_size, eye_y - highlight_offset + highlight_size,
            fill=self.highlight_color, outline=''
        )
        
        # Create initial expression
        self.create_expression("standby")
    
    def create_expression(self, expression_type: str):
        """Create different expressions while maintaining the circular eye design."""
        # Clear existing expression elements
        expression_elements = [key for key in self.elements.keys() if key.startswith('expr_')]
        for elem in expression_elements:
            self.canvas.delete(self.elements[elem])
            del self.elements[elem]
        
        left_x = self.center_x - self.eye_distance // 2
        right_x = self.center_x + self.eye_distance // 2
        eye_y = self.center_y
        
        if expression_type == "standby":
            self._create_neutral_expression(left_x, right_x, eye_y)
        elif expression_type == "listening":
            self._create_attentive_expression(left_x, right_x, eye_y)
        elif expression_type == "speaking":
            self._create_speaking_expression(left_x, right_x, eye_y)
        elif expression_type == "thinking":
            self._create_thinking_expression(left_x, right_x, eye_y)
        elif expression_type == "happy":
            self._create_happy_expression(left_x, right_x, eye_y)
        elif expression_type == "error":
            self._create_error_expression(left_x, right_x, eye_y)
    
    def _create_neutral_expression(self, left_x: int, right_x: int, eye_y: int):
        """Create neutral expression - just the basic eyes."""
        # Update iris color to neutral blue
        self.canvas.itemconfig(self.elements['left_iris'], fill=self.iris_color, outline=self.expression_color)
        self.canvas.itemconfig(self.elements['right_iris'], fill=self.iris_color, outline=self.expression_color)
    
    def _create_attentive_expression(self, left_x: int, right_x: int, eye_y: int):
        """Create animated listening expression with pulsing rings."""
        # Change iris to listening color
        self.canvas.itemconfig(self.elements['left_iris'], fill='#e6f7ff', outline=self.listening_color)
        self.canvas.itemconfig(self.elements['right_iris'], fill='#e6f7ff', outline=self.listening_color)
        
        # Add pulsing outer rings for listening animation
        ring_size = self.eye_radius + 15
        self.elements['expr_left_ring'] = self.canvas.create_oval(
            left_x - ring_size, eye_y - ring_size,
            left_x + ring_size, eye_y + ring_size,
            fill='', outline=self.listening_color, width=4
        )
        
        self.elements['expr_right_ring'] = self.canvas.create_oval(
            right_x - ring_size, eye_y - ring_size,
            right_x + ring_size, eye_y + ring_size,
            fill='', outline=self.listening_color, width=4
        )
        
        # Add scanning arcs for active listening effect
        for i in range(2):
            arc_start = i * 180
            self.elements[f'expr_left_arc_{i}'] = self.canvas.create_arc(
                left_x - ring_size - 10, eye_y - ring_size - 10,
                left_x + ring_size + 10, eye_y + ring_size + 10,
                start=arc_start, extent=90, outline=self.listening_color, width=3, style='arc'
            )
            
            self.elements[f'expr_right_arc_{i}'] = self.canvas.create_arc(
                right_x - ring_size - 10, eye_y - ring_size - 10,
                right_x + ring_size + 10, eye_y + ring_size + 10,
                start=arc_start, extent=90, outline=self.listening_color, width=3, style='arc'
            )
    
    def _create_speaking_expression(self, left_x: int, right_x: int, eye_y: int):
        """Create speaking expression with animated elements."""
        # Change iris to speaking color
        self.canvas.itemconfig(self.elements['left_iris'], fill='#fff2e6', outline=self.expression_color)
        self.canvas.itemconfig(self.elements['right_iris'], fill='#fff2e6', outline=self.expression_color)
        
        # Add sound wave effects around eyes
        for i in range(3):
            wave_radius = self.eye_radius + 20 + (i * 15)
            self.elements[f'expr_left_wave_{i}'] = self.canvas.create_arc(
                left_x - wave_radius, eye_y - wave_radius,
                left_x + wave_radius, eye_y + wave_radius,
                start=45, extent=90, outline=self.expression_color, width=2, style='arc'
            )
            
            self.elements[f'expr_right_wave_{i}'] = self.canvas.create_arc(
                right_x - wave_radius, eye_y - wave_radius,
                right_x + wave_radius, eye_y + wave_radius,
                start=45, extent=90, outline=self.expression_color, width=2, style='arc'
            )
    
    def _create_thinking_expression(self, left_x: int, right_x: int, eye_y: int):
        """Create thinking expression - eyes look up."""
        # Move pupils up to simulate looking up
        pupil_offset = self.pupil_radius // 2
        self.canvas.coords(self.elements['left_pupil'],
            left_x - self.pupil_radius, eye_y - self.pupil_radius - pupil_offset,
            left_x + self.pupil_radius, eye_y + self.pupil_radius - pupil_offset)
        
        self.canvas.coords(self.elements['right_pupil'],
            right_x - self.pupil_radius, eye_y - self.pupil_radius - pupil_offset,
            right_x + self.pupil_radius, eye_y + self.pupil_radius - pupil_offset)
        
        # Change iris to thinking color
        self.canvas.itemconfig(self.elements['left_iris'], fill='#fff7e6', outline=self.thinking_color)
        self.canvas.itemconfig(self.elements['right_iris'], fill='#fff7e6', outline=self.thinking_color)
        
        # Add thinking dots above eyes
        for i, x_offset in enumerate([-20, 0, 20]):
            dot_size = 4
            self.elements[f'expr_think_dot_{i}'] = self.canvas.create_oval(
                left_x + x_offset - dot_size, eye_y - self.eye_radius - 30 - dot_size,
                left_x + x_offset + dot_size, eye_y - self.eye_radius - 30 + dot_size,
                fill=self.thinking_color, outline=''
            )
    
    def _create_happy_expression(self, left_x: int, right_x: int, eye_y: int):
        """Create happy expression with sparkles and crescents."""
        # Change iris to happy color
        self.canvas.itemconfig(self.elements['left_iris'], fill='#f0fff0', outline=self.happy_color)
        self.canvas.itemconfig(self.elements['right_iris'], fill='#f0fff0', outline=self.happy_color)
        
        # Add happy crescents below eyes (like smile lines)
        crescent_y = eye_y + self.eye_radius + 10
        self.elements['expr_left_crescent'] = self.canvas.create_arc(
            left_x - 25, crescent_y - 15,
            left_x + 25, crescent_y + 15,
            start=0, extent=180, outline=self.happy_color, width=4, style='arc'
        )
        
        self.elements['expr_right_crescent'] = self.canvas.create_arc(
            right_x - 25, crescent_y - 15,
            right_x + 25, crescent_y + 15,
            start=0, extent=180, outline=self.happy_color, width=4, style='arc'
        )
        
        # Add sparkle effects around eyes
        sparkle_positions = [(-30, -30), (30, -30), (-35, 0), (35, 0), (0, -40)]
        for i, (x_off, y_off) in enumerate(sparkle_positions):
            self.elements[f'expr_sparkle_{i}'] = self.canvas.create_polygon(
                left_x + x_off, eye_y + y_off - 4,
                left_x + x_off - 3, eye_y + y_off,
                left_x + x_off, eye_y + y_off + 4,
                left_x + x_off + 3, eye_y + y_off,
                fill=self.happy_color, outline=''
            )
    
    def _create_error_expression(self, left_x: int, right_x: int, eye_y: int):
        """Create error expression with X marks and sad elements."""
        # Change iris to error color
        self.canvas.itemconfig(self.elements['left_iris'], fill='#ffe6e6', outline=self.error_color)
        self.canvas.itemconfig(self.elements['right_iris'], fill='#ffe6e6', outline=self.error_color)
        
        # Add X marks over eyes
        x_size = 20
        # Left X
        self.elements['expr_left_x1'] = self.canvas.create_line(
            left_x - x_size, eye_y - x_size,
            left_x + x_size, eye_y + x_size,
            fill=self.error_color, width=5, capstyle='round'
        )
        
        self.elements['expr_left_x2'] = self.canvas.create_line(
            left_x - x_size, eye_y + x_size,
            left_x + x_size, eye_y - x_size,
            fill=self.error_color, width=5, capstyle='round'
        )
        
        # Right X
        self.elements['expr_right_x1'] = self.canvas.create_line(
            right_x - x_size, eye_y - x_size,
            right_x + x_size, eye_y + x_size,
            fill=self.error_color, width=5, capstyle='round'
        )
        
        self.elements['expr_right_x2'] = self.canvas.create_line(
            right_x - x_size, eye_y + x_size,
            right_x + x_size, eye_y - x_size,
            fill=self.error_color, width=5, capstyle='round'
        )
        
        # Add sad arcs below eyes
        sad_y = eye_y + self.eye_radius + 10
        self.elements['expr_left_sad'] = self.canvas.create_arc(
            left_x - 25, sad_y - 15,
            left_x + 25, sad_y + 15,
            start=180, extent=180, outline=self.error_color, width=4, style='arc'
        )
        
        self.elements['expr_right_sad'] = self.canvas.create_arc(
            right_x - 25, sad_y - 15,
            right_x + 25, sad_y + 15,
            start=180, extent=180, outline=self.error_color, width=4, style='arc'
        )
    
    def start_glow_animation(self):
        """Start the eye glow animation."""
        if not self.animation_active:
            return
        
        self.glow_timer += 0.1
        glow_intensity = 0.7 + 0.3 * math.sin(self.glow_timer)
        
        # Update glow opacity by changing stipple pattern
        if glow_intensity > 0.8:
            stipple = 'gray75'
        elif glow_intensity > 0.6:
            stipple = 'gray50'
        else:
            stipple = 'gray25'
        
        for glow_elem in ['left_glow', 'right_glow']:
            if glow_elem in self.elements:
                self.canvas.itemconfig(self.elements[glow_elem], stipple=stipple)
        
        self.canvas.after(100, self.start_glow_animation)
    
    def animate_speaking_screens(self):
        """Animate the screens during speaking."""
        if not self.animation_active or not self.speaking:
            return
        
        self.speaking_timer += 1
        
        # Animate the oval expressions to simulate speech
        if 'expr_left_oval' in self.elements and 'expr_right_oval' in self.elements:
            # Change oval size based on speech pattern
            cycle = self.speaking_timer % 20
            if cycle < 5:
                oval_height = 20
            elif cycle < 10:
                oval_height = 15
            elif cycle < 15:
                oval_height = 25
            else:
                oval_height = 18
            
            # Update oval sizes
            left_x = self.center_x - self.screen_distance // 2
            right_x = self.center_x + self.screen_distance // 2
            screen_y = self.center_y
            oval_width = 15
            
            self.canvas.coords(self.elements['expr_left_oval'],
                left_x - oval_width, screen_y - oval_height,
                left_x + oval_width, screen_y + oval_height)
            
            self.canvas.coords(self.elements['expr_right_oval'],
                right_x - oval_width, screen_y - oval_height,
                right_x + oval_width, screen_y + oval_height)
        
        self.canvas.after(100, self.animate_speaking_screens)
    
    def update_state(self, state: str, intensity: float = 1.0):
        """Update the screen expressions based on emotional state."""
        self.current_state = state
        
        # Stop all animations first
        self.stop_all_animations()
        
        if state == "standby":
            self._show_standby_screens()
        elif state == "listening":
            self._show_listening_screens()
        elif state == "speaking":
            self._show_speaking_screens()
        elif state == "thinking":
            self._show_thinking_screens()
        elif state == "happy":
            self._show_happy_screens()
        elif state == "error":
            self._show_error_screens()
    
    def stop_all_animations(self):
        """Stop all specific animations."""
        self.stop_speaking_animation()
        self.stop_listening_animation()
    
    def stop_listening_animation(self):
        """Stop listening animation."""
        if hasattr(self, 'listening_timer'):
            self.listening_timer = 0
    
    def _show_standby_screens(self):
        """Show neutral standby expression."""
        self.create_expression("standby")
        self.stop_speaking_animation()
    
    def _show_listening_screens(self):
        """Show animated listening expression."""
        self.create_expression("listening")
        self.listening_timer = 0
        self.animate_listening_expression()
    
    def _show_speaking_screens(self):
        """Show speaking expression with animation."""
        self.speaking = True
        self.create_expression("speaking")
        self.animate_speaking_screens()
    
    def _show_thinking_screens(self):
        """Show thinking expression."""
        self.create_expression("thinking")
        self.stop_speaking_animation()
    
    def _show_happy_screens(self):
        """Show happy expression."""
        self.create_expression("happy")
        self.stop_speaking_animation()
    
    def _show_error_screens(self):
        """Show error expression."""
        self.create_expression("error")
        self.stop_speaking_animation()
    
    def stop_speaking_animation(self):
        """Stop speaking animation."""
        self.speaking = False
        self.speaking_timer = 0
    
    def start_speaking(self):
        """Start speaking animation."""
        self.speaking = True
        self.speaking_timer = 0
        if self.current_state != "speaking":
            self.update_state("speaking")
    
    def stop_speaking(self):
        """Stop speaking animation."""
        self.speaking = False
        self.stop_speaking_animation()
        if self.current_state == "speaking":
            self.update_state("standby")
    
    def start_animations(self):
        """Start all animations."""
        self.animation_active = True
        self.start_glow_animation()
        
        if self.current_state == "speaking":
            self.animate_speaking_screens()
        elif self.current_state == "listening":
            self.animate_listening_expression()
    
    def stop_animations(self):
        """Stop all animations."""
        self.animation_active = False
        self.speaking = False
        self.stop_speaking_animation()
    
    # Legacy methods for compatibility (no longer used but kept for compatibility)
    def create_expressive_mouth(self):
        """Legacy method - expressions now handled by screens."""
        pass
    
    def _set_mouth_state(self, state: str):
        """Legacy method - expressions now handled by screens."""
        pass
    
    def _animate_speaking_mouth(self):
        """Legacy method - speaking now handled by screen animation."""
        pass
    
    def _look_direction(self, offset_x: int, offset_y: int):
        """Legacy method - direction now handled by screen expressions."""
        pass
    
    def _set_eyelid_height(self, height: int):
        """Legacy method - expressions now handled by screens."""
        pass
    
    def start_natural_blinking(self):
        """Legacy method - blinking now handled by screen glow."""
        pass
    
    def _natural_blink(self):
        """Legacy method - blinking now handled by screen glow."""
        pass
    
    def _restore_from_blink(self):
        """Legacy method - blinking now handled by screen glow."""
        pass
    
    def _animate_thinking(self):
        """Legacy method - thinking now handled by screen expressions."""
        pass
    
    def _thinking_blink(self):
        """Legacy method - blinking now handled by screen glow."""
        pass
    
    def _restore_thinking_blink(self):
        """Legacy method - blinking now handled by screen glow."""
        pass
    
    def stop_thinking_animation(self):
        """Legacy method - thinking now handled by screen expressions."""
        pass
    
    def _animate_speaking(self):
        """Legacy method - speaking now handled by screen animation."""
        pass
    
    def _happy_blink_sequence(self):
        """Legacy method - expressions now handled by screens."""
        pass
    
    def _move_eye_parts(self, element_name: str, center_x: int, center_y: int, size: int):
        """Legacy method - no longer needed for TV screen style."""
        pass

    def animate_listening_expression(self):
        """Animate the listening expression with pulsing and scanning effects."""
        if not self.animation_active or self.current_state != "listening":
            return
        
        self.listening_timer += 1
        
        # Pulsing rings effect
        ring_cycle = self.listening_timer % 30
        if ring_cycle < 15:
            # Expand rings
            scale = 1.0 + (ring_cycle / 15.0) * 0.5
        else:
            # Contract rings
            scale = 1.5 - ((ring_cycle - 15) / 15.0) * 0.5
        
        # Update ring sizes
        left_x = self.center_x - self.screen_distance // 2
        right_x = self.center_x + self.screen_distance // 2
        screen_y = self.center_y
        
        ring_size = int(18 * scale)
        
        if 'expr_left_ring' in self.elements:
            self.canvas.coords(self.elements['expr_left_ring'],
                left_x - ring_size, screen_y - ring_size,
                left_x + ring_size, screen_y + ring_size)
        
        if 'expr_right_ring' in self.elements:
            self.canvas.coords(self.elements['expr_right_ring'],
                right_x - ring_size, screen_y - ring_size,
                right_x + ring_size, screen_y + ring_size)
        
        # Animated scanning lines
        scan_cycle = self.listening_timer % 20
        for i in range(3):
            if f'expr_scan_line_{i}' in self.elements:
                # Make lines appear and disappear in sequence
                if scan_cycle == i * 6:
                    self.canvas.itemconfig(self.elements[f'expr_scan_line_{i}'], state='normal')
                elif scan_cycle == (i * 6) + 10:
                    self.canvas.itemconfig(self.elements[f'expr_scan_line_{i}'], state='hidden')
        
        # Blinking dots effect
        if self.listening_timer % 40 < 5:  # Blink every 4 seconds for 0.5 seconds
            # Hide main dots temporarily
            if 'expr_left_dot' in self.elements:
                self.canvas.itemconfig(self.elements['expr_left_dot'], state='hidden')
            if 'expr_right_dot' in self.elements:
                self.canvas.itemconfig(self.elements['expr_right_dot'], state='hidden')
        else:
            # Show main dots
            if 'expr_left_dot' in self.elements:
                self.canvas.itemconfig(self.elements['expr_left_dot'], state='normal')
            if 'expr_right_dot' in self.elements:
                self.canvas.itemconfig(self.elements['expr_right_dot'], state='normal')
        
        # Continue animation
        self.canvas.after(100, self.animate_listening_expression)

class PremiumRobotFace:
    """Premium animated robot face with advanced emotional intelligence and fluid animations."""
    
    def __init__(self, canvas: tk.Canvas, center_x: int, center_y: int, size: int = 120, face_type: str = "robot"):
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.face_type = face_type
        self.elements = {}
        self.animation_active = False
        self.current_state = "standby"
        self.emotion_queue = queue.Queue()
        self.speaking = False
        self.mouth_animation_frame = 0
        
        # For simple robot eyes mode, use the new SimpleRobotEyes
        if face_type == "simple_eyes" or face_type == "loona_eyes":
            self.robot_eyes = SimpleRobotEyes(canvas, center_x, center_y, size)
            return
        
        # Advanced animation variables
        self.blink_timer = 0
        self.pulse_timer = 0
        self.wave_timer = 0
        self.emotion_timer = 0
        self.mouth_timer = 0
        self.breath_timer = 0
        self.micro_expression_timer = 0
        
        # Premium color schemes with gradients and effects
        if face_type == "dinosaur":
            self.color_schemes = {
                'standby': {
                    'face_primary': '#E8F8F0', 'face_secondary': '#D1F2EB',
                    'eyes_primary': '#2E8B57', 'eyes_secondary': '#20B2AA',
                    'mouth_primary': '#1B5E20', 'mouth_secondary': '#4CAF50',
                    'accent': '#66BB6A', 'glow': '#00FF7F',
                    'horn_primary': '#8FBC8F', 'horn_secondary': '#556B2F'
                },
                'listening': {
                    'face_primary': '#E0F7FA', 'face_secondary': '#B2EBF2',
                    'eyes_primary': '#00E676', 'eyes_secondary': '#1DE9B6',
                    'mouth_primary': '#00C853', 'mouth_secondary': '#69F0AE',
                    'accent': '#4DD0E1', 'glow': '#00FFFF',
                    'horn_primary': '#40E0D0', 'horn_secondary': '#008B8B'
                },
                'speaking': {
                    'face_primary': '#FFF8E1', 'face_secondary': '#FFF176',
                    'eyes_primary': '#FF9800', 'eyes_secondary': '#FFB74D',
                    'mouth_primary': '#F57C00', 'mouth_secondary': '#FFCC02',
                    'accent': '#FFD54F', 'glow': '#FFD700',
                    'horn_primary': '#DAA520', 'horn_secondary': '#B8860B'
                },
                'happy': {
                    'face_primary': '#FFF9C4', 'face_secondary': '#FFF59D',
                    'eyes_primary': '#CDDC39', 'eyes_secondary': '#FFEB3B',
                    'mouth_primary': '#689F38', 'mouth_secondary': '#8BC34A',
                    'accent': '#AED581', 'glow': '#ADFF2F',
                    'horn_primary': '#9ACD32', 'horn_secondary': '#6B8E23'
                },
                'thinking': {
                    'face_primary': '#F3E5F5', 'face_secondary': '#E1BEE7',
                    'eyes_primary': '#9C27B0', 'eyes_secondary': '#BA68C8',
                    'mouth_primary': '#7B1FA2', 'mouth_secondary': '#AB47BC',
                    'accent': '#CE93D8', 'glow': '#DA70D6',
                    'horn_primary': '#9370DB', 'horn_secondary': '#8A2BE2'
                }
            }
        elif face_type == "girl_robot":
            self.color_schemes = {
                'standby': {
                    'face_primary': '#FFF0F5', 'face_secondary': '#FFE4E1',
                    'eyes_primary': '#FF69B4', 'eyes_secondary': '#FF1493',
                    'mouth_primary': '#DC143C', 'mouth_secondary': '#FF6347',
                    'accent': '#FFB6C1', 'glow': '#FF69B4',
                    'bow_primary': '#FF69B4', 'bow_secondary': '#FF1493'
                },
                'listening': {
                    'face_primary': '#F8F8FF', 'face_secondary': '#E6E6FA',
                    'eyes_primary': '#9370DB', 'eyes_secondary': '#BA55D3',
                    'mouth_primary': '#8A2BE2', 'mouth_secondary': '#9932CC',
                    'accent': '#DDA0DD', 'glow': '#DA70D6',
                    'bow_primary': '#DDA0DD', 'bow_secondary': '#DA70D6'
                },
                'speaking': {
                    'face_primary': '#FFFACD', 'face_secondary': '#FFF8DC',
                    'eyes_primary': '#FFD700', 'eyes_secondary': '#FFA500',
                    'mouth_primary': '#FF8C00', 'mouth_secondary': '#FF6347',
                    'accent': '#FFDDAB', 'glow': '#FFD700',
                    'bow_primary': '#FFB347', 'bow_secondary': '#FFA500'
                },
                'happy': {
                    'face_primary': '#FFFAF0', 'face_secondary': '#FDF5E6',
                    'eyes_primary': '#FF69B4', 'eyes_secondary': '#FF1493',
                    'mouth_primary': '#FF6347', 'mouth_secondary': '#FF4500',
                    'accent': '#FFEFD5', 'glow': '#FFB6C1',
                    'bow_primary': '#FF69B4', 'bow_secondary': '#FF1493'
                },
                'thinking': {
                    'face_primary': '#F0F8FF', 'face_secondary': '#E0EFFF',
                    'eyes_primary': '#4169E1', 'eyes_secondary': '#6495ED',
                    'mouth_primary': '#1E90FF', 'mouth_secondary': '#87CEEB',
                    'accent': '#B0C4DE', 'glow': '#87CEFA',
                    'bow_primary': '#87CEEB', 'bow_secondary': '#6495ED'
                }
            }
        elif face_type == "modern_robot":
            self.color_schemes = {
                'standby': {
                    'body_primary': '#f5f5f5', 'body_secondary': '#ffffff',
                    'eye_glow': '#00ccff', 'eye_inner': '#004080',
                    'accent': '#e0e0e0', 'shadow': '#c0c0c0',
                    'mouth_primary': '#666666', 'mouth_secondary': '#888888'
                },
                'listening': {
                    'body_primary': '#f0f8ff', 'body_secondary': '#ffffff',
                    'eye_glow': '#00ff7f', 'eye_inner': '#006040',
                    'accent': '#d0e8d0', 'shadow': '#b0c0b0',
                    'mouth_primary': '#4caf50', 'mouth_secondary': '#66bb6a'
                },
                'speaking': {
                    'body_primary': '#fff8f0', 'body_secondary': '#ffffff',
                    'eye_glow': '#ff8c00', 'eye_inner': '#cc6600',
                    'accent': '#ffd080', 'shadow': '#e0b060',
                    'mouth_primary': '#ff7043', 'mouth_secondary': '#ff8a65'
                },
                'happy': {
                    'body_primary': '#fffaf0', 'body_secondary': '#ffffff',
                    'eye_glow': '#ffeb3b', 'eye_inner': '#f57f17',
                    'accent': '#fff176', 'shadow': '#e0d050',
                    'mouth_primary': '#ffeb3b', 'mouth_secondary': '#fff176'
                },
                'thinking': {
                    'body_primary': '#f8f0ff', 'body_secondary': '#ffffff',
                    'eye_glow': '#9c27b0', 'eye_inner': '#6a1b7b',
                    'accent': '#e1bee7', 'shadow': '#c090c0',
                    'mouth_primary': '#ab47bc', 'mouth_secondary': '#ba68c8'
                }
            }
        else:
            # Default robot design
            self.color_schemes = {
                'standby': {
                    'body_primary': '#f0f0f0', 'body_secondary': '#ffffff',
                    'eye_glow': '#4fc3f7', 'eye_inner': '#0277bd',
                    'accent': '#e0e0e0', 'shadow': '#c0c0c0',
                    'mouth_primary': '#666666', 'mouth_secondary': '#888888'
                },
                'listening': {
                    'body_primary': '#f0f8f0', 'body_secondary': '#ffffff',
                    'eye_glow': '#66bb6a', 'eye_inner': '#388e3c',
                    'accent': '#c8e6c9', 'shadow': '#a5d6a7',
                    'mouth_primary': '#4caf50', 'mouth_secondary': '#66bb6a'
                },
                'speaking': {
                    'body_primary': '#fff8f0', 'body_secondary': '#ffffff',
                    'eye_glow': '#ff7043', 'eye_inner': '#d84315',
                    'accent': '#ffccbc', 'shadow': '#ffab91',
                    'mouth_primary': '#ff7043', 'mouth_secondary': '#ff8a65'
                },
                'happy': {
                    'body_primary': '#fffde7', 'body_secondary': '#ffffff',
                    'eye_glow': '#ffeb3b', 'eye_inner': '#f57f17',
                    'accent': '#fff176', 'shadow': '#ffcc02',
                    'mouth_primary': '#ffeb3b', 'mouth_secondary': '#fff176'
                },
                'thinking': {
                    'body_primary': '#fce4ec', 'body_secondary': '#ffffff',
                    'eye_glow': '#ab47bc', 'eye_inner': '#7b1fa2',
                    'accent': '#f8bbd9', 'shadow': '#f48fb1',
                    'mouth_primary': '#ab47bc', 'mouth_secondary': '#ba68c8'
                }
            }
        
        self.create_premium_face()
    
    def create_premium_face(self):
        """Create premium face with advanced visual effects."""
        if self.face_type == "dinosaur":
            self._create_premium_dinosaur()
        elif self.face_type == "girl_robot":
            self._create_premium_girl_robot()
        elif self.face_type == "modern_robot":
            self._create_modern_robot()
        else:
            self._create_premium_default_robot()
    
    def _create_premium_dinosaur(self):
        """Create stunning premium dinosaur with advanced animations."""
        colors = self.color_schemes['standby']
        
        # Premium glow effect background
        self.elements['glow'] = self.canvas.create_oval(
            self.center_x - self.size//2 - 20, self.center_y - int(self.size * 0.6) - 20,
            self.center_x + self.size//2 + 20, self.center_y + int(self.size * 0.6) + 20,
            fill=colors['glow'], outline='', stipple='gray25'
        )
        
        # Main head with gradient effect
        head_width = self.size
        head_height = int(self.size * 1.2)
        self.elements['face_shadow'] = self.canvas.create_oval(
            self.center_x - head_width//2 + 3, self.center_y - head_height//2 + 3,
            self.center_x + head_width//2 + 3, self.center_y + head_height//2 + 3,
            fill='#C0C0C0', outline='', stipple='gray50'
        )
        
        self.elements['face'] = self.canvas.create_oval(
            self.center_x - head_width//2, self.center_y - head_height//2,
            self.center_x + head_width//2, self.center_y + head_height//2,
            fill=colors['face_primary'], outline=colors['accent'], width=5
        )
        
        # Premium crystalline horns with metallic effect
        horn_points = [
            (self.center_x - 30, self.center_y - head_height//2 + 15),
            (self.center_x - 20, self.center_y - head_height//2 - 25),
            (self.center_x - 40, self.center_y - head_height//2 - 15)
        ]
        self.elements['left_horn'] = self.canvas.create_polygon(
            horn_points, fill=colors['horn_primary'], outline=colors['horn_secondary'], width=3
        )
        
        horn_points = [
            (self.center_x + 30, self.center_y - head_height//2 + 15),
            (self.center_x + 20, self.center_y - head_height//2 - 25),
            (self.center_x + 40, self.center_y - head_height//2 - 15)
        ]
        self.elements['right_horn'] = self.canvas.create_polygon(
            horn_points, fill=colors['horn_primary'], outline=colors['horn_secondary'], width=3
        )
        
        # Expressive eyes with depth and life
        eye_offset_x = self.size // 3
        eye_offset_y = self.size // 8
        eye_size = self.size // 5
        
        # Eye whites with subtle shadow
        self.elements['left_eye_white'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill='white', outline='#E0E0E0', width=2
        )
        
        self.elements['right_eye_white'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill='white', outline='#E0E0E0', width=2
        )
        
        # Iris with premium gradient effect
        iris_size = eye_size - 8
        self.elements['left_iris'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - iris_size, self.center_y - eye_offset_y - iris_size,
            self.center_x - eye_offset_x + iris_size, self.center_y - eye_offset_y + iris_size,
            fill=colors['eyes_primary'], outline=colors['eyes_secondary'], width=2
        )
        
        self.elements['right_iris'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - iris_size, self.center_y - eye_offset_y - iris_size,
            self.center_x + eye_offset_x + iris_size, self.center_y - eye_offset_y + iris_size,
            fill=colors['eyes_primary'], outline=colors['eyes_secondary'], width=2
        )
        
        # Pupils with highlight
        pupil_size = iris_size - 8
        self.elements['left_pupil'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - pupil_size, self.center_y - eye_offset_y - pupil_size,
            self.center_x - eye_offset_x + pupil_size, self.center_y - eye_offset_y + pupil_size,
            fill='#1a1a1a', outline=''
        )
        
        self.elements['right_pupil'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - pupil_size, self.center_y - eye_offset_y - pupil_size,
            self.center_x + eye_offset_x + pupil_size, self.center_y - eye_offset_y + pupil_size,
            fill='#1a1a1a', outline=''
        )
        
        # Eye highlights for life-like appearance
        highlight_size = 4
        self.elements['left_highlight'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - highlight_size, self.center_y - eye_offset_y - highlight_size,
            self.center_x - eye_offset_x + highlight_size, self.center_y - eye_offset_y + highlight_size,
            fill='white', outline=''
        )
        
        self.elements['right_highlight'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - highlight_size, self.center_y + eye_offset_y - highlight_size,
            self.center_x + eye_offset_x + highlight_size, self.center_y + eye_offset_y + highlight_size,
            fill='white', outline=''
        )
        
        # Advanced animated mouth system
        self._create_advanced_mouth()
        
        # Premium nostrils with depth
        nostril_size = 6
        self.elements['left_nostril'] = self.canvas.create_oval(
            self.center_x - 12, self.center_y + 8,
            self.center_x - 12 + nostril_size, self.center_y + 8 + nostril_size,
            fill='#2E7D32', outline='#1B5E20', width=1
        )
        
        self.elements['right_nostril'] = self.canvas.create_oval(
            self.center_x + 6, self.center_y + 8,
            self.center_x + 6 + nostril_size, self.center_y + 8 + nostril_size,
            fill='#2E7D32', outline='#1B5E20', width=1
        )
        
        # Cute freckles for personality
        for i, (x_offset, y_offset) in enumerate([(-15, 20), (15, 20), (-8, 25), (8, 25)]):
            self.elements[f'freckle_{i}'] = self.canvas.create_oval(
                self.center_x + x_offset - 2, self.center_y + y_offset - 2,
                self.center_x + x_offset + 2, self.center_y + y_offset + 2,
                fill=colors['accent'], outline=''
            )
    
    def _create_premium_girl_robot(self):
        """Create stunning premium girl robot with elegant animations."""
        colors = self.color_schemes['standby']
        
        # Premium glow effect
        self.elements['glow'] = self.canvas.create_oval(
            self.center_x - self.size//2 - 25, self.center_y - self.size//2 - 25,
            self.center_x + self.size//2 + 25, self.center_y + self.size//2 + 25,
            fill=colors['glow'], outline='', stipple='gray25'
        )
        
        # Face with elegant shadow
        self.elements['face_shadow'] = self.canvas.create_oval(
            self.center_x - self.size//2 + 3, self.center_y - self.size//2 + 3,
            self.center_x + self.size//2 + 3, self.center_y + self.size//2 + 3,
            fill='#D3D3D3', outline='', stipple='gray50'
        )
        
        self.elements['face'] = self.canvas.create_oval(
            self.center_x - self.size//2, self.center_y - self.size//2,
            self.center_x + self.size//2, self.center_y + self.size//2,
            fill=colors['face_primary'], outline=colors['accent'], width=4
        )
        
        # Elegant premium bow with sparkle effects
        bow_y = self.center_y - self.size//2 - 15
        bow_points = [
            self.center_x - 20, bow_y,
            self.center_x - 8, bow_y - 12,
            self.center_x + 8, bow_y - 12,
            self.center_x + 20, bow_y,
            self.center_x + 12, bow_y + 8,
            self.center_x - 12, bow_y + 8
        ]
        self.elements['bow'] = self.canvas.create_polygon(
            bow_points, fill=colors['bow_primary'], outline=colors['bow_secondary'], width=3
        )
        
        # Bow center with premium finish
        self.elements['bow_center'] = self.canvas.create_oval(
            self.center_x - 8, bow_y - 5,
            self.center_x + 8, bow_y + 10,
            fill=colors['bow_secondary'], outline='white', width=2
        )
        
        # Sparkle effects on bow
        for i, (x_offset, y_offset) in enumerate([(-15, -8), (15, -8), (0, -15)]):
            self.elements[f'bow_sparkle_{i}'] = self.canvas.create_polygon(
                self.center_x + x_offset, bow_y + y_offset - 3,
                self.center_x + x_offset - 2, bow_y + y_offset,
                self.center_x + x_offset, bow_y + y_offset + 3,
                self.center_x + x_offset + 2, bow_y + y_offset,
                fill='white', outline=''
            )
        
        # Beautiful expressive eyes with long lashes
        eye_offset_x = self.size // 3.5
        eye_offset_y = self.size // 8
        eye_size = self.size // 4.5
        
        # Eye whites
        self.elements['left_eye_white'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill='white', outline='#F0F0F0', width=2
        )
        
        self.elements['right_eye_white'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill='white', outline='#F0F0F0', width=2
        )
        
        # Beautiful iris with shimmer
        iris_size = eye_size - 6
        self.elements['left_iris'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - iris_size, self.center_y - eye_offset_y - iris_size,
            self.center_x - eye_offset_x + iris_size, self.center_y - eye_offset_y + iris_size,
            fill=colors['eyes_primary'], outline=colors['eyes_secondary'], width=2
        )
        
        self.elements['right_iris'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - iris_size, self.center_y - eye_offset_y - iris_size,
            self.center_x + eye_offset_x + iris_size, self.center_y - eye_offset_y + iris_size,
            fill=colors['eyes_primary'], outline=colors['eyes_secondary'], width=2
        )
        
        # Pupils with beautiful highlights
        pupil_size = iris_size - 6
        self.elements['left_pupil'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - pupil_size, self.center_y - eye_offset_y - pupil_size,
            self.center_x - eye_offset_x + pupil_size, self.center_y - eye_offset_y + pupil_size,
            fill='#2a2a2a', outline=''
        )
        
        self.elements['right_pupil'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - pupil_size, self.center_y - eye_offset_y - pupil_size,
            self.center_x + eye_offset_x + pupil_size, self.center_y - eye_offset_y + pupil_size,
            fill='#2a2a2a', outline=''
        )
        
        # Multiple highlights for sparkling eyes
        highlight_size = 3
        for i, (hx, hy) in enumerate([(-2, -2), (2, 1)]):
            self.elements[f'left_highlight_{i}'] = self.canvas.create_oval(
                self.center_x - eye_offset_x + hx - highlight_size, self.center_y - eye_offset_y + hy - highlight_size,
                self.center_x - eye_offset_x + hx + highlight_size, self.center_y - eye_offset_y + hy + highlight_size,
                fill='white', outline=''
            )
            
            self.elements[f'right_highlight_{i}'] = self.canvas.create_oval(
                self.center_x + eye_offset_x + hx - highlight_size, self.center_y - eye_offset_y + hy - highlight_size,
                self.center_x + eye_offset_x + hx + highlight_size, self.center_y - eye_offset_y + hy + highlight_size,
                fill='white', outline=''
            )
        
        # Elegant eyelashes
        self._create_eyelashes()
        
        # Advanced animated mouth
        self._create_advanced_mouth()
        
        # Rosy cheeks for warmth
        cheek_size = 12
        self.elements['left_cheek'] = self.canvas.create_oval(
            self.center_x - self.size//2 + 10, self.center_y + 10,
            self.center_x - self.size//2 + 10 + cheek_size * 2, self.center_y + 10 + cheek_size,
            fill='#FFB6C1', outline='', stipple='gray25'
        )
        
        self.elements['right_cheek'] = self.canvas.create_oval(
            self.center_x + self.size//2 - 10 - cheek_size * 2, self.center_y + 10,
            self.center_x + self.size//2 - 10, self.center_y + 10 + cheek_size,
            fill='#FFB6C1', outline='', stipple='gray25'
        )
    
    def _create_eyelashes(self):
        """Create beautiful eyelashes for the girl robot."""
        eye_offset_x = self.size // 3.5
        eye_offset_y = self.size // 8
        eye_size = self.size // 4.5
        
        # Left eyelashes
        for i, angle in enumerate([120, 135, 150]):
            x1 = self.center_x - eye_offset_x + eye_size * math.cos(math.radians(angle))
            y1 = self.center_y - eye_offset_y + eye_size * math.sin(math.radians(angle))
            x2 = x1 + 8 * math.cos(math.radians(angle))
            y2 = y1 + 8 * math.sin(math.radians(angle))
            
            self.elements[f'left_lash_{i}'] = self.canvas.create_line(
                x1, y1, x2, y2, fill='#4a4a4a', width=2, capstyle='round'
            )
        
        # Right eyelashes
        for i, angle in enumerate([30, 45, 60]):
            x1 = self.center_x + eye_offset_x + eye_size * math.cos(math.radians(angle))
            y1 = self.center_y - eye_offset_y + eye_size * math.sin(math.radians(angle))
            x2 = x1 + 8 * math.cos(math.radians(angle))
            y2 = y1 + 8 * math.sin(math.radians(angle))
            
            self.elements[f'right_lash_{i}'] = self.canvas.create_line(
                x1, y1, x2, y2, fill='#4a4a4a', width=2, capstyle='round'
            )
    
    def _create_advanced_mouth(self):
        """Create advanced mouth system with multiple shapes for different emotions and speech."""
        mouth_y = self.center_y + self.size // 3
        
        # Adjust mouth position for modern robot
        if self.face_type == "modern_robot":
            mouth_y = self.center_y + self.size // 2.5
        
        # Multiple mouth shapes for different states
        self.mouth_shapes = {
            'neutral': self._create_mouth_shape('line', mouth_y, 20, 3),
            'happy': self._create_mouth_shape('arc', mouth_y - 5, 35, 20, 0, 180),
            'speaking_o': self._create_mouth_shape('oval', mouth_y, 12, 18),
            'speaking_a': self._create_mouth_shape('arc', mouth_y, 25, 12, 20, 140),
            'speaking_e': self._create_mouth_shape('arc', mouth_y, 20, 8, 30, 120),
            'speaking_i': self._create_mouth_shape('line', mouth_y, 15, 3),
            'surprised': self._create_mouth_shape('oval', mouth_y, 15, 25),
            'thinking': self._create_mouth_shape('arc', mouth_y, 20, 10, 45, 90)
        }
        
        # Start with neutral mouth
        self.current_mouth = 'neutral'
        # Remove existing mouth if present
        if 'mouth' in self.elements:
            self.canvas.delete(self.elements['mouth'])
        self.elements['mouth'] = self.mouth_shapes['neutral']
    
    def _create_mouth_shape(self, shape_type: str, y: int, width: int, height: int, start: int = 0, extent: int = 180):
        """Create individual mouth shape."""
        colors = self.color_schemes[self.current_state]
        
        if shape_type == 'arc':
            return self.canvas.create_arc(
                self.center_x - width//2, y - height//2,
                self.center_x + width//2, y + height//2,
                start=start, extent=extent,
                outline=colors['mouth_primary'], width=4, style='arc'
            )
        elif shape_type == 'oval':
            return self.canvas.create_oval(
                self.center_x - width//2, y - height//2,
                self.center_x + width//2, y + height//2,
                fill=colors['mouth_primary'], outline=colors['mouth_secondary'], width=2
            )
        elif shape_type == 'line':
            return self.canvas.create_line(
                self.center_x - width//2, y,
                self.center_x + width//2, y,
                fill=colors['mouth_primary'], width=height, capstyle='round'
            )
    
    def animate_mouth_speaking(self, text: str = ""):
        """Advanced mouth animation based on phonetics and speech patterns."""
        if not self.speaking:
            return
            
        # Simulate realistic mouth movements based on common phonemes
        phoneme_shapes = ['speaking_o', 'speaking_a', 'speaking_e', 'speaking_i']
        current_shape = phoneme_shapes[self.mouth_animation_frame % len(phoneme_shapes)]
        
        # Update mouth shape
        if 'mouth' in self.elements:
            self.canvas.delete(self.elements['mouth'])
        
        self.elements['mouth'] = self.mouth_shapes[current_shape]
        
        self.mouth_animation_frame += 1
        
        # Schedule next frame
        if self.speaking:
            self.canvas.after(120, self.animate_mouth_speaking)
    
    def update_state(self, state: str, intensity: float = 1.0):
        """Update face based on emotional state with premium color transitions."""
        # For simple robot eyes mode, delegate to the eyes
        if hasattr(self, 'robot_eyes'):
            self.robot_eyes.update_state(state, intensity)
            return
            
        self.current_state = state
        
        if state not in self.color_schemes:
            state = 'standby'  # fallback
        
        target_colors = self.color_schemes[state]
        self._transition_colors(target_colors, intensity)
        
        # Add state-specific behaviors
        if state == "happy":
            self._trigger_happiness_effects()
        elif state == "thinking":
            self._trigger_thinking_effects()
        elif state == "speaking":
            if not self.speaking:
                self.start_speaking()
    
    def start_speaking(self):
        """Start advanced speaking animation."""
        # For simple robot eyes mode, delegate to the eyes
        if hasattr(self, 'robot_eyes'):
            self.robot_eyes.start_speaking()
            return
            
        self.speaking = True
        self.speaking_timer = 0
        self.mouth_timer = 0
        if self.current_state != "speaking":
            self.update_state("speaking")
    
    def stop_speaking(self):
        """Stop speaking animation and return to neutral."""
        # For simple robot eyes mode, delegate to the eyes
        if hasattr(self, 'robot_eyes'):
            self.robot_eyes.stop_speaking()
            return
            
        self.speaking = False
        self.stop_speaking_animation()
        self._set_mouth_state("closed")  # Close mouth when done speaking
        if self.current_state == "speaking":
            self.update_state("standby")
    
    def start_animations(self):
        """Start all premium animations."""
        # For simple robot eyes mode, delegate to the eyes
        if hasattr(self, 'robot_eyes'):
            self.robot_eyes.start_animations()
            return
            
        self.animation_active = True
        self.animate_breathing()
        self.animate_micro_expressions()
    
    def stop_animations(self):
        """Stop all animations."""
        # For simple robot eyes mode, delegate to the eyes
        if hasattr(self, 'robot_eyes'):
            self.robot_eyes.stop_animations()
            return
            
        self.animation_active = False
        self.speaking = False
        self.stop_thinking_animation()
        self.stop_speaking_animation()
        self._set_mouth_state("closed")
    
    def _transition_colors(self, target_colors: Dict[str, str], intensity: float):
        """Smoothly transition colors to create premium visual effects."""
        # Update major face elements with new colors
        if 'face' in self.elements:
            self.canvas.itemconfig(self.elements['face'], fill=target_colors.get('face_primary', target_colors.get('body_primary', '#f0f0f0')))
        
        if 'body' in self.elements:
            self.canvas.itemconfig(self.elements['body'], fill=target_colors.get('body_primary', '#f0f0f0'))
        
        if 'body_highlight' in self.elements:
            self.canvas.itemconfig(self.elements['body_highlight'], fill=target_colors.get('body_secondary', '#ffffff'))
        
        if 'glow' in self.elements:
            self.canvas.itemconfig(self.elements['glow'], fill=target_colors.get('glow', target_colors.get('eye_glow', '#4fc3f7')))
        
        if 'outer_glow' in self.elements:
            self.canvas.itemconfig(self.elements['outer_glow'], fill=target_colors.get('glow', target_colors.get('eye_glow', '#4fc3f7')))
        
        # Update eyes with intensity-based brightness
        for eye_glow in ['left_eye_glow', 'right_eye_glow']:
            if eye_glow in self.elements:
                self.canvas.itemconfig(self.elements[eye_glow], outline=target_colors.get('eye_glow', '#4fc3f7'))
        
        for eye in ['left_eye', 'right_eye']:
            if eye in self.elements:
                self.canvas.itemconfig(self.elements[eye], fill=target_colors.get('eye_glow', '#4fc3f7'))
        
        for eye_inner in ['left_eye_inner', 'right_eye_inner']:
            if eye_inner in self.elements:
                self.canvas.itemconfig(self.elements[eye_inner], fill=target_colors.get('eye_inner', '#0277bd'))
        
        for iris in ['left_iris', 'right_iris']:
            if iris in self.elements:
                self.canvas.itemconfig(self.elements[iris], fill=target_colors.get('eyes_primary', target_colors.get('eye_glow', '#4fc3f7')))
        
        # Update face-specific elements
        if self.face_type == "dinosaur":
            for horn in ['left_horn', 'right_horn']:
                if horn in self.elements:
                    self.canvas.itemconfig(self.elements[horn], fill=target_colors.get('horn_primary', '#8FBC8F'))
        elif self.face_type == "girl_robot":
            for bow_part in ['bow', 'bow_center']:
                if bow_part in self.elements:
                    self.canvas.itemconfig(self.elements[bow_part], fill=target_colors.get('bow_primary', '#FF69B4'))
        elif self.face_type == "modern_robot":
            # Update modern robot accent elements
            for panel_line in ['panel_line_1', 'panel_line_2']:
                if panel_line in self.elements:
                    self.canvas.itemconfig(self.elements[panel_line], fill=target_colors.get('accent', '#e0e0e0'))
                    
        # Update mouth for modern robot
        if 'mouth' in self.elements and self.face_type == "modern_robot":
            mouth_color = target_colors.get('mouth_primary', target_colors.get('accent', '#666666'))
            self.canvas.itemconfig(self.elements['mouth'], fill=mouth_color)
    
    def animate_breathing(self):
        """Subtle breathing animation for life-like appearance."""
        if not self.animation_active:
            return
            
        self.breath_timer += 0.1
        scale_factor = 1 + 0.02 * math.sin(self.breath_timer)
        
        # Subtle face scaling for breathing effect
        if 'face' in self.elements:
            coords = self.canvas.coords(self.elements['face'])
            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            
            # This would require more complex scaling - simplified for now
        
        self.canvas.after(100, self.animate_breathing)
    
    def animate_micro_expressions(self):
        """Add subtle micro-expressions for premium realism."""
        if not self.animation_active:
            return
            
        self.micro_expression_timer += 0.1
        
        # Subtle eye movement
        if random.random() < 0.02:  # 2% chance per frame
            self._subtle_eye_movement()
        
        # Occasional blink
        if random.random() < 0.01:  # 1% chance per frame
            self._premium_blink()
        
        self.canvas.after(50, self.animate_micro_expressions)
    
    def _subtle_eye_movement(self):
        """Create subtle, natural eye movements."""
        movement_x = random.randint(-2, 2)
        movement_y = random.randint(-1, 1)
        
        for element in ['left_pupil', 'right_pupil']:
            if element in self.elements:
                self.canvas.move(self.elements[element], movement_x, movement_y)
        
        # Return to center after brief moment
        self.canvas.after(500, lambda: self._reset_eye_position(movement_x, movement_y))
    
    def _reset_eye_position(self, x: int, y: int):
        """Reset eye position to center."""
        for element in ['left_pupil', 'right_pupil']:
            if element in self.elements:
                self.canvas.move(self.elements[element], -x, -y)
    
    def _premium_blink(self):
        """Premium blink animation with realistic timing."""
        # Hide eyes briefly
        for element in ['left_iris', 'right_iris', 'left_pupil', 'right_pupil']:
            if element in self.elements:
                self.canvas.itemconfig(self.elements[element], state='hidden')
        
        # Show eyes again after realistic blink duration
        self.canvas.after(150, self._restore_eyes)
    
    def _restore_eyes(self):
        """Restore eyes after blink."""
        for element in ['left_iris', 'right_iris', 'left_pupil', 'right_pupil']:
            if element in self.elements:
                self.canvas.itemconfig(self.elements[element], state='normal')
    
    def _trigger_happiness_effects(self):
        """Create premium celebration particle effects."""
        # Check if canvas exists (GUI mode)
        if not self.canvas:
            return
            
        colors = ['#ffd700', '#ff69b4', '#00ff7f', '#87ceeb', '#da70d6']
        
        for i in range(20):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 200)
            color = random.choice(colors)
            
            # Create star-shaped celebration particle
            star = self._create_star(x, y, 8, color)
            if star:  # Only animate if star was created successfully
                self._animate_celebration_particle(star, x, y)
    
    def _create_star(self, x: int, y: int, size: int, color: str):
        """Create premium star shape for celebrations."""
        # Check if canvas exists (GUI mode)
        if not self.canvas:
            return None
            
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.extend([px, py])
        
        try:
            return self.canvas.create_polygon(points, fill=color, outline='white', width=1)
        except (tk.TclError, AttributeError):
            return None
    
    def _animate_celebration_particle(self, particle, start_x: int, start_y: int):
        """Animate premium celebration particle."""
        velocity_x = random.uniform(-3, 3)
        velocity_y = random.uniform(-5, -1)
        gravity = 0.2
        life = 60  # frames
        
        def animate():
            nonlocal velocity_y, life
            
            if life <= 0:
                try:
                    self.canvas.delete(particle)
                except tk.TclError:
                    pass
                return
            
            # Update physics
            velocity_y += gravity
            
            # Move particle
            try:
                self.canvas.move(particle, velocity_x, velocity_y)
                
                # Fade out
                alpha = life / 60
                # Note: tkinter doesn't support alpha, so we'll simulate with stipple
                if life < 30:
                    self.canvas.itemconfig(particle, stipple='gray50')
                if life < 15:
                    self.canvas.itemconfig(particle, stipple='gray25')
                
                life -= 1
                self.canvas.after(50, animate)
                
            except tk.TclError:
                pass  # Particle was deleted
        
        animate()
    
    def _trigger_thinking_effects(self):
        """Add subtle micro-expressions for thinking state."""
        # Subtle eye movement
        if random.random() < 0.02:  # 2% chance per frame
            self._subtle_eye_movement()
        
        # Occasional blink
        if random.random() < 0.01:  # 1% chance per frame
            self._premium_blink()
    
    def update_user(self, new_user: str):
        """Update user with premium transition effects."""
        old_user = self.current_user
        self.current_user = new_user
        
        # Create smooth transition effect
        if self.robot_eyes:
            # Fade out current eyes
            self._fade_transition(old_user, new_user)
    
    def _fade_transition(self, old_user: str, new_user: str):
        """Create premium fade transition effect."""
        if not self.canvas:
            return
            
        # Create fade overlay
        overlay = self.canvas.create_rectangle(
            0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
            fill='black', stipple='gray25'
        )
        
        # Animate fade out and in
        def fade_in():
            self.canvas.delete(overlay)
            
        self.canvas.after(300, fade_in)

class PremiumVisualFeedbackSystem:
    """Premium visual feedback system with simple robot eyes - inspired by Loona pet AI."""
    
    def __init__(self, width: int = 800, height: int = 480, current_user: str = None):
        self.width = width
        self.height = height
        self.current_user = current_user or "guest"
        self.running = False
        self.robot_face = None
        self.canvas = None
        self.root = None
        
        # Message display
        self.current_message = ""
        self.message_label = None
    
    def _get_premium_face_type(self, user: str) -> str:
        """Always use simple robot eyes for everyone."""
        return "simple_eyes"
    
    def start(self):
        """Start the premium visual feedback system."""
        if self.running:
            return
            
        self.running = True
        self._create_premium_ui()
    
    def run_gui(self):
        """Run the GUI main loop."""
        if self.root:
            self.root.mainloop()
        else:
            self.start()
            if self.root:
                self.root.mainloop()
    
    def stop(self):
        """Stop the visual feedback system."""
        self.running = False
        if self.robot_face:
            self.robot_face.stop_animations()
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def _create_premium_ui(self):
        """Create the UI with simple robot eyes."""
        self.root = tk.Tk()
        self.root.title("AI Assistant - Robot Eyes")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg='#000000')
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Create main canvas for robot eyes
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height - 100,  # Leave space for message
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Create robot eyes in center
        center_x = self.width // 2
        center_y = (self.height - 100) // 2
        
        self.robot_face = PremiumRobotFace(
            canvas=self.canvas,
            center_x=center_x,
            center_y=center_y,
            size=150,
            face_type="simple_eyes"
        )
        
        # Message area
        self.message_label = tk.Label(
            self.root,
            text="Ready to assist you!",
            font=("Arial", 16),
            fg="white",
            bg="#000000",
            wraplength=self.width - 40
        )
        self.message_label.pack(pady=10)
        
        # Start animations
        if self.robot_face and hasattr(self.robot_face, 'robot_eyes'):
            self.robot_face.robot_eyes.start_animations()
    
    def set_state(self, state: str, message: str = None, intensity: float = 1.0):
        """Set the current state of the robot eyes."""
        if self.robot_face:
            self.robot_face.update_state(state, intensity)
        
        if message:
            self.set_message(message)
    
    def set_message(self, message: str):
        """Update the message display."""
        self.current_message = message
        if self.message_label:
            self.message_label.config(text=message)
    
    def show_standby(self, message: str = "Ready to assist you!"):
        """Show standby state."""
        self.set_state("standby", message)
    
    def show_listening(self, message: str = "I'm listening..."):
        """Show listening state."""
        self.set_state("listening", message)
    
    def show_speaking(self, message: str = "Speaking..."):
        """Show speaking state."""
        self.set_state("speaking", message)
    
    def show_thinking(self, message: str = "Thinking..."):
        """Show thinking state."""
        self.set_state("thinking", message)
    
    def show_happy(self, message: str = "😊 Happy to help!"):
        """Show happy state."""
        self.set_state("happy", message)
    
    def show_error(self, message: str = "Something went wrong"):
        """Show error state."""
        self.set_state("error", message)
    
    def start_speaking(self):
        """Start speaking animation."""
        if self.robot_face:
            self.robot_face.start_speaking()
    
    def stop_speaking(self):
        """Stop speaking animation."""
        if self.robot_face:
            self.robot_face.stop_speaking()
    
    def update_user(self, new_user: str):
        """Update the current user (no change needed for simple eyes)."""
        self.current_user = new_user
        print(f"🤖 Simple robot eyes active for {new_user}")
    
    # Content display methods for compatibility
    def display_content(self, content: str, content_type: str = 'general', title: str = None):
        """Display content in message area."""
        if title:
            display_text = f"{title}\n\n{content}"
        else:
            display_text = content
        self.set_message(display_text[:200] + "..." if len(display_text) > 200 else display_text)

    def hide_content(self):
        """Hide content."""
        self.set_message("Ready to assist you!")

    def show_trivia_question(self, question: str, title: str = "Trivia Challenge"):
        """Show trivia question."""
        self.display_content(question, 'trivia', title)
        self.set_state("listening")

    def show_trivia_answer(self, answer: str, title: str = "Answer"):
        """Show trivia answer."""
        self.display_content(answer, 'answer', title)
        self.set_state("speaking")

    def show_quiz_content(self, content: str, title: str = "Quiz Time"):
        """Show quiz content."""
        self.display_content(content, 'quiz', title)
        self.set_state("speaking")
    
    def show_game_info(self, content: str, title: str = "Game Info"):
        """Show game information."""
        self.display_content(content, 'game', title)
        self.set_state("speaking")

    def show_explanation(self, content: str, title: str = "Explanation"):
        """Show explanation."""
        self.display_content(content, 'explanation', title)
        self.set_state("thinking")

    def auto_format_content(self, content: str, auto_detect_type: bool = True):
        """Auto-format content based on detected type."""
        if not auto_detect_type:
            self.display_content(content)
            return
        
        # Auto-detect content type and format accordingly
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['question:', 'q:', 'quiz:', 'what', 'how', 'why', 'when', 'where']):
            self.show_trivia_question(content)
        elif any(word in content_lower for word in ['answer:', 'a:', 'solution:', 'result:']):
            self.show_trivia_answer(content)
        elif any(word in content_lower for word in ['game', 'play', 'level', 'score', 'points']):
            self.show_game_info(content)
        elif any(word in content_lower for word in ['explain', 'because', 'reason', 'definition']):
            self.show_explanation(content)
        else:
            self.display_content(content)

    def display_image(self, image_path: str, title: str = "Generated Image"):
        """Display an image in the robot's window, replacing the robot eyes temporarily."""
        try:
            from PIL import Image, ImageTk
            
            # Hide robot face temporarily
            if hasattr(self, 'robot_face') and self.robot_face and hasattr(self.robot_face, 'robot_eyes'):
                # Stop animations first
                self.robot_face.robot_eyes.stop_animations()
                # Hide the canvas
                if self.canvas:
                    self.canvas.pack_forget()
            
            # Create image display frame if it doesn't exist
            if not hasattr(self, 'image_frame'):
                self.image_frame = tk.Frame(self.root, bg='#000000')
            
            # Clear any existing image content
            for widget in self.image_frame.winfo_children():
                widget.destroy()
            
            # Load and prepare image
            pil_image = Image.open(image_path)
            
            # Scale image to fit nicely in the robot window (400x400 for 5" screen)
            target_size = 350  # Slightly smaller to leave room for title and button
            pil_image = pil_image.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Create image label
            image_label = tk.Label(
                self.image_frame, 
                image=photo, 
                bg='#000000'
            )
            image_label.image = photo  # Keep reference
            image_label.pack(pady=10)
            
            # Add title
            title_label = tk.Label(
                self.image_frame,
                text=f"🎨 {title}",
                font=('Arial', 14, 'bold'),
                fg='#00ffff',
                bg='#000000'
            )
            title_label.pack(pady=5)
            
            # Add close button
            close_button = tk.Button(
                self.image_frame,
                text="✨ Close Image ✨",
                font=('Arial', 12, 'bold'),
                command=self.hide_image,
                bg='#4CAF50',
                fg='white',
                padx=20,
                pady=8,
                relief='raised',
                bd=3
            )
            close_button.pack(pady=10)
            
            # Show the image frame
            self.image_frame.pack(fill='both', expand=True)
            
            # Update status
            self.set_message("🎨 Image displayed! Click close when done.")
            
            logging.info(f"🖼️ Image displayed in robot window: {title}")
            
        except Exception as e:
            logging.error(f"Error displaying image in robot window: {e}")
            self.show_error("Sorry, couldn't display the image")
    
    def hide_image(self):
        """Hide the image and restore robot eyes with activation animation."""
        try:
            # Hide image frame
            if hasattr(self, 'image_frame'):
                self.image_frame.pack_forget()
            
            # Show robot face again with activation animation
            if hasattr(self, 'robot_face') and self.robot_face and hasattr(self.robot_face, 'robot_eyes'):
                # Show the canvas again
                if self.canvas:
                    self.canvas.pack(pady=20)
                
                # Start animations and trigger activation animation
                self.robot_face.robot_eyes.start_animations()
                self.show_happy("👀 Robot eyes activated!")
                
                # Start a brief happy animation sequence
                def activation_sequence():
                    import time
                    time.sleep(0.5)
                    self.show_standby("Ready to help you!")
                
                import threading
                threading.Thread(target=activation_sequence, daemon=True).start()
            
            logging.info("🤖 Robot eyes restored with activation animation")
            
        except Exception as e:
            logging.error(f"Error hiding image: {e}")
            self.show_standby("Ready to help you!")

class MinimalVisualFeedback:
    """Lightweight fallback visual feedback for resource-constrained environments."""
    
    def __init__(self):
        self.current_state = "standby"
        self.current_message = "Ready"
        self.current_content = ""
        
    def set_state(self, state: str, message: str = None):
        self.current_state = state
        if message:
            self.current_message = message
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {state.upper()}: {self.current_message}")
    
    def show_standby(self, message: str = "Ready"):
        self.set_state("standby", message)
    
    def show_listening(self, message: str = "Listening..."):
        self.set_state("listening", message)
    
    def show_speaking(self, message: str = "Speaking..."):
        self.set_state("speaking", message)
    
    def show_thinking(self, message: str = "Thinking..."):
        self.set_state("thinking", message)
    
    def show_happy(self, message: str = "Happy!"):
        self.set_state("happy", message)
    
    def show_error(self, message: str = "Error occurred"):
        self.set_state("error", message)
    
    def start(self):
        print("Minimal Visual Feedback started")
    
    def run_gui(self):
        """Run in non-GUI mode (for compatibility with main.py)."""
        print("Running Minimal Visual Feedback (console mode)")
    
    def stop(self):
        print("Minimal Visual Feedback stopped")
    
    def start_speaking(self):
        self.show_speaking()
    
    def stop_speaking(self):
        self.show_standby()
    
    def update_user(self, new_user: str):
        print(f"User updated to: {new_user}")
    
    # New content display methods for compatibility
    def display_content(self, content: str, content_type: str = 'general', title: str = None):
        """Display content in console mode."""
        if title:
            print(f"\n=== {title} ===")
        print(content)
        print("=" * 50)
        self.current_content = content
    
    def hide_content(self):
        """Hide content (no-op in console mode)."""
        pass
    
    def show_trivia_question(self, question: str, title: str = "Trivia Challenge"):
        """Show trivia question in console mode."""
        print(f"\n🤔 {title}")
        print("-" * 30)
        print(question)
        print("-" * 30)
        self.set_state("listening", "What's your answer?")
    
    def show_trivia_answer(self, answer: str, title: str = "Answer"):
        """Show trivia answer in console mode."""
        print(f"\n✅ {title}")
        print("-" * 30)
        print(answer)
        print("-" * 30)
        self.set_state("speaking", "Here's the answer!")
    
    def show_quiz_content(self, content: str, title: str = "Quiz Time"):
        """Show quiz content in console mode."""
        print(f"\n🎯 {title}")
        print("-" * 30)
        print(content)
        print("-" * 30)
        self.set_state("speaking", "Let's play a quiz!")
    
    def show_game_info(self, content: str, title: str = "Game Information"):
        """Show game information in console mode."""
        print(f"\n🎮 {title}")
        print("-" * 30)
        print(content)
        print("-" * 30)
        self.set_state("speaking", "Let's play!")
    
    def show_explanation(self, content: str, title: str = "Explanation"):
        """Show explanations in console mode."""
        print(f"\n💭 {title}")
        print("-" * 30)
        print(content)
        print("-" * 30)
        self.set_state("thinking", "Let me explain...")
    
    def auto_format_content(self, content: str, auto_detect_type: bool = True):
        """Auto-format content in console mode."""
        if not content.strip():
            return
            
        content_lower = content.lower()
        
        # Auto-detect and display appropriately
        if auto_detect_type:
            if any(keyword in content_lower for keyword in ['question:', 'what is', 'who is', 'when did', 'where is', 'how many']):
                if any(option in content for option in ['a)', 'b)', 'c)', 'd)', '1.', '2.', '3.', '4.']):
                    self.show_trivia_question(content)
                else:
                    self.display_content(content, 'general', "Question")
            elif any(keyword in content_lower for keyword in ['answer:', 'correct:', 'the answer is']):
                self.show_trivia_answer(content)
            elif any(keyword in content_lower for keyword in ['quiz', 'score:', 'points:']):
                self.show_quiz_content(content)
            elif any(keyword in content_lower for keyword in ['game', 'level:', 'round:', 'you win', 'you lose']):
                self.show_game_info(content)
            elif any(keyword in content_lower for keyword in ['explanation:', 'because', 'why:', 'fun fact:']):
                self.show_explanation(content)
            else:
                self.display_content(content, 'general')
        else:
            self.display_content(content, 'general')

def create_visual_feedback(use_gui: bool = True, current_user: str = None) -> PremiumVisualFeedbackSystem:
    """Factory function to create appropriate visual feedback system."""
    try:
        if use_gui:
            return PremiumVisualFeedbackSystem(current_user=current_user)
        else:
            return MinimalVisualFeedback()
    except Exception as e:
        logging.error(f"Failed to create premium GUI, falling back to minimal: {e}")
        return MinimalVisualFeedback()

if __name__ == "__main__":
    # Demo the premium visual feedback system
    logging.basicConfig(level=logging.INFO)
    
    system = create_visual_feedback(use_gui=True, current_user="sophia")
    
    def demo_sequence():
        """Demonstrate premium features including content display."""
        time.sleep(2)
        system.show_listening("I can hear you perfectly!")
        
        time.sleep(3)
        # Demo trivia question
        trivia_question = """What is the largest planet in our solar system?

A) Earth
B) Jupiter  
C) Saturn
D) Mars"""
        system.show_trivia_question(trivia_question, "Space Trivia")
        
        time.sleep(5)
        # Demo trivia answer
        trivia_answer = """Answer: B) Jupiter

Explanation: Jupiter is indeed the largest planet in our solar system. It's so massive that it could fit all the other planets inside it!

Fun fact: Jupiter has over 80 known moons, including the four large Galilean moons discovered by Galileo in 1610."""
        system.show_trivia_answer(trivia_answer, "Correct Answer")
        
        time.sleep(5)
        # Demo quiz content
        quiz_content = """Quiz: General Knowledge Challenge

Question 1: What is the capital of France?
Question 2: Who painted the Mona Lisa?
Question 3: What is 2 + 2?

Score: 0/3
Points: Ready to start!"""
        system.show_quiz_content(quiz_content, "Quiz Time")
        
        time.sleep(4)
        # Demo game info
        game_info = """Welcome to Number Guessing Game!

Rules:
- I'm thinking of a number between 1 and 100
- You have 7 attempts to guess it
- I'll tell you if your guess is too high or too low

Level: Beginner
Round: 1
Turn: Your turn to guess!

Good luck! 🎲"""
        system.show_game_info(game_info, "Let's Play!")
        
        time.sleep(4)
        # Demo explanation
        explanation = """Why is the sky blue?

Because: When sunlight enters Earth's atmosphere, it collides with gas molecules. Blue light waves are shorter and get scattered more than other colors.

Fun fact: On Mars, the sky appears reddish-orange due to iron oxide dust in the atmosphere!

Did you know: The same scattering effect makes sunsets appear red and orange."""
        system.show_explanation(explanation, "Science Explanation")
        
        time.sleep(4)
        system.show_happy("That was a wonderful interaction! ✨")
        
        time.sleep(3)
        # Demo auto-format content
        auto_content = """Question: What's the fastest land animal?

Answer: The cheetah can run up to 70 mph!

Fun fact: Cheetahs can accelerate from 0 to 60 mph in just 3 seconds."""
        system.auto_format_content(auto_content)
        
        time.sleep(3)
        system.show_standby("Ready for the next premium experience!")
    
    # Start demo in background thread
    demo_thread = threading.Thread(target=demo_sequence, daemon=True)
    demo_thread.start()
    
    system.run_gui() 