#!/usr/bin/env python3
"""
Quick Pi 5 Fix Script
Applies immediate fixes to resolve speech recognition getting stuck in listening mode.
"""

import os
import shutil
from pathlib import Path

def backup_and_fix_voice_detector():
    """Backup and fix the voice activity detector for Pi 5."""
    
    print("🔧 APPLYING QUICK PI 5 SPEECH RECOGNITION FIX")
    print("=" * 60)
    
    # Backup original file
    original_file = "voice_activity_detector.py"
    backup_file = "voice_activity_detector.py.backup"
    
    if not os.path.exists(backup_file):
        shutil.copy2(original_file, backup_file)
        print(f"✅ Backed up {original_file} to {backup_file}")
    
    # Read the original file
    with open(original_file, 'r') as f:
        content = f.read()
    
    # Apply Pi 5 specific fixes
    fixes_applied = []
    
    # Fix 1: Reduce silence threshold for Pi 5
    if 'silence_threshold = silence_threshold * settings[\'silence_tolerance_base\']' in content:
        content = content.replace(
            'silence_threshold = silence_threshold * settings[\'silence_tolerance_base\']',
            '''# Pi 5 SPECIFIC FIX: Reduce silence threshold for better responsiveness
            if self.platform_info['name'] == 'Raspberry Pi 5':
                silence_threshold = min(1.5, silence_threshold * settings['silence_tolerance_base'] * 0.7)
            else:
                silence_threshold = silence_threshold * settings['silence_tolerance_base']'''
        )
        fixes_applied.append("Reduced silence threshold for Pi 5")
    
    # Fix 2: Faster timeout detection for Pi 5
    if 'chunk_duration = settings[\'chunk_duration_base\']' in content:
        content = content.replace(
            'chunk_duration = settings[\'chunk_duration_base\']',
            '''# Pi 5 SPECIFIC FIX: Faster chunk processing
                    if self.platform_info['name'] == 'Raspberry Pi 5':
                        chunk_duration = settings['chunk_duration_base'] * 0.8  # Faster for Pi 5
                    else:
                        chunk_duration = settings['chunk_duration_base']'''
        )
        fixes_applied.append("Faster chunk processing for Pi 5")
    
    # Fix 3: Less strict AI speech detection for Pi 5
    if 'def is_ai_speech(self, text: str) -> bool:' in content:
        # Find the function and make it less strict for Pi 5
        lines = content.split('\n')
        new_lines = []
        in_ai_speech_function = False
        
        for line in lines:
            if 'def is_ai_speech(self, text: str) -> bool:' in line:
                in_ai_speech_function = True
                new_lines.append(line)
                new_lines.append('        """Check if text is AI speech - less strict for Pi 5."""')
                new_lines.append('        # Pi 5 SPECIFIC FIX: Be less strict about AI speech detection')
                new_lines.append('        if self.platform_info[\'name\'] == \'Raspberry Pi 5\':')
                new_lines.append('            # Only filter very obvious AI phrases on Pi 5')
                new_lines.append('            obvious_ai_phrases = [')
                new_lines.append('                "automatic conversation mode activated",')
                new_lines.append('                "i\'m listening",')
                new_lines.append('                "say goodbye to end",')
                new_lines.append('                "conversation mode"')
                new_lines.append('            ]')
                new_lines.append('            text_lower = text.lower().strip()')
                new_lines.append('            return any(phrase in text_lower for phrase in obvious_ai_phrases)')
                new_lines.append('')
                continue
            elif in_ai_speech_function and line.strip().startswith('def '):
                in_ai_speech_function = False
            
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        fixes_applied.append("Less strict AI speech detection for Pi 5")
    
    # Write the fixed file
    with open(original_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Applied {len(fixes_applied)} fixes:")
    for fix in fixes_applied:
        print(f"   • {fix}")
    
    return len(fixes_applied) > 0

def fix_main_listen_timeout():
    """Fix the main.py listen timeout to be more forgiving."""
    
    print("\n🔧 FIXING MAIN.PY LISTEN TIMEOUT")
    print("=" * 60)
    
    main_file = "main.py"
    backup_file = "main.py.backup"
    
    if not os.path.exists(backup_file):
        shutil.copy2(main_file, backup_file)
        print(f"✅ Backed up {main_file} to {backup_file}")
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    # Fix the silence threshold in main.py for Pi 5
    if 'silence_threshold=2.5,' in content:
        content = content.replace(
            'silence_threshold=2.5,',
            'silence_threshold=1.8,  # Pi 5 FIX: Reduced from 2.5 to 1.8'
        )
        print("✅ Reduced silence threshold in main.py from 2.5 to 1.8 seconds")
        
        with open(main_file, 'w') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Apply all quick fixes."""
    print("🚀 QUICK PI 5 SPEECH RECOGNITION FIX")
    print("🎯 This will resolve the 'stuck listening' issue")
    print("=" * 60)
    
    fixes_applied = 0
    
    # Fix 1: Voice Activity Detector
    if backup_and_fix_voice_detector():
        fixes_applied += 1
    
    # Fix 2: Main.py timeout
    if fix_main_listen_timeout():
        fixes_applied += 1
    
    print("\n" + "=" * 60)
    print("📊 QUICK FIX SUMMARY")
    print("=" * 60)
    
    if fixes_applied > 0:
        print(f"✅ Applied {fixes_applied} fixes successfully!")
        print("\n🚀 NEXT STEPS:")
        print("1. Copy these files to your Pi 5:")
        print("   • voice_activity_detector.py")
        print("   • main.py")
        print("2. Run: python3 main.py")
        print("3. Test speech recognition with face detection")
        print("\n💡 If still having issues, run:")
        print("   python3 test_pi5_audio_debug.py")
    else:
        print("⚠️ No fixes were needed or could be applied")
        print("💡 Run the diagnostic script:")
        print("   python3 test_pi5_audio_debug.py")

if __name__ == "__main__":
    main() 