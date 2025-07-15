import asyncio
import json
import random
from collections import defaultdict
import discord
from discord.ext import commands
from MagicTheShekelling.card_database import CardDatabase

class MagicTheShekellingGame:
    def __init__(self, bot):
        self.bot = bot
        self.user_collections = defaultdict(lambda: defaultdict(int))
        self.user_inventory = defaultdict(lambda: defaultdict(int))  # For crafting materials
        self.user_items = defaultdict(lambda: defaultdict(int))  # For crafted items
        self.card_db = CardDatabase()
        self.cards_database = self.card_db.generate_cards_database()
        self.special_cards = self.card_db.special_cards
        
    def get_user_rarity_boost(self, user_id):
        """Calculate total rarity boost from user's items"""
        boost = 0.0
        items = self.user_items.get(user_id, {})
        
        # Card Nerd: 10% boost
        boost += items.get('card_nerd', 0) * 0.10
        
        # Card Store: 20% boost
        boost += items.get('card_store', 0) * 0.20
        
        # Card Printer: 40% boost
        boost += items.get('card_printer', 0) * 0.40
        
        return boost
        
    def get_pack_contents(self, user_id=None):
        """Generate contents of a single pack with rarity boost applied"""
        pack = []
        
        # Get user's rarity boost
        rarity_boost = 0.0
        if user_id:
            rarity_boost = self.get_user_rarity_boost(user_id)
        
        # 7 Common cards
        common_ids = [i for i in range(1, 65)]
        for _ in range(7):
            pack.append(random.choice(common_ids))
        
        # 2 Uncommon cards
        uncommon_ids = [i for i in range(65, 97)]
        for _ in range(2):
            pack.append(random.choice(uncommon_ids))
        
        # 1 Rare or Ultra Rare slot with boost applied
        base_roll = random.randint(1, 100000)
        
        # Apply rarity boost by effectively lowering the roll
        # This increases the chance of getting rarer cards
        boosted_roll = int(base_roll * (1 - rarity_boost))
        boosted_roll = max(1, boosted_roll)  # Ensure it's at least 1
        
        if boosted_roll == 1:  # 1/100000 for 20k ultra rare
            pack.append('ULTRA_LEGENDARY')
        elif boosted_roll == 2:  # 1/100000 for Tom's Mirror
            pack.append('TOMS_MIRROR')
        elif boosted_roll <= 600:  # 599/100000 (about 1/167) for 5k ultra rare
            pack.append('ULTRA_RARE_5K')
        elif boosted_roll <= 1500:  # 900/100000 (about 1/111) for 1k ultra rare
            pack.append('ULTRA_RARE_1K')
        elif boosted_roll <= 2800:  # 1300/100000 (about 1/77) for 500 shekel rare
            pack.append('RARE_500')
        elif boosted_roll <= 4800:  # 2000/100000 (1/50) for 300 shekel rare
            pack.append('RARE_300')
        elif boosted_roll <= 9500:  # 4500/100000 (about 1/22) for 200 shekel rare
            pack.append('RARE_200')
        else:
            # Regular rare or mythic from remaining 90.5%
            remaining_chance = random.randint(1, 30)
            
            # Apply boost to mythic chance as well
            mythic_threshold = int(30 * (1 - rarity_boost * 0.5))
            mythic_threshold = max(15, mythic_threshold)  # At least 50% better chance
            
            if remaining_chance >= mythic_threshold:  # Boosted chance for mythic
                mythic_ids = [i for i in range(127, 152)]
                pack.append(random.choice(mythic_ids))
            else:  # Regular rare
                rare_ids = [i for i in range(97, 127)]
                pack.append(random.choice(rare_ids))
        
        return pack
    
    def create_card_display(self, card_id, index):
        """Create display for a single card"""
        lines = []
        
        if isinstance(card_id, str):  # Special card
            card = self.special_cards[card_id]
            if card_id == 'ULTRA_LEGENDARY':
                lines.append(f"{index}. 🌟 ULTRA LEGENDARY CARD! 🌟")
                lines.append(f"💎 {card['name']} 💎")
            elif card_id == 'TOMS_MIRROR':
                lines.append(f"{index}. 🪞 TOM'S MIRROR - ULTRA MYTHIC! 🪞")
                lines.append(f"✨ {card['description']} ✨")
            elif card_id == 'ULTRA_RARE_5K':
                lines.append(f"{index}. ✨ ULTRA RARE CARD! ✨")
                lines.append(f"💰 {card['name']} 💰")
            elif card_id == 'ULTRA_RARE_1K':
                lines.append(f"{index}. ⭐ ULTRA RARE CARD! ⭐")
                lines.append(f"💎 {card['name']} 💎")
            elif card_id == 'RARE_500':
                lines.append(f"{index}. 💰 PREMIUM RARE CARD! 💰")
                lines.append(f"🏆 {card['name']} 🏆")
            elif card_id == 'RARE_300':
                lines.append(f"{index}. 🎯 HIGH VALUE RARE! 🎯")
                lines.append(f"💎 {card['name']} 💎")
            else:  # RARE_200
                lines.append(f"{index}. 🔥 VALUABLE RARE! 🔥")
                lines.append(f"⚡ {card['name']} ⚡")
            
            lines.append(f"Power: {card['power']} | Toughness: {card['toughness']}")
            lines.append(f"Sell Value: §{card['sell_min']}-{card['sell_max']}")
        else:
            card = self.cards_database[card_id]
            rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
            lines.append(f"{index}. {rarity_symbol[card['rarity']]} {card['name']}")
            lines.append(f"   {card['power']}/{card['toughness']} | {card['description']}")
            lines.append(f"   Sell Value: §{card['sell_min']}-{card['sell_max']}")
        
        lines.append("```")
        lines.append(card['ascii_art'] if isinstance(card_id, str) else card['ascii_art'])
        lines.append("```")
        lines.append("─" * 50)
        
        return '\n'.join(lines)
    
    def create_notable_card_display(self, card_id, pack_number):
        """Create display for notable cards (rare, mythic, special) in 10-pack opening"""
        lines = []
        
        if isinstance(card_id, str):  # Special card
            card = self.special_cards[card_id]
            if card_id == 'ULTRA_LEGENDARY':
                lines.append(f"Pack {pack_number}: 🌟 ULTRA LEGENDARY CARD! 🌟")
                lines.append(f"💎 {card['name']} 💎")
            elif card_id == 'TOMS_MIRROR':
                lines.append(f"Pack {pack_number}: 🪞 TOM'S MIRROR - ULTRA MYTHIC! 🪞")
                lines.append(f"✨ {card['description']} ✨")
            elif card_id == 'ULTRA_RARE_5K':
                lines.append(f"Pack {pack_number}: ✨ ULTRA RARE CARD! ✨")
                lines.append(f"💰 {card['name']} 💰")
            elif card_id == 'ULTRA_RARE_1K':
                lines.append(f"Pack {pack_number}: ⭐ ULTRA RARE CARD! ⭐")
                lines.append(f"💎 {card['name']} 💎")
            elif card_id == 'RARE_500':
                lines.append(f"Pack {pack_number}: 💰 PREMIUM RARE CARD! 💰")
                lines.append(f"🏆 {card['name']} 🏆")
            elif card_id == 'RARE_300':
                lines.append(f"Pack {pack_number}: 🎯 HIGH VALUE RARE! 🎯")
                lines.append(f"💎 {card['name']} 💎")
            else:  # RARE_200
                lines.append(f"Pack {pack_number}: 🔥 VALUABLE RARE! 🔥")
                lines.append(f"⚡ {card['name']} ⚡")
            
            lines.append(f"Power: {card['power']} | Toughness: {card['toughness']}")
            lines.append(f"Sell Value: §{card['sell_min']}-{card['sell_max']}")
        else:
            card = self.cards_database[card_id]
            rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
            lines.append(f"Pack {pack_number}: {rarity_symbol[card['rarity']]} {card['name']}")
            lines.append(f"   {card['power']}/{card['toughness']} | {card['description']}")
            lines.append(f"   Sell Value: §{card['sell_min']}-{card['sell_max']}")
        
        lines.append("```")
        lines.append(card['ascii_art'] if isinstance(card_id, str) else card['ascii_art'])
        lines.append("```")
        lines.append("─" * 50)
        
        return '\n'.join(lines)


class MagicTheShekelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = MagicTheShekellingGame(bot)
        self.PACK_COST = 200
        
        # Crafting recipes
        self.crafting_recipes = {
            'card_nerd': {
                'name': 'Card Nerd',
                'cost': 10000,
                'materials': {'rare_earth_elements': 5},
                'boost': 0.10,
                'description': 'Increases rarity drop chance by 10%'
            },
            'card_store': {
                'name': 'Card Store',
                'cost': 15000,
                'materials': {'quantum_core': 2},
                'boost': 0.20,
                'description': 'Increases rarity drop chance by 20%'
            },
            'card_printer': {
                'name': 'Card Printer',
                'cost': 20000,
                'materials': {'exotic_matter': 1},
                'boost': 0.40,
                'description': 'Increases rarity drop chance by 40%'
            }
        }
        
    @commands.command(aliases=["buypack", "booster", "pack"])
    async def buy_pack(self, ctx):
        """!buypack - Buy a Magic the Shekelling booster pack for 200 shekels"""
        user_id = str(ctx.author.id)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= self.PACK_COST:
            # Remove currency
            self.bot.get_cog('Currency').remove_user_currency(user_id, self.PACK_COST)
            
            # Get rarity boost
            rarity_boost = self.game.get_user_rarity_boost(user_id)
            
            # Generate pack contents with boost
            pack_contents = self.game.get_pack_contents(user_id)
            
            # Create initial embed
            embed = discord.Embed(
                title="🎴 Opening Magic the Shekelling Booster Pack... 🎴",
                description="Your pack is being opened...",
                color=0xFFD700
            )
            
            # Add rarity boost info if applicable
            if rarity_boost > 0:
                embed.add_field(name="🎯 Rarity Boost Active", 
                              value=f"+{rarity_boost*100:.0f}% drop rate boost", 
                              inline=False)
            
            message = await ctx.send(embed=embed)
            
            # Update message with each card reveal
            revealed_cards = []
            for i, card_id in enumerate(pack_contents, 1):
                # Add card to user collection
                if isinstance(card_id, str):  # Special card
                    self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                else:
                    self.game.user_collections[user_id][card_id] += 1
                
                # Create card display
                card_display = self.game.create_card_display(card_id, i)
                revealed_cards.append(card_display)
                
                # Update embed
                embed.description = '\n'.join(revealed_cards)
                
                # Update balance in footer
                new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
                embed.set_footer(text=f"Balance: §{new_balance:.2f}")
                
                await message.edit(embed=embed)
                await asyncio.sleep(1)  # Wait 1 second between reveals
            
            # Final message
            embed.title = "🎴 Magic the Shekelling Booster Pack Opened! 🎴"
            embed.color = 0x00FF00
            await message.edit(embed=embed, delete_after=120)
            
        else:
            await ctx.send(f"You need §{self.PACK_COST} to buy a booster pack. You have §{user_balance:.2f}", 
                         delete_after=10)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["buy10packs", "10packs", "multipacks"])
    async def buy_10_packs(self, ctx):
        """!buy10packs - Buy 10 Magic the Shekelling booster packs for 2000 shekels"""
        user_id = str(ctx.author.id)
        total_cost = self.PACK_COST * 10
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= total_cost:
            # Remove currency
            self.bot.get_cog('Currency').remove_user_currency(user_id, total_cost)
            
            # Get rarity boost
            rarity_boost = self.game.get_user_rarity_boost(user_id)
            
            # Create initial embed
            embed = discord.Embed(
                title="🎴 Opening 10 Magic the Shekelling Booster Packs... 🎴",
                description="Your packs are being opened...",
                color=0xFFD700
            )
            
            # Add rarity boost info if applicable
            if rarity_boost > 0:
                embed.add_field(name="🎯 Rarity Boost Active", 
                              value=f"+{rarity_boost*100:.0f}% drop rate boost", 
                              inline=False)
            
            message = await ctx.send(embed=embed)
            
            # Track notable cards and all cards
            notable_cards = []
            all_cards_count = {'Common': 0, 'Uncommon': 0, 'Rare': 0, 'Mythic': 0, 'Special': 0}
            
            # Open 10 packs
            for pack_num in range(1, 11):
                pack_contents = self.game.get_pack_contents(user_id)
                
                # Process each card in the pack
                for card_id in pack_contents:
                    # Add card to user collection
                    if isinstance(card_id, str):  # Special card
                        self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                        all_cards_count['Special'] += 1
                        # Always show special cards
                        notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                    else:
                        self.game.user_collections[user_id][card_id] += 1
                        card = self.game.cards_database[card_id]
                        all_cards_count[card['rarity']] += 1
                        
                        # Only show rare and mythic cards
                        if card['rarity'] in ['Rare', 'Mythic']:
                            notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                
                # Update embed after each pack
                embed.description = f"Opened {pack_num}/10 packs..."
                await message.edit(embed=embed)
                await asyncio.sleep(0.5)  # Wait 0.5 seconds between packs
            
            # Final message with results
            embed.title = "🎴 10 Magic the Shekelling Booster Packs Opened! 🎴"
            embed.color = 0x00FF00
            
            # Show notable cards
            if notable_cards:
                # Due to Discord's character limit, we might need to split the message
                description_text = '\n'.join(notable_cards)
                if len(description_text) > 4000:  # Leave some room for other embed content
                    # Show first few cards and indicate there are more
                    truncated_cards = []
                    current_length = 0
                    for card_display in notable_cards:
                        if current_length + len(card_display) + 1 < 3500:
                            truncated_cards.append(card_display)
                            current_length += len(card_display) + 1
                        else:
                            break
                    
                    description_text = '\n'.join(truncated_cards)
                    description_text += f"\n\n... and {len(notable_cards) - len(truncated_cards)} more notable cards!"
                
                embed.description = description_text
            else:
                embed.description = "No rare, mythic, or special cards found in these packs!"
            
            # Add summary
            summary_text = f"📊 **Pack Summary:**\n"
            summary_text += f"⚪ Common: {all_cards_count['Common']}\n"
            summary_text += f"🔵 Uncommon: {all_cards_count['Uncommon']}\n"
            summary_text += f"🟡 Rare: {all_cards_count['Rare']}\n"
            summary_text += f"🔴 Mythic: {all_cards_count['Mythic']}\n"
            summary_text += f"🌟 Special: {all_cards_count['Special']}\n"
            
            embed.add_field(name="Summary", value=summary_text, inline=False)
            
            # Update balance in footer
            new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
            embed.set_footer(text=f"Balance: §{new_balance:.2f}")
            
            await message.edit(embed=embed, delete_after=180)  # Show for 3 minutes
            
        else:
            await ctx.send(f"You need §{total_cost} to buy 10 booster packs. You have §{user_balance:.2f}", 
                         delete_after=10)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["collection", "cards", "mycards"])
    async def view_collection(self, ctx, page: int = 1):
        """!collection [page] - View your card collection"""
        user_id = str(ctx.author.id)
        collection = self.game.user_collections[user_id]
        
        if not collection:
            await ctx.send("You don't have any cards yet! Buy a booster pack with !buypack", 
                         delete_after=15)
            return
        
        # Sort cards by rarity and create display
        common_cards = []
        uncommon_cards = []
        rare_cards = []
        mythic_cards = []
        special_cards = []
        
        for card_id, count in collection.items():
            if count > 0:  # Only show cards with count > 0
                if isinstance(card_id, str):  # Special card
                    card = self.game.special_cards[card_id]
                    card_info = f"{card['name']} x{count} (§{card['sell_min']}-{card['sell_max']})"
                    special_cards.append(card_info)
                else:
                    card = self.game.cards_database[card_id]
                    card_info = f"{card['name']} x{count} (§{card['sell_min']}-{card['sell_max']})"
                    
                    if card['rarity'] == 'Common':
                        common_cards.append(card_info)
                    elif card['rarity'] == 'Uncommon':
                        uncommon_cards.append(card_info)
                    elif card['rarity'] == 'Rare':
                        rare_cards.append(card_info)
                    else:  # Mythic
                        mythic_cards.append(card_info)
        
        embed = discord.Embed(
            title=f"🎴 {ctx.author.display_name}'s Card Collection (Page {page})",
            color=0x9932CC
        )
        
        # Add rarity boost info if user has items
        rarity_boost = self.game.get_user_rarity_boost(user_id)
        if rarity_boost > 0:
            embed.add_field(name="🎯 Active Rarity Boost", 
                          value=f"+{rarity_boost*100:.0f}% drop rate boost from items", 
                          inline=False)
        
        # Paginate results
        items_per_page = 5
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        if special_cards:
            embed.add_field(name="🌟 Special Cards", value="\n".join(special_cards[start_idx:end_idx]) or "None on this page", inline=False)
        if mythic_cards:
            embed.add_field(name="🔴 Mythic Cards", value="\n".join(mythic_cards[start_idx:end_idx]) or "None on this page", inline=False)
        if rare_cards:
            embed.add_field(name="🟡 Rare Cards", value="\n".join(rare_cards[start_idx:end_idx]) or "None on this page", inline=False)
        if uncommon_cards:
            embed.add_field(name="🔵 Uncommon Cards", value="\n".join(uncommon_cards[start_idx:end_idx]) or "None on this page", inline=False)
        if common_cards:
            embed.add_field(name="⚪ Common Cards", value="\n".join(common_cards[start_idx:end_idx]) or "None on this page", inline=False)
        
        # Calculate totals only from cards with count > 0
        total_cards = sum(count for count in collection.values() if count > 0)
        total_unique = len([card_id for card_id, count in collection.items() if count > 0])
        embed.add_field(name="📊 Total Cards", value=f"{total_cards} ({total_unique} unique)", inline=True)
        
        # Calculate total pages
        all_cards = special_cards + mythic_cards + rare_cards + uncommon_cards + common_cards
        total_pages = (len(all_cards) + items_per_page - 1) // items_per_page
        if total_pages > 1:
            embed.set_footer(text=f"Page {page}/{total_pages} - Use !collection [page] to see more")
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["m_sellcard"], name="m_sell")
    async def m_sell_card(self, ctx, *, card_name=None):
        """!m_sell [card name] - Sell a card from your collection"""
        if not card_name:
            await ctx.send("Please specify a card name to sell! Example: !m_sell Shekel Goblin", 
                         delete_after=10)
            return
        
        user_id = str(ctx.author.id)
        collection = self.game.user_collections[user_id]
        
        # Find the card
        card_found = None
        card_id_found = None
        
        # Check special cards first
        for special_id, special_card in self.game.special_cards.items():
            if special_card['name'].lower() == card_name.lower() and special_id in collection and collection[special_id] > 0:
                card_found = special_card
                card_id_found = special_id
                break
        
        # Check regular cards if not found in special
        if not card_found:
            for card_id, count in collection.items():
                if count > 0 and not isinstance(card_id, str):
                    card = self.game.cards_database[card_id]
                    if card['name'].lower() == card_name.lower():
                        card_found = card
                        card_id_found = card_id
                        break
        
        if not card_found:
            await ctx.send(f"You don't have any '{card_name}' cards to sell!", delete_after=10)
            return
        
        # Calculate sell value
        sell_value = random.randint(card_found['sell_min'], card_found['sell_max'])
        
        # Remove card from collection and add shekels
        self.game.user_collections[user_id][card_id_found] -= 1
        
        # Remove the card completely if count reaches 0
        if self.game.user_collections[user_id][card_id_found] <= 0:
            del self.game.user_collections[user_id][card_id_found]
        
        self.bot.get_cog('Currency').add_user_currency(user_id, sell_value)
        
        new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        embed = discord.Embed(
            title="💰 Card Sold!",
            description=f"Sold **{card_found['name']}** for §{sell_value}",
            color=0x00FF00
        )
        embed.add_field(name="💰 New Balance", value=f"§{new_balance:.2f}", inline=True)
        
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["selldupes", "sellduplicates", "m_selldupes"])
    async def sell_duplicates(self, ctx):
        """!sellduplicates - Sell all duplicate cards from your collection"""
        user_id = str(ctx.author.id)
        collection = self.game.user_collections[user_id]
        
        if not collection:
            await ctx.send("You don't have any cards to sell!", delete_after=10)
            return
        
        total_sold = 0
        total_value = 0
        cards_sold = []
        
        # Process each card type
        for card_id, count in list(collection.items()):
            if count > 1:
                # Sell all but one
                sell_count = count - 1
                
                if isinstance(card_id, str):  # Special card
                    card = self.game.special_cards[card_id]
                else:
                    card = self.game.cards_database[card_id]
                
                # Calculate total sell value for all duplicates
                card_total = 0
                for _ in range(sell_count):
                    card_total += random.randint(card['sell_min'], card['sell_max'])
                
                total_sold += sell_count
                total_value += card_total
                cards_sold.append(f"{card['name']} x{sell_count} for §{card_total}")
                
                # Update collection
                self.game.user_collections[user_id][card_id] = 1
        
        if total_sold == 0:
            await ctx.send("You don't have any duplicate cards to sell!", delete_after=10)
            return
        
        # Add currency
        self.bot.get_cog('Currency').add_user_currency(user_id, total_value)
        new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        embed = discord.Embed(
            title="💰 Duplicates Sold!",
            description=f"Sold {total_sold} duplicate cards for §{total_value}",
            color=0x00FF00
        )
        
        # Show first 10 cards sold
        if len(cards_sold) <= 10:
            embed.add_field(name="Cards Sold", value="\n".join(cards_sold), inline=False)
        else:
            embed.add_field(name="Cards Sold (showing first 10)", value="\n".join(cards_sold[:10]), inline=False)
            embed.add_field(name="", value=f"...and {len(cards_sold) - 10} more types", inline=False)
        
        embed.add_field(name="💰 New Balance", value=f"§{new_balance:.2f}", inline=True)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["cardinfo", "card"])
    async def view_card(self, ctx, *, card_name=None):
        """!cardinfo [card name] - View detailed information about a card"""
        if not card_name:
            await ctx.send("Please specify a card name! Example: !cardinfo Shekel Goblin", 
                         delete_after=10)
            return
        
        # Find the card in database
        card_found = None
        for card_id, card in self.game.cards_database.items():
            if card['name'].lower() == card_name.lower():
                card_found = card
                break
        
        if not card_found:
            await ctx.send(f"Card '{card_name}' not found!", delete_after=10)
            return
        
        rarity_colors = {
            'Common': 0x808080,
            'Uncommon': 0x0080FF,
            'Rare': 0xFFD700,
            'Mythic': 0xFF4500
        }
        
        embed = discord.Embed(
            title=f"🎴 {card_found['name']}",
            description=f"```\n{card_found['ascii_art']}\n```",
            color=rarity_colors[card_found['rarity']]
        )
        
        embed.add_field(name="⚔️ Power", value=card_found['power'], inline=True)
        embed.add_field(name="🛡️ Toughness", value=card_found['toughness'], inline=True)
        embed.add_field(name="💎 Rarity", value=card_found['rarity'], inline=True)
        embed.add_field(name="📜 Description", value=card_found['description'], inline=False)
        embed.add_field(name="💰 Sell Value", 
                       value=f"§{card_found['sell_min']}-{card_found['sell_max']}", inline=True)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["inventory", "materials", "mats"])
    async def view_inventory(self, ctx):
        """!inventory - View your crafting materials and items"""
        user_id = str(ctx.author.id)
        materials = self.game.user_inventory.get(user_id, {})
        items = self.game.user_items.get(user_id, {})
        
        embed = discord.Embed(
            title=f"🎒 {ctx.author.display_name}'s Inventory",
            color=0x00CED1
        )
        
        # Show materials
        material_text = ""
        if materials.get('rare_earth_elements', 0) > 0:
            material_text += f"🔷 Rare Earth Elements: {materials['rare_earth_elements']}\n"
        if materials.get('quantum_core', 0) > 0:
            material_text += f"⚛️ Quantum Cores: {materials['quantum_core']}\n"
        if materials.get('exotic_matter', 0) > 0:
            material_text += f"✨ Exotic Matter: {materials['exotic_matter']}\n"
        
        if material_text:
            embed.add_field(name="📦 Crafting Materials", value=material_text, inline=False)
        else:
            embed.add_field(name="📦 Crafting Materials", value="No materials yet!", inline=False)
        
        # Show items
        item_text = ""
        total_boost = 0
        if items.get('card_nerd', 0) > 0:
            item_text += f"🤓 Card Nerd: {items['card_nerd']} (+{items['card_nerd']*10}% rarity)\n"
            total_boost += items['card_nerd'] * 0.10
        if items.get('card_store', 0) > 0:
            item_text += f"🏪 Card Store: {items['card_store']} (+{items['card_store']*20}% rarity)\n"
            total_boost += items['card_store'] * 0.20
        if items.get('card_printer', 0) > 0:
            item_text += f"🖨️ Card Printer: {items['card_printer']} (+{items['card_printer']*40}% rarity)\n"
            total_boost += items['card_printer'] * 0.40
        
        if item_text:
            embed.add_field(name="🎯 Rarity Boost Items", value=item_text, inline=False)
            embed.add_field(name="📊 Total Rarity Boost", value=f"+{total_boost*100:.0f}%", inline=True)
        else:
            embed.add_field(name="🎯 Rarity Boost Items", value="No items crafted yet!", inline=False)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["craft", "create"])
    async def craft_item(self, ctx, *, item_name=None):
        """!craft [item name] - Craft a rarity boost item"""
        if not item_name:
            # Show crafting menu
            embed = discord.Embed(
                title="🔨 Crafting Menu",
                description="Available items to craft:",
                color=0xFFD700
            )
            
            for item_id, recipe in self.crafting_recipes.items():
                materials_text = ""
                for mat, count in recipe['materials'].items():
                    mat_display = mat.replace('_', ' ').title()
                    materials_text += f"{count}x {mat_display}\n"
                
                embed.add_field(
                    name=f"{recipe['name']} ({recipe['boost']*100:.0f}% boost)",
                    value=f"Cost: §{recipe['cost']:,}\nMaterials:\n{materials_text}",
                    inline=True
                )
            
            embed.set_footer(text="Use !craft [item name] to craft an item")
            await ctx.send(embed=embed, delete_after=30)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        # Find the item
        item_id = None
        recipe = None
        for id, r in self.crafting_recipes.items():
            if r['name'].lower() == item_name.lower():
                item_id = id
                recipe = r
                break
        
        if not recipe:
            await ctx.send(f"Item '{item_name}' not found! Use !craft to see available items.", 
                         delete_after=10)
            return
        
        user_id = str(ctx.author.id)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        user_materials = self.game.user_inventory.get(user_id, {})
        
        # Check if user has enough shekels
        if user_balance < recipe['cost']:
            await ctx.send(f"You need §{recipe['cost']:,} to craft {recipe['name']}. You have §{user_balance:.2f}", 
                         delete_after=10)
            return
        
        # Check if user has enough materials
        missing_materials = []
        for mat, required in recipe['materials'].items():
            if user_materials.get(mat, 0) < required:
                mat_display = mat.replace('_', ' ').title()
                missing_materials.append(f"{required - user_materials.get(mat, 0)}x {mat_display}")
        
        if missing_materials:
            await ctx.send(f"Missing materials for {recipe['name']}:\n" + "\n".join(missing_materials), 
                         delete_after=15)
            return
        
        # Craft the item
        self.bot.get_cog('Currency').remove_user_currency(user_id, recipe['cost'])
        
        # Remove materials
        for mat, required in recipe['materials'].items():
            self.game.user_inventory[user_id][mat] -= required
            if self.game.user_inventory[user_id][mat] <= 0:
                del self.game.user_inventory[user_id][mat]
        
        # Add the item
        if user_id not in self.game.user_items:
            self.game.user_items[user_id] = {}
        self.game.user_items[user_id][item_id] = self.game.user_items[user_id].get(item_id, 0) + 1
        
        # Calculate new total boost
        total_boost = self.game.get_user_rarity_boost(user_id)
        
        embed = discord.Embed(
            title="🔨 Item Crafted!",
            description=f"Successfully crafted **{recipe['name']}**!",
            color=0x00FF00
        )
        embed.add_field(name="🎯 Effect", value=recipe['description'], inline=False)
        embed.add_field(name="📊 Total Rarity Boost", value=f"+{total_boost*100:.0f}%", inline=True)
        embed.add_field(name="💰 New Balance", value=f"§{self.bot.get_cog('Currency').get_user_currency(user_id):.2f}", inline=True)
        
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    # Add these methods to the cog class
    async def load_data(self):
        """Load user collections, inventory, and items from files"""
        try:
            # Load collections
            with open(f'{self.bot.DATA_PATH}{self.qualified_name}_collections.json', 'r') as f:
                data = json.load(f)
                self.game.user_collections = defaultdict(lambda: defaultdict(int), data)
            print(f"Loaded {len(data)} user collections for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling collections file not found, starting fresh.")
        
        try:
            # Load inventory
            with open(f'{self.bot.DATA_PATH}{self.qualified_name}_inventory.json', 'r') as f:
                data = json.load(f)
                self.game.user_inventory = defaultdict(lambda: defaultdict(int), data)
            print(f"Loaded {len(data)} user inventories for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling inventory file not found, starting fresh.")
        
        try:
            # Load items
            with open(f'{self.bot.DATA_PATH}{self.qualified_name}_items.json', 'r') as f:
                data = json.load(f)
                self.game.user_items = defaultdict(lambda: defaultdict(int), data)
            print(f"Loaded {len(data)} user items for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling items file not found, starting fresh.")

    async def save_data(self):
        """Save user collections, inventory, and items to files"""
        try:
            # Save collections
            with open(f'{self.bot.DATA_PATH}{self.qualified_name}_collections.json', 'w') as f:
                json.dump(dict(self.game.user_collections), f, indent=2)
            
            # Save inventory
            with open(f'{self.bot.DATA_PATH}{self.qualified_name}_inventory.json', 'w') as f:
                json.dump(dict(self.game.user_inventory), f, indent=2)
            
            # Save items
            with open(f'{self.bot.DATA_PATH}{self.qualified_name}_items.json', 'w') as f:
                json.dump(dict(self.game.user_items), f, indent=2)
        except Exception as e:
            print(f"Error saving Magic the Shekelling data: {e}")


async def setup(bot):
    await bot.add_cog(MagicTheShekelling(bot))