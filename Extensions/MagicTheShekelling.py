import asyncio
import json
import random
from collections import defaultdict
import discord
from discord.ext import commands
from MagicTheShekelling.card_database import CardDatabase

# Enhancement items that boost pack rarity rates
ENHANCEMENT_ITEMS = {
    "nerd": {
        "name": "Card Nerd",
        "description": "A knowledgeable collector who knows where to find better cards",
        "cost": 10000,
        "materials": {"rare_earth": 5},
        "rarity_boost": 0.10,  # 10% increase in rare+ card chances
        "emoji": "🤓"
    },
    "store": {
        "name": "Card Store",
        "description": "Your own card shop with premium pack connections",
        "cost": 15000,
        "materials": {"quantum": 2},
        "rarity_boost": 0.20,  # 20% increase in rare+ card chances
        "emoji": "🏪"
    },
    "printer": {
        "name": "Card Printer",
        "description": "Advanced technology to manufacture premium cards",
        "cost": 20000,
        "materials": {"exotic": 1},
        "rarity_boost": 0.40,  # 40% increase in rare+ card chances
        "emoji": "🖨️"
    }
}

class MagicTheShekellingGame:
    def __init__(self, bot):
        self.bot = bot
        self.user_collections = defaultdict(lambda: defaultdict(int))
        self.user_enhancements = defaultdict(list)  # Track user's enhancement items
        self.card_db = CardDatabase()
        self.cards_database = self.card_db.generate_cards_database()
        self.special_cards = self.card_db.special_cards
        
    def get_user_rarity_boost(self, user_id):
        """Calculate total rarity boost from user's enhancement items"""
        total_boost = 0.0
        if user_id in self.user_enhancements:
            for enhancement in self.user_enhancements[user_id]:
                total_boost += ENHANCEMENT_ITEMS[enhancement]["rarity_boost"]
        return total_boost
        
    def get_pack_contents(self, user_id=None):
        """Generate contents of a single pack with potential rarity boosts"""
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
        
        # 1 Rare or Ultra Rare slot with enhanced chances
        rare_roll = random.randint(1, 100000)
        
        # Apply rarity boost by reducing the roll threshold
        boosted_roll = rare_roll * (1 - rarity_boost)
        
        if boosted_roll <= 1:  # 1/100000 for 20k ultra rare (boosted)
            pack.append('ULTRA_LEGENDARY')
        elif boosted_roll <= 2:  # 1/100000 for Tom's Mirror (boosted)
            pack.append('TOMS_MIRROR')
        elif boosted_roll <= 600:  # 599/100000 for 5k ultra rare (boosted)
            pack.append('ULTRA_RARE_5K')
        elif boosted_roll <= 1500:  # 900/100000 for 1k ultra rare (boosted)
            pack.append('ULTRA_RARE_1K')
        elif boosted_roll <= 2800:  # 1300/100000 for 500 shekel rare (boosted)
            pack.append('RARE_500')
        elif boosted_roll <= 4800:  # 2000/100000 for 300 shekel rare (boosted)
            pack.append('RARE_300')
        elif boosted_roll <= 9500:  # 4500/100000 for 200 shekel rare (boosted)
            pack.append('RARE_200')
        else:
            # Regular rare or mythic from remaining percentage (also boosted)
            remaining_chance = random.randint(1, int(30 * (1 - rarity_boost * 0.5)))  # Slight boost to mythic chance too
            if remaining_chance == 1:  # Enhanced mythic chance
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
        
    def get_user_mining_materials(self, user_id):
        """Get user's materials from the mining game"""
        try:
            mining_cog = self.bot.get_cog('MinerGame')
            if not mining_cog:
                return {}
            
            mining_cog.initialize_member_data(user_id)
            return mining_cog.member_materials.get(user_id, {})
        except:
            return {}
    
    def consume_mining_materials(self, user_id, materials_needed):
        """Consume materials from the mining game"""
        try:
            mining_cog = self.bot.get_cog('MinerGame')
            if not mining_cog:
                return False
            
            mining_cog.initialize_member_data(user_id)
            user_materials = mining_cog.member_materials.get(user_id, {})
            
            # Check if user has enough materials
            for material, amount in materials_needed.items():
                if user_materials.get(material, 0) < amount:
                    return False
            
            # Consume the materials
            for material, amount in materials_needed.items():
                user_materials[material] -= amount
            
            return True
        except:
            return False
        
    @commands.command(aliases=["buypack", "booster", "pack"])
    async def buy_pack(self, ctx):
        """!buypack - Buy a Magic the Shekelling booster pack for 200 shekels"""
        user_id = str(ctx.author.id)
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        
        if float(user_balance) >= self.PACK_COST:
            # Remove currency
            self.bot.get_cog('Currency').remove_user_currency(user_id, self.PACK_COST)
            
            # Generate pack contents with user's rarity boost
            pack_contents = self.game.get_pack_contents(user_id)
            
            # Create initial embed
            rarity_boost = self.game.get_user_rarity_boost(user_id)
            boost_text = f" (Rarity Boost: +{rarity_boost*100:.0f}%)" if rarity_boost > 0 else ""
            
            embed = discord.Embed(
                title=f"🎴 Opening Magic the Shekelling Booster Pack...{boost_text} 🎴",
                description="Your pack is being opened...",
                color=0xFFD700
            )
            
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
            embed.title = f"🎴 Magic the Shekelling Booster Pack Opened!{boost_text} 🎴"
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
            rarity_boost = self.game.get_user_rarity_boost(user_id)
            boost_text = f" (Rarity Boost: +{rarity_boost*100:.0f}%)" if rarity_boost > 0 else ""
            
            embed = discord.Embed(
                title=f"🎴 Opening 10 Magic the Shekelling Booster Packs...{boost_text} 🎴",
                description="Your packs are being opened...",
                color=0xFFD700
            )
            
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
            embed.title = f"🎴 10 Magic the Shekelling Booster Packs Opened!{boost_text} 🎴"
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
    
    @commands.command(aliases=["buyenhancement", "enhancement"])
    async def buy_enhancement(self, ctx, enhancement_name: str = ""):
        """!buy enhancement [name] - Buy enhancement items using shekels and mining materials
        
        Available enhancements:
        🤓 Card Nerd - 10k shekels + 5 Rare Earth Elements (+10% rarity boost)
        🏪 Card Store - 15k shekels + 2 Quantum Cores (+20% rarity boost)  
        🖨️ Card Printer - 20k shekels + 1 Exotic Matter (+40% rarity boost)
        
        Enhancements stack and permanently boost your pack opening luck!
        Materials come from the mining game - use !materials to check what you have.
        """
        user_id = str(ctx.author.id)
        enhancement_name = enhancement_name.lower()
        
        if not enhancement_name:
            # Show available enhancements
            embed = discord.Embed(
                title="🔧 Enhancement Items Available",
                description="Use materials from mining to boost your pack luck!",
                color=0x9932CC
            )
            
            user_materials = self.get_user_mining_materials(user_id)
            user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
            current_boost = self.game.get_user_rarity_boost(user_id)
            
            for item_id, item_data in ENHANCEMENT_ITEMS.items():
                materials_text = ""
                can_afford = True
                
                for mat, amount in item_data["materials"].items():
                    user_has = user_materials.get(mat, 0)
                    materials_text += f"{amount} {mat.replace('_', ' ').title()} ({user_has} owned)\n"
                    if user_has < amount:
                        can_afford = False
                
                if user_balance < item_data["cost"]:
                    can_afford = False
                
                status = "✅ Can afford" if can_afford else "❌ Cannot afford"
                
                embed.add_field(
                    name=f"{item_data['emoji']} {item_data['name']} (+{item_data['rarity_boost']*100:.0f}% rarity)",
                    value=f"Cost: §{item_data['cost']:,}\n{materials_text}{status}",
                    inline=True
                )
            
            if current_boost > 0:
                embed.set_footer(text=f"Current total rarity boost: +{current_boost*100:.0f}%")
            else:
                embed.set_footer(text="No current rarity boosts - buy enhancements to improve your luck!")
            
            await ctx.send(embed=embed, delete_after=60)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        if enhancement_name not in ENHANCEMENT_ITEMS:
            await ctx.send(f"Invalid enhancement! Use: {', '.join(ENHANCEMENT_ITEMS.keys())}", 
                         delete_after=10)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        enhancement = ENHANCEMENT_ITEMS[enhancement_name]
        user_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
        user_materials = self.get_user_mining_materials(user_id)
        
        # Check if user can afford it
        if user_balance < enhancement["cost"]:
            await ctx.send(f"You need §{enhancement['cost']:,} to buy {enhancement['name']}. You have §{user_balance:.2f}", 
                         delete_after=10)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        # Check materials
        missing_materials = []
        for material, amount in enhancement["materials"].items():
            user_has = user_materials.get(material, 0)
            if user_has < amount:
                missing_materials.append(f"{amount - user_has} more {material.replace('_', ' ').title()}")
        
        if missing_materials:
            await ctx.send(f"You need: {', '.join(missing_materials)} to buy {enhancement['name']}", 
                         delete_after=15)
            await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
            return
        
        # Purchase the enhancement
        self.bot.get_cog('Currency').remove_user_currency(user_id, enhancement["cost"])
        
        if self.consume_mining_materials(user_id, enhancement["materials"]):
            self.game.user_enhancements[user_id].append(enhancement_name)
            
            new_total_boost = self.game.get_user_rarity_boost(user_id)
            
            embed = discord.Embed(
                title="🎉 Enhancement Purchased!",
                description=f"You bought {enhancement['emoji']} **{enhancement['name']}**!",
                color=0x00FF00
            )
            embed.add_field(name="Rarity Boost", value=f"+{enhancement['rarity_boost']*100:.0f}%", inline=True)
            embed.add_field(name="Total Boost", value=f"+{new_total_boost*100:.0f}%", inline=True)
            embed.add_field(name="Description", value=enhancement["description"], inline=False)
            
            new_balance = self.bot.get_cog('Currency').get_user_currency(user_id)
            embed.set_footer(text=f"New balance: §{new_balance:.2f}")
            
            await ctx.send(embed=embed, delete_after=30)
        else:
            # Refund if material consumption failed
            self.bot.get_cog('Currency').add_user_currency(user_id, enhancement["cost"])
            await ctx.send("Failed to consume materials - purchase cancelled and refunded.", 
                         delete_after=10)
        
        await ctx.message.delete(delay=self.bot.SHORT_DELETE_DELAY)
    
    @commands.command(aliases=["enhancements", "myenhancements", "boosts"])
    async def view_enhancements(self, ctx, member: discord.Member = None):
        """!enhancements - View your enhancement items and total rarity boost"""
        member = member or ctx.author
        user_id = str(member.id)
        
        user_enhancements = self.game.user_enhancements.get(user_id, [])
        total_boost = self.game.get_user_rarity_boost(user_id)
        
        embed = discord.Embed(
            title=f"🔧 {member.display_name}'s Enhancement Items",
            color=0x9932CC
        )
        
        if user_enhancements:
            enhancement_list = []
            for enhancement_id in user_enhancements:
                enhancement = ENHANCEMENT_ITEMS[enhancement_id]
                enhancement_list.append(f"{enhancement['emoji']} **{enhancement['name']}** (+{enhancement['rarity_boost']*100:.0f}%)")
            
            embed.add_field(name="Owned Enhancements", value="\n".join(enhancement_list), inline=False)
            embed.add_field(name="📈 Total Rarity Boost", value=f"+{total_boost*100:.0f}%", inline=True)
            
            # Calculate enhanced drop rates
            base_rare_chance = 9.5  # Base 9.5% for rare+ cards
            enhanced_chance = base_rare_chance * (1 + total_boost)
            embed.add_field(name="🎯 Enhanced Rare+ Chance", value=f"{enhanced_chance:.1f}%", inline=True)
        else:
            embed.description = "No enhancement items owned yet!\nUse `!buy enhancement` to see available items."
        
        await ctx.send(embed=embed, delete_after=60)
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
        
        # Show rarity boost if any
        rarity_boost = self.game.get_user_rarity_boost(user_id)
        if rarity_boost > 0:
            embed.add_field(name="🔧 Rarity Boost", value=f"+{rarity_boost*100:.0f}%", inline=True)
        
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
    
    @commands.command(aliases=["help_enhancement", "helpenhancement"])
    async def help_enhancement(self, ctx):
        """!help enhancement - Detailed explanation of the enhancement system"""
        
        help_msg = """**🔧 Magic the Shekelling Enhancement System**

        **How Enhancements Work:**
        • Enhancement items permanently boost your pack opening luck
        • They use materials from the Mining Game plus shekels
        • Multiple enhancements stack for even better odds
        • Boosts apply to both single packs and 10-pack openings

        **Available Enhancement Items:**
        ```
        Item          | Cost        | Materials        | Rarity Boost
        --------------|-------------|------------------|-------------
        🤓 Card Nerd  | 10k shekels | 5 Rare Earth    | +10%
        🏪 Card Store | 15k shekels | 2 Quantum Cores | +20%  
        🖨️ Card Printer| 20k shekels | 1 Exotic Matter | +40%
        ```

        **Getting Materials:**
        • Materials drop from miners in the Mining Game
        • Higher tier miners have better material drop rates
        • Use `!materials` to see what mining materials you have

        **How Rarity Boost Works:**
        • Base chance for rare+ cards: ~9.5%
        • With +10% boost: ~10.45% chance
        • With +40% boost: ~13.3% chance
        • Boosts stack: Card Nerd + Store + Printer = +70% total!

        **Example Enhancement Path:**
        1. Start mining to collect Rare Earth Elements
        2. Buy Card Nerd for your first +10% boost
        3. Continue mining for Quantum Cores
        4. Buy Card Store for +20% more (+30% total)
        5. Hunt for Exotic Matter (very rare!)
        6. Buy Card Printer for ultimate +40% more (+70% total!)

        **Commands:**
        • `!buy enhancement` - See available enhancements
        • `!buy enhancement nerd` - Buy the Card Nerd
        • `!enhancements` - View your owned enhancements
        • `!materials` - Check mining materials (from Mining Game)
        
        **Cross-Game Synergy:**
        This creates a powerful connection between Mining and Card collecting!
        The more you mine, the better your card packs become.
        """

        await ctx.send(help_msg, delete_after=self.bot.LONG_DELETE_DELAY)
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
        
        # Load enhancements from separate file
        try:
            with open(f'/app/data/{self.qualified_name}_enhancements.json', 'r') as f:
                enhancement_data = json.load(f)
                self.game.user_enhancements = defaultdict(list, enhancement_data)
                print(f"Loaded {len(enhancement_data)} enhancement profiles for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling enhancements file not found, starting fresh.")

    async def save_data(self):
        """Save user collections to file"""
        try:
            with open(f'/app/data/{self.qualified_name}_collections.json', 'w') as f:
                json.dump(dict(self.game.user_collections), f, indent=2)
        except Exception as e:
            print(f"Error saving Magic the Shekelling collections data: {e}")
        
        # Save enhancements to separate file
        try:
            with open(f'/app/data/{self.qualified_name}_enhancements.json', 'w') as f:
                json.dump(dict(self.game.user_enhancements), f, indent=2)
        except Exception as e:
            print(f"Error saving Magic the Shekelling enhancements data: {e}")

async def setup(bot):
    await bot.add_cog(MagicTheShekelling(bot))