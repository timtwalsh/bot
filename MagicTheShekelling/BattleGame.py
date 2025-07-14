import asyncio
import random
from collections import defaultdict
import discord
from discord.ext import commands

class BattleGame:
    def __init__(self, bot, initiator_id, bet_amount):
        self.bot = bot
        self.initiator_id = initiator_id
        self.opponent_id = None
        self.bet_amount = bet_amount
        self.current_round = 0
        self.max_rounds = 5
        self.initiator_wins = 0
        self.opponent_wins = 0
        self.draws = 0
        self.game_active = False
        self.awaiting_opponent = True
        self.initiator_deck = []
        self.opponent_deck = []
        self.current_turn = None  # Will be set to initiator_id or opponent_id
        
    def join_game(self, opponent_id):
        """Join the battle game as opponent"""
        if self.awaiting_opponent:
            self.opponent_id = opponent_id
            self.awaiting_opponent = False
            self.game_active = True
            self.current_turn = self.initiator_id  # Initiator goes first
            return True
        return False
    
    def prepare_decks(self, magic_game):
        """Prepare shuffled decks for both players"""
        # Get initiator's collection
        initiator_collection = magic_game.user_collections[str(self.initiator_id)]
        self.initiator_deck = []
        
        for card_id, count in initiator_collection.items():
            for _ in range(count):
                self.initiator_deck.append(card_id)
        
        # Get opponent's collection
        opponent_collection = magic_game.user_collections[str(self.opponent_id)]
        self.opponent_deck = []
        
        for card_id, count in opponent_collection.items():
            for _ in range(count):
                self.opponent_deck.append(card_id)
        
        # Shuffle both decks
        random.shuffle(self.initiator_deck)
        random.shuffle(self.opponent_deck)
    
    def draw_card(self, player_id):
        """Draw the next card for a player"""
        if player_id == self.initiator_id:
            if self.initiator_deck:
                return self.initiator_deck.pop(0)
        elif player_id == self.opponent_id:
            if self.opponent_deck:
                return self.opponent_deck.pop(0)
        return None
    
    def get_card_stats(self, card_id, magic_game):
        """Get card stats from either regular or special cards"""
        if isinstance(card_id, str):  # Special card
            card = magic_game.special_cards[card_id]
            power = card['power']
            toughness = card['toughness']
            name = card['name']
        else:
            card = magic_game.cards_database[card_id]
            power = card['power']
            toughness = card['toughness']
            name = card['name']
        
        # Handle infinite stats
        if power == '∞':
            power = float('inf')
        if toughness == '∞':
            toughness = float('inf')
            
        return power, toughness, name
    
    def resolve_battle(self, card1_id, card2_id, magic_game):
        """Resolve battle between two cards"""
        power1, toughness1, name1 = self.get_card_stats(card1_id, magic_game)
        power2, toughness2, name2 = self.get_card_stats(card2_id, magic_game)
        
        # Handle infinite vs infinite
        if power1 == float('inf') and power2 == float('inf'):
            return "draw", f"Both cards have infinite power! It's a draw!"
        
        # Infinite always wins unless vs infinite
        if power1 == float('inf') and power2 != float('inf'):
            return "player1", f"{name1} (∞ power) destroys {name2}!"
        if power2 == float('inf') and power1 != float('inf'):
            return "player2", f"{name2} (∞ power) destroys {name1}!"
        
        # Check if cards kill each other
        card1_kills_card2 = power1 >= toughness2
        card2_kills_card1 = power2 >= toughness1
        
        if card1_kills_card2 and card2_kills_card1:
            return "draw", f"Both {name1} ({power1}/{toughness1}) and {name2} ({power2}/{toughness2}) destroy each other!"
        elif card1_kills_card2:
            return "player1", f"{name1} ({power1}/{toughness1}) destroys {name2} ({power2}/{toughness2})!"
        elif card2_kills_card1:
            return "player2", f"{name2} ({power2}/{toughness2}) destroys {name1} ({power1}/{toughness1})!"
        else:
            return "draw", f"Neither {name1} ({power1}/{toughness1}) nor {name2} ({power2}/{toughness2}) can destroy the other!"
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.current_round >= self.max_rounds
    
    def get_winner(self):
        """Get the winner of the game"""
        if self.initiator_wins > self.opponent_wins:
            return self.initiator_id
        elif self.opponent_wins > self.initiator_wins:
            return self.opponent_id
        else:
            return None  # Tie game


class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_battles = {}  # channel_id: BattleGame
        
    @commands.command(aliases=["fight", "duel"])
    async def battle(self, ctx, bet_amount: int = None):
        """!battle [amount] - Start or join a battle game"""
        if bet_amount is None:
            await ctx.send("Please specify a bet amount! Example: !battle 300", delete_after=10)
            return
        
        if bet_amount <= 0:
            await ctx.send("Bet amount must be positive!", delete_after=10)
            return
        
        user_id = ctx.author.id
        channel_id = ctx.channel.id
        
        # Check if user has enough shekels
        currency_cog = self.bot.get_cog('Currency')
        user_balance = currency_cog.get_user_currency(str(user_id))
        
        if float(user_balance) < bet_amount:
            await ctx.send(f"You need §{bet_amount} to battle. You have §{user_balance:.2f}", 
                         delete_after=10)
            return
        
        # Check if user has any cards
        magic_cog = self.bot.get_cog('MagicTheShekelling')
        if not magic_cog:
            await ctx.send("Magic the Shekelling game not available!", delete_after=10)
            return
        
        user_collection = magic_cog.game.user_collections[str(user_id)]
        if not user_collection or sum(user_collection.values()) == 0:
            await ctx.send("You need cards to battle! Buy some booster packs first.", delete_after=10)
            return
        
        # Check if there's already a battle in this channel
        if channel_id in self.active_battles:
            battle = self.active_battles[channel_id]
            
            if battle.awaiting_opponent and user_id != battle.initiator_id:
                # Join existing battle
                if float(user_balance) < battle.bet_amount:
                    await ctx.send(f"You need §{battle.bet_amount} to join this battle. You have §{user_balance:.2f}", 
                                 delete_after=10)
                    return
                
                # Check if opponent has cards
                opponent_collection = magic_cog.game.user_collections[str(user_id)]
                if not opponent_collection or sum(opponent_collection.values()) == 0:
                    await ctx.send("You need cards to battle! Buy some booster packs first.", delete_after=10)
                    return
                
                # Remove bet amounts from both players
                currency_cog.remove_user_currency(str(battle.initiator_id), battle.bet_amount)
                currency_cog.remove_user_currency(str(user_id), battle.bet_amount)
                
                # Join the battle
                battle.join_game(user_id)
                battle.prepare_decks(magic_cog.game)
                
                initiator = self.bot.get_user(battle.initiator_id)
                opponent = self.bot.get_user(user_id)
                
                embed = discord.Embed(
                    title="⚔️ Battle Started!",
                    description=f"**{initiator.display_name}** vs **{opponent.display_name}**\n"
                               f"Bet: §{battle.bet_amount} each (§{battle.bet_amount * 2} total pot)",
                    color=0xFF4500
                )
                embed.add_field(name="📋 Rules", 
                               value="• 5 rounds of card battles\n"
                                    "• Cards battle: Power vs Toughness\n"
                                    "• ∞ stats always win (except vs other ∞)\n"
                                    "• Most wins takes the pot!", inline=False)
                embed.add_field(name="🎯 Current Turn", 
                               value=f"{initiator.display_name} - Use `!draw_card` to draw your card!", inline=False)
                
                await ctx.send(embed=embed)
                
            else:
                await ctx.send("There's already a battle in progress in this channel!", delete_after=10)
                return
        else:
            # Start new battle
            if bet_amount != bet_amount:  # This catches the case where they joined with different bet
                await ctx.send(f"Battle bet amount is §{bet_amount}. Use `!battle {bet_amount}` to join.", 
                             delete_after=10)
                return
            
            # Create new battle
            battle = BattleGame(self.bot, user_id, bet_amount)
            self.active_battles[channel_id] = battle
            
            embed = discord.Embed(
                title="⚔️ Battle Challenge!",
                description=f"**{ctx.author.display_name}** challenges anyone to a card battle!\n"
                           f"Bet: §{bet_amount}",
                color=0xFFD700
            )
            embed.add_field(name="💰 Prize Pool", value=f"§{bet_amount * 2}", inline=True)
            embed.add_field(name="🎮 Join Battle", value=f"`!battle {bet_amount}`", inline=True)
            embed.set_footer(text="Waiting for opponent...")
            
            await ctx.send(embed=embed)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["draw", "play_card"])
    async def draw_card(self, ctx):
        """!draw_card - Draw your card for the current battle round"""
        channel_id = ctx.channel.id
        user_id = ctx.author.id
        
        if channel_id not in self.active_battles:
            await ctx.send("No active battle in this channel!", delete_after=10)
            return
        
        battle = self.active_battles[channel_id]
        
        if not battle.game_active:
            await ctx.send("Battle hasn't started yet!", delete_after=10)
            return
        
        if user_id not in [battle.initiator_id, battle.opponent_id]:
            await ctx.send("You're not part of this battle!", delete_after=10)
            return
        
        if battle.current_turn != user_id:
            other_player = battle.initiator_id if user_id == battle.opponent_id else battle.opponent_id
            other_user = self.bot.get_user(other_player)
            await ctx.send(f"It's {other_user.display_name}'s turn to draw!", delete_after=10)
            return
        
        if battle.is_game_over():
            await ctx.send("Battle is already over!", delete_after=10)
            return
        
        # Draw card
        magic_cog = self.bot.get_cog('MagicTheShekelling')
        card_id = battle.draw_card(user_id)
        
        if card_id is None:
            await ctx.send("You're out of cards! You lose this round.", delete_after=10)
            # Handle out of cards scenario
            if user_id == battle.initiator_id:
                battle.opponent_wins += 1
            else:
                battle.initiator_wins += 1
            battle.current_round += 1
        else:
            # Show the card drawn
            power, toughness, name = battle.get_card_stats(card_id, magic_cog.game)
            power_display = "∞" if power == float('inf') else str(power)
            toughness_display = "∞" if toughness == float('inf') else str(toughness)
            
            embed = discord.Embed(
                title="🎴 Card Drawn!",
                description=f"**{ctx.author.display_name}** draws: **{name}**\n"
                           f"Power: {power_display} | Toughness: {toughness_display}",
                color=0x00FF00
            )
            
            # Switch turns or resolve if both have drawn
            if battle.current_turn == battle.initiator_id:
                battle.current_turn = battle.opponent_id
                opponent = self.bot.get_user(battle.opponent_id)
                embed.add_field(name="⏭️ Next Turn", 
                               value=f"{opponent.display_name}, use `!draw_card` to draw your card!", 
                               inline=False)
                # Store the initiator's card
                battle.initiator_card = card_id
            else:
                # Both cards drawn, resolve battle
                battle.opponent_card = card_id
                result, description = battle.resolve_battle(battle.initiator_card, battle.opponent_card, magic_cog.game)
                
                # Update scores
                if result == "player1":
                    battle.initiator_wins += 1
                elif result == "player2":
                    battle.opponent_wins += 1
                else:
                    battle.draws += 1
                
                battle.current_round += 1
                
                # Show battle result
                embed.add_field(name="⚔️ Battle Result", value=description, inline=False)
                
                initiator = self.bot.get_user(battle.initiator_id)
                opponent = self.bot.get_user(battle.opponent_id)
                
                embed.add_field(name="📊 Score", 
                               value=f"{initiator.display_name}: {battle.initiator_wins}\n"
                                    f"{opponent.display_name}: {battle.opponent_wins}\n"
                                    f"Draws: {battle.draws}", inline=True)
                embed.add_field(name="🎯 Round", 
                               value=f"{battle.current_round}/{battle.max_rounds}", inline=True)
                
                # Check if game is over
                if battle.is_game_over():
                    winner_id = battle.get_winner()
                    
                    if winner_id:
                        winner = self.bot.get_user(winner_id)
                        # Award the pot to winner
                        currency_cog = self.bot.get_cog('Currency')
                        pot = battle.bet_amount * 2
                        currency_cog.add_user_currency(str(winner_id), pot)
                        
                        embed.add_field(name="🏆 Winner!", 
                                       value=f"**{winner.display_name}** wins §{pot}!", 
                                       inline=False)
                        embed.color = 0xFFD700
                    else:
                        # Tie game - return bets
                        currency_cog = self.bot.get_cog('Currency')
                        currency_cog.add_user_currency(str(battle.initiator_id), battle.bet_amount)
                        currency_cog.add_user_currency(str(battle.opponent_id), battle.bet_amount)
                        
                        embed.add_field(name="🤝 Tie Game!", 
                                       value="Bets returned to both players!", 
                                       inline=False)
                        embed.color = 0x808080
                    
                    # Clean up battle
                    del self.active_battles[channel_id]
                else:
                    # Next round
                    battle.current_turn = battle.initiator_id
                    embed.add_field(name="⏭️ Next Round", 
                                   value=f"{initiator.display_name}, use `!draw_card` to start round {battle.current_round + 1}!", 
                                   inline=False)
            
            await ctx.send(embed=embed)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["battle_status", "battle_info"])
    async def battle_score(self, ctx):
        """!battle_score - Show current battle status"""
        channel_id = ctx.channel.id
        
        if channel_id not in self.active_battles:
            await ctx.send("No active battle in this channel!", delete_after=10)
            return
        
        battle = self.active_battles[channel_id]
        
        if battle.awaiting_opponent:
            initiator = self.bot.get_user(battle.initiator_id)
            embed = discord.Embed(
                title="⚔️ Battle Waiting",
                description=f"**{initiator.display_name}** is waiting for an opponent!\n"
                           f"Bet: §{battle.bet_amount}",
                color=0xFFD700
            )
            embed.add_field(name="🎮 Join Battle", value=f"`!battle {battle.bet_amount}`", inline=True)
        else:
            initiator = self.bot.get_user(battle.initiator_id)
            opponent = self.bot.get_user(battle.opponent_id)
            current_player = self.bot.get_user(battle.current_turn)
            
            embed = discord.Embed(
                title="⚔️ Battle in Progress",
                description=f"**{initiator.display_name}** vs **{opponent.display_name}**",
                color=0xFF4500
            )
            embed.add_field(name="💰 Pot", value=f"§{battle.bet_amount * 2}", inline=True)
            embed.add_field(name="🎯 Round", value=f"{battle.current_round + 1}/{battle.max_rounds}", inline=True)
            embed.add_field(name="📊 Score", 
                           value=f"{initiator.display_name}: {battle.initiator_wins}\n"
                                f"{opponent.display_name}: {battle.opponent_wins}\n"
                                f"Draws: {battle.draws}", inline=False)
            embed.add_field(name="⏭️ Current Turn", 
                           value=f"{current_player.display_name} - Use `!draw_card`", inline=False)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["forfeit", "surrender"])
    async def cancel_battle(self, ctx):
        """!cancel_battle - Cancel the current battle (forfeit)"""
        channel_id = ctx.channel.id
        user_id = ctx.author.id
        
        if channel_id not in self.active_battles:
            await ctx.send("No active battle in this channel!", delete_after=10)
            return
        
        battle = self.active_battles[channel_id]
        
        if user_id not in [battle.initiator_id, battle.opponent_id]:
            await ctx.send("You're not part of this battle!", delete_after=10)
            return
        
        currency_cog = self.bot.get_cog('Currency')
        
        if battle.awaiting_opponent:
            # Battle hasn't started, just cancel it
            embed = discord.Embed(
                title="⚔️ Battle Cancelled",
                description=f"Battle cancelled by {ctx.author.display_name}",
                color=0x808080
            )
        else:
            # Battle in progress, other player wins
            winner_id = battle.opponent_id if user_id == battle.initiator_id else battle.initiator_id
            winner = self.bot.get_user(winner_id)
            
            # Award pot to winner
            pot = battle.bet_amount * 2
            currency_cog.add_user_currency(str(winner_id), pot)
            
            embed = discord.Embed(
                title="⚔️ Battle Forfeited",
                description=f"**{ctx.author.display_name}** forfeits the battle!\n"
                           f"**{winner.display_name}** wins §{pot}!",
                color=0xFF0000
            )
        
        # Clean up battle
        del self.active_battles[channel_id]
        
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)


async def setup(bot):
    await bot.add_cog(Battle(bot))