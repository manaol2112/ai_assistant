#!/usr/bin/env python3
"""
Visual Demo of Personalized Robot Faces
Shows the different face designs for each child
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tkinter as tk
from visual_feedback import VisualFeedbackSystem
import threading
import time

class FaceDemo:
    def __init__(self):
        self.demo_window = None
        self.faces = {}
        
    def create_demo_window(self):
        """Create a demonstration window showing all face types."""
        self.demo_window = tk.Tk()
        self.demo_window.title("AI Assistant - Personalized Robot Faces Demo")
        self.demo_window.geometry("1200x600")
        self.demo_window.configure(bg='#2C2C2C')
        
        # Title
        title_label = tk.Label(
            self.demo_window,
            text="🎨 Personalized Robot Faces for Each Child",
            font=('Comic Sans MS', 24, 'bold'),
            fg='#FFFFFF',
            bg='#2C2C2C'
        )
        title_label.pack(pady=20)
        
        # Create frames for each face type
        faces_frame = tk.Frame(self.demo_window, bg='#2C2C2C')
        faces_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Eladriel's Dinosaur Face
        self._create_face_demo(faces_frame, "Eladriel", "dinosaur", 0, 
                              "🦕 Cute Dinosaur Face", 
                              "Green colors, horns, teeth, prehistoric theme")
        
        # Sophia's Girl Robot Face  
        self._create_face_demo(faces_frame, "Sophia", "girl_robot", 1,
                              "👧 Sweet Girl Robot", 
                              "Pink colors, bow, eyelashes, sparkles & hearts")
        
        # Default Robot Face
        self._create_face_demo(faces_frame, "Parent", "robot", 2,
                              "🤖 Friendly Robot", 
                              "Blue colors, antennae, digital eyes, tech theme")
        
        # Control buttons
        button_frame = tk.Frame(self.demo_window, bg='#2C2C2C')
        button_frame.pack(pady=20)
        
        # Animation buttons
        tk.Button(button_frame, text="😊 Happy", command=self.show_happy,
                 font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🎤 Listening", command=self.show_listening,
                 font=('Arial', 12, 'bold'), bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="💭 Thinking", command=self.show_thinking,
                 font=('Arial', 12, 'bold'), bg='#9C27B0', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗣️ Speaking", command=self.show_speaking,
                 font=('Arial', 12, 'bold'), bg='#FF9800', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Close button
        tk.Button(self.demo_window, text="Close Demo", command=self.close_demo,
                 font=('Arial', 14, 'bold'), bg='#F44336', fg='white').pack(pady=10)
        
    def _create_face_demo(self, parent, user_name, face_type, column, title, description):
        """Create a demo section for one face type."""
        # Frame for this face
        face_frame = tk.Frame(parent, bg='#3C3C3C', relief=tk.RAISED, bd=2)
        face_frame.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        
        # Title
        title_label = tk.Label(face_frame, text=title, 
                              font=('Comic Sans MS', 16, 'bold'),
                              fg='#FFFFFF', bg='#3C3C3C')
        title_label.pack(pady=10)
        
        # Face canvas
        canvas = tk.Canvas(face_frame, width=300, height=300, bg='#1E1E1E', highlightthickness=0)
        canvas.pack(pady=10)
        
        # Create the robot face
        from visual_feedback import RobotFace
        robot_face = RobotFace(canvas, 150, 150, 100, face_type)
        self.faces[user_name] = robot_face
        
        # Description
        desc_label = tk.Label(face_frame, text=description,
                             font=('Arial', 10), fg='#CCCCCC', bg='#3C3C3C',
                             wraplength=280, justify=tk.CENTER)
        desc_label.pack(pady=10)
        
        # User name
        user_label = tk.Label(face_frame, text=f"For: {user_name}",
                             font=('Arial', 12, 'bold'), fg='#FFC107', bg='#3C3C3C')
        user_label.pack(pady=5)
    
    def show_happy(self):
        """Show happy state on all faces."""
        for face in self.faces.values():
            face.update_state('happy')
    
    def show_listening(self):
        """Show listening state on all faces."""
        for face in self.faces.values():
            face.update_state('listening')
    
    def show_thinking(self):
        """Show thinking state on all faces."""
        for face in self.faces.values():
            face.update_state('thinking')
    
    def show_speaking(self):
        """Show speaking state on all faces."""
        for face in self.faces.values():
            face.update_state('speaking')
    
    def close_demo(self):
        """Close the demo window."""
        if self.demo_window:
            self.demo_window.destroy()
    
    def run(self):
        """Run the face demo."""
        print("🎨 Starting personalized robot faces demo...")
        self.create_demo_window()
        self.demo_window.mainloop()

def main():
    """Main function to run the demo."""
    print("🎨 Welcome to the Personalized Robot Faces Demo!")
    print("This demo shows the different face designs for each child:")
    print("🦕 Eladriel gets a cute dinosaur face")
    print("👧 Sophia gets a sweet girl robot face") 
    print("🤖 Parents get a friendly default robot face")
    print("\nStarting demo window...")
    
    demo = FaceDemo()
    demo.run()

if __name__ == "__main__":
    main() 