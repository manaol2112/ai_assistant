#!/usr/bin/env python3
"""
Animal & Dinosaur Guessing Game for AI Assistant
Interactive game where kids show animal toys/figures to the camera for identification and trivia
Reuses existing ObjectIdentifier functionality with specialized prompts for animals and dinosaurs
"""

import logging
import random
import time
from typing import Dict, Any, List, Optional
from object_identifier import ObjectIdentifier

logger = logging.getLogger(__name__)

class AnimalGuessGame:
    """Interactive animal and dinosaur identification game for kids."""
    
    def __init__(self, ai_assistant=None):
        """Initialize the Animal Guess Game."""
        self.ai_assistant = ai_assistant
        self.object_identifier = ObjectIdentifier()
        self.game_active = False
        self.score = 0
        self.animals_identified = []
        self.current_user = None
        
        # Fun animal facts for bonus trivia
        self.bonus_facts = {
            "dinosaur": [
                "Some dinosaurs had feathers just like birds today!",
                "The word 'dinosaur' means 'terrible lizard' in Greek!",
                "Not all dinosaurs were huge - some were as small as chickens!",
                "Dinosaurs lived on Earth for over 160 million years!",
                "Birds are actually living dinosaurs - they're descendants of theropods!"
            ],
            "mammal": [
                "All mammals have hair or fur at some point in their lives!",
                "Mammals are warm-blooded, which means they control their own body temperature!",
                "Baby mammals drink milk from their mothers!",
                "The blue whale is the largest mammal and the largest animal ever!"
            ],
            "bird": [
                "Birds are the only animals alive today that have feathers!",
                "Some birds can fly backwards - like hummingbirds!",
                "Penguins are birds but they can't fly - they're amazing swimmers instead!",
                "The ostrich is the largest bird and can run up to 45 mph!"
            ],
            "reptile": [
                "Reptiles are cold-blooded and need the sun to warm up!",
                "Snakes can unhinge their jaws to eat prey bigger than their head!",
                "Some lizards can regrow their tails if they lose them!",
                "Crocodiles have been around since the time of dinosaurs!"
            ]
        }
        
        logger.info("AnimalGuessGame initialized successfully!")
    
    def start_game(self, user: str) -> str:
        """Start the animal guessing game."""
        self.current_user = user.lower()
        self.game_active = True
        self.score = 0
        self.animals_identified = []
        
        user_name = user.title()
        
        welcome_message = f"""🦕🐾 WELCOME TO THE ANIMAL GUESSING GAME! 🐾🦕

Hey {user_name}! I'm so excited to play with you! 

🎮 HOW TO PLAY:
• Show me any animal toy, figure, or picture
• I'll try to guess what animal it is
• I'll tell you amazing facts about your animal
• You can show me as many animals as you want!

🏆 WHAT I CAN IDENTIFY:
• Dinosaur toys and figures 🦕🦖
• Animal toys and stuffed animals 🐻🐯
• Pictures of real animals 📸
• Action figures and collectibles 🎭

🌟 SPECIAL FEATURES:
• Cool trivia and fun facts
• Learn about different animal types
• Discover amazing animal abilities
• Build your animal knowledge!

Ready to start? Just say "guess the animal" and show me your first creature! 🎉"""

        if self.ai_assistant:
            self.ai_assistant.speak(f"Welcome to the Animal Guessing Game, {user_name}! Get ready for some amazing animal discoveries!", user)
        
        return welcome_message
    
    def handle_animal_guess(self, user: str) -> str:
        """Handle the main animal guessing functionality."""
        if not self.game_active:
            return self.start_game(user)
        
        try:
            user_name = user.title()
            
            # Encourage the user
            encouragement = random.choice([
                f"Awesome {user_name}! Show me your animal!",
                f"I can't wait to see what creature you have, {user_name}!",
                f"This is going to be exciting, {user_name}! Let me see!",
                f"Ready for another amazing animal, {user_name}!"
            ])
            
            if self.ai_assistant:
                self.ai_assistant.speak(f"{encouragement} Hold it steady in front of the camera...", user)
            
            # Give user time to position the animal
            time.sleep(3)
            
            # Use the existing object identifier with specialized animal prompt
            result = self._identify_animal_with_vision(user)
            
            if result["success"]:
                self.score += 1
                response = self._format_animal_response(result, user)
                
                # Add to identified animals list
                if "animal_name" in result:
                    self.animals_identified.append(result["animal_name"])
                
                return response
            else:
                return f"Hmm, I had trouble seeing your animal clearly, {user_name}. {result.get('message', '')} Try holding it closer to the camera with good lighting!"
                
        except Exception as e:
            logger.error(f"Error in animal guessing: {e}")
            return "Oops! Something went wrong with the camera. Let's try again!"
    
    def _identify_animal_with_vision(self, user: str) -> Dict[str, Any]:
        """Use the existing ObjectIdentifier with specialized animal prompts."""
        try:
            # Capture image using existing camera functionality
            image_path = self.object_identifier.camera_manager.capture_image()
            
            if not image_path:
                return {
                    "success": False,
                    "message": "Failed to capture image. Please check the camera."
                }
            
            # Encode image to base64
            base64_image = self.object_identifier.camera_manager.encode_image_to_base64(image_path)
            
            if not base64_image:
                return {
                    "success": False,
                    "message": "I couldn't process the image properly."
                }
            
            # Create specialized animal identification prompt
            prompt = self._get_animal_identification_prompt(user)
            
            # Use OpenAI Vision API
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
            
            response = self.object_identifier.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Clean up image file
            try:
                import os
                os.remove(image_path)
            except:
                pass
            
            return {
                "success": True,
                "ai_response": ai_response,
                "user": user,
                "message": ai_response
            }
            
        except Exception as e:
            logger.error(f"Vision API error in animal identification: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I had trouble looking at the picture. Maybe try again?"
            }
    
    def _get_animal_identification_prompt(self, user: str) -> str:
        """Get specialized prompt for animal identification based on user."""
        user_lower = user.lower()
        
        if user_lower == "eladriel":
            return """🦕 DINOSAUR & ANIMAL EXPERT FOR ELADRIEL! 🦕

You're helping Eladriel, who LOVES dinosaurs and animals! Look at this image and provide an exciting identification:

🔍 IDENTIFICATION:
• What animal/dinosaur is this? (Be specific - T-Rex, Triceratops, Lion, etc.)
• Is it a toy, figure, stuffed animal, or real animal?
• What type of creature is it? (Dinosaur, mammal, bird, reptile, etc.)

🦖 DINOSAUR FOCUS (if it's a dinosaur):
• What period did it live in? (Triassic, Jurassic, Cretaceous)
• Was it a carnivore, herbivore, or omnivore?
• How big was it compared to humans?

🌟 AMAZING FACTS:
• Share 2-3 mind-blowing facts that will make Eladriel say "WOW!"
• Include cool abilities, behaviors, or discoveries
• Connect to modern animals if possible

🎯 ADVENTURE CONNECTION:
• How do scientists study this animal?
• What makes this creature special or unique?
• Any recent discoveries or cool research?

Keep it EXCITING and educational - like sharing an amazing discovery with a fellow explorer! Use emojis and make it feel like an adventure!"""
        
        else:  # Default for Sophia or other users
            return """🐾 ANIMAL EXPERT FOR CURIOUS KIDS! 🐾

You're helping a curious child learn about animals! Look at this image and provide a fun identification:

🔍 WHAT IS IT:
• What animal is this? (Be specific with the name)
• Is it a toy, stuffed animal, figure, or real animal?
• What type of animal is it? (Mammal, bird, reptile, fish, etc.)

🌈 DESCRIPTION:
• What colors and patterns do you see?
• What's special about how it looks?
• What size is this animal in real life?

✨ COOL FACTS:
• Share 2-3 amazing facts that will make them say "WOW!"
• What does this animal eat?
• Where does it live in the wild?
• What special abilities does it have?

🎓 LEARNING FUN:
• How does this animal help nature?
• What makes it different from other animals?
• Any fun sounds it makes or behaviors?

Keep it SHORT, exciting, and educational - like telling a friend something super cool you just learned! Use emojis and make it fun for kids!"""
    
    def _format_animal_response(self, result: Dict[str, Any], user: str) -> str:
        """Format the animal identification response with game elements."""
        user_name = user.title()
        ai_response = result.get("ai_response", "")
        
        # Add game elements
        game_header = f"🎯 ANIMAL GUESS #{self.score} - GREAT JOB {user_name.upper()}! 🎯\n\n"
        
        # Add bonus fact occasionally
        bonus_fact = ""
        if random.random() < 0.3:  # 30% chance for bonus fact
            category = random.choice(list(self.bonus_facts.keys()))
            fact = random.choice(self.bonus_facts[category])
            bonus_fact = f"\n\n🎁 BONUS FACT: {fact}"
        
        # Add encouragement for next round
        next_encouragement = f"\n\n🌟 Want to show me another animal? Just say 'guess the animal' again!"
        
        return game_header + ai_response + bonus_fact + next_encouragement
    
    def get_game_stats(self, user: str) -> str:
        """Get current game statistics."""
        if not self.game_active:
            return "No game is currently active. Say 'guess the animal' to start playing!"
        
        user_name = user.title()
        stats = f"""🏆 {user_name.upper()}'S ANIMAL ADVENTURE STATS 🏆

🎯 Animals Identified: {self.score}
🦕 Your Discoveries: {len(self.animals_identified)}

"""
        
        if self.animals_identified:
            stats += "🌟 Animals You've Shown Me:\n"
            for i, animal in enumerate(self.animals_identified[-5:], 1):  # Show last 5
                stats += f"   {i}. {animal}\n"
            
            if len(self.animals_identified) > 5:
                stats += f"   ... and {len(self.animals_identified) - 5} more!\n"
        
        stats += f"\n🎮 Keep going! Show me more amazing creatures!"
        
        return stats
    
    def end_game(self, user: str) -> str:
        """End the current game session."""
        if not self.game_active:
            return "No game is currently active."
        
        user_name = user.title()
        final_score = self.score
        total_animals = len(self.animals_identified)
        
        self.game_active = False
        
        end_message = f"""🎉 AMAZING ANIMAL ADVENTURE COMPLETE! 🎉

Wow {user_name}, what an incredible journey through the animal kingdom!

🏆 FINAL STATS:
• Animals Identified: {final_score}
• Different Creatures: {total_animals}
• Knowledge Gained: TONS!

🌟 YOU'RE AN ANIMAL EXPERT NOW!
You've learned so many cool facts about amazing creatures!

🦕 COME BACK SOON!
There are thousands more animals to discover!
Just say "guess the animal" anytime you want to play again!

Thanks for being such an awesome explorer, {user_name}! 🎊"""

        if self.ai_assistant:
            self.ai_assistant.speak(f"What an amazing animal adventure, {user_name}! You're becoming a real animal expert!", user)
        
        return end_message
    
    def get_game_help(self, user: str) -> str:
        """Get help information for the animal guessing game."""
        user_name = user.title()
        
        return f"""🎮 ANIMAL GUESSING GAME HELP FOR {user_name.upper()} 🎮

🗣️ VOICE COMMANDS:
• "Guess the animal" - Start identifying an animal
• "Animal stats" - See your game statistics  
• "End animal game" - Finish the current game
• "Animal help" - Show this help message

🎯 HOW TO PLAY:
1. Say "guess the animal"
2. Hold your animal toy/figure steady in front of the camera
3. Wait for me to identify it and share cool facts
4. Learn amazing things about your creature!
5. Show me more animals to keep playing!

🦕 WHAT I CAN IDENTIFY:
• Dinosaur toys and action figures
• Stuffed animals and plush toys
• Animal figurines and collectibles
• Pictures of real animals
• Toy animals of all kinds

💡 TIPS FOR BEST RESULTS:
• Hold the animal 12-18 inches from the camera
• Make sure there's good lighting
• Keep the animal steady for a few seconds
• Show the most recognizable side
• One animal at a time works best

🌟 SPECIAL FEATURES:
• Learn scientific names and classifications
• Discover amazing animal abilities
• Get fun facts and trivia
• Build your animal knowledge database
• Explore connections between different species

Ready to discover amazing animals? Say "guess the animal" and let's explore! 🚀"""
    
    def is_game_active(self) -> bool:
        """Check if the game is currently active."""
        return self.game_active
    
    def cleanup(self):
        """Clean up game resources."""
        try:
            if self.object_identifier:
                self.object_identifier.cleanup()
            logger.info("AnimalGuessGame cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during AnimalGuessGame cleanup: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Test the animal guessing game
    game = AnimalGuessGame()
    
    print("🦕 ANIMAL GUESSING GAME TEST 🦕")
    print("=" * 50)
    
    # Test game start
    print("\n1. Starting game for Eladriel:")
    print(game.start_game("eladriel"))
    
    print("\n2. Game help:")
    print(game.get_game_help("eladriel"))
    
    print("\n3. Game stats:")
    print(game.get_game_stats("eladriel"))
    
    print("\n✅ Animal Guessing Game initialized successfully!")
    print("🎮 Ready to identify dinosaurs and animals!") 