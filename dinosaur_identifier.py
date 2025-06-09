#!/usr/bin/env python3
"""
Dinosaur Identification Module for Eladriel
Uses OpenAI GPT-4 Vision to identify dinosaur toys and provide fun facts
"""

import base64
import logging
from typing import Optional, Dict, Any
import openai
from camera_utils import CameraManager

logger = logging.getLogger(__name__)

class DinosaurIdentifier:
    """Identifies dinosaurs from camera images and provides educational content."""
    
    def __init__(self, openai_client, config):
        """Initialize dinosaur identifier."""
        self.client = openai_client
        self.config = config
        self.camera_manager = CameraManager()
        
        # Dinosaur knowledge base for enhanced responses
        self.dinosaur_facts = {
            "t-rex": {
                "name": "Tyrannosaurus Rex",
                "period": "Late Cretaceous",
                "diet": "Carnivore",
                "size": "40 feet long, 12 feet tall",
                "fun_fact": "T-Rex had teeth as big as bananas and could bite with the force of 12,800 pounds!"
            },
            "triceratops": {
                "name": "Triceratops",
                "period": "Late Cretaceous", 
                "diet": "Herbivore",
                "size": "30 feet long, 10 feet tall",
                "fun_fact": "Triceratops had a frill that could be 7 feet across - like a giant shield!"
            },
            "stegosaurus": {
                "name": "Stegosaurus",
                "period": "Late Jurassic",
                "diet": "Herbivore", 
                "size": "30 feet long, 14 feet tall",
                "fun_fact": "Stegosaurus had a brain the size of a walnut but spikes on its tail called a 'thagomizer'!"
            },
            "brachiosaurus": {
                "name": "Brachiosaurus",
                "period": "Late Jurassic",
                "diet": "Herbivore",
                "size": "85 feet long, 40 feet tall",
                "fun_fact": "Brachiosaurus was so tall it could peek into a 4-story building!"
            }
        }
        
        logger.info("DinosaurIdentifier initialized for Eladriel!")
    
    def capture_and_identify(self) -> Dict[str, Any]:
        """Capture image and identify the dinosaur."""
        try:
            # Capture image
            logger.info("📸 Capturing dinosaur image...")
            image_path = self.camera_manager.capture_image()
            
            if not image_path:
                return {
                    "success": False,
                    "error": "Failed to capture image",
                    "message": "Hmm, I couldn't take a picture. Is your camera working?"
                }
            
            # Identify dinosaur using GPT-4 Vision
            identification = self._identify_dinosaur_with_vision(image_path)
            
            if identification["success"]:
                # Enhance with local knowledge
                enhanced_response = self._enhance_response(identification)
                return enhanced_response
            else:
                return identification
                
        except Exception as e:
            logger.error(f"Error in capture_and_identify: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Oops! Something went wrong while trying to identify your dinosaur."
            }
    
    def _identify_dinosaur_with_vision(self, image_path: str) -> Dict[str, Any]:
        """Use OpenAI GPT-4 Vision to identify the dinosaur."""
        try:
            # Encode image to base64
            base64_image = self.camera_manager.encode_image_to_base64(image_path)
            
            if not base64_image:
                return {
                    "success": False,
                    "error": "Failed to encode image",
                    "message": "I couldn't process the image properly."
                }
            
            # Create vision prompt for dinosaur identification
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """You are helping a kid named Eladriel who LOVES dinosaurs! 
                            
Look at this image and:
1. Identify what dinosaur toy/figure this is (be specific about the dinosaur name)
2. If it's not a dinosaur, identify what it is but relate it to dinosaurs if possible
3. Share 2-3 amazing, kid-friendly facts about this dinosaur
4. Make your response exciting and engaging for a curious child!
5. Keep it educational but fun

Format your response as:
DINOSAUR: [Name]
TYPE: [Carnivore/Herbivore/etc]
PERIOD: [When it lived]
COOL FACTS: [2-3 fun facts]

If it's not a dinosaur, still be enthusiastic and educational!"""
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
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "ai_response": ai_response,
                "image_path": image_path,
                "message": ai_response
            }
            
        except Exception as e:
            logger.error(f"Vision API error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I had trouble looking at the picture. Maybe try again?"
            }
    
    def _enhance_response(self, identification: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance the AI response with local dinosaur knowledge."""
        try:
            ai_response = identification["ai_response"].lower()
            
            # Check if we have additional facts for this dinosaur
            enhanced_facts = []
            for dino_key, facts in self.dinosaur_facts.items():
                if dino_key in ai_response or facts["name"].lower() in ai_response:
                    enhanced_facts.append(f"🦕 Extra cool fact: {facts['fun_fact']}")
                    break
            
            # Add encouraging message for Eladriel
            eladriel_message = "\n\n🌟 Wow Eladriel! You have such awesome dinosaur toys! Keep exploring and learning about these amazing creatures!"
            
            enhanced_response = identification["ai_response"]
            if enhanced_facts:
                enhanced_response += "\n\n" + "\n".join(enhanced_facts)
            enhanced_response += eladriel_message
            
            identification["message"] = enhanced_response
            identification["enhanced"] = True
            
            return identification
            
        except Exception as e:
            logger.error(f"Error enhancing response: {e}")
            return identification
    
    def test_camera(self) -> bool:
        """Test if camera is working for dinosaur identification."""
        return self.camera_manager.test_camera()
    
    def show_camera_preview(self, duration: int = 5) -> bool:
        """Show camera preview so Eladriel can see what the camera sees."""
        print("📸 Eladriel, look at the camera window to see what I can see!")
        return self.camera_manager.show_preview(duration)
    
    def get_dinosaur_tips(self) -> str:
        """Get tips for better dinosaur identification."""
        tips = """
🦕 Tips for better dinosaur identification:

1. 📸 Hold your dinosaur toy steady in front of the camera
2. 💡 Make sure there's good lighting
3. 🎯 Get close enough so I can see the details
4. 🔄 If I don't recognize it, try a different angle
5. 🌟 Clean dinosaur toys work better than dusty ones!

Ready to show me your awesome dinosaur collection?
        """
        return tips.strip()
    
    def cleanup(self):
        """Clean up camera resources."""
        self.camera_manager.cleanup()
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass 