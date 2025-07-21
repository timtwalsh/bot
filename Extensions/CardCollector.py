import json
import discord
import asyncio
from discord.ext import commands

from MagicTheShekelling.card_database_remake import CardDatabase, CardPack, Card
from MagicTheShekelling.pack_animation import PackAnimation

class CardCollector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_collections = {}  # {user_id: [Card, Card, ...]}
        self.card_db = CardDatabase()
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
            await ctx.send(f"{ctx.author.mention} is opening a pack...", delete_after=5)
            # Create and run the animation
            animation = PackAnimation(new_cards)
            frames = animation.generate_animation_frames()
            message = await ctx.send(f"\n```{frames[0]}```")

            revealed_cards_briefs = []

            # First 8 frames at 0.7s
            for i, frame in enumerate(frames[1:9]):
                await asyncio.sleep(0.7)
                if i < len(new_cards):
                    revealed_cards_briefs.append(new_cards[i].get_brief())
                content = "Cards:\n".join(revealed_cards_briefs) + f"\n```{frame}```"
                await message.edit(content=content)
            
            # Next frame at 1.5s
            if len(frames) > 9:
                await asyncio.sleep(1.5)
                if 8 < len(new_cards):
                    revealed_cards_briefs.append(new_cards[8].get_brief())
                content = "\n".join(revealed_cards_briefs) + f"\n```{frames[9]}```"
                await message.edit(content=content)
            
            # Remaining frames at 2s
            for i, frame in enumerate(frames[10:]):
                await asyncio.sleep(2)
                card_index = 9 + i
                if card_index < len(new_cards):
                    revealed_cards_briefs.append(new_cards[card_index].get_brief())
                content = "\n".join(revealed_cards_briefs) + f"\n```{frame}```"
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