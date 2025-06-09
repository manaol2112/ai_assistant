"""
Math Quiz Game Module for AI Assistant
Provides word problems where kids write equations and answers on paper
Uses camera to evaluate work and provides feedback
"""

import logging
import random
import re
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image
import pytesseract

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
        """Check the student's written math work using camera."""
        try:
            if not self.game_active or not self.current_problem:
                return "No math game is currently active. Say 'Math Game' to start!"

            user_name = user.title()
            
            # Capture image from camera
            result = self._capture_and_analyze_math_work()
            
            if not result['success']:
                return f"I couldn't see your work clearly, {user_name}. {result['message']} Try holding your paper closer to the camera with good lighting!"
            
            detected_equation = result.get('equation', '')
            detected_answer = result.get('answer', '')
            
            # Verify the math work
            equation_correct = self._verify_equation(detected_equation, self.current_problem['equation'])
            answer_correct = self._verify_answer(detected_answer, self.current_problem['answer'])
            
            self.problems_answered += 1
            
            # Provide feedback based on correctness
            if equation_correct and answer_correct:
                self.score += 1
                feedback = self._generate_correct_feedback(user, detected_equation, detected_answer)
                sound_type = 'correct'
            elif equation_correct and not answer_correct:
                feedback = self._generate_equation_right_answer_wrong_feedback(user, detected_equation, detected_answer)
                sound_type = 'partial'
            elif not equation_correct and answer_correct:
                feedback = self._generate_equation_wrong_answer_right_feedback(user, detected_equation, detected_answer)
                sound_type = 'partial'
            else:
                feedback = self._generate_incorrect_feedback(user, detected_equation, detected_answer)
                sound_type = 'incorrect'
            
            # Move to next problem or end game
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
            
        except Exception as e:
            logger.error(f"Error checking math answer: {e}")
            return f"Oops! I had trouble checking your work, {user_name}. Let's try again!"

    def _capture_and_analyze_math_work(self) -> Dict:
        """Capture image and analyze math work written on paper."""
        try:
            # Take a photo
            success, frame = self.camera_handler.cap.read()
            if not success:
                return {'success': False, 'message': 'Camera not available'}
            
            # Convert to PIL Image for processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Enhance image for better OCR
            enhanced_image = self._enhance_image_for_math_ocr(pil_image)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(enhanced_image, config='--psm 6')
            
            # Parse equation and answer from text
            parsed_result = self._parse_math_work(extracted_text)
            
            if parsed_result['equation'] or parsed_result['answer']:
                return {
                    'success': True,
                    'equation': parsed_result['equation'],
                    'answer': parsed_result['answer'],
                    'raw_text': extracted_text
                }
            else:
                return {
                    'success': False,
                    'message': 'Could not detect math work clearly'
                }
                
        except Exception as e:
            logger.error(f"Error in math work analysis: {e}")
            return {'success': False, 'message': 'Analysis failed'}

    def _enhance_image_for_math_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image specifically for math equation OCR."""
        # Convert to numpy array
        img_array = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding for better contrast
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Convert back to PIL Image
        return Image.fromarray(cleaned)

    def _parse_math_work(self, text: str) -> Dict[str, str]:
        """Parse equation and answer from OCR text."""
        text = text.strip().replace('\n', ' ')
        
        # Common OCR corrections for math symbols
        text = self._clean_math_text(text)
        
        # Look for equation patterns (like "3 + 2" or "3+2")
        equation_patterns = [
            r'(\d+\s*[+\-×÷∗/]\s*\d+(?:\s*[+\-×÷∗/]\s*\d+)*)',
            r'(\d+\s*[\+\-\*\/]\s*\d+(?:\s*[\+\-\*\/]\s*\d+)*)',
            r'(\(\s*\d+\s*[×∗]\s*\d+\s*\)\s*[+\-]\s*\(\s*\d+\s*[×∗]\s*\d+\s*\))'
        ]
        
        equation = ''
        for pattern in equation_patterns:
            match = re.search(pattern, text)
            if match:
                equation = match.group(1).strip()
                break
        
        # Look for answer patterns (like "= 5" or "5")
        answer_patterns = [
            r'=\s*(\d+)',  # "= 5"
            r'(\d+)(?:\s*$|\s+(?![\+\-×÷∗/]))',  # standalone number
        ]
        
        answer = ''
        for pattern in answer_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Take the last number found (likely the answer)
                answer = matches[-1].strip()
                break
        
        return {
            'equation': equation,
            'answer': answer
        }

    def _clean_math_text(self, text: str) -> str:
        """Clean and correct common OCR errors in math text."""
        # Common OCR corrections
        corrections = {
            'x': '×',
            'X': '×',
            '*': '×',
            '|': '1',
            'l': '1',
            'I': '1',
            'O': '0',
            'o': '0',
            'S': '5',
            's': '5',
            'B': '8',
            'Z': '2',
            'G': '6',
            '÷': '÷',
            '/': '÷'
        }
        
        for wrong, right in corrections.items():
            text = text.replace(wrong, right)
        
        return text

    def _verify_equation(self, detected: str, correct: str) -> bool:
        """Verify if the detected equation matches the correct one."""
        if not detected:
            return False
        
        # Normalize both equations for comparison
        detected_normalized = self._normalize_equation(detected)
        correct_normalized = self._normalize_equation(correct)
        
        return detected_normalized == correct_normalized

    def _verify_answer(self, detected: str, correct: int) -> bool:
        """Verify if the detected answer matches the correct one."""
        if not detected:
            return False
        
        try:
            detected_num = int(detected.strip())
            return detected_num == correct
        except ValueError:
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

    def _generate_equation_right_answer_wrong_feedback(self, user: str, equation: str, answer: str) -> str:
        """Generate feedback when equation is right but answer is wrong."""
        user_name = user.title()
        correct_answer = self.current_problem['answer']
        
        if user == 'sophia':
            feedback = f"Great equation, Sophia! '{equation}' is right! But let's check your math - the answer should be {correct_answer}. 🧮"
        elif user == 'eladriel':
            feedback = f"Good thinking, Eladriel! Your equation '{equation}' is perfect! But the answer should be {correct_answer}. Let's count again! 🦕"
        else:
            feedback = f"Equation correct: {equation}, but answer should be {correct_answer}"
        
        return feedback

    def _generate_equation_wrong_answer_right_feedback(self, user: str, equation: str, answer: str) -> str:
        """Generate feedback when answer is right but equation is wrong."""
        user_name = user.title()
        correct_equation = self.current_problem['equation']
        
        if user == 'sophia':
            feedback = f"Good answer, Sophia! '{answer}' is right! But the equation should be '{correct_equation}'. 📝"
        elif user == 'eladriel':
            feedback = f"Nice counting, Eladriel! '{answer}' is correct! But the equation should be '{correct_equation}'. 🦕"
        else:
            feedback = f"Answer correct: {answer}, but equation should be {correct_equation}"
        
        return feedback

    def _generate_incorrect_feedback(self, user: str, equation: str, answer: str) -> str:
        """Generate feedback for incorrect answers."""
        user_name = user.title()
        correct_equation = self.current_problem['equation']
        correct_answer = self.current_problem['answer']
        hint = self.current_problem['hint']
        
        if user == 'sophia':
            feedback = f"Not quite, Sophia! The equation should be '{correct_equation}' and the answer is {correct_answer}. {hint} ✨"
        elif user == 'eladriel':
            feedback = f"Let's try again, Eladriel! The equation is '{correct_equation}' and the answer is {correct_answer}. {hint} 🦕"
        else:
            feedback = f"Incorrect. Correct equation: {correct_equation}, Answer: {correct_answer}"
        
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
        
        # Check answer commands
        elif self.game_active and any(cmd in user_input_lower for cmd in ['ready', 'done', 'finished', 'check']):
            return self.check_math_answer(user)
        
        # End game commands
        elif any(cmd in user_input_lower for cmd in ['end math', 'stop math', 'quit math']):
            return self.end_game(user)
        
        # Help commands
        elif any(cmd in user_input_lower for cmd in ['math help', 'how to play math']):
            return self.get_help_message(user)
        
        else:
            return "Say 'Math Game' to start, 'Ready' to check your answer, or 'Math Help' for instructions!" 