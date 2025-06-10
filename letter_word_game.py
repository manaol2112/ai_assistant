#!/usr/bin/env python3
"""
Letter Word Game for Kids
A fun educational game where kids guess words that start with specific letters based on hints.
"""

import random
import logging
from typing import Dict, Any, List, Optional
import time

logger = logging.getLogger(__name__)

class LetterWordGame:
    """Interactive letter-based word guessing game for kids."""
    
    def __init__(self, ai_assistant=None):
        """Initialize the Letter Word Game."""
        self.ai_assistant = ai_assistant
        self.game_active = False
        self.current_letter = None
        self.current_word = None
        self.current_hint = None
        self.score = 0
        self.words_completed = []
        self.current_user = None
        self.attempts = 0
        self.max_attempts = 3
        
        # Elementary-level word database organized by letters with simple hints
        self.word_database = {
            'A': [
                {'word': 'APPLE', 'hint': 'A red or green fruit that grows on trees. Teachers like these!'},
                {'word': 'ANT', 'hint': 'A tiny black insect that works hard and lives in hills'},
                {'word': 'ARM', 'hint': 'The part of your body between your shoulder and hand. You have two of these!'},
                {'word': 'AXE', 'hint': 'A tool with a sharp blade that cuts wood. Firefighters use these!'}
            ],
            'B': [
                {'word': 'BALL', 'hint': 'A round toy that bounces. You play catch with this!'},
                {'word': 'BED', 'hint': 'A soft place where you sleep at night with pillows and blankets'},
                {'word': 'BUS', 'hint': 'A big yellow vehicle that takes kids to school every day'},
                {'word': 'BAT', 'hint': 'A small animal that flies at night and sleeps upside down'}
            ],
            'C': [
                {'word': 'CAT', 'hint': 'A furry pet that says meow and likes to chase mice'},
                {'word': 'CAR', 'hint': 'A vehicle with four wheels that drives on roads'},
                {'word': 'CUP', 'hint': 'Something you drink milk or juice from. It has a handle!'},
                {'word': 'COW', 'hint': 'A big farm animal that gives milk and says moo'}
            ],
            'D': [
                {'word': 'DOG', 'hint': 'A friendly pet that barks, wags its tail, and loves to play fetch'},
                {'word': 'DUCK', 'hint': 'A yellow bird that swims in ponds and says quack quack'},
                {'word': 'DOOR', 'hint': 'What you open to go into a room. You knock on this!'},
                {'word': 'DOLL', 'hint': 'A toy that looks like a baby or person. Kids love to play with these!'}
            ],
            'E': [
                {'word': 'EGG', 'hint': 'Something round and white that chickens lay. You can eat these for breakfast!'},
                {'word': 'EYE', 'hint': 'The part of your face that you see with. You have two of these!'},
                {'word': 'EAR', 'hint': 'The part of your head that you hear sounds with'},
                {'word': 'ELF', 'hint': 'A small magical person who helps Santa make toys'}
            ],
            'F': [
                {'word': 'FISH', 'hint': 'An animal that swims in water and has fins. Some people keep these as pets!'},
                {'word': 'FROG', 'hint': 'A green animal that hops and lives near water. It says ribbit!'},
                {'word': 'FAN', 'hint': 'Something that spins around to blow air and keep you cool on hot days'},
                {'word': 'FIRE', 'hint': 'Hot orange and red flames that give light and warmth'}
            ],
            'G': [
                {'word': 'GOAT', 'hint': 'A farm animal with horns that likes to eat grass and climb rocks'},
                {'word': 'GAME', 'hint': 'Something fun you play with friends. Like hide and seek!'},
                {'word': 'GATE', 'hint': 'A door in a fence that opens and closes'},
                {'word': 'GUM', 'hint': 'Something sweet and chewy that you chew but never swallow'}
            ],
            'H': [
                {'word': 'HAT', 'hint': 'Something you wear on your head to stay warm or block the sun'},
                {'word': 'HAND', 'hint': 'The part of your body with five fingers that you use to pick things up'},
                {'word': 'HORSE', 'hint': 'A big animal that people can ride. Cowboys ride these!'},
                {'word': 'HEN', 'hint': 'A female chicken that lays eggs on the farm'}
            ],
            'I': [
                {'word': 'ICE', 'hint': 'Frozen water that is very cold and slippery'},
                {'word': 'INK', 'hint': 'The colored liquid that comes out of pens when you write'},
                {'word': 'ILL', 'hint': 'When you feel sick and need to rest'},
                {'word': 'IMP', 'hint': 'A small playful creature from fairy tales'}
            ],
            'J': [
                {'word': 'JAR', 'hint': 'A glass container with a lid where you store cookies or jam'},
                {'word': 'JET', 'hint': 'A very fast airplane that flies high in the sky'},
                {'word': 'JOB', 'hint': 'Work that grown-ups do to earn money'},
                {'word': 'JAM', 'hint': 'Sweet fruit spread that you put on bread or toast'}
            ],
            'K': [
                {'word': 'KEY', 'hint': 'A small metal thing you use to unlock doors and start cars'},
                {'word': 'KID', 'hint': 'Another word for child. That\'s you!'},
                {'word': 'KITE', 'hint': 'A colorful toy that flies high in the sky on windy days'},
                {'word': 'KING', 'hint': 'A man who rules a kingdom and wears a crown'}
            ],
            'L': [
                {'word': 'LEG', 'hint': 'The part of your body you use to walk and run. You have two of these!'},
                {'word': 'LAMP', 'hint': 'Something that gives light when you turn it on in dark rooms'},
                {'word': 'LION', 'hint': 'A big wild cat with a mane that roars loudly'},
                {'word': 'LEAF', 'hint': 'The green parts that grow on trees and change colors in fall'}
            ],
            'M': [
                {'word': 'MOM', 'hint': 'Another word for mother. She takes care of you and loves you!'},
                {'word': 'MOON', 'hint': 'The bright round thing you see in the sky at night'},
                {'word': 'MOUSE', 'hint': 'A tiny gray animal with a long tail that cats like to chase'},
                {'word': 'MILK', 'hint': 'A white drink that comes from cows and makes your bones strong'}
            ],
            'N': [
                {'word': 'NET', 'hint': 'Something with holes used to catch fish or play sports'},
                {'word': 'NOSE', 'hint': 'The part of your face you smell flowers and food with'},
                {'word': 'NUT', 'hint': 'A hard shell with yummy food inside. Squirrels love these!'},
                {'word': 'NAP', 'hint': 'A short sleep you take during the day when you\'re tired'}
            ],
            'O': [
                {'word': 'OWL', 'hint': 'A wise bird with big eyes that flies at night and says hoo'},
                {'word': 'OX', 'hint': 'A very strong farm animal that helps pull heavy things'},
                {'word': 'OIL', 'hint': 'A slippery liquid used in cooking and cars'},
                {'word': 'ORB', 'hint': 'A perfectly round ball shape, like a marble'}
            ],
            'P': [
                {'word': 'PIG', 'hint': 'A pink farm animal that says oink and likes to roll in mud'},
                {'word': 'PEN', 'hint': 'What you use to write letters and draw pictures with ink'},
                {'word': 'POT', 'hint': 'What mommy cooks soup and pasta in on the stove'},
                {'word': 'PUP', 'hint': 'A baby dog that is very cute and playful'}
            ],
            'Q': [
                {'word': 'QUEEN', 'hint': 'A woman who rules a kingdom and wears a beautiful crown'},
                {'word': 'QUIT', 'hint': 'To stop doing something, like when you quit playing a game'},
                {'word': 'QUIZ', 'hint': 'A short test with questions to see what you know'},
                {'word': 'QUAY', 'hint': 'A special place where big boats park near the water'}
            ],
            'R': [
                {'word': 'RAT', 'hint': 'A small gray animal with a long tail, bigger than a mouse'},
                {'word': 'RUN', 'hint': 'To move very fast with your legs, faster than walking'},
                {'word': 'RED', 'hint': 'The color of fire trucks, strawberries, and stop signs'},
                {'word': 'RUG', 'hint': 'A soft carpet that goes on the floor to keep your feet warm'}
            ],
            'S': [
                {'word': 'SUN', 'hint': 'The bright yellow ball of light in the sky that keeps us warm'},
                {'word': 'STAR', 'hint': 'The tiny lights that twinkle in the night sky'},
                {'word': 'SOCK', 'hint': 'What you put on your feet before putting on your shoes'},
                {'word': 'SNAKE', 'hint': 'A long animal with no legs that slithers on the ground'}
            ],
            'T': [
                {'word': 'TOP', 'hint': 'A spinning toy that goes round and round when you twist it'},
                {'word': 'TOY', 'hint': 'Something fun that kids play with, like dolls or cars'},
                {'word': 'TREE', 'hint': 'A tall plant with leaves, branches, and a trunk where birds live'},
                {'word': 'TEN', 'hint': 'The number that comes after nine. Count your fingers!'}
            ],
            'U': [
                {'word': 'UP', 'hint': 'The opposite of down. Birds fly this way in the sky!'},
                {'word': 'USE', 'hint': 'What you do with tools or toys - you play with them!'},
                {'word': 'URN', 'hint': 'A special decorative jar or container'},
                {'word': 'UMP', 'hint': 'Short word for the person who makes calls in baseball games'}
            ],
            'V': [
                {'word': 'VAN', 'hint': 'A big car that can carry lots of people and their things'},
                {'word': 'VET', 'hint': 'A special doctor who takes care of sick animals'},
                {'word': 'VINE', 'hint': 'A long green plant that climbs up walls and fences'},
                {'word': 'VOW', 'hint': 'A very important promise that people make'}
            ],
            'W': [
                {'word': 'WEB', 'hint': 'The sticky net that spiders make to catch bugs for food'},
                {'word': 'WIG', 'hint': 'Fake hair that people can wear on their heads'},
                {'word': 'WIN', 'hint': 'What happens when you come first place in a game or race'},
                {'word': 'WAX', 'hint': 'The soft material that candles are made from'}
            ],
            'X': [
                {'word': 'X-RAY', 'hint': 'A special picture that doctors take to see your bones inside'},
                {'word': 'XYZ', 'hint': 'The very last three letters of the alphabet'},
                {'word': 'XBOX', 'hint': 'A popular video game machine that kids love to play'},
                {'word': 'XMAS', 'hint': 'A short fun way to write the word Christmas'}
            ],
            'Y': [
                {'word': 'YAK', 'hint': 'A big furry animal that looks like a cow with long hair'},
                {'word': 'YES', 'hint': 'The happy word you say when you agree - opposite of no'},
                {'word': 'YAM', 'hint': 'An orange vegetable that tastes sweet, like a sweet potato'},
                {'word': 'YAP', 'hint': 'The high-pitched sound that small dogs make when they bark'}
            ],
            'Z': [
                {'word': 'ZOO', 'hint': 'A fun place where you can see lions, elephants, and monkeys'},
                {'word': 'ZAP', 'hint': 'A quick electric sound, like lightning or a bug zapper'},
                {'word': 'ZIP', 'hint': 'To close something quickly, like the zipper on your jacket'},
                {'word': 'ZEN', 'hint': 'A special way of being very calm and peaceful inside'}
            ]
        }
        
        # Celebration messages for correct answers
        self.celebration_messages = [
            "🎉 Fantastic! You got it right!",
            "⭐ Amazing job! That's correct!",
            "🌟 Wonderful! You're so smart!",
            "🎊 Excellent! Perfect answer!",
            "💫 Brilliant! You nailed it!",
            "🏆 Outstanding! Great thinking!",
            "✨ Superb! You're a word wizard!",
            "🎈 Marvelous! Absolutely right!"
        ]
        
        # Encouragement messages for wrong answers
        self.encouragement_messages = [
            "Good try! Let me give you the answer:",
            "Nice effort! The word I was thinking of is:",
            "You're learning! The correct answer is:",
            "Keep trying! The word is:",
            "Almost there! The right word is:",
            "Good guess! Actually, it's:",
            "You're doing great! The answer is:",
            "Don't worry! The word I wanted is:"
        ]
        
        logger.info("LetterWordGame initialized successfully!")
    
    def start_game(self, user: str) -> str:
        """Start the letter word game."""
        self.current_user = user.lower()
        self.game_active = True
        self.score = 0
        self.words_completed = []
        
        user_name = user.title()
        
        # Select a random letter to start with
        self.current_letter = random.choice(list(self.word_database.keys()))
        word_data = random.choice(self.word_database[self.current_letter])
        self.current_word = word_data['word']
        self.current_hint = word_data['hint']
        self.attempts = 0
        
        welcome_message = f"""🔤 LETTER WORD GAME! 🔤

Hey {user_name}! Let's play a fun word guessing game! 

🎯 I'll give you a letter and a hint, and you guess the word!

Ready for your first challenge?

📝 Letter: {self.current_letter}
💡 Hint: {self.current_hint}

What word starts with '{self.current_letter}' and matches this hint?"""

        # Let the main handler manage speech - don't duplicate here
        return welcome_message
    
    def check_answer(self, user_answer: str, user: str) -> str:
        """Check the user's answer against the current word."""
        if not self.game_active:
            return "The game isn't active. Say 'Letter Game' to start playing!"
        
        # Extract the actual word from common phrases
        extracted_word = self._extract_word_from_answer(user_answer)
        
        # Check if the answer is correct
        if extracted_word == self.current_word:
            self.score += 1
            self.words_completed.append(self.current_word)
            
            # Celebrate the correct answer
            celebration = random.choice(self.celebration_messages)
            
            # Prepare next word
            next_word_message = self._prepare_next_word()
            
            response = f"""{celebration}

Yes! You got it right! 

📊 Score: {self.score} correct words!

{next_word_message}"""

            if self.ai_assistant:
                self.ai_assistant.speak(f"{celebration} Yes, that's right! Your score is {self.score}. {self._get_next_word_speech()}", user)
            
            return response
        
        else:
            self.attempts += 1
            
            if self.attempts >= self.max_attempts:
                # Store the correct answer before preparing next word
                correct_answer = self.current_word
                
                # Reveal the answer and move to next word
                encouragement = random.choice(self.encouragement_messages)
                next_word_message = self._prepare_next_word()
                
                response = f"""{encouragement} '{correct_answer}'

{next_word_message}"""

                if self.ai_assistant:
                    self.ai_assistant.speak(f"{encouragement} {correct_answer}. {self._get_next_word_speech()}", user)
                
                return response
            
            else:
                remaining_attempts = self.max_attempts - self.attempts
                hint_response = f"""🤔 That's not quite right! You guessed '{extracted_word}'

The word I'm thinking of starts with '{self.current_letter}' and: {self.current_hint}

You have {remaining_attempts} more attempt{'s' if remaining_attempts > 1 else ''}. Try again!"""

                if self.ai_assistant:
                    self.ai_assistant.speak(f"Not quite right! Try again. You have {remaining_attempts} more tries.", user)
                
                return hint_response
    
    def _extract_word_from_answer(self, user_answer: str) -> str:
        """Extract the actual word from phrases like 'the answer is fan' or 'it's a fan'."""
        clean_answer = user_answer.strip().upper()
        
        # Common phrases that indicate an answer
        answer_phrases = [
            "THE ANSWER IS ",
            "ANSWER IS ",
            "I THINK IT'S ",
            "I THINK IT IS ",
            "MY GUESS IS ",
            "GUESS IS ",
            "I SAY ",
            "IT'S A ",
            "IT IS A ",
            "IT'S AN ",
            "IT IS AN ",
            "IT'S ",
            "IT IS "
        ]
        
        # Check if the answer contains any of these phrases
        for phrase in answer_phrases:
            if phrase in clean_answer:
                # Extract the word after the phrase
                word_part = clean_answer.split(phrase, 1)[1].strip()
                # Take only the first word (in case there are multiple words)
                if word_part:
                    first_word = word_part.split()[0]
                    # Skip common articles and take the next word if needed
                    if first_word in ['A', 'AN', 'THE'] and len(word_part.split()) > 1:
                        return word_part.split()[1]
                    return first_word
        
        # If no phrase found, return the cleaned answer as is
        return clean_answer
    
    def _get_next_word_speech(self) -> str:
        """Get speech-friendly version of next word challenge without revealing previous answer."""
        return f"Here's your next challenge! Letter {self.current_letter}. {self.current_hint}. What word do you think it is?"
    
    def _prepare_next_word(self) -> str:
        """Prepare the next word challenge."""
        # Select a new letter (try to avoid repeating recent letters)
        available_letters = list(self.word_database.keys())
        if len(self.words_completed) >= 3:
            # Try to avoid letters from last 3 words
            recent_letters = [word[0] for word in self.words_completed[-3:]]
            available_letters = [letter for letter in available_letters if letter not in recent_letters]
            if not available_letters:  # If all letters were recent, use all letters
                available_letters = list(self.word_database.keys())
        
        self.current_letter = random.choice(available_letters)
        word_data = random.choice(self.word_database[self.current_letter])
        self.current_word = word_data['word']
        self.current_hint = word_data['hint']
        self.attempts = 0
        
        return f"""🎯 Next Challenge!

📝 Letter: {self.current_letter}
💡 Hint: {self.current_hint}

What word starts with '{self.current_letter}' and matches this hint?"""
    
    def get_hint(self, user: str) -> str:
        """Provide an additional hint for the current word."""
        if not self.game_active:
            return "The game isn't active. Say 'Letter Game' to start playing!"
        
        # Provide additional context or a different angle for the hint
        extra_hints = {
            'APPLE': "It's a fruit that can be red, green, or yellow!",
            'ANT': "This tiny bug is super strong and works with its friends!",
            'ARM': "You use these to hug people and pick things up!",
            'AXE': "Lumberjacks use this to cut down trees!",
            'BALL': "You can bounce it, throw it, or kick it!",
            'BED': "You lie down here with pillows and blankets!",
            'BUS': "It's bigger than a car and has lots of seats!",
            'BAT': "This animal hangs upside down and sleeps during the day!",
            'CAT': "This pet purrs when it's happy!",
            'CAR': "You ride in this to go places on roads!",
            'CUP': "You hold this when you drink water or juice!",
            'COW': "This animal says 'moo' and lives on farms!",
            'DOG': "This pet is called man's best friend!",
            'DUCK': "This bird likes to swim in ponds!",
            'DOOR': "You knock on this before entering a house!",
            'DOLL': "Children like to play dress-up with this toy!",
            'EGG': "Baby chickens grow inside these!",
            'EYE': "You have two of these on your face to see!",
            'EAR': "You have two of these to hear sounds!",
            'ELF': "Santa's helpers are these magical creatures!",
            'FISH': "This animal has fins and lives underwater!",
            'FROG': "This green animal can jump really far!",
            'FAN': "This spins around to make you feel cooler!",
            'FIRE': "This is hot and bright orange or red!",
            'GOAT': "This farm animal likes to eat grass and climb!",
            'GAME': "Monopoly and chess are types of this!",
            'GATE': "This opens and closes like a door in a fence!",
            'GUM': "You chew this but don't swallow it!",
            'HAT': "People wear this on sunny days or when it's cold!",
            'HAND': "You have fingers and a thumb on this!",
            'HORSE': "Cowboys ride this animal in movies!",
            'HEN': "This female bird lays eggs!",
            'ICE': "Water becomes this when it gets very cold!",
            'INK': "This liquid comes out when you write with a pen!",
            'JAR': "You can store cookies or jam in this!",
            'JET': "This airplane flies very fast and high!",
            'KEY': "You need this small metal thing to unlock doors!",
            'KITE': "Children love to fly this on windy days!",
            'LEG': "You have two of these and they help you walk!",
            'LAMP': "You turn this on when it gets dark!",
            'LION': "This big cat is the king of the jungle!",
            'MOM': "She takes care of you and loves you very much!",
            'MOON': "This bright circle shines in the sky at night!",
            'MOUSE': "This small animal likes to eat cheese!",
            'MILK': "This white drink helps make your bones strong!",
            'NET': "Tennis players hit the ball over this!",
            'NOSE': "You use this to smell flowers and food!",
            'OWL': "This wise bird says 'hoo' and has big eyes!",
            'PIG': "This pink animal rolls in mud and says 'oink'!",
            'PEN': "You use this to write letters and draw pictures!",
            'RAT': "This animal looks like a mouse but bigger!",
            'RUN': "This is faster than walking!",
            'RED': "Roses and strawberries are this color!",
            'SUN': "This bright yellow circle gives us light and warmth!",
            'STAR': "You make a wish when you see a shooting one!",
            'SNAKE': "This animal slithers on the ground!",
            'TOP': "You spin this toy with your fingers!",
            'TOY': "Children love to play with these!",
            'TREE': "Birds build nests in these tall plants!",
            'WEB': "Spiders make these to catch bugs!",
            'WIN': "This is what happens when you come first!",
            'ZOO': "You can see lions, elephants, and monkeys here!"
        }
        
        extra_hint = extra_hints.get(self.current_word, f"It definitely starts with the letter '{self.current_letter}'!")
        
        response = f"""💡 Extra Hint: {extra_hint}

🔄 Original hint: {self.current_hint}

Letter: {self.current_letter}

Keep thinking! You can do it!"""

        if self.ai_assistant:
            self.ai_assistant.speak(f"Here's an extra hint: {extra_hint}", user)
        
        return response
    
    def skip_word(self, user: str) -> str:
        """Skip the current word and move to the next one."""
        if not self.game_active:
            return "The game isn't active. Say 'Letter Game' to start playing!"
        
        skipped_word = self.current_word
        next_word_message = self._prepare_next_word()
        
        response = f"""⏭️ Skipped! The word was '{skipped_word}'

{next_word_message}"""

        if self.ai_assistant:
            self.ai_assistant.speak(f"Okay, we'll skip that one. The word was {skipped_word}. {self._get_next_word_speech()}", user)
        
        return response
    
    def get_game_stats(self, user: str) -> str:
        """Get current game statistics."""
        if not self.game_active:
            return "No game is currently active. Say 'Letter Game' to start playing!"
        
        total_attempts = len(self.words_completed) + (1 if self.current_word else 0)
        accuracy = (self.score / total_attempts * 100) if total_attempts > 0 else 0
        
        stats = f"""📊 GAME STATISTICS

🏆 Correct Words: {self.score}
📝 Words Attempted: {total_attempts}
🎯 Accuracy: {accuracy:.1f}%

✅ Words You Got Right:
{', '.join(self.words_completed) if self.words_completed else 'None yet - but you can do it!'}

🔤 Current Challenge: Letter {self.current_letter}
💪 Keep going! You're doing great!"""

        return stats
    
    def end_game(self, user: str) -> str:
        """End the current game and show final stats."""
        if not self.game_active:
            return "No game is currently active."
        
        self.game_active = False
        user_name = user.title()
        
        final_stats = f"""🎮 GAME OVER! Great job {user_name}!

📊 FINAL SCORE:
🏆 Correct Words: {self.score}
✅ Words Completed: {', '.join(self.words_completed) if self.words_completed else 'Keep practicing!'}

🌟 You learned about {len(self.words_completed)} new words today!

Want to play again? Just say 'Letter Game' to start a new round!

🧠 Remember: Every time you play, you're getting smarter! Great job!"""

        if self.ai_assistant:
            self.ai_assistant.speak(f"Game over! You got {self.score} words correct. Great job learning new words!", user)
        
        return final_stats
    
    def get_game_help(self, user: str) -> str:
        """Get help instructions for the game."""
        user_name = user.title()
        
        return f"""🔤 LETTER WORD GAME HELP - {user_name}

🎯 HOW TO PLAY:
• I'll give you a letter (like 'B') and a hint
• You guess what word starts with that letter
• You get 3 tries for each word
• If you get it right, you earn points!
• If you don't get it in 3 tries, I'll tell you the answer

🗣️ WHAT TO SAY:
• "Letter Game" - Start a new game
• Just say your guess - like "Butterfly" or "Ball"
• "Hint please" or "Give me a hint" - Get extra help
• "Skip" - Move to the next word
• "Stats" - See your current score
• "End game" - Finish and see final results

🏆 SCORING:
• +1 point for each correct word
• No penalty for wrong guesses
• The goal is to learn and have fun!

💡 TIPS FOR SUCCESS:
• Listen carefully to the hints
• Think about the letter sound at the beginning
• Don't be afraid to guess - that's how you learn!
• Ask for extra hints if you need them

🌟 Remember: This game helps you learn new words, practice letter sounds, and have fun! Every guess makes you smarter!

Ready to start? Just say "Letter Game"!"""
    
    def is_game_active(self) -> bool:
        """Check if a game is currently active."""
        return self.game_active
    
    def cleanup(self):
        """Clean up game resources."""
        try:
            self.game_active = False
            self.current_word = None
            self.current_hint = None
            self.current_letter = None
            logger.info("LetterWordGame cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during LetterWordGame cleanup: {e}")

# Example usage
if __name__ == "__main__":
    game = LetterWordGame()
    print(game.start_game("TestUser"))
    print(game.check_answer("RABBIT", "TestUser")) 