import asyncio
import json
from json import JSONEncoder
import discord
import random
from discord.ext import tasks, commands
from datetime import datetime, timedelta

DEBUG = False
DEBUG_TICKER = False
TICK_RATE = 6
LETTERS_TO_EMOJI_ASCII = {'A': '🇦', 'B': '🇧', 'C': '🇨', 'D': '🇩', 'E': '🇪', 'F': '🇫', 'G': '🇬', 'H': '🇭',
                          'I': '🇮',
                          'J': '🇯', 'K': '🇰', 'L': '🇱', 'M': '🇲', 'N': '🇳', 'O': '🇴', 'P': '🇵', 'Q': '🇶',
                          'R': '🇷',
                          'S': '🇸', 'T': '🇹', 'U': '🇺', 'V': '🇻', 'W': '🇼', 'X': '🇽', 'Y': '🇾', 'Z': '🇿',
                          ' ': '✴'}

# Enhanced mining sources with upgrade paths
MINING_SOURCES = {
    "idle": {"name": "Idle GPU Miner", "costIncrease": 1.1, "payoutTimer": 60, "payoutTimerEnglish": "/m", "price": 150,
             "description": "!buy idle", "payout": 1, "powerUse": 1.44, "sincePayment": 0, "tier": 1, "maxUpgrades": 5},
    "asic": {"name": "ASIC Miner", "costIncrease": 1.15, "payoutTimer": 600, "payoutTimerEnglish": "/10m", "price": 1525,
             "description": "!buy asic", "payout": 15, "powerUse": 2.16, "sincePayment": 0, "tier": 2, "maxUpgrades": 5},
    "rack": {"name": "Rack of Miners", "costIncrease": 1.25, "payoutTimer": 3600, "payoutTimerEnglish": "/h",
             "price": 7500, "description": "!buy rack", "payout": 150, "powerUse": 13.6, "sincePayment": 0, "tier": 3, "maxUpgrades": 5},
    "dcf": {"name": "DCF Container", "costIncrease": 1.33, "payoutTimer": 43200, "payoutTimerEnglish": "/12h",
            "price": 15000, "description": "!buy dcf", "payout": 2500, "powerUse": 27.2, "sincePayment": 0, "tier": 4, "maxUpgrades": 5}
}

POWER_SOURCES = {
    "panel": {"name": "Solar Panel", "costIncrease": 1.5, "timer": 60, "description": "!buy panel", "price": 500,
              "powerGenerated": 1.15, "tier": 1, "maxUpgrades": 5},
    "petrol": {"name": "Petrol Generator", "costIncrease": 2, "timer": 60, "price": 1200,
               "description": "!buy petrol", "powerGenerated": 2, "tier": 2, "maxUpgrades": 5},
    "farm": {"name": "Solar Farm", "costIncrease": 1.5, "timer": 60, "description": "!buy farm", "price": 9000,
             "powerGenerated": 15, "tier": 3, "maxUpgrades": 5},
    "gas": {"name": "Gas Generator", "costIncrease": 2.5, "timer": 60, "price": 15000,
            "description": "!buy gas", "powerGenerated": 30, "tier": 4, "maxUpgrades": 5}
}

# Roguelite features
RANDOM_EVENTS = [
    {"name": "Solar Storm", "type": "negative", "description": "Equipment damaged!", "effect": "damage_equipment", "probability": 0.05},
    {"name": "Lucky Find", "type": "positive", "description": "Found bonus resources!", "effect": "bonus_currency", "probability": 0.08},
    {"name": "Power Surge", "type": "positive", "description": "Extra power generation!", "effect": "power_boost", "probability": 0.06},
    {"name": "Market Crash", "type": "negative", "description": "Mining payouts reduced!", "effect": "payout_reduction", "probability": 0.04},
    {"name": "Tech Breakthrough", "type": "positive", "description": "Equipment efficiency improved!", "effect": "efficiency_boost", "probability": 0.03},
    {"name": "Blackout", "type": "negative", "description": "Power grid failure!", "effect": "power_outage", "probability": 0.02}
]

UPGRADE_MATERIALS = {
    "copper": {"name": "Copper Wire", "rarity": "common", "drop_rate": 0.15},
    "silicon": {"name": "Silicon Chip", "rarity": "common", "drop_rate": 0.12},
    "rare_earth": {"name": "Rare Earth Elements", "rarity": "uncommon", "drop_rate": 0.08},
    "quantum": {"name": "Quantum Core", "rarity": "rare", "drop_rate": 0.03},
    "exotic": {"name": "Exotic Matter", "rarity": "legendary", "drop_rate": 0.01}
}

ACHIEVEMENTS = {
    "first_miner": {"name": "First Steps", "description": "Buy your first miner", "reward": 100},
    "power_baron": {"name": "Power Baron", "description": "Generate 1000 kW-h", "reward": 500},
    "efficiency_expert": {"name": "Efficiency Expert", "description": "Upgrade 10 items", "reward": 1000},
    "survivor": {"name": "Survivor", "description": "Survive 5 negative events", "reward": 750},
    "millionaire": {"name": "Crypto Millionaire", "description": "Accumulate 1,000,000 currency", "reward": 5000}
}

SMALLEST_PAYMENT_TIMER = 60
BASE_POWER_SUPPLY = 1
POWER_EXPORT_BASE_VALUE = 0.008
MAXIMUM_EXPORT_MULTIPLIER = 96
POWER_PAYMENT_FREQUENCY = 60
SELL_MULTIPLIER = 0.8  # 80% sell value

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

def compounding_increase(principle, rate, count):
    amt = principle * (pow(rate, count))
    return float(amt)

class MinerGame(commands.Cog):
    def __init__(self, bot):
        global TICK_RATE
        TICK_RATE = bot.TICK_RATE
        self.bot = bot
        self.time_elapsed = 0
        self.world_power_supply = BASE_POWER_SUPPLY
        self.world_power_demand = 0
        self.power_demand_pct = 0
        self.current_power_price = POWER_EXPORT_BASE_VALUE
        self.member_generators = {}
        self.member_miners = {}
        self.member_total_power = {}
        self.member_total_power_usage = {}
        self.member_materials = {}
        self.member_achievements = {}
        self.member_event_buffs = {}
        self.member_stats = {}
        self.last_event_time = datetime.now()

    def get_item_sell_price(self, item_name, item_type, count):
        """Calculate sell price for an item (80% of current buy price)"""
        sources = MINING_SOURCES if item_type == "miner" else POWER_SOURCES
        current_price = compounding_increase(
            sources[item_name]['price'], 
            sources[item_name]['costIncrease'], 
            count - 1
        )
        return current_price * SELL_MULTIPLIER

    def initialize_member_data(self, member_id):
        """Initialize all member data structures"""
        member_id = str(member_id)
        if member_id not in self.member_generators:
            self.member_generators[member_id] = []
        if member_id not in self.member_miners:
            self.member_miners[member_id] = []
        if member_id not in self.member_total_power:
            self.member_total_power[member_id] = 0.0
        if member_id not in self.member_total_power_usage:
            self.member_total_power_usage[member_id] = 0.0
        if member_id not in self.member_materials:
            self.member_materials[member_id] = {mat: 0 for mat in UPGRADE_MATERIALS.keys()}
        if member_id not in self.member_achievements:
            self.member_achievements[member_id] = []
        if member_id not in self.member_event_buffs:
            self.member_event_buffs[member_id] = {}
        if member_id not in self.member_stats:
            self.member_stats[member_id] = {
                "total_power_generated": 0,
                "total_upgrades": 0,
                "events_survived": 0,
                "items_sold": 0
            }

    @commands.command(name="sell")
    async def sell(self, ctx, item_type: str = "", item_name: str = ""):
        """!sell [miner/power] [item_name] - sells an item for 80% of current buy price"""
        user_id = str(ctx.author.id)
        self.initialize_member_data(user_id)
        
        if not item_type or not item_name:
            msg = f"{ctx.author.name} - Usage: !sell [miner/power] [item_name]"
            await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return

        item_type = item_type.lower()
        item_name = item_name.lower()
        
        if item_type == "miner" and item_name in MINING_SOURCES:
            user_items = self.member_miners[user_id]
            sources = MINING_SOURCES
        elif item_type == "power" and item_name in POWER_SOURCES:
            user_items = self.member_generators[user_id]
            sources = POWER_SOURCES
        else:
            msg = f"{ctx.author.name} - Invalid item type or name!"
            await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return

        # Find and remove the item
        item_found = False
        item_count = 0
        for i, item in enumerate(user_items):
            if item['name'] == sources[item_name]['name']:
                if not item_found:
                    # Count total items for price calculation
                    for check_item in user_items:
                        if check_item['name'] == sources[item_name]['name']:
                            item_count += 1
                    
                    sell_price = self.get_item_sell_price(item_name, item_type, item_count)
                    user_items.pop(i)
                    self.bot.get_cog('Currency').add_user_currency(user_id, sell_price)
                    self.member_stats[user_id]["items_sold"] += 1
                    
                    msg = f"{ctx.author.name} - Sold {sources[item_name]['name']} for {self.bot.CURRENCY_TOKEN}{sell_price:.1f}"
                    item_found = True
                    break

        if not item_found:
            msg = f"{ctx.author.name} - You don't own any {sources[item_name]['name']}!"

        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        await self.save_data()

    @commands.command(name="upgrade")
    async def upgrade(self, ctx, item_type: str = "", item_name: str = ""):
        """!upgrade [miner/power] [item_name] - upgrades an item using materials"""
        user_id = str(ctx.author.id)
        self.initialize_member_data(user_id)
        
        if not item_type or not item_name:
            msg = f"{ctx.author.name} - Usage: !upgrade [miner/power] [item_name]"
            await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return

        item_type = item_type.lower()
        item_name = item_name.lower()
        
        if item_type == "miner" and item_name in MINING_SOURCES:
            user_items = self.member_miners[user_id]
            sources = MINING_SOURCES
        elif item_type == "power" and item_name in POWER_SOURCES:
            user_items = self.member_generators[user_id]
            sources = POWER_SOURCES
        else:
            msg = f"{ctx.author.name} - Invalid item type or name!"
            await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return

        # Find upgradeable item
        for item in user_items:
            if item['name'] == sources[item_name]['name']:
                current_upgrades = item.get('upgrades', 0)
                max_upgrades = sources[item_name]['maxUpgrades']
                
                if current_upgrades >= max_upgrades:
                    msg = f"{ctx.author.name} - {item['name']} is already at maximum upgrade level!"
                    break
                
                # Check materials (simplified - need copper and silicon)
                materials_needed = {"copper": 2 + current_upgrades, "silicon": 1 + current_upgrades}
                can_upgrade = True
                
                for mat, needed in materials_needed.items():
                    if self.member_materials[user_id][mat] < needed:
                        can_upgrade = False
                        break
                
                if can_upgrade:
                    # Consume materials
                    for mat, needed in materials_needed.items():
                        self.member_materials[user_id][mat] -= needed
                    
                    # Apply upgrade
                    item['upgrades'] = current_upgrades + 1
                    if item_type == "miner":
                        item['payout'] = int(item['payout'] * 1.2)
                    else:
                        item['powerGenerated'] = item['powerGenerated'] * 1.2
                    
                    self.member_stats[user_id]["total_upgrades"] += 1
                    msg = f"{ctx.author.name} - Upgraded {item['name']} to level {item['upgrades']}!"
                    break
                else:
                    msg = f"{ctx.author.name} - Not enough materials! Need: "
                    for mat, needed in materials_needed.items():
                        msg += f"{needed} {UPGRADE_MATERIALS[mat]['name']}, "
                    msg = msg.rstrip(", ")
                    break
        else:
            msg = f"{ctx.author.name} - You don't own any {sources[item_name]['name']}!"

        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        await self.save_data()

    @commands.command(name="materials")
    async def materials(self, ctx, member: discord.Member = None):
        """!materials - shows your materials and achievements"""
        member = member or ctx.author
        user_id = str(member.id)
        self.initialize_member_data(user_id)
        
        msg = f"{member.name}'s Materials & Progress:\n```"
        msg += f"Materials:\n"
        for mat_id, mat_data in UPGRADE_MATERIALS.items():
            count = self.member_materials[user_id][mat_id]
            msg += f"  {mat_data['name']}: {count}\n"
        
        msg += f"\nAchievements:\n"
        for ach_id, ach_data in ACHIEVEMENTS.items():
            status = "✓" if ach_id in self.member_achievements[user_id] else "✗"
            msg += f"  {status} {ach_data['name']}: {ach_data['description']}\n"
        
        msg += f"\nStats:\n"
        stats = self.member_stats[user_id]
        msg += f"  Power Generated: {stats['total_power_generated']:.1f} kW-h\n"
        msg += f"  Upgrades Made: {stats['total_upgrades']}\n"
        msg += f"  Events Survived: {stats['events_survived']}\n"
        msg += f"  Items Sold: {stats['items_sold']}\n"
        msg += "```"
        
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    def check_achievements(self, user_id):
        """Check and award achievements"""
        user_id = str(user_id)
        stats = self.member_stats[user_id]
        current_achievements = self.member_achievements[user_id]
        
        # Check each achievement
        new_achievements = []
        
        if "first_miner" not in current_achievements and len(self.member_miners[user_id]) > 0:
            current_achievements.append("first_miner")
            new_achievements.append("first_miner")
        
        if "power_baron" not in current_achievements and stats["total_power_generated"] >= 1000:
            current_achievements.append("power_baron")
            new_achievements.append("power_baron")
        
        if "efficiency_expert" not in current_achievements and stats["total_upgrades"] >= 10:
            current_achievements.append("efficiency_expert")
            new_achievements.append("efficiency_expert")
        
        if "survivor" not in current_achievements and stats["events_survived"] >= 5:
            current_achievements.append("survivor")
            new_achievements.append("survivor")
        
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        if "millionaire" not in current_achievements and user_balance >= 1000000:
            current_achievements.append("millionaire")
            new_achievements.append("millionaire")
        
        # Award achievement rewards
        for ach_id in new_achievements:
            reward = ACHIEVEMENTS[ach_id]["reward"]
            self.bot.get_cog('Currency').add_user_currency(user_id, reward)
        
        return new_achievements

    def trigger_random_event(self):
        """Trigger a random event affecting all players"""
        if random.random() < 0.1:  # 10% chance per timeout cycle
            event = random.choice(RANDOM_EVENTS)
            
            event_msg = f"🎲 **{event['name']}** - {event['description']}\n"
            
            for member_id in self.member_generators.keys():
                if event['effect'] == "damage_equipment":
                    # Randomly damage 20% of equipment
                    all_items = self.member_generators[member_id] + self.member_miners[member_id]
                    damage_count = max(1, len(all_items) // 5)
                    damaged_items = random.sample(all_items, min(damage_count, len(all_items)))
                    for item in damaged_items:
                        if item_type == "miner":
                            item['payout'] = max(1, int(item['payout'] * 0.8))
                        else:
                            item['powerGenerated'] = max(0.1, item['powerGenerated'] * 0.8)
                    self.member_stats[member_id]["events_survived"] += 1
                    
                elif event['effect'] == "bonus_currency":
                    bonus = random.randint(100, 500)
                    self.bot.get_cog('Currency').add_user_currency(member_id, bonus)
                    
                elif event['effect'] == "power_boost":
                    self.member_event_buffs[member_id]["power_boost"] = 5  # 5 cycles
                    
                elif event['effect'] == "payout_reduction":
                    self.member_event_buffs[member_id]["payout_reduction"] = 3  # 3 cycles
                    self.member_stats[member_id]["events_survived"] += 1
                    
                elif event['effect'] == "efficiency_boost":
                    # Give random materials
                    for mat in UPGRADE_MATERIALS.keys():
                        if random.random() < 0.3:
                            self.member_materials[member_id][mat] += random.randint(1, 3)
                    
                elif event['effect'] == "power_outage":
                    self.member_event_buffs[member_id]["power_outage"] = 2  # 2 cycles
                    self.member_stats[member_id]["events_survived"] += 1
            
            return event_msg
        return None

    def apply_event_buffs(self, member_id):
        """Apply temporary event buffs/debuffs"""
        buffs = self.member_event_buffs[member_id]
        power_multiplier = 1.0
        payout_multiplier = 1.0
        
        if "power_boost" in buffs and buffs["power_boost"] > 0:
            power_multiplier *= 1.5
            buffs["power_boost"] -= 1
            if buffs["power_boost"] <= 0:
                del buffs["power_boost"]
        
        if "payout_reduction" in buffs and buffs["payout_reduction"] > 0:
            payout_multiplier *= 0.7
            buffs["payout_reduction"] -= 1
            if buffs["payout_reduction"] <= 0:
                del buffs["payout_reduction"]
        
        if "power_outage" in buffs and buffs["power_outage"] > 0:
            power_multiplier *= 0.1
            buffs["power_outage"] -= 1
            if buffs["power_outage"] <= 0:
                del buffs["power_outage"]
        
        return power_multiplier, payout_multiplier

    def drop_materials(self, member_id):
        """Random material drops from mining"""
        for mat_id, mat_data in UPGRADE_MATERIALS.items():
            if random.random() < mat_data['drop_rate']:
                self.member_materials[member_id][mat_id] += 1

    @commands.command(name="my#")
    async def mybase(self, ctx, member: discord.Member = None):
        """!my# - displays all resources with upgrade levels"""
        member = member or ctx.author
        user_id = str(member.id)
        self.initialize_member_data(user_id)
        
        msg = f"{member.name}'s Base - Last Power Bill - Supply: `{self.member_total_power[user_id]:.2f}kW-h` Demand: `{self.member_total_power_usage[user_id]:.2f}kW-h`\n```"
        user_generators = self.member_generators[user_id]
        user_miners = self.member_miners[user_id]
        msg += f" #   | Resource Type        | Created          | Used          | Upgrades |\n"
        msg += f"-----|----------------------|------------------|---------------|----------|\n"
        
        if len(user_generators) > 0:
            msg += f"----- Power Generators ------------------------------------------------|\n"
            for generator in POWER_SOURCES.keys():
                count = 0
                avg_upgrades = 0
                total_power = 0
                for user_generator in user_generators:
                    if user_generator['name'] == POWER_SOURCES[generator]['name']:
                        count += 1
                        avg_upgrades += user_generator.get('upgrades', 0)
                        total_power += user_generator['powerGenerated']
                if count > 0:
                    avg_upgrades = avg_upgrades / count
                    msg += f" {count:<3} | {POWER_SOURCES[generator]['name']:<20} | {total_power:>8.2f}{' kW-h':<8} |{'|':>15} +{avg_upgrades:.1f}     |\n"
        
        if len(user_miners) > 0:
            msg += f"----- Miners ----------------------------------------------------------|\n"
            for miner in MINING_SOURCES.keys():
                count = 0
                avg_upgrades = 0
                total_payout = 0
                total_power_use = 0
                for mining_device in user_miners:
                    if mining_device['name'] == MINING_SOURCES[miner]['name']:
                        count += 1
                        avg_upgrades += mining_device.get('upgrades', 0)
                        total_payout += mining_device['payout']
                        total_power_use += mining_device['powerUse']
                if count > 0:
                    avg_upgrades = avg_upgrades / count
                    msg += f" {count:<3} | {MINING_SOURCES[miner]['name']:<20} | {total_payout:>8}{MINING_SOURCES[miner]['payoutTimerEnglish']:<8} | {total_power_use:>7.2f} kW-h  | +{avg_upgrades:.1f}     |\n"
        msg += "```"
        
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    @commands.command(name="power")
    async def power(self, ctx, *, member: discord.Member = None):
        """shows world power grid details"""
        member = member or ctx.author
        user_id = str(member.id)
        self.initialize_member_data(user_id)
        
        power_supply = self.member_total_power[user_id]
        power_usage = self.member_total_power_usage[user_id]
        power_pct = 0
        if power_usage > 0:
            power_pct = power_usage / power_supply if power_supply > 0 else 0
        
        msg = f"World Supply: `{self.world_power_supply:.1f} kW-h`, World Demand: `{self.world_power_demand:.1f} kW-h`, Price: `{self.bot.CURRENCY_TOKEN}{self.current_power_price:.2f}/kW-h`\n"
        msg += f"{member.mention} - Supply: `{power_supply:.1f}kW-h` Demand: `{power_usage:.1f}kW-h` (`{power_pct * 100:.1f}%`)"
        
        # Show active buffs
        buffs = self.member_event_buffs[user_id]
        if buffs:
            msg += f"\nActive Effects: "
            for buff, duration in buffs.items():
                msg += f"`{buff.replace('_', ' ').title()} ({duration})`  "
        
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    async def buy_miner(self, user_id="", item_name=""):
        """Buys miner, removes currency from user balance, returns message"""
        self.initialize_member_data(user_id)
        user_miners = self.member_miners[user_id]
        item_count = 0
        item = MINING_SOURCES[item_name]['name']
        
        for miner in user_miners:
            if miner["name"] == item:
                item_count += 1
        
        price = compounding_increase(MINING_SOURCES[item_name]['price'], 
                                   MINING_SOURCES[item_name]['costIncrease'], item_count)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= float(price):
            new_miner = MINING_SOURCES[item_name].copy()
            new_miner['upgrades'] = 0
            self.member_miners[user_id].append(new_miner)
            self.bot.get_cog('Currency').remove_user_currency(user_id, abs(float(price)))
            
            # Check achievements
            new_achievements = self.check_achievements(user_id)
            msg = f"Purchased {MINING_SOURCES[item_name]['name']} for {self.bot.CURRENCY_TOKEN}{price:.1f} now has {item_count + 1}"
            
            if new_achievements:
                msg += f" 🏆 Achievement unlocked: {', '.join([ACHIEVEMENTS[ach]['name'] for ach in new_achievements])}"
            
            return msg
        return f"You need {self.bot.CURRENCY_TOKEN}{price:.1f} to buy {MINING_SOURCES[item_name]['name']}"

    async def buy_generator(self, user_id="", item_name=""):
        """Buys power source, removes currency from user balance, returns message"""
        self.initialize_member_data(user_id)
        user_generators = self.member_generators[user_id]
        item_count = 0
        item = POWER_SOURCES[item_name]['name']
        
        for power in user_generators:
            if power["name"] == item:
                item_count += 1
        
        price = compounding_increase(POWER_SOURCES[item_name]['price'], 
                                   POWER_SOURCES[item_name]['costIncrease'], item_count)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= float(price):
            new_generator = POWER_SOURCES[item_name].copy()
            new_generator['upgrades'] = 0
            self.member_generators[user_id].append(new_generator)
            self.bot.get_cog('Currency').remove_user_currency(user_id, abs(float(price)))
            return f"Purchased {POWER_SOURCES[item_name]['name']} for {self.bot.CURRENCY_TOKEN}{price:.1f} now has {item_count + 1}"
        return f"You need {self.bot.CURRENCY_TOKEN}{price:.1f} to buy {POWER_SOURCES[item_name]['name']}"

    @commands.command(name="buy")
    async def buy(self, ctx, item_name: str = ""):
        """!buy [type] - buys power/mining items"""
        user_id = str(ctx.author.id)
        self.initialize_member_data(user_id)
        item_name = str(item_name).lower()
        outcome = f"{ctx.author.name} - "
        
        if item_name in MINING_SOURCES.keys():
            outcome += await self.buy_miner(user_id=user_id, item_name=item_name)
        elif item_name in POWER_SOURCES.keys():
            outcome += await self.buy_generator(user_id=user_id, item_name=item_name)
        else:
            outcome += f"Invalid item- Current Items..."
            outcome += "```"
            outcome += f" Resource Type      | Produces         | Uses       | Command      | Your Price   | Sell Price   |\n"
            outcome += f"--------------------|------------------|------------|--------------|--------------|-------------|\n"
            outcome += f"- Power Generation ---------------------------------------------------------------------|\n"
            for (key, item) in POWER_SOURCES.items():
                user_count = sum(1 for gen in self.member_generators[user_id] if gen['name'] == item['name'])
                buy_price = compounding_increase(item['price'], item['costIncrease'], user_count)
                sell_price = self.get_item_sell_price(key, "power", user_count) if user_count > 0 else 0
                outcome += f" {item['name']:<18} | {item['powerGenerated']:>9.2f} {'kW-h':<6} | {'|':>12} {item['description']:<13}| ${buy_price:^12.2f}| ${sell_price:^11.2f}|\n"
            outcome += f"- Miners ---------------------------------------------------------------------------|\n"
            for (key, item) in MINING_SOURCES.items():
                user_count = sum(1 for miner in self.member_miners[user_id] if miner['name'] == item['name'])
                buy_price = compounding_increase(item['price'], item['costIncrease'], user_count)
                sell_price = self.get_item_sell_price(key, "miner", user_count) if user_count > 0 else 0
                outcome += f" {item['name']:<18} | {item['payout']:>8} {item['payoutTimerEnglish']:<7} | {item['powerUse']:>6.2f}kW-h | {item['description']:<13}| ${buy_price:^12.2f}| ${sell_price:^11.2f}|\n"
            outcome += "```"
            outcome += "Commands: !buy [item], !sell [miner/power] [item], !upgrade [miner/power] [item], !materials"
        
        await ctx.channel.send(outcome, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        await self.save_data()

async def load_data(self):
    """Load game data from file"""
    print(f"Loading Mining game data...")
    try:
        with open(f'/app/data/{self.qualified_name}_data.json', 'r+') as in_file:
            data = json.load(in_file)
            self.time_elapsed = data.get('uptime', 0)
            self.world_power_supply = data.get('world_power_supply', BASE_POWER_SUPPLY)
            self.world_power_demand = data.get('world_power_demand', 0)
            self.power_demand_pct = data.get('power_demand_pct', 0)
            self.current_power_price = data.get('current_power_price', POWER_EXPORT_BASE_VALUE)
            self.member_generators = data.get('member_generators', {})
            self.member_miners = data.get('member_miners', {})
            self.member_materials = data.get('member_materials', {})
            self.member_achievements = data.get('member_achievements', {})
            self.member_event_buffs = data.get('member_event_buffs', {})
            self.member_stats = data.get('member_stats', {})
            print(f"Loaded {len(self.member_generators)} Members Idle Game Data.")
    except FileNotFoundError:
        for member in self.bot.get_all_members():
            if len(member.roles) > 1:
                for role in member.roles:
                    if role.name == 'game':
                        self.initialize_member_data(member.id)
        print(f"Mining game initialized... with {len(self.member_generators)} members.")

    async def save_data(self):
        """Save game data to file"""
        if len(self.member_generators) > 0:
            save_data = {
                'uptime': self.time_elapsed,
                'world_power_supply': self.world_power_supply,
                'world_power_demand': self.world_power_demand,
                'power_demand_pct': self.power_demand_pct,
                'current_power_price': self.current_power_price,
                'member_generators': self.member_generators,
                'member_miners': self.member_miners,
                'member_materials': self.member_materials,
                'member_achievements': self.member_achievements,
                'member_event_buffs': self.member_event_buffs,
                'member_stats': self.member_stats,
            }
            with open(f'/app/data/{self.qualified_name}_data.json', 'w+') as out_file:
                json.dump(save_data, out_file, sort_keys=False, indent=4)

    async def timeout(self):
        """Main game loop - handles payouts, events, and calculations"""
        if self.time_elapsed >= SMALLEST_PAYMENT_TIMER:
            # Initialize new game members
            for member in self.bot.get_all_members():
                if len(member.roles) > 1:
                    for role in member.roles:
                        if role.name == 'game':
                            self.initialize_member_data(member.id)

            # Calculate world power supply and demand
            self.world_power_supply = BASE_POWER_SUPPLY
            self.world_power_demand = 0
            
            for member_id in self.member_generators:
                power_multiplier, _ = self.apply_event_buffs(member_id)
                for generator in self.member_generators[member_id]:
                    self.world_power_supply += generator['powerGenerated'] * power_multiplier
            
            for member_id in self.member_miners:
                for miner in self.member_miners[member_id]:
                    self.world_power_demand += miner['powerUse']

            # Calculate power price based on supply/demand
            self.power_demand_pct = self.world_power_demand / self.world_power_supply if self.world_power_supply > 0 else 0
            
            if self.power_demand_pct >= 0.99:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER
            elif self.power_demand_pct >= 0.98:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.95
            elif self.power_demand_pct >= 0.97:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.8
            elif self.power_demand_pct >= 0.95:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.66
            elif self.power_demand_pct >= 0.925:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.50
            elif self.power_demand_pct >= 0.90:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.33
            elif self.power_demand_pct >= 0.85:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.25
            elif self.power_demand_pct >= 0.80:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.10
            else:
                self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.05

            # Process each member
            power_bill = f"Power Bills: \n" \
                        f"Supply: `{self.world_power_supply:.2f}` " \
                        f"Demand: `{self.world_power_demand:.2f}` (`{self.power_demand_pct*100:.2f}%`) " \
                        f"Price: `{self.bot.CURRENCY_TOKEN}{self.current_power_price:.2f}`\n"

            for member_id in self.member_generators.keys():
                power_multiplier, payout_multiplier = self.apply_event_buffs(member_id)
                
                # Calculate power generation
                self.member_total_power[member_id] = 0
                for generator in self.member_generators[member_id]:
                    self.member_total_power[member_id] += generator["powerGenerated"] * power_multiplier
                
                # Calculate power consumption and mining payouts
                self.member_total_power_usage[member_id] = 0
                for miner in self.member_miners[member_id]:
                    self.member_total_power_usage[member_id] += miner["powerUse"]
                    miner['sincePayment'] += self.time_elapsed
                    
                    if miner['sincePayment'] >= miner['payoutTimer']:
                        miner["sincePayment"] = 0
                        payout = int(miner["payout"] * payout_multiplier)
                        self.bot.get_cog('Currency').add_user_currency(member_id, payout)
                        
                        # Drop materials on mining payout
                        self.drop_materials(member_id)
                
                # Update stats
                self.member_stats[member_id]["total_power_generated"] += self.member_total_power[member_id]
                
                # Calculate power bill
                member_power = float(self.member_total_power[member_id]) - float(self.member_total_power_usage[member_id])
                if member_power > 0:
                    # Sell excess power
                    power_bill += f"> {str(self.bot.get_user(int(member_id)))} `Sold ${abs(member_power * self.current_power_price):.2f}`\n"
                    self.bot.get_cog('Currency').add_user_currency(member_id, abs(member_power * self.current_power_price))
                elif member_power < 0:
                    # Buy needed power
                    power_bill += f"> {str(self.bot.get_user(int(member_id)))} `Needed ${abs(member_power * self.current_power_price):.2f}`\n"
                    self.bot.get_cog('Currency').remove_user_currency(member_id, abs(member_power * self.current_power_price))
                
                # Check achievements
                self.check_achievements(member_id)

            # Trigger random events
            event_msg = self.trigger_random_event()
            if event_msg:
                power_bill = event_msg + "\n" + power_bill

            # Send power bill to log channel
            log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(power_bill)
            self.time_elapsed = 0
        
        await self.save_data()
        self.time_elapsed += self.bot.TICK_RATE


async def setup(bot):
    await bot.add_cog(MinerGame(bot))