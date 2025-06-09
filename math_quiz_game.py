"""
Math Quiz Game Module for AI Assistant
Provides word problems where kids write equations and answers on paper
Uses camera and OpenAI vision API to evaluate work and provides feedback
"""

import logging
import random
import re
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class MathQuizGame:
    def __init__(self, camera_handler, ocr_handler=None):
        """Initialize the Math Quiz Game with camera and OCR capabilities."""
        self.camera_handler = camera_handler
        self.ocr_handler = ocr_handler
        self.game_active = False
        self.current_problem = None
        self.problem_index = 0
        self.score = 0
        self.problems_answered = 0
        
        # Math word problems for different difficulty levels
        self.math_problems = {
            'easy': [
                {
                    'problem': "Sarah has 3 apples. Her mom gives her 2 more apples. How many apples does Sarah have now?",
                    'equation': "3 + 2",
                    'answer': 5,
                    'hint': "Count all the apples together!"
                },
                {
                    'problem': "There are 8 birds in a tree. 3 birds fly away. How many birds are left in the tree?",
                    'equation': "8 - 3", 
                    'answer': 5,
                    'hint': "Start with 8 and take away 3!"
                },
                {
                    'problem': "Tom has 4 toy cars. His friend gives him 3 more cars. How many toy cars does Tom have in total?",
                    'equation': "4 + 3",
                    'answer': 7,
                    'hint': "Add the cars Tom had with the new cars!"
                },
                {
                    'problem': "There are 10 cookies in a jar. Mom takes out 4 cookies. How many cookies are left?",
                    'equation': "10 - 4",
                    'answer': 6,
                    'hint': "Start with 10 and subtract 4!"
                },
                {
                    'problem': "Emma sees 6 flowers in the garden. She picks 2 flowers. How many flowers are still in the garden?",
                    'equation': "6 - 2",
                    'answer': 4,
                    'hint': "Take away the flowers Emma picked!"
                }
            ],
            'medium': [
                {
                    'problem': "A box has 15 crayons. Another box has 8 crayons. How many crayons are there altogether?",
                    'equation': "15 + 8",
                    'answer': 23,
                    'hint': "Add the crayons from both boxes!"
                },
                {
                    'problem': "Jake had 20 stickers. He gave 7 stickers to his sister. How many stickers does Jake have left?",
                    'equation': "20 - 7",
                    'answer': 13,
                    'hint': "Subtract the stickers Jake gave away!"
                },
                {
                    'problem': "There are 3 groups of children. Each group has 4 children. How many children are there in total?",
                    'equation': "3 × 4",
                    'answer': 12,
                    'hint': "Multiply groups by children per group!"
                },
                {
                    'problem': "Mom baked 24 cupcakes. She put them equally into 6 boxes. How many cupcakes are in each box?",
                    'equation': "24 ÷ 6",
                    'answer': 4,
                    'hint': "Divide the cupcakes equally among the boxes!"
                },
                {
                    'problem': "Lisa has 12 pencils. She buys 8 more pencils. Then she loses 5 pencils. How many pencils does she have now?",
                    'equation': "12 + 8 - 5",
                    'answer': 15,
                    'hint': "First add, then subtract the lost pencils!"
                }
            ],
            'hard': [
                {
                    'problem': "A farmer has 36 chickens. He sells 1/4 of them. How many chickens did he sell?",
                    'equation': "36 ÷ 4",
                    'answer': 9,
                    'hint': "One-fourth means divide by 4!"
                },
                {
                    'problem': "There are 5 bags with 7 marbles each, and 3 bags with 9 marbles each. How many marbles are there in total?",
                    'equation': "(5 × 7) + (3 × 9)",
                    'answer': 62,
                    'hint': "Calculate each group separately, then add!"
                },
                {
                    'problem': "Amy buys 3 packs of gum. Each pack costs $2. She pays with a $10 bill. How much change does she get?",
                    'equation': "10 - (3 × 2)",
                    'answer': 4,
                    'hint': "First find the total cost, then subtract from $10!"
                }
            ]
        }

    def start_game(self, user: str, difficulty: str = 'easy') -> str:
        """Start a new math quiz game."""
        try:
            self.game_active = True
            self.problem_index = 0
            self.score = 0
            self.problems_answered = 0
            
            # Select difficulty level
            if difficulty not in self.math_problems:
                difficulty = 'easy'
            
            # Shuffle problems for variety
            problems_list = self.math_problems[difficulty].copy()
            random.shuffle(problems_list)
            self.current_problems = problems_list
            
            # Get first problem
            self.current_problem = self.current_problems[self.problem_index]
            
            user_name = user.title()
            
            # Personalized introductions
            if user == 'sophia':
                intro = f"🧮 Hi Sophia! Ready for some fun math problems? Let's solve them together! ✨"
            elif user == 'eladriel':
                intro = f"🦕 Hey Eladriel! Time for a math adventure! Let's count like dinosaurs! 🧮"
            else:  # parent
                intro = f"📊 Parent Mode: Math Quiz Game - {difficulty.title()} Level"
            
            problem_text = self.current_problem['problem']
            hint = self.current_problem['hint']
            
            instructions = f"""{intro}

🧮 MATH PROBLEM TIME! 🧮

Problem #1:
{problem_text}

📝 ON YOUR PAPER, WRITE:
• The math equation (like: 3 + 2)
• The answer (like: = 5)

💡 Hint: {hint}

🗣️ Say 'Ready' when you're done!
👀 Or just show me your paper!

Let's solve this! 🚀"""
            
            return instructions
            
        except Exception as e:
            logger.error(f"Error starting math game: {e}")
            return "Oops! Let's try starting the math game again! 🧮"

    def check_math_answer(self, user: str) -> str:
        """Check the student's written math work using camera and OpenAI vision."""
        try:
            if not self.game_active or not self.current_problem:
                return "No math game is currently active. Say 'Math Game' to start!"

            user_name = user.title()
            
            # Use the same approach as spelling game - OpenAI vision without custom_prompt
            expected_equation = self.current_problem['equation']
            expected_answer = str(self.current_problem['answer'])
            
            # Create expected_word format that the vision system can understand
            expected_math_work = f"{expected_equation} = {expected_answer}"
            
            # Use the existing object identifier with correct parameters
            result = self.ai_assistant.object_identifier.capture_and_identify_text(
                user, 
                expected_word=expected_math_work
            )
            
            if result["success"]:
                ai_description = result["message"].lower()
                
                # Verify the math work using AI description
                equation_correct = self._verify_equation_from_description(ai_description, expected_equation)
                answer_correct = self._verify_answer_from_description(ai_description, expected_answer)
                
                self.problems_answered += 1
                
                # Provide feedback based on correctness
                if equation_correct and answer_correct:
                    self.score += 1
                    feedback = self._generate_correct_feedback(user, expected_equation, expected_answer)
                    
                    # Play correct sound
                    try:
                        if hasattr(self, 'ai_assistant') and self.ai_assistant:
                            self.ai_assistant.play_math_correct_sound()
                    except:
                        pass
                    
                elif equation_correct and not answer_correct:
                    feedback = self._generate_equation_right_answer_wrong_feedback(user, expected_equation, expected_answer)
                    
                    # Play wrong sound
                    try:
                        if hasattr(self, 'ai_assistant') and self.ai_assistant:
                            self.ai_assistant.play_math_wrong_sound()
                    except:
                        pass
                        
                elif not equation_correct and answer_correct:
                    feedback = self._generate_equation_wrong_answer_right_feedback(user, expected_equation, expected_answer)
                    
                    # Play wrong sound  
                    try:
                        if hasattr(self, 'ai_assistant') and self.ai_assistant:
                            self.ai_assistant.play_math_wrong_sound()
                    except:
                        pass
                        
                else:
                    feedback = self._generate_incorrect_feedback(user, expected_equation, expected_answer)
                    
                    # Play wrong sound
                    try:
                        if hasattr(self, 'ai_assistant') and self.ai_assistant:
                            self.ai_assistant.play_math_wrong_sound()
                    except:
                        pass
                
                # Move to next problem or end game automatically if correct
                if equation_correct and answer_correct:
                    if self.problem_index < len(self.current_problems) - 1:
                        self.problem_index += 1
                        self.current_problem = self.current_problems[self.problem_index]
                        next_problem = self._generate_next_problem_text(user)
                        feedback += f"\n\n{next_problem}"
                    else:
                        # Game complete
                        final_score = self._generate_final_score(user)
                        feedback += f"\n\n{final_score}"
                        self.game_active = False
                
                return feedback
            else:
                return f"I can't see your math work clearly, {user_name}. Make sure to write with BIG, dark numbers and hold your paper steady in front of the camera. Say 'Ready' to try again! 📝"
            
        except Exception as e:
            logger.error(f"Error checking math answer: {e}")
            return f"Oops! I had trouble checking your work, {user_name}. Let's try again!"

    def _verify_equation_from_description(self, ai_description: str, expected_equation: str) -> bool:
        """Verify if the equation is correctly written based on AI description."""
        import re
        
        # Normalize the expected equation for comparison
        normalized_expected = self._normalize_equation(expected_equation)
        
        # Look for equation patterns in the AI description
        equation_patterns = [
            rf"{re.escape(expected_equation)}",
            rf"{re.escape(normalized_expected)}",
            rf"equation\s*['\"`]?{re.escape(expected_equation)}['\"`]?",
            rf"written\s*['\"`]?{re.escape(expected_equation)}['\"`]?",
            rf"shows\s*['\"`]?{re.escape(expected_equation)}['\"`]?",
            rf"math\s*['\"`]?{re.escape(expected_equation)}['\"`]?",
        ]
        
        # Also check for the individual numbers and operators
        parts = expected_equation.replace(' ', '').replace('+', ' + ').replace('-', ' - ').replace('×', ' × ').replace('÷', ' ÷ ').split()
        all_parts_found = True
        for part in parts:
            if part.strip() and part not in ai_description:
                all_parts_found = False
                break
        
        # Check patterns or all parts
        for pattern in equation_patterns:
            if re.search(pattern, ai_description, re.IGNORECASE):
                logger.info(f"✅ Equation found in AI description: '{expected_equation}'")
                return True
        
        if all_parts_found and len(parts) >= 3:  # At least number operator number
            logger.info(f"✅ All equation parts found: {parts}")
            return True
        
        logger.info(f"❌ Equation not found in description: '{expected_equation}'")
        return False

    def _verify_answer_from_description(self, ai_description: str, expected_answer: str) -> bool:
        """Verify if the answer is correctly written based on AI description."""
        import re
        
        # Look for answer patterns in the AI description
        answer_patterns = [
            rf"=\s*{re.escape(expected_answer)}",
            rf"answer\s*['\"`]?{re.escape(expected_answer)}['\"`]?",
            rf"equals\s*{re.escape(expected_answer)}",
            rf"result\s*['\"`]?{re.escape(expected_answer)}['\"`]?",
            rf"solution\s*['\"`]?{re.escape(expected_answer)}['\"`]?",
            rf"{re.escape(expected_answer)}\s*written",
            rf"shows\s*{re.escape(expected_answer)}",
        ]
        
        for pattern in answer_patterns:
            if re.search(pattern, ai_description, re.IGNORECASE):
                logger.info(f"✅ Answer found in AI description: '{expected_answer}'")
                return True
        
        # Also check if the number appears prominently
        if expected_answer in ai_description:
            # Make sure it's not just part of the equation
            answer_context_patterns = [
                rf"=.*{re.escape(expected_answer)}",
                rf"{re.escape(expected_answer)}.*answer",
                rf"answer.*{re.escape(expected_answer)}",
                rf"{re.escape(expected_answer)}.*result",
                rf"result.*{re.escape(expected_answer)}",
            ]
            
            for pattern in answer_context_patterns:
                if re.search(pattern, ai_description, re.IGNORECASE):
                    logger.info(f"✅ Answer found in context: '{expected_answer}'")
                    return True
        
        logger.info(f"❌ Answer not found in description: '{expected_answer}'")
        return False

    def _normalize_equation(self, equation: str) -> str:
        """Normalize equation for comparison (remove spaces, standardize operators)."""
        # Remove all spaces
        normalized = equation.replace(' ', '')
        
        # Standardize operators
        normalized = normalized.replace('*', '×')
        normalized = normalized.replace('x', '×')
        normalized = normalized.replace('X', '×')
        normalized = normalized.replace('/', '÷')
        
        return normalized.lower()

    def _generate_correct_feedback(self, user: str, equation: str, answer: str) -> str:
        """Generate feedback for completely correct answers."""
        user_name = user.title()
        
        if user == 'sophia':
            feedback = f"🌟 Perfect, Sophia! Your equation '{equation}' and answer '{answer}' are exactly right! ✨"
        elif user == 'eladriel':
            feedback = f"🦕 Roar-some work, Eladriel! Your math '{equation} = {answer}' is perfect! 🌟"
        else:
            feedback = f"✅ Correct! Equation: {equation}, Answer: {answer}"
        
        return feedback

    def _generate_equation_right_answer_wrong_feedback(self, user: str, equation: str, expected_answer: str) -> str:
        """Generate feedback when equation is right but answer is wrong."""
        user_name = user.title()
        
        if user == 'sophia':
            feedback = f"Great equation, Sophia! '{equation}' is right! But let's check your math - the answer should be {expected_answer}. 🧮"
        elif user == 'eladriel':
            feedback = f"Good thinking, Eladriel! Your equation '{equation}' is perfect! But the answer should be {expected_answer}. Let's count again! 🦕"
        else:
            feedback = f"Equation correct: {equation}, but answer should be {expected_answer}"
        
        return feedback

    def _generate_equation_wrong_answer_right_feedback(self, user: str, expected_equation: str, answer: str) -> str:
        """Generate feedback when answer is right but equation is wrong."""
        user_name = user.title()
        
        if user == 'sophia':
            feedback = f"Good answer, Sophia! '{answer}' is right! But the equation should be '{expected_equation}'. 📝"
        elif user == 'eladriel':
            feedback = f"Nice counting, Eladriel! '{answer}' is correct! But the equation should be '{expected_equation}'. 🦕"
        else:
            feedback = f"Answer correct: {answer}, but equation should be {expected_equation}"
        
        return feedback

    def _generate_incorrect_feedback(self, user: str, expected_equation: str, expected_answer: str) -> str:
        """Generate feedback for incorrect answers."""
        user_name = user.title()
        hint = self.current_problem['hint']
        
        if user == 'sophia':
            feedback = f"Not quite, Sophia! The equation should be '{expected_equation}' and the answer is {expected_answer}. {hint} ✨"
        elif user == 'eladriel':
            feedback = f"Let's try again, Eladriel! The equation is '{expected_equation}' and the answer is {expected_answer}. {hint} 🦕"
        else:
            feedback = f"Incorrect. Correct equation: {expected_equation}, Answer: {expected_answer}"
        
        return feedback

    def _generate_next_problem_text(self, user: str) -> str:
        """Generate text for the next problem."""
        problem_num = self.problem_index + 1
        problem_text = self.current_problem['problem']
        hint = self.current_problem['hint']
        
        if user == 'sophia':
            intro = f"🌟 Ready for problem #{problem_num}, Sophia?"
        elif user == 'eladriel':
            intro = f"🦕 Next adventure, Eladriel! Problem #{problem_num}:"
        else:
            intro = f"Problem #{problem_num}:"
        
        return f"""{intro}

{problem_text}

💡 Hint: {hint}

📝 Write your equation and answer, then say 'Ready'!"""

    def _generate_final_score(self, user: str) -> str:
        """Generate final score message."""
        user_name = user.title()
        percentage = (self.score / self.problems_answered * 100) if self.problems_answered > 0 else 0
        
        if user == 'sophia':
            if percentage >= 80:
                message = f"🌟 Amazing job, Sophia! You got {self.score} out of {self.problems_answered} problems right! You're a math star! ✨"
            elif percentage >= 60:
                message = f"Great work, Sophia! You got {self.score} out of {self.problems_answered} right! Keep practicing! 🌟"
            else:
                message = f"Good try, Sophia! You got {self.score} out of {self.problems_answered} right! Math takes practice! 💪"
        elif user == 'eladriel':
            if percentage >= 80:
                message = f"🦕 Dino-mite work, Eladriel! You got {self.score} out of {self.problems_answered} problems right! You're a math-a-saurus! 🌟"
            elif percentage >= 60:
                message = f"Roar-some job, Eladriel! You got {self.score} out of {self.problems_answered} right! Keep counting! 🦕"
            else:
                message = f"Good effort, Eladriel! You got {self.score} out of {self.problems_answered} right! Even dinosaurs practice math! 💪"
        else:
            message = f"Game Complete! Score: {self.score}/{self.problems_answered} ({percentage:.0f}%)"
        
        return f"{message}\n\n🧮 Say 'Math Game' anytime to play again!"

    def end_game(self, user: str) -> str:
        """End the current math game."""
        if not self.game_active:
            return "No math game is currently active."
        
        user_name = user.title()
        self.game_active = False
        
        final_score = f"Game ended! You answered {self.problems_answered} problems and got {self.score} correct."
        
        if user == 'sophia':
            return f"Math game ended, Sophia! {final_score} Great job practicing! 🌟"
        elif user == 'eladriel':
            return f"Math adventure complete, Eladriel! {final_score} You're getting stronger at math! 🦕"
        else:
            return f"Math game ended. {final_score}"

    def get_help_message(self, user: str) -> str:
        """Get help instructions for the math game."""
        if user == 'sophia':
            return """🧮 MATH GAME HELP - Sophia 🌟

HOW TO PLAY:
• I'll give you word problems to solve
• Write the equation AND answer on paper
• Say 'Ready' when you're done!
• I'll check your work with my camera

EXAMPLE:
Problem: "You have 3 toys and get 2 more. How many total?"
Write: "3 + 2 = 5"

TIPS:
• Write BIG and CLEAR numbers
• Show your paper to the camera
• Ask for help if you need it!

Say 'Math Game' to start! ✨"""
        
        elif user == 'eladriel':
            return """🦕 MATH ADVENTURE HELP - Eladriel 🧮

DINO-MATH RULES:
• I tell you math stories to solve
• Write equation AND answer like a paleontologist!
• Roar 'Ready' when you're done!
• I'll check with my dino-vision

EXAMPLE:
Problem: "5 dinosaurs, 3 walk away. How many left?"
Write: "5 - 3 = 2"

DINO-TIPS:
• Write with dino-sized numbers!
• Hold paper steady for my dino-eyes
• Ask for help anytime!

Say 'Math Game' to start the adventure! 🌟"""
        
        else:
            return """📊 MATH GAME HELP

GAME MECHANICS:
• Word problems with visual answer checking
• Students write equation + answer on paper
• Camera OCR analyzes mathematical work
• Provides detailed feedback and progression

DIFFICULTY LEVELS:
• Easy: Addition/subtraction (1-20)
• Medium: Multi-step, multiplication/division
• Hard: Fractions, multi-operation problems

FEATURES:
• Equation accuracy verification
• Answer correctness checking
• Progressive difficulty
• Score tracking
• Audio feedback integration"""

    def is_math_game_command(self, user_input: str) -> bool:
        """Check if user input is a math game command."""
        math_commands = [
            'math game', 'math quiz', 'math problems', 'word problems',
            'start math', 'play math', 'math practice', 'solve problems'
        ]
        user_input_lower = user_input.lower()
        return any(cmd in user_input_lower for cmd in math_commands)

    def handle_math_command(self, user_input: str, user: str) -> str:
        """Handle math game related commands."""
        user_input_lower = user_input.lower()
        
        # Start game commands
        if any(cmd in user_input_lower for cmd in ['math game', 'start math', 'play math']):
            difficulty = 'easy'  # Default difficulty
            if 'medium' in user_input_lower or 'harder' in user_input_lower:
                difficulty = 'medium'
            elif 'hard' in user_input_lower or 'difficult' in user_input_lower:
                difficulty = 'hard'
            return self.start_game(user, difficulty)
        
        # Check for verbal answers when game is active
        elif self.game_active and self.current_problem:
            # Check for verbal answer patterns
            verbal_answer = self._extract_verbal_answer(user_input_lower)
            if verbal_answer is not None:
                return self._handle_verbal_answer(verbal_answer, user)
        
        # Check answer commands (camera-based)
        if self.game_active and any(cmd in user_input_lower for cmd in ['ready', 'done', 'finished', 'check']):
            return self.check_math_answer(user)
        
        # End game commands
        elif any(cmd in user_input_lower for cmd in ['end math', 'stop math', 'quit math']):
            return self.end_game(user)
        
        # Help commands
        elif any(cmd in user_input_lower for cmd in ['math help', 'how to play math']):
            return self.get_help_message(user)
        
        else:
            return "Say 'Math Game' to start, 'Ready' to check your answer, or 'Math Help' for instructions!"

    def _extract_verbal_answer(self, user_input: str) -> int:
        """Extract numerical answer from verbal input."""
        import re
        
        # Common patterns for verbal answers
        answer_patterns = [
            r'the answer is (\d+)',
            r'answer is (\d+)',
            r'it is (\d+)',
            r'it\'s (\d+)',
            r'equals (\d+)',
            r'is (\d+)',
            r'^(\d+)$',  # Just a number
            r'(\d+) is the answer',
            r'(\d+) is my answer'
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, user_input)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        # Check for number words
        number_words = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20
        }
        
        for word, num in number_words.items():
            if f'answer is {word}' in user_input or f'the answer is {word}' in user_input:
                return num
        
        return None

    def _handle_verbal_answer(self, verbal_answer: int, user: str) -> str:
        """Handle verbal answer from student."""
        user_name = user.title()
        correct_answer = self.current_problem['answer']
        
        self.problems_answered += 1
        
        if verbal_answer == correct_answer:
            # Correct answer - automatically move to next problem
            self.score += 1
            
            # Play correct sound if available
            try:
                if hasattr(self, 'ai_assistant') and self.ai_assistant:
                    self.ai_assistant.play_math_correct_sound()
            except:
                pass
            
            if user == 'sophia':
                feedback = f"🌟 Excellent, Sophia! {verbal_answer} is exactly right!"
            elif user == 'eladriel':
                feedback = f"🦕 Roar-some, Eladriel! {verbal_answer} is perfect!"
            else:
                feedback = f"Correct! The answer is {verbal_answer}."
            
            # Automatically move to next problem
            if self.problem_index < len(self.current_problems) - 1:
                self.problem_index += 1
                self.current_problem = self.current_problems[self.problem_index]
                next_problem = self._generate_next_problem_text(user)
                feedback += f"\n\n{next_problem}"
            else:
                # Game complete
                final_score = self._generate_final_score(user)
                feedback += f"\n\n{final_score}"
                self.game_active = False
            
            return feedback
        else:
            # Wrong answer - give hint and stay on same problem
            try:
                if hasattr(self, 'ai_assistant') and self.ai_assistant:
                    self.ai_assistant.play_math_wrong_sound()
            except:
                pass
            
            hint = self.current_problem['hint']
            if user == 'sophia':
                return f"Not quite, Sophia! The answer isn't {verbal_answer}. {hint} Try again! ✨"
            elif user == 'eladriel':
                return f"Hmm, not quite, Eladriel! The answer isn't {verbal_answer}. {hint} Keep trying! 🦕"
            else:
                return f"Incorrect. The answer isn't {verbal_answer}. {hint}" 