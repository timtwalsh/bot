import asyncio
from .card_database_remake import Card

class PackAnimation:
    def __init__(self, pack_cards):
        self.pack_cards = pack_cards
        self.num_cards = len(pack_cards)
        self.card_height = 7
        self.card_width = 11
        self.revealed_cards = [False] * self.num_cards
        self.ROW_SPACING = 1  # Number of blank lines between rows
        self.COL_SPACING = 1  # Number of spaces between columns

        self.back_of_card = [
            "┎▬▬▬▬▬▬▬▬▬╻",
            "┃         ┃",
            "┃         ┃",
            "┃    ?    ┃",
            "┃         ┃",
            "┃         ┃",
            "┃         ┃",
            "╹▬▬▬▬▬▬▬▬▬╹",
        ]

    def _get_card_art(self, card_index):
        if self.revealed_cards[card_index]:
            card = self.pack_cards[card_index]
            art = card.get_display_art()
            # Pad each line to the full card width and ensure the art has the correct height
            padded_art = [line.ljust(self.card_width) for line in art]
            while len(padded_art) < self.card_height:
                # Add the middle part of the frame for empty lines
                padded_art.insert(len(art) -1, '┃' + ' ' * (self.card_width - 2) + '┃')
            return padded_art
        else:
            return self.back_of_card

    def _render_pack_state_to_grid(self):
        layout = [
            (0, 0), (0, 1), (0, 2), (0, 3),  # Row 1
            (1, 0), (1, 1), (1, 2), (1, 3),  # Row 2
            (2, 1), (2, 2)                   # Row 3 (centered)
        ]

        grid_rows = (self.card_height + self.ROW_SPACING) * 3
        grid_cols = (self.card_width + self.COL_SPACING) * 4 - self.COL_SPACING
        grid = [[' ' for _ in range(grid_cols)] for _ in range(grid_rows)]

        for i in range(self.num_cards):
            card_art = self._get_card_art(i)
            row_idx, col_idx = layout[i]
            start_row = row_idx * (self.card_height + self.ROW_SPACING)
            start_col = col_idx * (self.card_width + self.COL_SPACING)

            for r, line in enumerate(card_art):
                for c, char in enumerate(line):
                    if start_row + r < grid_rows and start_col + c < grid_cols:
                        grid[start_row + r][start_col + c] = char
        
        return "\n".join("".join(row) for row in grid)

    def generate_animation_frames(self):
        frames = []
        frames.append(self._render_pack_state_to_grid())

        for i in range(self.num_cards):
            self.revealed_cards[i] = True
            frames.append(self._render_pack_state_to_grid())
        
        return frames

async def main():
    from card_database_remake import CardDatabase, CardPack

    card_db = CardDatabase()
    card_pack_roller = CardPack(card_db)
    my_pack = card_pack_roller.open()

    animation = PackAnimation(my_pack)
    frames = animation.generate_animation_frames()

    for frame in frames:
        print("\033[H\033[J", end="")
        print(frame)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())