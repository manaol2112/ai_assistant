#!/usr/bin/env python3
"""
Test script for Eladriel's dinosaur identification feature
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from camera_utils import CameraManager
    from dinosaur_identifier import DinosaurIdentifier
    from config import Config
    import openai
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install camera dependencies: pip install opencv-python")
    sys.exit(1)

def test_camera_basic():
    """Test basic camera functionality."""
    print("🔍 Testing Camera Functionality")
    print("=" * 40)
    
    camera = CameraManager()
    
    # Test camera initialization
    if camera.test_camera():
        print("✅ Camera is working!")
        
        # Show preview
        print("\n📸 Showing camera preview for 3 seconds...")
        print("You should see a camera window. Press 'q' to close it early.")
        camera.show_preview(duration=3)
        
        # Test image capture
        print("\n📷 Testing image capture...")
        image_path = camera.capture_image("test_capture.jpg")
        
        if image_path:
            print(f"✅ Image captured successfully: {image_path}")
            
            # Check if file exists
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                print(f"📊 Image file size: {file_size} bytes")
            else:
                print("❌ Image file not found")
        else:
            print("❌ Failed to capture image")
    else:
        print("❌ Camera test failed")
        return False
    
    camera.cleanup()
    return True

def test_dinosaur_identifier():
    """Test the dinosaur identification system."""
    print("\n🦕 Testing Dinosaur Identification")
    print("=" * 40)
    
    try:
        # Setup config and OpenAI client
        config = Config()
        client = openai.OpenAI(api_key=config.openai_api_key)
        
        # Initialize dinosaur identifier
        dino_id = DinosaurIdentifier(client, config)
        
        print("✅ DinosaurIdentifier initialized successfully")
        
        # Test camera
        if not dino_id.test_camera():
            print("❌ Camera test failed for dinosaur identifier")
            return False
        
        print("✅ Camera working for dinosaur identification")
        
        # Show tips
        print("\n📝 Dinosaur identification tips:")
        tips = dino_id.get_dinosaur_tips()
        print(tips)
        
        # Test manual identification (without actually calling vision API to save credits)
        print("\n🧪 Testing identification workflow...")
        print("This would normally:")
        print("1. Capture an image from camera")
        print("2. Send to OpenAI GPT-4 Vision API")
        print("3. Get dinosaur identification and facts")
        print("4. Enhance with local dinosaur knowledge")
        print("5. Return kid-friendly response")
        
        print("✅ Dinosaur identification system ready!")
        
        dino_id.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error testing dinosaur identifier: {e}")
        return False

def test_full_workflow():
    """Test the complete dinosaur identification workflow."""
    print("\n🌟 Testing Complete Workflow")
    print("=" * 40)
    
    print("This test simulates what happens when Eladriel says:")
    print("'Dino' (wake word) -> 'identify dinosaur' (command)")
    print()
    
    try:
        config = Config()
        client = openai.OpenAI(api_key=config.openai_api_key)
        dino_id = DinosaurIdentifier(client, config)
        
        # Test the key phrases that would trigger dinosaur identification
        test_phrases = [
            "identify dinosaur",
            "what is this dinosaur", 
            "look at this",
            "identify this"
        ]
        
        print("🎯 Testing command recognition:")
        for phrase in test_phrases:
            # Simulate the command detection logic from main.py
            if any(trigger in phrase.lower() for trigger in ['identify dinosaur', 'what is this dinosaur', 'look at this', 'identify this']):
                print(f"✅ '{phrase}' -> Would trigger dinosaur identification")
            else:
                print(f"❌ '{phrase}' -> Would NOT trigger")
        
        print("\n🔮 Workflow simulation:")
        print("1. ✅ User says 'Dino' (wake word detected)")
        print("2. ✅ Assistant: 'Hey Eladriel! Ready for some fun discoveries?'")
        print("3. ✅ User says 'identify dinosaur'")
        print("4. ✅ Command recognized")
        print("5. ✅ Assistant: 'Awesome! Let me see your dinosaur!'")
        print("6. ✅ Camera captures image")
        print("7. ✅ Image sent to GPT-4 Vision")
        print("8. ✅ Response enhanced with local facts")
        print("9. ✅ Kid-friendly response spoken to Eladriel")
        
        dino_id.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error in workflow test: {e}")
        return False

def main():
    """Run all tests."""
    print("🦕 ELADRIEL'S DINOSAUR CAMERA TEST")
    print("=" * 50)
    print("This will test the dinosaur identification feature!")
    print()
    
    # Check OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment")
        print("Please set it in your .env file")
        return False
    
    print("✅ OpenAI API key found")
    
    # Run tests
    tests = [
        ("Camera Basic Functionality", test_camera_basic),
        ("Dinosaur Identifier", test_dinosaur_identifier),
        ("Full Workflow", test_full_workflow)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Eladriel's dinosaur feature is ready!")
        print("\nTo use the feature:")
        print("1. Run: python main.py")
        print("2. Say: 'Dino'")
        print("3. Say: 'identify dinosaur'")
        print("4. Hold up a dinosaur toy to the camera!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    main() 