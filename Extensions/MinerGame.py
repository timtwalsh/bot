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

# Mining sources
MINING_SOURCES = {
    "idle": {"name": "Idle GPU Miner", "costIncrease": 1.1, "payoutTimer": 60, "payoutTimerEnglish": "/m", "price": 150,
             "description": "!buy idle", "payout": 1, "powerUse": 1.44, "sincePayment": 0, "tier": 1},
    "asic": {"name": "ASIC Miner", "costIncrease": 1.15, "payoutTimer": 600, "payoutTimerEnglish": "/10m", "price": 1525,
             "description": "!buy asic", "payout": 15, "powerUse": 2.16, "sincePayment": 0, "tier": 2},
    "rack": {"name": "Rack of Miners", "costIncrease": 1.25, "payoutTimer": 3600, "payoutTimerEnglish": "/h",
             "price": 7500, "description": "!buy rack", "payout": 150, "powerUse": 13.6, "sincePayment": 0, "tier": 3},
    "dcf": {"name": "DCF Container", "costIncrease": 1.33, "payoutTimer": 43200, "payoutTimerEnglish": "/12h",
            "price": 15000, "description": "!buy dcf", "payout": 2500, "powerUse": 21.0, "sincePayment": 0, "tier": 4}
}

POWER_SOURCES = {
    "panel": {"name": "Solar Panel", "costIncrease": 1.5, "timer": 60, "description": "!buy panel", "price": 500,
              "powerGenerated": 1.15, "tier": 1},
    "petrol": {"name": "Petrol Generator", "costIncrease": 2, "timer": 60, "price": 1200,
               "description": "!buy petrol", "powerGenerated": 2.75, "tier": 2},
    "farm": {"name": "Solar Farm", "costIncrease": 1.5, "timer": 60, "description": "!buy farm", "price": 9000,
             "powerGenerated": 15, "tier": 3},
    "gas": {"name": "Gas Generator", "costIncrease": 2.5, "timer": 60, "price": 15000,
            "description": "!buy gas", "powerGenerated": 30, "tier": 4}
}



BASE_POWER_SUPPLY = 10
POWER_EXPORT_BASE_VALUE = 0.007
MAXIMUM_EXPORT_MULTIPLIER = 6000
POWER_PAYMENT_FREQUENCY = 600  # Power bills every 10min
SELL_MULTIPLIER = 0  # 80% sell value
TIMEOUT_LOOP_FREQUENCY = 60

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
        self.world_power_supply = BASE_POWER_SUPPLY
        self.world_power_demand = 0
        self.power_demand_pct = 0
        self.current_power_price = POWER_EXPORT_BASE_VALUE
        self.member_generators = {}
        self.member_miners = {}
        self.member_total_power = {}
        self.member_total_power_usage = {}
        self.member_stats = {}
        self.time_since_power_processing = 0
        
        # Start the game loop
        self.game_loop.start()

    def cog_unload(self):
        """Clean up when the cog is unloaded"""
        self.game_loop.cancel()

    @tasks.loop(seconds=TIMEOUT_LOOP_FREQUENCY)
    async def game_loop(self):
        """Main game loop TASK_LOOP_RATE seconds"""
        try:
            await self.game_timeout()
        except Exception as e:
            print(f"Error in game loop: {e}")
            import traceback
            traceback.print_exc()

    @game_loop.before_loop
    async def before_game_loop(self):
        """Wait for bot to be ready before starting the loop"""
        await self.bot.wait_until_ready()
        await self.load_data()

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
        if member_id not in self.member_stats:
            self.member_stats[member_id] = {
                "total_power_generated": 0,
                "items_sold": 0
            }

    @commands.command(name="destroy")
    async def destroy(self, ctx, item_type: str = "", item_name: str = ""):
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

    @commands.command(name="my#")
    async def mybase(self, ctx, member: discord.Member = None):
        """!my# - displays all resources"""
        member = member or ctx.author
        user_id = str(member.id)
        self.initialize_member_data(user_id)
        try: 
            msg = f"{member.name}'s Base - Last Power Bill - Supply: `{self.member_total_power[user_id]:.2f}kW-h` Demand: `{self.member_total_power_usage[user_id]:.2f}kW-h`\n```"
            user_generators = self.member_generators[user_id]
            user_miners = self.member_miners[user_id]
            msg += f" #   | Resource Type        | Created          | Used          |\n"
            msg += f"-----|----------------------|------------------|---------------|\n"
            
            if len(user_generators) > 0:
                msg += f"-----| Power Generators ----|------------------|---------------|\n"
                for generator in POWER_SOURCES.keys():
                    count = 0
                    total_power = 0
                    for user_generator in user_generators:
                        if user_generator['name'] == POWER_SOURCES[generator]['name']:
                            count += 1
                            total_power += user_generator['powerGenerated']
                    if count > 0:
                        msg += f" {count:<3} | {POWER_SOURCES[generator]['name']:<20} | {total_power:>8.2f}{' kW-h':<8} |{'|':>16}\n"
            
            if len(user_miners) > 0:
                msg += f"-----| Miners --------------|------------------|---------------|\n"
                for miner in MINING_SOURCES.keys():
                    count = 0
                    total_payout = 0
                    total_power_use = 0
                    for mining_device in user_miners:
                        if mining_device['name'] == MINING_SOURCES[miner]['name']:
                            count += 1
                            total_payout += mining_device['payout']
                            total_power_use += mining_device['powerUse']
                    if count > 0:
                        msg += f" {count:<3} | {MINING_SOURCES[miner]['name']:<20} | {total_payout:>8}{MINING_SOURCES[miner]['payoutTimerEnglish']:<8} | {total_power_use:>7.2f} kW-h  |\n"
                daily_income = sum(
                    (miner['payout'] * (86400 / miner['payoutTimer']))
                    for miner in user_miners
                )
                msg += f"     | Total Miner Income   | {daily_income:>8.0f}/day     | \n"




            msg += "```"
            
            await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        except Exception as e:
            print(f"Error displaying base: {e}")

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
            self.member_miners[user_id].append(new_miner)
            self.bot.get_cog('Currency').remove_user_currency(user_id, abs(float(price)))
            
            msg = f"Purchased {MINING_SOURCES[item_name]['name']} for {self.bot.CURRENCY_TOKEN}{price:.1f} now has {item_count + 1}"
            
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
            outcome += f"--------------------|------------------|------------|--------------|--------------|--------------|\n"
            outcome += f"- Power Generation ------------------------------------------------------------------------------|\n"
            for (key, item) in POWER_SOURCES.items():
                user_count = sum(1 for gen in self.member_generators[user_id] if gen['name'] == item['name'])
                buy_price = compounding_increase(item['price'], item['costIncrease'], user_count)
                sell_price = self.get_item_sell_price(key, "power", user_count) if user_count > 0 else 0
                outcome += f" {item['name']:<18} | {item['powerGenerated']:>9.2f} {'kW-h':<6} | {'|':>12} {item['description']:<13}| ${buy_price:^12.2f}| ${sell_price:^11.2f}|\n"
            outcome += f"- Miners ----------------------------------------------------------------------------------------|\n"
            for (key, item) in MINING_SOURCES.items():
                user_count = sum(1 for miner in self.member_miners[user_id] if miner['name'] == item['name'])
                buy_price = compounding_increase(item['price'], item['costIncrease'], user_count)
                sell_price = self.get_item_sell_price(key, "miner", user_count) if user_count > 0 else 0
                outcome += f" {item['name']:<18} | {item['payout']:>8} {item['payoutTimerEnglish']:<7} | {item['powerUse']:>6.2f}kW-h | {item['description']:<13}| ${buy_price:^12.2f}| ${sell_price:^11.2f}|\n"
            outcome += "```"
            outcome += "Commands: !buy [item], !sell [item]"
        
        await ctx.channel.send(outcome, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        await self.save_data()

    async def process_power_bills(self):
        """Process power bills - called exactly once per minute"""
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
            for generator in self.member_generators[member_id]:
                self.world_power_supply += generator['powerGenerated']
        
        for member_id in self.member_miners:
            for miner in self.member_miners[member_id]:
                self.world_power_demand += miner['powerUse']

        # Calculate power price based on supply/demand
        self.power_demand_pct = self.world_power_demand / self.world_power_supply if self.world_power_supply > 0 else 0
        
        if self.power_demand_pct >= 2:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER
        elif self.power_demand_pct >= 1.75:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.90
        elif self.power_demand_pct >= 1.5:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.75
        elif self.power_demand_pct >= 1.25:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.5
        elif self.power_demand_pct >= 1:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.25
        elif self.power_demand_pct >= 0.90:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.165
        elif self.power_demand_pct >= 0.70:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.0825
        elif self.power_demand_pct >= 0.50:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.04125
        else:
            self.current_power_price = POWER_EXPORT_BASE_VALUE * MAXIMUM_EXPORT_MULTIPLIER * 0.025

        # Build power bill message
        power_bill = f"Power Bills: \n" \
                    f"Supply: `{self.world_power_supply:.2f}` " \
                    f"Demand: `{self.world_power_demand:.2f}` (`{self.power_demand_pct*100:.2f}%`) " \
                    f"Price: `{self.bot.CURRENCY_TOKEN}{self.current_power_price:.2f}`\n"

        # Get all members who have either generators or miners
        all_active_members = set(self.member_generators.keys()) | set(self.member_miners.keys())
        
        # Process each member's power bills
        for member_id in all_active_members:
            try:
                # Calculate power generation
                self.member_total_power[member_id] = 0
                if member_id in self.member_generators:
                    for generator in self.member_generators[member_id]:
                        self.member_total_power[member_id] += generator["powerGenerated"]
                
                # Calculate power consumption
                self.member_total_power_usage[member_id] = 0
                if member_id in self.member_miners:
                    for miner in self.member_miners[member_id]:
                        self.member_total_power_usage[member_id] += miner["powerUse"]
                
                # Update stats
                power_generated_this_cycle = self.member_total_power[member_id] * (POWER_PAYMENT_FREQUENCY / 3600)  # Convert to kW-h
                self.member_stats[member_id]["total_power_generated"] += power_generated_this_cycle
                member_power = float(self.member_total_power[member_id]) - float(self.member_total_power_usage[member_id])
                if member_power > 0:
                    # Sell excess power
                    hourly_rate = member_power * self.current_power_price
                    actual_payment = abs(member_power * self.current_power_price * (POWER_PAYMENT_FREQUENCY / 3600))
                    power_bill += f"> {str(self.bot.get_user(int(member_id)))} `Earned ${actual_payment:.3f} for {POWER_PAYMENT_FREQUENCY/60:.0f}m of power production. (${hourly_rate:.2f}/hr)`\n"
                    self.bot.get_cog('Currency').add_user_currency(member_id, actual_payment)
                elif member_power < 0:
                    # Buy needed power
                    hourly_rate = abs(member_power) * self.current_power_price
                    actual_cost = abs(member_power * self.current_power_price * (POWER_PAYMENT_FREQUENCY / 3600))
                    power_bill += f"> {str(self.bot.get_user(int(member_id)))} `Spent ${actual_cost:.3f} for {POWER_PAYMENT_FREQUENCY/60:.0f}m of power usage. (${hourly_rate:.2f}/hr)`\n"
                    self.bot.get_cog('Currency').remove_user_currency(member_id, actual_cost)
                
            except Exception as e:
                print(f"Error processing member {member_id}: {e}")
                continue

        # Send power bill to log channel only once per cycle
        try:
            log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(power_bill)
            await log.delete(delay=1200)
            if DEBUG:
                print(f"Power bill sent at {datetime.now()}")
        except Exception as e:
            print(f"Could not send to log channel: {e}")

    async def process_mining_payouts(self):
        """Process mining payouts - called every TIMEOUT_LOOP_FREQUENCY seconds"""
        # Get all members who have miners
        for member_id in self.member_miners:
            try:
                for miner in self.member_miners[member_id]:
                    miner['sincePayment'] += TIMEOUT_LOOP_FREQUENCY
                    
                    # Check if miner should pay out
                    if miner['sincePayment'] >= miner['payoutTimer']:
                        miner["sincePayment"] = 0
                        payout = miner["payout"]
                        print(f"Member {member_id} was paid {payout} for {miner['name']}")
                        self.bot.get_cog('Currency').add_user_currency(member_id, payout)
                        
            except Exception as e:
                print(f"Error processing mining payouts for member {member_id}: {e}")
                continue

    async def load_data(self):
        """Load game data from file"""
        print(f"Loading Mining game data...")
        try:
            with open(f'/app/data/{self.qualified_name}_data.json', 'r+') as in_file:
                data = json.load(in_file)
                self.world_power_supply = data.get('world_power_supply', BASE_POWER_SUPPLY)
                self.world_power_demand = data.get('world_power_demand', 0)
                self.power_demand_pct = data.get('power_demand_pct', 0)
                self.current_power_price = data.get('current_power_price', POWER_EXPORT_BASE_VALUE)
                self.member_generators = data.get('member_generators', {})
                self.member_miners = data.get('member_miners', {})
                self.member_total_power = data.get('member_total_power', {})
                self.member_total_power_usage = data.get('member_total_power_usage', {})
                self.member_stats = data.get('member_stats', {})
                print(f"Loaded {len(self.member_generators)} Members Idle Game Data.")
        except FileNotFoundError:
            for member in self.bot.get_all_members():
                if len(member.roles) > 1:
                    for role in member.roles:
                        if role.name == 'game':
                            self.initialize_member_data(member.id)
            print(f"Mining game initialized... with {len(self.member_generators)} members.")
        except Exception as e:
            print(f"Error loading mining game data: {e}")

    async def save_data(self):
        """Save game data to file"""
        try:
            if len(self.member_generators) > 0:
                save_data = {
                    'world_power_supply': self.world_power_supply,
                    'world_power_demand': self.world_power_demand,
                    'power_demand_pct': self.power_demand_pct,
                    'current_power_price': self.current_power_price,
                    'member_generators': self.member_generators,
                    'member_miners': self.member_miners,
                    'member_total_power': self.member_total_power,
                    'member_total_power_usage': self.member_total_power_usage,
                    'member_stats': self.member_stats,
                }
                
                # Ensure data directory exists
                import os
                os.makedirs('/app/data', exist_ok=True)
                
                with open(f'/app/data/{self.qualified_name}_data.json', 'w+') as out_file:
                    json.dump(save_data, out_file, sort_keys=False, indent=4)
                    
        except Exception as e:
            print(f"Error saving mining game data: {e}")

    async def game_timeout(self):
        """Main game loop - handles power bills and mining payouts every 60 seconds"""
        # Process mining payouts
        await self.process_mining_payouts()
        # Process power bills every 60 seconds
        self.time_since_power_processing += TIMEOUT_LOOP_FREQUENCY
        if (self.time_since_power_processing >= POWER_PAYMENT_FREQUENCY):
            print(f"Power bill processed at {datetime.now()}")
            await self.process_power_bills()
            self.time_since_power_processing = 0
        if DEBUG:
            print(f"Power bill processed at {datetime.now()}")
        
        # Always save data to prevent loss
        await self.save_data()

async def setup(bot):
    await bot.add_cog(MinerGame(bot))


