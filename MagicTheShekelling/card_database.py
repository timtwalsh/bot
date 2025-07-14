import random

class CardDatabase:
    def __init__(self):
        self.special_cards = {}
        
    def generate_cards_database(self):
        """Generate all 151 cards with their stats and ASCII art"""
        cards = {}
        
        # Special cards dictionary
        self.special_cards = {
            'ULTRA_LEGENDARY': {
                'name': 'The Ultimate Shekel Master',
                'rarity': 'Ultra Legendary',
                'power': '∞',
                'toughness': '∞',
                'description': 'The ultimate card of infinite wealth',
                'ascii_art': "    ♦♦♦♦♦    \n   ♦     ♦   \n  ♦  $$  ♦  \n   ♦     ♦   \n    ♦♦♦♦♦    ",
                'sell_min': 15000,
                'sell_max': 20000
            },
            'TOMS_MIRROR': {
                'name': "Tom's Mirror",
                'rarity': 'Ultra Mythic',
                'power': '∞',
                'toughness': '∞',
                'description': 'The reflection of infinite wealth',
                'ascii_art': "   ╔═══════════════╗   \n  ╔╝ ✨ TOM'S MIRROR ✨ ╚╗  \n ╔╝ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ╚╗ \n╔╝ ♦ ╔═══════════╗ ♦ ╚╗\n║ ♦ ║  $ YOU $  ║ ♦ ║\n║ ♦ ║ $ REFLECT $ ║ ♦ ║\n║ ♦ ║  $ ALL $  ║ ♦ ║\n╚╗ ♦ ╚═══════════╝ ♦ ╔╝\n ╚╗ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ╔╝ \n  ╚╗ ✨ INFINITE ✨ ╔╝  \n   ╚═══════════════╝   ",
                'sell_min': 12000,
                'sell_max': 15000
            },
            'ULTRA_RARE_5K': {
                'name': 'Golden Shekel Dragon',
                'rarity': 'Ultra Rare',
                'power': 15,
                'toughness': 15,
                'description': 'A dragon made of pure shekels',
                'ascii_art': "    ★★★★★    \n   ★     ★   \n  ★  $$  ★  \n   ★     ★   \n    ★★★★★    ",
                'sell_min': 4000,
                'sell_max': 5000
            },
            'ULTRA_RARE_1K': {
                'name': 'Crystal Coin Guardian',
                'rarity': 'Ultra Rare',
                'power': 10,
                'toughness': 10,
                'description': 'Guardian of the crystal vault',
                'ascii_art': "    ◆◆◆◆◆    \n   ◆     ◆   \n  ◆  $$  ◆  \n   ◆     ◆   \n    ◆◆◆◆◆    ",
                'sell_min': 800,
                'sell_max': 1000
            },
            'RARE_500': {
                'name': 'Vault Master',
                'rarity': 'Premium Rare',
                'power': 8,
                'toughness': 8,
                'description': 'Master of the shekel vaults',
                'ascii_art': "   ▲▲▲▲▲   \n  ▲  $  ▲  \n   ▲▲▲▲▲   ",
                'sell_min': 400,
                'sell_max': 500
            },
            'RARE_300': {
                'name': 'Treasure Keeper',
                'rarity': 'High Value Rare',
                'power': 7,
                'toughness': 7,
                'description': 'Keeper of ancient treasures',
                'ascii_art': "   ●●●●●   \n  ●  $  ●  \n   ●●●●●   ",
                'sell_min': 250,
                'sell_max': 300
            },
            'RARE_200': {
                'name': 'Coin Collector',
                'rarity': 'Valuable Rare',
                'power': 6,
                'toughness': 6,
                'description': 'Collector of rare coins',
                'ascii_art': "   ■■■■■   \n  ■  $  ■  \n   ■■■■■   ",
                'sell_min': 150,
                'sell_max': 200
            }
        }
        
        # Common cards (1-64)
        common_names = [
            "Shekel Goblin", "Penny Pincher", "Copper Coin", "Budget Warrior", "Frugal Mage",
            "Thrift Store Knight", "Bargain Hunter", "Discount Demon", "Cheap Shot", "Sale Specter",
            "Clearance Cleric", "Markdown Monk", "Coupon Collector", "Scrooge Spirit", "Miser Mouse",
            "Wallet Warden", "Piggy Bank", "Spare Change", "Loose Coin", "Empty Purse",
            "Broke Bard", "Pauper Paladin", "Destitute Dragon", "Bankrupt Beast", "Poor Peasant",
            "Humble Hobbit", "Modest Mage", "Simple Soldier", "Basic Berserker", "Plain Paladin",
            "Common Conjurer", "Ordinary Orc", "Regular Rogue", "Standard Slime", "Typical Troll",
            "Average Archer", "Normal Necromancer", "Usual Unicorn", "Everyday Elf", "Mundane Minotaur",
            "Generic Gnome", "Default Dwarf", "Standard Sphinx", "Common Centaur", "Basic Basilisk",
            "Ordinary Ogre", "Regular Rat", "Simple Serpent", "Plain Phoenix", "Common Crow",
            "Basic Bat", "Standard Spider", "Typical Tiger", "Average Ant", "Normal Newt",
            "Usual Unicorn", "Everyday Eagle", "Mundane Mantis", "Generic Gecko", "Default Deer",
            "Standard Stag", "Common Cat", "Basic Bear", "Regular Rabbit", "Simple Shark"
        ]
        
        # Uncommon cards (65-96)
        uncommon_names = [
            "Silver Shekel", "Gold Grabber", "Treasure Troll", "Coin Collector", "Wealth Wizard",
            "Rich Rogue", "Prosperous Paladin", "Affluent Archer", "Loaded Lancer", "Moneyed Mage",
            "Wealthy Warrior", "Fortunate Fighter", "Lucky Looter", "Blessed Banker", "Divine Depositor",
            "Sacred Saver", "Holy Hoarder", "Blessed Buyer", "Charmed Collector", "Enchanted Economist",
            "Magical Merchant", "Mystical Miser", "Arcane Accountant", "Ethereal Exchanger", "Spectral Spender",
            "Ghostly Gambler", "Phantom Purchaser", "Wraith Wallet", "Spirit Saver", "Astral Auctioneer",
            "Cosmic Collector", "Stellar Spender"
        ]
        
        # Rare cards (97-126)
        rare_names = [
            "Diamond Dealer", "Platinum Purse", "Emerald Emperor", "Ruby Regent", "Sapphire Sultan",
            "Crystal Crusher", "Gem Guardian", "Jewel Juggernaut", "Precious Protector", "Valuable Valkyrie",
            "Expensive Executioner", "Costly Crusader", "Pricey Paladin", "Lavish Lancer", "Sumptuous Sorcerer",
            "Opulent Oracle", "Luxurious Lich", "Extravagant Elemental", "Deluxe Demon", "Premium Phoenix",
            "Elite Enchanter", "Shitty Wizard", "Magnificent Minotaur", "Glorious Griffin", "Majestic Manticore",
            "Regal Roc", "Imperial Imp", "Royal Reaper", "Noble Nightmare", "Aristocratic Angel"
        ]
        
        # Mythic cards (127-151)
        mythic_names = [
            "Legendary Shekel Lord", "Mythical Moneybags", "Epic Economy", "Fabled Fortune", "Legendary Loot",
            "Transcendent Treasurer", "Omnipotent Oligarch", "Divine Dollar", "Celestial Coin", "Heavenly Hoard",
            "Godly Gold", "Almighty Assets", "Supreme Shekel", "Ultimate Unicorn", "Perfect Phoenix",
            "Flawless Fighter", "Immaculate Imp", "Pristine Paladin", "Spotless Sphinx", "Unblemished Unicorn",
            "Faultless Fighter", "Impeccable Imp", "Untainted Troll", "Pure Paladin", "Clean Crusher"
        ]
        
        card_id = 1
        
        # Generate Common cards (64 cards)
        for i in range(64):
            name = common_names[i % len(common_names)]
            if i >= len(common_names):
                name += f" {i // len(common_names) + 1}"
            
            cards[card_id] = {
                'name': name,
                'rarity': 'Common',
                'power': random.randint(1, 3),
                'toughness': random.randint(1, 3),
                'description': f"A humble {name.lower()} seeking shekels.",
                'ascii_art': self.generate_ascii_art('common', name),
                'sell_min': 1,
                'sell_max': 10
            }
            card_id += 1
        
        # Generate Uncommon cards (32 cards)
        for i in range(32):
            name = uncommon_names[i % len(uncommon_names)]
            if i >= len(uncommon_names):
                name += f" {i // len(uncommon_names) + 1}"
                
            cards[card_id] = {
                'name': name,
                'rarity': 'Uncommon',
                'power': random.randint(2, 5),
                'toughness': random.randint(2, 5),
                'description': f"An uncommon {name.lower()} with moderate power.",
                'ascii_art': self.generate_ascii_art('uncommon', name),
                'sell_min': 5,
                'sell_max': 20
            }
            card_id += 1
        
        # Generate Rare cards (30 cards)
        for i in range(30):
            name = rare_names[i % len(rare_names)]
            if i >= len(rare_names):
                name += f" {i // len(rare_names) + 1}"
                
            cards[card_id] = {
                'name': name,
                'rarity': 'Rare',
                'power': random.randint(4, 8),
                'toughness': random.randint(4, 8),
                'description': f"A rare and powerful {name.lower()}.",
                'ascii_art': self.generate_ascii_art('rare', name),
                'sell_min': 10,
                'sell_max': 40
            }
            card_id += 1
        
        # Generate Mythic cards (25 cards)
        for i in range(25):
            name = mythic_names[i % len(mythic_names)]
            if i >= len(mythic_names):
                name += f" {i // len(mythic_names) + 1}"
                
            cards[card_id] = {
                'name': name,
                'rarity': 'Mythic',
                'power': random.randint(6, 12),
                'toughness': random.randint(6, 12),
                'description': f"A mythical {name.lower()} of immense power.",
                'ascii_art': self.generate_ascii_art('mythic', name),
                'sell_min': 20,
                'sell_max': 60
            }
            card_id += 1
        
        return cards
    
    def get_card_type(self, card_name):
        """Determine card type from name for themed ASCII art"""
        name_lower = card_name.lower()
        
        if 'goblin' in name_lower:
            return 'goblin'
        elif 'demon' in name_lower:
            return 'demon'
        elif 'hunter' in name_lower or 'grabber' in name_lower:
            return 'hunter'
        elif 'warrior' in name_lower or 'knight' in name_lower or 'fighter' in name_lower:
            return 'warrior'
        elif 'mage' in name_lower or 'wizard' in name_lower or 'sorcerer' in name_lower or 'enchanter' in name_lower:
            return 'mage'
        elif 'silver' in name_lower or 'gold' in name_lower or 'coin' in name_lower:
            return 'silver'
        elif 'treasure' in name_lower or 'troll' in name_lower:
            return 'treasure'
        elif 'collector' in name_lower:
            return 'collector'
        elif 'diamond' in name_lower or 'gem' in name_lower or 'jewel' in name_lower:
            return 'diamond'
        elif 'emperor' in name_lower or 'sultan' in name_lower or 'regent' in name_lower:
            return 'emperor'
        elif 'crystal' in name_lower:
            return 'crystal'
        elif 'guardian' in name_lower or 'protector' in name_lower:
            return 'guardian'
        elif 'legendary' in name_lower:
            return 'legendary'
        elif 'lord' in name_lower:
            return 'lord'
        elif 'shitty' in name_lower:
            return 'shitty'
        elif 'divine' in name_lower or 'godly' in name_lower or 'celestial' in name_lower or 'heavenly' in name_lower:
            return 'divine'
        elif 'perfect' in name_lower or 'flawless' in name_lower or 'immaculate' in name_lower or 'pristine' in name_lower:
            return 'perfect'
        elif 'omnipotent' in name_lower or 'almighty' in name_lower or 'supreme' in name_lower:
            return 'omnipotent'
        else:
            return 'generic'
    
    def generate_ascii_art(self, rarity, card_name=""):
        """Generate themed ASCII art based on rarity and card type"""
        
        # Determine card type from name
        card_type = self.get_card_type(card_name)
        
        if rarity == 'common':
            arts = {
                'goblin': [
                    "  /\\   \n /oo\\  \n(    ) \n \\__/  \n  \\/   ",
                    " .---.  \n( o o ) \n \\   / \n  '-'  ",
                    "  ^    \n /|\\   \n<ooo>  \n / \\   "
                ],
                'demon': [
                    "  /\\/\\  \n ( >< ) \n  \\/\\/  \n   ||   \n  /__\\  ",
                    " .---.  \n( \\_/ ) \n \\___/ \n   |   ",
                    "  ^^^   \n /   \\  \n( X X ) \n \\___/  "
                ],
                'hunter': [
                    "  /\\   \n /  \\  \n( () ) \n \\__/  \n  ||   ",
                    " .---.  \n( -.- ) \n  ~~~  \n   |   ",
                    "  -->  \n /|\\   \n / \\   \n  ||   "
                ],
                'warrior': [
                    "  [=]   \n /|\\   \n / \\   \n  ||   ",
                    " .---.  \n( |_| ) \n  ^^^  \n   |   ",
                    "  /|\\  \n<-+--> \n / \\   "
                ],
                'mage': [
                    "  *    \n /|\\   \n<~~~>  \n / \\   ",
                    " .---.  \n( @ @ ) \n  ~~~  \n   *   ",
                    "  /\\   \n /*\\   \n(   ) \n \\*/  "
                ],
                'generic': [
                    "  o    \n /|\\   \n / \\   ",
                    " .--.  \n(    ) \n '--'  ",
                    "  /\\   \n /  \\  \n\\  / \n \\/   "
                ]
            }
        elif rarity == 'uncommon':
            arts = {
                'silver': [
                    "  /$\\  \n /$$$\\ \n($$$$$)\n \\$$$/ \n  \\$/  ",
                    " .---. \n( $$$ )\n '---' ",
                    "  $$$  \n /$$$\\ \n\\$$$$$/"
                ],
                'grabber': [
                    "  {^^}  \n {{ }} \n  \\/\\/ \n  ||||  \n  ~~~~  ",
                    " .---. \n( ))) )\n  \\\\\\  \n   |||  ",
                    "  ^^^  \n /|||\\  \n<{{{>  \n \\|||/ "
                ],
                'treasure': [
                    "  /^^^\\ \n |$$$| \n |$$$| \n \\___/ ",
                    " .---. \n|$$$$$|\n '---' ",
                    "  ^^^  \n /$$$\\ \n \\$$$/ "
                ],
                'collector': [
                    "  [@]  \n /|||\\  \n<$$$>  \n \\|/ ",
                    " .---. \n( $$$ )\n  ~~~  \n   @   ",
                    "  $@$  \n /|\\   \n<$$$>  \n / \\   "
                ],
                'generic': [
                    "  @@   \n /||\\  \n / \\   ",
                    " .---. \n(  @  )\n '---' ",
                    "  /\\\\  \n /  \\\\ \n\\  / \n \\/  "
                ]
            }
        elif rarity == 'rare':
            arts = {
                'diamond': [
                    "  /^^^\\  \n/<>  <>\\n|  <>  |\n\\<>  <>/\n \\___/  ",
                    " .^^^^^. \n( <> <> )\n '^^^^^' ",
                    "   <>   \n  /<>\\  \n <> <> \n  \\<>/  "
                ],
                'emperor': [
                    "  /^^^\\  \n |   | \n | W | \n |___| \n  ^^^  ",
                    " .^^^. \n( ### )\n '^^^' ",
                    "  ###  \n /^^^\\  \n<  W  > \n \\___/ "
                ],
                'crystal': [
                    "   /\\   \n  /  \\  \n /####\\ \n \\####/ \n  \\  /  \n   \\/   ",
                    " .####. \n(######)\n '####' ",
                    "  ####  \n /####\\  \n \\####/ "
                ],
                'guardian': [
                    "  /^^^\\  \n |[ ]| \n |^^^| \n |___| \n  |||  ",
                    " .^^^. \n( [#] )\n '^^^' ",
                    "  [#]  \n /^^^\\  \n<[#]>  \n \\___/ "
                ],
                'generic': [
                    "  ###  \n /###\\  \n \\###/ ",
                    " .---. \n( ### )\n '---' ",
                    "  /^^^\\  \n /   \\ \n\\   /\n \\___/ "
                ],
                'shitty' : [
                    "  /^^^\\  \n |[ ]| \n |^^^| \n |___| \n  |||  ",
                    "  .^^^.  \n ( [#] ) \n  '^^^'  ",
                    "  [#]  \n /^^^\\  \n<[#]>  \n \\___/ "
                ],
            }
        else:  # mythic
            arts = {
                'legendary': [
                    "       ★★★★★★★       \n     ★*  $$$  *★     \n   ★* /$$$$$$$\\ *★   \n  ★ |$$$  $  $$$| ★  \n ★  |$  $$$$$  $|  ★ \n ★  |$$$  $  $$$|  ★ \n  ★ |  $$$$$$$  | ★  \n   ★* \\$$$$$$$/ *★   \n     ★*  $$$  *★     \n       ★★★★★★★       ",
                    "    ◆◆◆◆◆◆◆◆◆◆◆    \n  ◆◆               ◆◆  \n ◆   $$$ LEGEND $$$   ◆ \n◆    /$$$$$$$$$$$\\    ◆\n◆   /$  $$$$$$$  $\\   ◆\n◆  |$$$  $$$  $$$|   ◆\n◆  |$ $$$ ♦ $$$ $|   ◆\n◆  |$$$  $$$  $$$|   ◆\n◆   \\$  $$$$$$$  $/   ◆\n◆    \\$$$$$$$$$$$$/    ◆\n ◆   $$$ POWER $$$   ◆ \n  ◆◆               ◆◆  \n    ◆◆◆◆◆◆◆◆◆◆◆    ",
                    "   ╔═══════════════╗   \n  ╔╝ ★ LEGENDARY ★ ╚╗  \n ╔╝  $$$$$$$$$$$$$ ╚╗ \n╔╝  $$$ /░░░░░\\ $$$  ╚╗\n║  $$$/ ░░░★░░░ \\$$$  ║\n║ $$$| ░░░░░░░░░ |$$$ ║\n║ $$$| ░░░♦♦♦░░░ |$$$ ║\n║ $$$| ░░░░░░░░░ |$$$ ║\n║  $$$\\ ░░░★░░░ /$$$ ║\n╚╗  $$$ \\░░░░░/ $$$  ╔╝\n ╚╗  $$$$$$$$$$$$$ ╔╝ \n  ╚╗ ★ INFINITE ★ ╔╝  \n   ╚═══════════════╝   "
                ],
                'lord': [
                    "      ♛ SHEKEL LORD ♛      \n    ═══════════════════    \n   ║$$$ ♛ SUPREME ♛ $$$║   \n  ║$$$$$$$$$$$$$$$$$$$║  \n ║$$$ ┌─────────────┐ $$$║ \n║$$$ │ ♦ ♦ ♦ ♦ ♦ ♦ │ $$$║\n║$$$ │ ♦ $$$ W $$$ ♦ │ $$$║\n║$$$ │ ♦ $ POWER $ ♦ │ $$$║\n║$$$ │ ♦ $$$ ♛ $$$ ♦ │ $$$║\n║$$$ │ ♦ ♦ ♦ ♦ ♦ ♦ │ $$$║\n ║$$$ └─────────────┘ $$$║ \n  ║$$$$$$$$$$$$$$$$$$$║  \n   ║$$$ ♛ ETERNAL ♛ $$$║   \n    ═══════════════════    \n      ♛ RULER OF ALL ♛     ",
                    "     ♔♔♔♔♔♔♔♔♔♔♔♔♔     \n   ♔♔$$$$$$$$$$$$$$$♔♔   \n  ♔$$$  ♛ THRONE ♛  $$$♔  \n ♔$$$  ═══════════  $$$♔ \n♔$$$  ║           ║  $$$♔\n♔$$$ ║ ◆◆◆◆◆◆◆◆◆ ║ $$$♔\n♔$$$ ║ ◆$$$♛$$$◆ ║ $$$♔\n♔$$$ ║ ◆$♛$W$♛$◆ ║ $$$♔\n♔$$$ ║ ◆$$$♛$$$◆ ║ $$$♔\n♔$$$ ║ ◆◆◆◆◆◆◆◆◆ ║ $$$♔\n♔$$$  ║           ║  $$$♔\n ♔$$$  ═══════════  $$$♔ \n  ♔$$$  ♛ DOMINION ♛ $$$♔ \n   ♔♔$$$$$$$$$$$$$$$♔♔   \n     ♔♔♔♔♔♔♔♔♔♔♔♔♔     "
                ],
                'divine': [
                    "         ★  ✧  ★         \n       ✧ ★ ♦ ★ ✧       \n     ★ ♦ ◆ ☆ ◆ ♦ ★     \n   ✧ ♦ ◆ ╔═══╗ ◆ ♦ ✧   \n  ★ ◆ ☆ ║ ♦◊♦ ║ ☆ ◆ ★  \n ♦ ◆ ╔══╬═════╬══╗ ◆ ♦ \n ◆ ☆ ║  ║ $$$ ║  ║ ☆ ◆ \n☆ ╔══╬══╬═♦◊♦═╬══╬══╗ ☆\n ◆║  ║$$║ $$$ ║$$║  ║◆ \n ♦║ $║$$║$$$$$║$$║$ ║♦ \n ◆║  ║$$║ $$$ ║$$║  ║◆ \n☆ ╚══╬══╬═♦◊♦═╬══╬══╝ ☆\n ◆ ☆ ║  ║ $$$ ║  ║ ☆ ◆ \n ♦ ◆ ╚══╬═════╬══╝ ◆ ♦ \n  ★ ◆ ☆ ║ ♦◊♦ ║ ☆ ◆ ★  \n   ✧ ♦ ◆ ╚═══╝ ◆ ♦ ✧   \n     ★ ♦ ◆ ☆ ◆ ♦ ★     \n       ✧ ★ ♦ ★ ✧       \n         ★  ✧  ★         ",
                    "    ☀️ CELESTIAL BEING ☀️    \n  ═══════════════════════  \n ║ ☀️ ✧ ★ DIVINE ★ ✧ ☀️ ║ \n║  ★ ♦ ◆ ╔═══════╗ ◆ ♦ ★  ║\n║ ♦ ◆ ☆ ║ ♦♦♦♦♦ ║ ☆ ◆ ♦ ║\n║ ◆ ☆ ♦ ║♦ $$$ ♦║ ♦ ☆ ◆ ║\n║ ☆ ♦ ◆ ║♦ $♦$ ♦║ ◆ ♦ ☆ ║\n║ ♦ ◆ ☆ ║♦ $$$ ♦║ ☆ ◆ ♦ ║\n║ ◆ ☆ ♦ ║ ♦♦♦♦♦ ║ ♦ ☆ ◆ ║\n║  ★ ♦ ◆ ╚═══════╝ ◆ ♦ ★  ║\n ║ ☀️ ✧ ★ POWER ★ ✧ ☀️ ║ \n  ═══════════════════════  \n    ☀️ IMMORTAL FORCE ☀️    "
                ],
                'omnipotent': [
                    "♦♦♦♦♦♦♦ OMNIPOTENT ♦♦♦♦♦♦♦\n♦ ═══════════════════════ ♦\n♦ ║ ★ ◆ ♦ ☆ ♛ ☆ ♦ ◆ ★ ║ ♦\n♦ ║ ◆ ╔═══════════════╗ ◆ ║ ♦\n♦ ║ ♦ ║ $$ MASTER $$ ║ ♦ ║ ♦\n♦ ║ ☆ ║ $ ♦♦♦♦♦♦♦♦♦ $ ║ ☆ ║ ♦\n♦ ║ ♛ ║ $♦ ╔═════╗ ♦$ ║ ♛ ║ ♦\n♦ ║ ☆ ║ $♦ ║ ∞ ∞ ∞ ║ ♦$ ║ ☆ ║ ♦\n♦ ║ ♦ ║ $♦ ║ ∞ ♛ ∞ ║ ♦$ ║ ♦ ║ ♦\n♦ ║ ◆ ║ $♦ ║ ∞ ∞ ∞ ║ ♦$ ║ ◆ ║ ♦\n♦ ║ ★ ║ $♦ ╚═════╝ ♦$ ║ ★ ║ ♦\n♦ ║ ◆ ║ $ ♦♦♦♦♦♦♦♦♦ $ ║ ◆ ║ ♦\n♦ ║ ♦ ║ $$ INFINITE $$ ║ ♦ ║ ♦\n♦ ║ ☆ ╚═══════════════╝ ☆ ║ ♦\n♦ ║ ★ ◆ ♦ ☆ ♛ ☆ ♦ ◆ ★ ║ ♦\n♦ ═══════════════════════ ♦\n♦♦♦♦♦♦♦ SUPREME GOD ♦♦♦♦♦♦♦",
                    "     ∞∞∞∞∞∞∞∞∞∞∞∞∞     \n   ∞∞ OMNIPOTENT BEING ∞∞   \n  ∞ ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ ∞  \n ∞ ♦ ☆★☆★☆★☆★☆★☆ ♦ ∞ \n∞ ♦ ☆ ╔═══════════╗ ☆ ♦ ∞\n∞ ♦ ★ ║ $ ALL $ ║ ★ ♦ ∞\n∞ ♦ ☆ ║ $ ♦♦♦♦♦♦♦ $ ║ ☆ ♦ ∞\n∞ ♦ ★ ║ $♦ ∞∞∞∞∞ ♦$ ║ ★ ♦ ∞\n∞ ♦ ☆ ║ $♦ ∞ ♛ ∞ ♦$ ║ ☆ ♦ ∞\n∞ ♦ ★ ║ $♦ ∞∞∞∞∞ ♦$ ║ ★ ♦ ∞\n∞ ♦ ☆ ║ $ ♦♦♦♦♦♦♦ $ ║ ☆ ♦ ∞\n∞ ♦ ★ ║ $ POWER $ ║ ★ ♦ ∞\n∞ ♦ ☆ ╚═══════════╝ ☆ ♦ ∞\n ∞ ♦ ☆★☆★☆★☆★☆★☆ ♦ ∞ \n  ∞ ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ ∞  \n   ∞∞ CREATOR OF ALL ∞∞   \n     ∞∞∞∞∞∞∞∞∞∞∞∞∞     "
                ],
                'perfect': [
                    "  ✧✧✧ PERFECT BEING ✧✧✧  \n ✧ ═══════════════════ ✧ \n✧ ║ ♦ ◆ ★ ☆ ♛ ☆ ★ ◆ ♦ ║ ✧\n✧ ║ ◆ ┌───────────────┐ ◆ ║ ✧\n✧ ║ ★ │ $ FLAWLESS $ │ ★ ║ ✧\n✧ ║ ☆ │ $ ♦ ◆ ★ ◆ ♦ $ │ ☆ ║ ✧\n✧ ║ ♛ │ $♦ ╔═════╗ ♦$ │ ♛ ║ ✧\n✧ ║ ☆ │ $♦ ║ ✧♛✧ ║ ♦$ │ ☆ ║ ✧\n✧ ║ ★ │ $♦ ║ ♛☆♛ ║ ♦$ │ ★ ║ ✧\n✧ ║ ◆ │ $♦ ║ ✧♛✧ ║ ♦$ │ ◆ ║ ✧\n✧ ║ ♦ │ $♦ ╚═════╝ ♦$ │ ♦ ║ ✧\n✧ ║ ◆ │ $ ♦ ◆ ★ ◆ ♦ $ │ ◆ ║ ✧\n✧ ║ ★ │ $ PRISTINE $ │ ★ ║ ✧\n✧ ║ ☆ └───────────────┘ ☆ ║ ✧\n✧ ║ ♦ ◆ ★ ☆ ♛ ☆ ★ ◆ ♦ ║ ✧\n ✧ ═══════════════════ ✧ \n  ✧✧✧ IMMACULATE ✧✧✧  "
                ],
                'generic': [
                    "     ♦♦♦ MYTHIC ♦♦♦     \n   ♦♦ $$ ♦♦   \n  ♦ $  ♛  ♛  $ ♦  \n ♦ $ ╔═════╗ $ ♦ \n♦ $ ║ ♦ ◆ ♦ ║ $ ♦\n♦ $ ║ ◆ ♛ ◆ ║ $ ♦\n♦ $ ║ ♦ ◆ ♦ ║ $ ♦\n ♦ $ ╚═════╝ $ ♦ \n  ♦ $  ♛  ♛  $ ♦  \n   ♦♦ $$ ♦♦   \n     ♦♦♦ POWER ♦♦♦     ",
                    "    ★★★★★★★★★★★★★    \n  ★★ RARE MYTHIC ★★  \n ★ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ★ \n★ ♦ $$ ♦ ★\n★ ♦ $ ╔═════════╗ $ ♦ ★\n★ ♦ $ ║ ♦ ♛ ◆ ♛ ♦ ║ $ ♦ ★\n★ ♦ $ ║ ♛ ◆ ♦ ◆ ♛ ║ $ ♦ ★\n★ ♦ $ ║ ◆ ♦ ♛ ♦ ◆ ║ $ ♦ ★\n★ ♦ $ ║ ♛ ◆ ♦ ◆ ♛ ║ $ ♦ ★\n★ ♦ $ ║ ♦ ♛ ◆ ♛ ♦ ║ $ ♦ ★\n★ ♦ $ ╚═════════╝ $ ♦ ★\n★ ♦ $$ ♦ ★\n ★ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ★ \n  ★★ LEGENDARY ★★  \n    ★★★★★★★★★★★★★    "
                ]
            }
        
        # Get appropriate art set
        art_set = arts.get(card_type, arts['generic'])
        return random.choice(art_set)