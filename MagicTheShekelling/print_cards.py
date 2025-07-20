# Assuming card_database_remake.py contains the Card, CardDeck, and CardDatabase classes
from card_database_remake import CardDatabase, Card

def print_all_cards():
    """
    Prints details for all card templates by instantiating Card objects
    and using their display method.
    """
    db = CardDatabase()
    # db.generate_card_data() is no longer needed as templates are initialized in __init__

    print("\n--- Card Templates Display ---")
    # Iterate through the card_data_templates which holds the definitions
    for category, cards_in_category in db.card_data_templates.items():
        if not cards_in_category:  # Skip if no cards in category
            continue

        print(f'\nCategory Count: {category} {len(cards_in_category)}')
        print(f"\n{category.upper()} CARDS:")

        for card_name in cards_in_category:
            # Get an instance of the card (stats will be rolled randomly for display)
            # This returns a Card object
            card_instance = db.get_card_instance(category, card_name)

            if card_instance:
                # Use the Card object's display method to print its details, including art
                card_instance.display()
            else:
                print(f"Could not get instance for {card_name} in {category}.")
            
            # Changed to prompt per card for better review flow, as per previous iteration
            input(f"Press Enter to continue to next card in {category.upper()}...") 
        
        # Prompt after all cards in a category are displayed
        input(f"Press Enter to continue to next category ({category.upper()})...")

if __name__ == "__main__":
    print_all_cards()
