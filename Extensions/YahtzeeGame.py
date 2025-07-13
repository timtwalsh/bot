import asyncio
import random
from collections import defaultdict, Counter
import discord
from discord.ext import commands
from discord_ui import Button, SelectMenu, SelectOption, UI

DEBUG = False
TICK_RATE = 6  # Default

# ASCII Art for dice faces
DICE_ART = {
    1: ["┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"],
    2: ["┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"],
    3: ["┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"],
    4: ["┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"],
    5: ["┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"],
    6: ["┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"]
}

# Yahtzee scoring categories
SCORING_CATEGORIES = {
    'ones': 'Ones',
    'twos': 'Twos',
    'threes': 'Threes',
    'fours': 'Fours',
    'fives': 'Fives',
    'sixes': 'Sixes',
    'three_of_a_kind': 'Three of a Kind',
    'four_of_a_kind': 'Four of a Kind',
    'full_house': 'Full House',
    'small_straight': 'Small Straight',
    'large_straight': 'Large Straight',
    'yahtzee': 'YAHTZEE!',
    'chance': 'Chance'
}

YAHTZEE_HEADER = [
    "██╗   ██╗ █████╗ ██╗  ██╗████████╗███████╗███████╗███████╗",
    "╚██╗ ██╔╝██╔══██╗██║  ██║╚══██╔══╝╚══███╔╝██╔════╝██╔════╝",
    " ╚████╔╝ ███████║███████║   ██║     ███╔╝ █████╗  █████╗  ",
    "  ╚██╔╝  ██╔══██║██╔══██║   ██║    ███╔╝  ██╔══╝  ██╔══╝  ",
    "   ██║   ██║  ██║██║  ██║   ██║   ███████╗███████╗███████╗",
    "   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝╚══════╝"
]

def format_dice_display(dice_values):
    """Format dice in a side-by-side ASCII display"""
    dice_lines = [[] for _ in range(5)]
    
    for value in dice_values:
        for i, line in enumerate(DICE_ART[value]):
            dice_lines[i].append(line)
    
    # Join dice horizontally with spacing
    formatted_lines = []
    for line_parts in dice_lines:
        formatted_lines.append("  ".join(line_parts))
    
    return "\n".join(formatted_lines)

def calculate_score(dice, category):
    """Calculate score for a given category"""
    counts = Counter(dice)
    dice_sum = sum(dice)
    
    if category == 'ones':
        return dice.count(1) * 1
    elif category == 'twos':
        return dice.count(2) * 2
    elif category == 'threes':
        return dice.count(3) * 3
    elif category == 'fours':
        return dice.count(4) * 4
    elif category == 'fives':
        return dice.count(5) * 5
    elif category == 'sixes':
        return dice.count(6) * 6
    elif category == 'three_of_a_kind':
        return dice_sum if any(count >= 3 for count in counts.values()) else 0
    elif category == 'four_of_a_kind':
        return dice_sum if any(count >= 4 for count in counts.values()) else 0
    elif category == 'full_house':
        return 25 if (3 in counts.values() and 2 in counts.values()) else 0
    elif category == 'small_straight':
        # Check for consecutive sequences of 4
        sorted_dice = sorted(set(dice))
        for i in range(len(sorted_dice) - 3):
            if sorted_dice[i:i+4] == list(range(sorted_dice[i], sorted_dice[i] + 4)):
                return 30
        return 0
    elif category == 'large_straight':
        # Check for consecutive sequences of 5
        sorted_dice = sorted(dice)
        return 40 if sorted_dice == [1,2,3,4,5] or sorted_dice == [2,3,4,5,6] else 0
    elif category == 'yahtzee':
        return 50 if len(set(dice)) == 1 else 0
    elif category == 'chance':
        return dice_sum
    
    return 0
 


class YahtzeeGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.ui = UI(bot)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.custom_id.startswith("yahtzee_die_"):
            player_id = str(interaction.author.id)
            if player_id in self.games:
                game = self.games[player_id]
                die_index = int(interaction.custom_id.split('_')[2])
                if 0 <= die_index < 5:
                    game.held_dice[die_index] = not game.held_dice[die_index]
                    await interaction.respond(content=f"Die {die_index+1} {'held' if game.held_dice[die_index] else 'released'}.", ephemeral=True)
                    # Re-send the message with updated button states
                    dice_display = format_dice_display(game.dice)
                    embed = discord.Embed(
                        title="Yahtzee Dice Roll!",
                        description=f"```\n{dice_display}\n```",
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Rolls Left", value=game.rolls_left, inline=True)
                    embed.add_field(name="Current Dice", value=str(game.dice), inline=True)

                    buttons = []
                    for i, die_value in enumerate(game.dice):
                        color = "green" if game.held_dice[i] else "blurple"
                        buttons.append(Button(label=f"Die {i+1}: {die_value}", custom_id=f"yahtzee_die_{i}", color=color))
                    buttons.append(Button(label="Re-roll selected", custom_id="yahtzee_reroll", color="green"))
                    buttons.append(Button(label="Score this roll", custom_id="yahtzee_score", color="red"))
                    await interaction.edit_original_message(embed=embed, components=buttons)

        elif interaction.custom_id == "yahtzee_reroll":
            player_id = str(interaction.author.id)
            if player_id in self.games:
                game = self.games[player_id]
                if game.rolls_left > 0:
                    game._roll_dice() # This will re-roll non-held dice and update possible scores
                    dice_display = format_dice_display(game.dice)
                    embed = discord.Embed(
                        title="Yahtzee Dice Roll!",
                        description=f"```\n{dice_display}\n```",
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Rolls Left", value=game.rolls_left, inline=True)
                    embed.add_field(name="Current Dice", value=str(game.dice), inline=True)

                    buttons = []
                    for i, die_value in enumerate(game.dice):
                        color = "green" if game.held_dice[i] else "blurple"
                        buttons.append(Button(label=f"Die {i+1}: {die_value}", custom_id=f"yahtzee_die_{i}", color=color))
                    buttons.append(Button(label="Re-roll selected", custom_id="yahtzee_reroll", color="green"))
                    buttons.append(Button(label="Score this roll", custom_id="yahtzee_score", color="red"))
                    await interaction.edit_original_message(embed=embed, components=buttons)
                    await interaction.respond(content="Dice re-rolled!", ephemeral=True)
                else:
                    await interaction.respond(content="No rolls left! Please score your dice.", ephemeral=True)

        elif interaction.custom_id == "yahtzee_score":
            player_id = str(interaction.author.id)
            if player_id in self.games:
                game = self.games[player_id]
                # Present scoring options using a SelectMenu
                options = []
                for category, score in game.current_roll_scores.items():
                    options.append(SelectOption(label=f"{SCORING_CATEGORIES[category]} ({score} points)", value=category))
                
                select_menu = SelectMenu(
                    options=options,
                    custom_id="yahtzee_score_select",
                    placeholder="Select a category to score"
                )
                await interaction.respond(content="Select a category to score:", components=[select_menu], ephemeral=True)

    @commands.Cog.listener()
    async def on_select_option(self, interaction):
        if interaction.custom_id == "yahtzee_score_select":
            player_id = str(interaction.author.id)
            if player_id in self.games:
                game = self.games[player_id]
                selected_category = interaction.values[0]
                if game.score_category(selected_category):
                    score = game.scorecard[selected_category]
                    await interaction.respond(content=f"Scored {SCORING_CATEGORIES[selected_category]} for {score} points! Total score: {game.total_score}", ephemeral=True)
                    if game.game_over:
                        await interaction.followup.send(f"Game Over! Final Score: {game.total_score}")
                        del self.games[player_id]
                    else:
                        # Start next turn
                        game._roll_dice()
                    await game.send_dice_display(interaction.channel)
                else:
                    await interaction.respond(content="Invalid category or already scored.", ephemeral=True)

    @commands.command(name='yahtzee')
    async def start_yahtzee(self, ctx):
        player_id = str(ctx.author.id)
        player_name = str(ctx.author)
        if player_id in self.games:
            await ctx.send("You already have a Yahtzee game in progress!")
            return
        self.games[player_id] = YahtzeeGameState(player_id, player_name)
        self.games[player_id]._roll_dice()
        await self.games[player_id].send_dice_display(ctx.channel)

class YahtzeeGameState:
    def __init__(self, player_id, player_name):
        self.player_id = player_id
        self.player_name = player_name
        self.dice = [1, 1, 1, 1, 1]
        self.held_dice = [False, False, False, False, False]
        self.rolls_left = 3
        self.turn = 1
        self.max_turns = 13
        self.scorecard = {}
        self.total_score = 0
        self.game_over = False
        self.current_roll_scores = {}
        
    def _roll_dice(self):
        """Roll all non-held dice (internal logic)"""
        if self.rolls_left > 0:
            for i in range(5):
                if not self.held_dice[i]:
                    self.dice[i] = random.randint(1, 6)
            self.rolls_left -= 1
            self.calculate_possible_scores()
            return True
        return False

    async def send_dice_display(self, channel):
        dice_display = format_dice_display(self.dice)
        embed = discord.Embed(
            title="Yahtzee Dice Roll!",
            description=f"```\n{dice_display}\n```",
            color=discord.Color.blue()
        )
        embed.add_field(name="Rolls Left", value=self.rolls_left, inline=True)
        embed.add_field(name="Current Dice", value=str(self.dice), inline=True)

        buttons = []
        for i, die_value in enumerate(self.dice):
            color = "green" if self.held_dice[i] else "blurple"
            buttons.append(Button(label=f"Die {i+1}: {die_value}", custom_id=f"yahtzee_die_{i}", color=color))
        buttons.append(Button(label="Re-roll selected", custom_id="yahtzee_reroll", color="green"))
        buttons.append(Button(label="Score this roll", custom_id="yahtzee_score", color="red"))

        await channel.send(embed=embed, components=buttons)
    
    def hold_dice(self, positions):
        """Hold dice at specified positions (1-5)"""
        for pos in positions:
            if 1 <= pos <= 5:
                self.held_dice[pos - 1] = True
    
    def release_dice(self, positions):
        """Release held dice at specified positions (1-5)"""
        for pos in positions:
            if 1 <= pos <= 5:
                self.held_dice[pos - 1] = False
    
    def calculate_possible_scores(self):
        """Calculate possible scores for all categories"""
        self.current_roll_scores = {}
        for category in SCORING_CATEGORIES:
            if category not in self.scorecard:
                self.current_roll_scores[category] = calculate_score(self.dice, category)
    
    def score_category(self, category):
        """Score a category and move to next turn"""
        if category in SCORING_CATEGORIES and category not in self.scorecard:
            score = calculate_score(self.dice, category)
            self.scorecard[category] = score
            self.total_score += score
            
            # Reset for next turn
            self.held_dice = [False, False, False, False, False]
            self.rolls_left = 3
            self.turn += 1
            
            if self.turn > self.max_turns:
                self.game_over = True
                # Calculate bonus for upper section
                upper_score = sum(self.scorecard.get(cat, 0) for cat in ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'])
                if upper_score >= 63:
                    self.total_score += 35
            
            return True
        return False
    def get_scorecard_display(self):

        """Generate scorecard display"""
        lines = ["```", "SCORECARD - Turn {}/{}".format(self.turn, self.max_turns), "=" * 30]
        
        # Upper section
        lines.append("UPPER SECTION:")
        upper_total = 0
        for category in ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']:
            if category in self.scorecard:
                score = self.scorecard[category]
                upper_total += score
                lines.append(f"{SCORING_CATEGORIES[category]:<15} {score:>3}")
            else:
                lines.append(f"{SCORING_CATEGORIES[category]:<15} ---")
        
        lines.append("-" * 20)
        lines.append(f"Upper Total: {upper_total}")
        if upper_total >= 63:
            lines.append("Bonus: +35")
        lines.append("")
        
        # Lower section
        lines.append("LOWER SECTION:")
        for category in ['three_of_a_kind', 'four_of_a_kind', 'full_house', 'small_straight', 'large_straight', 'yahtzee', 'chance']:
            if category in self.scorecard:
                score = self.scorecard[category]
                lines.append(f"{SCORING_CATEGORIES[category]:<15} {score:>3}")
            else:
                lines.append(f"{SCORING_CATEGORIES[category]:<15} ---")
        
        lines.append("-" * 20)
        lines.append(f"TOTAL SCORE: {self.total_score}")
        lines.append("```")
        
        return "\n".join(lines)
    
    def get_current_roll_display(self):
        """Display current dice roll with possible scores"""
        lines = ["```"]
        lines.extend(YAHTZEE_HEADER)
        lines.append("")
        lines.append(f"Player: {self.player_name}")
        lines.append(f"Turn: {self.turn}/{self.max_turns} | Rolls Left: {self.rolls_left}")
        lines.append("")
        
        # Show dice with color indicators
        dice_display = format_dice_display(self.dice)
        lines.append(dice_display)
        
        # Color indicators for dice
        color_display = []
        for i, held in enumerate(self.held_dice):
            if held:
                color_display.append("    BLUE    ")  # Held dice are blue
            else:
                color_display.append("    RED     ")  # Dice to re-roll are red
        
        lines.append("  ".join(color_display))
        
        # Show dice numbers
        dice_numbers = "  ".join([f"    {i+1}     " for i in range(5)])
        lines.append(dice_numbers)
        lines.append("")
        
        # Add instructions
        lines.append("INSTRUCTIONS:")
        lines.append("- BLUE dice will be kept for next roll")
        lines.append("- RED dice will be re-rolled")
        lines.append("- Use !yhold <positions> to keep dice")
        lines.append("- Use !yrelease <positions> to unkeep dice")
        lines.append("")
        
        # Show possible scores
        if self.current_roll_scores:
            lines.append("POSSIBLE SCORES:")
            for category, score in self.current_roll_scores.items():
                if score > 0:
                    lines.append(f"{category:<20} {score:>3} points")
        
        lines.append("```")
        return "\n".join(lines)


def setup(bot):
    bot.add_cog(YahtzeeGame(bot))

class YahtzeeGame(commands.Cog):
    def __init__(self, bot):
        global TICK_RATE
        TICK_RATE = bot.TICK_RATE
        self.bot = bot
        self.games = {}
        self.time_elapsed = 0
    
    @commands.command()
    async def yahtzee(self, ctx):
        """!yahtzee - Start a new Yahtzee game"""
        player_id = str(ctx.author.id)
        player_name = str(ctx.author.name)
        
        if player_id in self.games and not self.games[player_id].game_over:
            await ctx.send(f"{ctx.author.mention}, you already have a game in progress! Use `!yroll` to continue.", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        # Start new game
        game = YahtzeeGameState(player_id, player_name)
        self.games[player_id] = game
        
        # Initial roll
        game.roll_dice()
        
        msg = game.get_current_roll_display()
        msg += "\n**Commands:**\n"
        msg += "`!yroll` - Roll dice\n"
        msg += "`!yhold 1 2 3` - Hold dice at positions 1, 2, 3\n"
        msg += "`!yrelease 1 2` - Release held dice\n"
        msg += "`!yscore category` - Score in category (e.g., !yscore ones)\n"
        msg += "`!ycard` - Show scorecard\n"
        
        await ctx.send(msg, delete_after=self.bot.LONG_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command()
    async def yroll(self, ctx):
        """!yroll - Roll the dice"""
        player_id = str(ctx.author.id)
        
        if player_id not in self.games:
            await ctx.send(f"{ctx.author.mention}, start a game first with `!yahtzee`!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        game = self.games[player_id]
        
        if game.game_over:
            await ctx.send(f"{ctx.author.mention}, your game is over! Final score: {game.total_score}. Start a new game with `!yahtzee`.", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        if not game.roll_dice():
            await ctx.send(f"{ctx.author.mention}, no rolls left! You must score a category with `!yscore`.", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        msg = game.get_current_roll_display()
        if game.rolls_left == 0:
            msg += "\n**No more rolls! You must score a category with `!yscore category`**"
        
        await ctx.send(msg, delete_after=self.bot.LONG_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command()
    async def yhold(self, ctx, *positions):
        """!yhold 1 2 3 - Hold dice at specified positions"""
        player_id = str(ctx.author.id)
        
        if player_id not in self.games:
            await ctx.send(f"{ctx.author.mention}, start a game first with `!yahtzee`!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        game = self.games[player_id]
        
        if game.game_over:
            await ctx.send(f"{ctx.author.mention}, your game is over!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        try:
            positions = [int(pos) for pos in positions]
            game.hold_dice(positions)
            await ctx.send(f"{ctx.author.mention}, held dice at positions: {', '.join(map(str, positions))}", delete_after=self.bot.MEDIUM_DELETE_DELAY)
        except ValueError:
            await ctx.send(f"{ctx.author.mention}, please use numbers 1-5 for dice positions!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command()
    async def yrelease(self, ctx, *positions):
        """!yrelease 1 2 - Release held dice at specified positions"""
        player_id = str(ctx.author.id)
        
        if player_id not in self.games:
            await ctx.send(f"{ctx.author.mention}, start a game first with `!yahtzee`!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        game = self.games[player_id]
        
        if game.game_over:
            await ctx.send(f"{ctx.author.mention}, your game is over!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        try:
            positions = [int(pos) for pos in positions]
            game.release_dice(positions)
            await ctx.send(f"{ctx.author.mention}, released dice at positions: {', '.join(map(str, positions))}", delete_after=self.bot.MEDIUM_DELETE_DELAY)
        except ValueError:
            await ctx.send(f"{ctx.author.mention}, please use numbers 1-5 for dice positions!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command()
    async def yscore(self, ctx, category: str):
        """!yscore category - Score in a category (e.g., ones, yahtzee, full_house)"""
        player_id = str(ctx.author.id)
        
        if player_id not in self.games:
            await ctx.send(f"{ctx.author.mention}, start a game first with `!yahtzee`!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        game = self.games[player_id]
        
        if game.game_over:
            await ctx.send(f"{ctx.author.mention}, your game is over! Final score: {game.total_score}", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        category = category.lower()
        if category not in SCORING_CATEGORIES:
            await ctx.send(f"{ctx.author.mention}, invalid category! Use: {', '.join(SCORING_CATEGORIES.keys())}", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        if not game.score_category(category):
            await ctx.send(f"{ctx.author.mention}, you've already scored in that category!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        score = game.scorecard[category]
        msg = f"{ctx.author.mention}, scored {score} points in {SCORING_CATEGORIES[category]}!"
        
        if game.game_over:
            msg += f"\n🎉 **GAME COMPLETE!** 🎉\nFinal Score: **{game.total_score}** points!"
            if game.total_score >= 300:
                msg += "\n⭐ **EXCELLENT GAME!** ⭐"
            elif game.total_score >= 250:
                msg += "\n👏 **Great job!** 👏"
            
            # Award currency based on score
            if hasattr(self.bot, 'get_cog') and self.bot.get_cog('Currency'):
                currency_reward = max(10, game.total_score // 10)
                self.bot.get_cog('Currency').add_user_currency(player_id, currency_reward)
                msg += f"\n💰 Earned {currency_reward} {getattr(self.bot, 'CURRENCY_NAME', 'coins')}!"
        else:
            # Start next turn
            game.roll_dice()
            msg += f"\n**Turn {game.turn}/{game.max_turns}** - New dice rolled!"
        
        await ctx.send(msg, delete_after=self.bot.LONG_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command()
    async def ycard(self, ctx):
        """!ycard - Show your scorecard"""
        player_id = str(ctx.author.id)
        
        if player_id not in self.games:
            await ctx.send(f"{ctx.author.mention}, start a game first with `!yahtzee`!", delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        game = self.games[player_id]
        msg = game.get_scorecard_display()
        
        await ctx.send(msg, delete_after=self.bot.LONG_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command()
    async def ycategories(self, ctx):
        """!ycategories - Show all scoring categories"""
        msg = "```YAHTZEE SCORING CATEGORIES:\n"
        msg += "=" * 40 + "\n"
        msg += "UPPER SECTION (sum of matching dice):\n"
        msg += "ones, twos, threes, fours, fives, sixes\n\n"
        msg += "LOWER SECTION:\n"
        msg += "three_of_a_kind - 3+ of same (sum all dice)\n"
        msg += "four_of_a_kind  - 4+ of same (sum all dice)\n"
        msg += "full_house      - 3 of one + 2 of another (25 pts)\n"
        msg += "small_straight  - 4 consecutive dice (30 pts)\n"
        msg += "large_straight  - 5 consecutive dice (40 pts)\n"
        msg += "yahtzee         - All 5 dice same (50 pts)\n"
        msg += "chance          - Any combination (sum all dice)\n"
        msg += "```"
        
        await ctx.send(msg, delete_after=self.bot.LONG_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    async def timeout(self):
        """Periodic cleanup of old games"""
        if not self.bot.is_closed():
            self.time_elapsed += TICK_RATE
            # Clean up finished games older than 1 hour
            if self.time_elapsed % 3600 == 0:  # Every hour
                finished_games = [pid for pid, game in self.games.items() if game.game_over]
                for pid in finished_games:
                    del self.games[pid]
                if DEBUG and finished_games:
                    print(f"Cleaned up {len(finished_games)} finished Yahtzee games")

async def setup(bot):
    await bot.add_cog(YahtzeeGame(bot))
