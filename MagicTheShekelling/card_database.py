import random

class CardDatabase:
    def __init__(self):
        self.special_cards = {}
        self.holo_special_cards = {}
        
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
                'sell_min': 6924,
                'sell_max': 9232
            },
            'TOMS_MIRROR': {
                'name': "Tom's Mirror",
                'rarity': 'Ultra Mythic',
                'power': '∞',
                'toughness': '∞',
                'description': 'The reflection of infinite wealth',
                'ascii_art': "   ╔═══════════════╗   \n  ╔╝ ✨ TOM'S MIRROR ✨ ╚╗  \n ╔╝ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ╚╗ \n╔╝ ♦ ╔═══════════╗ ♦ ╚╗\n║ ♦ ║  $ YOU $  ║ ♦ ║\n║ ♦ ║ $ REFLECT $ ║ ♦ ║\n║ ♦ ║  $ ALL $  ║ ♦ ║\n╚╗ ♦ ╚═══════════╝ ♦ ╔╝\n ╚╗ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ╔╝ \n  ╚╗ ✨ INFINITE ✨ ╔╝  \n   ╚═══════════════╝   ",
                'sell_min': 5539,
                'sell_max': 6924
            },
            'ULTRA_RARE_20K': {
                'name': 'Cosmic Shekel Sovereign',
                'rarity': 'Ultra Rare',
                'power': 25,
                'toughness': 25,
                'description': 'Sovereign of the cosmic treasury, master of universal wealth',
                'ascii_art': "      ★★★★★★★★★★★★★      \n    ★★★★★★★★★★★★★★★★★    \n  ★★★★ $$$$$$$$$$$ ★★★★  \n ★★★★ $$$$$$$$$$$$$$ ★★★★ \n★★★★ $$$$$ ♦♦♦ $$$$$ ★★★★\n★★★ $$$$$ ♦ ∞ ♦ $$$$$ ★★★\n★★★ $$$$$ ♦ ♦ ♦ $$$$$ ★★★\n★★★★ $$$$$ ♦♦♦ $$$$$ ★★★★\n ★★★★ $$$$$$$$$$$$$$ ★★★★ \n  ★★★★ $$$$$$$$$$$ ★★★★  \n    ★★★★★★★★★★★★★★★★★    \n      ★★★★★★★★★★★★★      ",
                'sell_min': 8309,
                'sell_max': 11540
            },
            'ULTRA_RARE_10K': {
                'name': 'Platinum Shekel Emperor',
                'rarity': 'Ultra Rare',
                'power': 20,
                'toughness': 20,
                'description': 'Emperor of the platinum realm, ruler of infinite wealth',
                'ascii_art': "   ♔♔♔♔♔♔♔♔♔♔♔   \n  ♔♔♔♔♔♔♔♔♔♔♔♔♔  \n ♔♔♔ $$$ ♔ $$$ ♔♔♔ \n♔♔♔ $$$$ ♔ $$$$ ♔♔♔\n♔♔ $$$$$ ♔ $$$$$ ♔♔\n♔♔ $$$$$ ♔ $$$$$ ♔♔\n♔♔♔ $$$$ ♔ $$$$ ♔♔♔\n ♔♔♔ $$$ ♔ $$$ ♔♔♔ \n  ♔♔♔♔♔♔♔♔♔♔♔♔♔  \n   ♔♔♔♔♔♔♔♔♔♔♔   ",
                'sell_min': 3693,
                'sell_max': 5539
            },
            'ULTRA_RARE_5K': {
                'name': 'Golden Shekel Dragon',
                'rarity': 'Ultra Rare',
                'power': 15,
                'toughness': 15,
                'description': 'A dragon made of pure shekels',
                'ascii_art': "    ★★★★★    \n   ★     ★   \n  ★  $$  ★  \n   ★     ★   \n    ★★★★★    ",
                'sell_min': 1846,
                'sell_max': 2308
            },
            'ULTRA_RARE_1K': {
                'name': 'Crystal Coin Guardian',
                'rarity': 'Ultra Rare',
                'power': 10,
                'toughness': 10,
                'description': 'Guardian of the crystal vault',
                'ascii_art': "    ◆◆◆◆◆    \n   ◆     ◆   \n  ◆  $$  ◆  \n   ◆     ◆   \n    ◆◆◆◆◆    ",
                'sell_min': 462,
                'sell_max': 923
            },
            'RARE_500': {
                'name': 'Vault Master',
                'rarity': 'Premium Rare',
                'power': 8,
                'toughness': 8,
                'description': 'Master of the shekel vaults',
                'ascii_art': "   ▲▲▲▲▲   \n  ▲  $  ▲  \n   ▲▲▲▲▲   ",
                'sell_min': 369,
                'sell_max': 554
            },
            'RARE_300': {
                'name': 'Treasure Keeper',
                'rarity': 'High Value Rare',
                'power': 7,
                'toughness': 7,
                'description': 'Keeper of ancient treasures',
                'ascii_art': "   ●●●●●   \n  ●  $  ●  \n   ●●●●●   ",
                'sell_min': 231,
                'sell_max': 462
            },
            'RARE_200': {
                'name': 'Coin Collector',
                'rarity': 'Valuable Rare',
                'power': 6,
                'toughness': 6,
                'description': 'Collector of rare coins',
                'ascii_art': "   ■■■■■   \n  ■  $  ■  \n   ■■■■■   ",
                'sell_min': 231,
                'sell_max': 462
            }
        }
        
        # Generate holo foil versions of special cards
        self.holo_special_cards = {}
        for card_id, card_data in self.special_cards.items():
            holo_id = f"HOLO_{card_id}"
            self.holo_special_cards[holo_id] = {
                'name': f"Holo {card_data['name']}",
                'rarity': f"Holo {card_data['rarity']}",
                'power': card_data['power'],
                'toughness': card_data['toughness'],
                'description': f"Holo foil version - {card_data['description']}",
                'ascii_art': self.generate_holo_ascii_art(card_data['ascii_art']),
                'sell_min': card_data['sell_min'] * 2,
                'sell_max': card_data['sell_max'] * 2
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
                'sell_max': 5
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
                'sell_min': 2,
                'sell_max': 9
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
                'sell_min': 5,
                'sell_max': 18
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
                'sell_min': 92,
                'sell_max': 231
            }
            card_id += 1
        
        # Generate holo foil versions of regular cards
        holo_cards = {}
        for card_id, card_data in cards.items():
            holo_id = f"HOLO_{card_id}"
            holo_cards[holo_id] = {
                'name': f"Holo {card_data['name']}",
                'rarity': f"Holo {card_data['rarity']}",
                'power': card_data['power'],
                'toughness': card_data['toughness'],
                'description': f"Holo foil version - {card_data['description']}",
                'ascii_art': self.generate_holo_ascii_art(card_data['ascii_art']),
                'sell_min': card_data['sell_min'] * 2,
                'sell_max': card_data['sell_max'] * 2
            }
        
        # Add holo cards to the main cards dictionary
        cards.update(holo_cards)
        
        return cards
    
    def generate_holo_ascii_art(self, original_art):
        """Generate holo foil version of ASCII art"""
        # Create a shimmering holo effect by replacing filled characters with hollow ones
        holo_replacements = {
            '♦': '◇',
            '★': '☆',
            '♛': '♕',
            '♔': '♕',
            '●': '○',
            '■': '□',
            '▲': '△',
            '◆': '◇',
            '█': '▓',
            '▓': '▒',
            '▒': '░',
            '░': '·',
            '#': '▒',
            '$': '¤',
            '∞': '∞',  # Keep infinity symbol
            '╔': '╔',  # Keep box drawing
            '╗': '╗',
            '╚': '╚',
            '╝': '╝',
            '║': '║',
            '═': '═',
            '┌': '┌',
            '┐': '┐',
            '└': '└',
            '┘': '┘',
            '─': '─',
            '│': '│',
            '├': '├',
            '┤': '┤',
            '┬': '┬',
            '┴': '┴',
            '┼': '┼'
        }
        
        holo_art = original_art
        for original, holo in holo_replacements.items():
            holo_art = holo_art.replace(original, holo)
        
        # Add sparkle effects around the holo art
        lines = holo_art.split('\n')
        max_width = max(len(line) for line in lines) if lines else 0
        
        # Add sparkle border
        sparkle_chars = ['✧', '✦', '✪', '✫', '✬', '✭', '✮', '✯', '✰']
        
        # Add random sparkles around the art
        enhanced_lines = []
        for i, line in enumerate(lines):
            if i == 0:
                # Top sparkle line
                sparkle_line = ''.join(random.choice(sparkle_chars + [' ', ' ']) for _ in range(max_width + 4))
                enhanced_lines.append(sparkle_line)
            
            # Add sparkles to sides
            left_sparkle = random.choice(sparkle_chars + [' '])
            right_sparkle = random.choice(sparkle_chars + [' '])
            enhanced_lines.append(f"{left_sparkle} {line.ljust(max_width)} {right_sparkle}")
            
            if i == len(lines) - 1:
                # Bottom sparkle line
                sparkle_line = ''.join(random.choice(sparkle_chars + [' ', ' ']) for _ in range(max_width + 4))
                enhanced_lines.append(sparkle_line)
        
        return '\n'.join(enhanced_lines)
    
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
