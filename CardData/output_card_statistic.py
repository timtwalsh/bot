from ast import Assert
import unittest
import statistics
import random
import sys
from .card_datastore import CardPack
from .card_template_data import CARD_DATA_TEMPLATES
from .pack_animation import PackAnimation
from .card_datastore import CardDatabase, Card, CardDeck, Stat


class TestCardPackAnimation(unittest.TestCase):
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