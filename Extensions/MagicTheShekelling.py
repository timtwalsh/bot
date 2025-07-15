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
        self.user_enhancements = defaultdict(lambda: defaultdict(int))  # Track enhancement items
        self.card_db = CardDatabase()
        self.cards_database = self.card_db.generate_cards_database()
        self.special_cards = self.card_db.special_cards
        
        # Enhancement items that boost card pack odds
        self.enhancement_items = {
            "card_nerd": {
                "name": "Card Nerd",
                "description": "A fellow enthusiast who increases your pack luck!",
                "cost": 10000,
                "materials": {"rare_earth": 5},
                "rarity_boost": 0.10,  # 10% boost to rare+ drops
                "ascii_art": """
   🤓
  /|\\
   |
  / \\
NERD!
                """
            },
            "card_store": {
                "name": "Card Store",
                "description": "Your own shop with premium pack connections!",
                "cost": 15000,
                "materials": {"quantum": 2},
                "rarity_boost": 0.20,  # 20% boost to rare+ drops
                "ascii_art": """
┌─────────┐
│ CARDS!! │
│ [$$] ⭐  │
│ STORE   │
└─────────┘
                """
            },
            "card_printer": {
                "name": "Card Printer",
                "description": "Mysterious device that prints premium cards!",
                "cost": 20000,
                "materials": {"exotic": 1},
                "rarity_boost": 0.40,  # 40% boost to rare+ drops
                "ascii_art": """
┌─────────┐
│░░░░░░░░░│
│░ PRINT ░│
│░ CARDS ░│
│░░░░░░░░░│
└─────────┘
                """
            }
        }
        
    def get_user_rarity_boost(self, user_id):
        """Calculate total rarity boost from user's enhancement items"""
        total_boost = 0.0
        for item_id, item_data in self.enhancement_items.items():
            if self.user_enhancements[user_id][item_id] > 0:
                total_boost += item_data["rarity_boost"]
        return min(total_boost, 2.0)  # Cap at 200% boost

    def get_pack_contents(self, user_id=None):
        """Generate contents of a single pack with potential rarity boost"""
        pack = []
        
        # Calculate rarity boost
        rarity_boost = 0.0
        if user_id:
            rarity_boost = self.get_user_rarity_boost(user_id)
        
        # 7 Common cards (some might upgrade to uncommon with boost)
        common_ids = [i for i in range(1, 65)]
        uncommon_ids = [i for i in range(65, 97)]
        
        for _ in range(7):
            if random.random() < rarity_boost * 0.3:  # 30% of boost affects common->uncommon
                pack.append(random.choice(uncommon_ids))
            else:
                pack.append(random.choice(common_ids))
        
        # 2 Uncommon cards (some might upgrade to rare with boost)
        rare_ids = [i for i in range(97, 127)]
        for _ in range(2):
            if random.random() < rarity_boost * 0.5:  # 50% of boost affects uncommon->rare
                pack.append(random.choice(rare_ids))
            else:
                pack.append(random.choice(uncommon_ids))
        
        # 1 Rare or Ultra Rare slot (enhanced by boost)
        rare_roll = random.randint(1, 100000)
        
        # Apply rarity boost to rare rolls (makes better cards more likely)
        boosted_threshold = int(9500 * (1 + rarity_boost))  # Increase chance of special cards
        
        if rare_roll == 1:  # 1/100000 for 20k ultra rare
            pack.append('ULTRA_LEGENDARY')
        elif rare_roll == 2:  # 1/100000 for Tom's Mirror
            pack.append('TOMS_MIRROR')
        elif rare_roll <= int(600 * (1 + rarity_boost * 2)):  # Enhanced ultra rare chance
            pack.append('ULTRA_RARE_5K')
        elif rare_roll <= int(1500 * (1 + rarity_boost * 1.8)):
            pack.append('ULTRA_RARE_1K')
        elif rare_roll <= int(2800 * (1 + rarity_boost * 1.6)):
            pack.append('RARE_500')
        elif rare_roll <= int(4800 * (1 + rarity_boost * 1.4)):
            pack.append('RARE_300')
        elif rare_roll <= int(9500 * (1 + rarity_boost * 1.2)):
            pack.append('RARE_200')
        else:
            # Regular rare or mythic from remaining percentage
            remaining_chance = random.randint(1, 30)
            mythic_chance = int(1 / (1 - rarity_boost * 0.5)) if rarity_boost > 0 else 1
            if remaining_chance <= mythic_chance:  # Enhanced mythic chance
                mythic_ids = [i for i in range(127, 152)]
                pack.append(random.choice(mythic_ids))
            else:  # Regular rare
                pack.append(random.choice(rare_ids))
        
        return pack
    
    def create_card_display(self, card_id, index):
        """Create display for a single card"""
        lines = []
        
        try:
            if isinstance(card_id, str):  # Special card
                if card_id not in self.special_cards:
                    lines.append(f"{index}. ❌ Unknown Special Card: {card_id}")
                    lines.append("```\n[ERROR: Card not found]\n```")
                    return '\n'.join(lines)
                    
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
                
                lines.append(f"Power: {card.get('power', 'N/A')} | Toughness: {card.get('toughness', 'N/A')}")
                lines.append(f"Sell Value: §{card.get('sell_min', 0)}-{card.get('sell_max', 0)}")
            else:
                if card_id not in self.cards_database:
                    lines.append(f"{index}. ❌ Unknown Card ID: {card_id}")
                    lines.append("```\n[ERROR: Card not found]\n```")
                    return '\n'.join(lines)
                    
                card = self.cards_database[card_id]
                rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
                symbol = rarity_symbol.get(card.get('rarity', 'Common'), '⚪')
                lines.append(f"{index}. {symbol} {card.get('name', 'Unknown Card')}")
                lines.append(f"   {card.get('power', 'N/A')}/{card.get('toughness', 'N/A')} | {card.get('description', 'No description')}")
                lines.append(f"   Sell Value: §{card.get('sell_min', 0)}-{card.get('sell_max', 0)}")
            
            lines.append("```")
            ascii_art = card.get('ascii_art', '[No ASCII art available]')
            lines.append(ascii_art)
            lines.append("```")
            lines.append("─" * 50)
            
        except Exception as e:
            lines = [f"{index}. ❌ Error displaying card: {str(e)}", "```\n[Display Error]\n```"]
            
        return '\n'.join(lines)
    
    def create_notable_card_display(self, card_id, pack_number):
        """Create display for notable cards (rare, mythic, special) in 10-pack opening"""
        lines = []
        
        try:
            if isinstance(card_id, str):  # Special card
                if card_id not in self.special_cards:
                    lines.append(f"Pack {pack_number}: ❌ Unknown Special Card: {card_id}")
                    return '\n'.join(lines)
                    
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
                
                lines.append(f"Power: {card.get('power', 'N/A')} | Toughness: {card.get('toughness', 'N/A')}")
                lines.append(f"Sell Value: §{card.get('sell_min', 0)}-{card.get('sell_max', 0)}")
            else:
                if card_id not in self.cards_database:
                    lines.append(f"Pack {pack_number}: ❌ Unknown Card ID: {card_id}")
                    return '\n'.join(lines)
                    
                card = self.cards_database[card_id]
                rarity_symbol = {'Common': '⚪', 'Uncommon': '🔵', 'Rare': '🟡', 'Mythic': '🔴'}
                symbol = rarity_symbol.get(card.get('rarity', 'Common'), '⚪')
                lines.append(f"Pack {pack_number}: {symbol} {card.get('name', 'Unknown Card')}")
                lines.append(f"   {card.get('power', 'N/A')}/{card.get('toughness', 'N/A')} | {card.get('description', 'No description')}")
                lines.append(f"   Sell Value: §{card.get('sell_min', 0)}-{card.get('sell_max', 0)}")
            
            lines.append("```")
            ascii_art = card.get('ascii_art', '[No ASCII art available]')
            lines.append(ascii_art)
            lines.append("```")
            lines.append("─" * 50)
            
        except Exception as e:
            lines = [f"Pack {pack_number}: ❌ Error displaying card: {str(e)}"]
            
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
        
        try:
            # Check if Currency cog is available
            currency_cog = self.bot.get_cog('Currency')
            if not currency_cog:
                await ctx.send("❌ Currency system not available! Please contact an admin.", delete_after=10)
                return
            
            user_balance = currency_cog.get_user_currency(user_id)
            
            if float(user_balance) >= self.PACK_COST:
                # Remove currency
                currency_cog.remove_user_currency(user_id, self.PACK_COST)
                
                # Generate pack contents with user's rarity boost
                pack_contents = self.game.get_pack_contents(user_id)
                
                # Show enhancement boost if any
                rarity_boost = self.game.get_user_rarity_boost(user_id)
                boost_msg = ""
                if rarity_boost > 0:
                    boost_msg = f" (📈 +{rarity_boost*100:.0f}% rarity boost!)"
                
                # Create initial embed
                embed = discord.Embed(
                    title=f"🎴 Opening Magic the Shekelling Booster Pack...{boost_msg} 🎴",
                    description="Your pack is being opened...",
                    color=0xFFD700
                )
                
                message = await ctx.send(embed=embed)
                
                # Update message with each card reveal
                revealed_cards = []
                for i, card_id in enumerate(pack_contents, 1):
                    try:
                        # Add card to user collection
                        if isinstance(card_id, str):  # Special card
                            current_count = self.game.user_collections[user_id].get(card_id, 0)
                            self.game.user_collections[user_id][card_id] = current_count + 1
                        else:
                            self.game.user_collections[user_id][card_id] += 1
                        
                        # Create card display
                        card_display = self.game.create_card_display(card_id, i)
                        revealed_cards.append(card_display)
                        
                        # Check if description is getting too long for Discord
                        description_text = '\n'.join(revealed_cards)
                        if len(description_text) > 4000:  # Discord embed description limit
                            # Truncate and add summary
                            truncated = '\n'.join(revealed_cards[:-1])
                            truncated += f"\n\n... Card {i}/{len(pack_contents)} (truncated due to length)"
                            embed.description = truncated
                        else:
                            embed.description = description_text
                        
                        # Update balance in footer
                        new_balance = currency_cog.get_user_currency(user_id)
                        embed.set_footer(text=f"Balance: §{new_balance:.2f}")
                        
                        await message.edit(embed=embed)
                        await asyncio.sleep(1)  # Wait 1 second between reveals
                        
                    except Exception as e:
                        print(f"Error processing card {card_id}: {str(e)}")
                        # Continue with next card instead of breaking
                        continue
                
                # Final message
                embed.title = f"🎴 Magic the Shekelling Booster Pack Opened!{boost_msg} 🎴"
                embed.color = 0x00FF00
                await message.edit(embed=embed, delete_after=120)
                
                # Auto-save after pack opening
                await self.save_data()
                
            else:
                await ctx.send(f"You need §{self.PACK_COST} to buy a booster pack. You have §{user_balance:.2f}", 
                             delete_after=10)
        
        except Exception as e:
            await ctx.send(f"❌ Error opening pack: {str(e)}", delete_after=10)
            print(f"Error in buy_pack command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass  # Ignore deletion errors
    
    @commands.command(aliases=["buy10packs", "10packs", "multipacks"])
    async def buy_10_packs(self, ctx):
        """!buy10packs - Buy 10 Magic the Shekelling booster packs for 2000 shekels"""
        user_id = str(ctx.author.id)
        total_cost = self.PACK_COST * 10
        
        try:
            # Check if Currency cog is available
            currency_cog = self.bot.get_cog('Currency')
            if not currency_cog:
                await ctx.send("❌ Currency system not available! Please contact an admin.", delete_after=10)
                return
                
            user_balance = currency_cog.get_user_currency(user_id)
            
            if float(user_balance) >= total_cost:
                # Remove currency
                currency_cog.remove_user_currency(user_id, total_cost)
                
                # Show enhancement boost if any
                rarity_boost = self.game.get_user_rarity_boost(user_id)
                boost_msg = ""
                if rarity_boost > 0:
                    boost_msg = f" (📈 +{rarity_boost*100:.0f}% rarity boost!)"
                
                # Create initial embed
                embed = discord.Embed(
                    title=f"🎴 Opening 10 Magic the Shekelling Booster Packs...{boost_msg} 🎴",
                    description="Your packs are being opened...",
                    color=0xFFD700
                )
                
                message = await ctx.send(embed=embed)
                
                # Track notable cards and all cards
                notable_cards = []
                all_cards_count = {'Common': 0, 'Uncommon': 0, 'Rare': 0, 'Mythic': 0, 'Special': 0}
                
                # Open 10 packs
                for pack_num in range(1, 11):
                    try:
                        pack_contents = self.game.get_pack_contents(user_id)
                        
                        # Process each card in the pack
                        for card_id in pack_contents:
                            try:
                                # Add card to user collection
                                if isinstance(card_id, str):  # Special card
                                    current_count = self.game.user_collections[user_id].get(card_id, 0)
                                    self.game.user_collections[user_id][card_id] = current_count + 1
                                    all_cards_count['Special'] += 1
                                    # Always show special cards
                                    notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                                else:
                                    self.game.user_collections[user_id][card_id] += 1
                                    if card_id in self.game.cards_database:
                                        card = self.game.cards_database[card_id]
                                        rarity = card.get('rarity', 'Common')
                                        all_cards_count[rarity] += 1
                                        
                                        # Only show rare and mythic cards
                                        if rarity in ['Rare', 'Mythic']:
                                            notable_cards.append(self.game.create_notable_card_display(card_id, pack_num))
                                    else:
                                        all_cards_count['Common'] += 1  # Default to common if unknown
                            except Exception as e:
                                print(f"Error processing card {card_id} in pack {pack_num}: {str(e)}")
                                continue
                        
                        # Update embed after each pack
                        embed.description = f"Opened {pack_num}/10 packs..."
                        await message.edit(embed=embed)
                        await asyncio.sleep(0.5)  # Wait 0.5 seconds between packs
                        
                    except Exception as e:
                        print(f"Error opening pack {pack_num}: {str(e)}")
                        continue
                
                # Final message with results
                embed.title = f"🎴 10 Magic the Shekelling Booster Packs Opened!{boost_msg} 🎴"
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
                new_balance = currency_cog.get_user_currency(user_id)
                embed.set_footer(text=f"Balance: §{new_balance:.2f}")
                
                await message.edit(embed=embed, delete_after=180)  # Show for 3 minutes
                
                # Auto-save after 10-pack opening
                await self.save_data()
                
            else:
                await ctx.send(f"You need §{total_cost} to buy 10 booster packs. You have §{user_balance:.2f}", 
                             delete_after=10)
        
        except Exception as e:
            await ctx.send(f"❌ Error opening 10 packs: {str(e)}", delete_after=10)
            print(f"Error in buy_10_packs command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass

    @commands.command(aliases=["buyenhancement", "buy_enhancement", "cardenhancement"])
    async def buy_card_enhancement(self, ctx, enhancement_name: str = ""):
        """!buyenhancement [card_nerd/card_store/card_printer] - Buy card enhancement items using materials from mining"""
        user_id = str(ctx.author.id)
        
        try:
            if not enhancement_name:
                msg = "**🎴 Card Enhancement Shop 🎴**\n\n"
                msg += "**Available Enhancements:**\n"
                for item_id, item_data in self.game.enhancement_items.items():
                    materials_text = ", ".join([f"{count} {mat_name.replace('_', ' ').title()}" 
                                              for mat_name, count in item_data['materials'].items()])
                    msg += f"🔹 **{item_data['name']}** - §{item_data['cost']:,} + {materials_text}\n"
                    msg += f"   📈 +{item_data['rarity_boost']*100:.0f}% rarity boost for all packs\n"
                    msg += f"   {item_data['description']}\n\n"
                
                msg += "**Usage:** `!buyenhancement card_nerd` or `!buyenhancement card_store` or `!buyenhancement card_printer`\n"
                msg += "**Note:** Materials come from your mining game progress!"
                
                await ctx.send(msg, delete_after=60)
                await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
                return
            
            enhancement_name = enhancement_name.lower()
            if enhancement_name not in self.game.enhancement_items:
                await ctx.send("Invalid enhancement! Use: card_nerd, card_store, or card_printer", delete_after=10)
                return
            
            item_data = self.game.enhancement_items[enhancement_name]
            
            # Check if user already has this enhancement
            if self.game.user_enhancements[user_id][enhancement_name] > 0:
                await ctx.send(f"You already own {item_data['name']}! Each enhancement can only be purchased once.", delete_after=15)
                return
            
            # Check currency balance
            currency_cog = self.bot.get_cog('Currency')
            if not currency_cog:
                await ctx.send("❌ Currency system not available! Please contact an admin.", delete_after=10)
                return
                
            user_balance = currency_cog.get_user_currency(user_id)
            if user_balance < item_data['cost']:
                await ctx.send(f"You need §{item_data['cost']:,} to buy {item_data['name']}. You have §{user_balance:.2f}", delete_after=15)
                return
            
            # Check materials from mining game
            mining_game = self.bot.get_cog('MinerGame')
            if not mining_game:
                await ctx.send("Mining game not available! Materials come from the mining game.", delete_after=15)
                return
            
            mining_game.initialize_member_data(user_id)
            user_materials = mining_game.member_materials[user_id]
            
            # Check if user has required materials
            missing_materials = []
            for material, needed_count in item_data['materials'].items():
                if user_materials.get(material, 0) < needed_count:
                    missing_materials.append(f"{needed_count} {material.replace('_', ' ').title()}")
            
            if missing_materials:
                await ctx.send(f"You need: {', '.join(missing_materials)} to buy {item_data['name']}!", delete_after=15)
                return
            
            # Purchase the enhancement
            # Remove currency
            currency_cog.remove_user_currency(user_id, item_data['cost'])
            
            # Remove materials
            for material, needed_count in item_data['materials'].items():
                user_materials[material] -= needed_count
            
            # Add enhancement to user
            self.game.user_enhancements[user_id][enhancement_name] = 1
            
            # Save mining game data (for materials)
            await mining_game.save_data()
            
            # Save our data too
            await self.save_data()
            
            new_balance = currency_cog.get_user_currency(user_id)
            total_boost = self.game.get_user_rarity_boost(user_id)
            
            embed = discord.Embed(
                title="🎴 Enhancement Purchased! 🎴",
                description=f"```\n{item_data['ascii_art']}\n```",
                color=0x00FF00
            )
            
            embed.add_field(name="📦 Item", value=item_data['name'], inline=True)
            embed.add_field(name="📈 Boost", value=f"+{item_data['rarity_boost']*100:.0f}%", inline=True)
            embed.add_field(name="💰 New Balance", value=f"§{new_balance:.2f}", inline=True)
            embed.add_field(name="🔥 Total Rarity Boost", value=f"+{total_boost*100:.0f}%", inline=False)
            embed.add_field(name="📝 Description", value=item_data['description'], inline=False)
            
            await ctx.send(embed=embed, delete_after=60)
            
        except Exception as e:
            await ctx.send(f"❌ Error purchasing enhancement: {str(e)}", delete_after=10)
            print(f"Error in buy_card_enhancement command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass

    @commands.command(aliases=["enhancements", "myenhancements", "cardenhancements"])
    async def view_enhancements(self, ctx, member: discord.Member = None):
        """!enhancements - View your card enhancement items and rarity boost"""
        member = member or ctx.author
        user_id = str(member.id)
        
        try:
            user_enhancements = self.game.user_enhancements[user_id]
            total_boost = self.game.get_user_rarity_boost(user_id)
            
            embed = discord.Embed(
                title=f"🎴 {member.display_name}'s Card Enhancements 🎴",
                color=0x9932CC
            )
            
            if any(count > 0 for count in user_enhancements.values()):
                owned_items = []
                for item_id, count in user_enhancements.items():
                    if count > 0:
                        item_data = self.game.enhancement_items[item_id]
                        owned_items.append(f"✅ **{item_data['name']}** (+{item_data['rarity_boost']*100:.0f}% boost)")
                        owned_items.append(f"   {item_data['description']}")
                
                embed.add_field(name="🔧 Owned Enhancements", value="\n".join(owned_items), inline=False)
            else:
                embed.add_field(name="🔧 Owned Enhancements", value="None - Use !buyenhancement to get started!", inline=False)
            
            embed.add_field(name="📈 Total Rarity Boost", value=f"+{total_boost*100:.0f}%", inline=True)
            embed.add_field(name="🎯 Effect", value="Increases rare+ card chances in all packs!", inline=True)
            
            # Show available enhancements
            available_items = []
            for item_id, item_data in self.game.enhancement_items.items():
                if user_enhancements[item_id] == 0:
                    materials_text = ", ".join([f"{count} {mat_name.replace('_', ' ').title()}" 
                                              for mat_name, count in item_data['materials'].items()])
                    available_items.append(f"🔹 **{item_data['name']}** - §{item_data['cost']:,} + {materials_text}")
            
            if available_items:
                embed.add_field(name="🛒 Available to Buy", value="\n".join(available_items), inline=False)
            
            await ctx.send(embed=embed, delete_after=60)
            
        except Exception as e:
            await ctx.send(f"❌ Error viewing enhancements: {str(e)}", delete_after=10)
            print(f"Error in view_enhancements command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass
    
    @commands.command(aliases=["collection", "cards", "mycards"])
    async def view_collection(self, ctx, page: int = 1):
        """!collection [page] - View your card collection"""
        user_id = str(ctx.author.id)
        
        try:
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
                    try:
                        if isinstance(card_id, str):  # Special card
                            if card_id in self.game.special_cards:
                                card = self.game.special_cards[card_id]
                                card_info = f"{card['name']} x{count} (§{card.get('sell_min', 0)}-{card.get('sell_max', 0)})"
                                special_cards.append(card_info)
                        else:
                            if card_id in self.game.cards_database:
                                card = self.game.cards_database[card_id]
                                card_info = f"{card['name']} x{count} (§{card.get('sell_min', 0)}-{card.get('sell_max', 0)})"
                                
                                rarity = card.get('rarity', 'Common')
                                if rarity == 'Common':
                                    common_cards.append(card_info)
                                elif rarity == 'Uncommon':
                                    uncommon_cards.append(card_info)
                                elif rarity == 'Rare':
                                    rare_cards.append(card_info)
                                else:  # Mythic
                                    mythic_cards.append(card_info)
                    except Exception as e:
                        print(f"Error processing card {card_id} in collection: {str(e)}")
                        continue
            
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
            
            # Show enhancement boost
            rarity_boost = self.game.get_user_rarity_boost(ctx.author.id)
            if rarity_boost > 0:
                embed.add_field(name="📈 Rarity Boost", value=f"+{rarity_boost*100:.0f}%", inline=True)
            
            # Calculate total pages
            all_cards = special_cards + mythic_cards + rare_cards + uncommon_cards + common_cards
            total_pages = max(1, (len(all_cards) + items_per_page - 1) // items_per_page)
            if total_pages > 1:
                embed.set_footer(text=f"Page {page}/{total_pages} - Use !collection [page] to see more")
            
            await ctx.send(embed=embed, delete_after=60)
            
        except Exception as e:
            await ctx.send(f"❌ Error viewing collection: {str(e)}", delete_after=10)
            print(f"Error in view_collection command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass
    
    @commands.command(aliases=["m_sellcard"], name="m_sell")
    async def m_sell_card(self, ctx, *, card_name=None):
        """!m_sell [card name] - Sell a card from your collection"""
        if not card_name:
            await ctx.send("Please specify a card name to sell! Example: !m_sell Shekel Goblin", 
                         delete_after=10)
            return
        
        user_id = str(ctx.author.id)
        
        try:
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
                        if card_id in self.game.cards_database:
                            card = self.game.cards_database[card_id]
                            if card['name'].lower() == card_name.lower():
                                card_found = card
                                card_id_found = card_id
                                break
            
            if not card_found:
                await ctx.send(f"You don't have any '{card_name}' cards to sell!", delete_after=10)
                return
            
            # Calculate sell value
            sell_value = random.randint(card_found.get('sell_min', 1), card_found.get('sell_max', 10))
            
            # Remove card from collection and add shekels
            self.game.user_collections[user_id][card_id_found] -= 1
            
            # Remove the card completely if count reaches 0
            if self.game.user_collections[user_id][card_id_found] <= 0:
                del self.game.user_collections[user_id][card_id_found]
            
            currency_cog = self.bot.get_cog('Currency')
            if currency_cog:
                currency_cog.add_user_currency(user_id, sell_value)
                new_balance = currency_cog.get_user_currency(user_id)
            else:
                new_balance = 0
                await ctx.send("⚠️ Currency system not available, but card was removed.", delete_after=10)
            
            # Save data after selling
            await self.save_data()
            
            embed = discord.Embed(
                title="💰 Card Sold!",
                description=f"Sold **{card_found['name']}** for §{sell_value}",
                color=0x00FF00
            )
            embed.add_field(name="💰 New Balance", value=f"§{new_balance:.2f}", inline=True)
            
            await ctx.send(embed=embed, delete_after=30)
            
        except Exception as e:
            await ctx.send(f"❌ Error selling card: {str(e)}", delete_after=10)
            print(f"Error in m_sell_card command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass
    
    @commands.command(aliases=["selldupes", "sellduplicates", "m_selldupes"])
    async def sell_duplicates(self, ctx):
        """!sellduplicates - Sell all duplicate cards from your collection"""
        user_id = str(ctx.author.id)
        
        try:
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
                    try:
                        # Sell all but one
                        sell_count = count - 1
                        
                        if isinstance(card_id, str):  # Special card
                            if card_id in self.game.special_cards:
                                card = self.game.special_cards[card_id]
                            else:
                                continue  # Skip unknown special cards
                        else:
                            if card_id in self.game.cards_database:
                                card = self.game.cards_database[card_id]
                            else:
                                continue  # Skip unknown cards
                        
                        # Calculate total sell value for all duplicates
                        card_total = 0
                        for _ in range(sell_count):
                            card_total += random.randint(card.get('sell_min', 1), card.get('sell_max', 10))
                        
                        total_sold += sell_count
                        total_value += card_total
                        cards_sold.append(f"{card['name']} x{sell_count} for §{card_total}")
                        
                        # Update collection
                        self.game.user_collections[user_id][card_id] = 1
                        
                    except Exception as e:
                        print(f"Error processing duplicate card {card_id}: {str(e)}")
                        continue
            
            if total_sold == 0:
                await ctx.send("You don't have any duplicate cards to sell!", delete_after=10)
                return
            
            # Add currency
            currency_cog = self.bot.get_cog('Currency')
            if currency_cog:
                currency_cog.add_user_currency(user_id, total_value)
                new_balance = currency_cog.get_user_currency(user_id)
            else:
                new_balance = 0
                await ctx.send("⚠️ Currency system not available, but duplicates were removed.", delete_after=10)
            
            # Save data after selling duplicates
            await self.save_data()
            
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
            
        except Exception as e:
            await ctx.send(f"❌ Error selling duplicates: {str(e)}", delete_after=10)
            print(f"Error in sell_duplicates command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass
    
    @commands.command(aliases=["cardinfo", "card"])
    async def view_card(self, ctx, *, card_name=None):
        """!cardinfo [card name] - View detailed information about a card"""
        if not card_name:
            await ctx.send("Please specify a card name! Example: !cardinfo Shekel Goblin", 
                         delete_after=10)
            return
        
        try:
            # Find the card in database
            card_found = None
            
            # Check special cards first
            for special_id, special_card in self.game.special_cards.items():
                if special_card['name'].lower() == card_name.lower():
                    card_found = special_card
                    break
            
            # Check regular cards if not found in special
            if not card_found:
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
                'Mythic': 0xFF4500,
                'Special': 0xFF69B4
            }
            
            rarity = card_found.get('rarity', 'Special')
            
            embed = discord.Embed(
                title=f"🎴 {card_found['name']}",
                description=f"```\n{card_found.get('ascii_art', '[No ASCII art available]')}\n```",
                color=rarity_colors.get(rarity, 0x9932CC)
            )
            
            embed.add_field(name="⚔️ Power", value=card_found.get('power', 'N/A'), inline=True)
            embed.add_field(name="🛡️ Toughness", value=card_found.get('toughness', 'N/A'), inline=True)
            embed.add_field(name="💎 Rarity", value=rarity, inline=True)
            embed.add_field(name="📜 Description", value=card_found.get('description', 'No description available'), inline=False)
            embed.add_field(name="💰 Sell Value", 
                           value=f"§{card_found.get('sell_min', 0)}-{card_found.get('sell_max', 0)}", inline=True)
            
            await ctx.send(embed=embed, delete_after=60)
            
        except Exception as e:
            await ctx.send(f"❌ Error viewing card info: {str(e)}", delete_after=10)
            print(f"Error in view_card command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass

    @commands.command(aliases=["cardhelp", "helpcard", "cardcommands"])
    async def card_help(self, ctx):
        """!cardhelp - Show all Magic the Shekelling commands and enhancement info"""
        try:
            embed = discord.Embed(
                title="🎴 Magic the Shekelling - Command Guide 🎴",
                color=0x9932CC
            )
            
            # Basic commands
            basic_commands = [
                "🎁 `!buypack` - Buy a booster pack (§200)",
                "📦 `!buy10packs` - Buy 10 packs (§2000)",
                "👁️ `!collection [page]` - View your cards",
                "💰 `!m_sell [card name]` - Sell a specific card",
                "🔄 `!sellduplicates` - Sell all duplicate cards",
                "📖 `!cardinfo [card name]` - View card details"
            ]
            embed.add_field(name="📋 Basic Commands", value="\n".join(basic_commands), inline=False)
            
            # Enhancement commands
            enhancement_commands = [
                "🔧 `!buyenhancement` - View enhancement shop",
                "🛒 `!buyenhancement card_nerd` - Buy Card Nerd (§10k + 5 Rare Earth)",
                "🏪 `!buyenhancement card_store` - Buy Card Store (§15k + 2 Quantum Core)",
                "🖨️ `!buyenhancement card_printer` - Buy Card Printer (§20k + 1 Exotic Matter)",
                "📈 `!enhancements` - View your enhancement items"
            ]
            embed.add_field(name="🔧 Enhancement Commands", value="\n".join(enhancement_commands), inline=False)
            
            # Enhancement benefits
            enhancement_info = [
                "🤓 **Card Nerd** (+10% rarity boost) - Fellow enthusiast helps with pack luck",
                "🏪 **Card Store** (+20% rarity boost) - Premium pack connections",
                "🖨️ **Card Printer** (+40% rarity boost) - Mysterious card printing device",
                "",
                "💡 **How it works:** Enhancements increase your chances of getting rare, mythic, and special cards!",
                "🔗 **Materials come from the Mining Game** - Use `!materials` to check your mining materials"
            ]
            embed.add_field(name="📈 Enhancement System", value="\n".join(enhancement_info), inline=False)
            
            # Rarity information
            rarity_info = [
                "⚪ **Common** (70% base chance) - Basic cards",
                "🔵 **Uncommon** (20% base chance) - Better cards", 
                "🟡 **Rare** (9% base chance) - Valuable cards",
                "🔴 **Mythic** (~1% base chance) - Very rare cards",
                "🌟 **Special Cards** (Ultra rare) - Extremely valuable and rare!"
            ]
            embed.add_field(name="💎 Card Rarities", value="\n".join(rarity_info), inline=False)
            
            embed.set_footer(text="💡 Tip: Stack enhancements for maximum rarity boost! Max boost is 200%.")
            
            await ctx.send(embed=embed, delete_after=120)
            
        except Exception as e:
            await ctx.send(f"❌ Error showing help: {str(e)}", delete_after=10)
            print(f"Error in card_help command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass

    # Backup and restore commands for deployment safety
    @commands.command(aliases=["backupcards"])
    @commands.has_permissions(administrator=True)
    async def backup_card_data(self, ctx):
        """!backupcards - Admin command to create a backup of all card data"""
        try:
            import os
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create backup directory if it doesn't exist
            backup_dir = "/app/data/backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup collections
            collections_backup = f"{backup_dir}/magic_collections_backup_{timestamp}.json"
            with open(collections_backup, 'w') as f:
                json.dump(dict(self.game.user_collections), f, indent=2)
            
            # Backup enhancements
            enhancements_backup = f"{backup_dir}/magic_enhancements_backup_{timestamp}.json"
            with open(enhancements_backup, 'w') as f:
                json.dump(dict(self.game.user_enhancements), f, indent=2)
            
            embed = discord.Embed(
                title="✅ Backup Created Successfully!",
                description=f"Card data backed up with timestamp: {timestamp}",
                color=0x00FF00
            )
            embed.add_field(name="Collections", value=f"✅ {len(self.game.user_collections)} users", inline=True)
            embed.add_field(name="Enhancements", value=f"✅ {len(self.game.user_enhancements)} users", inline=True)
            
            await ctx.send(embed=embed, delete_after=30)
            
        except Exception as e:
            await ctx.send(f"❌ Error creating backup: {str(e)}", delete_after=10)
            print(f"Error in backup_card_data command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass

    @commands.command(aliases=["restorecards"])
    @commands.has_permissions(administrator=True)
    async def restore_card_data(self, ctx, timestamp: str = ""):
        """!restorecards [timestamp] - Admin command to restore card data from backup"""
        if not timestamp:
            await ctx.send("Please provide a timestamp! Example: !restorecards 20241215_143022", delete_after=15)
            return
        
        try:
            import os
            
            backup_dir = "/app/data/backups"
            
            # Check if backup files exist
            collections_backup = f"{backup_dir}/magic_collections_backup_{timestamp}.json"
            enhancements_backup = f"{backup_dir}/magic_enhancements_backup_{timestamp}.json"
            
            if not os.path.exists(collections_backup):
                await ctx.send(f"❌ Collections backup not found for timestamp: {timestamp}", delete_after=15)
                return
            
            if not os.path.exists(enhancements_backup):
                await ctx.send(f"❌ Enhancements backup not found for timestamp: {timestamp}", delete_after=15)
                return
            
            # Load backup data
            with open(collections_backup, 'r') as f:
                collections_data = json.load(f)
            
            with open(enhancements_backup, 'r') as f:
                enhancements_data = json.load(f)
            
            # Restore data
            self.game.user_collections = defaultdict(lambda: defaultdict(int), collections_data)
            self.game.user_enhancements = defaultdict(lambda: defaultdict(int), enhancements_data)
            
            # Save restored data
            await self.save_data()
            
            embed = discord.Embed(
                title="✅ Data Restored Successfully!",
                description=f"Card data restored from backup: {timestamp}",
                color=0x00FF00
            )
            embed.add_field(name="Collections", value=f"✅ {len(self.game.user_collections)} users", inline=True)
            embed.add_field(name="Enhancements", value=f"✅ {len(self.game.user_enhancements)} users", inline=True)
            
            await ctx.send(embed=embed, delete_after=30)
            
        except Exception as e:
            await ctx.send(f"❌ Error restoring data: {str(e)}", delete_after=10)
            print(f"Error in restore_card_data command: {str(e)}")
        
        try:
            await ctx.message.delete(delay=getattr(self.bot, 'SHORT_DELETE_DELAY', 5))
        except:
            pass

    async def load_data(self):
        """Load user collections and enhancements from file"""
        try:
            # Load collections
            with open(f'/app/data/{self.qualified_name}_collections.json', 'r') as f:
                data = json.load(f)
                self.game.user_collections = defaultdict(lambda: defaultdict(int), data)
                print(f"Loaded {len(data)} user collections for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling collections file not found, starting fresh.")
        except Exception as e:
            print(f"Error loading Magic the Shekelling collections: {e}")
        
        try:
            # Load enhancements
            with open(f'/app/data/{self.qualified_name}_enhancements.json', 'r') as f:
                data = json.load(f)
                self.game.user_enhancements = defaultdict(lambda: defaultdict(int), data)
                print(f"Loaded {len(data)} user enhancements for Magic the Shekelling.")
        except FileNotFoundError:
            print("Magic the Shekelling enhancements file not found, starting fresh.")
        except Exception as e:
            print(f"Error loading Magic the Shekelling enhancements: {e}")

    async def save_data(self):
        """Save user collections and enhancements to file"""
        try:
            import os
            
            # Ensure data directory exists
            os.makedirs('/app/data', exist_ok=True)
            
            # Save collections
            with open(f'/app/data/{self.qualified_name}_collections.json', 'w') as f:
                json.dump(dict(self.game.user_collections), f, indent=2)
            
            # Save enhancements
            with open(f'/app/data/{self.qualified_name}_enhancements.json', 'w') as f:
                json.dump(dict(self.game.user_enhancements), f, indent=2)
                
            print("Magic the Shekelling data saved successfully.")
            
        except Exception as e:
            print(f"Error saving Magic the Shekelling data: {e}")

    # Auto-save every 5 minutes to prevent data loss
    @commands.Cog.listener()
    async def on_ready(self):
        """Auto-save data periodically"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
                await self.save_data()
            except Exception as e:
                print(f"Error in auto-save: {e}")


async def setup(bot):
    cog = MagicTheShekelling(bot)
    await cog.load_data()
    await bot.add_cog(cog)
