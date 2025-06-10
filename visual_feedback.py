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


class RobotFace:
    """Cute animated robot face with different expressions and states."""
    
    def __init__(self, canvas: tk.Canvas, center_x: int, center_y: int, size: int = 100):
        """Initialize robot face at given position and size."""
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.elements = {}
        self.animation_active = False
        self.current_state = "standby"
        
        # Animation variables
        self.blink_timer = 0
        self.pulse_timer = 0
        self.wave_timer = 0
        
        # Colors for different states
        self.colors = {
            'standby': {'face': '#E8F4FD', 'eyes': '#4A90E2', 'mouth': '#666666'},
            'listening': {'face': '#E8F8F5', 'eyes': '#00C853', 'mouth': '#4CAF50'},
            'speaking': {'face': '#FFF3E0', 'eyes': '#FF9800', 'mouth': '#F57C00'},
            'thinking': {'face': '#F3E5F5', 'eyes': '#9C27B0', 'mouth': '#7B1FA2'},
            'happy': {'face': '#E8F5E8', 'eyes': '#4CAF50', 'mouth': '#2E7D32'},
            'error': {'face': '#FFEBEE', 'eyes': '#F44336', 'mouth': '#C62828'},
            'sleeping': {'face': '#F5F5F5', 'eyes': '#9E9E9E', 'mouth': '#757575'}
        }
        
        self.create_face()
    
    def create_face(self):
        """Create the basic robot face structure."""
        # Face outline (circle)
        self.elements['face'] = self.canvas.create_oval(
            self.center_x - self.size//2, self.center_y - self.size//2,
            self.center_x + self.size//2, self.center_y + self.size//2,
            fill=self.colors['standby']['face'], 
            outline='#CCCCCC', 
            width=3
        )
        
        # Left eye
        eye_offset_x = self.size // 4
        eye_offset_y = self.size // 6
        eye_size = self.size // 8
        
        self.elements['left_eye'] = self.canvas.create_oval(
            self.center_x - eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x - eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#333333', 
            width=2
        )
        
        # Right eye
        self.elements['right_eye'] = self.canvas.create_oval(
            self.center_x + eye_offset_x - eye_size, self.center_y - eye_offset_y - eye_size,
            self.center_x + eye_offset_x + eye_size, self.center_y - eye_offset_y + eye_size,
            fill=self.colors['standby']['eyes'], 
            outline='#333333', 
            width=2
        )
        
        # Mouth
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
        
        # Status indicator (small circle on forehead)
        self.elements['status'] = self.canvas.create_oval(
            self.center_x - 8, self.center_y - self.size//3 - 8,
            self.center_x + 8, self.center_y - self.size//3 + 8,
            fill='#CCCCCC', 
            outline='#999999', 
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
    """Main visual feedback system for the AI Assistant robot."""
    
    def __init__(self, width: int = 800, height: int = 480):
        """Initialize the visual feedback system."""
        self.width = width
        self.height = height
        self.window = None
        self.canvas = None
        self.robot_face = None
        self.status_text = None
        self.message_queue = queue.Queue()
        
        self.logger = logging.getLogger(__name__)
        
        # Thread control
        self.running = False
        self.animation_thread = None
        
        # Current status
        self.current_state = "standby"
        self.current_message = "Ready to help!"
        
        self.logger.info("Visual Feedback System initialized")
    
    def start(self):
        """Start the visual feedback system."""
        if self.running:
            return
            
        self.running = True
        
        # Create UI on main thread
        self._create_ui()
        
        self.logger.info("Visual feedback system started")
    
    def stop(self):
        """Stop the visual feedback system."""
        self.running = False
        if self.window:
            self.window.quit()
        self.logger.info("Visual feedback system stopped")
    
    def _create_ui(self):
        """Create the main UI window."""
        self.window = tk.Tk()
        self.window.title("AI Assistant Robot - Visual Feedback")
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg='#1A1A1A')  # Dark background
        
        # Make it fullscreen for Raspberry Pi
        # self.window.attributes('-fullscreen', True)  # Uncomment for Pi
        
        # Main canvas for drawing
        self.canvas = tk.Canvas(
            self.window, 
            width=self.width, 
            height=self.height-100,
            bg='#1A1A1A',
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Robot face
        face_x = self.width // 2
        face_y = (self.height - 100) // 2
        self.robot_face = RobotFace(self.canvas, face_x, face_y, 120)
        
        # Status text
        self.status_text = self.canvas.create_text(
            face_x, face_y + 120,
            text=self.current_message,
            fill='#FFFFFF',
            font=('Arial', 16, 'bold')
        )
        
        # Add decorative elements
        self._add_decorative_elements()
        
        # Start animation thread after UI is created
        self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.animation_thread.start()
        
        # Process message queue
        self.window.after(100, self._process_messages)
        
        # Set up close protocol
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
    
    def run_gui(self):
        """Run the GUI main loop (blocking)."""
        if self.window:
            self.window.mainloop()
    
    def _add_decorative_elements(self):
        """Add decorative elements to make it more engaging."""
        # Corner decorations
        for x in [50, self.width-50]:
            for y in [50, self.height-150]:
                self.canvas.create_oval(
                    x-5, y-5, x+5, y+5,
                    fill='#333333', outline='#555555'
                )
        
        # Side status bars
        for i in range(5):
            y = 100 + i * 40
            self.canvas.create_rectangle(
                20, y, 40, y+20,
                fill='#333333', outline='#555555'
            )
            self.canvas.create_rectangle(
                self.width-40, y, self.width-20, y+20,
                fill='#333333', outline='#555555'
            )
    
    def _process_messages(self):
        """Process messages from the queue."""
        try:
            while not self.message_queue.empty():
                message_type, data = self.message_queue.get_nowait()
                
                if message_type == 'state':
                    self.current_state = data
                    if self.robot_face:
                        self.robot_face.update_state(data)
                
                elif message_type == 'message':
                    self.current_message = data
                    if self.status_text:
                        self.canvas.itemconfig(self.status_text, text=data)
        
        except queue.Empty:
            pass
        
        if self.running and self.window:
            self.window.after(100, self._process_messages)
    
    def _animation_loop(self):
        """Main animation loop."""
        while self.running:
            try:
                if self.robot_face:
                    # Run state-specific animations
                    if self.current_state == 'listening':
                        self.robot_face.animate_listening()
                    elif self.current_state == 'speaking':
                        self.robot_face.animate_speaking()
                    elif self.current_state == 'thinking':
                        self.robot_face.animate_thinking()
                    
                    # Always try to blink
                    self.robot_face.blink()
                
                time.sleep(0.1)  # 10 FPS
            except Exception as e:
                self.logger.error(f"Animation loop error: {e}")
                time.sleep(0.5)
    
    def set_state(self, state: str, message: str = None):
        """Set the current state and optional message."""
        try:
            self.message_queue.put(('state', state))
            if message:
                self.message_queue.put(('message', message))
            
            self.logger.info(f"Visual feedback state changed to: {state}")
            if message:
                self.logger.info(f"Visual feedback message: {message}")
        except Exception as e:
            self.logger.error(f"Error setting visual state: {e}")
    
    def set_message(self, message: str):
        """Set just the message without changing state."""
        try:
            self.message_queue.put(('message', message))
        except Exception as e:
            self.logger.error(f"Error setting visual message: {e}")
    
    # Convenience methods for different states
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
        """Show happy state."""
        self.set_state('happy', message)
    
    def show_error(self, message: str = "Oops! Something went wrong."):
        """Show error state."""
        self.set_state('error', message)
    
    def show_sleeping(self, message: str = "Sleeping..."):
        """Show sleeping state."""
        self.set_state('sleeping', message)


class MinimalVisualFeedback:
    """Lightweight visual feedback for resource-constrained environments."""
    
    def __init__(self):
        """Initialize minimal visual feedback using console output."""
        self.logger = logging.getLogger(__name__)
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
            self.logger.info(f"Robot state: {state} - {message or 'No message'}")
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


def create_visual_feedback(use_gui: bool = True) -> VisualFeedbackSystem:
    """Factory function to create appropriate visual feedback system."""
    try:
        if use_gui:
            return VisualFeedbackSystem()
        else:
            return MinimalVisualFeedback()
    except Exception as e:
        logging.getLogger(__name__).warning(f"Failed to create GUI feedback, using minimal: {e}")
        return MinimalVisualFeedback() 