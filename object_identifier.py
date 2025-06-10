#!/usr/bin/env python3
"""
Universal Object Identification Module for Sophia and Eladriel
Uses OpenAI GPT-4 Vision to identify any object and provide educational information
"""

import base64
import logging
from typing import Optional, Dict, Any
import openai
from camera_utils import CameraManager
import os
from pathlib import Path
import cv2
import time
from .config import Config
from .logger import Logger

logger = logging.getLogger(__name__)

class ObjectIdentifier:
    """Identifies any object from camera images and provides comprehensive educational content."""
    
    def __init__(self, shared_camera: Optional[Any] = None):
        """Initialize the Object Identifier with optional shared camera."""
        self.logger = Logger("ObjectIdentifier")
        self.config = Config()
        
        # Camera configuration
        self.shared_camera = shared_camera
        self.using_shared_camera = shared_camera is not None
        
        if self.using_shared_camera:
            self.logger.info("ObjectIdentifier initialized with shared camera")
        else:
            self.logger.info("ObjectIdentifier initialized with standalone camera")
            self.camera_manager = CameraManager()
        
        # Initialize OpenAI client
        try:
            openai.api_key = self.config.openai_api_key
            self.logger.info("OpenAI API initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI API: {e}")
        
        # Object categories for enhanced responses
        self.object_categories = {
            "toys": {
                "description": "Fun playthings that help children learn and develop",
                "educational_focus": ["creativity", "motor skills", "imagination", "social skills"]
            },
            "household_items": {
                "description": "Everyday objects we use in our homes",
                "educational_focus": ["daily life", "responsibility", "organization", "safety"]
            },
            "tools": {
                "description": "Objects that help us accomplish tasks",
                "educational_focus": ["problem solving", "craftsmanship", "engineering", "safety"]
            },
            "books": {
                "description": "Sources of knowledge and entertainment",
                "educational_focus": ["reading", "learning", "imagination", "knowledge"]
            },
            "art_supplies": {
                "description": "Materials for creative expression",
                "educational_focus": ["creativity", "self-expression", "fine motor skills", "color theory"]
            },
            "electronics": {
                "description": "Devices that use electricity to function",
                "educational_focus": ["technology", "innovation", "digital literacy", "safety"]
            },
            "clothing": {
                "description": "Items we wear for protection and style",
                "educational_focus": ["self-care", "weather protection", "cultural expression", "materials"]
            },
            "food_items": {
                "description": "Things we eat for nutrition and enjoyment",
                "educational_focus": ["nutrition", "health", "cooking", "cultural diversity"]
            },
            "nature_items": {
                "description": "Objects from the natural world",
                "educational_focus": ["science", "environment", "biology", "conservation"]
            },
            "vehicles": {
                "description": "Objects that help us travel and transport things",
                "educational_focus": ["transportation", "engineering", "physics", "safety"]
            }
        }
        
        logger.info("ObjectIdentifier initialized for comprehensive object recognition!")
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 string."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image: {e}")
            raise
    
    def identify_object(self, image_path: str, user_question: Optional[str] = None) -> Dict[str, Any]:
        """
        Identify objects in an image and provide educational information.
        
        Args:
            image_path: Path to the image file
            user_question: Optional specific question about the object
            
        Returns:
            Dictionary containing identification results and educational info
        """
        try:
            # Validate image file exists
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Encode image
            base64_image = self.encode_image(image_path)
            
            # Prepare the prompt
            if user_question:
                prompt = f"""Please analyze this image and answer the specific question: "{user_question}"
                
Additionally, provide:
1. Object identification and description
2. Educational information about the object(s)
3. Interesting facts or context
4. Any safety considerations if applicable

Please be detailed and educational in your response."""
            else:
                prompt = """Please analyze this image and provide:

1. **Object Identification**: What objects do you see in the image?
2. **Detailed Description**: Describe the main object(s) in detail
3. **Educational Information**: Share interesting facts, history, or scientific information about the object(s)
4. **Context**: Where might this object typically be found or used?
5. **Safety Information**: Any important safety considerations (if applicable)

Please be thorough and educational in your response, as if teaching someone who is curious to learn."""
            
            # Make API call to OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Updated to current model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extract response
            identification_result = response.choices[0].message.content
            
            return {
                "success": True,
                "identification": identification_result,
                "image_path": image_path,
                "user_question": user_question,
                "model_used": "gpt-4o"
            }
            
        except Exception as e:
            logger.error(f"Error identifying object: {e}")
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path,
                "user_question": user_question
            }
    
    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific object by name.
        
        Args:
            object_name: Name of the object to get information about
            
        Returns:
            Dictionary containing detailed object information
        """
        try:
            prompt = f"""Please provide comprehensive educational information about: {object_name}

Include:
1. **Definition and Description**: What is this object?
2. **History and Origin**: When and where was it developed?
3. **How it Works**: Technical or functional details
4. **Uses and Applications**: What is it used for?
5. **Interesting Facts**: Fun or surprising information
6. **Variations**: Different types or models
7. **Safety Considerations**: Any important safety information
8. **Related Objects**: Similar or related items

Please be detailed and educational."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Updated to current model
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            object_info = response.choices[0].message.content
            
            return {
                "success": True,
                "object_name": object_name,
                "information": object_info,
                "model_used": "gpt-4o"
            }
            
        except Exception as e:
            logger.error(f"Error getting object information: {e}")
            return {
                "success": False,
                "error": str(e),
                "object_name": object_name
            }
    
    def capture_and_identify(self) -> Dict[str, Any]:
        """Capture an image and identify the object."""
        try:
            # Check camera availability
            if self.using_shared_camera and not self.shared_camera:
                return {
                    "success": False,
                    "error": "Shared camera not available",
                    "message": "The camera is not available for object identification."
                }
            
            # Capture image
            if self.using_shared_camera:
                ret, frame = self.shared_camera.read()
                if not ret:
                    return {
                        "success": False,
                        "error": "Failed to capture image from shared camera",
                        "message": "I couldn't take a picture. The camera might be busy."
                    }
            else:
                frame = self.camera_manager.capture_frame()
                if frame is None:
                    return {
                        "success": False,
                        "error": "Failed to capture frame",
                        "message": "I couldn't take a picture. Please check the camera connection."
                    }
            
            # Create directory for captured images
            capture_dir = "captured_images"
            os.makedirs(capture_dir, exist_ok=True)
            
            # Save the captured image
            timestamp = int(time.time())
            image_path = os.path.join(capture_dir, f"object_{timestamp}.jpg")
            
            success = cv2.imwrite(image_path, frame)
            if not success:
                return {
                    "success": False,
                    "error": "Failed to save image",
                    "message": "I took a picture but couldn't save it."
                }
            
            self.logger.info(f"Image captured and saved: {image_path}")
            
            # Identify the object using GPT-4 Vision
            return self._identify_object_with_vision(image_path)
            
        except Exception as e:
            self.logger.error(f"Error in capture_and_identify: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "An error occurred while trying to identify the object."
            }
    
    def _identify_object_with_vision(self, image_path: str) -> Dict[str, Any]:
        """Use OpenAI GPT-4 Vision to identify the object and provide educational information."""
        try:
            # Encode image to base64
            if self.using_shared_camera:
                # For shared camera, encode the image file directly
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                # For standalone camera manager, use its method
                base64_image = self.camera_manager.encode_image_to_base64(image_path)
            
            if not base64_image:
                return {
                    "success": False,
                    "error": "Failed to encode image",
                    "message": "I couldn't process the image properly."
                }

            # Create personalized vision prompt based on user
            if self.using_shared_camera:
                prompt = self._get_shared_camera_prompt()
            else:
                prompt = self._get_standalone_camera_prompt()
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
            
            # Call GPT-4 Vision
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "ai_response": ai_response,
                "image_path": image_path,
                "message": ai_response,
                "model_used": "gpt-4o"
            }
            
        except Exception as e:
            logger.error(f"Vision API error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I had trouble looking at the picture. Maybe try again?"
            }
    
    def _get_shared_camera_prompt(self) -> str:
        """Get identification prompt tailored for shared camera."""
        return """You are helping a curious child named Sophia who loves to learn! 

Look at this image and give a SHORT, fun response about the object:

🔍 WHAT IS IT: Name the object in 1-2 words
🎨 QUICK LOOK: One sentence about its color/shape
✨ COOL TRIVIA: Share 1-2 amazing facts that will make Sophia say "WOW!"
🌟 WHY IT'S AWESOME: One sentence about why it's useful or special

Keep it SHORT and exciting - like telling a friend something super cool you just learned! Use emojis and make it fun!"""
    
    def _get_standalone_camera_prompt(self) -> str:
        """Get identification prompt tailored for standalone camera."""
        return """You are helping an adventurous child named Eladriel who LOVES dinosaurs and exploring! 

Look at this image and give a SHORT, exciting response:

🔍 WHAT IS IT: Name the object in 1-2 words
🦕 DINOSAUR CONNECTION: If possible, connect it to dinosaurs or prehistoric times (1 sentence)
🚀 COOL DISCOVERY: Share 1-2 mind-blowing facts that will amaze Eladriel
🌟 ADVENTURE FACT: One sentence about how explorers or scientists use this

Keep it SHORT and adventurous - like sharing an exciting discovery! Use emojis and make it feel like an expedition!"""
    
    def get_identification_tips(self, user: str = "sophia") -> str:
        """Get tips for better object identification."""
        if user.lower() == "eladriel":
            return """🦕 ELADRIEL'S OBJECT IDENTIFICATION ADVENTURE GUIDE! 🦕

🎯 HOW TO SHOW OBJECTS:
• Hold the object steady in front of the camera
• Make sure there's good lighting (like a dinosaur explorer needs!)
• Get close enough so I can see all the details
• Try to have a plain background behind the object

🔍 WHAT I CAN IDENTIFY:
• Dinosaur toys and figures (my specialty!)
• Any toys and games
• Household items and tools
• Books and art supplies
• Electronics and gadgets
• Clothing and accessories
• Food items and kitchen tools
• Nature items like rocks, leaves, shells
• Vehicles and transportation toys

🌟 BEST RESULTS:
• One object at a time works best
• Clean the object if it's dusty (like a fossil!)
• Hold it still for 2-3 seconds
• Ask "What is this?" or "Identify this object!"

🦕 SPECIAL FEATURES:
• I'll connect things to dinosaurs when possible!
• I'll share adventure and exploration facts
• I'll tell you about discoveries and inventions
• I'll make learning feel like an expedition!

Ready for some object identification adventures? Show me what you've discovered! 🚀"""
        
        else:  # Sophia
            return """🌟 SOPHIA'S OBJECT IDENTIFICATION GUIDE! 🌟

🎯 HOW TO SHOW OBJECTS:
• Hold the object steady in front of the camera
• Make sure there's good lighting
• Get close enough so I can see all the details clearly
• Try to have a clean background behind the object

🔍 WHAT I CAN IDENTIFY:
• Toys and games
• Household items and tools
• Books and educational materials
• Art and craft supplies
• Electronics and devices
• Clothing and accessories
• Food items and kitchen utensils
• Nature items like flowers, rocks, leaves
• Musical instruments
• Sports equipment

🌟 BEST RESULTS:
• Show one object at a time
• Make sure the object is clean and visible
• Hold it steady for a few seconds
• Ask "What is this?" or "Tell me about this object!"

✨ WHAT YOU'LL LEARN:
• The name and purpose of the object
• Interesting colors, shapes, and materials
• How it works and why it's useful
• Cool historical facts and stories
• Fun facts that will amaze you
• Safety tips and proper usage

I love helping you learn about the world around you! Show me anything you're curious about! 📚✨"""
    
    def show_camera_preview(self, duration: int = 5) -> bool:
        """Show camera preview to help users position objects."""
        try:
            logger.info(f"Showing camera preview for {duration} seconds...")
            if self.using_shared_camera:
                # For shared camera, we can't show preview as it would conflict
                logger.info("Using shared camera - preview not available in shared mode")
                return True  # Return success but don't actually show preview
            else:
                return self.camera_manager.show_preview(duration)
        except Exception as e:
            logger.error(f"Error showing camera preview: {e}")
            return False
    
    def test_camera(self) -> bool:
        """Test if camera is working properly."""
        try:
            if self.using_shared_camera:
                return self.shared_camera.is_camera_available()
            else:
                return self.camera_manager.test_camera()
        except Exception as e:
            logger.error(f"Camera test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up camera resources."""
        try:
            if self.using_shared_camera:
                logger.info("ObjectIdentifier cleanup - shared camera remains active")
            else:
                self.camera_manager.cleanup()
                logger.info("ObjectIdentifier cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_object_categories(self) -> Dict[str, Any]:
        """Get information about object categories that can be identified."""
        return self.object_categories
    
    def enhance_response_with_category(self, response: str, detected_category: str) -> str:
        """Enhance the AI response with category-specific educational information."""
        if detected_category.lower() in self.object_categories:
            category_info = self.object_categories[detected_category.lower()]
            enhancement = f"\n\n🎓 LEARNING CATEGORY: {detected_category.title()}\n"
            enhancement += f"📖 About this category: {category_info['description']}\n"
            enhancement += f"🧠 Educational focus: {', '.join(category_info['educational_focus'])}"
            return response + enhancement
        return response 

    def capture_and_identify_text(self, user: str = "sophia", expected_word: str = None) -> Dict[str, Any]:
        """
        Capture an image and identify text/handwriting with enhanced OCR for spelling verification.
        
        Args:
            user: The user for personalized messaging
            expected_word: The word we expect to see (for spelling games)
            
        Returns:
            Dictionary with text detection results
        """
        try:
            logger.info(f"Capturing image for text identification - Expected: '{expected_word}'")
            
            # Capture image using appropriate camera handler
            if self.using_shared_camera:
                # Use shared camera handler
                if not self.shared_camera:
                    return {
                        "success": False,
                        "message": "Shared camera not available for text capture.",
                        "detected_text": "",
                        "image_path": None
                    }
                
                # Capture frame and save as image
                ret, frame = self.shared_camera.read()
                if not ret:
                    return {
                        "success": False,
                        "message": "Failed to capture image for text reading.",
                        "detected_text": "",
                        "image_path": None
                    }
                
                # Save frame as image file
                timestamp = int(time.time())
                image_path = f"captured_images/text_capture_{timestamp}.jpg"
                
                # Create directory if it doesn't exist
                os.makedirs("captured_images", exist_ok=True)
                
                # Save the captured frame
                success = cv2.imwrite(image_path, frame)
                if not success:
                    return {
                        "success": False,
                        "message": "Failed to save captured image for text reading.",
                        "detected_text": "",
                        "image_path": None
                    }
            else:
                # Use standalone camera manager
                image_path = self.camera_manager.capture_image()
                if not image_path:
                    return {
                        "success": False,
                        "message": "Failed to capture image. Please check the camera.",
                        "detected_text": "",
                        "image_path": None
                    }
            
            # Identify text with enhanced prompts for handwriting
            result = self._identify_text_with_vision(image_path, user, expected_word)
            
            # Cleanup - remove temporary image file
            try:
                os.remove(image_path)
            except:
                pass
            
            return result
            
        except Exception as e:
            logger.error(f"Error in text capture and identification: {e}")
            return {
                "success": False,
                "message": f"Error during text identification: {str(e)}",
                "detected_text": "",
                "image_path": None
            }

    def _identify_text_with_vision(self, image_path: str, user: str, expected_word: str = None) -> Dict[str, Any]:
        """Use GPT-4 Vision to identify handwritten text with OCR focus."""
        try:
            # Encode image for Vision API
            base64_image = self.encode_image(image_path)
            
            # Create enhanced prompt for text/handwriting recognition
            if expected_word:
                prompt = f"""HANDWRITING AND TEXT RECOGNITION TASK:

You are analyzing an image of handwritten text, specifically looking for a word that should spell: "{expected_word.upper()}"

Please perform these tasks:
1. **OCR ANALYSIS**: Extract ALL visible text, letters, and words from the image
2. **HANDWRITING FOCUS**: Pay special attention to handwritten letters and words
3. **SPELLING VERIFICATION**: Determine if the handwritten word matches "{expected_word}"
4. **DETAILED DESCRIPTION**: Describe exactly what letters/words you can see

CRITICAL: For the spelling game verification, I need you to:
- State clearly if you can see the word "{expected_word}" written correctly
- If you see other text, tell me exactly what letters/words are visible
- Be precise about spelling - even one wrong letter means incorrect spelling

Format your response as:
DETECTED TEXT: [exact letters/words you can see]
SPELLING MATCH: [YES/NO - does it match "{expected_word}" exactly?]
DESCRIPTION: [detailed description of what's written]

Remember: This is for educational spelling practice, so accuracy is crucial!"""
            else:
                prompt = """HANDWRITING AND TEXT RECOGNITION:

Please analyze this image and extract any visible text, handwriting, or letters.

Provide:
1. **DETECTED TEXT**: All visible text, letters, and words
2. **HANDWRITING ANALYSIS**: Description of any handwritten content
3. **TEXT QUALITY**: Assessment of legibility and clarity
4. **DETAILED DESCRIPTION**: What you can see in the image

Be as precise as possible in identifying text and letters."""
            
            # Make Vision API call
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1  # Low temperature for more consistent OCR results
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Parse detected text from the response
            detected_text = self._extract_detected_text(ai_response)
            
            logger.info(f"Text identification complete - Expected: '{expected_word}', Detected: '{detected_text}'")
            
            return {
                "success": True,
                "message": ai_response,
                "detected_text": detected_text,
                "image_path": image_path,
                "model_used": "gpt-4o",
                "expected_word": expected_word
            }
            
        except Exception as e:
            logger.error(f"Error in Vision API text identification: {e}")
            return {
                "success": False,
                "message": f"Sorry, I had trouble reading the text in your image. Error: {str(e)}",
                "detected_text": "",
                "image_path": image_path
            }

    def _extract_detected_text(self, ai_response: str) -> str:
        """Extract the detected text from AI response."""
        try:
            import re
            
            # Look for "DETECTED TEXT:" pattern
            pattern = r"DETECTED TEXT:\s*([^\n\r]+)"
            match = re.search(pattern, ai_response, re.IGNORECASE)
            
            if match:
                detected = match.group(1).strip()
                # Clean up common OCR artifacts
                detected = re.sub(r'[\[\]"]', '', detected)  # Remove brackets and quotes
                detected = detected.strip()
                return detected
            
            # Fallback: look for quoted text
            quote_patterns = [
                r'"([^"]+)"',
                r"'([^']+)'",
                r"`([^`]+)`"
            ]
            
            for pattern in quote_patterns:
                matches = re.findall(pattern, ai_response)
                if matches:
                    return matches[0].strip()
            
            # Last resort: extract first word-like sequence
            word_match = re.search(r'\b[a-zA-Z]{2,}\b', ai_response)
            if word_match:
                return word_match.group(0).strip()
            
            return ""  # No text detected
            
        except Exception as e:
            logger.error(f"Error extracting detected text: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    identifier = ObjectIdentifier()
    
    # Test with a sample image (you would replace with actual image path)
    # result = identifier.identify_object("path/to/your/image.jpg")
    # print(result)
    
    # Test getting information about a specific object
    info = identifier.get_object_info("telescope")
    print(info) 