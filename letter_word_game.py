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
                {'word': 'APPLE', 'hint': 'A red or green fruit that grows on trees'},
                {'word': 'ANT', 'hint': 'A tiny insect that works hard and carries food'},
                {'word': 'ARM', 'hint': 'The part of your body between your shoulder and hand'},
                {'word': 'AXE', 'hint': 'A tool used to chop wood'}
            ],
            'B': [
                {'word': 'BALL', 'hint': 'A round toy that you can throw and catch'},
                {'word': 'BED', 'hint': 'Where you sleep at night'},
                {'word': 'BUS', 'hint': 'A big yellow vehicle that takes kids to school'},
                {'word': 'BAT', 'hint': 'An animal that flies at night'}
            ],
            'C': [
                {'word': 'CAT', 'hint': 'A furry pet that says meow'},
                {'word': 'CAR', 'hint': 'A vehicle with four wheels'},
                {'word': 'CUP', 'hint': 'Something you drink from'},
                {'word': 'COW', 'hint': 'A farm animal that gives milk'}
            ],
            'D': [
                {'word': 'DOG', 'hint': 'A pet that barks and wags its tail'},
                {'word': 'DUCK', 'hint': 'A bird that swims and says quack'},
                {'word': 'DOOR', 'hint': 'What you open to go into a room'},
                {'word': 'DOLL', 'hint': 'A toy that looks like a person'}
            ],
            'E': [
                {'word': 'EGG', 'hint': 'Something chickens lay that you can eat'},
                {'word': 'EYE', 'hint': 'The part of your body that you see with'},
                {'word': 'EAR', 'hint': 'The part of your body that you hear with'},
                {'word': 'ELF', 'hint': 'A small magical person from stories'}
            ],
            'F': [
                {'word': 'FISH', 'hint': 'An animal that swims in water'},
                {'word': 'FROG', 'hint': 'A green animal that hops and says ribbit'},
                {'word': 'FAN', 'hint': 'Something that blows air to keep you cool'},
                {'word': 'FIRE', 'hint': 'Hot orange flames'}
            ],
            'G': [
                {'word': 'GOAT', 'hint': 'A farm animal with horns'},
                {'word': 'GAME', 'hint': 'Something fun you play'},
                {'word': 'GATE', 'hint': 'A door in a fence'},
                {'word': 'GUM', 'hint': 'Something chewy and sweet'}
            ],
            'H': [
                {'word': 'HAT', 'hint': 'Something you wear on your head'},
                {'word': 'HAND', 'hint': 'The part of your body with five fingers'},
                {'word': 'HORSE', 'hint': 'A big animal that people can ride'},
                {'word': 'HEN', 'hint': 'A female chicken'}
            ],
            'I': [
                {'word': 'ICE', 'hint': 'Frozen water that is cold'},
                {'word': 'INK', 'hint': 'What comes out of a pen when you write'},
                {'word': 'ILL', 'hint': 'When you feel sick'},
                {'word': 'IMP', 'hint': 'A small mischievous creature'}
            ],
            'J': [
                {'word': 'JAR', 'hint': 'A glass container with a lid'},
                {'word': 'JET', 'hint': 'A fast airplane'},
                {'word': 'JOB', 'hint': 'Work that people do'},
                {'word': 'JAM', 'hint': 'Sweet fruit spread for bread'}
            ],
            'K': [
                {'word': 'KEY', 'hint': 'What you use to open locks'},
                {'word': 'KID', 'hint': 'Another word for child'},
                {'word': 'KITE', 'hint': 'A colorful toy that flies in the wind'},
                {'word': 'KING', 'hint': 'A man who rules a kingdom'}
            ],
            'L': [
                {'word': 'LEG', 'hint': 'The part of your body you walk with'},
                {'word': 'LAMP', 'hint': 'Something that gives light'},
                {'word': 'LION', 'hint': 'A big cat that roars'},
                {'word': 'LEAF', 'hint': 'The green part of trees'}
            ],
            'M': [
                {'word': 'MOM', 'hint': 'Another word for mother'},
                {'word': 'MOON', 'hint': 'What you see in the sky at night'},
                {'word': 'MOUSE', 'hint': 'A tiny animal that cats chase'},
                {'word': 'MILK', 'hint': 'A white drink that comes from cows'}
            ],
            'N': [
                {'word': 'NET', 'hint': 'Something with holes used to catch fish'},
                {'word': 'NOSE', 'hint': 'The part of your face you smell with'},
                {'word': 'NUT', 'hint': 'A hard shell with food inside'},
                {'word': 'NAP', 'hint': 'A short sleep during the day'}
            ],
            'O': [
                {'word': 'OWL', 'hint': 'A bird that hoots at night'},
                {'word': 'OX', 'hint': 'A strong farm animal'},
                {'word': 'OIL', 'hint': 'A slippery liquid'},
                {'word': 'ORB', 'hint': 'A round ball shape'}
            ],
            'P': [
                {'word': 'PIG', 'hint': 'A pink farm animal that oinks'},
                {'word': 'PEN', 'hint': 'What you write with'},
                {'word': 'POT', 'hint': 'What you cook food in'},
                {'word': 'PUP', 'hint': 'A baby dog'}
            ],
            'Q': [
                {'word': 'QUEEN', 'hint': 'A woman who rules a kingdom'},
                {'word': 'QUIT', 'hint': 'To stop doing something'},
                {'word': 'QUIZ', 'hint': 'A short test with questions'},
                {'word': 'QUAY', 'hint': 'A place where boats dock'}
            ],
            'R': [
                {'word': 'RAT', 'hint': 'A small animal with a long tail'},
                {'word': 'RUN', 'hint': 'To move fast with your legs'},
                {'word': 'RED', 'hint': 'The color of fire trucks'},
                {'word': 'RUG', 'hint': 'Something soft on the floor'}
            ],
            'S': [
                {'word': 'SUN', 'hint': 'The bright light in the sky during day'},
                {'word': 'STAR', 'hint': 'What twinkles in the night sky'},
                {'word': 'SOCK', 'hint': 'What you wear on your feet inside shoes'},
                {'word': 'SNAKE', 'hint': 'A long animal with no legs'}
            ],
            'T': [
                {'word': 'TOP', 'hint': 'A spinning toy'},
                {'word': 'TOY', 'hint': 'Something fun to play with'},
                {'word': 'TREE', 'hint': 'A tall plant with leaves and branches'},
                {'word': 'TEN', 'hint': 'The number after nine'}
            ],
            'U': [
                {'word': 'UP', 'hint': 'The opposite of down'},
                {'word': 'USE', 'hint': 'To do something with an object'},
                {'word': 'URN', 'hint': 'A special jar or container'},
                {'word': 'UMP', 'hint': 'Short for umpire in baseball'}
            ],
            'V': [
                {'word': 'VAN', 'hint': 'A big car that carries many people'},
                {'word': 'VET', 'hint': 'A doctor who helps animals'},
                {'word': 'VINE', 'hint': 'A plant that climbs up walls'},
                {'word': 'VOW', 'hint': 'A special promise'}
            ],
            'W': [
                {'word': 'WEB', 'hint': 'What a spider makes'},
                {'word': 'WIG', 'hint': 'Fake hair you can wear'},
                {'word': 'WIN', 'hint': 'To come first in a game'},
                {'word': 'WAX', 'hint': 'What candles are made of'}
            ],
            'X': [
                {'word': 'X-RAY', 'hint': 'A picture that shows your bones'},
                {'word': 'XYZ', 'hint': 'The last three letters of the alphabet'},
                {'word': 'XBOX', 'hint': 'A video game machine'},
                {'word': 'XMAS', 'hint': 'A short way to write Christmas'}
            ],
            'Y': [
                {'word': 'YAK', 'hint': 'A furry animal like a big cow'},
                {'word': 'YES', 'hint': 'The opposite of no'},
                {'word': 'YAM', 'hint': 'An orange vegetable like a sweet potato'},
                {'word': 'YAP', 'hint': 'The sound a small dog makes'}
            ],
            'Z': [
                {'word': 'ZOO', 'hint': 'A place where you can see animals'},
                {'word': 'ZAP', 'hint': 'A quick electric sound'},
                {'word': 'ZIP', 'hint': 'To close something quickly'},
                {'word': 'ZEN', 'hint': 'Being very calm and peaceful'}
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

        if self.ai_assistant:
            self.ai_assistant.speak(f"Letter word game started! Your first letter is {self.current_letter}. {self.current_hint} What word do you think it is?", user)
            
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