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
        """Update emotional state with smooth transitions and intensity."""
        if state not in self.color_schemes:
            state = 'standby'
            
        self.current_state = state
        colors = self.color_schemes[state]
        
        # Smooth color transitions
        self._transition_colors(colors, intensity)
        
        # Update mouth shape based on state
        mouth_map = {
            'standby': 'neutral',
            'listening': 'neutral',
            'speaking': 'speaking_o',
            'thinking': 'thinking',
            'happy': 'happy',
            'error': 'surprised'
        }
        
        new_mouth = mouth_map.get(state, 'neutral')
        if new_mouth != self.current_mouth:
            self.current_mouth = new_mouth
            if 'mouth' in self.elements:
                self.canvas.delete(self.elements['mouth'])
                self.elements['mouth'] = self.mouth_shapes[new_mouth]
    
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
    
    def start_speaking(self):
        """Start advanced speaking animation."""
        self.speaking = True
        self.mouth_animation_frame = 0
        self.animate_mouth_speaking()
    
    def stop_speaking(self):
        """Stop speaking animation and return to neutral."""
        self.speaking = False
        if 'mouth' in self.elements:
            self.canvas.delete(self.elements['mouth'])
            self.elements['mouth'] = self.mouth_shapes['neutral']
    
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
    
    def start_animations(self):
        """Start all premium animations."""
        self.animation_active = True
        self.animate_breathing()
        self.animate_micro_expressions()
    
    def stop_animations(self):
        """Stop all animations."""
        self.animation_active = False
        self.stop_speaking()

    def _create_modern_robot(self):
        """Create sleek modern robot matching the reference design - white with blue glowing eyes."""
        colors = self.color_schemes.get('standby', {
            'body_primary': '#f5f5f5',
            'body_secondary': '#ffffff', 
            'eye_glow': '#00ccff',
            'eye_inner': '#004080',
            'accent': '#e0e0e0',
            'shadow': '#c0c0c0'
        })
        
        # Premium glow effect background
        self.elements['outer_glow'] = self.canvas.create_oval(
            self.center_x - self.size//2 - 30, self.center_y - int(self.size * 0.7) - 30,
            self.center_x + self.size//2 + 30, self.center_y + int(self.size * 0.7) + 30,
            fill='#e6f7ff', outline='', stipple='gray12'
        )
        
        # Robot body shadow
        body_width = int(self.size * 1.1)
        body_height = int(self.size * 1.3)
        self.elements['body_shadow'] = self.canvas.create_oval(
            self.center_x - body_width//2 + 4, self.center_y - body_height//2 + 4,
            self.center_x + body_width//2 + 4, self.center_y + body_height//2 + 4,
            fill='#d0d0d0', outline='', stipple='gray25'
        )
        
        # Main robot body - sleek oval shape
        self.elements['body'] = self.canvas.create_oval(
            self.center_x - body_width//2, self.center_y - body_height//2,
            self.center_x + body_width//2, self.center_y + body_height//2,
            fill=colors['body_primary'], outline=colors['accent'], width=3
        )
        
        # Inner body highlight for premium look
        self.elements['body_highlight'] = self.canvas.create_oval(
            self.center_x - body_width//2 + 8, self.center_y - body_height//2 + 8,
            self.center_x + body_width//2 - 8, self.center_y + body_height//2 - 8,
            fill=colors['body_secondary'], outline='', stipple='gray12'
        )
        
        # Large prominent blue glowing eyes
        eye_size = self.size // 3  # Much larger eyes
        eye_offset_x = self.size // 4
        eye_offset_y = self.size // 6
        
        # Eye outer glow rings
        glow_size = eye_size + 12
        self.elements['left_eye_glow'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - glow_size, self.center_y - eye_offset_y - glow_size,
            self.center_x - eye_offset_x + glow_size, self.center_y - eye_offset_y + glow_size,
            fill='', outline=colors['eye_glow'], width=4
        )
        
        self.elements['right_eye_glow'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - glow_size, self.center_y - eye_offset_y - glow_size,
            self.center_x + eye_offset_x + glow_size, self.center_y - eye_offset_y + glow_size,
            fill='', outline=colors['eye_glow'], width=4
        )
        
        # Eye frames (black bezels)
        frame_size = eye_size + 6
        self.elements['left_eye_frame'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - frame_size, self.center_y - eye_offset_y - frame_size,
            self.center_x - eye_offset_x + frame_size, self.center_y - eye_offset_y + frame_size,
            fill='#2a2a2a', outline='#1a1a1a', width=2
        )
        
        self.elements['right_eye_frame'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - frame_size, self.center_y - eye_offset_y - frame_size,
            self.center_x + eye_offset_x + frame_size, self.center_y - eye_offset_y + frame_size,
            fill='#2a2a2a', outline='#1a1a1a', width=2
        )
        
        # Main eye globes with blue glow
        self.elements['left_eye'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=colors['eye_glow'], outline=colors['eye_inner'], width=3
        )
        
        self.elements['right_eye'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=colors['eye_glow'], outline=colors['eye_inner'], width=3
        )
        
        # Inner eye circles for depth
        inner_size = eye_size - 8
        self.elements['left_eye_inner'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - inner_size, self.center_y - eye_offset_y - inner_size,
            self.center_x - eye_offset_x + inner_size, self.center_y - eye_offset_y + inner_size,
            fill=colors['eye_inner'], outline=''
        )
        
        self.elements['right_eye_inner'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - inner_size, self.center_y - eye_offset_y - inner_size,
            self.center_x + eye_offset_x + inner_size, self.center_y - eye_offset_y + inner_size,
            fill=colors['eye_inner'], outline=''
        )
        
        # Bright center pupils for life-like appearance
        pupil_size = 8
        self.elements['left_pupil'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - pupil_size, self.center_y - eye_offset_y - pupil_size,
            self.center_x - eye_offset_x + pupil_size, self.center_y - eye_offset_y + pupil_size,
            fill='#66d9ff', outline='white', width=1
        )
        
        self.elements['right_pupil'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - pupil_size, self.center_y - eye_offset_y - pupil_size,
            self.center_x + eye_offset_x + pupil_size, self.center_y - eye_offset_y + pupil_size,
            fill='#66d9ff', outline='white', width=1
        )
        
        # Bright highlights for premium look
        highlight_size = 4
        self.elements['left_highlight'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - highlight_size - 6, self.center_y - eye_offset_y - highlight_size - 6,
            self.center_x - eye_offset_x + highlight_size - 6, self.center_y - eye_offset_y + highlight_size - 6,
            fill='#ffffff', outline=''
        )
        
        self.elements['right_highlight'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - highlight_size - 6, self.center_y - eye_offset_y - highlight_size - 6,
            self.center_x + eye_offset_x + highlight_size - 6, self.center_y - eye_offset_y + highlight_size - 6,
            fill='#ffffff', outline=''
        )
        
        # Body panel lines for modern tech look
        panel_y1 = self.center_y + self.size // 3
        panel_y2 = self.center_y + self.size // 2
        
        self.elements['panel_line_1'] = self.canvas.create_line(
            self.center_x - 25, panel_y1,
            self.center_x + 25, panel_y1,
            fill=colors['accent'], width=2
        )
        
        self.elements['panel_line_2'] = self.canvas.create_line(
            self.center_x - 20, panel_y2,
            self.center_x + 20, panel_y2,
            fill=colors['accent'], width=2
        )
        
        # Small status LED
        self.elements['status_led'] = self.canvas.create_oval(
            self.center_x - 3, self.center_y - self.size // 2 + 15,
            self.center_x + 3, self.center_y - self.size // 2 + 21,
            fill='#00ff00', outline='#00cc00', width=1
        )
        
        # Initialize advanced mouth system for modern robot
        self._create_advanced_mouth()

    def _create_premium_default_robot(self):
        """Create default modern robot design."""
        # Use the same design as modern_robot
        self._create_modern_robot()

class PremiumVisualFeedbackSystem:
    """Enterprise-grade visual feedback system with advanced emotional AI and premium aesthetics."""
    
    def __init__(self, width: int = 800, height: int = 480, current_user: str = None):
        """Initialize premium visual feedback system."""
        self.width = width
        self.height = height
        self.current_user = current_user or "default"
        self.robot_face = None
        self.root = None
        self.canvas = None
        self.message_queue = queue.Queue()
        self.animation_thread = None
        self.running = False
        self.premium_effects = True
        
        # Premium UI elements
        self.status_bar = None
        self.message_display = None
        self.current_message = "Ready to assist you"
        self.ambient_particles = []
        self.background_gradient = None
        
        # Advanced state management
        self.emotional_history = []
        self.interaction_level = 0.5  # 0.0 to 1.0
        self.user_engagement_score = 0.7
        
        # Premium sound visualization
        self.sound_visualizer = None
        self.sound_bars = []
        
        logging.info(f"Premium Visual Feedback System initialized for user: {current_user}")
    
    def _get_premium_face_type(self, user: str) -> str:
        """Determine premium face type based on user preferences."""
        user_preferences = {
            "eladriel": "modern_robot",
            "sophia": "modern_robot", 
            "alex": "modern_robot",
            "default": "modern_robot"
        }
        return user_preferences.get(user.lower(), "modern_robot")
    
    def start(self):
        """Start the premium visual feedback system."""
        if self.running:
            return
            
        self.running = True
        self._create_premium_ui()
        self._start_animation_thread()
        
        # Don't run mainloop here - let run_gui() handle it
    
    def run_gui(self):
        """Run the GUI main loop (for compatibility with main.py)."""
        if self.root:
            self.root.mainloop()
        else:
            # Start first if not already started
            self.start()
            if self.root:
                self.root.mainloop()
    
    def stop(self):
        """Stop the premium visual feedback system."""
        self.running = False
        if self.robot_face:
            self.robot_face.stop_animations()
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def _create_premium_ui(self):
        """Create premium user interface with enterprise aesthetics."""
        self.root = tk.Tk()
        self.root.title("Premium AI Assistant - Visual Feedback")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg='#0a0a0a')
        self.root.attributes('-topmost', True)
        
        # Remove window decorations for sleek look
        self.root.overrideredirect(True)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Premium gradient background
        self._create_premium_background()
        
        # Main canvas with premium styling
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height - 100,
            bg='#0f0f0f',
            highlightthickness=0,
            relief='flat'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create premium robot face
        face_type = self._get_premium_face_type(self.current_user)
        center_x = self.width // 2
        center_y = (self.height - 100) // 2
        
        self.robot_face = PremiumRobotFace(
            canvas=self.canvas,
            center_x=center_x,
            center_y=center_y,
            size=140,
            face_type=face_type
        )
        
        # Start premium animations
        self.robot_face.start_animations()
        
        # Create premium status bar
        self._create_premium_status_bar()
        
        # Add premium ambient effects
        self._create_ambient_effects()
        
        # Add premium sound visualizer
        self._create_sound_visualizer()
        
        # Bind premium interaction events
        self._bind_premium_events()
        
        # Process message queue
        self._process_messages()
    
    def _create_premium_background(self):
        """Create premium gradient background with subtle animations."""
        # This would typically use a more sophisticated gradient
        # For now, creating a sophisticated dark theme
        self.root.configure(bg='#0a0a0a')
    
    def _create_premium_status_bar(self):
        """Create elegant status bar with premium styling."""
        status_frame = tk.Frame(
            self.root,
            bg='#1a1a1a',
            height=100,
            relief='flat'
        )
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        # User info with premium styling
        user_label = tk.Label(
            status_frame,
            text=f"Assistant for {self.current_user.title()}",
            font=('SF Pro Display', 12, 'normal'),
            fg='#ffffff',
            bg='#1a1a1a',
            pady=5
        )
        user_label.pack(side=tk.TOP)
        
        # Message display with premium typography
        self.message_display = tk.Label(
            status_frame,
            text=self.current_message,
            font=('SF Pro Display', 14, 'normal'),
            fg='#e0e0e0',
            bg='#1a1a1a',
            wraplength=self.width - 40,
            justify=tk.CENTER,
            pady=10
        )
        self.message_display.pack(side=tk.TOP, expand=True)
        
        # Premium status indicators
        indicator_frame = tk.Frame(status_frame, bg='#1a1a1a')
        indicator_frame.pack(side=tk.BOTTOM, pady=5)
        
        # AI Status indicator
        self.status_indicator = tk.Label(
            indicator_frame,
            text="● READY",
            font=('SF Pro Display', 10, 'bold'),
            fg='#00ff7f',
            bg='#1a1a1a'
        )
        self.status_indicator.pack(side=tk.LEFT, padx=10)
        
        # Engagement level indicator
        self.engagement_indicator = tk.Label(
            indicator_frame,
            text=f"Engagement: {int(self.user_engagement_score * 100)}%",
            font=('SF Pro Display', 10, 'normal'),
            fg='#87ceeb',
            bg='#1a1a1a'
        )
        self.engagement_indicator.pack(side=tk.RIGHT, padx=10)
    
    def _create_ambient_effects(self):
        """Create premium ambient particle effects."""
        # Check if canvas exists (GUI mode)
        if not self.canvas:
            return
            
        # Create floating ambient particles
        for i in range(15):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 150)
            size = random.randint(1, 3)
            
            try:
                particle = self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill='#404040', outline='', stipple='gray25'
                )
                
                self.ambient_particles.append({
                    'element': particle,
                    'x': x, 'y': y,
                    'velocity_x': random.uniform(-0.5, 0.5),
                    'velocity_y': random.uniform(-0.3, 0.3),
                    'size': size
                })
            except (tk.TclError, AttributeError):
                continue
        
        self._animate_ambient_effects()
    
    def _animate_ambient_effects(self):
        """Animate premium ambient effects."""
        if not self.running or not self.canvas:
            return
            
        for particle in self.ambient_particles:
            # Update particle position
            particle['x'] += particle['velocity_x']
            particle['y'] += particle['velocity_y']
            
            # Wrap around screen edges
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
                
            if particle['y'] < 0:
                particle['y'] = self.height - 150
            elif particle['y'] > self.height - 150:
                particle['y'] = 0
            
            # Update canvas position
            try:
                size = particle['size']
                self.canvas.coords(
                    particle['element'],
                    particle['x'] - size, particle['y'] - size,
                    particle['x'] + size, particle['y'] + size
                )
            except (tk.TclError, AttributeError):
                continue
        
        self.canvas.after(50, self._animate_ambient_effects)
    
    def _create_sound_visualizer(self):
        """Create premium sound visualization bars."""
        # Check if canvas exists (GUI mode)
        if not self.canvas:
            return
            
        bar_width = 8
        bar_spacing = 12
        num_bars = 20
        start_x = (self.width - (num_bars * bar_spacing)) // 2
        base_y = self.height - 120
        
        for i in range(num_bars):
            x = start_x + i * bar_spacing
            try:
                bar = self.canvas.create_rectangle(
                    x, base_y, x + bar_width, base_y - 5,
                    fill='#404040', outline=''
                )
                self.sound_bars.append(bar)
            except (tk.TclError, AttributeError):
                continue
        
        self._animate_sound_visualizer()
    
    def _animate_sound_visualizer(self):
        """Animate premium sound visualization."""
        if not self.running or not self.canvas:
            return
            
        base_y = self.height - 120
        
        for i, bar in enumerate(self.sound_bars):
            # Create realistic sound visualization pattern
            height = random.randint(5, 40) if self.robot_face and self.robot_face.speaking else random.randint(5, 15)
            
            try:
                coords = self.canvas.coords(bar)
                self.canvas.coords(bar, coords[0], base_y, coords[2], base_y - height)
                
                # Color based on height for premium effect
                if height > 30:
                    color = '#00ff7f'
                elif height > 20:
                    color = '#87ceeb'
                elif height > 10:
                    color = '#ffd700'
                else:
                    color = '#404040'
                    
                self.canvas.itemconfig(bar, fill=color)
            except (tk.TclError, AttributeError, IndexError):
                continue
        
        self.canvas.after(100, self._animate_sound_visualizer)
    
    def _bind_premium_events(self):
        """Bind premium interaction events."""
        # Mouse hover effects
        self.root.bind('<Button-1>', self._on_click)
        self.root.bind('<Motion>', self._on_mouse_move)
        self.root.bind('<KeyPress>', self._on_key_press)
        self.root.focus_set()
        
        # Window management
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
    
    def _on_click(self, event):
        """Handle premium click interactions."""
        # Increase engagement on interaction
        self.user_engagement_score = min(1.0, self.user_engagement_score + 0.1)
        self._update_engagement_display()
        
        # Add click ripple effect
        self._create_ripple_effect(event.x, event.y)
    
    def _on_mouse_move(self, event):
        """Handle premium mouse movement."""
        # Subtle face tracking
        if self.robot_face and hasattr(self.robot_face, 'elements'):
            # Very subtle pupil following
            pass  # Implementation would require more complex eye tracking
    
    def _on_key_press(self, event):
        """Handle premium keyboard interactions."""
        if event.keysym == 'Escape':
            self.stop()
        elif event.keysym == 'space':
            self._trigger_happy_emotion()
    
    def _create_ripple_effect(self, x: int, y: int):
        """Create premium ripple effect at click location."""
        # Check if canvas exists (GUI mode)
        if not self.canvas:
            return
            
        ripple_colors = ['#00ff7f', '#87ceeb', '#ffd700']
        
        for i, color in enumerate(ripple_colors):
            size = 10 + i * 15
            try:
                ripple = self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    outline=color, width=2, fill=''
                )
                
                # Animate ripple expansion and fade
                self._animate_ripple(ripple, size, i * 100)
            except (tk.TclError, AttributeError):
                continue
    
    def _animate_ripple(self, ripple_element, initial_size: int, delay: int):
        """Animate individual ripple effect."""
        def animate():
            try:
                coords = self.canvas.coords(ripple_element)
                if not coords:
                    return
                    
                # Expand ripple
                self.canvas.coords(
                    ripple_element,
                    coords[0] - 2, coords[1] - 2,
                    coords[2] + 2, coords[3] + 2
                )
                
                # Check if ripple is too large
                if coords[2] - coords[0] > initial_size * 3:
                    self.canvas.delete(ripple_element)
                else:
                    self.canvas.after(50, animate)
            except tk.TclError:
                pass  # Element was deleted
        
        self.canvas.after(delay, animate)
    
    def _trigger_happy_emotion(self):
        """Trigger premium happy emotion."""
        if self.robot_face:
            self.robot_face.update_state('happy', intensity=1.0)
            self.set_message("I'm so happy! 😊")
            
        # Revert after a moment
        self.canvas.after(3000, lambda: self.robot_face.update_state('standby') if self.robot_face else None)
    
    def _update_engagement_display(self):
        """Update premium engagement indicator."""
        if self.engagement_indicator:
            self.engagement_indicator.config(
                text=f"Engagement: {int(self.user_engagement_score * 100)}%"
            )
    
    def _start_animation_thread(self):
        """Start premium animation processing thread."""
        def animation_worker():
            while self.running:
                try:
                    time.sleep(0.016)  # ~60 FPS
                    # Additional background processing could go here
                except Exception as e:
                    logging.error(f"Animation thread error: {e}")
        
        self.animation_thread = threading.Thread(target=animation_worker, daemon=True)
        self.animation_thread.start()
    
    def _process_messages(self):
        """Process premium message queue."""
        if not self.running:
            return
            
        try:
            while not self.message_queue.empty():
                message_data = self.message_queue.get_nowait()
                state = message_data.get('state', 'standby')
                message = message_data.get('message', '')
                intensity = message_data.get('intensity', 1.0)
                
                if self.robot_face:
                    self.robot_face.update_state(state, intensity)
                
                if message:
                    self.set_message(message)
                
                # Update status indicator
                self._update_status_indicator(state)
                
        except queue.Empty:
            pass
        except Exception as e:
            logging.error(f"Message processing error: {e}")
        
        self.canvas.after(50, self._process_messages)
    
    def _update_status_indicator(self, state: str):
        """Update premium status indicator."""
        status_map = {
            'standby': ('● READY', '#00ff7f'),
            'listening': ('● LISTENING', '#87ceeb'),
            'speaking': ('● SPEAKING', '#ffd700'),
            'thinking': ('● THINKING', '#da70d6'),
            'happy': ('● HAPPY', '#ffb6c1'),
            'error': ('● ERROR', '#ff6b6b')
        }
        
        text, color = status_map.get(state, ('● READY', '#00ff7f'))
        
        if self.status_indicator:
            self.status_indicator.config(text=text, fg=color)
    
    def set_state(self, state: str, message: str = None, intensity: float = 1.0):
        """Set premium emotional state with advanced features."""
        message_data = {
            'state': state,
            'message': message,
            'intensity': intensity
        }
        
        try:
            self.message_queue.put_nowait(message_data)
        except queue.Full:
            logging.warning("Message queue full, dropping message")
    
    def set_message(self, message: str):
        """Set premium message display."""
        self.current_message = message
        if self.message_display:
            self.message_display.config(text=message)
    
    def show_standby(self, message: str = "Ready to assist you with premium experience"):
        """Show premium standby state."""
        self.set_state("standby", message)
    
    def show_listening(self, message: str = "I'm listening with full attention..."):
        """Show premium listening state with advanced visual feedback."""
        self.set_state("listening", message)
        if self.robot_face:
            # Add special listening effects
            pass
    
    def show_speaking(self, message: str = "Speaking with emotion and intelligence..."):
        """Show premium speaking state with advanced mouth animation."""
        self.set_state("speaking", message)
        if self.robot_face:
            self.robot_face.start_speaking()
    
    def show_thinking(self, message: str = "Processing with advanced AI reasoning..."):
        """Show premium thinking state."""
        self.set_state("thinking", message)
    
    def show_happy(self, message: str = "Wonderful! I'm delighted to help! 🌟"):
        """Show premium happy state with celebration effects."""
        self.set_state("happy", message, intensity=1.0)
        
        # Add celebration particle effects
        self._create_celebration_effects()
    
    def show_error(self, message: str = "I apologize for the inconvenience. Let me help fix this."):
        """Show premium error state with professional handling."""
        self.set_state("error", message)
    
    def _create_celebration_effects(self):
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
    
    def stop_speaking(self):
        """Stop premium speaking animation."""
        if self.robot_face:
            self.robot_face.stop_speaking()
    
    def update_user(self, new_user: str):
        """Update user with premium transition effects."""
        old_user = self.current_user
        self.current_user = new_user
        
        # Create smooth transition effect
        if self.robot_face:
            # Fade out current face
            self._fade_transition(old_user, new_user)
    
    def _fade_transition(self, old_user: str, new_user: str):
        """Create premium fade transition between users."""
        # This would implement a sophisticated transition
        # For now, we'll recreate the face with the new type
        if self.canvas and self.robot_face:
            # Stop current animations
            self.robot_face.stop_animations()
            
            # Clear current face elements
            for element in self.robot_face.elements.values():
                try:
                    self.canvas.delete(element)
                except tk.TclError:
                    pass
            
            # Create new face
            face_type = self._get_premium_face_type(new_user)
            center_x = self.width // 2
            center_y = (self.height - 100) // 2
            
            self.robot_face = PremiumRobotFace(
                canvas=self.canvas,
                center_x=center_x,
                center_y=center_y,
                size=140,
                face_type=face_type
            )
            
            # Restart animations
            self.robot_face.start_animations()
            
            # Update user display
            self.set_message(f"Hello {new_user.title()}! I'm your premium AI assistant.")

class MinimalVisualFeedback:
    """Lightweight fallback visual feedback for resource-constrained environments."""
    
    def __init__(self):
        self.current_state = "standby"
        self.current_message = "Ready"
        
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
        """Demonstrate premium features."""
        time.sleep(2)
        system.show_listening("I can hear you perfectly!")
        time.sleep(3)
        system.show_thinking("Let me process this with my advanced AI...")
        time.sleep(3)
        system.show_speaking("Here's my response with emotional intelligence!")
        time.sleep(4)
        system.show_happy("That was a wonderful interaction! ✨")
        time.sleep(3)
        system.show_standby("Ready for the next premium experience!")
    
    # Start demo in background thread
    demo_thread = threading.Thread(target=demo_sequence, daemon=True)
    demo_thread.start()
    
    system.run_gui() 