import json
from tokenize import String
import discord
import asyncio
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

    async def load_data(self):
        try:
            with open(f'/app/data/{self.qualified_name}_data.json', 'r') as in_file:
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
            with open(f'/app/data/{self.qualified_name}_data.json', 'w+') as out_file:
                json.dump(save_data, out_file, sort_keys=True, indent=4)

    @commands.is_owner()
    @commands.command(name="buypack")
    async def buypack(self, ctx):
        """Buys a pack of cards for 500 shekels."""
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

            reveal_delays = [0.7] * 8 + [1.5] + [2.0] * (len(new_cards) - 9)
            print(f'reveal_delays {reveal_delays}')
            for i, frame in enumerate(frames[1:]):
                print(f'frame {i} sleeping: {reveal_delays[i]} if {i} < {len(reveal_delays)} else {2.0}')
                await asyncio.sleep(reveal_delays[i] if i < len(reveal_delays) else 2.0)
                # Add revealed card to the table
                print(1)
                card = new_cards[i]
                perfection_str = f"{card.get_perfection():.2%}"
                ansi_name = card.get_ansi_name()
                visible_length = len(card.get_name())
                print(2)
                padded_name = ansi_name + ' ' * (25 - visible_length)
                table += f"| {padded_name} | {perfection_str.ljust(7)} | ${str(card.value).rjust(7)} |\n"
                print(3)
                # Update the message with the new table and animation frame
                content = f"{ctx.author.mention}'s pack:\n```ansi\n{table}```\n```ansi\n{frame}```"
                print(4)
                print(content)
                await message.edit(content=content)

        else:
            await ctx.send(f"You don't have enough shekels to buy a pack. You need {self.PACK_PRICE}.")

    @commands.command(name="collection")
    async def collection(self, ctx):
        """Shows your card collection."""
        await ctx.send("Collection viewing coming soon!")

    @commands.command(name="showcard")
    async def cardinfo(self, ctx, *, card_name: str):
        """Shows info about a specific card IF it is in the user's collection."""
        await ctx.send(f"Card info for '{card_name}' coming soon!")

async def setup(bot):
    await bot.add_cog(CardCollector(bot))