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
        self.card_db = CardDatabase()
        self.cards_database = self.card_db.generate_cards_database()
        self.special_cards = self.card_db.special_cards
        self.holo_special_cards = self.card_db.holo_special_cards
        
    def get_pack_contents(self):
        """Generate contents of a single pack"""
        pack = []
        
        # 7 Common cards (with holo foil chance)
        common_ids = [i for i in range(1, 65)]
        for _ in range(7):
            card_id = random.choice(common_ids)
            # 1 in 3 chance for holo foil (3 times more rare)
            if random.randint(1, 3) == 1:
                pack.append(f"HOLO_{card_id}")
            else:
                pack.append(card_id)
        
        # 2 Uncommon cards (with holo foil chance)
        uncommon_ids = [i for i in range(65, 97)]
        for _ in range(2):
            card_id = random.choice(uncommon_ids)
            # 1 in 3 chance for holo foil (3 times more rare)
            if random.randint(1, 3) == 1:
                pack.append(f"HOLO_{card_id}")
            else:
                pack.append(card_id)
        
        # 1 Rare or Ultra Rare slot
        rare_roll = random.randint(1, 100000)
        
        if rare_roll == 1:  # 1/100000 for 20k ultra rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_ULTRA_LEGENDARY')
            else:
                pack.append('ULTRA_LEGENDARY')
        elif rare_roll == 2:  # 1/100000 for Tom's Mirror
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_TOMS_MIRROR')
            else:
                pack.append('TOMS_MIRROR')
        elif rare_roll <= 50:  # 49/100000 for 20k ultra rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_ULTRA_RARE_20K')
            else:
                pack.append('ULTRA_RARE_20K')
        elif rare_roll <= 150:  # 100/100000 for 10k ultra rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_ULTRA_RARE_10K')
            else:
                pack.append('ULTRA_RARE_10K')
        elif rare_roll <= 600:  # 450/100000 for 5k ultra rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_ULTRA_RARE_5K')
            else:
                pack.append('ULTRA_RARE_5K')
        elif rare_roll <= 1500:  # 900/100000 (about 1/111) for 1k ultra rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_ULTRA_RARE_1K')
            else:
                pack.append('ULTRA_RARE_1K')
        elif rare_roll <= 2800:  # 1300/100000 (about 1/77) for 500 shekel rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_RARE_500')
            else:
                pack.append('RARE_500')
        elif rare_roll <= 4800:  # 2000/100000 (1/50) for 300 shekel rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_RARE_300')
            else:
                pack.append('RARE_300')
        elif rare_roll <= 9500:  # 4500/100000 (about 1/22) for 200 shekel rare
            # Check for holo foil
            if random.randint(1, 3) == 1:
                pack.append('HOLO_RARE_200')
            else:
                pack.append('RARE_200')
        else:
            # Regular rare or mythic from remaining 90.5%
            remaining_chance = random.randint(1, 30)
            if remaining_chance == 1:  # 1/30 for mythic
                mythic_ids = [i for i in range(127, 152)]
                card_id = random.choice(mythic_ids)
                # Check for holo foil
                if random.randint(1, 3) == 1:
                    pack.append(f"HOLO_{card_id}")
                else:
                    pack.append(card_id)
            else:  # Regular rare
                rare_ids = [i for i in range(97, 127)]
                card_id = random.choice(rare_ids)
                # Check for holo foil
                if random.randint(1, 3) == 1:
                    pack.append(f"HOLO_{card_id}")
                else:
                    pack.append(card_id)
        
        return pack
    
    def create_card_display(self, card_id, index):
        """Create display for a single card"""
        lines = []
        
        if isinstance(card_id, str):  # Special or holo card
            # Check if it's a holo special card
            if card_id.startswith('HOLO_'):
                if card_id in self.card_db.holo_special_cards:
                    card = self.card_db.holo_special_cards[card_id]
                    lines.append(f"{index}. ✧ HOLO FOIL ✧ {card['name']} ✧")
                else:
                    # It's a holo regular card
                    original_id = int(card_id.replace('HOLO_', ''))
                    card = self.cards_database[f"HOLO_{original_id}"]
                    rarity_symbol = {'Holo Common': '◇', 'Holo Uncommon': '◈', 'Holo Rare': '◉', 'Holo Mythic': '◊'}
                    lines.append(f"{index}. ✧ {rarity_symbol.get(card['rarity'], '◇')} HOLO FOIL {card['name']} ✧")
            else:
                # Regular special card
                card = self.special_cards[card_id]
                if card_id == 'ULTRA_LEGENDARY':
                    lines.append(f"{index}. 🌟 ULTRA LEGENDARY CARD! 🌟")
                    lines.append(f"💎 {card['name']} 💎")
                elif card_id == 'TOMS_MIRROR':
                    lines.append(f"{index}. 🪞 TOM'S MIRROR - ULTRA MYTHIC! 🪞")
                    lines.append(f"✨ {card['description']} ✨")
                elif card_id == 'ULTRA_RARE_20K':
                    lines.append(f"{index}. 🌌 COSMIC ULTRA RARE! 🌌")
                    lines.append(f"💫 {card['name']} 💫")
                elif card_id == 'ULTRA_RARE_10K':
                    lines.append(f"{index}. 👑 PLATINUM ULTRA RARE! 👑")
                    lines.append(f"💎 {card['name']} 💎")
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
            # Regular card
            card = self.cards_database[card_id]
            rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
            lines.append(f"{index}. {rarity_symbol[card['rarity']]} {card['name']}")
            lines.append(f"   {card['power']}/{card['toughness']} | {card['description']}")
            lines.append(f"   Sell Value: §{card['sell_min']}-{card['sell_max']}")
        
        lines.append("```")
        lines.append(card['ascii_art'])
        lines.append("```")
        lines.append("─" * 50)
        
        return '\n'.join(lines)
    
    def create_notable_card_display(self, card_id, pack_number):
        """Create display for notable cards (rare, mythic, special) in 10-pack opening"""
        lines = []
        
        if isinstance(card_id, str):  # Special or holo card
            # Check if it's a holo special card
            if card_id.startswith('HOLO_'):
                if card_id in self.card_db.holo_special_cards:
                    card = self.card_db.holo_special_cards[card_id]
                    lines.append(f"Pack {pack_number}: ✧ HOLO FOIL ✧ {card['name']} ✧")
                else:
                    # It's a holo regular card
                    original_id = int(card_id.replace('HOLO_', ''))
                    card = self.cards_database[f"HOLO_{original_id}"]
                    rarity_symbol = {'Holo Common': '◇', 'Holo Uncommon': '◈', 'Holo Rare': '◉', 'Holo Mythic': '◊'}
                    lines.append(f"Pack {pack_number}: ✧ {rarity_symbol.get(card['rarity'], '◇')} HOLO FOIL {card['name']} ✧")
            else:
                # Regular special card
                card = self.special_cards[card_id]
                if card_id == 'ULTRA_LEGENDARY':
                    lines.append(f"Pack {pack_number}: 🌟 ULTRA LEGENDARY CARD! 🌟")
                    lines.append(f"💎 {card['name']} 💎")
                elif card_id == 'TOMS_MIRROR':
                    lines.append(f"Pack {pack_number}: 🪞 TOM'S MIRROR - ULTRA MYTHIC! 🪞")
                    lines.append(f"✨ {card['description']} ✨")
                elif card_id == 'ULTRA_RARE_20K':
                    lines.append(f"Pack {pack_number}: 🌌 COSMIC ULTRA RARE! 🌌")
                    lines.append(f"💫 {card['name']} 💫")
                elif card_id == 'ULTRA_RARE_10K':
                    lines.append(f"Pack {pack_number}: 👑 PLATINUM ULTRA RARE! 👑")
                    lines.append(f"💎 {card['name']} 💎")
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
            # Regular card
            card = self.cards_database[card_id]
            rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
            lines.append(f"Pack {pack_number}: {rarity_symbol[card['rarity']]} {card['name']}")
            lines.append(f"   {card['power']}/{card['toughness']} | {card['description']}")
            lines.append(f"   Sell Value: §{card['sell_min']}-{card['sell_max']}")
        
        lines.append("```")
        lines.append(card['ascii_art'])
        lines.append("```")
        lines.append("─" * 50)
        
        return '\n'.join(lines)


class MagicTheShekelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = MagicTheShekellingGame(bot)
        self.PACK_COST = 200
        
    @commands.command(aliases=["buypack", "booster", "pack"])
    async def buy_pack(self, ctx):
        """!buypack - Buy a Magic the Shekelling booster pack for 200 shekels"""
        user_id = str(ctx.author.id)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= self.PACK_COST:
            # Remove currency
            self.bot.get_cog('Currency').remove_user_currency(user_id, self.PACK_COST)
            
            # Generate pack contents
            pack_contents = self.game.get_pack_contents()
            
            # Create initial embed
            embed = discord.Embed(
                title="🎴 Opening Magic the Shekelling Booster Pack... 🎴",
                description="Your pack is being opened...",
                color=0xFFD700
            )
            
            message = await ctx.send(embed=embed)
            
            # Update message with each card reveal
            revealed_cards = []
            for i, card_id in enumerate(pack_contents, 1):
                # Add card to user collection
                if isinstance(card_id, str):  # Special or holo card
                    if card_id.startswith('HOLO_'):
                        # Check if it's a holo special card or regular holo card
                        if card_id in self.game.card_db.holo_special_cards:
                            self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                        else:
                            # It's a holo regular card
                            self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                    else:
                        # Regular special card
                        self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                else:
                    # Regular card
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
            
            # Create initial embed
            embed = discord.Embed(
                title="🎴 Opening 10 Magic the Shekelling Booster Packs... 🎴",
                description="Your packs are being opened...",
                color=0xFFD700
            )
            
            message = await ctx.send(embed=embed)
            
            # Track notable cards and all cards
            notable_cards = []
            all_cards_count = {'Common': 0, 'Uncommon': 0, 'Rare': 0, 'Mythic': 0, 'Special': 0}
            
            # Open 10 packs
            for pack_num in range(1, 11):
                pack_contents = self.game.get_pack_contents()
                
                # Process each card in the pack
                for card_id in pack_contents:
                    # Add card to user collection
                    if isinstance(card_id, str):  # Special or holo card
                        if card_id.startswith('HOLO_'):
                            # Check if it's a holo special card or regular holo card
                            if card_id in self.game.card_db.holo_special_cards:
                                self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                                all_cards_count['Special'] += 1
                                # Always show holo special cards
                                notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                            else:
                                # It's a holo regular card
                                self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                                original_id = int(card_id.replace('HOLO_', ''))
                                card = self.game.cards_database[f"HOLO_{original_id}"]
                                rarity_base = card['rarity'].replace('Holo ', '')
                                all_cards_count[rarity_base] += 1
                                
                                # Show holo rare and mythic cards
                                if rarity_base in ['Rare', 'Mythic']:
                                    notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                        else:
                            # Regular special card
                            self.game.user_collections[user_id][card_id] = self.game.user_collections[user_id].get(card_id, 0) + 1
                            all_cards_count['Special'] += 1
                            # Always show special cards
                            notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                    else:
                        # Regular card
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
        holo_cards = []
        
        for card_id, count in collection.items():
            if count > 0:  # Only show cards with count > 0
                if isinstance(card_id, str):  # Special or holo card
                    if card_id.startswith('HOLO_'):
                        if card_id in self.game.card_db.holo_special_cards:
                            card = self.game.card_db.holo_special_cards[card_id]
                        else:
                            original_id = int(card_id.replace('HOLO_', ''))
                            card = self.game.cards_database[f"HOLO_{original_id}"]
                        card_info = f"✧ {card['name']} x{count} (§{card['sell_min']}-{card['sell_max']})"
                        holo_cards.append(card_info)
                    else:
                        # Regular special card
                        card = self.game.special_cards[card_id]
                        card_info = f"{card['name']} x{count} (§{card['sell_min']}-{card['sell_max']})"
                        special_cards.append(card_info)
                else:
                    # Regular card
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
        
        # Paginate results
        items_per_page = 5
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        if holo_cards:
            embed.add_field(name="✧ Holo Foil Cards", value="\n".join(holo_cards[start_idx:end_idx]) or "None on this page", inline=False)
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
        all_cards = holo_cards + special_cards + mythic_cards + rare_cards + uncommon_cards + common_cards
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
        
        # Check holo special cards first
        for holo_special_id, holo_special_card in self.game.card_db.holo_special_cards.items():
            if holo_special_card['name'].lower() == card_name.lower() and holo_special_id in collection and collection[holo_special_id] > 0:
                card_found = holo_special_card
                card_id_found = holo_special_id
                break
        
        # Check special cards if not found in holo special
        if not card_found:
            for special_id, special_card in self.game.special_cards.items():
                if special_card['name'].lower() == card_name.lower() and special_id in collection and collection[special_id] > 0:
                    card_found = special_card
                    card_id_found = special_id
                    break
        
        # Check holo regular cards if not found in special
        if not card_found:
            for card_id, count in collection.items():
                if count > 0 and isinstance(card_id, str) and card_id.startswith('HOLO_'):
                    original_id = int(card_id.replace('HOLO_', ''))
                    if f"HOLO_{original_id}" in self.game.cards_database:
                        card = self.game.cards_database[f"HOLO_{original_id}"]
                        if card['name'].lower() == card_name.lower():
                            card_found = card
                            card_id_found = card_id
                            break
        
        # Check regular cards if not found in holo
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
                
                if isinstance(card_id, str):  # Special or holo card
                    if card_id.startswith('HOLO_'):
                        if card_id in self.game.card_db.holo_special_cards:
                            card = self.game.card_db.holo_special_cards[card_id]
                        else:
                            original_id = int(card_id.replace('HOLO_', ''))
                            card = self.game.cards_database[f"HOLO_{original_id}"]
                    else:
                        # Regular special card
                        card = self.game.special_cards[card_id]
                else:
                    # Regular card
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
        is_holo = False
        
        # Check holo special cards first
        for holo_special_id, holo_special_card in self.game.card_db.holo_special_cards.items():
            if holo_special_card['name'].lower() == card_name.lower():
                card_found = holo_special_card
                is_holo = True
                break
        
        # Check special cards if not found in holo special
        if not card_found:
            for special_id, special_card in self.game.special_cards.items():
                if special_card['name'].lower() == card_name.lower():
                    card_found = special_card
                    break
        
        # Check holo regular cards if not found in special
        if not card_found:
            for card_id, card in self.game.cards_database.items():
                if isinstance(card_id, str) and card_id.startswith('HOLO_'):
                    if card['name'].lower() == card_name.lower():
                        card_found = card
                        is_holo = True
                        break
        
        # Check regular cards if not found in holo
        if not card_found:
            for card_id, card in self.game.cards_database.items():
                if not isinstance(card_id, str) and card['name'].lower() == card_name.lower():
                    card_found = card
                    break
        
        if not card_found:
            await ctx.send(f"Card '{card_name}' not found!", delete_after=10)
            return
        
        rarity_colors = {
            'Common': 0x808080,
            'Uncommon': 0x0080FF,
            'Rare': 0xFFD700,
            'Mythic': 0xFF4500,
            'Holo Common': 0xC0C0C0,
            'Holo Uncommon': 0x40A0FF,
            'Holo Rare': 0xFFE55C,
            'Holo Mythic': 0xFF7F50,
            'Ultra Legendary': 0xFF00FF,
            'Ultra Mythic': 0x9400D3,
            'Ultra Rare': 0xFF1493,
            'Premium Rare': 0x8B4513,
            'High Value Rare': 0xDC143C,
            'Valuable Rare': 0xB22222
        }
        
        title = f"🎴 {card_found['name']}"
        if is_holo:
            title = f"✧ {title} ✧"
        
        embed = discord.Embed(
            title=title,
            description=f"```\n{card_found['ascii_art']}\n```",
            color=rarity_colors.get(card_found['rarity'], 0x808080)
        )
        
        embed.add_field(name="⚔️ Power", value=card_found['power'], inline=True)
        embed.add_field(name="🛡️ Toughness", value=card_found['toughness'], inline=True)
        embed.add_field(name="💎 Rarity", value=card_found['rarity'], inline=True)
        embed.add_field(name="📜 Description", value=card_found['description'], inline=False)
        embed.add_field(name="💰 Sell Value", 
                       value=f"§{card_found['sell_min']}-{card_found['sell_max']}", inline=True)
        
        await ctx.send(embed=embed, delete_after=60)
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    

async def load_data(self):
    """Load user collections from file"""
    try:
        with open(f'/app/data/{self.qualified_name}_collections.json', 'r') as f:
            data = json.load(f)
            self.game.user_collections = defaultdict(lambda: defaultdict(int), data)
            print(f"Loaded {len(data)} user collections for Magic the Shekelling.")
    except FileNotFoundError:
        print("Magic the Shekelling collections file not found, starting fresh.")

async def save_data(self):
    """Save user collections to file"""
    try:
        with open(f'/app/data/{self.qualified_name}_collections.json', 'w') as f:
            json.dump(dict(self.game.user_collections), f, indent=2)
    except Exception as e:
        print(f"Error saving Magic the Shekelling data: {e}")

async def setup(bot):
    await bot.add_cog(MagicTheShekelling(bot))
    