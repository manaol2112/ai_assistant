#!/usr/bin/env python3
"""
Filipino Translation Game for Kids
Educational module for learning Filipino language through English-Filipino translation
"""

import logging
import random
import difflib
from typing import Dict, List, Optional
import pygame
import numpy as np

logger = logging.getLogger(__name__)

class FilipinoTranslator:
    def __init__(self, openai_client, ai_assistant=None):
        """Initialize the Filipino translator with OpenAI client and AI assistant reference."""
        self.client = openai_client
        self.ai_assistant = ai_assistant  # Reference to main AI assistant for speak_no_interrupt
        self.game_active = False
        self.current_translation = None
        
        # Initialize pygame mixer for sound effects
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Generate sound effects
        self.correct_sound = self._generate_applause_sound()
        self.wrong_sound = self._generate_buzzer_sound()
        
        # Expanded Filipino vocabulary for advanced learning
        self.basic_vocabulary = {
            # Family & Relationships
            "mother": "nanay",
            "father": "tatay", 
            "sister": "ate",
            "brother": "kuya",
            "grandmother": "lola",
            "grandfather": "lolo",
            "family": "pamilya",
            "baby": "sanggol",
            "cousin": "pinsan",
            "aunt": "tita",
            "uncle": "tito",
            "daughter": "anak na babae",
            "son": "anak na lalaki",
            "wife": "asawa",
            "husband": "asawa",
            "neighbor": "kapitbahay",
            
            # Daily Life & Actions
            "hello": "kumusta",
            "goodbye": "paalam",
            "thank you": "salamat",
            "please": "pakisuyo",
            "sorry": "pasensya",
            "yes": "oo",
            "no": "hindi",
            "maybe": "siguro",
            "always": "lagi",
            "never": "hindi kailanman",
            "sometimes": "minsan",
            "today": "ngayon",
            "tomorrow": "bukas",
            "yesterday": "kahapon",
            "morning": "umaga",
            "afternoon": "hapon",
            "evening": "gabi",
            "night": "gabi",
            "work": "trabaho",
            "study": "mag-aral",
            "sleep": "tulog",
            "eat": "kain",
            "drink": "inom",
            "play": "laro",
            "read": "basa",
            "write": "sulat",
            "listen": "pakinggan",
            "speak": "magsalita",
            "walk": "lakad",
            "run": "takbo",
            "swim": "langoy",
            "dance": "sayaw",
            "sing": "kanta",
            "cook": "luto",
            "clean": "linis",
            "wash": "huggas",
            "buy": "bili",
            "sell": "tinda",
            "give": "bigay",
            "take": "kuha",
            "help": "tulong",
            "wait": "hintay",
            "come": "halika",
            "go": "alis",
            "stay": "dito",
            "sit": "upo",
            "stand": "tayo",
            "open": "bukas",
            "close": "sara",
            
            # Food & Drinks
            "water": "tubig",
            "food": "pagkain",
            "rice": "kanin",
            "bread": "tinapay",
            "meat": "karne",
            "fish": "isda",
            "chicken": "manok",
            "pork": "baboy",
            "beef": "baka",
            "vegetables": "gulay",
            "fruit": "prutas",
            "milk": "gatas",
            "coffee": "kape",
            "tea": "tsaa",
            "juice": "juice",
            "sugar": "asukal",
            "salt": "asin",
            "pepper": "paminta",
            "egg": "itlog",
            "noodles": "pansit",
            "soup": "sabaw",
            "cake": "cake",
            "candy": "kendi",
            "ice cream": "sorbetes",
            
            # Places & Locations
            "house": "bahay",
            "school": "paaralan",
            "hospital": "ospital",
            "church": "simbahan",
            "market": "palengke",
            "store": "tindahan",
            "restaurant": "restaurant",
            "park": "parke",
            "beach": "dalampasigan",
            "mountain": "bundok",
            "river": "ilog",
            "road": "daan",
            "street": "kalye",
            "bridge": "tulay",
            "building": "gusali",
            "office": "opisina",
            "mall": "mall",
            "airport": "paliparan",
            "farm": "bukid",
            "garden": "hardin",
            "bathroom": "banyo",
            "kitchen": "kusina",
            "bedroom": "silid-tulugan",
            "living room": "sala",
            
            # Transportation
            "car": "kotse",
            "bus": "bus",
            "jeep": "dyip",
            "tricycle": "traysikel",
            "motorcycle": "motor",
            "bicycle": "bisikleta",
            "boat": "bangka",
            "airplane": "eroplano",
            "train": "tren",
            "taxi": "taxi",
            
            # Weather & Nature
            "sun": "araw",
            "moon": "buwan",
            "star": "bituin",
            "rain": "ulan",
            "wind": "hangin",
            "cloud": "ulap",
            "thunder": "kulog",
            "lightning": "kidlat",
            "storm": "bagyo",
            "hot": "mainit",
            "cold": "malamig",
            "warm": "mainit-init",
            "cool": "malamig-lamig",
            "wet": "basa",
            "dry": "tuyo",
            "tree": "puno",
            "flower": "bulaklak",
            "grass": "damo",
            "stone": "bato",
            "sand": "buhangin",
            "water": "tubig",
            "fire": "apoy",
            "earth": "lupa",
            "sky": "langit",
            
            # Emotions & Feelings
            "love": "mahal",
            "like": "gusto",
            "hate": "galit",
            "angry": "galit",
            "happy": "masaya",
            "sad": "malungkot",
            "excited": "nasasabik",
            "worried": "nag-aalala",
            "scared": "takot",
            "brave": "matapang",
            "proud": "proud",
            "jealous": "nagseselos",
            "tired": "pagod",
            "hungry": "gutom",
            "thirsty": "uhaw",
            "sleepy": "antok",
            "awake": "gising",
            "sick": "may sakit",
            "healthy": "malusog",
            "strong": "malakas",
            "weak": "mahina",
            
            # Descriptions & Qualities
            "beautiful": "maganda",
            "ugly": "pangit",
            "good": "mabuti",
            "bad": "masama",
            "big": "malaki",
            "small": "maliit",
            "tall": "matangkad",
            "short": "maikli",
            "fat": "mataba",
            "thin": "payat",
            "old": "matanda",
            "young": "bata",
            "new": "bago",
            "clean": "malinis",
            "dirty": "marumi",
            "fast": "mabilis",
            "slow": "mabagal",
            "loud": "malakas",
            "quiet": "tahimik",
            "easy": "madali",
            "difficult": "mahirap",
            "rich": "mayaman",
            "poor": "mahirap",
            "smart": "matalino",
            "stupid": "tanga",
            "kind": "mabait",
            "mean": "masama",
            "funny": "nakakatawa",
            "serious": "seryoso",
            
            # Colors (expanded)
            "red": "pula",
            "blue": "asul",
            "green": "berde",
            "yellow": "dilaw",
            "black": "itim",
            "white": "puti",
            "brown": "kayumanggi",
            "orange": "orange",
            "purple": "lila",
            "pink": "rosas",
            "gray": "kulay-abo",
            "gold": "ginto",
            "silver": "pilak",
            
            # Numbers (expanded)
            "one": "isa",
            "two": "dalawa",
            "three": "tatlo",
            "four": "apat",
            "five": "lima",
            "six": "anim",
            "seven": "pito",
            "eight": "walo",
            "nine": "siyam",
            "ten": "sampu",
            "eleven": "labing-isa",
            "twelve": "labindalawa",
            "thirteen": "labintatlo",
            "fourteen": "labing-apat",
            "fifteen": "labinlima",
            "twenty": "dalawampu",
            "thirty": "tatlumpu",
            "forty": "apatnapu",
            "fifty": "limampu",
            "hundred": "daan",
            "thousand": "libo",
            
            # Animals (expanded)
            "dog": "aso",
            "cat": "pusa",
            "bird": "ibon",
            "fish": "isda",
            "horse": "kabayo",
            "cow": "baka",
            "chicken": "manok",
            "pig": "baboy",
            "goat": "kambing",
            "duck": "pato",
            "rabbit": "kuneho",
            "mouse": "daga",
            "snake": "ahas",
            "lizard": "butiki",
            "frog": "palaka",
            "butterfly": "paru-paro",
            "bee": "bubuyog",
            "ant": "langgam",
            "spider": "gagamba",
            "monkey": "unggoy",
            "tiger": "tigre",
            "lion": "leon",
            "elephant": "elepante",
            
            # Body Parts (expanded)
            "head": "ulo",
            "hair": "buhok",
            "eyes": "mata",
            "nose": "ilong",
            "mouth": "bibig",
            "teeth": "ngipin",
            "tongue": "dila",
            "ear": "tenga",
            "neck": "leeg",
            "shoulder": "balikat",
            "arm": "braso",
            "hand": "kamay",
            "finger": "daliri",
            "chest": "dibdib",
            "stomach": "tiyan",
            "back": "likod",
            "leg": "binti",
            "knee": "tuhod",
            "foot": "paa",
            "toe": "daliri ng paa",
            "skin": "balat",
            "bone": "buto",
            "blood": "dugo",
            "heart": "puso",
            
            # School & Learning
            "teacher": "guro",
            "student": "estudyante",
            "book": "libro",
            "pen": "bolpen",
            "pencil": "lapis",
            "paper": "papel",
            "desk": "mesa",
            "chair": "upuan",
            "blackboard": "pisara",
            "lesson": "aralin",
            "homework": "takdang-aralin",
            "exam": "pagsusulit",
            "grade": "marka",
            "learn": "matuto",
            "understand": "intindi",
            "remember": "tandaan",
            "forget": "kalimutan",
            "answer": "sagot",
            "question": "tanong",
            "problem": "problema",
            "solution": "solusyon",
            
            # Time & Days
            "time": "oras",
            "hour": "oras",
            "minute": "minuto",
            "second": "segundo",
            "day": "araw",
            "week": "linggo",
            "month": "buwan",
            "year": "taon",
            "monday": "lunes",
            "tuesday": "martes",
            "wednesday": "miyerkules",
            "thursday": "huwebes",
            "friday": "biyernes",
            "saturday": "sabado",
            "sunday": "linggo",
            "birthday": "kaarawan",
            "holiday": "pista",
            "vacation": "bakasyon",
            
            # Money & Shopping
            "money": "pera",
            "peso": "piso",
            "centavo": "sentimo",
            "price": "presyo",
            "expensive": "mahal",
            "cheap": "mura",
            "free": "libre",
            "discount": "diskwento",
            "receipt": "resibo",
            "change": "sukli",
            "cash": "cash",
            "credit card": "credit card",
            
            # Technology & Modern Life
            "phone": "telepono",
            "computer": "computer",
            "internet": "internet",
            "television": "telebisyon",
            "radio": "radyo",
            "camera": "camera",
            "video": "video",
            "picture": "larawan",
            "music": "musika",
            "movie": "pelikula",
            "game": "laro",
            "toy": "laruan",
            "gift": "regalo",
            "party": "party",
            "celebration": "pagdiriwang"
        }

        # Alternative pronunciations that speech recognition might capture (expanded)
        self.pronunciation_alternatives = {
            # Family & Relationships
            "nanay": ["nana", "nanai", "nanny"],
            "tatay": ["tata", "tatai", "daddy"],
            "ate": ["ah-te", "ati", "ahtay"],
            "kuya": ["koo-ya", "cooya", "koya"],
            "lola": ["loh-la", "lohla", "lula"],
            "lolo": ["loh-lo", "lohlo", "lulo"],
            "pamilya": ["familia", "pamiliya", "family"],
            "sanggol": ["sang-gol", "sanggul", "sango"],
            "pinsan": ["peen-san", "pensan", "pinson"],
            "tita": ["tee-ta", "teeta", "teta"],
            "tito": ["tee-to", "teeto", "teto"],
            "kapitbahay": ["kapitbahy", "kapetbahay", "kapitbai"],
            
            # Daily Life & Actions
            "kumusta": ["como esta", "kumosta", "comosta"],
            "paalam": ["pa-alam", "palam", "palahm"],
            "salamat": ["salamut", "salmat", "salamat"],
            "pakisuyo": ["packy", "pucky", "pocky"],
            "pasensya": ["pasencia", "pasensiya", "pasencia"],
            "oo": ["oh", "ooh", "uh"],
            "hindi": ["hindy", "hinde", "hendy"],
            "siguro": ["seguro", "sigoro", "shiguro"],
            "lagi": ["lah-gee", "lagee", "lagy"],
            "minsan": ["min-san", "minsahn", "mensan"],
            "ngayon": ["nga-yon", "ngayun", "ngayown"],
            "bukas": ["boo-kas", "bookas", "bucas"],
            "kahapon": ["ka-hapon", "kahapon", "cahapon"],
            "umaga": ["oo-maga", "oomaga", "umahga"],
            "hapon": ["ha-pon", "hapon", "hapoon"],
            "gabi": ["ga-bee", "gabee", "gaby"],
            "trabaho": ["tra-baho", "trabajo", "trabaju"],
            "mag-aral": ["mag-arel", "magaral", "magarel"],
            "tulog": ["too-log", "toolug", "tolug"],
            "kain": ["ka-in", "kine", "kayn"],
            "inom": ["ee-nom", "inom", "enom"],
            "laro": ["la-ro", "laro", "lahro"],
            "basa": ["ba-sa", "basha", "basa"],
            "sulat": ["soo-lat", "soolat", "sulate"],
            "pakinggan": ["pa-kingan", "pakingan", "pakengan"],
            "magsalita": ["mag-salita", "magsaleeta", "magsaleata"],
            "lakad": ["la-kad", "lakahd", "lacad"],
            "takbo": ["tak-bo", "tackbo", "takbu"],
            "langoy": ["lan-goy", "langoy", "languy"],
            "sayaw": ["sa-yaw", "sayow", "sayaow"],
            "kanta": ["kan-ta", "canta", "kantah"],
            "luto": ["loo-to", "looto", "luto"],
            "linis": ["lee-nis", "leenis", "lenees"],
            "huggas": ["hug-gas", "hugaas", "huggas"],
            "bili": ["bee-lee", "beeli", "belly"],
            "tinda": ["teen-da", "teenda", "tenda"],
            "bigay": ["bee-gay", "beegay", "begay"],
            "kuha": ["koo-ha", "kooha", "cuha"],
            "tulong": ["too-long", "toolong", "tulung"],
            "hintay": ["hin-tay", "hentay", "hintai"],
            "halika": ["ha-lika", "halica", "haleyca"],
            "alis": ["ah-lis", "ales", "ahles"],
            "dito": ["dee-to", "deeto", "deto"],
            "upo": ["oo-po", "oopu", "upu"],
            "tayo": ["ta-yo", "taiyo", "tayoo"],
            "bukas": ["boo-kas", "bookas", "bucas"],
            "sara": ["sa-ra", "sarah", "sarra"],
            
            # Food & Drinks
            "tubig": ["tubeg", "toobig", "tube"],
            "pagkain": ["pagkaen", "pugkain", "pagkan"],
            "kanin": ["canin", "kaneen", "conin"],
            "tinapay": ["teena-pay", "teenapay", "tenapay"],
            "karne": ["car-ne", "carney", "carni"],
            "isda": ["ees-da", "isda", "esda"],
            "manok": ["ma-nok", "manock", "maknok"],
            "baboy": ["ba-boy", "babuoy", "babuy"],
            "baka": ["ba-ka", "baca", "backa"],
            "gulay": ["goo-lay", "goolay", "gulai"],
            "prutas": ["proo-tas", "prootas", "frutas"],
            "gatas": ["ga-tas", "gatahs", "gatash"],
            "kape": ["ka-pe", "capay", "capy"],
            "tsaa": ["cha", "chah", "tsa"],
            "asukal": ["a-sookal", "asoocar", "azucar"],
            "asin": ["ah-seen", "ahseen", "aseen"],
            "paminta": ["pa-minta", "pamenta", "pameenta"],
            "itlog": ["eet-log", "eetlog", "etlog"],
            "pansit": ["pan-sit", "panseet", "pansyt"],
            "sabaw": ["sa-baw", "sabao", "sabow"],
            "kendi": ["ken-dee", "kendee", "candy"],
            "sorbetes": ["sor-betes", "sorbetis", "sorbetes"],
            
            # Places & Locations
            "bahay": ["ba-hi", "bahey", "bahai"],
            "paaralan": ["paralan", "pa-aralan", "pahralan"],
            "ospital": ["os-pital", "hospital", "ospetal"],
            "simbahan": ["sim-bahan", "simbahahn", "sembahan"],
            "palengke": ["pa-lengke", "palengkey", "palenke"],
            "tindahan": ["teen-dahan", "teendahan", "tendahan"],
            "dalampasigan": ["dalampaseegan", "dalampaseejan", "dalampasigang"],
            "bundok": ["boon-dok", "boondok", "bunduc"],
            "ilog": ["ee-log", "eelog", "elog"],
            "daan": ["da-an", "dahan", "dan"],
            "kalye": ["kal-ye", "calye", "kalyeh"],
            "tulay": ["too-lay", "toolay", "tolai"],
            "gusali": ["goo-sali", "goosali", "gusale"],
            "opisina": ["o-pisina", "opiseena", "ofisina"],
            "paliparan": ["pa-liparan", "paleeparan", "paleparahn"],
            "bukid": ["boo-kid", "bookeed", "buked"],
            "hardin": ["har-din", "hardeen", "jardeen"],
            "banyo": ["ban-yo", "banyoo", "baniyo"],
            "kusina": ["koo-sina", "kooseena", "cuseena"],
            "silid-tulugan": ["seleed-toolugan", "silid-toologan", "siled-tulugan"],
            "sala": ["sa-la", "salah", "salaa"],
            
            # Transportation
            "kotse": ["kot-se", "cotse", "kotsee"],
            "dyip": ["jeep", "dyeep", "jip"],
            "traysikel": ["tricycle", "traysekel", "treysikel"],
            "motor": ["mo-tor", "motoor", "mutor"],
            "bisikleta": ["biseekleta", "bicycle", "biseecleta"],
            "bangka": ["bang-ka", "bangcah", "banka"],
            "eroplano": ["airplane", "eroplanu", "ayroplano"],
            "tren": ["train", "treyn", "trene"],
            
            # Weather & Nature
            "araw": ["ah-raw", "ahraw", "arow"],
            "buwan": ["boo-wan", "boowan", "buoan"],
            "bituin": ["bee-tuin", "beetoin", "beetoyen"],
            "ulan": ["oo-lan", "oolan", "ulahn"],
            "hangin": ["hang-gin", "hanggeen", "hanjen"],
            "ulap": ["oo-lap", "oolap", "ulaph"],
            "kulog": ["koo-log", "koolog", "culog"],
            "kidlat": ["keed-lat", "keedlat", "kidlaht"],
            "bagyo": ["bag-yo", "bagyoo", "bajiyo"],
            "mainit": ["my-neet", "myneet", "mayneet"],
            "malamig": ["ma-lamig", "ma-lamig", "malameeg"],
            "basa": ["ba-sa", "basha", "basah"],
            "tuyo": ["too-yo", "tooyo", "tuyoo"],
            "puno": ["poo-no", "poono", "punoo"],
            "bulaklak": ["boolak-lak", "boolaklahk", "bulaclac"],
            "damo": ["da-mo", "damu", "dahmo"],
            "bato": ["ba-to", "bahto", "batoo"],
            "buhangin": ["boo-hangin", "boohanggeen", "buhangeen"],
            "apoy": ["ah-poy", "ahpuy", "apuy"],
            "lupa": ["loo-pa", "loopa", "lupah"],
            "langit": ["lang-git", "langgeet", "langeet"],
            
            # Emotions & Feelings
            "mahal": ["ma-hal", "mahaal", "mahal"],
            "gusto": ["goos-to", "goosto", "gustu"],
            "galit": ["ga-leet", "galeet", "galyt"],
            "masaya": ["ma-saya", "masayah", "masya"],
            "malungkot": ["malungkut", "ma-lungkot", "malungkut"],
            "nasasabik": ["na-sasabik", "nasasabeek", "nasasabyk"],
            "nag-aalala": ["nag-alala", "nagaalala", "nag-ahlala"],
            "takot": ["ta-kot", "tacot", "takut"],
            "matapang": ["ma-tapang", "matapaang", "matapahng"],
            "nagseselos": ["nag-selos", "nagselos", "nagseselus"],
            "pagod": ["pa-god", "pagud", "pahgod"],
            "gutom": ["goo-tom", "gootom", "gutum"],
            "uhaw": ["oo-haw", "oohaw", "uhao"],
            "antok": ["an-tok", "antuk", "ahtok"],
            "gising": ["gee-sing", "geesing", "jesing"],
            "malusog": ["ma-lusog", "malusug", "malosog"],
            "malakas": ["ma-lakas", "malacas", "malahkas"],
            "mahina": ["ma-hina", "maheena", "mahyna"]
        }

    def start_filipino_game(self, user: str) -> str:
        """Start the Filipino translation game."""
        try:
            self.game_active = True
            self.current_translation = None
            
            if user == 'sophia':
                intro = "🇵🇭 Filipino Game Started! I'll say English, you say Filipino!"
            elif user == 'eladriel':
                intro = "🦕🇵🇭 Filipino Game! English to Filipino translation time!"
            else:
                intro = "Filipino Translation Game - English to Filipino"
            
            # Start with first question immediately
            question = self.get_random_question(user)
            return intro + "\n\n" + question
            
        except Exception as e:
            logger.error(f"Error starting Filipino game: {e}")
            return "Error starting game. Try again!"

    def get_random_question(self, user: str) -> str:
        """Get a random translation question."""
        try:
            english_word = random.choice(list(self.basic_vocabulary.keys()))
            filipino_translation = self.basic_vocabulary[english_word]
            
            self.current_translation = {
                'english': english_word,
                'filipino': filipino_translation
            }
            
            question_text = f"How do you say '{english_word}' in Filipino?"
            
            return question_text
            
        except Exception as e:
            logger.error(f"Error getting question: {e}")
            return "Error getting question. Try again!"

    def check_translation_answer(self, user_answer: str, user: str) -> str:
        """Check the user's translation answer with flexible matching for speech recognition."""
        try:
            if not self.current_translation:
                return "No active question. Say 'Filipino game' to start!"
            
            correct_filipino = self.current_translation['filipino'].lower()
            user_answer_lower = user_answer.lower().strip()
            english_word = self.current_translation['english']
            
            # Check if answer is correct (exact match or alternative pronunciation)
            is_correct = False
            
            # 1. Exact match
            if user_answer_lower == correct_filipino:
                is_correct = True
            
            # 2. Check alternative pronunciations
            elif correct_filipino in self.pronunciation_alternatives:
                alternatives = self.pronunciation_alternatives[correct_filipino]
                if any(alt.lower() == user_answer_lower for alt in alternatives):
                    is_correct = True
            
            # 3. Fuzzy matching for close pronunciations
            elif self._is_close_pronunciation(user_answer_lower, correct_filipino):
                is_correct = True
            
            # Clear current question first
            self.current_translation = None
            
            if is_correct:
                # Correct!
                self.play_correct_sound()
                feedback = f"✅ Excellent! {english_word} is {correct_filipino}."
                result = feedback + "\n\n"
            else:
                # Wrong - provide pronunciation help
                pronunciation = self.get_pronunciation_help(english_word, correct_filipino)
                self.play_wrong_sound()
                feedback = f"Close try! {english_word} is {correct_filipino}. {pronunciation}"
                result = feedback + "\n\n"
            
            # Add next question immediately
            result += self.get_random_question(user)
            return result
            
        except Exception as e:
            logger.error(f"Error checking answer: {e}")
            return "Error checking answer. Try again!"

    def _is_close_pronunciation(self, user_answer: str, correct_answer: str) -> bool:
        """Check if the user's answer is phonetically close to the correct answer."""
        # Remove common speech recognition artifacts
        user_clean = user_answer.replace('-', '').replace(' ', '').lower()
        correct_clean = correct_answer.replace('-', '').replace(' ', '').lower()
        
        # Check if user answer is contained in correct answer or vice versa
        if len(user_clean) >= 3:
            if user_clean in correct_clean or correct_clean in user_clean:
                return True
        
        # Check similar length and overlapping characters
        if abs(len(user_clean) - len(correct_clean)) <= 2:
            # Count matching characters in similar positions
            matches = 0
            min_len = min(len(user_clean), len(correct_clean))
            for i in range(min_len):
                if i < len(user_clean) and i < len(correct_clean):
                    if user_clean[i] == correct_clean[i]:
                        matches += 1
            
            # If more than 60% of characters match, consider it close
            if min_len > 0 and matches / min_len >= 0.6:
                return True
        
        return False

    def get_pronunciation_help(self, english_word: str, filipino_word: str) -> str:
        """Get pronunciation help for Filipino words."""
        pronunciation_tips = {
            "nanay": "Say 'NAH-nigh' (like 'nah' + 'night' without the 't')",
            "tatay": "Say 'TAH-tigh' (like 'ta' + 'tie')", 
            "ate": "Say 'AH-teh' (like 'ah' + 'teh')",
            "kuya": "Say 'KOO-yah' (like 'cool' + 'ya')",
            "lola": "Say 'LOH-lah' (like 'low' + 'la')",
            "lolo": "Say 'LOH-loh' (like 'low' + 'low')",
            "pamilya": "Say 'pah-MEEL-yah' (pa-mil-ya)",
            "sanggol": "Say 'sahng-GOHL' (sang-gol)",
            "kumusta": "Say 'koo-MOOS-tah' (like 'cool moose' + 'ta')",
            "paalam": "Say 'pah-ah-LAHM' (like 'pa' + 'alarm' without 'r')",
            "salamat": "Say 'sah-lah-MAHT' (like 'sala' + 'mat')",
            "pakisuyo": "Say 'PAH-kee' (like 'pa' + 'key')",
            "oo": "Say 'OH-oh' (like saying 'oh' twice)",
            "hindi": "Say 'hin-DEE' (like 'hind' + 'dee')",
            "tubig": "Say 'TOO-big' (like 'tube' + 'big')",
            "pagkain": "Say 'pahg-kah-EEN' (like 'pug' + 'car' + 'een')",
            "kanin": "Say 'kah-NEEN' (like 'car' + 'neen')",
            "bahay": "Say 'BAH-high' (like 'ba' + 'hi')",
            "paaralan": "Say 'pah-ah-rah-LAHN' (pa-a-ra-lan)",
            "kaibigan": "Say 'kah-ee-bee-GAHN' (kai-bi-gan)",
            "mahal": "Say 'mah-HAHL' (like 'ma' + 'hall')",
            "maganda": "Say 'mah-gan-DAH' (like 'ma' + 'ganda')",
            "mabuti": "Say 'mah-boo-TEE' (ma-bu-ti)",
            "malaki": "Say 'mah-lah-KEE' (ma-la-ki)",
            "maliit": "Say 'mah-lee-EET' (ma-li-it)",
            "masaya": "Say 'mah-sah-YAH' (like 'ma' + 'saya')",
            "malungkot": "Say 'mah-loong-KOHT' (ma-lung-kot)",
            "pula": "Say 'POO-lah' (like 'pool' + 'ah')",
            "asul": "Say 'AH-sool' (like 'ah' + 'school' without 'ch')",
            "berde": "Say 'BER-deh' (like 'bear' + 'deh')",
            "dilaw": "Say 'dee-LAHW' (di-law)",
            "itim": "Say 'EE-tim' (i-tim)",
            "puti": "Say 'POO-tee' (pu-ti)",
            "isa": "Say 'EE-sah' (like 'easy' without 'zy')",
            "dalawa": "Say 'dah-lah-WAH' (like 'da' + 'lava')",
            "tatlo": "Say 'TAHT-loh' (tat-lo)",
            "apat": "Say 'AH-paht' (a-pat)",
            "lima": "Say 'LEE-mah' (li-ma)",
            "anim": "Say 'AH-nim' (a-nim)",
            "pito": "Say 'PEE-toh' (pi-to)",
            "walo": "Say 'WAH-loh' (wa-lo)",
            "siyam": "Say 'SEE-yahm' (si-yam)",
            "sampu": "Say 'sahm-POO' (sam-pu)",
            "aso": "Say 'AH-so' (like 'ah' + 'so')",
            "pusa": "Say 'POO-sah' (like 'push' + 'ah')",
            "ibon": "Say 'EE-bohn' (i-bon)",
            "isda": "Say 'ees-DAH' (is-da)",
            "kabayo": "Say 'kah-bah-YOH' (ka-ba-yo)",
            "baka": "Say 'BAH-kah' (ba-ka)",
            "manok": "Say 'mah-NOHK' (ma-nok)",
            "ulo": "Say 'OO-loh' (u-lo)",
            "mata": "Say 'MAH-tah' (ma-ta)",
            "ilong": "Say 'EE-lohng' (i-long)",
            "bibig": "Say 'BEE-big' (bi-big)",
            "kamay": "Say 'kah-MIGH' (ka-may)",
            "paa": "Say 'PAH-ah' (pa-a)"
        }
        
        tip = pronunciation_tips.get(filipino_word, f"Practice saying '{filipino_word}' slowly")
        return f"🗣️ {tip}"

    def end_game(self):
        """End the current Filipino translation game."""
        if not self.game_active:
            return "No active Filipino game."
        
        final_message = "🇵🇭 Game Over! Great job learning Filipino!"
        
        # Reset game state
        self.game_active = False
        self.current_translation = None
        
        return final_message

    def is_filipino_game_command(self, user_input: str) -> bool:
        """Check if the input is related to the Filipino game."""
        filipino_commands = [
            'filipino game', 'learn filipino', 'filipino translation',
            'end filipino game', 'stop filipino'
        ]
        
        user_input_lower = user_input.lower()
        
        # If game is active and there's a current question, treat any input as a potential answer
        if self.game_active and self.current_translation:
            return True
            
        return any(command in user_input_lower for command in filipino_commands)

    def handle_filipino_command(self, user_input: str, user: str) -> str:
        """Handle Filipino game related commands."""
        user_input_lower = user_input.lower()
        
        if any(phrase in user_input_lower for phrase in ['filipino game', 'learn filipino']):
            return self.start_filipino_game(user)
        
        elif any(phrase in user_input_lower for phrase in ['end filipino game', 'stop filipino']):
            return self.end_game()
        
        elif self.game_active and self.current_translation:
            # User is giving an answer to current question
            return self.check_translation_answer(user_input, user)
        
        else:
            return "Say 'Filipino game' to start!"

    def _generate_applause_sound(self):
        """Generate a celebratory victory sound for correct answers."""
        try:
            sample_rate = 22050
            duration = 1.8  # 1.8 seconds
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Create a "Ta-Da!" victory sound with ascending musical notes
            celebration = np.zeros_like(t)
            
            # First part: Rising musical phrase (Ta!)
            first_part_end = 0.6
            first_mask = t <= first_part_end
            
            # Rising chord progression for excitement
            frequencies_rising = [
                (220, 0.0, 0.2),   # A3 
                (277, 0.1, 0.3),   # C#4
                (330, 0.2, 0.4),   # E4
                (440, 0.3, 0.6),   # A4 (climax)
            ]
            
            for freq, start_time, end_time in frequencies_rising:
                note_mask = (t >= start_time) & (t <= end_time)
                if np.any(note_mask):
                    note_t = t[note_mask] - start_time
                    # Create a bell-like tone with harmonics
                    fundamental = np.sin(2 * np.pi * freq * note_t)
                    harmonic2 = 0.3 * np.sin(2 * np.pi * freq * 2 * note_t)
                    harmonic3 = 0.1 * np.sin(2 * np.pi * freq * 3 * note_t)
                    
                    # Bell envelope - quick attack, gradual decay
                    envelope = np.exp(-note_t * 4) * (1 - np.exp(-note_t * 50))
                    
                    note = (fundamental + harmonic2 + harmonic3) * envelope
                    celebration[note_mask] += note * 0.4
            
            # Second part: Sparkle effect (Da!)
            sparkle_start = 0.5
            sparkle_end = 1.8
            sparkle_mask = (t >= sparkle_start) & (t <= sparkle_end)
            
            if np.any(sparkle_mask):
                sparkle_t = t[sparkle_mask] - sparkle_start
                
                # Add magical sparkle with high frequency components
                sparkle_freqs = [880, 1108, 1397, 1760, 2217]  # High harmonious frequencies
                
                for i, freq in enumerate(sparkle_freqs):
                    delay = i * 0.08  # Staggered sparkles
                    if len(sparkle_t) > int(delay * sample_rate):
                        delayed_t = sparkle_t[int(delay * sample_rate):]
                        if len(delayed_t) > 0:
                            # Create shimmering effect
                            shimmer = np.sin(2 * np.pi * freq * delayed_t)
                            shimmer *= np.exp(-delayed_t * 2)  # Decay
                            shimmer *= (1 + 0.5 * np.sin(10 * delayed_t))  # Tremolo effect
                            
                            # Add to the celebration sound
                            start_idx = int((sparkle_start + delay) * sample_rate)
                            end_idx = start_idx + len(shimmer)
                            if end_idx <= len(celebration):
                                celebration[start_idx:end_idx] += shimmer * 0.15
            
            # Third part: Final triumphant chord
            final_start = 1.2
            final_mask = t >= final_start
            
            if np.any(final_mask):
                final_t = t[final_mask] - final_start
                
                # Major chord for triumphant ending
                chord_freqs = [440, 554, 659]  # A major chord
                for freq in chord_freqs:
                    chord_note = np.sin(2 * np.pi * freq * final_t)
                    chord_envelope = np.exp(-final_t * 1.5) * 0.6
                    celebration[final_mask] += chord_note * chord_envelope * 0.3
            
            # Add some gentle reverb effect
            reverb_delay = int(0.05 * sample_rate)  # 50ms delay
            if len(celebration) > reverb_delay:
                reverb = np.zeros_like(celebration)
                reverb[reverb_delay:] = celebration[:-reverb_delay] * 0.2
                celebration += reverb
            
            # Apply overall envelope for natural sound
            overall_envelope = np.ones_like(t)
            # Gentle fade out at the end
            fade_start = 1.5
            fade_mask = t >= fade_start
            if np.any(fade_mask):
                fade_t = (t[fade_mask] - fade_start) / (duration - fade_start)
                overall_envelope[fade_mask] = 1 - fade_t
            
            celebration *= overall_envelope
            
            # Normalize and convert to pygame sound format
            celebration = np.clip(celebration, -1, 1)
            celebration = (celebration * 32767 * 0.7).astype(np.int16)  # Good volume level
            
            # Create stereo sound
            stereo_sound = np.zeros((len(celebration), 2), dtype=np.int16)
            stereo_sound[:, 0] = celebration  # Left channel
            stereo_sound[:, 1] = celebration  # Right channel
            
            return pygame.sndarray.make_sound(stereo_sound)
        except Exception as e:
            logger.error(f"Error generating celebration sound: {e}")
            return None

    def _generate_buzzer_sound(self):
        """Generate a buzzer sound for wrong answers."""
        try:
            sample_rate = 22050
            duration = 0.8  # 0.8 seconds
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            # Create buzzer sound with low frequency
            frequency = 150  # Low buzzer frequency
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Add some harmonics to make it sound more like a buzzer
            wave += 0.5 * np.sin(2 * np.pi * frequency * 2 * t)  # Octave
            wave += 0.3 * np.sin(2 * np.pi * frequency * 3 * t)  # Fifth
            
            # Apply envelope for natural sound decay
            envelope = np.exp(-t * 1.5)
            buzzer = wave * envelope
            
            # Normalize and convert to pygame sound format
            buzzer = np.clip(buzzer, -1, 1)
            buzzer = (buzzer * 32767).astype(np.int16)
            
            # Create stereo sound
            stereo_sound = np.zeros((len(buzzer), 2), dtype=np.int16)
            stereo_sound[:, 0] = buzzer  # Left channel
            stereo_sound[:, 1] = buzzer  # Right channel
            
            return pygame.sndarray.make_sound(stereo_sound)
        except Exception as e:
            logger.error(f"Error generating buzzer sound: {e}")
            return None

    def play_correct_sound(self):
        """Play applause sound for correct answers."""
        try:
            if self.correct_sound and hasattr(self.ai_assistant, 'audio_feedback_enabled') and self.ai_assistant.audio_feedback_enabled:
                self.correct_sound.play()
        except Exception as e:
            logger.error(f"Error playing correct sound: {e}")

    def play_wrong_sound(self):
        """Play buzzer sound for wrong answers."""
        try:
            if self.wrong_sound and hasattr(self.ai_assistant, 'audio_feedback_enabled') and self.ai_assistant.audio_feedback_enabled:
                self.wrong_sound.play()
        except Exception as e:
            logger.error(f"Error playing wrong sound: {e}") 