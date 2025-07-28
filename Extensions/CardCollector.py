import json
from tokenize import String
import discord
import asyncio
import os
from discord.ext import commands

from CardData.card_datastore import CardDatabase, CardPack, RareCardPack, Card
from CardData.card_template_data import CARD_DATA_TEMPLATES
from CardData.pack_animation import PackAnimation

TIMEOUT_LOOP_FREQUENCY = 6

class CardCollector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_collections = {}  # {user_id: [Card, Card, ...]}
        self.card_db = CardDatabase(CARD_DATA_TEMPLATES)
        self.card_pack_roller = CardPack(self.card_db)
        self.rare_card_pack_roller = RareCardPack(self.card_db)
        self.TICK_RATE = self.bot.TICK_RATE
        self.PACK_PRICE = 500
        self.data_path = f'data/{self.qualified_name}_data.json'
        self.pack_dooldown =  15 # how long the cooldown is
        self.pack_dooldown_timer = 0 # a timer, don't change this
        
     
    async def is_pack_on_cooldown(self, ctx):
        if self.pack_dooldown_timer <= 0: 
            self.pack_dooldown_timer = self.pack_dooldown
            return False;
        return True


    async def load_data(self):
        try:
            with open(self.data_path, 'r') as in_file:
                data = json.load(in_file)
                user_collections_data = data.get('user_collections', {})
                self.user_collections = {
                    user_id: [Card.from_dict(card_data) for card_data in cards_list]
                    for user_id, cards_list in user_collections_data.items()
                }
                print(f"Loaded {len(self.user_collections)} user collections.")
        except Exception as e:
            print(f"CardCollector loading failed: {e}")
            self.user_collections = {}

    async def save_data(self):
        try:
            if self.user_collections:
                # Serialize card objects to dictionaries
                serializable_collections = {
                    user_id: [card.to_dict() for card in cards_list]
                    for user_id, cards_list in self.user_collections.items()
                }
                save_data = {'user_collections': serializable_collections}
                with open(self.data_path, 'w+') as out_file:
                    json.dump(save_data, out_file, sort_keys=True, indent=4)
            else:
                with open(self.data_path, 'w+') as out_file:
                    json.dump({'user_collections': {}}, out_file, sort_keys=True, indent=4)
        except Exception as e:
            print(f"CardCollector loading failed: {e}")
            self.user_collections = {}

    def get_card_bonus(self, user_id):
        """Returns the number of unique cards in a user's collection."""
        user_id = str(user_id)
        if user_id not in self.user_collections:
            return 0
        
        user_card_list = self.user_collections[user_id]
        if not user_card_list:
            return 0

        # Create a set of unique card names from the user's collection
        user_card_list.sort(key=lambda x: x.get_perfection(), reverse=True)
        unique_cards = set()
        bonus = 0
        for card in user_card_list:
            if card.name not in unique_cards:
                unique_cards.add(card.name)
                if card.is_holo:
                    bonus += 1
        
        # Return the count of unique cards
        return len(unique_cards)+bonus
    
    @commands.command(name="buypack", aliases=["rippack", "rippacks", "buypacks", "buycards"])
    async def buypack(self, ctx):
        """Buys a pack of cards for 500 shekels."""
        try:
            on_cooldown = await self.is_pack_on_cooldown(ctx)
            if not on_cooldown:
                user_id = str(ctx.author.id)
                currency_cog = self.bot.get_cog('Currency')

                if not currency_cog:
                    await ctx.send("Currency system is not available.")
                    return

                if currency_cog.remove_user_currency(user_id, self.PACK_PRICE):
                    new_cards = self.card_pack_roller.open()

                    if user_id not in self.user_collections:
                        self.user_collections[user_id] = []

                    for card in new_cards:
                        self.user_collections[user_id].append(card)
                    
                    await self.save_data()
                    animation = PackAnimation(new_cards)
                    frames = animation.generate_animation_frames()

                    message_content = f"{ctx.author.mention} is opening a pack...\n```ansi\n{frames[0]}```"
                    message = await ctx.send(message_content)

                    reveal_delays = [0.5] * 4 + [1.0] * 4 + [2.0] + [3.0] * (len(new_cards) - 9)
                    for i, frame in enumerate(frames[1:]):
                        await asyncio.sleep(reveal_delays[i] if i < len(reveal_delays) else 2.0)
                        # Update the message with the new animation frame
                        content = f"{ctx.author.mention} is opening a pack...\n```ansi\n{frame}```"
                        await message.edit(content=content)

                    header = f"| {'Card Name'.ljust(25)} | {'Quality'.ljust(7)} | {'Value'.ljust(8)} |\n"
                    separator = f"|{'-'*27}|{'-'*9}|{'-'*10}|\n"
                    table = header + separator
                    for card in new_cards:
                        perfection_str = f"{card.get_perfection():.2%}"
                        ansi_name = card.get_ansi_name()
                        visible_length = len(card.get_name())
                        padded_name = ansi_name + ' ' * (25 - visible_length)
                        table += f"| {padded_name} | {perfection_str.ljust(7)} | ${str(card.value).rjust(7)} |\n"
                    
                    await ctx.send(f"{ctx.author.mention}'s pack:\n```ansi\n{table}```")
                    await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

                else:
                    await ctx.send(f"You don't have enough shekels to buy a pack. You need {self.PACK_PRICE}.")
                    await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            else:
                await ctx.message.delete(delay=0)
        except Exception as e:
            print(f'Error in buypack: {e}')

    # DISABLED FOR NOW
    @commands.command(name="buyrarepack", aliases=["riprarepack", "riprarepacks", "buyrarepacks", "buyrarecards"])
    async def buyrarepack(self, ctx):
        """Buys a pack of 9 rare cards for 5000 shekels."""
        try:
            on_cooldown = await self.is_pack_on_cooldown(ctx)
            if not on_cooldown:
                user_id = str(ctx.author.id)
                currency_cog = self.bot.get_cog('Currency')

                if not currency_cog:
                    await ctx.send("Currency system is not available.")
                    return

                if currency_cog.remove_user_currency(user_id, self.PACK_PRICE * 10):
                    new_cards = self.rare_card_pack_roller.open()

                    if user_id not in self.user_collections:
                        self.user_collections[user_id] = []

                    for card in new_cards:
                        self.user_collections[user_id].append(card)
                    
                    await self.save_data()
                    animation = PackAnimation(new_cards, "ninepack")
                    frames = animation.generate_animation_frames()

                    message_content = f"{ctx.author.mention} is opening a rare pack...\n```ansi\n{frames[0]}```"
                    message = await ctx.send(message_content)

                    reveal_delays = [1.25] * len(new_cards)
                    for i, frame in enumerate(frames[1:]):
                        await asyncio.sleep(reveal_delays[i] if i < len(reveal_delays) else 2.0)
                        # Update the message with the new animation frame
                        content = f"{ctx.author.mention} is opening a pack...\n```ansi\n{frame}```"
                        await message.edit(content=content)

                    header = f"| {'Card Name'.ljust(25)} | {'Quality'.ljust(7)} | {'Value'.ljust(8)} |\n"
                    separator = f"|{'-'*27}|{'-'*9}|{'-'*10}|\n"
                    table = header + separator
                    for card in new_cards:
                        perfection_str = f"{card.get_perfection():.2%}"
                        ansi_name = card.get_ansi_name()
                        visible_length = len(card.get_name())
                        padded_name = ansi_name + ' ' * (25 - visible_length)
                        table += f"| {padded_name} | {perfection_str.ljust(7)} | ${str(card.value).rjust(7)} |\n"
                    
                    await ctx.send(f"{ctx.author.mention}'s pack:\n```ansi\n{table}```")
                    await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

                else:
                    await ctx.send(f"You don't have enough shekels to buy a pack. You need {self.PACK_PRICE}.")
                    await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            else:
                await ctx.message.delete(delay=0)
        except Exception as e:
            print(f'Error in buyrarepack: {e}')

    @commands.command(name="cards", aliases=["my%", "collection"])
    async def cards(self, ctx, member: discord.Member = None):
        """Shows a summary of your card collection."""
        user_id = str(member.id if member else ctx.author.id)
        user_cards = self.user_collections.get(user_id, [])

        if not user_cards:
            await ctx.send("You don't have any cards yet! Use the `buypack` command to get some.")
            return

        rarities = ["legendary", "mythic", "rare", "uncommon", "common"]
        rarity_stats = {r: {"total": 0, "holo": 0, "unique_names": set()} for r in rarities}
        total_value = 0
        card_groups = {}

        for card in user_cards:
            rarity = card.rarity
            if rarity in rarity_stats:
                rarity_stats[rarity]['total'] += 1
                if card.is_holo:
                    rarity_stats[rarity]['holo'] += 1
                rarity_stats[rarity]['unique_names'].add(card.name)
            
            total_value += card.get_value()

            if card.name not in card_groups:
                card_groups[card.name] = []
            card_groups[card.name].append(card)

        duplicate_value = 0
        for name, cards in card_groups.items():
            if len(cards) > 1:
                cards.sort(key=lambda c: c.get_value(), reverse=True)
                for i in range(1, len(cards)):
                    duplicate_value += cards[i].get_value()

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Card Collection Summary",
            color=0x9932CC
        )

        rarity_icons = {
            'common': '⚪',
            'uncommon': '🟢',
            'rare': '🔵',
            'mythic': '🟣',
            'legendary': '🔴'
        }

        description = []
        for rarity in rarities:
            stats = rarity_stats[rarity]
            if stats['total'] > 0:
                unique_count = len(stats['unique_names'])
                max_possible = len(self.card_db.card_data.get(rarity, {}))
                line = f"{rarity_icons[rarity]} **{rarity.capitalize()}**: {stats['total']} Total, {stats['holo']} Holo, ({unique_count}/{max_possible} Unique)"
                description.append(line)
        
        embed.description = "\n".join(description)

        embed.add_field(name="Total Collection Value", value=f"$ {total_value:,}", inline=True)
        embed.add_field(name="Duplicate Card Value", value=f"$ {duplicate_value:,}", inline=True)

        total_unique_cards = len(card_groups)
        total_cards = len(user_cards)
        
        # Calculate total holo count and max possible holo count
        total_holo_count = sum(stats['holo'] for stats in rarity_stats.values())
        max_possible_holo_count = sum(len(self.card_db.card_data.get(rarity, {})) for rarity in rarities)
        
        embed.set_footer(text=f"Total Cards: {total_cards} ({total_unique_cards} unique, {total_holo_count}/{max_possible_holo_count} holo)")

        await ctx.send(embed=embed)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)

    @commands.command(name="card", aliases=["showcard", "viewcard"])
    async def card(self, ctx, card_name: str):
        """Shows a user any of their own cards. Prefers High Quality."""
        user_id = str(ctx.author.id)
        if user_id not in self.user_collections:
            await ctx.send(f"You don't have any cards in your collection.", delete_after=self.bot.SHORT_DELETE_DELAY)
            return
        user_cards = self.user_collections[user_id]
        if not user_cards:
            await ctx.send(f"You don't have any cards in your collection.", delete_after=self.bot.SHORT_DELETE_DELAY)
            return
        user_cards = self.user_collections[user_id]
        user_cards.sort(key=lambda c: c.get_perfection(), reverse=True)
        selected_card = None
        for user_card in user_cards:
            if user_card.name.lower() == card_name.lower():
                selected_card = user_card
                break
        if not selected_card:
            await ctx.send(f"Card '{card_name}' not found in your collection.", delete_after=self.bot.SHORT_DELETE_DELAY)
            return
        msg = f"{ctx.author.mention}'s best {selected_card.name}\n```ansi\n"
        for line in selected_card.display():
            msg += line + "\n"
        msg += "```"
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)


    @commands.command(name="sellduplicates", aliases=["selldupes", "selld"])
    async def sellduplicates(self, ctx):
        """Sells all duplicate cards, keeping the one with the highest perfection."""
        user_id = str(ctx.author.id)
        if user_id not in self.user_collections:
            await ctx.send(f"You don't have any cards in your collection.")
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        user_card_list = self.user_collections[user_id]
        if not user_card_list:
            await ctx.send(f"You don't have any cards in your collection.")
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        # Group cards by name
        card_groups = {}
        for card in user_card_list:
            if card.name not in card_groups:
                card_groups[card.name] = []
            card_groups[card.name].append(card)
        
        # Keep the best card of each name, sell the rest
        keep_list = []
        sell_list = []
        
        for name, cards in card_groups.items():
            if len(cards) > 1:
                # Sort by perfection, keep the best one
                cards.sort(key=lambda c: c.get_perfection(), reverse=True)
                keep_list.append(cards[0])  # Keep the best
                sell_list.extend(cards[1:])  # Sell the rest
            else:
                keep_list.append(cards[0])  # Only one card, keep it
        
        if not sell_list:
            await ctx.send("You don't have any duplicate cards to sell!", delete_after=self.bot.SHORT_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
    
        total_value = 0.0
        for card in sell_list:
            try: 
                total_value += int(card.get_value())
            except Exception as e:
                print(f'error with {card.get_name()} {e}')
    
        try: 
            currency_cog = self.bot.get_cog("Currency")
            if not currency_cog:
                await ctx.send(f"Currency cog not found. Contact bot owner")
                await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
                return
            currency_cog.add_user_currency(user_id, total_value, False)
            self.user_collections[user_id] = keep_list
            msg = f"{ctx.author.mention} Successfully sold {len(sell_list)} cards for ${total_value:,}"
            await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        except Exception as e:
            print(f'error with sell {e}')

    @commands.command(name="mycardlist", aliases=["mycards", "mycardcollection", "mycollection"])
    async def mycardlist(self, ctx):
        """Shows a user their card collection."""
        try: 
            user_id = str(ctx.author.id)
            if user_id not in self.user_collections:
                await ctx.send(f"You don't have any cards in your collection.", delete_after=self.bot.SHORT_DELETE_DELAY)
                return
            user_cards = self.user_collections[user_id]
            if not user_cards:
                await ctx.send(f"You don't have any cards in your collection.", delete_after=self.bot.SHORT_DELETE_DELAY)
                return
            user_cards = self.user_collections[user_id]
            # send the requesting user multiple dms, each showing 30 card names grouped by rarity (common, uncommon, rare, mythic, legendary) and then sorted by quality (high to low)
            rarity_groups = {
                'common': [],
                'uncommon': [],
                'rare': [],
                'mythic': [],
                'legendary': []
            }

            for card in user_cards:
                rarity = card.rarity.lower()
                rarity_groups[rarity].append(card)
            rarity_groups['common'].sort(key=lambda c: c.get_perfection(), reverse=True)
            rarity_groups['uncommon'].sort(key=lambda c: c.get_perfection(), reverse=True)
            rarity_groups['rare'].sort(key=lambda c: c.get_perfection(), reverse=True)
            rarity_groups['mythic'].sort(key=lambda c: c.get_perfection(), reverse=True)
            rarity_groups['legendary'].sort(key=lambda c: c.get_perfection(), reverse=True)

            all_cards = []
            for rarity in ['legendary', 'mythic', 'rare', 'uncommon', 'common']:
                for card in rarity_groups[rarity]:
                    all_cards.append((rarity, card))
            all_cards.sort(key=lambda c: c[1].number, reverse=True)
            chunk_size = 30
            chunks = [all_cards[i:i + chunk_size] for i in range(0, len(all_cards), chunk_size)]
            
            for i, chunk in enumerate(chunks):
                msg = f"**Card Collection (Part {i + 1}/{len(chunks)})**\n\n"
                current_rarity = None
                
                for rarity, card in chunk:
                    if current_rarity != rarity:
                        if current_rarity is not None:
                            msg += "\n"
                        msg += f"{rarity.capitalize()} Cards\n"
                        current_rarity = rarity
                    msg += f"#{card.number}. {card.name} ({card.get_perfection():.1f}%)\n"
                
                await ctx.author.send(msg)
                await asyncio.sleep(1)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
        except Exception as e:
            print(f'error with mycardlist {e}')

    @tasks.loop(seconds=TIMEOUT_LOOP_FREQUENCY)
    async def cooldown_loop(self):
        """Main game loop TASK_LOOP_RATE seconds"""
        try:
            if self.pack_dooldown_timer >= 0:
                self.pack_dooldown_timer -= TIMEOUT_LOOP_FREQUENCY

        except Exception as e:
            print(f"Error in cooldown loop: {e}")

    @cooldown_loop.before_loop
    async def before_game_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(CardCollector(bot))