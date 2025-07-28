from ast import Assert
import unittest
import statistics
import random
import sys
from collections import defaultdict, Counter
from .card_datastore import CardPack
from .card_template_data import CARD_DATA_TEMPLATES
from .pack_animation import PackAnimation
from .card_datastore import CardDatabase, Card, CardDeck, Stat


class TestCardPackStats(unittest.TestCase):
    def calculate_average_card_values(rolls_per_card):
        card_db_for_avg = CardDatabase(CARD_DATA_TEMPLATES)
        averages = {}
        for rarity, cards in card_db_for_avg.card_data.items():
            averages[rarity] = {}
            for card_name in cards.keys():
                total_value = 0.0
                for _ in range(rolls_per_card):
                    card_instance = card_db_for_avg.create_card_instance(rarity, card_name)
                    total_value += float(card_instance.get_value())
                average_value = total_value / rolls_per_card
                averages[rarity][card_name] = average_value
        return averages

    def pack_roller_simulation(num_packs=100000):
        """Opens specified number of packs and tracks all card pulls with rarity statistics"""
        card_db = CardDatabase(CARD_DATA_TEMPLATES)
        card_pack = CardPack(card_db)
        
        # Track all pulled cards
        all_pulled_cards = []
        rarity_counts = Counter()
        card_name_counts = defaultdict(int)
        holo_counts = Counter()
        total_value = 0.0
        
        print(f"\n--- Pack Roller Simulation: Opening {num_packs:,} packs ---")
        print("Processing packs...")
        
        # Progress tracking
        progress_intervals = [num_packs // 10 * i for i in range(1, 11)]
        
        for pack_num in range(num_packs):
            if pack_num + 1 in progress_intervals:
                progress = ((pack_num + 1) / num_packs) * 100
                print(f"Progress: {progress:.0f}% ({pack_num + 1:,}/{num_packs:,} packs)")
            
            pack_cards = card_pack.open()
            
            for card in pack_cards:
                if card:
                    all_pulled_cards.append(card)
                    rarity_counts[card.rarity] += 1
                    card_name_counts[f"{card.name} ({card.rarity})"] += 1
                    total_value += card.get_value()
                    
                    if card.is_holo:
                        holo_counts[card.rarity] += 1
        
        print(f"\nSimulation Complete! Opened {num_packs:,} packs")
        print(f"Total cards pulled: {len(all_pulled_cards):,}")
        print(f"Total value of all cards: ${total_value:,.2f}")
        print(f"Average value per card: ${total_value/len(all_pulled_cards):.2f}")
        print(f"Average value per pack: ${total_value/num_packs:.2f}")
        
        # Rarity Statistics
        print("\n--- Rarity Statistics ---")
        total_cards = sum(rarity_counts.values())
        for rarity in ['common', 'uncommon', 'rare', 'mythic', 'legendary']:
            count = rarity_counts.get(rarity, 0)
            percentage = (count / total_cards) * 100 if total_cards > 0 else 0
            holo_count = holo_counts.get(rarity, 0)
            holo_rate = (holo_count / count) * 100 if count > 0 else 0
            print(f"  {rarity.capitalize()}: {count:,} cards ({percentage:.2f}%) - {holo_count:,} holos ({holo_rate:.2f}% holo rate)")
        
        # Most/Least pulled cards
        print("\n--- Most Pulled Cards (Top 10) ---")
        most_pulled = sorted(card_name_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for card_name, count in most_pulled:
            percentage = (count / total_cards) * 100
            print(f"  {card_name}: {count:,} times ({percentage:.3f}%)")
        
        print("\n--- Least Pulled Cards (Bottom 10) ---")
        least_pulled = sorted(card_name_counts.items(), key=lambda x: x[1])[:10]
        for card_name, count in least_pulled:
            percentage = (count / total_cards) * 100
            print(f"  {card_name}: {count:,} times ({percentage:.3f}%)")
        
        # Holo Statistics
        total_holos = sum(holo_counts.values())
        print(f"\n--- Holo Card Statistics ---")
        print(f"Total holo cards: {total_holos:,} ({(total_holos/total_cards)*100:.3f}% of all cards)")
        
        return {
            'total_packs': num_packs,
            'total_cards': len(all_pulled_cards),
            'total_value': total_value,
            'rarity_counts': dict(rarity_counts),
            'card_name_counts': dict(card_name_counts),
            'holo_counts': dict(holo_counts),
            'all_cards': all_pulled_cards
        }

    rolls_per_card = 100000
    try:
        with open("card_statistics.txt", 'w') as f:
            sys.stdout = f
            print(f"Averages calculated based on {rolls_per_card} rolls per card...")

            averages = calculate_average_card_values(rolls_per_card)
            print("\n--- Overall Average Value per Category ---")
            for category, cards_data in averages.items():
                if cards_data:
                    overall_category_avg = sum(cards_data.values()) / len(cards_data)
                    overall_category_median = statistics.median(cards_data.values())
                    print(f"  {category.capitalize()} Category Average: {overall_category_avg:.2f}")
                    print(f"  {category.capitalize()} Category Median:  {overall_category_median:.2f}")
                else:
                    print(f"  {category.capitalize()} Category: No cards to evaluate.")
            
            # Add the pack roller simulation
            pack_roller_simulation(100000)
            
            print("\n--- 10 Packs of cards ---")
            card_db_example = CardDatabase(CARD_DATA_TEMPLATES)
            card_pack = CardPack(card_db_example)
            
            for iteration in range(10):
                pack_cards = card_pack.open()
                my_deck = CardDeck()
                for card in pack_cards:
                    if card:
                        my_deck.add_card(card)
                
                print(f"\nPack {iteration + 1} contents:")
                for i, card in enumerate(pack_cards, 1):
                    if card:
                        print(f"  Card {i}: {card.name} ({card.rarity}) - Value: {card.get_value()}")
                print(f"Pack {iteration + 1} has {len(my_deck)} cards, Total value: {my_deck.get_total_value()}, Average value: {my_deck.get_average_value():.2f}")

                
            print("\n--- Average Card Values per Card ---")
            for category, cards_data in averages.items():
                print(f"\nCategory: {category.capitalize()}")
                if cards_data:
                    for card_name, avg_value in cards_data.items():
                        print(f"  {card_name}: Average Value = {avg_value:.2f}")
                else:
                    print(f"  No cards found in {category} category.")
    except Exception as e:
        print(f'An error while generating stats {e}')


if __name__ == '__main__':
    unittest.main()