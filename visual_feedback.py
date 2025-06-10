"""
Visual Feedback System for AI Assistant Robot
Creates cute animated faces and status indicators for different robot states
Optimized for Raspberry Pi with touch screen displays
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
import logging
from typing import Optional, Tuple
from datetime import datetime
import queue
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


class RobotFace:
    """Cute animated robot face with different types and expressions for each child."""
    
    def __init__(self, canvas: tk.Canvas, center_x: int, center_y: int, size: int = 100, face_type: str = "robot"):
        """Initialize robot face at given position and size with specified type."""
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.face_type = face_type  # "robot", "dinosaur", "girl_robot"
        self.elements = {}
        self.animation_active = False
        self.current_state = "standby"
        
        # Animation variables
        self.blink_timer = 0
        self.pulse_timer = 0
        self.wave_timer = 0
        
        # Colors for different states - customized per face type
        if face_type == "dinosaur":
            self.colors = {
                'standby': {'face': '#E8F5E8', 'eyes': '#2E7D32', 'mouth': '#1B5E20', 'accent': '#4CAF50'},
                'listening': {'face': '#E0F2F1', 'eyes': '#00C853', 'mouth': '#00E676', 'accent': '#4CAF50'},
                'speaking': {'face': '#E8F5E8', 'eyes': '#43A047', 'mouth': '#2E7D32', 'accent': '#66BB6A'},
                'thinking': {'face': '#F1F8E9', 'eyes': '#689F38', 'mouth': '#558B2F', 'accent': '#8BC34A'},
                'happy': {'face': '#E8F5E8', 'eyes': '#2E7D32', 'mouth': '#1B5E20', 'accent': '#4CAF50'},
                'error': {'face': '#FFEBEE', 'eyes': '#E57373', 'mouth': '#F44336', 'accent': '#FF5722'},
                'sleeping': {'face': '#F5F5F5', 'eyes': '#9E9E9E', 'mouth': '#757575', 'accent': '#BDBDBD'}
            }
        elif face_type == "girl_robot":
            self.colors = {
                'standby': {'face': '#FCE4EC', 'eyes': '#E91E63', 'mouth': '#AD1457', 'accent': '#F8BBD9'},
                'listening': {'face': '#F3E5F5', 'eyes': '#9C27B0', 'mouth': '#7B1FA2', 'accent': '#CE93D8'},
                'speaking': {'face': '#FFF3E0', 'eyes': '#FF9800', 'mouth': '#F57C00', 'accent': '#FFCC02'},
                'thinking': {'face': '#E8EAF6', 'eyes': '#3F51B5', 'mouth': '#303F9F', 'accent': '#9FA8DA'},
                'happy': {'face': '#FCE4EC', 'eyes': '#E91E63', 'mouth': '#AD1457', 'accent': '#F8BBD9'},
                'error': {'face': '#FFEBEE', 'eyes': '#F44336', 'mouth': '#C62828', 'accent': '#FFCDD2'},
                'sleeping': {'face': '#F5F5F5', 'eyes': '#9E9E9E', 'mouth': '#757575', 'accent': '#E0E0E0'}
            }
        else:  # default friendly robot
            self.colors = {
                'standby': {'face': '#E3F2FD', 'eyes': '#2196F3', 'mouth': '#1976D2', 'accent': '#BBDEFB'},
                'listening': {'face': '#E8F8F5', 'eyes': '#00C853', 'mouth': '#4CAF50', 'accent': '#C8E6C9'},
                'speaking': {'face': '#FFF8E1', 'eyes': '#FFC107', 'mouth': '#FF9800', 'accent': '#FFE082'},
                'thinking': {'face': '#F3E5F5', 'eyes': '#9C27B0', 'mouth': '#7B1FA2', 'accent': '#CE93D8'},
                'happy': {'face': '#E8F5E8', 'eyes': '#4CAF50', 'mouth': '#2E7D32', 'accent': '#A5D6A7'},
                'error': {'face': '#FFEBEE', 'eyes': '#F44336', 'mouth': '#C62828', 'accent': '#FFCDD2'},
                'sleeping': {'face': '#F5F5F5', 'eyes': '#9E9E9E', 'mouth': '#757575', 'accent': '#E0E0E0'}
            }
        
        self.create_face()
    
    def create_face(self):
        """Create the face based on the specified type."""
        if self.face_type == "dinosaur":
            self._create_dinosaur_face()
        elif self.face_type == "girl_robot":
            self._create_girl_robot_face()
        else:
            self._create_default_robot_face()
    
    def _create_dinosaur_face(self):
        """Create a cute dinosaur face for Eladriel."""
        # Dinosaur head (oval, wider at bottom)
        head_width = self.size
        head_height = int(self.size * 1.2)
        self.elements['face'] = self.canvas.create_oval(
            self.center_x - head_width//2, self.center_y - head_height//2,
            self.center_x + head_width//2, self.center_y + head_height//2,
            fill=self.colors['standby']['face'], 
            outline='#4CAF50', 
            width=4
        )
        
        # Small cute horns
        horn_size = 15
        self.elements['left_horn'] = self.canvas.create_polygon(
            self.center_x - 25, self.center_y - head_height//2 + 10,
            self.center_x - 25 + horn_size, self.center_y - head_height//2 - horn_size,
            self.center_x - 25 - horn_size, self.center_y - head_height//2 - horn_size,
            fill=self.colors['standby']['accent'], outline='#2E7D32', width=2
        )
        
        self.elements['right_horn'] = self.canvas.create_polygon(
            self.center_x + 25, self.center_y - head_height//2 + 10,
            self.center_x + 25 + horn_size, self.center_y - head_height//2 - horn_size,
            self.center_x + 25 - horn_size, self.center_y - head_height//2 - horn_size,
            fill=self.colors['standby']['accent'], outline='#2E7D32', width=2
        )
        
        # Large friendly dinosaur eyes
        eye_offset_x = self.size // 3
        eye_offset_y = self.size // 8
        eye_size = self.size // 6
        
        self.elements['left_eye'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#1B5E20', 
            width=3
        )
        
        self.elements['right_eye'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#1B5E20', 
            width=3
        )
        
        # Cute dinosaur smile with small teeth
        mouth_y = self.center_y + self.size // 3
        self.elements['mouth'] = self.canvas.create_arc(
            self.center_x - 30, mouth_y - 10,
            self.center_x + 30, mouth_y + 15,
            start=0, extent=180, 
            outline=self.colors['standby']['mouth'], 
            width=5, 
            style='arc'
        )
        
        # Small cute teeth
        for i, x_offset in enumerate([-10, 0, 10]):
            self.elements[f'tooth_{i}'] = self.canvas.create_polygon(
                self.center_x + x_offset - 3, mouth_y,
                self.center_x + x_offset + 3, mouth_y,
                self.center_x + x_offset, mouth_y + 8,
                fill='white', outline='#E0E0E0', width=1
            )
        
        # Cute nostrils
        self.elements['left_nostril'] = self.canvas.create_oval(
            self.center_x - 8, self.center_y + 5,
            self.center_x - 4, self.center_y + 9,
            fill='#2E7D32', outline=''
        )
        self.elements['right_nostril'] = self.canvas.create_oval(
            self.center_x + 4, self.center_y + 5,
            self.center_x + 8, self.center_y + 9,
            fill='#2E7D32', outline=''
        )
    
    def _create_girl_robot_face(self):
        """Create a cute girl robot face for Sophia."""
        # Soft round face
        self.elements['face'] = self.canvas.create_oval(
            self.center_x - self.size//2, self.center_y - self.size//2,
            self.center_x + self.size//2, self.center_y + self.size//2,
            fill=self.colors['standby']['face'], 
            outline='#E91E63', 
            width=3
        )
        
        # Cute bow on top
        bow_y = self.center_y - self.size//2 - 10
        self.elements['bow'] = self.canvas.create_polygon(
            self.center_x - 15, bow_y,
            self.center_x - 5, bow_y - 10,
            self.center_x + 5, bow_y - 10,
            self.center_x + 15, bow_y,
            self.center_x + 10, bow_y + 5,
            self.center_x - 10, bow_y + 5,
            fill='#F8BBD9', outline='#E91E63', width=2
        )
        
        # Center bow knot
        self.elements['bow_center'] = self.canvas.create_oval(
            self.center_x - 5, bow_y - 3,
            self.center_x + 5, bow_y + 7,
            fill='#E91E63', outline='#AD1457', width=2
        )
        
        # Pretty eyes with eyelashes
        eye_offset_x = self.size // 4
        eye_offset_y = self.size // 6
        eye_size = self.size // 7
        
        self.elements['left_eye'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#AD1457', 
            width=2
        )
        
        self.elements['right_eye'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#AD1457', 
            width=2
        )
        
        # Cute eyelashes
        for i, (x_base, side) in enumerate([(self.center_x - eye_offset_x, -1), (self.center_x + eye_offset_x, 1)]):
            for j, angle in enumerate([-30, 0, 30]):
                lash_x = x_base + side * 8
                lash_y = self.center_y - eye_offset_y - eye_size - 2
                lash_end_x = lash_x + side * 5 * math.cos(math.radians(angle + 90))
                lash_end_y = lash_y + 8 * math.sin(math.radians(angle + 90))
                
                self.elements[f'eyelash_{i}_{j}'] = self.canvas.create_line(
                    lash_x, lash_y, lash_end_x, lash_end_y,
                    fill='#AD1457', width=2
                )
        
        # Sweet smile
        mouth_width = self.size // 3
        mouth_y = self.center_y + self.size // 4
        
        self.elements['mouth'] = self.canvas.create_arc(
            self.center_x - mouth_width//2, mouth_y - 8,
            self.center_x + mouth_width//2, mouth_y + 8,
            start=0, extent=180, 
            outline=self.colors['standby']['mouth'], 
            width=4, 
            style='arc'
        )
        
        # Cute blush marks
        self.elements['left_blush'] = self.canvas.create_oval(
            self.center_x - self.size//3, self.center_y + 5,
            self.center_x - self.size//3 + 12, self.center_y + 15,
            fill='#F8BBD9', outline=''
        )
        self.elements['right_blush'] = self.canvas.create_oval(
            self.center_x + self.size//3 - 12, self.center_y + 5,
            self.center_x + self.size//3, self.center_y + 15,
            fill='#F8BBD9', outline=''
        )
    
    def _create_default_robot_face(self):
        """Create a friendly default robot face."""
        # Friendly round face
        self.elements['face'] = self.canvas.create_oval(
            self.center_x - self.size//2, self.center_y - self.size//2,
            self.center_x + self.size//2, self.center_y + self.size//2,
            fill=self.colors['standby']['face'], 
            outline='#2196F3', 
            width=3
        )
        
        # Friendly robot antennae
        antenna_height = 20
        self.elements['left_antenna'] = self.canvas.create_line(
            self.center_x - 15, self.center_y - self.size//2,
            self.center_x - 15, self.center_y - self.size//2 - antenna_height,
            fill='#1976D2', width=3
        )
        self.elements['right_antenna'] = self.canvas.create_line(
            self.center_x + 15, self.center_y - self.size//2,
            self.center_x + 15, self.center_y - self.size//2 - antenna_height,
            fill='#1976D2', width=3
        )
        
        # Antenna tips
        self.elements['left_antenna_tip'] = self.canvas.create_oval(
            self.center_x - 20, self.center_y - self.size//2 - antenna_height - 5,
            self.center_x - 10, self.center_y - self.size//2 - antenna_height + 5,
            fill='#FFC107', outline='#FF9800', width=2
        )
        self.elements['right_antenna_tip'] = self.canvas.create_oval(
            self.center_x + 10, self.center_y - self.size//2 - antenna_height - 5,
            self.center_x + 20, self.center_y - self.size//2 - antenna_height + 5,
            fill='#FFC107', outline='#FF9800', width=2
        )
        
        # Friendly digital eyes
        eye_offset_x = self.size // 4
        eye_offset_y = self.size // 6
        eye_size = self.size // 8
        
        self.elements['left_eye'] = self.canvas.create_rectangle(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#1976D2', 
            width=2
        )
        
        self.elements['right_eye'] = self.canvas.create_rectangle(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#1976D2', 
            width=2
        )
        
        # Happy smile
        mouth_width = self.size // 3
        mouth_y = self.center_y + self.size // 4
        
        self.elements['mouth'] = self.canvas.create_arc(
            self.center_x - mouth_width//2, mouth_y - 10,
            self.center_x + mouth_width//2, mouth_y + 10,
            start=0, extent=180, 
            outline=self.colors['standby']['mouth'], 
            width=4, 
            style='arc'
        )
        
        # Status LED
        self.elements['status'] = self.canvas.create_oval(
            self.center_x - 6, self.center_y - self.size//3 - 6,
            self.center_x + 6, self.center_y - self.size//3 + 6,
            fill=self.colors['standby']['accent'], 
            outline='#1976D2', 
            width=2
        )
    
    def update_state(self, state: str):
        """Update face to show different state."""
        if state not in self.colors:
            return
            
        self.current_state = state
        colors = self.colors[state]
        
        # Update face color
        self.canvas.itemconfig(self.elements['face'], fill=colors['face'])
        
        # Update eye colors
        self.canvas.itemconfig(self.elements['left_eye'], fill=colors['eyes'])
        self.canvas.itemconfig(self.elements['right_eye'], fill=colors['eyes'])
        
        # Update mouth expression based on state
        if state == 'happy':
            # Happy smile
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=0, extent=180, style='arc')
        elif state == 'speaking':
            # Speaking mouth (oval)
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=0, extent=360, style='arc')
        elif state == 'sleeping':
            # Sleeping mouth (small line)
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=90, extent=180, style='arc')
        else:
            # Default neutral mouth
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=0, extent=180, style='arc')
        
        self.canvas.itemconfig(self.elements['mouth'], outline=colors['mouth'])
        
        # Update status indicator
        status_colors = {
            'standby': '#CCCCCC',
            'listening': '#4CAF50',
            'speaking': '#FF9800', 
            'thinking': '#9C27B0',
            'happy': '#2E7D32',
            'error': '#F44336',
            'sleeping': '#9E9E9E'
        }
        
        self.canvas.itemconfig(self.elements['status'], 
                             fill=status_colors.get(state, '#CCCCCC'))
    
    def animate_listening(self):
        """Animate eyes for listening state (pulsing green)."""
        if self.current_state != 'listening':
            return
            
        # Pulsing effect
        pulse = (math.sin(self.pulse_timer) + 1) / 2  # 0 to 1
        intensity = int(200 + 55 * pulse)  # Varies green intensity
        color = f"#{0:02x}{intensity:02x}{83:02x}"  # Green variations
        
        self.canvas.itemconfig(self.elements['left_eye'], fill=color)
        self.canvas.itemconfig(self.elements['right_eye'], fill=color)
        self.canvas.itemconfig(self.elements['status'], fill=color)
        
        self.pulse_timer += 0.3
    
    def animate_speaking(self):
        """Animate mouth for speaking state."""
        if self.current_state != 'speaking':
            return
            
        # Mouth movement simulation
        wave = math.sin(self.wave_timer)
        if wave > 0.5:
            # Open mouth more
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=0, extent=360, style='pieslice')
        elif wave > 0:
            # Partially open
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=0, extent=180, style='arc')
        else:
            # Closed/small opening
            self.canvas.itemconfig(self.elements['mouth'], 
                                 start=45, extent=90, style='arc')
        
        self.wave_timer += 0.5
    
    def animate_thinking(self):
        """Animate for thinking state (rotating eyes)."""
        if self.current_state != 'thinking':
            return
            
        # Rotating effect by changing eye positions slightly
        offset = math.sin(self.pulse_timer) * 3
        
        # Move eyes slightly to simulate "looking around"
        eye_coords_left = self.canvas.coords(self.elements['left_eye'])
        eye_coords_right = self.canvas.coords(self.elements['right_eye'])
        
        # Small movement
        for i in [0, 2]:  # x coordinates
            eye_coords_left[i] += offset
            eye_coords_right[i] += offset
        
        self.pulse_timer += 0.2
    
    def blink(self):
        """Make the robot blink occasionally."""
        if self.current_state == 'sleeping':
            return  # Don't blink when sleeping
            
        # Random blinking
        if time.time() - self.blink_timer > 3:  # Blink every ~3 seconds
            # Quick blink effect
            original_height = self.canvas.coords(self.elements['left_eye'])[3] - self.canvas.coords(self.elements['left_eye'])[1]
            
            # Shrink eyes vertically for blink
            self.canvas.after(50, self._restore_eyes)
            self.blink_timer = time.time()
    
    def _restore_eyes(self):
        """Restore eyes after blink."""
        self.update_state(self.current_state)


class VisualFeedbackSystem:
    """Main visual feedback system with GUI interface and robot face animations."""
    
    def __init__(self, width: int = 800, height: int = 480, current_user: str = None):
        """Initialize visual feedback system with user-specific customization."""
        self.config = VisualConfig()
        self.width = self.config.WINDOW_WIDTH if hasattr(self.config, 'WINDOW_WIDTH') else width
        self.height = self.config.WINDOW_HEIGHT if hasattr(self.config, 'WINDOW_HEIGHT') else height
        self.current_user = current_user or "default"
        
        # Determine face type based on current user
        self.face_type = self._get_face_type_for_user(self.current_user)
        
        self.window = None
        self.canvas = None
        self.robot_face = None
        self.message_queue = queue.Queue()
        self.running = False
        self.gui_thread = None
        
        # Window monitoring and recovery
        self.window_monitor_thread = None
        self.window_lost_count = 0
        self.max_window_recovery_attempts = 3
        
        # Message display
        self.current_message = "Ready to help!"
        self.message_label = None
        
        print(f"🎨 Visual feedback initialized for {self.current_user} with {self.face_type} face")
    
    def _get_face_type_for_user(self, user: str) -> str:
        """Determine the appropriate face type based on the user."""
        user_lower = user.lower() if user else "default"
        
        if "eladriel" in user_lower:
            return "dinosaur"
        elif "sophia" in user_lower:
            return "girl_robot"
        else:
            return "robot"  # Default friendly robot
    
    def update_user(self, new_user: str):
        """Update the current user and change face type accordingly."""
        if new_user != self.current_user:
            self.current_user = new_user
            new_face_type = self._get_face_type_for_user(new_user)
            
            if new_face_type != self.face_type:
                self.face_type = new_face_type
                print(f"🎨 Switching to {self.face_type} face for {new_user}")
                
                # Recreate the robot face if GUI is running
                if self.canvas and self.robot_face:
                    # Clear existing face
                    for element in self.robot_face.elements.values():
                        try:
                            self.canvas.delete(element)
                        except:
                            pass
                    
                    # Create new face with updated type
                    center_x = self.width // 2
                    center_y = (self.height // 2) - 50
                    self.robot_face = RobotFace(self.canvas, center_x, center_y, 120, self.face_type)
    
    def start(self):
        """Start the visual feedback system."""
        if self.running:
            return
            
        self.running = True
        
        # Create UI on main thread
        self._create_ui()
        
        # Start window monitoring for automatic recovery
        self._start_window_monitor()
        
        print("🎨 Visual feedback system started with monitoring")
    
    def stop(self):
        """Stop the visual feedback system."""
        self.running = False
        if self.window:
            try:
                self.window.quit()    # Exit mainloop
                self.window.destroy() # Destroy window
            except Exception as e:
                print(f"⚠️ Error closing window: {e}")
        print("🎨 Visual feedback system stopped")
    
    def _create_ui(self):
        """Create the main UI interface with personalized elements."""
        self.window = tk.Tk()
        self.window.title(f"AI Assistant - {self.current_user}'s Helper")
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg='#1E1E1E')
        
        # Make window always on top and remove decorations for kiosk mode
        self.window.attributes('-topmost', True)
        
        # Configure window close behavior
        def on_window_close():
            print("🎨 Visual feedback window minimized")
            self.window.iconify()  # Minimize instead of quit
        
        self.window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Main canvas for robot face
        self.canvas = tk.Canvas(
            self.window, 
            width=self.width, 
            height=self.height-100,
            bg='#1E1E1E',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create robot face in center
        center_x = self.width // 2
        center_y = (self.height // 2) - 50
        self.robot_face = RobotFace(self.canvas, center_x, center_y, 120, self.face_type)
        
        # Add decorative elements specific to each face type
        self._add_decorative_elements()
        
        # Message display area
        self.message_label = tk.Label(
            self.window,
            text=self.current_message,
            font=('Comic Sans MS', 16, 'bold'),
            fg='#FFFFFF',
            bg='#1E1E1E',
            wraplength=self.width-40,
            justify='center'
        )
        self.message_label.pack(side=tk.BOTTOM, pady=20)
        
        print(f"🎨 {self.face_type.title()} face created for {self.current_user}")
    
    def _add_decorative_elements(self):
        """Add decorative elements specific to each face type."""
        if self.face_type == "dinosaur":
            # Add cute dinosaur decorations
            # Small plants around the corners
            for x, y in [(50, 50), (self.width-50, 50), (50, self.height-150), (self.width-50, self.height-150)]:
                self.canvas.create_oval(x-15, y-5, x+15, y+25, fill='#4CAF50', outline='#2E7D32', width=2)
                self.canvas.create_rectangle(x-3, y+20, x+3, y+35, fill='#8BC34A', outline='#558B2F', width=1)
            
            # Prehistoric background pattern
            for i in range(0, self.width, 100):
                for j in range(0, self.height-100, 100):
                    if (i + j) % 200 == 0:
                        self.canvas.create_oval(i+80, j+80, i+90, j+90, fill='#C8E6C9', outline='')
        
        elif self.face_type == "girl_robot":
            # Add sparkles and hearts
            import random
            for _ in range(8):
                x = random.randint(50, self.width-50)
                y = random.randint(50, self.height-150)
                if abs(x - self.width//2) > 100 or abs(y - (self.height//2 - 50)) > 100:
                    # Sparkle
                    sparkle_size = random.randint(3, 8)
                    self.canvas.create_polygon(
                        x, y-sparkle_size, x+sparkle_size//2, y, x, y+sparkle_size, x-sparkle_size//2, y,
                        fill='#F8BBD9', outline='#E91E63', width=1
                    )
            
            # Hearts in corners
            for x, y in [(80, 80), (self.width-80, 80), (80, self.height-180), (self.width-80, self.height-180)]:
                # Heart shape
                self.canvas.create_oval(x-10, y-5, x, y+5, fill='#F8BBD9', outline='#E91E63', width=2)
                self.canvas.create_oval(x, y-5, x+10, y+5, fill='#F8BBD9', outline='#E91E63', width=2)
                self.canvas.create_polygon(x-10, y, x+10, y, x, y+15, fill='#F8BBD9', outline='#E91E63', width=2)
        
        else:  # default robot
            # Tech-style decorations
            # Circuit patterns
            for i in range(4):
                x = 30 + i * (self.width - 60) // 3
                y1 = 30
                y2 = self.height - 130
                
                self.canvas.create_line(x, y1, x, y1+20, fill='#BBDEFB', width=2)
                self.canvas.create_line(x, y2-20, x, y2, fill='#BBDEFB', width=2)
                self.canvas.create_oval(x-4, y1+16, x+4, y1+24, fill='#2196F3', outline='#1976D2', width=1)
                self.canvas.create_oval(x-4, y2-24, x+4, y2-16, fill='#2196F3', outline='#1976D2', width=1)
    
    def _process_messages(self):
        """Process messages from the queue and update the interface."""
        try:
            message_count = 0
            while not self.message_queue.empty() and message_count < 10:  # Limit processing per cycle
                try:
                    message = self.message_queue.get_nowait()
                    
                    # Validate message format
                    if not isinstance(message, tuple) or len(message) != 2:
                        print(f"⚠️ Invalid message format ignored: {message} (expected tuple with 2 elements)")
                        message_count += 1
                        continue
                    
                    message_type, data = message
                    
                    if message_type == 'state':
                        if self.robot_face:
                            self.robot_face.update_state(data)
                    elif message_type == 'message':
                        self.current_message = data
                        if self.message_label and self.message_label.winfo_exists():
                            self.message_label.config(text=data)
                    else:
                        print(f"⚠️ Unknown message type ignored: {message_type}")
                    
                    message_count += 1
                    
                except queue.Empty:
                    break
                except Exception as msg_error:
                    print(f"⚠️ Message processing exception handled gracefully: {msg_error}")
                    # Continue processing other messages
                    message_count += 1
        
        except Exception as e:
            print(f"⚠️ Error in message processing loop: {e}")
        finally:
            # Schedule next message processing - add extra safety checks
            try:
                if self.running and self.window and self.window.winfo_exists():
                    self.window.after(100, self._process_messages)
                elif self.running and not self.window:
                    print("⚠️ Window lost during message processing")
            except Exception as schedule_error:
                print(f"⚠️ Error scheduling next message processing: {schedule_error}")
    
    def _animation_loop(self):
        """Main animation loop for the robot face with improved error handling."""
        animation_error_count = 0
        max_errors = 5
        
        print("🎬 Starting animation loop...")
        
        while self.running:
            try:
                if self.robot_face and self.robot_face.animation_active:
                    # Check if canvas still exists before animating
                    if hasattr(self.robot_face, 'canvas') and self.robot_face.canvas:
                        try:
                            self.robot_face.canvas.winfo_exists()  # Test if canvas is valid
                            self.robot_face.blink()
                            animation_error_count = 0  # Reset error count on success
                        except tk.TclError as canvas_error:
                            print(f"⚠️ Canvas error in animation: {canvas_error}")
                            animation_error_count += 1
                            if animation_error_count >= max_errors:
                                print("❌ Too many animation errors, stopping animation")
                                break
                
                time.sleep(0.1)  # 100ms delay for smooth animation
                
            except Exception as e:
                animation_error_count += 1
                print(f"⚠️ Animation loop error ({animation_error_count}/{max_errors}): {e}")
                
                if animation_error_count >= max_errors:
                    print("❌ Too many animation errors, stopping animation loop")
                    break
                    
                time.sleep(1)  # Longer delay on error
        
        print("🎬 Animation loop stopped")
    
    def set_state(self, state: str, message: str = None):
        """Set the current state and update visual feedback accordingly."""
        try:
            if not isinstance(state, str):
                print(f"⚠️ Invalid state type: {type(state)} - {state}")
                return
            
            self.message_queue.put(('state', state))
            if message:
                if not isinstance(message, str):
                    print(f"⚠️ Invalid message type: {type(message)} - {message}")
                    return
                self.message_queue.put(('message', message))
            print(f"🎨 Visual feedback state changed to: {state}")
        except Exception as e:
            print(f"⚠️ Error setting visual state: {e}")
            import traceback
            traceback.print_exc()
    
    def set_message(self, message: str):
        """Update the display message."""
        try:
            self.message_queue.put(('message', message))
            print(f"💬 Visual feedback message: {message}")
        except Exception as e:
            print(f"⚠️ Error setting visual message: {e}")
    
    def show_standby(self, message: str = "Ready to help!"):
        """Show standby state."""
        self.set_state('standby', message)
    
    def show_listening(self, message: str = "I'm listening..."):
        """Show listening state."""
        self.set_state('listening', message)
    
    def show_speaking(self, message: str = "Speaking..."):
        """Show speaking state."""
        self.set_state('speaking', message)
    
    def show_thinking(self, message: str = "Let me think..."):
        """Show thinking state."""
        self.set_state('thinking', message)
    
    def show_happy(self, message: str = "Great job!"):
        """Show happy/celebration state."""
        self.set_state('happy', message)
    
    def show_error(self, message: str = "Oops! Something went wrong."):
        """Show error state."""
        self.set_state('error', message)
    
    def show_sleeping(self, message: str = "Sleeping..."):
        """Show sleeping state."""
        self.set_state('sleeping', message)
    
    def restore_window(self):
        """Restore the minimized window."""
        try:
            if self.window:
                self.window.deiconify()  # Restore from minimized state
                self.window.lift()       # Bring to front
                self.window.focus_force() # Give it focus
                print("🎨 Visual feedback window restored")
        except Exception as e:
            print(f"⚠️ Error restoring window: {e}")

    def run_gui(self):
        """Run the GUI main loop (blocking) with bulletproof exception handling and auto-recovery."""
        if not self.window:
            print("⚠️ No window to run GUI - visual feedback not started")
            return
            
        print("🎨 Starting visual feedback GUI main loop...")
        
        crash_count = 0
        max_crashes = 3
        
        while self.running and crash_count < max_crashes:
            try:
                # Start animation and message processing
                self.gui_thread = threading.Thread(target=self._animation_loop, daemon=True)
                self.gui_thread.start()
                self.window.after(100, self._process_messages)
                
                # Start the main GUI loop with exception handling
                while self.running and self.window:
                    try:
                        self.window.mainloop()
                        break  # Normal exit
                    except Exception as e:
                        print(f"⚠️ GUI mainloop error: {e}")
                        print("🔄 Attempting to recover GUI...")
                        
                        # Try to recover the window
                        try:
                            if self.window and self.window.winfo_exists():
                                self.window.update_idletasks()
                                self.window.update()
                                time.sleep(1)
                                continue
                            else:
                                print("❌ Window destroyed, recreating...")
                                self._recreate_window()
                                crash_count += 1
                                time.sleep(2)  # Brief pause before retry
                                break  # Break inner loop to retry outer loop
                        except Exception as recovery_error:
                            print(f"❌ Recovery failed: {recovery_error}")
                            crash_count += 1
                            break
                            
            except Exception as e:
                print(f"❌ Critical GUI error: {e}")
                crash_count += 1
                
                if crash_count < max_crashes:
                    print(f"🔄 Attempting auto-recovery ({crash_count}/{max_crashes})...")
                    try:
                        self._recreate_window()
                        time.sleep(2)  # Wait before retry
                    except Exception as recreate_error:
                        print(f"❌ Auto-recovery failed: {recreate_error}")
                        
        if crash_count >= max_crashes:
            print(f"❌ Visual feedback GUI failed {max_crashes} times - switching to minimal mode")
            # Fall back to minimal visual feedback that just prints to console
            self._switch_to_minimal_mode()
        else:
            print("🎨 Visual feedback GUI loop ended normally")
    
    def _switch_to_minimal_mode(self):
        """Switch to minimal console-only mode when GUI fails completely."""
        print("🔄 Switching to console-only visual feedback mode...")
        self.running = False  # Stop GUI attempts
        
        # Override key methods to work in console mode
        original_set_state = self.set_state
        
        def console_set_state(state: str, message: str = None):
            print(f"🎨 [CONSOLE MODE] State: {state}" + (f" - {message}" if message else ""))
        
        self.set_state = console_set_state
        print("✅ Console-only mode active - visual feedback will show in terminal")
    
    def _recreate_window(self):
        """Recreate the visual feedback window after a crash."""
        try:
            print("🔄 Recreating visual feedback window...")
            
            # Clear old window reference
            self.window = None
            self.canvas = None
            self.robot_face = None
            self.message_label = None
            
            # Create new UI
            self._create_ui()
            
            # Restore current state
            if hasattr(self, 'current_message'):
                self.set_message(self.current_message)
            
            print("✅ Visual feedback window recreated successfully")
            
        except Exception as e:
            print(f"❌ Failed to recreate window: {e}")
            self.running = False
    
    def _start_window_monitor(self):
        """Start window monitoring thread to detect and recover from window issues."""
        if self.window_monitor_thread and self.window_monitor_thread.is_alive():
            return
            
        def monitor_window():
            print("🔍 Starting window monitor...")
            
            while self.running:
                try:
                    time.sleep(5)  # Check every 5 seconds
                    
                    if not self.running:
                        break
                        
                    # Check if window still exists
                    if self.window:
                        try:
                            self.window.winfo_exists()
                            # Window is healthy, reset lost count
                            if self.window_lost_count > 0:
                                print("✅ Window recovered, resetting lost count")
                                self.window_lost_count = 0
                        except tk.TclError:
                            # Window is lost
                            self.window_lost_count += 1
                            print(f"⚠️ Window lost detected (attempt {self.window_lost_count}/{self.max_window_recovery_attempts})")
                            
                            if self.window_lost_count <= self.max_window_recovery_attempts:
                                print("🔄 Attempting automatic window recovery...")
                                try:
                                    self._recreate_window()
                                    if self.window:
                                        print("✅ Window automatically recovered")
                                        self.window_lost_count = 0
                                except Exception as recovery_error:
                                    print(f"❌ Automatic recovery failed: {recovery_error}")
                            else:
                                print("❌ Maximum recovery attempts reached, stopping monitoring")
                                break
                    else:
                        # No window at all
                        if self.running:
                            print("⚠️ No window found, attempting to create one...")
                            try:
                                self._create_ui()
                                if self.window:
                                    print("✅ Window created successfully")
                            except Exception as create_error:
                                print(f"❌ Failed to create window: {create_error}")
                
                except Exception as monitor_error:
                    print(f"⚠️ Window monitor error: {monitor_error}")
                    time.sleep(5)
            
            print("🔍 Window monitor stopped")
        
        self.window_monitor_thread = threading.Thread(target=monitor_window, daemon=True)
        self.window_monitor_thread.start()
    
    def _check_window_health(self):
        """Check if the window is healthy and responsive."""
        try:
            if not self.window:
                return False
                
            # Test if window exists and is responsive
            self.window.winfo_exists()
            self.window.update_idletasks()
            return True
            
        except Exception as e:
            print(f"⚠️ Window health check failed: {e}")
            return False


class MinimalVisualFeedback:
    """Lightweight visual feedback for resource-constrained environments."""
    
    def __init__(self):
        """Initialize minimal visual feedback using console output."""
        self.current_state = "standby"
        
        # State indicators
        self.indicators = {
            'standby': '😴',
            'listening': '👂',
            'speaking': '🗣️',
            'thinking': '🤔',
            'happy': '😊',
            'error': '😵',
            'sleeping': '💤'
        }
    
    def set_state(self, state: str, message: str = None):
        """Set state with console output."""
        if state in self.indicators:
            indicator = self.indicators[state]
            output = f"{indicator} {state.upper()}"
            if message:
                output += f" - {message}"
            
            print(f"\n[ROBOT STATUS] {output}\n")
            self.current_state = state
    
    # Same convenience methods as full system
    def show_standby(self, message: str = "Ready to help!"):
        self.set_state('standby', message)
    
    def show_listening(self, message: str = "I'm listening..."):
        self.set_state('listening', message)
    
    def show_speaking(self, message: str = "Speaking..."):
        self.set_state('speaking', message)
    
    def show_thinking(self, message: str = "Let me think..."):
        self.set_state('thinking', message)
    
    def show_happy(self, message: str = "Great job!"):
        self.set_state('happy', message)
    
    def show_error(self, message: str = "Oops! Something went wrong."):
        self.set_state('error', message)
    
    def show_sleeping(self, message: str = "Sleeping..."):
        self.set_state('sleeping', message)
    
    def start(self):
        """Start minimal feedback."""
        self.show_standby()
    
    def stop(self):
        """Stop minimal feedback."""
        print("\n[ROBOT STATUS] 🔴 OFFLINE\n")


def create_visual_feedback(use_gui: bool = True, current_user: str = None) -> VisualFeedbackSystem:
    """
    Factory function to create appropriate visual feedback system.
    
    Args:
        use_gui: Whether to use GUI interface
        current_user: Current user name for personalized experience
        
    Returns:
        VisualFeedbackSystem instance
    """
    try:
        config = VisualConfig()
        
        # Get config values with defaults
        window_width = getattr(config, 'WINDOW_WIDTH', 800)
        window_height = getattr(config, 'WINDOW_HEIGHT', 480)
        use_gui_setting = getattr(config, 'USE_GUI', True)
        
        if use_gui and use_gui_setting:
            return VisualFeedbackSystem(
                width=window_width,
                height=window_height,
                current_user=current_user
            )
        else:
            return MinimalVisualFeedback()
            
    except Exception as e:
        print(f"Error creating visual feedback: {e}")
        return MinimalVisualFeedback() 