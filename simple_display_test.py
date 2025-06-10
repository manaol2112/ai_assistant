#!/usr/bin/env python3
"""
Simple pygame display test for macOS debugging
"""

import pygame
import sys
import os
import time

def test_pygame_basic():
    """Test basic pygame functionality step by step."""
    print("🔍 Testing pygame step by step...")
    
    try:
        print("1. Setting environment variables...")
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        print("2. Initializing pygame...")
        pygame.init()
        
        print("3. Getting display info...")
        info = pygame.display.Info()
        print(f"   Display size: {info.w}x{info.h}")
        
        print("4. Trying different screen modes...")
        
        # Try different approaches
        approaches = [
            ("Standard mode", lambda: pygame.display.set_mode((640, 480))),
            ("With flags", lambda: pygame.display.set_mode((640, 480), pygame.SHOWN)),
            ("Smaller size", lambda: pygame.display.set_mode((320, 240))),
            ("Legacy mode", lambda: pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)),
        ]
        
        for name, create_func in approaches:
            try:
                print(f"   Trying {name}...")
                screen = create_func()
                if screen:
                    size = screen.get_size()
                    print(f"   ✅ Success! Size: {size}")
                    
                    # Test drawing
                    screen.fill((255, 0, 0))  # Red background
                    pygame.display.flip()
                    
                    print(f"   Window should be visible now (Red background)")
                    print(f"   Waiting 3 seconds...")
                    time.sleep(3)
                    
                    pygame.quit()
                    return True
                else:
                    print(f"   ❌ Screen is None")
            except Exception as e:
                print(f"   ❌ Failed: {e}")
        
        print("❌ All approaches failed")
        return False
        
    except Exception as e:
        print(f"❌ General error: {e}")
        return False

def test_headless_detection():
    """Test if we're actually in headless mode."""
    print("\n🔍 Checking environment...")
    
    env_vars = ['DISPLAY', 'SSH_CLIENT', 'SSH_TTY', 'TERM', 'XDG_SESSION_TYPE']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"   {var}: {value}")
    
    print(f"   Platform: {sys.platform}")
    
    # Check if we're running in an IDE or terminal
    if 'SSH_CLIENT' in os.environ or 'SSH_TTY' in os.environ:
        print("   🔍 Running via SSH - headless mode")
        return True
    elif os.environ.get('TERM_PROGRAM') == 'vscode':
        print("   🔍 Running in VS Code")
        return False
    elif os.environ.get('DISPLAY') is None and sys.platform.startswith('linux'):
        print("   🔍 No DISPLAY set on Linux - headless mode")
        return True
    else:
        print("   🔍 Should have display access")
        return False

if __name__ == "__main__":
    print("🖥️ macOS Display Debugging Tool")
    print("=" * 50)
    
    # Test environment
    is_headless = test_headless_detection()
    
    if is_headless:
        print("\n⚠️  Detected headless environment - display may not work")
    else:
        print("\n✅ Environment should support display")
    
    # Test pygame
    success = test_pygame_basic()
    
    if success:
        print("\n✅ pygame display is working!")
    else:
        print("\n❌ pygame display is not working on this system")
        print("\n💡 Possible solutions:")
        print("   1. Try running from Terminal.app instead of an IDE")
        print("   2. Install XQuartz if using X11 forwarding")
        print("   3. Use a different video driver")
        print("   4. The system may require display permission") 