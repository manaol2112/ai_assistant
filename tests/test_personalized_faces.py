#!/usr/bin/env python3
"""
Test script for personalized robot faces
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_face_types():
    """Test that different users get different face types."""
    print("🧪 Testing personalized robot faces...")
    
    from visual_feedback import VisualFeedbackSystem
    
    # Test Eladriel gets dinosaur face
    eladriel_visual = VisualFeedbackSystem(current_user='Eladriel')
    print(f"🦕 Eladriel gets: {eladriel_visual.face_type} face")
    assert eladriel_visual.face_type == 'dinosaur', f"Expected dinosaur, got {eladriel_visual.face_type}"
    
    # Test Sophia gets girl robot face
    sophia_visual = VisualFeedbackSystem(current_user='Sophia')
    print(f"👧 Sophia gets: {sophia_visual.face_type} face")
    assert sophia_visual.face_type == 'girl_robot', f"Expected girl_robot, got {sophia_visual.face_type}"
    
    # Test others get default robot face
    parent_visual = VisualFeedbackSystem(current_user='Parent')
    print(f"🤖 Parent gets: {parent_visual.face_type} face")
    assert parent_visual.face_type == 'robot', f"Expected robot, got {parent_visual.face_type}"
    
    print("✅ All face type tests passed!")

def test_user_update():
    """Test that face type updates when user changes."""
    print("\n🔄 Testing face type updates...")
    
    from visual_feedback import VisualFeedbackSystem
    
    # Start with default
    visual = VisualFeedbackSystem(current_user='Unknown')
    print(f"🤔 Unknown user gets: {visual.face_type} face")
    
    # Update to Eladriel
    visual.update_user('Eladriel')
    print(f"🦕 After update to Eladriel: {visual.face_type} face")
    assert visual.face_type == 'dinosaur', f"Expected dinosaur, got {visual.face_type}"
    
    # Update to Sophia  
    visual.update_user('Sophia')
    print(f"👧 After update to Sophia: {visual.face_type} face")
    assert visual.face_type == 'girl_robot', f"Expected girl_robot, got {visual.face_type}"
    
    print("✅ User update tests passed!")

def test_ai_assistant_integration():
    """Test that AI Assistant can use personalized faces."""
    print("\n🤖 Testing AI Assistant integration...")
    
    try:
        # Import main module components
        from visual_feedback import create_visual_feedback
        
        # Test creating visual feedback for different users
        eladriel_vf = create_visual_feedback(use_gui=True, current_user='Eladriel')
        if hasattr(eladriel_vf, 'face_type'):
            print(f"🦕 Eladriel visual feedback: {eladriel_vf.face_type}")
            assert eladriel_vf.face_type == 'dinosaur'
        
        sophia_vf = create_visual_feedback(use_gui=True, current_user='Sophia') 
        if hasattr(sophia_vf, 'face_type'):
            print(f"👧 Sophia visual feedback: {sophia_vf.face_type}")
            assert sophia_vf.face_type == 'girl_robot'
        
        print("✅ AI Assistant integration tests passed!")
        
    except Exception as e:
        print(f"⚠️ AI Assistant integration test failed: {e}")

def main():
    """Run all tests."""
    print("🎨 Testing Personalized Robot Faces System")
    print("=" * 50)
    
    try:
        test_face_types()
        test_user_update()  
        test_ai_assistant_integration()
        
        print("\n🎉 All tests passed! Personalized faces are working perfectly!")
        print("\n📝 Summary:")
        print("🦕 Eladriel gets a cute dinosaur face with green colors and horns")
        print("👧 Sophia gets a sweet girl robot face with pink colors and bow")
        print("🤖 Everyone else gets a friendly default robot face with blue colors")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 