import random


class Card:
    """
    Represents an instantiated card with its rolled stats.
    """
    def __init__(self, name, rarity, art, description, health, attack, armor, barrier, value):
        self.normal_frame = {"top": "┏━━━━━━━━━┓", "mid": "┃{0}┃", "bottom": "┗━━━━━━━━━┛"}
        self.holo_frame = {"top": "┏━★★★★★━┓", "mid": "┃{0}┃", "bottom": "┗━★★★★★━┛"}
        self.name = name
        self.rarity = rarity
        self.art = art
        self.frame = False
        self.is_holo = False
        self.cannot_be_sold = False
        self.description = description
        self.health = health
        self.attack = attack
        self.armor = armor
        self.barrier = barrier
        self.value = value
        self.in_deck = 0
        self.set_frame(self.normal_frame)

    def display(self):
        """
        Prints the card's ASCII art and stats.
        """
        print(f"\n--- {self.name} ({self.rarity.capitalize()}) ---")
        for line in self.get_display_art():
            print(line)
        print(f"Description: {self.description}")
        print(f"Health  : {self.health}")
        print(f"Attack  : {self.attack}")
        print(f"Armor   : {self.armor}")
        print(f"Barrier : {self.barrier}")
        print(f"Value   : {self.value}")
        print("--------------------------")

    def set_frame(self, frame):
        self.frame = frame

    def set_holo(self, is_holo):
        self.is_holo = is_holo

    def get_display_art(self):
        """Returns the card's art formatted with its frame"""
        if not self.frame:
            return self.art
            
        display = []
        display.append(self.frame["top"])
        for line in self.art.values():
            display.append(f'{self.frame["mid"].format(line)}')
        display.append(self.frame["bottom"])
        return display

    def __str__(self):
        return f"{self.name} ({self.rarity})"

    def __repr__(self):
        return f"Card(name='{self.name}', rarity='{self.rarity}')"


class CardDeck:
    """
    Represents a collection of Card objects.
    """
    def __init__(self, cards=None):
        self.cards = []
        if cards:
            self.cards.extend(cards)

    def add_card(self, card):
        """Adds a single Card object to the deck."""
        if isinstance(card, Card):
            self.cards.append(card)
        else:
            print(f"Warning: Attempted to add non-Card object to deck: {type(card)}")

    def add_cards(self, card_list):
        """Adds a list of Card objects to the deck."""
        for card in card_list:
            self.add_card(card)

    def get_total_value(self):
        """Calculates the sum of values of all cards in the deck."""
        return sum(card.value for card in self.cards)

    def get_average_value(self):
        """Calculates the average value of all cards in the deck."""
        if not self.cards:
            return 0
        return self.get_total_value() / len(self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

class CardDatabase:
    def __init__(self):
        self.special_cards = {} # Placeholder for special cards as per original class
        self.card_data_templates = {}
        self._initialize_card_templates()

    def _initialize_card_templates(self):
        """
        Defines the templates for all cards, including their stat generation functions and ASCII art.
        Each stat (health, attack, armor, barrier, value) is now a function that returns a value.
        """
        self.card_data_templates = {
            "common": {
                "Min Min Mangles": {
                    "art": {
                        1: "It don't ",
                        2: "    work ",
                        3: " ,.''.,, ",
                        4: "(  o o  )",
                        5: " | ╯┺╰ | ",
                        6: " \ ╰─╯ / ",
                    },
                    "description": "he tried",
                    "health": lambda: int(random.randint(1,3)),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(1,5),
                },
                "Silver Shekel": {
                    "art": {
                        1: "  .---.  ",
                        2: " /     \ ",
                        3: "|   1   |",
                        4: "|   §   |",
                        5: " \     / ",
                        6: "  '---'  ",
                    },
                    "description": "A common old silver shekel",
                    "health": lambda: int(random.randint(1,2)),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Gold Grabber": {
                    "art": {
                        1: " []  YESS",
                        2: "  \()    ",
                        3: "   ▐▌\   ",
                        4: "  _/\_ []",
                        5: "[]       ",
                        6: " [][] [] ",
                    },
                    "description": "A commoner grabbing up fake gold",
                    "health": lambda: int(random.randint(1,2)),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,15),
                },
                "Treasure Troll": {
                    "art": {
                        1: "  ___  _ ",
                        2: " ($_$/ / ",
                        3: " /| / /  ",
                        4: " \}/ /{> ",
                        5: "  /_/\   ",
                        6: " '    '  ",
                    },
                    "description": "A treasure obsessed troll",
                    "health": lambda: int(random.randint(1,3)),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,8),
                },
                "Coin Collector": {
                    "art": {
                        1: " ()  YESS",
                        2: "  \()    ",
                        3: "   ▐▌\   ",
                        4: "  _/\_ ()",
                        5: "()       ",
                        6: " ()() () ",
                    },
                    "description": "A commoner trying to collect all the coin varieties",
                    "health": lambda: int(random.randint(1,3)),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,8),
                },
                "Wealth Wizard": {
                    "art": {
                        1: "  /\     ",
                        2: "_/  \_   ",
                        3: "(-oᶗo) * ",
                        4: " /$$\╭/  ",
                        5: "/$$$$\   ",
                        6: " |  |    ",
                    },
                    "description": "A wizard who will do magic for pay, disgusting",
                    "health": lambda: int(random.randint(1,1)),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(5,15),
                },
                "Rich Rogue": {
                    "art": {
                        1: "    ,(ssh",
                        2: "   Ậ()   ",
                        3: "<=+/▐▌   ",
                        4: "  _/,|   ",
                        5: "    [ $ ]",
                        6: "$ ][ $ ][",
                    },
                    "description": "A rich rogue trying to get more riches",
                    "health": lambda: int(random.randint(1,2)),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,25),
                },
                "Prosperous Paladin": {
                    "art": {
                        1: " _  ()   ",
                        2: "['\_||.  ",
                        3: "  \_/_|\ ",
                        4: "  //  \  ",
                        5: "         ",
                        6: "         ",
                    },
                    "description": "A paladin who will fight for money",
                    "health": lambda: int(random.randint(2,3)),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,15),
                },
                "Affluent Archer": {
                    "art": {
                        1: "((O))  * ",
                        2: " .  /|() ",
                        3: "  <-(-██'",
                        4: "  * \|/| ",
                        5: " ☼  _/ | ",
                        6: " .  *    ",
                    },
                    "description": "A archer who loves shooting targets for her followers",
                    "health": lambda: 1,
                    "attack": lambda: random.randint(5,6),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Loaded Lancer": {
                    "art": {
                        1: "|        ",
                        2: "|  /\    ",
                        3: "| _ \()  ",
                        4: "|['\_||. ",
                        5: "|  \_/_|\\",
                        6: "|  //  \ ",
                    },
                    "description": "a lancer who has the best equipment but no idea",
                    "health": lambda: random.randint(2,3),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,7),

                },
                "Moneyed Mage": {
                    "art": {
                        1: "  /\    *",
                        2: "_/  \_ / ",
                        3: "(o,o-)/  ",
                        4: "╭/$$\/   ",
                        5: "/$$$/\   ",
                        6: "_| /|    ",
                    },
                    "description": "a rich kid who is pretending to be a mage",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(1,30),
                },
                "Wealthy Warrior": {
                    "art": {
                        1: " ┃       ",
                        2: " ┃  ____ ",
                        3: "╼╂╾(w,w )",
                        4: " ╰_(())| ",
                        5: "    ((() ",
                        6: "   / / \ ",
                    },
                    "description": "a capable warrior",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,30),
                },
                "Fortunate Fighter": {
                    "art": {
                        1: "■╦►      ",
                        2: " ║  /  \ ",
                        3: " ║ (f,f )",
                        4: " ╰_(())| ",
                        5: "    ((() ",
                        6: "   / / \ ",
                    },
                    "description": "lucky fighter who accidentally avoids being hit",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(5,10),
                },
                "Lucky Looter": {
                    "art": {
                        1: "     !!  ",
                        2: "   (l,l )",
                        3: " |  ( (\ ",
                        4: "_| / | | ",
                        5: "$\   / \ ",
                        6: "$$\      ",
                    },
                    "description": "lucky looter who hunts riches",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,20),
                },
                "Blessed Banker": {
                    "art": {
                        1: "|[BANK]| ",
                        2: "|[][][]| ",
                        3: "|[][][]| ",
                        4: "|()[]| | ",
                        5: "/||\--  -",
                        6: "-/\------",
                    },
                    "description": "a banker who has a lot of money",
                    "health": lambda: 1,
                    "attack": lambda: 0,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,50),
                },
                "Divine Depositor": {
                    "art": {
                        1: "| SPERM| ",
                        2: "| BANK | ",
                        3: "|/\[][]| ",
                        4: "|()[]| | ",
                        5: "/||\--  -",
                        6: "-/\------",
                    },
                    "description": "a depositor who has a lot of sperm",
                    "health": lambda: 1,
                    "attack": lambda: 0,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(15,30),
                },
                "Humble Hobbit": {
                    "art": {
                        4: ",_(‟)_o  ",
                        5: "  | |    ",
                        1: "   _/\_  ",
                        2: " | (  )  ",
                        3: " |./  \  ",
                        6: " | '||'  ",
                    },
                    "description": "a humble hobbit",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(1,5),
                },
                "Modest Mage": {
                    "art": {
                        1: "   /\    ",
                        2: " _/  \_ O",
                        3: " (o,o-)/ ",
                        4: " ╭/  \/  ",
                        5: " /   /\  ",
                        6: " _| /|   ",
                    },
                    "description": "a modest mage",
                    "health": lambda: 1,
                    "attack": lambda: random.randint(2,5),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(1,5),
                },
                "Simple Soldier": {
                    "art": {
                        1: "         ",
                        2: "◄█►      ",
                        3: " ┃ (s,s )",
                        4: " ╰_(())| ",
                        5: "    ((() ",
                        6: "   / / \ ",
                    },
                    "description": "a simple soldier",
                    "health": lambda: 2,
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,10),
                },
                "Basic Berserker": {
                    "art": {
                        1: "         ",
                        2: "(-╦-) /''",
                        3: "  ║  (b_b",
                        4: "  ╰_(())|",
                        5: "     ((()",
                        6: "    / / \\",
                    },
                    "description": "a basic berserker",
                    "health": lambda: 1,
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(6,8),

                },
                "Plain Paladin": {
                    "art": {
                        1: "         ",
                        2: "         ",
                        3: "   ()} _ ",
                        4: "  /||_/']",
                        5: " /|_\_/  ",
                        6: "  /  \\\  ",
                    },
                    "description": "a plain paladin",
                    "health": lambda: random.randint(1,3),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(1,5),
                },                
                "Common Conjurer": {
                    "art": {
                        1: " /\     m",
                        2: "/  \_   e",
                        3: "-━ᶗ━)   w",
                        4: "/**\╭  / ",
                        5: "****\oo_S",
                        6: "|  | /\ \\",
                    },
                    "description": "a common conjurer",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(2,6),
                },
                "Ordinary Orc": {
                    "art": {
                        1: "work _,_ ",
                        2: "work(;; )",
                        3: "    ╭()))",
                        4: "   / (())",
                        5: " (/)(/ (\\",
                        6: "   .(|.(|",
                    },
                    "description": "an ordinary orc",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,6),
                },
                "Regular Rogue": {
                    "art": {
                        1: " Work    ",
                        2: " Sucks   ",
                        3: "   \     ",
                        4: "   Ậ()   ",
                        5: "<=+/▐▌   ",
                        6: "  _/,|   ",
                    },
                    "description": "a regular rogue",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 1 if random.randint(0,100) > 95 else 0,
                    "value": lambda: random.randint(5,7),
                },
                "Standard Slime": {
                    "art": {
                        1: "  _____  ",
                        2: " (_o.o_) ",
                        3: "         ",
                        4: "   (o.o) ",
                        5: "  ___    ",
                        6: " (   )   ",
                    },
                    "description": "a bunch of slimes",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,8),
                },
                "Typical Troll": {
                    "art": {
                        1: "  ___  _ ",
                        2: " (>,</ / ",
                        3: " /| / /  ",
                        4: " \}/ /{> ",
                        5: "  /_/\   ",
                        6: " '    '  ",
                    },
                    "description": "a typical troll, holding a massive log, he looks mad",
                    "health": lambda: random.randint(1,5),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(2,5),
                },
                "Average Archer": {
                    "art": {
                        1: "         ",
                        2: "(O)) /() ",
                        3: "   <(-██'",
                        4: "     \/| ",
                        5: "    _/ | ",
                        6: "         ",
                    },
                    "description": "maybe below average",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,9),
                },
                "Normal Necromancer": {
                    "art": {
                        1: "╺■■■┃ () ",
                        2: ".-. ┃-██'",
                        3: "o.o)┃ /| ",
                        4: "|=| ┃/ | ",
                        5: "_|__     ",
                        6: "=|=.\\\\   ",
                    },
                    "description": "just a regular guy, don't be wierd",
                    "health": lambda: random.randint(2,3),
                    "attack": lambda: 1,
                    "armor": lambda: 1,
                    "barrier": lambda: 1 if random.randint(0,100) > 66 else 0,
                    "value": lambda: random.randint(1,8),
                },
                "Usual Unicorn": {
                    "art": {
                        1: "  Rip    ",
                        2: "   More  ",
                        3: " ║╲ Packs",
                        4: "[≤'\───┐ ",
                        5: "  |╲___/\\",
                        6: " /  ╲  ╲ ",
                    },
                    "description": "Damn it's the shit one",
                    "health": lambda: random.randint(1,3),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(2,4),
                    "value": lambda: random.randint(1,50),
                },
                "PLS ADD BUY100PACKS": {
                    "art": {
                        1: "buy10pack",
                        2: "buy10pack",
                        3: "buy10pack",
                        4: "buy10pack",
                        5: "buy10pack",
                        6: "buy10pack",
                    },
                    "description": "need more money for packs",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: 100 if random.randint(0,100) > 90 else 1,
                },
                "Mundane Minotaur": {
                    "art": {
                        1: "         ",
                        2: "((_,.,_))",
                        3: "/ |╾ ╼| \\",
                        4: "  \   /  ",
                        5: "  /╰╩╯\  ",
                        6: "\ )   ( /",
                    },
                    "description": "HERE is the beef",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 2,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,15),
                },
                "Generic Gnome": {
                    "art": {
                        1: "         ",
                        2: "      ʌ  ",
                        3: "  []_(‟)_",
                        4: "  ʌ  | | ",
                        5: "_(‟)_,   ",
                        6: " | |     ",
                    },
                    "description": "theres two of em!",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(5,20),
                },
                "Default Dwarf": {
                    "art": {
                        1: "  And    ",
                        2: "  (|)    ",
                        3: "   |_(╦)_",
                        4: "   ' / \ ",
                        5: "  my     ",
                        6: "  Axe!   ",
                    },
                    "description": "and my axe!",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(3,5),
                    "armor": lambda: 3 if random.randint(0,100) > 80 else 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Standard Sphinx": {
                    "art": {
                        1: "         ",
                        2: "  /\-/\\  ",
                        3: " | o_o | ",
                        4: "| \_^_/ |",
                        5: "|  |_|  |",
                        6: "'uuu uuu'",
                    },
                    "description": "look, I don't know what to tell you about this",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(5,10),
                },
                "Common Centaur": {
                    "art": {
                        1: "  ,___   ",
                        2: "  ()/    ",
                        3: " /||___, ",
                        5: "  |╲___|\\",
                        6: " /  ╲  ╲ ",
                        6: "         ",
                    },
                    "description": "he's throwing a spear",
                    "health": lambda: random.randint(3,5),
                    "attack": lambda: 2,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,5),
                },
                "Basic Basilisk": {
                    "art": {
                        1: "    _    ",
                        2: " __' '__ ",
                        3: "/ (0 0) \\",
                        4: ")  (_)  (",
                        5: "\__   __/",
                        6: "   '-'   ",
                    },
                    "description": "yeah I don't know about that art either",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Ordinary Ogre": {
                    "art": {
                        1: "   ___   ",
                        2: "  (o,o)  ",
                        3: " / . . \ ",
                        4: "/(     )\\",
                        5: " //   \\\\ ",
                        6: "  '    ' ",
                    },
                    "description": "I'm an OGRE",
                    "health": lambda: random.randint(3,6),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 1,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,10),
                },
                "Regular Rat": {
                    "art": {
                        1: "         ",
                        2: "  __QQ   ",
                        3: " (_)_\">  ",
                        4: "_)  __QQ ",
                        5: "   (_)_\">",
                        6: "  _)     ",
                    },
                    "description": "Q's are ears, _) are tails u,u",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Simple Skeleton": {
                    "art": {
                        1: "   .-.   ",
                        2: "  (o.o)  ",
                        3: "   |=|   ",
                        4: "  __|__  ",
                        5: "//.=|=.\\\\",
                        6: "/ .=|=. \\",
                    },
                    "description": "a skelebob",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(4,5),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Sad Skeleton": {
                    "art": {
                        1: "         ",
                        2: "   .-.   ",
                        3: "  (u.u)  ",
                        4: "  _|n| _ ",
                        5: "//.=|=.\\\\",
                        6: "/ .=|=. \\",
                    },
                    "description": "it's a sad skelebob",
                    "health": lambda: 1,
                    "attack": lambda: 6,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Plain Phoenix": {
                    "art": {
                        1: "         ",
                        2: "   ___   ",
                        3: ";;(°v°);;",
                        4: "  _/ \_  ",
                        5: "  _|Y|_  ",
                        6: "         ",
                    },
                    "description": "not as nice as the good one",
                    "health": lambda: random.randint(2,3),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(1,10),
                },
                "Common Crow": {
                    "art": {
                        1: "         ",
                        2: "   \\\\    ",
                        3: "    (o > ",
                        4: "\\\\_// )  ",
                        5: " \//__)  ",
                        6: "   \/    ",
                    },
                    "description": "hard to catch",
                    "health": lambda: 1,
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 2,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Basic Bat": {
                    "art": {
                        1: "         ",
                        2: " /^v^\   ",
                        3: "         ",
                        4: "    /^v^\\",
                        5: "         ",
                        6: " /^v^\   ",
                    },
                    "description": "annoying to hit",
                    "health": lambda: 3,
                    "attack": lambda: 1,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Opulent Ogre": {
                    "art": {
                        1: "  /$\    ",
                        2: " (o,o)   ",
                        3: " /. . \  ",
                        4: "/(   )|. ",
                        5: "  / \[$$]",
                        6: " '   '   ",
                    },
                    "description": "surely it's better than the ordinary one",
                    "health": lambda: random.randint(2,7),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 1,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(15,30),
                },
                "Standard Spider": {
                    "art": {
                        1: "         ",
                        2: "         ",
                        3: "  ||  || ",
                        4: "  \\\\()// ",
                        5: " //(__)\\\\",
                        6: " ||    ||",
                    },
                    "description": "yuck",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,6),
                },
                "Average Ant": {
                    "art": {
                        1: "     ,   ",
                        2: " ooo<    ",
                        3: " /||     ",
                        4: " __     ,",
                        5: "(__).o.@c",
                        6: " /  |  \ ",
                    },
                    "description": "annoying but weak",
                    "health": lambda: 4,
                    "attack": lambda: 1,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Normal Newt": {
                    "art": {
                        1: "         ",
                        2: "   c0__  ",
                        3: "    /`=, ",
                        4: "     ,='\\",
                        5: "     |   ",
                        6: "         ",
                    },
                    "description": "like an ant but needs a bigger shoe",
                    "health": lambda: 2,
                    "attack": lambda: 1,
                    "armor": lambda: 1,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Deluxe Demon": {
                    "art": {
                        1: " /\/|\/\ ",
                        2: "|  \|/  |",
                        3: "( 0\ /0 )",
                        4: " \ ◄◙► / ",
                        5: "  \___/  ",
                        6: " /     \ ",
                    },
                    "description": "1/6/1 6/1/1 6/6/1 which is it?",
                    "health": lambda: 6 if random.randint(0,100) > 66 else 1,
                    "attack": lambda: 6 if random.randint(0,100) > 66 else 1,
                    "armor": lambda: 1 if random.randint(0,100) > 66 else 1,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,66),
                },
                "Everyday Eagle": {
                    "art": {
                        1: "      __ ",
                        2: "     <{'\\",
                        3: "  ____) (",
                        4: " //'--;  ",
                        5: "///////\_",
                        6: "       m ",
                    },
                    "description": "my eagle's too busy looking out for me",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Mundane Mantis": {
                    "art": {
                        1: " _     _ ",
                        2: "' \ _ / '",
                        3: " /(.Y.)\ ",
                        4: "\--\ /--/",
                        5: " \  '  / ",
                        6: " /     \ ",
                    },
                    "description": "yuck",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Generic Gecko": {
                    "art": {
                        1: "         ",
                        2: "         ",
                        3: " c(()__  ",
                        4: "   /`=,, ",
                        5: "    ,='`\\",
                        6: "   |     ",
                    },
                    "description": "like a newt but a bigger target",
                    "health": lambda: 3,
                    "attack": lambda: 1,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Default Deer": {
                    "art": {
                        1: "     ,_, ",
                        2: "   __/\". ",
                        3: " -/__ | /",
                        4: "  || ||/ ",
                        5: "______/ ~",
                        6: " ~    ~  ",
                    },
                    "description": "it's a deer next to a watering hole",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(0,1),
                    "value": lambda: random.randint(1,10),
                },
                "Standard Stag": {
                    "art": {
                        1: "         ",
                        2: "         ",
                        3: "    '\\_/'",
                        4: "   __/\". ",
                        5: "  /__ |  ",
                        6: "  || ||  ",
                    },
                    "description": "it's a deer, but less magical",
                    "health": lambda: random.randint(3,4),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Common Cat": {
                    "art": {
                        1: "Fuck you.",
                        2: "/\_/\  ( ",
                        3: " o.o ) _)",
                        4: " \\\"/  (  ",
                        5: " | | )   ",
                        6: "_d b__)  ",
                    },
                    "description": "typical cat",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(3,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Basic Bear": {
                    "art": {
                        1: "  \\'''/  ",
                        2: "(0     0)",
                        3: "  /( )\  ",
                        4: "  \_Y_/  ",
                        5: "\_______/",
                        6: "         ",
                    },
                    "description": "big boy",
                    "health": lambda: random.randint(4,5),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Regular Rabbit": {
                    "art": {
                        1: "   WE    ",
                        2: "  FUCK   ",
                        3: "  //'    ",
                        4: " (◦Ͻ     ",
                        5: "./rr     ",
                        6: "╰\))_    ",
                    },
                    "description": "basically harmless",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: 1,
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,40),
                },
                "Simple Shark": {
                    "art": {
                        1: "     .=( ",
                        2: " ☼  (   (",
                        3: "    _`- _",
                        4: "   / |   ",
                        5: "__/  |___",
                        6: "  ~ ~  ~ ",
                    },
                    "description": "stay outta that water",
                    "health": lambda: random.randint(2,3),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Thrift Store Knight": {
                    "art": {
                        1: "This     ",
                        2: "Saturday ",
                        3: " \.''.,, ",
                        4: "(  ○ ○  )",
                        5: " | ╯┺╰ | ",
                        6: " \  ─╯ / ",
                    },
                    "description": "looks sorta like mangles",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 1,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,10),
                },
                "Bargain Hunter": {
                    "art": {
                        1: " # /|    ",
                        2: "@ /      ",
                        3: " / 0  () ",
                        4: "/  |`-██'",
                        5: "|     /| ",
                        6: "    _/ | ",
                    },
                    "description": "just browsing thanks mater",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,100),
                },
                "Discount Demon": {
                    "art": {
                        1: " /\   /\ ",
                        2: "|  \ /  |",
                        3: "( ☼╲ ╱☼ )",
                        4: " \  _  / ",
                        5: "  \___/  ",
                        6: " /     \ ",
                    },
                    "description": "it's worthless? maybe stronger",
                    "health": lambda: random.randint(1,6),
                    "attack": lambda: random.randint(1,6),
                    "armor": lambda: random.randint(1,6),
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(1,66),
                },
                "Cheap Shot": {
                    "art": {
                        1: "   ()    ",
                        2: "<(-▐▌'   ",
                        3: "   /|    ",
                        4: "e     Ậ()",
                        5: "z  <=+/▐▌",
                        6: "     _/,|",
                    },
                    "description": "he won't even see it coming",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(3,5),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,15),
                },
                "Clearance Cleric": {
                    "art": {
                        1: "     __  ",
                        2: "    |╋ | ",
                        3: "   (o,o-)",
                        4: " ┃ ╭/  \╮",
                        5: " ┃-╯|__|/",
                        6: " ┃ _|  |_",
                    },
                    "description": "surely he could get a nicer rod",
                    "health": lambda: random.randint(2,3),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda:  2 if random.randint(0,100) > 66 else 0,
                    "value": lambda: random.randint(1,10),
                },
                "Ordinary Oracle": {
                    "art": {
                        1: "    \~~/ ",
                        2: "   (-,- )",
                        3: "   ╭/  \╮",
                        4: "   /∈()∋\\",
                        5: "   _|  |_",
                        6: "         ",
                    },
                    "description": "predict this",
                    "health": lambda: random.randint(3,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 2 if random.randint(0,100) > 80 else 1,
                    "value": lambda: random.randint(25,50),
                },
                "Toms Joke": {
                    "art": {
                        1: " __   __ ",
                        2: "|  | |  |",
                        3: "|  | |  |",
                        4: "|  | |  |",
                        5: "|__|-|__|",
                        6: "|___|___|",
                    },
                    "description": "it looks like a pair of linked buildings?",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,50),
                },
            },
            "uncommon": {
                "Gutter Goblin": {
                    "art": {
                        1: "_________",
                        2: "======[__",
                        3: "(|)      ",
                        4: " |(;;)   ",
                        5: "  /  \   ",
                        6: "         ",
                    },
                    "description": "it's a little goblin next to a drain",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Mangles Endgame": {
                    "art": {
                        1: " ,.''.,, ",
                        2: "( ^   ^ )",
                        3: " | ╯┺╰ | ",
                        4: " _\ ▼ /_ ",
                        5: "/       \\",
                        6: " ENDGAME ",
                    },
                    "description": "another mangles",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(15,20),
                },
                "Premium Phoenix": {
                    "art": {
                        1: "   ~~~   ",
                        2: ";;(°v°);;",
                        3: "  _/ \_  ",
                        4: "         ",
                        5: "         ",
                        6: " $       ",
                    },
                    "description": "better than the common one I guess",
                    "health": lambda: random.randint(1,3),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 1,
                    "barrier": lambda: 1 if random.randint(0,100) > 60 else 0,
                    "value": lambda: random.randint(10,15),
                },
                "Consecrated Cleric": {
                    "art": {
                        1: " ╻   /\  ",
                        2: "╼╋╾ |╋ | ",
                        3: " ┃ (o,o-)",
                        4: " ┃ ╭/  \╮",
                        5: " ┃-╯|__|/",
                        6: " ┃ _|  |_",
                    },
                    "description": "oh shit look at that rod",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 2 if random.randint(0,100) > 85 else 0,
                    "value": lambda: random.randint(10,15),
                },
                "Glue horse": {
                    "art": {
                        1: "         ",
                        2: "         ",
                        3: " __      ",
                        4: "[≤'\───┐,",
                        5: "  |╲___|\\",
                        6: " /  ╲  ╲ ",
                    },
                    "description": "not the best horse, has _a_ use",
                    "health": lambda: random.randint(1,3),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(25,45),
                },
                "Aristocratic Angel": {
                    "art": {
                        1: "      ⊂⊃ ",
                        2: "   _∫(ᵔ͜ᵔ)",
                        3: "__/ ( Y )",
                        4: "/ / /|__|",
                        5: "/ /  /  \\",
                        6: "/        ",
                    },
                    "description": "not sure if she's an aristocrat",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(20,25),
                },
                "Orc Bard Barista": {
                    "art": {
                        1: "order_,_ ",
                        2: "for (;; )",
                        3: "ne[]╭()))",
                        4: "st \\\(())",
                        5: "or ( % )\\",
                        6: "???.(|.(|",
                    },
                    "description": "he's got that grindset",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(1,3),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(25,50),
                },
                "Max Min Mangles": {
                    "art": {
                        1: "TERRACOTT",
                        2: "A SOLDIER",
                        3: " ,.''.,, ",
                        4: "( ^   ^ )",
                        5: " | ╯┺╰ | ",
                        6: " \  ─╯ / ",
                    },
                    "description": "is this my favourite mangles?",
                    "health": lambda: random.randint(3,4),
                    "attack": lambda: random.randint(3,4),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: random.randint(0,2),
                    "value": lambda: random.randint(1,50),
                },
                "Shekel Goblin": {
                    "art": {
                        1: "      (s)",
                        2: "  (^^)/  ",
                        3: "  /  \   ",
                        4: "         ",
                        5: "         ",
                        6: "         ",
                    },
                    "description": "aww look at em",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Destitute Dragon": {
                    "art": {
                        2: " \\\\_v_// ",
                        3: "  )_^_(  ",
                        4: " / 0 0 \ ",
                        5: "| /. .\ |",
                        6: " \\\\v_v// ",
                        6: " _/wvwv\_"
                    },
                    "description": "it's sad for a dragon card",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(50,75),
                },
                "Empty Purse": {
                    "art": {
                        1: " /    \  ",
                        1: " \     | ",
                        2: "   ╮ ╭'  ",
                        3: "   ╯ ╰   ",
                        5: "    '    ",
                        6: "   _'_   ",
                    },
                    "description": "it's a moneyback you sicko",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(50,100),
                },
                "Scrum Master": {
                    "art": {
                        1: "         ",
                        2: "   ...   ",
                        3: "         ",
                        4: "   ...   ",
                        5: "         ",
                        6: "         ",
                    },
                    "description": "that's what it's worth?",
                    "health": lambda: 1,
                    "attack": lambda: 1,
                    "armor": lambda: 1,
                    "barrier": lambda: 1,
                    "value": lambda: 1,
                },
                "Diamond Dealer": {
                    "art": {
                        1: "         ",
                        2: ",-|‾‾‾|-,",
                        3: "|  \ /  |",
                        4: " \ | | / ",
                        5: "   \_/   ",
                        6: "         ",
                    },
                    "description": "I'm not drawing that",
                    "health": lambda: random.randint(1,3),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,100),
                },
                "Platinum Purse": {
                    "art": {
                        1: " /0oO0\  ",
                        1: " \oO,oO| ",
                        2: "   ╮O╭'  ",
                        3: "   ╯0╰   ",
                        5: "  0o()Oo ",
                        6: "o0()()0oO",
                    },
                    "description": "it's a full coin bag you sicko",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(100,150),
                },
                "Emerald Emperor": {
                    "art": {
                        1: "     __  ",
                        2: "|S| /  \ ",
                        3: "\┰/(e,e-)",
                        4: " ┃ ╭/  \╮",
                        5: " ┃-╯\__//",
                        6: " ┃ _|  |_",
                    },
                    "description": "yeah I'm not sure about his eyes",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(1,2),
                    "value": lambda: random.randint(10,15),
                },
                "Ruby Regent": {
                    "art": {
                        1: "/ \      ",
                        2: "\┰/|/\/\|",
                        3: " ┃ (r,r-)",
                        4: " ┃ ╭/  \╮",
                        5: " ┃-╯\__//",
                        6: " ┃ _|  |_",
                    },
                    "description": "I like his crown",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(4,5),
                    "armor": lambda: 2,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(10,15),
                },
                "Sapphire Sultan": {
                    "art": {
                        1: "         ",
                        2: " ▲  /||\ ",
                        3: " ▼ (s,s-)",
                        4: " ┃╭/    \\",
                        5: " ┃╯\____/",
                        6: " ┃ _|  |_",
                    },
                    "description": "It's a good sized staff",
                    "health": lambda: random.randint(1,5),
                    "attack": lambda: random.randint(4,5),
                    "armor": lambda: random.randint(0,3),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(5,10),
                },
                "Crystal Crusher": {
                    "art": {
                        1: "|   )  | ",
                        2: "|   \  | ",
                        3: "\  / ||  ",
                        4: " || \__/ ",
                        5: "\__/  /\ ",
                        6: "   /\/\/\\",
                    },
                    "description": "those are legs",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(4,6),
                    "armor": lambda: random.randint(1,3),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1,20),
                },
                "Gem Guardian": {
                    "art": {
                        1: "         ",
                        2: "    (g,g)",
                        3: "   ╭(()))",
                        4: "<>/ (()) ",
                        5: "   (/ (\\ ",
                        6: " .(| .(| ",
                    },
                    "description": "it's a construct",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(3,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Jewel Juggernaut": {
                    "art": {
                        1: " /\   _,_",
                        2: " \/ (jj )",
                        3: "  \_╭()))",
                        4: "     (())",
                        5: "    (/ (\\",
                        6: "  .(| .(|",
                    },
                    "description": "bitch",
                    "health": lambda: random.randint(3,5),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Precious Protector": {
                    "art": {
                        1: "         ",
                        2: "  <>  /\ ",
                        3: "( o,o)\/ ",
                        4: " /  \╭/  ",
                        5: " |--| [$]",
                        6: " |\ |_[$]",
                    },
                    "description": "I'm not sure what he's up to",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(50,100),
                },
                "Valuable Valkyrie": {
                    "art": {
                        1: "         ",
                        2: "[$$]     ",
                        3: "  \_∫(--)",
                        4: "__/  |  |",
                        5: "/ / /|__|",
                        6: "/ /  /  \\",
                    },
                    "description": "i think it's a wing, with an arm holding money above it",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(3,5),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,40),
                },
                "Expensive Executioner": {
                    "art": {
                        1: "    ( | )",
                        2: " ┓┓┓┓ |  ",
                        3: "( o,o)|  ",
                        4: " /  \╭|  ",
                        5: " |--|    ",
                        6: " |\ |_   ",
                    },
                    "description": "what is that helmet?",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: 3,
                    "armor": lambda: random.randint(2,3),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Costly Crusader": {
                    "art": {
                        1: "         ",
                        2: "[_|      ",
                        3: "  |()/ _ ",
                        4: "  |||_/']",
                        5: " /|_\_/  ",
                        6: "  /  \\\  ",
                    },
                    "description": "magic + armor?",
                    "health": lambda: random.randint(3,4),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(10,15),
                },
                "Pricey Paladin": {
                    "art": {
                        1: "         ",
                        2: "[_|      ",
                        3: "  |()/ _ ",
                        4: "  |||_/']",
                        5: " /|_\_/  ",
                        6: "  /  \\\  ",
                    },
                    "description": "magic + armor!",
                    "health": lambda: random.randint(2,3),
                    "attack": lambda: random.randint(3,4),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(10,15),
                },
                "Lavish Lancer": {
                    "art": {
                        1: "        |",
                        2: "     /| |",
                        3: "  ()/ _ |",
                        4: " .||_/']|",
                        5: "/|_\_/  |",
                        6: " /  \\\  |",    
                    },
                    "description": "armor + lance!",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,3),
                    "armor": lambda: random.randint(1,3),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(10,15),
                },
                "Sumptuous Sorcerer": {
                    "art": {
                        1: "  /\     ",
                        2: "_/--\_   ",
                        3: "(-o,o)   ",
                        4: " /--\_() ",
                        5: "/----\   ",
                        6: " |_ |_   ",
                    },
                    "description": "don't like that name at all",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(1,5),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(10,15),
                },
                "Opulent Oracle": {
                    "art": {
                        1: "    ____ ",
                        2: "   ($,$ )",
                        3: "   ╭/  \╮",
                        4: "   /∈()∋\\",
                        5: "   _|  |_",
                        6: "         ",
                    },
                    "description": "sit down at my table, put your mind at ease",
                    "health": lambda: random.randint(1,4),
                    "attack": lambda: random.randint(1,5),
                    "armor": lambda: 0,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(10,50),
                },
            },
            "rare": {
                "Poncho's Party": {
                    "art": {
                        1: " JUSTICE ",
                        2: "    _    ",
                        3: "   | |   ",
                        4: "  |PON|  ",
                        5: "  |CHO|  ",
                        6: "  ( S )  ",
                    },
                    "description": "caramel sauce is ruined forever",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 2 if random.randint(0,100) > 90 else 1,
                    "value": lambda: random.randint(100,200),
                },
                "Butter Chicken Pizza": {
                    "art": {
                        1: "P |    | ",
                        2: "I |____| ",
                        3: "Z/(   )//",
                        4: "Z-----'' ",
                        5: "A  /___/,",
                        6: "B C'---' ",
                    },
                    "description": "May as well have a butter chicken as well",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(2,5),
                    "armor": lambda: 2,
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "Hemoglobin": {
                    "art": {
                        1: "    (RBC)",
                        2: " (HGB)   ",
                        3: "   (HCT) ",
                        4: "(HGB)    ",
                        5: "  (PLT)  ",
                        6: "(HGB)(MD)",
                    },
                    "description": "She'll be a genius!",
                    "health": lambda: random.randint(3,6),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 25 else 0,
                    "value": lambda: random.randint(100,300),
                },
                "No Joy": {
                    "art": {
                        1: "L3: idnnn",
                        2: "   [nff] ",
                        3: "    /|\  ",
                        4: "     |   ",
                        5: "   [nbp] ",
                        6: "L2: nojoy",
                    },
                    "description": "internet data no fault found no fault found no fault found",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "Any Danger": {
                    "art": {
                        1: "  HURRY  ",
                        2: " ,----.  ",
                        3: "/      \ ",
                        4: "\ STOP / ",
                        5: " '____'  ",
                        6: "   UP    ",
                    },
                    "description": "annny danger of a pickup",
                    "health": lambda: random.randint(3,5),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: 2,
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "Busy Night Tonight Mate?": {
                    "art": {
                        1: "    __   ",
                        2: " __/  \_ ",
                        3: "'-0---0-'",
                        4: "    __   ",
                        5: " __/oo\_ ",
                        6: "'-0---0-'",
                    },
                    "description": "yeaaaah flat out",
                    "health": lambda: random.randint(4,7),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(100,200),
                },
                "Cold Drink of Water": {
                    "art": {
                        1: "YAHTZEE??",
                        2: "    _    ",
                        3: "   / \   ",
                        4: "  |   |  ",
                        5: "  |h20|  ",
                        6: "  (   )  ",
                    },
                    "description": "brb, just gotta grab a cold water",
                    "health": lambda: random.randint(3,5),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "One in the Cuck Chair": {
                    "art": {
                        1: "    `\\0_ ",
                        2: "   ╭|▄█╭|",
                        3: "  _______",
                        4: " /|/ |/ /",
                        5: "/,/ ,/ //",
                        6: "(0)(0)// ",
                    },
                    "description": "he's loving it",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(3,4),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,300),
                },
                "Thicc Codpiece": {
                    "art": {
                        1: "__\___/__",
                        2: "_  eyes _",
                        3: " \ up  / ",
                        4: "  |here| ",
                        5: " / Ɑ͞ ̶͞ධ \\ ",
                        6: "/   /\  \\",
                    },
                    "description": "That's definitely a codepiece",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 2 if random.randint(0,100) > 90 else 1,
                    "value": lambda: random.randint(100,200),
                },
                "Toms 'Long Shot' Odds": {
                    "art": {
                        1: " 100:1   ",
                        2: " No Way  ",
                        3: "  Yuki   ",
                        4: "  Gets   ",
                        5: "the Seat ",
                        6: "-Tom, Pro",
                    },
                    "description": "gl on the value roll",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(1,1000),
                },
                "Day 2 Trap Reroll": {
                    "art": {
                        1: "Day ____ ",
                        2: " 2 |BOSS|",
                        3: "  /~~~~/m",
                        4: "\()  Boys",
                        5: " ||\ Trap",
                        6: " /\  Time",
                    },
                    "description": "thats a computer!",
                    "health": lambda: random.randint(1,3),
                    "attack": lambda: random.randint(5,10),
                    "armor": lambda: 0,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(100,300),
                },
                "Half a Pack o Winny Blues": {
                    "art": {
                        1: "   ___●_ ",
                        2: "  |___█_|",
                        3: ",/ooo_▀_/",
                        4: "|Winni ||",
                        5: "| Blues||",
                        6: "|______|/",
                    },
                    "description": "I don't know this reference",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "6'5 Blue Eyes": {
                    "art": {
                        1: " TRUST   ",
                        2: "    FUND ",
                        3: "         ",
                        4: "   _._   ",
                        5: " .'  ☼`. ",
                        6: "c|     |Ↄ",
                    },
                    "description": "it's the back of a head",
                    "health": lambda: random.randint(4,6),
                    "attack": lambda: random.randint(1,2),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,500),
                },
                "Min Max Mangles": {
                    "art": {
                        1: "Day 7:   ",
                        2: "Maps suck",
                        3: " ,.''.,, ",
                        4: "( u   u )",
                        5: " | ╯┺╰ | ",
                        6: "  \ ‾ /  ",
                    },
                    "description": "He's doing it!",
                    "health": lambda: random.randint(3,5),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 1,
                    "barrier": lambda: 1 if random.randint(0,100) > 66 else 0,
                    "value": lambda: random.randint(50,500),
                },
                "Donkey Kongs Donkey Dong": {
                    "art": {
                        1: "    // B ",
                        2: "  /  | A ",
                        3: " / ,|  N ",
                        4: "|  '|  A ",
                        5: " \  '\ N ",
                        6: "   \ | A ",
                    },
                    "description": "it's just a banana",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(4,5),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "Production Rollback": {
                    "art": {
                        1: " I LOST  ",
                        2: "   MY    ",
                        3: "  CARDS  ",
                        4: "   wtf   ",
                        5: "         ",
                        6: "         ",
                    },
                    "description": "yeah sorry",
                    "health": lambda: random.randint(1,8),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "Ice Raid": {
                    "art": {
                        1: "-~-~-,   ",
                        2: "-|0 __ `,",
                        3: " __/  \_'",
                        4: "'-0---0-'",
                        5: "  >-|0   ",
                        6: "    0|-< ",
                    },
                    "description": "Border of the circle 3 boys in 3 cards hitting 3 try-hards",
                    "health": lambda: 3,
                    "attack": lambda: 3,
                    "armor": lambda: 3,
                    "barrier":1,
                    "value": lambda: random.randint(100,200),
                },
                "Royal Reaper": {
                    "art": {
                        1: "  ,_____ ",
                        2: " ┓▄▄▄  / ",
                        3: "(o,o-)/  ",
                        4: "╭/  \/   ",
                        5: "/   /\   ",
                        6: "_| /|    ",
                    },
                    "description": "It's scythe damnit",
                    "health": lambda: random.randint(2,6),
                    "attack": lambda: random.randint(2,6),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,200),
                },
                "Pirate Punch": {
                    "art": {
                        1: "  (___)  ",
                        2: "--|yar|--",
                        3: "__'---'_ ",
                        4: " it's a  ",
                        5: "bucket o'",
                        6: " liquor  ",
                    },
                    "description": "thank god we don't do this anymore",
                    "health": lambda: random.randint(3,5),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 2,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(100,300),
                },
                "Daves Cokecan": {
                    "art": {
                        1: " ALWAYS  ",
                        2: "COCA COLA",
                        3: " ╭──╥──╮ ",
                        4: " ├─   ─┤ ",
                        5: " |     | ",
                        6: "(   Y   )",
                    },
                    "description": "alotta girth, not a lot of range",
                    "health": lambda: random.randint(6,12),
                    "attack": lambda: random.randint(2,3),
                    "armor": lambda: 1,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(100,400),
                },
                "Debt Demon": {
                    "art": {
                        1: " /\   /\ ",
                        2: "|  \ /  |",
                        3: "( $\ /$ )",
                        4: " \ <=>  /",
                        5: "  \___/  ",
                        6: " /     \ ",
                    },
                    "description": "666",
                    "health": lambda: 6,
                    "attack":6,
                    "armor": lambda: random.randint(1,3),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: 6,
                },
                "Codename Cough": {
                    "art": {
                        1: "  COUGH  ",
                        2: "   ...   ",
                        3: "   :D    ",
                        4: "  YEAH   ",
                        5: "   ;)    ",
                        6: "WE GOT IT",
                    },
                    "description": "This card is rigged",
                    "health": lambda: 3,
                    "attack": lambda: 4,
                    "armor": lambda: 1,
                    "barrier": lambda: 1,
                    "value": lambda: 500,
                },
                "Imperial Imp": {
                    "art": {
                        1: " \ ═╬═ / ",
                        2: " |  ║  | ",
                        3: "( ☼╲ ╱☼ )",
                        4: " \  ▼  / ",
                        5: "  \___/  ",
                        6: " /    '\ ",
                    },
                    "description": "An imp cardinal?",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 2 if random.randint(0,100) > 33 else 1,
                    "value": lambda: random.randint(100,350),
                },
                "Transmutation": {
                    "art": {
                        1: " (  (  _)",
                        2: "  \ / /  ",
                        3: "  /\|/\  ",
                        4: " |   //| ",
                        5: " |  // | ",
                        6: "  \___/  ",
                    },
                    "description": "it makes it blue",
                    "health": lambda: random.randint(3,8),
                    "attack": lambda: random.randint(1,7),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(100,400),
                },
                "Alchemy": {
                    "art": {
                        1: "Alch ,_  ",
                        2: "   _)~ \ ",
                        3: " ~( &   ~",
                        4: "  ~)__ Go",
                        5: "  (  a|  ",
                        6: "   \_/   ",
                    },
                    "description": "it makes it gold",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(100,350),
                },
                "Perfect Phoenix": {
                    "art": {
                        1: "  * . ◦ *",
                        2: "◦    *   ",
                        3: " ' mmm   ",
                        4: ";;(°v°);;",
                        5: "* _/ \_  ",
                        6: "  ◦   *  ",
                    },
                    "description": "So shiny",
                    "health": lambda: random.randint(2,4),
                    "attack": lambda: random.randint(4,5),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 60 else 0,
                    "value": lambda: random.randint(50,250),
                },
                "Supreme Shekel": {
                    "art": {
                        1: "  .---.  ",
                        2: " / § § \ ",
                        3: "| § § § |",
                        4: "|  § §  |",
                        5: " \  §  / ",
                        6: "  '---'  ",
                    },
                    "description": "E Z",
                    "health": lambda: random.randint(4,5),
                    "attack": lambda: random.randint(3,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(100,750),
                },
                "Fabled Fortune": {
                    "art": {
                        1: "  * ____ ",
                        2: "  '|    |",
                        3: "\* |____|",
                        4: "' /$$$$/|",
                        5: "-/____/ /",
                        6: " |____|/ ",
                    },
                    "description": "POG",
                    "health": lambda: random.randint(2,5),
                    "attack": lambda: random.randint(1,4),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 1 if random.randint(0,100) > 90 else 0,
                    "value": lambda: random.randint(100,800),
                },
            },
            "mythic": {
                "League Start with the Boys": {
                    "art": {
                        1: "   [POE] ",
                        2: "___[DAY]_",
                        3: "  ZzZ    ",
                        4: "zZ       ",
                        5: "| 0|-<  _",
                        6: "|tomsbed|",
                    },
                    "description": "9:42am - I think Tom's gone to lay down",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: 2,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(400,1200),
                },
                "Big Booty Bitches (WOO)": {
                    "art": {
                        1: "  |||||  ",
                        2: " ||◦╷◦|| ",
                        3: "|||\ꜚ/|||",
                        4: "/(.) (.)\\",
                        5: "\ ) . ( /",
                        6: "'(  v  )`"
                    },
                    "description": "NSFW",
                    "health": lambda: random.randint(4,8),
                    "attack": lambda: random.randint(4,10),
                    "armor": lambda: 1,
                    "barrier": lambda: 2 if random.randint(0,100) > 80 else 1,
                    "value": lambda: random.randint(400,2000),
                },
                "Batman Butt-naked": {
                    "art": {
                        1: " ,.''.,, ",
                        2: "( 0   0 )",
                        3: " |< ┺ >| ",
                        4: " /(_M_)\ ",
                        5: "|  , .  |",
                        6: " \/~V~\/ "
                    },
                    "description": "That's a bat, not a beard",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: 2,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(500,1000),
                },
                "Two Boys in the Cupboard": {
                    "art": {
                        1: ".| / ___ ",
                        2: " |/╭|cc╭|",
                        3: " /  ____ ",
                        4: "/ /    /|",
                        5: " /    /  ",
                        6: "/(  )/   ",
                    },
                    "description": "They're waiting",
                    "health": lambda: random.randint(2,8),
                    "attack": lambda: random.randint(1,9),
                    "armor": lambda: 1,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(500,1200),
                },
                "Ultimate Unicorn": {
                    "art": {
                        1: " ◌ *    *",
                        2: "   ·  ◌  ",
                        3: " ║╲  * · ",
                        4: "[≤'\───┐ ",
                        5: " ◌|╲___/\\",
                        6: " /· ╲  ╲ ",
                    },
                    "description": "Unicorn Unleashed!",
                    "health": lambda: random.randint(5,10),
                    "attack": lambda: random.randint(3,8),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(2,4),
                    "value": lambda: random.randint(500,1500),
                },
                "Celestial Coin": {
                    "art": {
                        1: "  .---.  ",
                        2: " / C C \ ",
                        3: "| C c C |",
                        4: "|  C C  |",
                        5: " \  *  / ",
                        6: "  '---'  ",
                    },
                    "description": "1/6 for 2.5k, 5/6 for 1k",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: 0,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: 2500 if random.randint(0,100) > 16 else 1000,
                },
                "Divine Dollar": {
                    "art": {
                        1: "  .---.  ",
                        2: " / D D \ ",
                        3: "| D $ D |",
                        4: "|  D D  |",
                        5: " \  $  / ",
                        6: "  '---'  ",
                    },
                    "description": "50/50 for 2.5k",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: 0,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda:  2500 if random.randint(0,100) > 50 else 1,
                },
                "Legendary Shekel Lord": {
                    "art": {
                        1: "  ┌───┐  ",
                        2: "┌─┴───┴─┐",
                        3: "│ □ □ □ │",
                        4: "└───────┘",
                        5: "  \()/(§)",
                        6: "   ||    ",
                    },
                    "description": "fuck this guy in particular",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(4,6),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(100,1000),
                },
                "Untainted Troll": {
                    "art": {
                        1: "  ___  _ ",
                        2: " (o_o/ / ",
                        3: " /| / /  ",
                        4: " \}/ /{> ",
                        5: "  /_/\   ",
                        6: " '    '  ",
                    },
                    "description": "Lookout, this guy is straight edge",
                    "health": lambda: 8,
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(2,4),
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(100,1000),
                },
                "Heeeyyy fellaaaas": {
                    "art": {
                        1: "/ Heeeey ",
                        2: "| Fellaas",
                        3: " ,.''.,, ",
                        4: "(  ♦ ♦  )",
                        5: " | ╯┺╰ | ",
                        6: " \ (_) / ",
                    },
                    "description": "daading",
                    "health": lambda: random.randint(4,7),
                    "attack": lambda: random.randint(7,9),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 2 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(500,1000),
                },
                "Max Max Mangles": {
                    "art": {
                        1: "  META   ",
                        2: "  SLAVE  ",
                        3: " ,.''.,, ",
                        4: "(  ♦ ♦  )",
                        5: " | ╯┺╰ | ",
                        6: " \ '‾' / ",
                    },
                    "description": "doing things 'right' is fucking boring",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(600,1200),
                },
                "Never Lucky": {
                    "art": {
                        1: "  ___ | ●",
                        2: " |●●●| ¯¯",
                        3: "  ¯¯¯ ___",
                        4: " ___ | ● ",
                        5: "| ● | ¯¯¯",
                        6: " ¯¯¯  :( ",
                    },
                    "description": "It's all dc15 d20 rolls, GL. (Highest Potential in the game)",
                    "health": lambda: random.randint(1,20),
                    "attack": lambda: random.randint(1,20),
                    "armor": lambda: 2 if random.randint(0,20) > 15 else 0,
                    "barrier": lambda: 2 if random.randint(0,20) > 15 else 0,
                    "value": lambda: 20000 if random.randint(0,20) > 15 else 0,
                },
                "Dave's Premature Refund": {
                    "art": {
                        1: "   :/    ",
                        2: " Yeah    ",
                        3: " Nah     ",
                        4: " Refunded",
                        5: " Already ",
                        6: "   :|    ",
                    },
                    "description": "below average",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(1,500),
                },
                "250k bonus": {
                    "art": {
                        1: "HA HA HA ",
                        2: "NOT REAL ",
                        3: "  :^)    ",
                        4: " IT IS   ",
                        5: "ACTUALLY ",
                        6: "$1million",
                    },
                    "description": "it isn't",
                    "health": lambda: random.randint(1,2),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: 2,
                    "value": lambda: random.randint(100,2500),
                },
                "Immaculate Imp": {
                    "art": {
                        1: "  / ║ \  ",
                        2: " / ═╬═ \ ",
                        3: "( ☼╲ ╱☼ )",
                        4: " \ ◄▬► / ",
                        5: "  \___/  ",
                        6: " /    '\ ",
                    },
                    "description": "well here we are 141 cards in",
                    "health": lambda: random.randint(5,9),
                    "attack": lambda: random.randint(3,6),
                    "armor": lambda: 0,
                    "barrier": lambda: 3 if random.randint(0,100) > 66 else 0,
                    "value": lambda: random.randint(100,1000),
                },
                "Impeccable Imp": {
                    "art": {
                        1: "  / ║ \  ",
                        2: " / ═╬═ \ ",
                        3: "( ☼╲ ╱☼ )",
                        4: " \ ▼▾▼ / ",
                        5: "  \___/  ",
                        6: " /    '\ ",
                    },
                    "description": "I'm running out of ideas here",
                    "health": lambda: random.randint(3,6),
                    "attack": lambda: random.randint(5,9),
                    "armor": lambda: 0,
                    "barrier": lambda: 3 if random.randint(0,100) > 75 else 1,
                    "value": lambda: random.randint(100,1000),
                },
                "Chris in a Calculator": {
                    "art": {
                        1: "   +1    ",
                        2: " [ CHRIS]",
                        3: " [][][][]",
                        4: " [][][][]",
                        5: " [][][][]",
                        6: "         ",
                    },
                    "description": "Sounds like it",
                    "health": lambda: random.randint(4,8),
                    "attack": lambda: random.randint(5,9),
                    "armor": lambda: 2,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(100,1000),
                },
                "I buy experiences!": {
                    "art": {
                        1: "    I    ",
                        2: "( ಠ ͜ʖ ರೃ)",
                        3: "   BUY   ",
                        4: "( ಠ ͜ʖ ರೃ)",
                        5: "EXPER    ",
                        6: "   IENCES",
                    },
                    "description": "I said I prefer them",
                    "health": lambda: random.randint(3,6),
                    "attack": lambda: random.randint(2,6),
                    "armor": lambda: random.randint(0,1),
                    "barrier": lambda: 2,
                    "value": lambda: random.randint(1,5000),
                },
                "Daves 'Guild'": {
                    "art": {
                        1: "|       |",
                        2: "\       /",
                        3: " ∋)╭╮(∈ /",
                        4: "_∋)╰╯(∈_|",
                        5: "   /*\   ",
                        6: "  /╰╧╯\  ",
                    },
                    "description": "Everything fits in there",
                    "health": lambda: 10,
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(2,4),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(100,1000),
                },
                "TomSmells": {
                    "art": {
                        1: " Tom    ~",
                        2: "Smells ~ ",
                        3: "   ()  ~ ",
                        4: "  /||\  ~",
                        5: "   /\ ╭∩╮",
                        6: "     ╭ʖ╮ ",
                    },
                    "description": "Unoriginal, yet endearing",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(100,2000),
                },
                "Divine Orb": {
                    "art": {
                        1: "$$  ____*",
                        2: "  */u  u|",
                        3: " /  ▲ * |",
                        4: "*| --  / ",
                        5: " \____/ *",
                        6: "    *  $$",
                    },
                    "description": "It used to be worth less",
                    "health": lambda: 1,
                    "attack": lambda: 1,
                    "armor": lambda: 1,
                    "barrier": lambda: 1,
                    "value": lambda: 2500,
                },
                "Top 100 Nestor": {
                    "art": {
                        1: " Top 100 ",
                        2: "♨(ಠ_ಠ)m  ",
                        3: "    _____",
                        4: ".--/ ϭ  /",
                        5: " \/____/ ",
                        6: "         ",
                    },
                    "description": "6-8k mmr ez",
                    "health": lambda: random.randint(8,12),
                    "attack": lambda: random.randint(8,12),
                    "armor": lambda: random.randint(0,2),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(1000,2000),
                },
                "Want it and Not Want it": {
                    "art": {
                        1: "▓MEH▓/  /",
                        2: "▓▓▓▓/  /░",
                        3: "▓▓▓/  /░░",
                        4: "▓▓/  /░░░",
                        5: "▓/  /░░░░",
                        6: "/  /░PLS░",
                    },
                    "description": "You've just got to do both",
                    "health": lambda: random.randint(5,8),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 0,
                    "value": lambda: random.randint(500,1000),
                },
                "The One True Liberal": {
                    "art": {
                        1: "!?!?!?!/ ",
                        2: "  (  )/  ",
                        3: " /|   |  ",
                        4: "/ | ==[++",
                        5: "  | ) )  ",
                        6: " / / \ \ ",
                    },
                    "description": "Always, until he isn't",
                    "health": lambda: random.randint(6,10),
                    "attack": lambda: random.randint(3,9),
                    "armor": lambda: 0,
                    "barrier": lambda: 1 if random.randint(0,100) > 80 else 0,
                    "value": lambda: random.randint(1,2000),
                },
                "Ascended Shitty Wizard": {
                    "art": {
                        1: "  /\  ~  ",
                        2: "_/  \_   ",
                        3: "(-━ᶗ━) * ",
                        4: " /**\╭/  ",
                        5: "/****\  ~",
                        6: " |  | ╭∩╮",
                    },
                    "description": "Um actually- he was shitty, he is now a master",
                    "health": lambda: random.randint(2,6),
                    "attack": lambda: random.randint(5,12),
                    "armor": lambda: 0,
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(100,1000),
                },
            },
            "legendary": {
                "Toms Mirror Stash": {
                    "art": {
                        1: "    ___  ",
                        2: "   /o *\ ",
                        3: "T {* ∞ o}",
                        4: "O  \* o/ ",
                        5: "M   ˘˘˘  ",
                        6: "STASH    ",
                    },
                    "description": "If you don't roll you cannot succeed",
                    "health": lambda: random.randint(1,15),
                    "attack": lambda: random.randint(1,10),
                    "armor": lambda: random.randint(0,3),
                    "barrier": lambda: 1,
                    "value": lambda: random.randint(50000,250000),
                },
                "Tim's D&D Campaigns": {
                    "art": {
                        1: "Tims     ",
                        2: "   _____,",
                        3: "  / 5e //",
                        4: " /____// ",
                        5: "(____(/  ",
                        6: "   Dreams",
                    },
                    "description": "Don't @ me about this shit, it'll never happen :(",
                    "health": lambda: random.randint(10,30),
                    "attack": lambda: 5,
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: random.randint(1,2),
                    "value": lambda: random.randint(5000,10000),
                },
                "Spirit of the lap": {
                    "art": {
                        1: "    __   ",
                        2: " __/  \_ ",
                        3: "'-0---0-'",
                        4: "  ╭‼╮aah!",
                        5: "ꞈ/▐█▌\,  ",
                        6: " _/▀\_   ",
                    },
                    "description": "You'll feel it if you've gone far enough",
                    "health": lambda: random.randint(5,7),
                    "attack": lambda: random.randint(2,4),
                    "armor": lambda: 0,
                    "barrier": lambda: random.randint(3,6),
                    "value": lambda: random.randint(5000,25000),
                },
                "Dave's Pinny Money": {
                    "art": {
                        1: "║  $$$  ║",
                        2: "║=======║",
                        3: "║ooo-,,╗║",
                        4: "║    |\║║",
                        5: "║|_  _|║║",
                        6: "╚══╩╩══╩╝",
                    },
                    "description": "What could a banana cost? $10?",
                    "health": lambda: random.randint(5,10),
                    "attack": lambda: random.randint(5,10),
                    "armor": lambda: random.randint(1,2),
                    "barrier": lambda: 1 if random.randint(0,100) > 66 else 0,
                    "value": lambda: random.randint(15000,25000),
                },
                "Machiavellian Mangles": {
                    "art": {
                        1: " ,.''.,, ",
                        2: "( ◣\/◢ ) ",
                        3: " |  ┺  | ",
                        4: " \ ▼▼▼ / ",
                        5: "║ ΔΔΔΔΔ ║",
                        6: "╚3▒▒▒▒▒Ɛ╝",
                    },
                    "description": "Vice president, surely not! (Has plot armor)",
                    "health": lambda: random.randint(8,12),
                    "attack": lambda: random.randint(4,8),
                    "armor": lambda: random.randint(3,5),
                    "barrier": lambda: random.randint(1,4),
                    "value": lambda: random.randint(10000,50000),
                }
            }
        }

    def _roll_stat(self, stat_generator_function):
        """
        Rolls a single stat by calling the provided stat generation function.
        """
        if callable(stat_generator_function):
            return stat_generator_function()
        return stat_generator_function

    def get_card_instance(self, rarity, card_name):
        """
        Generates a new instance of a Card class with randomly rolled stats
        based on its template. Each call produces a new set of random stats.

        Args:
            category (str): The category of the card (e.g., "common", "rare").
            card_name (str): The name of the specific card.

        Returns:
            Card: A Card object representing the card instance with rolled stats,
                  or None if the card/category is not found.
        """
        if rarity not in self.card_data_templates:
            print(f"Error: Category '{rarity}' not found.")
            return None
        if card_name not in self.card_data_templates[rarity]:
            print(f"Error: Card '{card_name}' not found in category '{rarity}'.")
            return None

        template = self.card_data_templates[rarity][card_name]
        
        try:
            # Roll all stats by calling their respective functions
            rolled_health = self._roll_stat(template["health"])
            rolled_attack = self._roll_stat(template["attack"])
            rolled_armor = self._roll_stat(template["armor"])
            rolled_barrier = self._roll_stat(template["barrier"])
            rolled_value = self._roll_stat(template["value"])

            # Create and return a Card instance
            card_instance = Card(
                name=card_name,
                rarity=rarity,
                art=template.get("art", {}),
                description=template.get("description", ""),
                health=rolled_health,
                attack=rolled_attack,
                armor=rolled_armor,
                barrier=rolled_barrier,
                value=rolled_value
            )
            return card_instance
        except KeyError as e:
            print(f"Error: Failed to create card instance for '{card_name}' in category '{rarity}'. Missing key: {e}")
            return None
        except Exception as e:
            print(f"Error: Failed to create card instance for '{card_name}' in category '{rarity}'. Unexpected error: {e}")
            return None

def calculate_average_card_values(num_rolls_per_card=100):
    """
    Calculates the average 'value' for each card across all categories
    after simulating a set number of rolls for each card.

    Args:
        num_rolls_per_card (int): The number of times to generate stats for each card
                                  to calculate its average value.

    Returns:
        dict: A nested dictionary where keys are categories, and values are
              dictionaries of card names to their average 'value'.
    """
    card_db = CardDatabase()
    
    category_averages = {}

    # Iterate through each category defined in the card templates
    for category, cards_in_category in card_db.card_data_templates.items():
        category_averages[category] = {}
        # Iterate through each card within the current category
        for card_name in cards_in_category:
            total_value = 0
            # Perform the specified number of rolls for the current card
            for _ in range(num_rolls_per_card):
                card_instance = card_db.get_card_instance(category, card_name)
                if card_instance:
                    total_value += card_instance.value # Access value from Card object
            
            # Calculate the average value for the card
            if num_rolls_per_card > 0:
                average_value = total_value / num_rolls_per_card
                category_averages[category][card_name] = average_value
            else:
                # Handle the case where num_rolls_per_card is 0 to avoid division by zero
                category_averages[category][card_name] = 0

    return category_averages

# TESTS
if __name__ == "__main__":
    # Define the number of rolls to perform for each card
    rolls_per_card = 1000
    print(f"Calculating average card values based on {rolls_per_card} rolls per card...")

    # Calculate the averages
    averages = calculate_average_card_values(rolls_per_card)

    # Print the detailed average values for each card
    print("\n--- Average Card Values per Card ---")
    for category, cards_data in averages.items():
        print(f"\nCategory: {category.capitalize()}")
        if cards_data:
            for card_name, avg_value in cards_data.items():
                print(f"  {card_name}: Average Value = {avg_value:.2f}")
        else:
            print(f"  No cards found in {category} category.")

    # Print the overall average value for each category
    print("\n--- Overall Average Value per Category ---")
    for category, cards_data in averages.items():
        if cards_data:
            # Calculate the average of all card averages within the category
            overall_category_avg = sum(cards_data.values()) / len(cards_data)
            print(f"  {category.capitalize()} Category Average: {overall_category_avg:.2f}")
        else:
            print(f"  {category.capitalize()} Category Average: No cards to average.")

    # Example of instantiating a Card and CardDeck:
    print("\n--- Example Card and Deck Usage ---")
    card_db_example = CardDatabase()
    
    example_rarity = random.choice(list(card_db_example.card_data_templates.keys()))
    example_card = random.choice(list(card_db_example.card_data_templates[example_rarity].keys()))
    # Get a single card instance
    my_card = card_db_example.get_card_instance(example_rarity, example_card)
    if my_card:
        my_card.display()

    # Create a deck and add some cards
    my_deck = CardDeck()
    for _ in range(5): # Add 5 random common cards to the deck
        card = card_db_example.get_card_instance(example_rarity, example_card)
        if card:
            my_deck.add_card(card)
    
    print(f"\nDeck has {len(my_deck)} cards.")
    print(f"Total value of cards in deck: {my_deck.get_total_value()}")
    print(f"Average value of cards in deck: {my_deck.get_average_value():.2f}")
