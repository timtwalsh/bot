from card_database_remake import CardDatabase

def print_all_cards():
    db = CardDatabase()
    db.generate_card_data()
    normal_frame = {"top": "┏━━━━━━━━━┓", "mid": "┃{0}┃", "bottom": "┗━━━━━━━━━┛"}
    print("\n--- Cards ---")
    for rarity, cards in db.card_data.items():
        if not cards:  # Skip if no cards in rarity
            continue
        print(f'Category Count: {rarity} {len(cards.items())}')
        print(f"\n{rarity.upper()} CARDS:")
        for card_name, card_data in cards.items():
            print(f"\n{card_name}")
            
            #db.normal_frame['mid']
            # Print card art if available
            if 'art' in card_data:
                art_lines = []
                art_lines.append(normal_frame['top'])
                for line_num in range(1, 7):
                    if line_num in card_data['art']:
                        art_lines.append(normal_frame['mid'].format(card_data['art'][line_num]))
                art_lines.append(normal_frame['bottom'])
                if art_lines:
                    print('\n'.join(art_lines))
            print("-" * 14)  # Separator between cards
        input("Press Enter to continue to next rarity...")
if __name__ == "__main__":
    print_all_cards()