import asyncio
import json
from json import JSONEncoder

import discord
import random
from discord.ext import tasks, commands

DEBUG = False
DEBUG_TICKER = False
TICK_RATE = 6
LETTERS_TO_EMOJI_ASCII = {'A': '🇦', 'B': '🇧', 'C': '🇨', 'D': '🇩', 'E': '🇪', 'F': '🇫', 'G': '🇬', 'H': '🇭',
                          'I': '🇮',
                          'J': '🇯', 'K': '🇰', 'L': '🇱', 'M': '🇲', 'N': '🇳', 'O': '🇴', 'P': '🇵', 'Q': '🇶',
                          'R': '🇷',
                          'S': '🇸', 'T': '🇹', 'U': '🇺', 'V': '🇻', 'W': '🇼', 'X': '🇽', 'Y': '🇾', 'Z': '🇿',
                          ' ': '✴'}

MINING_SOURCES = {
    "idle": {"name": "Idle GPU Miner", "costIncrease": 1.1, "payoutTimer": 60, "payoutTimerEnglish": "/m", "price": 150,
             "description": "!buy idle",
             "payout": 1,
             "powerUse": 1.44, "sincePayment": 0},
    "asic": {"name": "ASIC Miner", "costIncrease": 1.15, "payoutTimer": 600, "payoutTimerEnglish": "/10m", "price": 1525,
             "description": "!buy asic",
             "payout": 15,
             "powerUse": 2.16, "sincePayment": 0},
    "rack": {"name": "Rack of Miners", "costIncrease": 1.25, "payoutTimer": 3600, "payoutTimerEnglish": "/h",
             "price": 7500,
             "description": "!buy rack",
             "payout": 150, "powerUse": 13.6, "sincePayment": 0},
    "dcf": {"name": "DCF Container", "costIncrease": 1.33, "payoutTimer": 43200, "payoutTimerEnglish": "/12h",
            "price": 15000,
            "description": "!buy dcf",
            "payout": 2500, "powerUse": 27.2, "sincePayment": 0}
}
POWER_SOURCES = {
    "panel": {"name": "Solar Panel", "costIncrease": 1.5, "timer": 60, "description": "!buy panel", "price": 500,
              "powerGenerated": 1.15},
    "petrol": {"name": "Petrol Generator", "costIncrease": 2, "timer": 60, "price": 1200,
               "description": "!buy petrol", "powerGenerated": 2},
    "farm": {"name": "Solar Farm", "costIncrease": 1.5, "timer": 60, "description": "!buy farm", "price": 9000,
             "powerGenerated": 15},
    "gas": {"name": "Gas Generator", "costIncrease": 2.5, "timer": 60, "price": 15000,
            "description": "!buy gas", "powerGenerated": 30}
}

SMALLEST_PAYMENT_TIMER = 60
BASE_POWER_SUPPLY = 1
POWER_EXPORT_BASE_VALUE = 0.008
MAXIMUM_EXPORT_MULTIPLIER = 96
POWER_PAYMENT_FREQUENCY = 60

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

    @commands.command(name="my#")
    async def mybase(self, ctx, member: discord.Member = None):
        """!my# - displays all resources"""
        i = 0
        member = member or ctx.author
        print(self.member_total_power_usage)
        print(self.member_total_power)
        print(member.id)
        msg = f"{member.name}'s Base - Last Power Bill - Supply: `{self.member_total_power[str(member.id)]:.2f}kW-h` Demand: `{self.member_total_power_usage[str(member.id)]:.2f}kW-h`\n```"
        user_generators = self.member_generators[str(member.id)]
        user_miners = self.member_miners[str(member.id)]
        msg += f" #   | Resource Type        | Created          | Used          |\n"
        msg += f"-----|----------------------|------------------|---------------|\n"
        if len(user_generators) > 0:
            msg += f"----- Power Generators ----------------------------------------|\n"
            for generator in POWER_SOURCES.keys():
                count = 0
                for user_generator in user_generators:
                    if user_generator['name'] == POWER_SOURCES[generator]['name']:
                        count += 1
                msg += f" {count:<3} | {POWER_SOURCES[generator]['name']:<20} | {POWER_SOURCES[generator]['powerGenerated'] * count:>8.2f}{' kW-h':<8} |{'|':>16}\n"
        if len(user_miners) > 0:
            msg += f"----- Miners --------------------------------------------------|\n"
            for miner in MINING_SOURCES.keys():
                count = 0
                for mining_device in user_miners:
                    print(f"{mining_device['name']} == {MINING_SOURCES[miner]['name']}")
                    if mining_device['name'] == MINING_SOURCES[miner]['name']:
                        count += 1
                msg += f" {count:<3} | {MINING_SOURCES[miner]['name']:<20} | {MINING_SOURCES[miner]['payout'] * count:>8}{MINING_SOURCES[miner]['payoutTimerEnglish']:<8} | {MINING_SOURCES[miner]['powerUse'] * count:>7.2f} kW-h  |\n"
        msg += "```"
        i += 1
        print(i)
        log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(msg)
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    @commands.command(name="power")
    async def power(self, ctx, *, member: discord.Member = None):
        """shows world power grid details"""
        member = member or ctx.author
        print(member)
        print('world_power_demand',self.world_power_demand)
        print('world_power_supply',self.world_power_supply)
        print('current_power_price',self.current_power_price)
        power_supply = self.member_total_power[str(member.id)]
        print('power_supply', power_supply)
        power_usage = self.member_total_power_usage[str(member.id)]
        print('power_usage', power_usage)
        power_pct = 0
        if power_usage > 0:
            if power_supply > 0:
                power_pct = power_usage / power_supply
            else:
                power_pct = 0
        else:
            if power_supply > 0:
                power_pct = 0
        print('power_pct',power_pct)
        msg = f"World Supply: `{self.world_power_supply:.1f} kW-h`, World Demand: `{self.world_power_demand:.1f} kW-h`, Price: `{self.bot.CURRENCY_TOKEN}{self.current_power_price:.2f}/kW-h`\n"
        print(msg)
        msg += f"{member.mention} - Supply: `{power_supply:.1f}kW-h` Demand: `{power_usage:.1f}kW-h` (`{power_pct * 100:.1f}%`)"
        log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(msg)
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    async def buy_miner(self, user_id="", item_name=""):
        """ Buys miner, removes currency from user balance, returns true if purchase completed """
        user_miners = self.member_miners[user_id]
        item_count = 0
        item = MINING_SOURCES[item_name]['name']
        for miner in user_miners:
            if miner["name"] == item:
                item_count += 1
        price = compounding_increase(MINING_SOURCES[item_name]['price'], (MINING_SOURCES[item_name]['costIncrease']),
                                     item_count)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        if float(user_balance) >= float(price):
            self.member_miners[user_id].append(MINING_SOURCES[item_name])
            self.bot.get_cog('Currency').remove_user_currency(user_id, abs(float(price)))
            return f"Purchased {MINING_SOURCES[item_name]['name']} for {self.bot.CURRENCY_TOKEN}{price:.1f} now has {item_count + 1} "
        return f"You need {price} to buy {MINING_SOURCES[item_name]['name']}"

    async def buy_generator(self, user_id="", item_name=""):
        """ Buys power source, removes currency from user balance, returns true if purchase completed """
        user_generators = self.member_generators[user_id]
        item_count = 0
        item = POWER_SOURCES[item_name]['name']
        for power in user_generators:
            if power["name"] == item:
                item_count += 1
        price = compounding_increase(POWER_SOURCES[item_name]['price'], (POWER_SOURCES[item_name]['costIncrease']),
                                     item_count)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        if float(user_balance) >= float(price):
            self.member_generators[user_id].append(POWER_SOURCES[item_name])
            self.bot.get_cog('Currency').remove_user_currency(user_id, abs(float(price)))
            return f"Purchased {POWER_SOURCES[item_name]['name']} for {self.bot.CURRENCY_TOKEN}{price:.1f} now has {item_count + 1} "
        return f"You need {price} to buy {POWER_SOURCES[item_name]['name']}"

    @commands.command(name="buy")
    async def buy(self, ctx, item_name: str = ""):
        """!buy [type] - buys power/mining items"""
        user_id = str(ctx.author.id)
        item_name = str(item_name).lower()
        outcome = f"{ctx.author.name} - "
        print(ctx.author.name, item_name)
        if item_name in MINING_SOURCES.keys():
            print('MINER PURCHASE!')
            outcome += await self.buy_miner(user_id=user_id, item_name=item_name)
        elif item_name in POWER_SOURCES.keys():
            print('POWER SOURCE PURCHASE!')
            outcome += await self.buy_generator(user_id=user_id, item_name=item_name)
        else:
            outcome += f"Invalid item- Current Items..."
            outcome += "```"
            outcome += f" Resource Type      | Produces         | Uses       | Command      | Your Price   |\n"
            outcome += f"--------------------|------------------|------------|--------------|--------------|\n"
            outcome += f"- Power Generation ---------------------------------------------------------------|\n"
            for (key, item) in POWER_SOURCES.items():
                outcome += f" {POWER_SOURCES[key]['name']:<18} | {POWER_SOURCES[key]['powerGenerated']:>9.2f} {'kW-h':<6} | {'|':>12} {POWER_SOURCES[key]['description']:<13}| ${POWER_SOURCES[key]['price']:^12.2f}|\n"
            outcome += f"- Miners -------------------------------------------------------------------------|\n"
            for (key, item) in MINING_SOURCES.items():
                outcome += f" {MINING_SOURCES[key]['name']:<18} | {MINING_SOURCES[key]['payout']:>8} {MINING_SOURCES[key]['payoutTimerEnglish']:<7} | {MINING_SOURCES[key]['powerUse']:>6.2f}kW-h | {MINING_SOURCES[key]['description']:<13}| ${MINING_SOURCES[key]['price']:^12.2f}|\n"
            outcome += "``` Eg '!buy idle' or '!buy panel'"
        await ctx.channel.send(outcome, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(outcome)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        await self.save_data()

    async def load_data(self):
        print(f"Loading Mining game data...")
        try:
            with open(f'/app/data/{self.qualified_name}_data.json', 'r+') as in_file:
                data = json.load(in_file)
                self.time_elapsed = data['uptime']
                self.world_power_supply = data['world_power_supply']
                self.world_power_demand = data['world_power_demand']
                self.power_demand_pct = data['power_demand_pct']
                self.current_power_price = data['current_power_price']
                self.member_generators = data['member_generators']
                self.member_miners = data['member_miners']
                print(f"Loaded {len(data['member_generators'])} Members Idle Game Data.")
        except FileNotFoundError:  # file doesn't exist, init all members with 0 currency to avoid index errors
            for member in self.bot.get_all_members():
                if len(member.roles) > 1:
                    for role in member.roles:
                        if role.name == 'game':
                            self.member_generators[member.id] = []
                            self.member_miners[member.id] = []
            print(f"Mining game initialized... with {len(self.member_generators)} members.")

    async def save_data(self):
        if len(self.member_generators) > 0:
            save_data = {'uptime': self.time_elapsed,
                         'world_power_supply': self.world_power_supply,
                         'world_power_demand': self.world_power_demand,
                         'power_demand_pct': self.power_demand_pct,
                         'current_power_price': self.current_power_price,
                         'member_generators': self.member_generators,
                         'member_miners': self.member_miners,
                         }
            with open(f'/app/data/{self.qualified_name}_data.json', 'w+') as out_file:
                json.dump(save_data, out_file, sort_keys=False, indent=4)

    async def timeout(self):
        if self.time_elapsed >= SMALLEST_PAYMENT_TIMER:
            for member in self.bot.get_all_members():  # add new game members
                if len(member.roles) > 1:
                    for role in member.roles:
                        if role.name == 'game':
                            if str(member.id) not in self.member_generators.keys():  # init new members
                                self.member_generators[str(member.id)] = []
                                self.member_miners[str(member.id)] = []
                                self.member_total_power[str(member.id)] = 0.0
                                self.member_total_power_usage[str(member.id)] = 0.0
                                print("New Member:", member)
            self.world_power_supply = BASE_POWER_SUPPLY
            self.world_power_demand = 0
            for member in self.member_generators:
                for generator in self.member_generators[member]:
                    self.world_power_supply += generator['powerGenerated']
            for member in self.member_miners:
                for miner in self.member_miners[member]:
                    self.world_power_demand += miner['powerUse']
            if DEBUG:
                print(f"world power calc outcome: sup: {self.world_power_supply} / dem: {self.world_power_demand}")
            self.current_power_price = POWER_EXPORT_BASE_VALUE  # default
            self.power_demand_pct = self.world_power_demand / self.world_power_supply
            print('self.power_demand_pct', self.power_demand_pct)
            print('before self.current_power_price', self.current_power_price)
            print(self.power_demand_pct >= 0.99)
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

            print('after self.current_power_price', self.current_power_price)
            for member_id in self.member_generators.keys():  # calc count generation and usage
                if len(self.member_generators[member_id]) > 0:
                    if DEBUG:
                        print(
                            f"Power Demand: {self.world_power_demand} Supply: {self.world_power_supply} Old Price: {self.current_power_price}",
                            sep=" ")
            if DEBUG:
                print(f"Power Usage {self.power_demand_pct * 100}% New Price: {self.current_power_price}")
            power_bill = f"Power Bills: \n" \
                         f"Supply: `{self.world_power_supply:.2f}` " \
                         f"Demand: `{self.world_power_demand:.2f}` (`{self.power_demand_pct*100:.2f}%`) " \
                        f"Price: `{self.bot.CURRENCY_TOKEN}{self.current_power_price:.2f}`\n"
            for member_id in self.member_generators.keys():
                # generate
                self.member_total_power[member_id] = 0
                count = 0
                for generator in self.member_generators[member_id]:
                    count += 1
                    self.member_total_power[member_id] += generator["powerGenerated"]
                if DEBUG and self.member_total_power[member_id] > 0:
                    print(f"{member_id} - Total: {self.member_total_power[member_id]} count:{count}")
                # consume
                self.member_total_power_usage[member_id] = 0
                for miner in self.member_miners[member_id]:
                    self.member_total_power_usage[member_id] += miner["powerUse"]
                    miner['sincePayment'] += self.time_elapsed
                    if miner['sincePayment'] >= miner['payoutTimer']:
                        miner["sincePayment"] = 0
                        print(f"PAYOUT TIME: {member_id}, {miner['payout']}")
                        self.bot.get_cog('Currency').add_user_currency(member_id, miner["payout"])
                # calculate difference and power payment
                member_power = float(self.member_total_power[member_id]) - float(self.member_total_power_usage[member_id])
                if member_power > 0:
                    # sell power
                    power_bill += f"> {str(self.bot.get_user(int(member_id)))} `Sold ${abs(member_power * self.current_power_price):.2f}`\n"
                    self.bot.get_cog('Currency').add_user_currency(member_id, abs(member_power * self.current_power_price))
                elif member_power < 0:
                    # buy power
                    power_bill += f"> {str(self.bot.get_user(int(member_id)))} `Needed ${abs(member_power * self.current_power_price):.2f}`\n"
                    self.bot.get_cog('Currency').remove_user_currency(member_id, abs(member_power * self.current_power_price))
            print(f"log... {power_bill}")
            log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(power_bill)
            self.time_elapsed = 0
        await self.save_data()
        self.time_elapsed += self.bot.TICK_RATE


async def setup(bot):
    await bot.add_cog(MinerGame(bot))
