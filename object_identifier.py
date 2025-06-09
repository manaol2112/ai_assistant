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

logger = logging.getLogger(__name__)

class ObjectIdentifier:
    """Identifies any object from camera images and provides comprehensive educational content."""
    
    def __init__(self):
        """Initialize the Object Identifier with OpenAI API."""
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.camera_manager = CameraManager()
        
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
    
    def capture_and_identify(self, user: str = "sophia") -> Dict[str, Any]:
        """Capture image and identify the object with educational information."""
        try:
            # Capture image
            logger.info("📸 Capturing object image...")
            image_path = self.camera_manager.capture_image()
            
            if not image_path:
                return {
                    "success": False,
                    "error": "Failed to capture image",
                    "message": "Hmm, I couldn't take a picture. Is the camera working?"
                }
            
            # Identify object using GPT-4 Vision
            identification = self._identify_object_with_vision(image_path, user)
            
            if identification["success"]:
                return identification
            else:
                return identification
                
        except Exception as e:
            logger.error(f"Error in capture_and_identify: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Oops! Something went wrong while trying to identify your object."
            }
    
    def _identify_object_with_vision(self, image_path: str, user: str) -> Dict[str, Any]:
        """Use OpenAI GPT-4 Vision to identify the object and provide educational information."""
        try:
            # Encode image to base64
            base64_image = self.camera_manager.encode_image_to_base64(image_path)
            
            if not base64_image:
                return {
                    "success": False,
                    "error": "Failed to encode image",
                    "message": "I couldn't process the image properly."
                }
            
            # Create personalized vision prompt based on user
            if user.lower() == "eladriel":
                prompt = self._get_eladriel_prompt()
            else:  # Default to Sophia
                prompt = self._get_sophia_prompt()
            
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
                "user": user
            }
            
        except Exception as e:
            logger.error(f"Vision API error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I had trouble looking at the picture. Maybe try again?"
            }
    
    def _get_sophia_prompt(self) -> str:
        """Get identification prompt tailored for Sophia."""
        return """You are helping a curious child named Sophia who loves to learn! 

Look at this image and give a SHORT, fun response about the object:

🔍 WHAT IS IT: Name the object in 1-2 words
🎨 QUICK LOOK: One sentence about its color/shape
✨ COOL TRIVIA: Share 1-2 amazing facts that will make Sophia say "WOW!"
🌟 WHY IT'S AWESOME: One sentence about why it's useful or special

Keep it SHORT and exciting - like telling a friend something super cool you just learned! Use emojis and make it fun!"""
    
    def _get_eladriel_prompt(self) -> str:
        """Get identification prompt tailored for Eladriel (with dinosaur connections when possible)."""
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
            return self.camera_manager.show_preview(duration)
        except Exception as e:
            logger.error(f"Error showing camera preview: {e}")
            return False
    
    def test_camera(self) -> bool:
        """Test if camera is working properly."""
        try:
            return self.camera_manager.test_camera()
        except Exception as e:
            logger.error(f"Camera test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up camera resources."""
        try:
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

# Example usage
if __name__ == "__main__":
    identifier = ObjectIdentifier()
    
    # Test with a sample image (you would replace with actual image path)
    # result = identifier.identify_object("path/to/your/image.jpg")
    # print(result)
    
    # Test getting information about a specific object
    info = identifier.get_object_info("telescope")
    print(info) 