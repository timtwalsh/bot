import json
from datetime import datetime
from json import JSONEncoder
from operator import itemgetter

import discord
import random
from discord.ext import tasks, commands
from discord.utils import get

DEBUG = False
TICK_RATE = 6  # Default
LETTERS_TO_EMOJI_ASCII = {'A': '🇦', 'B': '🇧', 'C': '🇨', 'D': '🇩', 'E': '🇪', 'F': '🇫', 'G': '🇬', 'H': '🇭',
                          'I': '🇮',
                          'J': '🇯', 'K': '🇰', 'L': '🇱', 'M': '🇲', 'N': '🇳', 'O': '🇴', 'P': '🇵', 'Q': '🇶',
                          'R': '🇷',
                          'S': '🇸', 'T': '🇹', 'U': '🇺', 'V': '🇻', 'W': '🇼', 'X': '🇽', 'Y': '🇾', 'Z': '🇿',
                          ' ': '✴'}


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


class Currency(commands.Cog):
    def __init__(self, bot):
        global TICK_RATE
        TICK_RATE = bot.TICK_RATE
        self.bot = bot
        self.member_currency = {}
        # Bonuses - Note: Cumulative - ie 1+0.5+4 = 5;0.5*IDLE_RATE
        self.IDLE_RATE = 25 / 60 / 60 * TICK_RATE  # per hour rate
        self.VOICE_BONUS = 0.25  # (25% while in a voice channel)
        self.ACTIVITY_BONUS = 0.25  # (25% while active)
        self.HAPPY_HOUR_BONUS = 8  # (800% during happy hour)
        self.CARD_COLLECTION_BONUS_PER_UNIQUE = 0.001  # 0.1% bonus per unique card (applied globally to all shekel gains)
        self.time_elapsed = 0

    def get_user_currency(self, user_id=""):
        if user_id != "":
            return self.member_currency[user_id]
        else:
            print("Error, must specify a user_id")
            return False

    def remove_user_currency(self, user_id="", amount=0):
        # Removes currency from user balance, returns true if user has sufficient balance
        if user_id != "":
            if self.member_currency[user_id] >= amount:
                self.member_currency[user_id] -= amount
                return True
            else:
                return False
        else:
            print("Error, must specify a user_id")
            return False

    def add_user_currency(self, user_id="", amount=0):
        # adds currency from user balance, returns true if user has sufficient balance
        if user_id != "":
            if amount > 0:
                # Apply card collection bonus to all currency gains
                card_bonus = self.get_user_card_collection_bonus(user_id)
                bonus_multiplier = 1.0 + card_bonus
                final_amount = amount * bonus_multiplier
                
                self.member_currency[user_id] += final_amount
                return True
            else:
                return False
        else:
            print("Error, must specify a user_id")
            return False

    def get_user_card_collection_bonus(self, user_id):
        """Calculate bonus from unique card collection"""
        try:
            # Get the Magic the Shekelling cog
            magic_cog = self.bot.get_cog('MagicTheShekelling')
            if not magic_cog:
                return 0.0
            
            # Get user's card collection
            user_collections = magic_cog.game.user_collections
            if user_id not in user_collections:
                return 0.0
            
            # Count unique cards (cards with count > 0)
            unique_cards = len([card_id for card_id, count in user_collections[user_id].items() if count > 0])
            
            # Calculate bonus: 0.1% per unique card
            bonus = unique_cards * self.CARD_COLLECTION_BONUS_PER_UNIQUE
            
            return bonus
            
        except Exception as e:
            print(f"Error calculating card collection bonus: {e}")
            return 0.0

    async def load_data(self):
        try:
            with open(f'/app/data/{self.qualified_name}_data.json', 'r+') as in_file:
                data = json.load(in_file)
                self.time_elapsed = data['uptime']
                self.member_currency = data['member_currency']
                print(f"Loaded {len(data['member_currency'])} Members Currency Data.")
        except FileNotFoundError:  # file doesn't exist, init all members with 0 currency to avoid index errors
            for member in self.bot.get_all_members():
                self.member_currency[str(member.id)] = 0

    async def save_data(self):
        if len(self.member_currency) > 0:
            save_data = {'uptime': self.time_elapsed,
                         'member_currency': self.member_currency}
            with open(f'/app/data/{self.qualified_name}_data.json', 'w+') as out_file:
                json.dump(save_data, out_file, sort_keys=False, indent=4)

    @commands.command(name="joingame", aliases=["join"])
    async def join(self, ctx):
        """Joins the Game, allowing currency to be earned."""
        member = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="game")
        print(f"Game Joined by {member} adding role {role}")
        # role = discord.utils.get(member.guild.roles, name="Bots")
        await member.add_roles(role)

    @commands.command(name="mycurrency", aliases=["my$", "my $", "my$hekels", "user$", "user $"])
    async def mycurrency(self, ctx, *, member: discord.Member = None):
        """!my$ or user$ [user] - Shows currency balance and collection bonus"""
        member = member or ctx.author
        user_id = str(member.id)
        currency = self.member_currency[user_id]
        currency_name = self.bot.CURRENCY_NAME if 2 > currency >= 1 else self.bot.CURRENCY_NAME + 's'
        
        # Get card collection bonus
        card_bonus = self.get_user_card_collection_bonus(user_id)
        
        msg = f"{member.mention} has {currency:.3f} {currency_name}"
        
        if card_bonus > 0:
            unique_cards = int(card_bonus / self.CARD_COLLECTION_BONUS_PER_UNIQUE)
            msg += f"\n🎴 Card Collection Bonus: +{card_bonus*100:.1f}% ({unique_cards} unique cards)"
        
        log = await self.bot.get_channel(self.bot.LOG_CHANNEL).send(msg)
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    @commands.command(name="topcurrency", aliases=["top$", "topmoney", "topdollars"])
    async def topcurrency(self, ctx):
        """!top$ - Shows top earners with their collection bonuses"""
        member = self.member_currency.keys()
        cash = self.member_currency.values()
        member_and_cash = list(zip(member, cash))
        member_and_cash = sorted(member_and_cash, key=itemgetter(1, 0), reverse=True)
        member_and_cash = member_and_cash[:10]
        msg = f"{ctx.guild.name} Top {str(self.bot.CURRENCY_NAME).capitalize()} Earners \n```"
        msg += f"{'User':<20.20} | {str(self.bot.CURRENCY_NAME).capitalize():>15}s | {'Card Bonus':>12} |\n"
        msg += f"---------------------|------------------|-------------|\n"
        
        for member_id, cash in member_and_cash:
            user = self.bot.get_user(int(member_id))
            card_bonus = self.get_user_card_collection_bonus(member_id)
            bonus_text = f"+{card_bonus*100:.1f}%" if card_bonus > 0 else "None"
            msg += f"{str(user):<20.20} | {self.bot.CURRENCY_TOKEN}{cash:>15.1f} | {bonus_text:>11} |\n"
        msg += "```"
        
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    @commands.command(name="bonuses", aliases=["mybonuses", "rates"])
    async def view_bonuses(self, ctx, *, member: discord.Member = None):
        """!bonuses - View all active bonuses affecting your shekel generation"""
        member = member or ctx.author
        user_id = str(member.id)
        
        # Base rate
        base_rate_per_hour = (25 / 60 / 60) * 3600  # Convert to per hour for display
        
        embed = discord.Embed(
            title=f"💰 {member.display_name}'s Shekel Generation Bonuses",
            color=0xFFD700
        )
        
        # Current bonuses
        bonuses = []
        total_multiplier = 1.0
        
        # Activity bonus
        if member.activity is not None:
            bonuses.append("🎮 Activity Bonus: +25%")
            total_multiplier += self.ACTIVITY_BONUS
        
        # Voice bonus
        if member.voice is not None:
            bonuses.append("🎤 Voice Channel Bonus: +25%")
            total_multiplier += self.VOICE_BONUS
        
        # Happy hour bonus
        weekday = datetime.today().weekday()
        hour = datetime.today().hour + datetime.today().minute / 60
        if weekday >= 5 or (18 <= hour < 24):
            bonuses.append("🎉 Happy Hour Bonus: +800%")
            total_multiplier += self.HAPPY_HOUR_BONUS
        
        # Card collection bonus
        card_bonus = self.get_user_card_collection_bonus(user_id)
        if card_bonus > 0:
            unique_cards = int(card_bonus / self.CARD_COLLECTION_BONUS_PER_UNIQUE)
            bonuses.append(f"🎴 Card Collection Bonus: +{card_bonus*100:.1f}% ({unique_cards} unique cards)")
            total_multiplier += card_bonus
        
        # Display bonuses
        if bonuses:
            embed.add_field(name="🔥 Active Bonuses", value="\n".join(bonuses), inline=False)
        else:
            embed.add_field(name="🔥 Active Bonuses", value="None currently active", inline=False)
        
        # Rate calculations
        current_rate = base_rate_per_hour * total_multiplier
        embed.add_field(name="⚡ Base Rate", value=f"{base_rate_per_hour:.2f} {self.bot.CURRENCY_NAME}s/hour", inline=True)
        embed.add_field(name="🚀 Current Rate", value=f"{current_rate:.2f} {self.bot.CURRENCY_NAME}s/hour", inline=True)
        embed.add_field(name="📈 Total Multiplier", value=f"{total_multiplier:.2f}x", inline=True)
        
        embed.set_footer(text="💰 Card collection bonus is permanent and grows with your collection!")
        
        await ctx.send(embed=embed, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    async def timeout(self):
        debug_channel = self.bot.get_channel(self.bot.DEBUG_CHANNEL)
        log_channel = self.bot.get_channel(self.bot.LOG_CHANNEL)
        if not self.bot.is_closed() and len(self.member_currency) > 0:
            for member in self.bot.get_all_members():
                if len(member.roles) > 1:
                    for role in member.roles:
                        if role.name == 'game':
                            if str(member.id) not in self.member_currency.keys():
                                print("New Member:", member)
                                self.member_currency[str(member.id)] = 0.0
                                current_member_currency = 0.0
                            else:
                                current_member_currency = self.member_currency[str(member.id)]
                            
                            # Apply Activity Bonuses to encourage member participation
                            cumulative_activity_bonus = 1
                            
                            if member.activity is not None:
                                cumulative_activity_bonus += self.ACTIVITY_BONUS
                            if member.voice is not None:
                                cumulative_activity_bonus += self.VOICE_BONUS

                            # Apply Happy Hour Bonus, 6pm-midnight on weekdays, all hours on Saturday/Sunday
                            weekday = datetime.today().weekday()
                            hour = datetime.today().hour + datetime.today().minute / 60
                            if weekday >= 5:
                                cumulative_activity_bonus += self.HAPPY_HOUR_BONUS
                            else:
                                if 18 <= hour < 24:
                                    cumulative_activity_bonus += self.HAPPY_HOUR_BONUS
                            
                            # Card collection bonus is now applied globally in add_user_currency
                            idle_gain = self.IDLE_RATE * cumulative_activity_bonus
                            self.add_user_currency(str(member.id), idle_gain)
                            
                            if DEBUG:
                                card_bonus = self.get_user_card_collection_bonus(str(member.id))
                                unique_cards = int(card_bonus / self.CARD_COLLECTION_BONUS_PER_UNIQUE) if card_bonus > 0 else 0
                                print(f"{member.id},{member},{self.member_currency[str(member.id)]:.3f},+{card_bonus*100:.1f}%({unique_cards} cards)")
                                
            await self.save_data()
            self.time_elapsed += TICK_RATE


async def setup(bot):
    await bot.add_cog(Currency(bot))