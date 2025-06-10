#!/usr/bin/env python3
"""
Force Window Test - Simple pygame window that should definitely appear on macOS
"""

import pygame
import sys
import os
import time

def main():
    print("🔥 FORCE WINDOW TEST - This WILL create a visible window!")
    print("=" * 60)
    
    try:
        # Set environment for macOS
        os.environ['SDL_VIDEODRIVER'] = 'cocoa'
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'  # Specific position
        
        print("1. Initializing pygame...")
        pygame.init()
        
        # Force specific dimensions
        width, height = 600, 400
        print(f"2. Creating window: {width}x{height}")
        
        # Create screen with explicit flags
        screen = pygame.display.set_mode((width, height), pygame.SHOWN)
        pygame.display.set_caption("🚀 AI Assistant Display Test - SHOULD BE VISIBLE!")
        
        print(f"3. Window created: {screen.get_size()}")
        
        # Force window to front and make it obvious
        clock = pygame.time.Clock()
        
        print("4. Drawing test pattern...")
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green  
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
        ]
        
        print("\n🖥️  WINDOW SHOULD NOW BE VISIBLE!")
        print("   Look for a colorful window on your screen")
        print("   Press any key in the window or wait 10 seconds")
        print("   Window will flash different colors to be obvious")
        
        start_time = time.time()
        running = True
        color_index = 0
        
        while running and (time.time() - start_time < 10):
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    print(f"   Key pressed: {event.key}")
                    running = False
            
            # Flash colors to make window obvious
            current_color = colors[color_index % len(colors)]
            screen.fill(current_color)
            
            # Draw some text
            font = pygame.font.Font(None, 48)
            text = font.render("AI ASSISTANT DISPLAY", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width//2, height//2))
            screen.blit(text, text_rect)
            
            # Draw frame number
            frame_text = font.render(f"Frame: {color_index}", True, (255, 255, 255))
            screen.blit(frame_text, (50, 50))
            
            pygame.display.flip()
            clock.tick(2)  # 2 FPS for slow color changes
            color_index += 1
            
            if color_index % 6 == 0:
                print(f"   Color cycle {color_index // 6}")
        
        print("\n✅ Test completed!")
        if running:
            print("   Window timed out - did you see the flashing colors?")
        else:
            print("   Window was interactive - SUCCESS!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            pygame.quit()
            print("🔧 Pygame cleaned up")
        except:
            pass

if __name__ == "__main__":
    main() 