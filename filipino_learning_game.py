#!/usr/bin/env python3
"""
Filipino Learning Game for Kids
An interactive game where kids learn Tagalog by translating English words/phrases and practicing pronunciation.
"""

import random
import logging
from typing import Dict, Any, List, Optional
import time
import re

logger = logging.getLogger(__name__)

class FilipinoLearningGame:
    """Interactive Filipino/Tagalog learning game for kids."""
    
    def __init__(self, ai_assistant=None):
        """Initialize the Filipino Learning Game."""
        self.ai_assistant = ai_assistant
        self.game_active = False
        self.current_english = None
        self.current_tagalog = None
        self.current_pronunciation = None
        self.score = 0
        self.words_learned = []
        self.current_user = None
        self.waiting_for_english = True
        self.waiting_for_repetition = False
        self.current_attempts = 0
        self.max_attempts = 3
        
        # English to Tagalog database with pronunciation guides
        self.translation_database = {
            # Basic Greetings
            'hello': {'tagalog': 'Kumusta', 'pronunciation': 'koo-MUS-tah', 'category': 'greetings'},
            'good morning': {'tagalog': 'Magandang umaga', 'pronunciation': 'ma-ga-DANG oo-MA-ga', 'category': 'greetings'},
            'good afternoon': {'tagalog': 'Magandang hapon', 'pronunciation': 'ma-ga-DANG ha-PON', 'category': 'greetings'},
            'good evening': {'tagalog': 'Magandang gabi', 'pronunciation': 'ma-ga-DANG ga-BEE', 'category': 'greetings'},
            'goodbye': {'tagalog': 'Paalam', 'pronunciation': 'pa-AH-lam', 'category': 'greetings'},
            'thank you': {'tagalog': 'Salamat', 'pronunciation': 'sa-LA-mat', 'category': 'greetings'},
            'please': {'tagalog': 'Pakisuyo', 'pronunciation': 'pa-ki-SUH-yo', 'category': 'greetings'},
            'excuse me': {'tagalog': 'Excuse me', 'pronunciation': 'ex-KYUS mee', 'category': 'greetings'},
            
            # Family Members
            'mother': {'tagalog': 'Ina', 'pronunciation': 'EE-na', 'category': 'family'},
            'father': {'tagalog': 'Ama', 'pronunciation': 'AH-ma', 'category': 'family'},
            'mom': {'tagalog': 'Nanay', 'pronunciation': 'na-NIGH', 'category': 'family'},
            'dad': {'tagalog': 'Tatay', 'pronunciation': 'ta-TIGH', 'category': 'family'},
            'brother': {'tagalog': 'Kapatid na lalaki', 'pronunciation': 'ka-pa-TEED na la-LA-kee', 'category': 'family'},
            'sister': {'tagalog': 'Kapatid na babae', 'pronunciation': 'ka-pa-TEED na ba-BA-eh', 'category': 'family'},
            'grandmother': {'tagalog': 'Lola', 'pronunciation': 'LO-la', 'category': 'family'},
            'grandfather': {'tagalog': 'Lolo', 'pronunciation': 'LO-lo', 'category': 'family'},
            
            # Colors
            'red': {'tagalog': 'Pula', 'pronunciation': 'POO-la', 'category': 'colors'},
            'blue': {'tagalog': 'Asul', 'pronunciation': 'ah-SOOL', 'category': 'colors'},
            'green': {'tagalog': 'Berde', 'pronunciation': 'BER-deh', 'category': 'colors'},
            'yellow': {'tagalog': 'Dilaw', 'pronunciation': 'DEE-law', 'category': 'colors'},
            'black': {'tagalog': 'Itim', 'pronunciation': 'EE-tim', 'category': 'colors'},
            'white': {'tagalog': 'Puti', 'pronunciation': 'POO-tee', 'category': 'colors'},
            'pink': {'tagalog': 'Rosas', 'pronunciation': 'ro-SAS', 'category': 'colors'},
            'orange': {'tagalog': 'Kahel', 'pronunciation': 'ka-HEL', 'category': 'colors'},
            
            # Numbers 1-10
            'one': {'tagalog': 'Isa', 'pronunciation': 'EE-sa', 'category': 'numbers'},
            'two': {'tagalog': 'Dalawa', 'pronunciation': 'da-LA-wa', 'category': 'numbers'},
            'three': {'tagalog': 'Tatlo', 'pronunciation': 'TAT-lo', 'category': 'numbers'},
            'four': {'tagalog': 'Apat', 'pronunciation': 'AH-pat', 'category': 'numbers'},
            'five': {'tagalog': 'Lima', 'pronunciation': 'LEE-ma', 'category': 'numbers'},
            'six': {'tagalog': 'Anim', 'pronunciation': 'AH-nim', 'category': 'numbers'},
            'seven': {'tagalog': 'Pito', 'pronunciation': 'PEE-to', 'category': 'numbers'},
            'eight': {'tagalog': 'Walo', 'pronunciation': 'wa-LO', 'category': 'numbers'},
            'nine': {'tagalog': 'Siyam', 'pronunciation': 'SEE-yam', 'category': 'numbers'},
            'ten': {'tagalog': 'Sampu', 'pronunciation': 'sam-POO', 'category': 'numbers'},
            
            # Body Parts
            'head': {'tagalog': 'Ulo', 'pronunciation': 'OO-lo', 'category': 'body'},
            'eyes': {'tagalog': 'Mata', 'pronunciation': 'ma-TA', 'category': 'body'},
            'nose': {'tagalog': 'Ilong', 'pronunciation': 'EE-long', 'category': 'body'},
            'mouth': {'tagalog': 'Bibig', 'pronunciation': 'BEE-big', 'category': 'body'},
            'ears': {'tagalog': 'Tenga', 'pronunciation': 'te-NGA', 'category': 'body'},
            'hands': {'tagalog': 'Kamay', 'pronunciation': 'ka-MIGH', 'category': 'body'},
            'feet': {'tagalog': 'Paa', 'pronunciation': 'pa-AH', 'category': 'body'},
            
            # Food
            'rice': {'tagalog': 'Kanin', 'pronunciation': 'ka-NIN', 'category': 'food'},
            'water': {'tagalog': 'Tubig', 'pronunciation': 'TOO-big', 'category': 'food'},
            'fish': {'tagalog': 'Isda', 'pronunciation': 'is-DA', 'category': 'food'},
            'chicken': {'tagalog': 'Manok', 'pronunciation': 'ma-NOK', 'category': 'food'},
            'bread': {'tagalog': 'Tinapay', 'pronunciation': 'ti-na-PIGH', 'category': 'food'},
            'milk': {'tagalog': 'Gatas', 'pronunciation': 'ga-TAS', 'category': 'food'},
            'fruit': {'tagalog': 'Prutas', 'pronunciation': 'PROO-tas', 'category': 'food'},
            
            # Animals
            'dog': {'tagalog': 'Aso', 'pronunciation': 'AH-so', 'category': 'animals'},
            'cat': {'tagalog': 'Pusa', 'pronunciation': 'POO-sa', 'category': 'animals'},
            'bird': {'tagalog': 'Ibon', 'pronunciation': 'EE-bon', 'category': 'animals'},
            'cow': {'tagalog': 'Baka', 'pronunciation': 'ba-KA', 'category': 'animals'},
            'pig': {'tagalog': 'Baboy', 'pronunciation': 'ba-BOY', 'category': 'animals'},
            'horse': {'tagalog': 'Kabayo', 'pronunciation': 'ka-ba-YO', 'category': 'animals'},
            
            # Common Phrases
            'how are you': {'tagalog': 'Kumusta ka', 'pronunciation': 'koo-MUS-ta ka', 'category': 'phrases'},
            'what is your name': {'tagalog': 'Ano ang pangalan mo', 'pronunciation': 'AH-no ang pa-nga-LAN mo', 'category': 'phrases'},
            'i love you': {'tagalog': 'Mahal kita', 'pronunciation': 'ma-HAL ki-TA', 'category': 'phrases'},
            'i am hungry': {'tagalog': 'Gutom ako', 'pronunciation': 'GOO-tom ah-KO', 'category': 'phrases'},
            'i am thirsty': {'tagalog': 'Uhaw ako', 'pronunciation': 'OO-haw ah-KO', 'category': 'phrases'},
            'where is': {'tagalog': 'Nasaan ang', 'pronunciation': 'na-sa-AN ang', 'category': 'phrases'},
            'yes': {'tagalog': 'Oo', 'pronunciation': 'OH-oh', 'category': 'phrases'},
            'no': {'tagalog': 'Hindi', 'pronunciation': 'hin-DEE', 'category': 'phrases'},
        }
        
        # Celebration messages for correct pronunciation
        self.celebration_messages = [
            "🎉 Excellent pronunciation! You sound like a native speaker!",
            "⭐ Amazing! You said that perfectly!",
            "🌟 Wonderful! Your Tagalog is getting better!",
            "🎊 Perfect! You nailed the pronunciation!",
            "💫 Brilliant! You're learning so fast!",
            "🏆 Outstanding! Keep up the great work!",
            "✨ Superb! You're becoming a Tagalog speaker!",
            "🎈 Marvelous! Filipino people would understand you perfectly!"
        ]
        
        # Encouragement messages for pronunciation attempts
        self.encouragement_messages = [
            "Good try! Let's practice that pronunciation again:",
            "Nice effort! Here's how to say it better:",
            "You're learning! Try to pronounce it like this:",
            "Keep trying! Listen carefully and repeat:",
            "Almost there! Let's work on the pronunciation:",
            "Good attempt! Here's the correct way to say it:",
            "You're doing great! Let's practice this sound:",
            "Don't worry! Pronunciation takes practice. Try again:"
        ]
        
        logger.info("FilipinoLearningGame initialized successfully!")
    
    def start_game(self, user: str) -> str:
        """Start the Filipino learning game."""
        self.current_user = user.lower()
        self.game_active = True
        self.score = 0
        self.words_learned = []
        self.waiting_for_english = True
        self.waiting_for_repetition = False
        
        user_name = user.title()
        
        welcome_message = f"""🇵🇭 FILIPINO LEARNING GAME! 🇵🇭

Kumusta {user_name}! Let's learn Filipino (Tagalog) together! 

🎯 HOW TO PLAY:
• Tell me an English word or phrase you want to learn
• I'll translate it to Tagalog and teach you how to say it
• Then you try to repeat the Tagalog pronunciation
• If you get it right, we'll learn another word!

💡 EXAMPLES OF WHAT TO SAY:
• "How do you say 'hello' in Tagalog?"
• "Translate 'thank you'"
• "What is 'water' in Filipino?"
• Or just say the English word like "dog" or "red"

🌟 Ready to start learning? Give me an English word or phrase you'd like to know in Tagalog!"""

        return welcome_message
    
    def process_input(self, user_input: str, user: str) -> str:
        """Process user input - either English for translation or Tagalog repetition."""
        if not self.game_active:
            return "The game isn't active. Say 'Filipino Game' or 'Learn Filipino' to start!"
        
        if self.waiting_for_english:
            return self._handle_english_input(user_input, user)
        elif self.waiting_for_repetition:
            return self._handle_pronunciation_attempt(user_input, user)
        else:
            return "Something went wrong. Let's restart! Give me an English word to translate."
    
    def _handle_english_input(self, user_input: str, user: str) -> str:
        """Handle English word/phrase input for translation."""
        # Extract the English word/phrase from common question formats
        english_word = self._extract_english_from_input(user_input)
        
        if not english_word:
            return """🤔 I didn't catch that! Please tell me an English word or phrase you want to learn in Tagalog.

💡 You can say things like:
• "How do you say 'hello'?"
• "Translate 'thank you'"
• "What is 'water' in Filipino?"
• Or just say "dog" or "red" directly!"""
        
        # Look up the translation
        translation_data = self.translation_database.get(english_word.lower())
        
        if not translation_data:
            return f"""🔍 I don't have '{english_word}' in my Filipino database yet!

📚 Try one of these words I can teach you:
• Family: mom, dad, brother, sister
• Colors: red, blue, green, yellow
• Numbers: one, two, three, four, five
• Greetings: hello, thank you, goodbye
• Animals: dog, cat, bird, fish

Just say an English word from the list above!"""
        
        # Set up for pronunciation practice
        self.current_english = english_word
        self.current_tagalog = translation_data['tagalog']
        self.current_pronunciation = translation_data['pronunciation']
        self.current_attempts = 0
        self.waiting_for_english = False
        self.waiting_for_repetition = True
        
        return f"""🇵🇭 TRANSLATION:

English: "{english_word.title()}"
Tagalog: "{self.current_tagalog}"
Pronunciation: "{self.current_pronunciation}"

🗣️ Now try to say "{self.current_tagalog}" out loud! 

💡 Remember: Listen to how I break it down: {self.current_pronunciation}

Go ahead, give it a try!"""
    
    def _handle_pronunciation_attempt(self, user_input: str, user: str) -> str:
        """Handle user's attempt to pronounce the Tagalog word."""
        self.current_attempts += 1
        
        # Clean and normalize the user's attempt
        user_attempt = self._clean_pronunciation_attempt(user_input)
        target_word = self._clean_pronunciation_attempt(self.current_tagalog)
        
        # Check if pronunciation is close enough
        if self._is_pronunciation_acceptable(user_attempt, target_word):
            # Correct pronunciation!
            self.score += 1
            self.words_learned.append({
                'english': self.current_english,
                'tagalog': self.current_tagalog,
                'pronunciation': self.current_pronunciation
            })
            
            celebration = random.choice(self.celebration_messages)
            
            # Reset for next word
            self.waiting_for_english = True
            self.waiting_for_repetition = False
            self.current_english = None
            self.current_tagalog = None
            self.current_pronunciation = None
            
            return f"""{celebration}

🎯 Perfect! You said "{self.current_tagalog}" correctly!

📊 Words Learned: {self.score}

🌟 Ready for another word? Give me a new English word or phrase you want to learn in Tagalog!"""
        
        else:
            # Incorrect pronunciation
            if self.current_attempts >= self.max_attempts:
                # Maximum attempts reached, move on
                encouragement = random.choice(self.encouragement_messages)
                
                # Reset for next word
                self.waiting_for_english = True
                self.waiting_for_repetition = False
                self.current_english = None
                self.current_tagalog = None
                self.current_pronunciation = None
                
                return f"""💪 Good effort! Pronunciation is tricky - it takes practice!

The word was "{self.current_tagalog}" (pronounced: {self.current_pronunciation})

🌟 Don't worry! Even Filipino kids need practice. Let's try a different word!

Give me another English word you want to learn in Tagalog!"""
            
            else:
                remaining_attempts = self.max_attempts - self.current_attempts
                encouragement = random.choice(self.encouragement_messages)
                
                return f"""{encouragement}

🎯 The word is: "{self.current_tagalog}"
🗣️ Pronunciation guide: "{self.current_pronunciation}"

💡 Try breaking it into syllables and say it slowly!

You have {remaining_attempts} more attempt{'s' if remaining_attempts > 1 else ''}. Try again!"""
    
    def _extract_english_from_input(self, user_input: str) -> str:
        """Extract English word from various question formats."""
        input_lower = user_input.lower().strip()
        
        # Common question patterns
        patterns = [
            r"how do you say['\"]?(.+?)['\"]?(\?|$)",
            r"what is['\"]?(.+?)['\"]?in (tagalog|filipino)",
            r"translate['\"]?(.+?)['\"]?(\?|$)",
            r"how to say['\"]?(.+?)['\"]?(\?|$)",
            r"what's['\"]?(.+?)['\"]?in (tagalog|filipino)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, input_lower)
            if match:
                return match.group(1).strip()
        
        # If no pattern matches, assume the entire input is the English word
        # Remove common question words
        cleaned = re.sub(r'\b(how|do|you|say|what|is|in|tagalog|filipino|translate|the)\b', '', input_lower)
        cleaned = re.sub(r'[^\w\s]', '', cleaned).strip()
        
        if cleaned:
            return cleaned
        
        return None
    
    def _clean_pronunciation_attempt(self, text: str) -> str:
        """Clean and normalize pronunciation attempt for comparison."""
        if not text:
            return ""
        
        # Remove non-alphabetic characters and convert to lowercase
        cleaned = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
    def _is_pronunciation_acceptable(self, user_attempt: str, target_word: str) -> bool:
        """Check if the user's pronunciation attempt is acceptable."""
        if not user_attempt or not target_word:
            return False
        
        # Exact match
        if user_attempt == target_word:
            return True
        
        # Check if user attempt contains the target word
        if target_word in user_attempt or user_attempt in target_word:
            return True
        
        # Check for similar sounds (basic phonetic matching)
        # This is a simplified approach - in a real app you'd use more sophisticated phonetic matching
        similarity_score = self._calculate_similarity(user_attempt, target_word)
        return similarity_score > 0.6  # 60% similarity threshold
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings."""
        if not str1 or not str2:
            return 0.0
        
        # Simple Levenshtein distance-based similarity
        longer = str1 if len(str1) > len(str2) else str2
        shorter = str2 if len(str1) > len(str2) else str1
        
        if len(longer) == 0:
            return 1.0
        
        distance = self._levenshtein_distance(longer, shorter)
        return (len(longer) - distance) / len(longer)
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def get_hint(self, user: str) -> str:
        """Provide pronunciation help for the current word."""
        if not self.game_active:
            return "The game isn't active. Say 'Filipino Game' to start learning!"
        
        if self.waiting_for_english:
            return """💡 I'm waiting for you to give me an English word to translate!

📚 Try asking me to translate:
• Family words: mom, dad, sister, brother
• Colors: red, blue, green, yellow
• Numbers: one, two, three, four
• Greetings: hello, goodbye, thank you"""
        
        elif self.waiting_for_repetition and self.current_tagalog:
            return f"""🗣️ PRONUNCIATION HELP:

Word: "{self.current_tagalog}"
Break it down: "{self.current_pronunciation}"

💡 Tips:
• Say each syllable slowly first
• Most Filipino words end with emphasis on the second-to-last syllable
• 'A' sounds like 'ah' in "father"
• 'I' sounds like 'ee' in "see"
• 'O' sounds like 'oh' in "go"

Try saying it again: "{self.current_tagalog}"!"""
        
        else:
            return "Let's start learning! Give me an English word you want to learn in Tagalog!"
    
    def skip_word(self, user: str) -> str:
        """Skip the current word and get a new English word to translate."""
        if not self.game_active:
            return "The game isn't active. Say 'Filipino Game' to start learning!"
        
        if self.waiting_for_repetition:
            skipped_word = f"{self.current_english} = {self.current_tagalog}"
            
            # Reset for next word
            self.waiting_for_english = True
            self.waiting_for_repetition = False
            self.current_english = None
            self.current_tagalog = None
            self.current_pronunciation = None
            
            return f"""⏭️ No problem! We skipped: {skipped_word}

🌟 Let's try a different word! Give me another English word or phrase you want to learn in Tagalog!"""
        
        else:
            return "Give me an English word you want to learn in Tagalog first!"
    
    def get_game_stats(self, user: str) -> str:
        """Get current learning statistics."""
        if not self.game_active:
            return "No learning session is active. Say 'Filipino Game' to start!"
        
        words_list = []
        for word_data in self.words_learned:
            words_list.append(f"• {word_data['english']} = {word_data['tagalog']}")
        
        words_learned_text = '\n'.join(words_list) if words_list else "None yet - but you're just getting started!"
        
        stats = f"""📊 FILIPINO LEARNING PROGRESS

🏆 Words Learned: {self.score}
🎯 Success Rate: Great job learning!

✅ Words You've Mastered:
{words_learned_text}

🇵🇭 Keep going! Every word you learn brings you closer to speaking Filipino fluently!

Ready for another word? Just tell me an English word to translate!"""

        return stats
    
    def end_game(self, user: str) -> str:
        """End the current learning session and show final progress."""
        if not self.game_active:
            return "No learning session is currently active."
        
        self.game_active = False
        user_name = user.title()
        
        words_list = []
        for word_data in self.words_learned:
            words_list.append(f"• {word_data['english']} = {word_data['tagalog']}")
        
        words_learned_text = '\n'.join(words_list) if words_list else "Keep practicing - you'll get there!"
        
        final_stats = f"""🎮 LEARNING SESSION COMPLETE! Salamat {user_name}!

📊 FINAL PROGRESS:
🏆 Words Learned: {self.score}
🇵🇭 You're on your way to speaking Filipino!

✅ Words You Learned Today:
{words_learned_text}

🌟 Remember to practice these words with your family!

💡 Want to learn more? Just say 'Filipino Game' to start another session!

🎊 Magaling! (That means "Great job!" in Tagalog!)"""

        return final_stats
    
    def get_word_suggestion(self, user: str) -> str:
        """Suggest a random word from the database for translation."""
        if not self.game_active:
            return "Start the Filipino game first! Say 'Filipino Game' to begin learning!"
        
        # Get a random word from the database
        categories = {}
        for english, data in self.translation_database.items():
            category = data['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(english)
        
        # Pick a random category and word
        random_category = random.choice(list(categories.keys()))
        random_word = random.choice(categories[random_category])
        
        return f"""💡 WORD SUGGESTION:

Try learning the word "{random_word}" - it's in the {random_category} category!

Just say "translate {random_word}" or "how do you say {random_word}" and I'll teach you!

Or pick any other English word you want to learn in Tagalog!"""
    
    def get_game_help(self, user: str) -> str:
        """Get help instructions for the Filipino learning game."""
        user_name = user.title()
        
        return f"""🇵🇭 FILIPINO LEARNING GAME HELP - {user_name}

🎯 HOW TO PLAY:
• Tell me an English word/phrase you want to learn
• I'll translate it to Tagalog and teach pronunciation
• You practice saying the Tagalog word
• When you get it right, we learn another word!

🗣️ WHAT TO SAY:
• "Filipino Game" - Start learning session
• "How do you say hello?" - Ask for translation
• "Translate thank you" - Direct translation request
• Just say the English word like "water" or "dog"
• "Hint please" - Get pronunciation help
• "Skip" - Try a different word
• "Stats" - See your learning progress
• "End game" - Finish the session

📚 AVAILABLE CATEGORIES:
• Greetings: hello, thank you, goodbye
• Family: mom, dad, brother, sister
• Colors: red, blue, green, yellow
• Numbers: one through ten
• Body parts: head, eyes, nose, mouth
• Animals: dog, cat, bird, fish
• Food: rice, water, bread, milk

🗣️ PRONUNCIATION TIPS:
• Filipino vowels: A=ah, E=eh, I=ee, O=oh, U=oo
• Most words stress the second-to-last syllable
• Speak clearly and take your time
• Practice makes perfect!

🌟 Remember: Learning a language is a journey! Every word you learn is progress!

Ready to start? Just say "Filipino Game" or give me an English word to translate!"""
    
    def is_game_active(self) -> bool:
        """Check if a learning session is currently active."""
        return self.game_active
    
    def cleanup(self):
        """Clean up game resources."""
        try:
            self.game_active = False
            self.current_english = None
            self.current_tagalog = None
            self.current_pronunciation = None
            self.waiting_for_english = True
            self.waiting_for_repetition = False
            logger.info("FilipinoLearningGame cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during FilipinoLearningGame cleanup: {e}")

# Example usage
if __name__ == "__main__":
    game = FilipinoLearningGame()
    print(game.start_game("TestUser"))
    print(game.process_input("how do you say hello", "TestUser"))
    print(game.process_input("kumusta", "TestUser")) 