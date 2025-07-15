#!/usr/bin/env python3
import sys
sys.path.append('/Users/nestorxplor/projects/bot')

from MagicTheShekelling.card_database import CardDatabase

# Calculate expected value of a pack
db = CardDatabase()
cards = db.generate_cards_database()

print("Calculating Expected Value of a Magic the Shekelling Pack")
print("=" * 60)

# Pack probabilities based on get_pack_contents logic
def calculate_expected_value():
    total_expected_value = 0
    
    # Each pack has 15 cards: 14 regular + 1 rare slot
    
    # 14 regular cards (each has 1/3 chance to be holo)
    regular_expected = 0
    for i in range(1, 97):  # Cards 1-96 are regular
        card = cards[i]
        holo_card = cards[f"HOLO_{i}"]
        
        # 2/3 chance regular, 1/3 chance holo
        card_expected = (2/3) * ((card['sell_min'] + card['sell_max']) / 2) + (1/3) * ((holo_card['sell_min'] + holo_card['sell_max']) / 2)
        regular_expected += card_expected
    
    # Average expected value per regular card
    regular_expected /= 96
    
    # 14 regular cards in a pack
    total_expected_value += 14 * regular_expected
    
    # 1 rare slot with complex probability structure
    rare_expected = 0
    
    # Ultra rare special cards (probability from rare_roll logic)
    # Ultra Legendary: 1/100000
    ultra_legendary = db.holo_special_cards.get('HOLO_ULTRA_LEGENDARY', db.special_cards['ULTRA_LEGENDARY'])
    rare_expected += (1/100000) * (2/3) * ((db.special_cards['ULTRA_LEGENDARY']['sell_min'] + db.special_cards['ULTRA_LEGENDARY']['sell_max']) / 2)
    rare_expected += (1/100000) * (1/3) * ((ultra_legendary['sell_min'] + ultra_legendary['sell_max']) / 2)
    
    # Tom's Mirror: 1/100000
    toms_mirror = db.holo_special_cards.get('HOLO_TOMS_MIRROR', db.special_cards['TOMS_MIRROR'])
    rare_expected += (1/100000) * (2/3) * ((db.special_cards['TOMS_MIRROR']['sell_min'] + db.special_cards['TOMS_MIRROR']['sell_max']) / 2)
    rare_expected += (1/100000) * (1/3) * ((toms_mirror['sell_min'] + toms_mirror['sell_max']) / 2)
    
    # Other ultra rares
    ultra_rare_probs = {
        'ULTRA_RARE_20K': 49/100000,
        'ULTRA_RARE_10K': 100/100000,
        'ULTRA_RARE_5K': 450/100000,
        'ULTRA_RARE_1K': 900/100000,
        'RARE_500': 1300/100000,
        'RARE_300': 2000/100000,
        'RARE_200': 4700/100000
    }
    
    for card_type, prob in ultra_rare_probs.items():
        regular_card = db.special_cards[card_type]
        holo_card = db.holo_special_cards.get(f'HOLO_{card_type}', regular_card)
        
        rare_expected += prob * (2/3) * ((regular_card['sell_min'] + regular_card['sell_max']) / 2)
        rare_expected += prob * (1/3) * ((holo_card['sell_min'] + holo_card['sell_max']) / 2)
    
    # Regular rare/mythic cards (remaining 90.5%)
    remaining_prob = 90500/100000
    
    # 1/30 chance for mythic (cards 127-151)
    mythic_expected = 0
    for i in range(127, 152):
        card = cards[i]
        holo_card = cards[f"HOLO_{i}"]
        mythic_expected += (2/3) * ((card['sell_min'] + card['sell_max']) / 2) + (1/3) * ((holo_card['sell_min'] + holo_card['sell_max']) / 2)
    mythic_expected /= 25  # Average of 25 mythic cards
    
    # 29/30 chance for rare (cards 97-126)
    rare_card_expected = 0
    for i in range(97, 127):
        card = cards[i]
        holo_card = cards[f"HOLO_{i}"]
        rare_card_expected += (2/3) * ((card['sell_min'] + card['sell_max']) / 2) + (1/3) * ((holo_card['sell_min'] + holo_card['sell_max']) / 2)
    rare_card_expected /= 30  # Average of 30 rare cards
    
    # Add to rare expected value
    rare_expected += remaining_prob * (1/30) * mythic_expected
    rare_expected += remaining_prob * (29/30) * rare_card_expected
    
    total_expected_value += rare_expected
    
    return total_expected_value

expected_value = calculate_expected_value()
current_pack_cost = 200

print(f"Expected value per pack: §{expected_value:.2f}")
print(f"Current pack cost: §{current_pack_cost}")
print(f"Current expected value ratio: {(expected_value/current_pack_cost)*100:.1f}%")
print()

# Calculate new pack cost for 80% expected value
target_ratio = 0.80
new_pack_cost = expected_value / target_ratio

print(f"For 80% expected value ratio:")
print(f"New pack cost should be: §{new_pack_cost:.2f}")
print(f"Rounded to nearest shekel: §{round(new_pack_cost)}")
