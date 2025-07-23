import random
from .card_template_data import CARD_DATA_TEMPLATES

class Stat:
    def __init__(self, value, min_val, max_val):
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

    def get_perfection(self):
        if self.max_val == self.min_val:
            return 1.0
        return (self.value - self.min_val) / (self.max_val - self.min_val)

    def __str__(self):
        return str(self.value)

    def to_dict(self):
        return {'value': self.value, 'min_val': self.min_val, 'max_val': self.max_val}

    @classmethod
    def from_dict(cls, data):
        return cls(data['value'], data['min_val'], data['max_val'])

class Card:
    """
    Represents an instantiated card with its rolled stats.
    """
    RARITY_ICONS = {
        'common': ':white_circle:',
        'uncommon': ':green_circle:',
        'rare': ':blue_circle:',
        'mythic': ':purple_circle:',
        'legendary': ':orange_circle:'
    },
    ANSI_STYLES = {
        "default": "\033[0m",
        "gray": "\033[30m", 
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "pink": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    RARITY_ANSI_COLORS = {
        'common': ANSI_STYLES["default"],
        'uncommon': ANSI_STYLES["green"],
        'rare': ANSI_STYLES["blue"],
        'mythic': ANSI_STYLES["pink"],
        'legendary': ANSI_STYLES["red"],
    }

    def __init__(self, name, rarity, number, art, description, health, attack, armor, barrier, value):
        self.normal_frame = {
            "top": "┌─────────┐", 
            "mid": "│{art}│", 
            "bottom": "└─────────┘"}
        self.holo_frame = {
            "top": f"{self.RARITY_ANSI_COLORS.get(rarity)}┏━━*****━━┓{self.ANSI_STYLES.get('default')}", 
            "mid": self.RARITY_ANSI_COLORS.get(rarity)+"┃"+self.ANSI_STYLES.get('default')+"{art}"+self.RARITY_ANSI_COLORS.get(rarity)+"┃"+self.ANSI_STYLES.get('default'),
            "bottom": f"{self.RARITY_ANSI_COLORS.get(rarity)}┗━━*****━━┛{self.ANSI_STYLES.get('default')}"
            }
        self.name = name
        self.number = number
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
        self.check_and_set_holo()

    def check_and_set_holo(self):
        if self.get_perfection() >= 0.95:
            self.set_holo(True)

    def get_perfection(self):
        stats_to_average = [self.health, self.attack, self.armor, self.barrier]
        perfection_sum = sum(stat.get_perfection() for stat in stats_to_average)
        return perfection_sum / len(stats_to_average)

    def get_name(self):
        return self.name

    def get_ansi_name(self):
        return f"{self.RARITY_ANSI_COLORS.get(self.rarity)}{self.name}{self.ANSI_STYLES.get('default')}"
    
    def get_ansi_rarity(self):
        return f"{self.RARITY_ANSI_COLORS.get(self.rarity)}{self.rarity.capitalize()}{self.ANSI_STYLES.get('default')}"


    def display(self):
        """
        Prints the card's ASCII art and stats.
        """
        display_lines = []
        name_display = f"*{self.name}*" if self.is_holo else self.name
        display_lines.append(f"\n--- {name_display} ({self.rarity.capitalize()}) [{self.get_perfection():.2%}] ---")
        for line in self.get_display_art():
            display_lines.append(line)
        card_template = CARD_DATA_TEMPLATES[self.rarity][self.name]
        display_lines.append(f"Desc    : {self.description}")
        display_lines.append(f"Health  : {self.health}/{card_template['health_range'][1]}")
        display_lines.append(f"Attack  : {self.attack}/{card_template['attack_range'][1]}")
        if card_template['armor_range'][1] > 0:
            display_lines.append(f"Armor   : {self.armor}/{card_template['armor_range'][1]}")
        if card_template['barrier_range'][1] > 0:
            display_lines.append(f"Barrier : {self.barrier}/{card_template['barrier_range'][1]}")
        display_lines.append(f"Value   : {self.value}/{card_template['value_range'][1]}")
        return display_lines


    def set_frame(self, frame):
        self.frame = frame

    def set_holo(self, is_holo):
        self.is_holo = is_holo
        if self.is_holo:
            self.set_frame(self.holo_frame)
        else:
            self.set_frame(self.normal_frame)

    def get_display_art(self):
        """Returns the card's art formatted with its frame"""
        if not self.frame:
            return self.art
            
        display = []
        display.append(self.frame["top"])
        for line in self.art.values():
            display.append(f'{self.frame["mid"].format(art=line)}')
        display.append(self.frame["bottom"])
        return display

    def get_brief(self):
        """Returns a brief one-line description of the card."""
        rarity_icon = self.RARITY_ICONS.get(self.rarity, '')
        name_display = f"*{self.name}*" if self.is_holo else self.name
        return f"{rarity_icon} {name_display} ({self.attack}atk/{self.health}hp/{self.armor}a/{self.barrier}b) ${self.value} [{self.get_perfection():.2%}]"
    
    def get_value(self): 
        return float(self.value.value)

    def to_dict(self):
        """
        Serializes the card object to a dictionary.
        """
        return {
            'name': self.name,
            'rarity': self.rarity,
            'art': self.art,
            'description': self.description,
            'health': self.health.to_dict(),
            'attack': self.attack.to_dict(),
            'armor': self.armor.to_dict(),
            'barrier': self.barrier.to_dict(),
            'value': self.value.to_dict(),
            'is_holo': self.is_holo,
            'cannot_be_sold': self.cannot_be_sold
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Card instance from a dictionary.
        """
        card = cls(
            name=data['name'],
            rarity=data['rarity'],
            art=data['art'],
            description=data['description'],
            health=Stat.from_dict(data['health']),
            attack=Stat.from_dict(data['attack']),
            armor=Stat.from_dict(data['armor']),
            barrier=Stat.from_dict(data['barrier']),
            value=Stat.from_dict(data['value'])
        )
        card.set_holo(data.get('is_holo', False))
        # cannot_be_sold can be set here if needed
        return card

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
        return sum(card.get_value() for card in self.cards)

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
    def __init__(self, card_templates):

        self.special_cards = {} # Placeholder for special cards as per original class
        self.card_data = {}
        self.generate_card_data(card_templates)


    def _create_stat(self, template, stat_name):
        min_val, max_val = template[f'{stat_name}_range']
        value = template[stat_name]()
        return Stat(value, min_val, max_val)

    def create_card_instance(self, rarity, name):
        """
        Creates a Card instance from a template, rolling for stats.
        """
        template = self.card_data[rarity][name]
        return Card(
            name=name,
            rarity=rarity,
            number=template['card_number'],
            art=template['art'],
            description=template['description'],
            health=self._create_stat(template, 'health'),
            attack=self._create_stat(template, 'attack'),
            armor=self._create_stat(template, 'armor'),
            barrier=self._create_stat(template, 'barrier'),
            value=self._create_stat(template, 'value')
        )

    def get_random_card(self, rarity):
        # A card could be in multiple rarities, so we need to handle that.
        if rarity not in self.card_data:
            return None
        card_name = random.choice(list(self.card_data[rarity].keys()))
        return self.create_card_instance(rarity, card_name)

    def generate_card_data(self, card_templates):

        """
        Defines the templates for all cards, including their stat generation functions and ASCII art.
        Each stat (health, attack, armor, barrier, value) is now a function that returns a value.
        """
        self.card_data = card_templates

    def get_card_data_by_name(self, rarity, name):
        return self.card_data[rarity][name]


class CardPack:
    def __init__(self, card_db: CardDatabase):
        self.card_db = card_db
        self.CARDS_PER_PACK = 10
        self.NINTH_CARD_RARE_CHANCE = 0.1  # 1/10
        self.RARE_PLUS_CHANCES = {
            'rare': 0.9475,
            'mythic': 0.05,
            'legendary': 0.0025
        }

    def _roll_rare_plus(self):
        rarities = list(self.RARE_PLUS_CHANCES.keys())
        chances = list(self.RARE_PLUS_CHANCES.values())
        # Ensure that the rarity chosen has cards defined
        while True:
            chosen_rarity = random.choices(rarities, weights=chances, k=1)[0]
            if self.card_db.card_data.get(chosen_rarity):
                return self.card_db.get_random_card(chosen_rarity)

    def open(self):
        pack = []
        # 8 common/uncommon cards
        for _ in range(8):
            rarity = random.choice(['common', 'uncommon'])
            pack.append(self.card_db.get_random_card(rarity))

        # 9th card
        if random.random() < self.NINTH_CARD_RARE_CHANCE:
            pack.append(self._roll_rare_plus())
        else:
            rarity = random.choice(['common', 'uncommon'])
            pack.append(self.card_db.get_random_card(rarity))

        # 10th card (guaranteed rare+)
        pack.append(self._roll_rare_plus())
        return pack
