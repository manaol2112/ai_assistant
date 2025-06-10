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
        
        # Word database organized by letters with hints
        self.word_database = {
            'A': [
                {'word': 'APPLE', 'hint': 'A round, red or green fruit that grows on trees. Snow White ate one!'},
                {'word': 'AIRPLANE', 'hint': 'A big machine that flies in the sky and carries people to faraway places.'},
                {'word': 'ANT', 'hint': 'A tiny insect that works very hard and carries food back to its home.'},
                {'word': 'ALLIGATOR', 'hint': 'A large green animal with big teeth that lives in water and swamps.'},
                {'word': 'ASTRONAUT', 'hint': 'A person who travels to space and walks on the moon!'},
                {'word': 'AMBULANCE', 'hint': 'A special vehicle that helps sick people get to the hospital quickly.'},
                {'word': 'ARROW', 'hint': 'A pointy stick that flies through the air when shot from a bow.'},
                {'word': 'ANCHOR', 'hint': 'A heavy metal object that keeps boats from floating away.'}
            ],
            'B': [
                {'word': 'BUTTERFLY', 'hint': 'A beautiful insect with colorful wings that flies from flower to flower.'},
                {'word': 'BANANA', 'hint': 'A long, yellow fruit that monkeys love to eat.'},
                {'word': 'BEAR', 'hint': 'A big, furry animal that loves honey and sleeps all winter.'},
                {'word': 'BALL', 'hint': 'A round toy that you can throw, catch, or kick.'},
                {'word': 'BIRD', 'hint': 'An animal with feathers and wings that can fly and sing beautiful songs.'},
                {'word': 'BOOK', 'hint': 'Something with pages full of stories and pictures that you can read.'},
                {'word': 'BICYCLE', 'hint': 'A vehicle with two wheels that you pedal with your feet to move.'},
                {'word': 'BALLOON', 'hint': 'A colorful, round thing that floats in the air when filled with gas.'}
            ],
            'C': [
                {'word': 'CAT', 'hint': 'A furry pet that says "meow" and loves to chase mice.'},
                {'word': 'CAR', 'hint': 'A vehicle with four wheels that drives on roads and takes you places.'},
                {'word': 'CAKE', 'hint': 'A sweet dessert that you eat on birthdays with candles on top.'},
                {'word': 'CASTLE', 'hint': 'A big, stone building where kings and queens used to live.'},
                {'word': 'CLOUD', 'hint': 'White, fluffy things in the sky that sometimes bring rain.'},
                {'word': 'COOKIE', 'hint': 'A small, sweet treat that you can eat as a snack.'},
                {'word': 'CROWN', 'hint': 'A golden hat with jewels that kings and queens wear on their heads.'},
                {'word': 'CARROT', 'hint': 'An orange vegetable that grows underground and rabbits love to eat.'}
            ],
            'D': [
                {'word': 'DOG', 'hint': 'A loyal pet that barks, wags its tail, and loves to play fetch.'},
                {'word': 'DINOSAUR', 'hint': 'A huge, ancient animal that lived millions of years ago like T-Rex!'},
                {'word': 'DRAGON', 'hint': 'A magical creature from stories that can breathe fire and fly.'},
                {'word': 'DUCK', 'hint': 'A bird that swims in ponds, says "quack," and has webbed feet.'},
                {'word': 'DONUT', 'hint': 'A round, sweet food with a hole in the middle, often covered in sprinkles.'},
                {'word': 'DOOR', 'hint': 'Something you open and close to go in and out of rooms.'},
                {'word': 'DOLPHIN', 'hint': 'A smart, gray sea animal that jumps out of water and is very friendly.'},
                {'word': 'DRUM', 'hint': 'A musical instrument that you hit with sticks to make loud sounds.'}
            ],
            'E': [
                {'word': 'ELEPHANT', 'hint': 'The biggest land animal with a long nose called a trunk.'},
                {'word': 'EGG', 'hint': 'A round, white thing that chickens lay and you can cook for breakfast.'},
                {'word': 'EAGLE', 'hint': 'A large bird with sharp eyes that soars high in the sky.'},
                {'word': 'EARTH', 'hint': 'The planet we live on with land, water, and all the animals.'},
                {'word': 'ERASER', 'hint': 'A small, rubbery thing that removes pencil marks from paper.'},
                {'word': 'ENGINE', 'hint': 'The part of a car or train that makes it move and go fast.'},
                {'word': 'ENVELOPE', 'hint': 'A paper holder that you put letters in before mailing them.'},
                {'word': 'ELBOW', 'hint': 'The bendy part in the middle of your arm.'}
            ],
            'F': [
                {'word': 'FISH', 'hint': 'An animal that swims in water and breathes through gills.'},
                {'word': 'FROG', 'hint': 'A green animal that hops and says "ribbit" and lives near ponds.'},
                {'word': 'FLOWER', 'hint': 'A colorful, pretty plant that smells nice and attracts bees.'},
                {'word': 'FIRE', 'hint': 'Hot, orange flames that give light and heat but can be dangerous.'},
                {'word': 'FLAG', 'hint': 'A colorful piece of cloth that represents a country and waves in the wind.'},
                {'word': 'FORK', 'hint': 'A tool with pointy ends that you use to eat food.'},
                {'word': 'FOOTBALL', 'hint': 'An oval-shaped ball used in a sport where players try to score touchdowns.'},
                {'word': 'FEATHER', 'hint': 'A light, soft thing that covers birds and helps them fly.'}
            ],
            'G': [
                {'word': 'GIRAFFE', 'hint': 'The tallest animal in the world with a very long neck and spots.'},
                {'word': 'GUITAR', 'hint': 'A musical instrument with strings that you play with your fingers.'},
                {'word': 'GRAPES', 'hint': 'Small, round, purple or green fruits that grow in bunches.'},
                {'word': 'GHOST', 'hint': 'A spooky, white spirit from scary stories that says "BOO!"'},
                {'word': 'GIFT', 'hint': 'A present wrapped in pretty paper that you give to someone special.'},
                {'word': 'GLOBE', 'hint': 'A round model of Earth that spins and shows all the countries.'},
                {'word': 'GOAT', 'hint': 'A farm animal with horns that likes to climb and eat grass.'},
                {'word': 'GOLDFISH', 'hint': 'A small, orange fish that swims in a bowl and is kept as a pet.'}
            ],
            'H': [
                {'word': 'HORSE', 'hint': 'A large animal that people can ride and says "neigh."'},
                {'word': 'HOUSE', 'hint': 'A building where people live with rooms, doors, and windows.'},
                {'word': 'HAT', 'hint': 'Something you wear on your head to keep warm or look stylish.'},
                {'word': 'HEART', 'hint': 'The part of your body that pumps blood and represents love.'},
                {'word': 'HAMMER', 'hint': 'A tool used to hit nails into wood when building things.'},
                {'word': 'HELICOPTER', 'hint': 'A flying machine with spinning blades on top that can hover in air.'},
                {'word': 'HONEY', 'hint': 'A sweet, golden liquid that bees make in their hives.'},
                {'word': 'HIPPO', 'hint': 'A huge, gray animal that loves water and has a very big mouth.'}
            ],
            'I': [
                {'word': 'ICE', 'hint': 'Frozen water that is cold, slippery, and melts in warm weather.'},
                {'word': 'IGLOO', 'hint': 'A round house made of ice blocks where Eskimos live.'},
                {'word': 'ISLAND', 'hint': 'A piece of land completely surrounded by water.'},
                {'word': 'INSECT', 'hint': 'A tiny creature with six legs like ants, bees, or butterflies.'},
                {'word': 'IRON', 'hint': 'A hot tool used to make wrinkled clothes smooth and flat.'},
                {'word': 'ICICLE', 'hint': 'A long, pointy piece of ice that hangs down from roofs in winter.'},
                {'word': 'IGUANA', 'hint': 'A large, green lizard that likes to sit in the sun.'},
                {'word': 'INK', 'hint': 'The colored liquid inside pens that makes marks when you write.'}
            ],
            'J': [
                {'word': 'JUNGLE', 'hint': 'A thick forest full of trees, vines, and wild animals.'},
                {'word': 'JUICE', 'hint': 'A sweet drink made from fruits like oranges or apples.'},
                {'word': 'JELLYFISH', 'hint': 'A see-through sea creature that looks like jelly and can sting.'},
                {'word': 'JACKET', 'hint': 'A piece of clothing you wear over your shirt to stay warm.'},
                {'word': 'JUMP', 'hint': 'To push yourself up in the air with your legs and land back down.'},
                {'word': 'JAR', 'hint': 'A glass container with a lid used to store food like jam or cookies.'},
                {'word': 'JEWEL', 'hint': 'A precious, shiny stone like diamonds that sparkle in the light.'},
                {'word': 'JIGSAW', 'hint': 'A puzzle made of many pieces that fit together to make a picture.'}
            ],
            'K': [
                {'word': 'KANGAROO', 'hint': 'An animal from Australia that hops on strong legs and carries babies in a pouch.'},
                {'word': 'KITE', 'hint': 'A colorful toy that flies high in the sky when the wind blows.'},
                {'word': 'KING', 'hint': 'A man who rules a kingdom and wears a crown on his head.'},
                {'word': 'KITTEN', 'hint': 'A baby cat that is small, cute, and loves to play.'},
                {'word': 'KITCHEN', 'hint': 'The room in your house where food is cooked and prepared.'},
                {'word': 'KEY', 'hint': 'A small metal object that opens locks and doors.'},
                {'word': 'KNEE', 'hint': 'The bendy part in the middle of your leg that helps you walk.'},
                {'word': 'KOALA', 'hint': 'A cute, gray animal from Australia that climbs trees and eats leaves.'}
            ],
            'L': [
                {'word': 'LION', 'hint': 'The king of the jungle with a big mane who roars very loudly.'},
                {'word': 'LADDER', 'hint': 'A tall tool with steps that you climb to reach high places.'},
                {'word': 'LAMP', 'hint': 'Something that gives light when you turn it on in dark rooms.'},
                {'word': 'LEAF', 'hint': 'The green part of trees and plants that falls off in autumn.'},
                {'word': 'LETTER', 'hint': 'A message written on paper that you send to friends in the mail.'},
                {'word': 'LIZARD', 'hint': 'A small reptile with a long tail that likes to sit on rocks.'},
                {'word': 'LEMON', 'hint': 'A yellow, sour fruit that makes your face scrunch up when you taste it.'},
                {'word': 'LIBRARY', 'hint': 'A quiet place full of books where you can read and learn.'}
            ],
            'M': [
                {'word': 'MOUSE', 'hint': 'A tiny animal with a long tail that cats like to chase.'},
                {'word': 'MOON', 'hint': 'The big, round, white light you see in the sky at night.'},
                {'word': 'MONKEY', 'hint': 'A playful animal that swings from trees and loves bananas.'},
                {'word': 'MOUNTAIN', 'hint': 'A very tall, rocky hill that reaches up toward the clouds.'},
                {'word': 'MIRROR', 'hint': 'A shiny surface that shows your reflection when you look at it.'},
                {'word': 'MILK', 'hint': 'A white drink that comes from cows and makes your bones strong.'},
                {'word': 'MAGIC', 'hint': 'Special tricks and spells that seem impossible but are amazing to watch.'},
                {'word': 'MERMAID', 'hint': 'A magical sea creature that is half person and half fish.'}
            ],
            'N': [
                {'word': 'NEST', 'hint': 'A cozy home that birds build in trees to keep their eggs safe.'},
                {'word': 'NOSE', 'hint': 'The part of your face that helps you smell flowers and food.'},
                {'word': 'NIGHT', 'hint': 'The dark time when the sun goes down and stars come out.'},
                {'word': 'NURSE', 'hint': 'A kind person who helps doctors take care of sick people.'},
                {'word': 'NECKLACE', 'hint': 'Pretty jewelry that you wear around your neck.'},
                {'word': 'NOTEBOOK', 'hint': 'A book with blank pages where you can write or draw pictures.'},
                {'word': 'NUTS', 'hint': 'Hard-shelled foods that squirrels love to collect and eat.'},
                {'word': 'NEEDLE', 'hint': 'A thin, sharp tool used for sewing clothes and fabric together.'}
            ],
            'O': [
                {'word': 'OCTOPUS', 'hint': 'A sea creature with eight long arms that can change colors.'},
                {'word': 'ORANGE', 'hint': 'A round, orange fruit full of vitamin C that\'s sweet and juicy.'},
                {'word': 'OWL', 'hint': 'A wise bird with big eyes that hoots and hunts at night.'},
                {'word': 'OCEAN', 'hint': 'A huge body of salty water where whales, fish, and dolphins live.'},
                {'word': 'OVEN', 'hint': 'A hot box in the kitchen used to bake cookies and cook food.'},
                {'word': 'ONION', 'hint': 'A round vegetable with layers that makes you cry when you cut it.'},
                {'word': 'OSTRICH', 'hint': 'The biggest bird in the world that can\'t fly but runs very fast.'},
                {'word': 'OTTER', 'hint': 'A playful water animal with thick fur that slides down muddy banks.'}
            ],
            'P': [
                {'word': 'PENGUIN', 'hint': 'A black and white bird that can\'t fly but is an excellent swimmer.'},
                {'word': 'PIZZA', 'hint': 'A round food with cheese and toppings that everyone loves to eat.'},
                {'word': 'PUPPY', 'hint': 'A baby dog that is playful, cute, and loves to chew on things.'},
                {'word': 'PRINCESS', 'hint': 'A royal lady who lives in a castle and might marry a prince.'},
                {'word': 'PIANO', 'hint': 'A big musical instrument with black and white keys that you press.'},
                {'word': 'PARROT', 'hint': 'A colorful bird that can copy words and sounds that people make.'},
                {'word': 'PEACOCK', 'hint': 'A beautiful bird with a long neck and colorful tail feathers like a fan.'},
                {'word': 'PANDA', 'hint': 'A black and white bear from China that loves to eat bamboo.'}
            ],
            'Q': [
                {'word': 'QUEEN', 'hint': 'A royal woman who rules a kingdom and wears a beautiful crown.'},
                {'word': 'QUACK', 'hint': 'The sound that ducks make when they talk to each other.'},
                {'word': 'QUESTION', 'hint': 'Something you ask when you want to learn or know more about something.'},
                {'word': 'QUILT', 'hint': 'A warm blanket made from many colorful pieces of fabric sewn together.'},
                {'word': 'QUIET', 'hint': 'Making no noise at all, like when everyone is sleeping.'},
                {'word': 'QUARTER', 'hint': 'A silver coin worth 25 cents that you can use to buy things.'},
                {'word': 'QUIVER', 'hint': 'A container that holds arrows for people who use bows.'},
                {'word': 'QUAIL', 'hint': 'A small, plump bird that makes its nest on the ground.'}
            ],
            'R': [
                {'word': 'RABBIT', 'hint': 'A soft, furry animal with long ears that hops and loves carrots.'},
                {'word': 'RAINBOW', 'hint': 'Beautiful colors that appear in the sky after it rains.'},
                {'word': 'ROBOT', 'hint': 'A mechanical person made of metal that can move and do tasks.'},
                {'word': 'ROCKET', 'hint': 'A space ship that blasts off and flies to the moon and stars.'},
                {'word': 'ROSE', 'hint': 'A beautiful red flower with thorns that smells very sweet.'},
                {'word': 'RIVER', 'hint': 'A long stream of water that flows from mountains to the ocean.'},
                {'word': 'RING', 'hint': 'A circular piece of jewelry that people wear on their fingers.'},
                {'word': 'RHINOCEROS', 'hint': 'A huge, gray animal with a horn on its nose that lives in Africa.'}
            ],
            'S': [
                {'word': 'SNAKE', 'hint': 'A long, slithery animal with no legs that moves by wiggling its body.'},
                {'word': 'STAR', 'hint': 'A bright, twinkling light in the night sky that\'s very far away.'},
                {'word': 'SPIDER', 'hint': 'An eight-legged creature that spins webs to catch flies.'},
                {'word': 'SNOWMAN', 'hint': 'A person made of snow with a carrot nose and coal for eyes.'},
                {'word': 'SUBMARINE', 'hint': 'A boat that can go underwater to explore the deep ocean.'},
                {'word': 'SANDWICH', 'hint': 'Food made with two pieces of bread and yummy things in between.'},
                {'word': 'SUNFLOWER', 'hint': 'A tall, yellow flower that always turns to face the sun.'},
                {'word': 'SQUIRREL', 'hint': 'A small animal with a bushy tail that collects nuts for winter.'}
            ],
            'T': [
                {'word': 'TIGER', 'hint': 'A big, orange cat with black stripes that lives in the jungle.'},
                {'word': 'TURTLE', 'hint': 'A slow animal that carries its house on its back and can hide inside.'},
                {'word': 'TRAIN', 'hint': 'A long vehicle that runs on tracks and makes "choo-choo" sounds.'},
                {'word': 'TREE', 'hint': 'A tall plant with leaves, branches, and a thick brown trunk.'},
                {'word': 'TELESCOPE', 'hint': 'A tool that makes faraway things look bigger, like stars and planets.'},
                {'word': 'TREASURE', 'hint': 'Valuable things like gold and jewels that pirates bury in chests.'},
                {'word': 'TORNADO', 'hint': 'A spinning wind storm that looks like a gray funnel in the sky.'},
                {'word': 'TROPHY', 'hint': 'A shiny prize you get when you win a game or competition.'}
            ],
            'U': [
                {'word': 'UMBRELLA', 'hint': 'Something you hold over your head to stay dry when it rains.'},
                {'word': 'UNICORN', 'hint': 'A magical horse with a horn on its head from fairy tales.'},
                {'word': 'UNIVERSE', 'hint': 'Everything that exists including all the stars, planets, and space.'},
                {'word': 'UNIFORM', 'hint': 'Special clothes that people wear for work, like police or firefighters.'},
                {'word': 'UNDERWATER', 'hint': 'Below the surface of water where fish swim and coral grows.'},
                {'word': 'UNCLE', 'hint': 'Your mom or dad\'s brother who is part of your family.'},
                {'word': 'UPSET', 'hint': 'How you feel when something makes you sad or angry.'},
                {'word': 'UPSTAIRS', 'hint': 'The higher level of a house where you go up steps to reach.'}
            ],
            'V': [
                {'word': 'VIOLIN', 'hint': 'A musical instrument that you hold under your chin and play with a bow.'},
                {'word': 'VOLCANO', 'hint': 'A mountain that sometimes erupts with hot lava and ash.'},
                {'word': 'VAMPIRE', 'hint': 'A spooky creature from stories that sleeps during the day.'},
                {'word': 'VEGETABLE', 'hint': 'Healthy food that grows in gardens like carrots, peas, and broccoli.'},
                {'word': 'VILLAGE', 'hint': 'A small town where not many people live, smaller than a city.'},
                {'word': 'VACUUM', 'hint': 'A machine that sucks up dirt and dust from carpets and floors.'},
                {'word': 'VALLEY', 'hint': 'Low land between hills or mountains where rivers often flow.'},
                {'word': 'VEST', 'hint': 'A piece of clothing worn over a shirt that has no sleeves.'}
            ],
            'W': [
                {'word': 'WHALE', 'hint': 'The biggest animal in the ocean that spouts water from its head.'},
                {'word': 'WIZARD', 'hint': 'A magical person who casts spells and has a long beard and pointy hat.'},
                {'word': 'WATERFALL', 'hint': 'Water that falls down from high rocks making a beautiful rushing sound.'},
                {'word': 'WOLF', 'hint': 'A wild animal that looks like a big dog and howls at the moon.'},
                {'word': 'WINDMILL', 'hint': 'A tall building with spinning blades that uses wind to make power.'},
                {'word': 'WORM', 'hint': 'A long, squishy creature that lives in dirt and helps plants grow.'},
                {'word': 'WINDOW', 'hint': 'A clear opening in walls that lets you see outside and lets light in.'},
                {'word': 'WITCH', 'hint': 'A magical person from stories who rides a broomstick and makes potions.'}
            ],
            'X': [
                {'word': 'XRAY', 'hint': 'A special picture that doctors take to see inside your body and bones.'},
                {'word': 'XYLOPHONE', 'hint': 'A musical instrument with colorful bars that you hit with mallets.'},
                {'word': 'XERUS', 'hint': 'A type of ground squirrel that lives in Africa and digs burrows.'},
                {'word': 'XENOPS', 'hint': 'A small bird from South America with a curved beak.'},
                {'word': 'XBOX', 'hint': 'A video game console that you can play fun games on with controllers.'},
                {'word': 'XEROX', 'hint': 'A machine that makes copies of papers and documents.'},
                {'word': 'XYLEM', 'hint': 'The part of plants that carries water from roots up to the leaves.'},
                {'word': 'XMAS', 'hint': 'A short way to write Christmas, the holiday with presents and Santa.'}
            ],
            'Y': [
                {'word': 'YACHT', 'hint': 'A fancy, big boat that rich people use for sailing on the ocean.'},
                {'word': 'YARD', 'hint': 'The grassy area around your house where you can play outside.'},
                {'word': 'YELL', 'hint': 'To shout very loudly when you want someone far away to hear you.'},
                {'word': 'YELLOW', 'hint': 'A bright, sunny color like bananas, lemons, and the sun.'},
                {'word': 'YOGA', 'hint': 'Gentle exercises where you stretch and bend your body in peaceful ways.'},
                {'word': 'YAWN', 'hint': 'What you do when you\'re tired - opening your mouth wide and breathing deep.'},
                {'word': 'YARN', 'hint': 'Soft, colorful string used for knitting sweaters and making crafts.'},
                {'word': 'YOLK', 'hint': 'The yellow part inside an egg that\'s round and nutritious.'}
            ],
            'Z': [
                {'word': 'ZEBRA', 'hint': 'A horse-like animal from Africa with black and white stripes.'},
                {'word': 'ZOO', 'hint': 'A place where you can visit and see animals from all around the world.'},
                {'word': 'ZIPPER', 'hint': 'A fastener on clothes and bags that opens and closes with a sliding tab.'},
                {'word': 'ZERO', 'hint': 'The number that means nothing or none, shaped like a circle.'},
                {'word': 'ZONE', 'hint': 'A special area or section set aside for particular activities.'},
                {'word': 'ZOOM', 'hint': 'To move very fast or to make something look bigger and closer.'},
                {'word': 'ZUCCHINI', 'hint': 'A long, green vegetable that grows in gardens and is good for you.'},
                {'word': 'ZIGZAG', 'hint': 'A pattern that goes back and forth like lightning or stairs.'}
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
        
        # Clean up the answer
        clean_answer = user_answer.strip().upper()
        
        # Check if the answer is correct
        if clean_answer == self.current_word:
            self.score += 1
            self.words_completed.append(self.current_word)
            
            # Celebrate the correct answer
            celebration = random.choice(self.celebration_messages)
            
            # Prepare next word
            next_word_message = self._prepare_next_word()
            
            response = f"""{celebration}

The word was indeed '{self.current_word}'! 

📊 Score: {self.score} correct words!

{next_word_message}"""

            if self.ai_assistant:
                self.ai_assistant.speak(f"{celebration} The word was {self.current_word}! Your score is {self.score}. {next_word_message}", user)
            
            return response
        
        else:
            self.attempts += 1
            
            if self.attempts >= self.max_attempts:
                # Reveal the answer and move to next word
                encouragement = random.choice(self.encouragement_messages)
                next_word_message = self._prepare_next_word()
                
                response = f"""{encouragement} '{self.current_word}'

{next_word_message}"""

                if self.ai_assistant:
                    self.ai_assistant.speak(f"{encouragement} {self.current_word}. {next_word_message}", user)
                
                return response
            
            else:
                remaining_attempts = self.max_attempts - self.attempts
                hint_response = f"""🤔 That's not quite right! You guessed '{clean_answer}'

The word I'm thinking of starts with '{self.current_letter}' and: {self.current_hint}

You have {remaining_attempts} more attempt{'s' if remaining_attempts > 1 else ''}. Try again!"""

                if self.ai_assistant:
                    self.ai_assistant.speak(f"Not quite right! Try again. {self.current_hint}. You have {remaining_attempts} more tries.", user)
                
                return hint_response
    
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
            'APPLE': "Think of what teachers get as gifts, or what keeps doctors away!",
            'RABBIT': "This animal is famous for being in magic tricks and eating garden vegetables!",
            'BUTTERFLY': "It starts as a caterpillar and becomes something beautiful that can fly!",
            'ELEPHANT': "This animal never forgets and is afraid of tiny mice!",
            'PENGUIN': "This bird looks like it's wearing a tuxedo and lives where it's very cold!",
            'RAINBOW': "You can see this after rain, and it has all the colors you can think of!",
            'DINOSAUR': "These huge creatures lived long, long ago before any people existed!",
            'CASTLE': "Knights and princesses lived in these tall, stone buildings!",
            'GIRAFFE': "This animal can eat leaves from the very top of tall trees!",
            'VOLCANO': "This mountain can explode with hot, melted rock!"
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
            self.ai_assistant.speak(f"Okay, we'll skip that one. The word was {skipped_word}. {next_word_message}", user)
        
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