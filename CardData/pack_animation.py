import asyncio
import re
import unittest

from CardData.card_template_data import CARD_DATA_TEMPLATES
from .card_datastore import Card, Stat


class PackAnimation:
    def __init__(self, pack_cards, layout="default"):
        self.pack_cards = pack_cards
        self.num_cards = len(pack_cards)
        self.card_height = 8
        self.card_width = 11
        self.revealed_cards = [False] * self.num_cards
        self.ROW_SPACING = 1
        self.COL_SPACING = 1
        self.GRID_ROWS = 3
        self.GRID_COLS = 4

        self.back_of_card = [
            "┌─────────┐",
            "│         │",
            "│  ╭───╮  │",
            "│    ╭─╯  │",
            "│    ╵    │",
            "│    ●    │",
            "│         │",
            "└─────────┘",
        ]

        layout_tenpack = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2)
        ]
        layout_ninepack = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        if layout == "default":
            self.layout = layout_tenpack[:self.num_cards]
        elif layout == "ninepack":
            self.GRID_COLS = 3
            self.layout = layout_ninepack[:self.num_cards]
        self.layout_map = {pos: i for i, pos in enumerate(self.layout)}

    def _strip_ansi(self, text):
        """Removes ANSI escape codes from a string."""
        return re.sub(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', text)

    def _get_visible_length(self, text):
        """Returns the visible length of a string, excluding ANSI codes."""
        return len(self._strip_ansi(text))

    def _get_card_art(self, card_index):
        if self.revealed_cards[card_index]:
            card = self.pack_cards[card_index]
            art = card.get_display_art()
            return art
        else:
            return self.back_of_card


    def _render_pack_state_to_grid(self):
        grid_rows = (self.card_height + self.ROW_SPACING) * self.GRID_ROWS
        # Increased the buffer for ANSI codes, can be trimmed later
        grid_cols = ((self.card_width + self.COL_SPACING) * self.GRID_COLS - self.COL_SPACING) + 100

        grid = [[' ' for _ in range(grid_cols)] for _ in range(grid_rows)]
        grid_row_ansi_offsets = [0] * grid_rows

        # Process cards in the order they appear on the grid (top-to-bottom, left-to-right)
        sorted_layout_indices = sorted(range(self.num_cards), key=lambda i: self.layout[i])

        for i in sorted_layout_indices:
            card_art = self._get_card_art(i)
            row_idx, col_idx = self.layout[i]
            start_row = row_idx * (self.card_height + self.ROW_SPACING)
            start_col = col_idx * (self.card_width + self.COL_SPACING)

            for r, line in enumerate(card_art):
                grid_r = start_row + r
                
                # The write position starts at the card's column + the accumulated ANSI offset for that row
                write_pos = start_col + grid_row_ansi_offsets[grid_r]
                
                line_ansi_count = 0
                in_ansi = False
                
                for char in line:
                    if char == '\x1b':
                        in_ansi = True
                    
                    if write_pos < grid_cols:
                        grid[grid_r][write_pos] = char
                    
                    write_pos += 1
                    
                    if in_ansi:
                        line_ansi_count += 1
                    
                    if in_ansi and char == 'm':
                        in_ansi = False
                
                # Update the total ANSI offset for this grid row for the next card on this row
                grid_row_ansi_offsets[grid_r] += line_ansi_count

        frame = "\n".join("".join(row).rstrip() for row in grid)

        return frame


    def generate_animation_frames(self):
        frames = []
        frames.append(self._render_pack_state_to_grid())
        for i in range(self.num_cards):
            self.revealed_cards[i] = True
            frames.append(self._render_pack_state_to_grid())
        return frames
