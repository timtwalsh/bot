import json
from tokenize import String
import discord
import asyncio
import os
from discord.ext import commands

from CardData.card_datastore import CardDatabase, CardPack, Card
from CardData.card_template_data import CARD_DATA_TEMPLATES
from CardData.pack_animation import PackAnimation

class CardCollector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_collections = {}  # {user_id: [Card, Card, ...]}
        self.card_db = CardDatabase(CARD_DATA_TEMPLATES)
        self.card_pack_roller = CardPack(self.card_db)
        self.PACK_PRICE = 500
        self.data_path = f'data/{self.qualified_name}_data.json'

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
        except FileNotFoundError:
            print("CardCollector_data.json not found. Starting with empty collections.")
            self.user_collections = {}

    async def save_data(self):
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

    def get_unique_card_count(self, user_id):
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
            if card.get_perfection() >= 95:
                bonus += 1
            unique_cards.add(card.name)
        
        # Return the count of unique cards
        return len(unique_cards)+bonus

    # can only be run by 1 person  at a time
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.is_owner()
    @commands.command(name="buypack", aliases=["rippack", "buypacks"])
    async def buypack(self, ctx):
        """Buys a pack of cards for 500 shekels."""
        try:
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
                content = f"{ctx.author.mention} is opening a pack..."
                animation = PackAnimation(new_cards)
                frames = animation.generate_animation_frames()

                message_content = f"{ctx.author.mention} is opening a pack...\n```ansi\n{frames[0]}```"
                message = await ctx.send(message_content)
                header = f"| {'Card Name'.ljust(25)} | {'Quality'.ljust(7)} | {'Value'.ljust(8)} |\n"
                separator = f"|{'-'*27}|{'-'*9}|{'-'*10}|\n"
                table = header + separator

                reveal_delays = [0.5] * 4 + [1.0] * 4 + [2.0] + [3.0] * (len(new_cards) - 9)
                print(f'reveal_delays {reveal_delays}')
                for i, frame in enumerate(frames[1:]):
                    print(f'frame {i} sleeping: {reveal_delays[i]} if {i} < {len(reveal_delays)} else {2.0}')
                    await asyncio.sleep(reveal_delays[i] if i < len(reveal_delays) else 2.0)
                    card = new_cards[i]
                    perfection_str = f"{card.get_perfection():.2%}"
                    ansi_name = card.get_ansi_name()
                    visible_length = len(card.get_name())
                    padded_name = ansi_name + ' ' * (25 - visible_length)
                    table += f"| {padded_name} | {perfection_str.ljust(7)} | ${str(card.value).rjust(7)} |\n"
                    # Update the message with the new table and animation frame
                    content = f"{ctx.author.mention}'s pack:\n```ansi\n{table}```\n```ansi\n{frame}```"
                    await message.edit(content=content)

            else:
                await ctx.send(f"You don't have enough shekels to buy a pack. You need {self.PACK_PRICE}.")
        except Exception as e:
            print(f'Error in buypack: {e}')
            import traceback
            traceback.print_exc()

    @commands.command(name="cards", aliases=["mycards, collection"])
    async def cards(self, ctx):
        """Shows a summary of your card collection."""
        user_id = str(ctx.author.id)
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
                line = f"{rarity_icons[rarity]} **{rarity.capitalize()}**: {stats['total']} Total, {stats['holo']} Holo, {unique_count} Unique"
                description.append(line)
        
        embed.description = "\n".join(description)

        embed.add_field(name="Total Collection Value", value=f"$ {total_value:,}", inline=True)
        embed.add_field(name="Duplicate Card Value", value=f"$ {duplicate_value:,}", inline=True)

        total_unique_cards = len(card_groups)
        total_cards = len(user_cards)
        embed.set_footer(text=f"Total Cards: {total_cards} ({total_unique_cards} unique)")

        await ctx.send(embed=embed)

    @commands.command(name="card", aliases=["showcard", "viewcard"])
    async def card(self, ctx, card_name: str):
        """Shows a user any of their own cards. Prefers High Quality."""
        user_id = str(ctx.author.id)
        if user_id not in self.user_collections:
            await ctx.send(f"You don't have any cards in your collection.")
            return
        user_cards = self.user_collections[user_id]
        if not user_cards:
            await ctx.send(f"You don't have any cards in your collection.")
            return
        user_cards = self.user_collections[user_id]
        user_cards.sort(key=lambda c: c.get_perfection(), reverse=True)
        selected_card = None
        for user_card in user_cards:
            if user_card.name.lower() == card_name.lower():
                selected_card = user_card
                break
        if not selected_card:
            await ctx.send(f"Card '{card_name}' not found in your collection.")
            return
        msg = f"{ctx.author.mention}'s best {selected_card.name}\n```ansi\n"
        for line in selected_card.display():
            msg += line + "\n"
        msg += "```"
        await ctx.send(msg, delete_after=self.bot.MEDIUM_DELETE_DELAY)


    @commands.command(name="sellduplicates", aliases=["selldupes", "selld"])
    async def sellduplicates(self, ctx):
        """Sells all duplicate cards, keeping the one with the highest perfection."""
        user_id = str(ctx.author.id)
        if user_id not in self.user_collections:
            await ctx.send(f"You don't have any cards in your collection.")
            return
        user_card_list = self.user_collections[user_id]
        if not user_card_list:
            await ctx.send(f"You don't have any cards in your collection.")
            return
        sell_list = user_card_list.copy()
        sell_list.sort(key=lambda c: c.get_perfection(), reverse=True)
        keep_list = []
        for card in user_card_list:
            if card.name not in keep_list:
                keep_list.append(card)
                sell_list.remove(card)

        total_value = 0.0
        # total_value = sum(float(card.value) for card in sell_list) # something wierd going on here
        for card in sell_list:
            try: 
                total_value += int(card.get_value())
            except Exception as e:
                print(f'error with {card.get_name()} {e}')

        try: 
            currency_cog = self.bot.get_cog("Currency")
            if not currency_cog:
                await ctx.send(f"Currency cog not found. Contact bot owner")
                return
            currency_cog.add_user_currency(user_id, total_value)
            self.user_collections[user_id] = keep_list
            msg = f"{ctx.author.mention} Successfully sold {len(sell_list)} cards for ${total_value:,}"
            await ctx.send(msg, delete_after=self.bot.SHORT_DELETE_DELAY)
        except Exception as e:
            print(f'error with sell {e}')
    


async def setup(bot):
    await bot.add_cog(CardCollector(bot))