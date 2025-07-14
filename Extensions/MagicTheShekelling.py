import asyncio
import json
import random
from collections import defaultdict
from io import BytesIO
import discord
from discord.ext import commands

class MagicTheShekellingGame:
    def __init__(self, bot):
        self.bot = bot
        self.PACK_COST = 200
        self.user_collections = defaultdict(lambda: defaultdict(int))
        self.cards_database = self.generate_cards_database()
        
    def generate_cards_database(self):
        """Generate all 151 cards with their stats and ASCII art"""
        cards = {}
        
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
                    "♦♦♦♦♦♦♦ OMNIPOTENT ♦♦♦♦♦♦♦\n♦ ═══════════════════════ ♦\n♦ ║ ★ ◆ ♦ ☆ ♛ ☆ ♦ ◆ ★ ║ ♦\n♦ ║ ◆ ╔═══════════════╗ ◆ ║ ♦\n♦ ║ ♦ ║ $$$ MASTER $$$ ║ ♦ ║ ♦\n♦ ║ ☆ ║ $ ♦♦♦♦♦♦♦♦♦ $ ║ ☆ ║ ♦\n♦ ║ ♛ ║ $♦ ╔═════╗ ♦$ ║ ♛ ║ ♦\n♦ ║ ☆ ║ $♦ ║ ∞ ∞ ∞ ║ ♦$ ║ ☆ ║ ♦\n♦ ║ ♦ ║ $♦ ║ ∞ ♛ ∞ ║ ♦$ ║ ♦ ║ ♦\n♦ ║ ◆ ║ $♦ ║ ∞ ∞ ∞ ║ ♦$ ║ ◆ ║ ♦\n♦ ║ ★ ║ $♦ ╚═════╝ ♦$ ║ ★ ║ ♦\n♦ ║ ◆ ║ $ ♦♦♦♦♦♦♦♦♦ $ ║ ◆ ║ ♦\n♦ ║ ♦ ║ $$$ INFINITE $$$ ║ ♦ ║ ♦\n♦ ║ ☆ ╚═══════════════╝ ☆ ║ ♦\n♦ ║ ★ ◆ ♦ ☆ ♛ ☆ ♦ ◆ ★ ║ ♦\n♦ ═══════════════════════ ♦\n♦♦♦♦♦♦♦ SUPREME GOD ♦♦♦♦♦♦♦",
                    "     ∞∞∞∞∞∞∞∞∞∞∞∞∞     \n   ∞∞ OMNIPOTENT BEING ∞∞   \n  ∞ ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ ∞  \n ∞ ♦ ☆★☆★☆★☆★☆★☆ ♦ ∞ \n∞ ♦ ☆ ╔═══════════╗ ☆ ♦ ∞\n∞ ♦ ★ ║ $$ ALL $$ ║ ★ ♦ ∞\n∞ ♦ ☆ ║ $ ♦♦♦♦♦♦♦ $ ║ ☆ ♦ ∞\n∞ ♦ ★ ║ $♦ ∞∞∞∞∞ ♦$ ║ ★ ♦ ∞\n∞ ♦ ☆ ║ $♦ ∞ ♛ ∞ ♦$ ║ ☆ ♦ ∞\n∞ ♦ ★ ║ $♦ ∞∞∞∞∞ ♦$ ║ ★ ♦ ∞\n∞ ♦ ☆ ║ $ ♦♦♦♦♦♦♦ $ ║ ☆ ♦ ∞\n∞ ♦ ★ ║ $$ POWER $$ ║ ★ ♦ ∞\n∞ ♦ ☆ ╚═══════════╝ ☆ ♦ ∞\n ∞ ♦ ☆★☆★☆★☆★☆★☆ ♦ ∞ \n  ∞ ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ ∞  \n   ∞∞ CREATOR OF ALL ∞∞   \n     ∞∞∞∞∞∞∞∞∞∞∞∞∞     "
                ],
                'perfect': [
                    "  ✧✧✧ PERFECT BEING ✧✧✧  \n ✧ ═══════════════════ ✧ \n✧ ║ ♦ ◆ ★ ☆ ♛ ☆ ★ ◆ ♦ ║ ✧\n✧ ║ ◆ ┌───────────────┐ ◆ ║ ✧\n✧ ║ ★ │ $$ FLAWLESS $$ │ ★ ║ ✧\n✧ ║ ☆ │ $ ♦ ◆ ★ ◆ ♦ $ │ ☆ ║ ✧\n✧ ║ ♛ │ $♦ ╔═════╗ ♦$ │ ♛ ║ ✧\n✧ ║ ☆ │ $♦ ║ ✧♛✧ ║ ♦$ │ ☆ ║ ✧\n✧ ║ ★ │ $♦ ║ ♛☆♛ ║ ♦$ │ ★ ║ ✧\n✧ ║ ◆ │ $♦ ║ ✧♛✧ ║ ♦$ │ ◆ ║ ✧\n✧ ║ ♦ │ $♦ ╚═════╝ ♦$ │ ♦ ║ ✧\n✧ ║ ◆ │ $ ♦ ◆ ★ ◆ ♦ $ │ ◆ ║ ✧\n✧ ║ ★ │ $$ PRISTINE $$ │ ★ ║ ✧\n✧ ║ ☆ └───────────────┘ ☆ ║ ✧\n✧ ║ ♦ ◆ ★ ☆ ♛ ☆ ★ ◆ ♦ ║ ✧\n ✧ ═══════════════════ ✧ \n  ✧✧✧ IMMACULATE ✧✧✧  "
                ],
                'generic': [
                    "     ♦♦♦ MYTHIC ♦♦♦     \n   ♦♦ $$$$$$ ♦♦   \n  ♦ $$  ♛  ♛  $$ ♦  \n ♦ $$ ╔═════╗ $$ ♦ \n♦ $$ ║ ♦ ◆ ♦ ║ $$ ♦\n♦ $$ ║ ◆ ♛ ◆ ║ $$ ♦\n♦ $$ ║ ♦ ◆ ♦ ║ $$ ♦\n ♦ $$ ╚═════╝ $$ ♦ \n  ♦ $$  ♛  ♛  $$ ♦  \n   ♦♦ $$$$$$ ♦♦   \n     ♦♦♦ POWER ♦♦♦     ",
                    "    ★★★★★★★★★★★★★    \n  ★★ RARE MYTHIC ★★  \n ★ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ★ \n★ ♦ $$$$$$$ ♦ ★\n★ ♦ $ ╔═════════╗ $ ♦ ★\n★ ♦ $ ║ ♦ ♛ ◆ ♛ ♦ ║ $ ♦ ★\n★ ♦ $ ║ ♛ ◆ ♦ ◆ ♛ ║ $ ♦ ★\n★ ♦ $ ║ ◆ ♦ ♛ ♦ ◆ ║ $ ♦ ★\n★ ♦ $ ║ ♛ ◆ ♦ ◆ ♛ ║ $ ♦ ★\n★ ♦ $ ║ ♦ ♛ ◆ ♛ ♦ ║ $ ♦ ★\n★ ♦ $ ╚═════════╝ $ ♦ ★\n★ ♦ $$$$$$$ ♦ ★\n ★ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ★ \n  ★★ LEGENDARY ★★  \n    ★★★★★★★★★★★★★    "
                ]
            }
        
        # Get appropriate art set
        art_set = arts.get(card_type, arts['generic'])
        return random.choice(art_set)
    
    def get_pack_contents(self):
        """Generate contents of a single pack"""
        pack = []
        
        # 7 Common cards
        common_ids = [i for i in range(1, 65)]
        for _ in range(7):
            pack.append(random.choice(common_ids))
        
        # 2 Uncommon cards
        uncommon_ids = [i for i in range(65, 97)]
        for _ in range(2):
            pack.append(random.choice(uncommon_ids))
        
        # 1 Rare or Ultra Rare slot
        rare_roll = random.randint(1, 100000)
        
        if rare_roll == 1:  # 1/100000 for 20k ultra rare
            pack.append('ULTRA_LEGENDARY')
        elif rare_roll == 2:  # 1/100000 for Tom's Mirror
            pack.append('TOMS_MIRROR')
        elif rare_roll <= 600:  # 599/100000 (about 1/167) for 5k ultra rare
            pack.append('ULTRA_RARE_5K')
        elif rare_roll <= 1500:  # 900/100000 (about 1/111) for 1k ultra rare
            pack.append('ULTRA_RARE_1K')
        elif rare_roll <= 2800:  # 1300/100000 (about 1/77) for 500 shekel rare
            pack.append('RARE_500')
        elif rare_roll <= 4800:  # 2000/100000 (1/50) for 300 shekel rare
            pack.append('RARE_300')
        elif rare_roll <= 9500:  # 4500/100000 (about 1/22) for 200 shekel rare
            pack.append('RARE_200')
        else:
            # Regular rare or mythic from remaining 90.5%
            remaining_chance = random.randint(1, 30)
            if remaining_chance == 1:  # 1/30 for mythic
                mythic_ids = [i for i in range(127, 152)]
                pack.append(random.choice(mythic_ids))
            else:  # Regular rare
                rare_ids = [i for i in range(97, 127)]
                pack.append(random.choice(rare_ids))
        
        return pack
    
    def create_pack_image(self, pack_contents):
        """Create ASCII representation of pack contents"""
        image_lines = []
        image_lines.append("═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════")
        image_lines.append("                                                                    🎴 MAGIC THE SHEKELLING BOOSTER PACK 🎴")
        image_lines.append("═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════")
        
        for i, card_id in enumerate(pack_contents, 1):
            if isinstance(card_id, str):  # Ultra rare
                if card_id == 'ULTRA_LEGENDARY':
                    image_lines.append(f"🌟 ULTRA LEGENDARY CARD! 🌟")
                    image_lines.append(f"💎 THE ULTIMATE SHEKEL MASTER 💎")
                    image_lines.append(f"Power: ∞ | Toughness: ∞")
                    image_lines.append(f"Value: 20,000 Shekels!")
                    image_lines.append("    ♦♦♦♦♦    ")
                    image_lines.append("   ♦     ♦   ")
                    image_lines.append("  ♦ $$$ ♦  ")
                    image_lines.append("   ♦     ♦   ")
                    image_lines.append("    ♦♦♦♦♦    ")
                elif card_id == 'TOMS_MIRROR':
                    image_lines.append(f"🪞 TOM'S MIRROR - ULTRA MYTHIC! 🪞")
                    image_lines.append(f"✨ THE REFLECTION OF INFINITE WEALTH ✨")
                    image_lines.append(f"Power: ∞ | Toughness: ∞")
                    image_lines.append(f"Value: 15,000 Shekels!")
                    image_lines.append("   ╔═══════════════╗   ")
                    image_lines.append("  ╔╝ ✨ TOM'S MIRROR ✨ ╚╗  ")
                    image_lines.append(" ╔╝ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ╚╗ ")
                    image_lines.append("╔╝ ♦ ╔═══════════╗ ♦ ╚╗")
                    image_lines.append("║ ♦ ║ $$ YOU $$ ║ ♦ ║")
                    image_lines.append("║ ♦ ║ $ REFLECT $ ║ ♦ ║")
                    image_lines.append("║ ♦ ║ $$ ALL $$ ║ ♦ ║")
                    image_lines.append("╚╗ ♦ ╚═══════════╝ ♦ ╔╝")
                    image_lines.append(" ╚╗ ♦♦♦♦♦♦♦♦♦♦♦♦♦ ╔╝ ")
                    image_lines.append("  ╚╗ ✨ INFINITE ✨ ╔╝  ")
                    image_lines.append("   ╚═══════════════╝   ")
                elif card_id == 'ULTRA_RARE_5K':
                    image_lines.append(f"✨ ULTRA RARE CARD! ✨")
                    image_lines.append(f"💰 GOLDEN SHEKEL DRAGON 💰")
                    image_lines.append(f"Power: 15 | Toughness: 15")
                    image_lines.append(f"Value: 5,000 Shekels!")
                    image_lines.append("    ★★★★★    ")
                    image_lines.append("   ★     ★   ")
                    image_lines.append("  ★ $$$ ★  ")
                    image_lines.append("   ★     ★   ")
                    image_lines.append("    ★★★★★    ")
                elif card_id == 'ULTRA_RARE_1K':
                    image_lines.append(f"⭐ ULTRA RARE CARD! ⭐")
                    image_lines.append(f"💎 CRYSTAL COIN GUARDIAN 💎")
                    image_lines.append(f"Power: 10 | Toughness: 10")
                    image_lines.append(f"Value: 1,000 Shekels!")
                    image_lines.append("    ◆◆◆◆◆    ")
                    image_lines.append("   ◆     ◆   ")
                    image_lines.append("  ◆ $$$ ◆  ")
                    image_lines.append("   ◆     ◆   ")
                    image_lines.append("    ◆◆◆◆◆    ")
                elif card_id == 'RARE_500':
                    image_lines.append(f"💰 PREMIUM RARE CARD! 💰")
                    image_lines.append(f"🏆 VAULT MASTER 🏆")
                    image_lines.append(f"Power: 8 | Toughness: 8")
                    image_lines.append(f"Value: 500 Shekels!")
                    image_lines.append("   ▲▲▲▲▲   ")
                    image_lines.append("  ▲ $$ ▲  ")
                    image_lines.append("   ▲▲▲▲▲   ")
                elif card_id == 'RARE_300':
                    image_lines.append(f"🎯 HIGH VALUE RARE! 🎯")
                    image_lines.append(f"💎 TREASURE KEEPER 💎")
                    image_lines.append(f"Power: 7 | Toughness: 7")
                    image_lines.append(f"Value: 300 Shekels!")
                    image_lines.append("   ●●●●●   ")
                    image_lines.append("  ● $$ ●  ")
                    image_lines.append("   ●●●●●   ")
                else:  # RARE_200
                    image_lines.append(f"🔥 VALUABLE RARE! 🔥")
                    image_lines.append(f"⚡ COIN COLLECTOR ⚡")
                    image_lines.append(f"Power: 6 | Toughness: 6")
                    image_lines.append(f"Value: 200 Shekels!")
                    image_lines.append("   ■■■■■   ")
                    image_lines.append("  ■ $$ ■  ")
                    image_lines.append("   ■■■■■   ")
            else:
                card = self.cards_database[card_id]
                rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
                image_lines.append(f"{i}. {rarity_symbol[card['rarity']]} {card['name']}")
                image_lines.append(f"   {card['power']}/{card['toughness']} | {card['description']}")
                image_lines.append(f"   {card['ascii_art']}")
            
            image_lines.append("─" * 160)
        
        image_lines.append("═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════")
        
        return '\n'.join(image_lines)


class MagicTheShekelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = MagicTheShekellingGame(bot)
        self.PACK_COST = 200
        
    @commands.command(aliases=["buypack", "booster", "pack"])
    async def buy_pack(self, ctx):
        """!buypack - Buy a Magic the Shekelling booster pack for 200 shekels"""
        user_id = str(ctx.author.id)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= self.PACK_COST:
            # Remove currency
            self.bot.get_cog('Currency').remove_user_currency(user_id, self.PACK_COST)
            
            # Generate pack contents
            pack_contents = self.game.get_pack_contents()
            
            # Add cards to user collection
            shekel_value = 0
            for card_id in pack_contents:
                if isinstance(card_id, str):  # Ultra rare
                    if card_id == 'ULTRA_LEGENDARY':
                        shekel_value += 20000
                    elif card_id == 'TOMS_MIRROR':
                        shekel_value += 15000
                    elif card_id == 'ULTRA_RARE_5K':
                        shekel_value += 5000
                    elif card_id == 'ULTRA_RARE_1K':
                        shekel_value += 1000
                    elif card_id == 'RARE_500':
                        shekel_value += 500
                    elif card_id == 'RARE_300':
                        shekel_value += 300
                    else:  # RARE_200
                        shekel_value += 200
                else:
                    self.game.user_collections[user_id][card_id] += 1
            
            # If ultra rare, add shekels directly
            if shekel_value > 0:
                self.bot.get_cog('Currency').add_user_currency(user_id, shekel_value)
            
            # Create pack image
            pack_image = self.game.create_pack_image(pack_contents)
            
            # Send the pack opening message
            embed = discord.Embed(
                title="🎴 Magic the Shekelling Booster Pack Opened! 🎴",
                description=f"```\n{pack_image}\n```",
                color=0xFFD700
            )
            
            new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
            embed.add_field(name="💰 Balance", value=f"§{new_balance:.2f}", inline=True)
            
            if shekel_value > 0:
                embed.add_field(name="🎉 BONUS SHEKELS!", value=f"§{shekel_value}", inline=True)
            
            await ctx.send(embed=embed, delete_after=120)
            
        else:
            await ctx.send(f"You need §{self.PACK_COST} to buy a booster pack. You have §{user_balance:.2f}", 
                         delete_after=10)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["collection", "cards", "mycards"])
    async def view_collection(self, ctx):
        """!collection - View your card collection"""
        user_id = str(ctx.author.id)
        collection = self.game.user_collections[user_id]
        
        if not collection:
            await ctx.send("You don't have any cards yet! Buy a booster pack with !buypack", 
                         delete_after=15)
            return
        
        # Sort cards by rarity and create display
        common_cards = []
        uncommon_cards = []
        rare_cards = []
        mythic_cards = []
        
        for card_id, count in collection.items():
            card = self.game.cards_database[card_id]
            card_info = f"{card['name']} x{count}"
            
            if card['rarity'] == 'Common':
                common_cards.append(card_info)
            elif card['rarity'] == 'Uncommon':
                uncommon_cards.append(card_info)
            elif card['rarity'] == 'Rare':
                rare_cards.append(card_info)
            else:  # Mythic
                mythic_cards.append(card_info)
        
        embed = discord.Embed(
            title=f"🎴 {ctx.author.display_name}'s Card Collection",
            color=0x9932CC
        )
        
        if common_cards:
            embed.add_field(name="⚪ Common Cards", value="\n".join(common_cards[:10]), inline=False)
        if uncommon_cards:
            embed.add_field(name="🔵 Uncommon Cards", value="\n".join(uncommon_cards[:10]), inline=False)
        if rare_cards:
            embed.add_field(name="🟡 Rare Cards", value="\n".join(rare_cards[:10]), inline=False)
        if mythic_cards:
            embed.add_field(name="🔴 Mythic Cards", value="\n".join(mythic_cards[:10]), inline=False)
        
        total_cards = sum(collection.values())
        embed.add_field(name="📊 Total Cards", value=str(total_cards), inline=True)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["sellcard", "sell"])
    async def sell_card(self, ctx, *, card_name=None):
        """!sellcard [card name] - Sell a card from your collection"""
        if not card_name:
            await ctx.send("Please specify a card name to sell! Example: !sellcard Shekel Goblin", 
                         delete_after=10)
            return
        
        user_id = str(ctx.author.id)
        collection = self.game.user_collections[user_id]
        
        # Find the card
        card_found = None
        for card_id, count in collection.items():
            if count > 0:
                card = self.game.cards_database[card_id]
                if card['name'].lower() == card_name.lower():
                    card_found = (card_id, card)
                    break
        
        if not card_found:
            await ctx.send(f"You don't have any '{card_name}' cards to sell!", delete_after=10)
            return
        
        card_id, card = card_found
        
        # Calculate sell value
        sell_value = random.randint(card['sell_min'], card['sell_max'])
        
        # Remove card from collection and add shekels
        self.game.user_collections[user_id][card_id] -= 1
        if self.game.user_collections[user_id][card_id] <= 0:
            del self.game.user_collections[user_id][card_id]
        
        self.bot.get_cog('Currency').add_user_currency(user_id, sell_value)
        
        new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        embed = discord.Embed(
            title="💰 Card Sold!",
            description=f"Sold **{card['name']}** for §{sell_value}",
            color=0x00FF00
        )
        embed.add_field(name="💰 New Balance", value=f"§{new_balance:.2f}", inline=True)
        
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["cardinfo", "card"])
    async def view_card(self, ctx, *, card_name=None):
        """!cardinfo [card name] - View detailed information about a card"""
        if not card_name:
            await ctx.send("Please specify a card name! Example: !cardinfo Shekel Goblin", 
                         delete_after=10)
            return
        
        # Find the card in database
        card_found = None
        for card_id, card in self.game.cards_database.items():
            if card['name'].lower() == card_name.lower():
                card_found = card
                break
        
        if not card_found:
            await ctx.send(f"Card '{card_name}' not found!", delete_after=10)
            return
        
        rarity_colors = {
            'Common': 0x808080,
            'Uncommon': 0x0080FF,
            'Rare': 0xFFD700,
            'Mythic': 0xFF4500
        }
        
        embed = discord.Embed(
            title=f"🎴 {card_found['name']}",
            description=f"```\n{card_found['ascii_art']}\n```",
            color=rarity_colors[card_found['rarity']]
        )
        
        embed.add_field(name="⚔️ Power", value=card_found['power'], inline=True)
        embed.add_field(name="🛡️ Toughness", value=card_found['toughness'], inline=True)
        embed.add_field(name="💎 Rarity", value=card_found['rarity'], inline=True)
        embed.add_field(name="📜 Description", value=card_found['description'], inline=False)
        embed.add_field(name="💰 Sell Value", 
                       value=f"§{card_found['sell_min']}-{card_found['sell_max']}", inline=True)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    async def load_data(self):
        """Load user collections from file"""
        try:
            with open(f'{self.qualified_name}_collections.json', 'r') as f:
                data = json.load(f)
                self.game.user_collections = defaultdict(lambda: defaultdict(int), data)
                print(f"Loaded {len(data)} user collections for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling collections file not found, starting fresh.")
    
    async def save_data(self):
        """Save user collections to file"""
        try:
            with open(f'{self.qualified_name}_collections.json', 'w') as f:
                json.dump(dict(self.game.user_collections), f, indent=2)
        except Exception as e:
            print(f"Error saving Magic the Shekelling data: {e}")

async def setup(bot):
    await bot.add_cog(MagicTheShekelling(bot))