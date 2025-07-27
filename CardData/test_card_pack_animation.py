from ast import Assert
import unittest

from .card_datastore import CardPack
from .card_template_data import CARD_DATA_TEMPLATES
from .pack_animation import PackAnimation, Card, Stat


class TestCardPackAnimation(unittest.TestCase):
    def test_render_9pack(self):
        # Test rendering multiple cards in a grid
        mock_cards = [Card(
            name=f"Test Card {i}",
            number=i,
            rarity="rare",
            art={
                1: f"<start{i:02}>",
                2: "<artline>",
                3: "<artline>",
                4: "<artline>",
                5: "<artline>",
                6: f"<end  {i:02}>",
            },
            description="A test card.",
            health=Stat(0,0,1),
            attack=Stat(1,0,2),
            armor=Stat(1,0,2),
            barrier=Stat(1,0,2),
            value=Stat(1,0,2),
        ) for i in range(1,10)]
        self.assertEqual(len(mock_cards), 9)
        animation = PackAnimation(mock_cards, layout="ninepack")
        frames = animation.generate_animation_frames()
        print(frames[9])
    def test_render_10pack(self):
        # Test rendering multiple cards in a grid
        mock_cards = [Card(
            name=f"Test Card {i}",
            number=i,
            rarity="rare",
            art={
                1: f"<start{i:02}>",
                2: "<artline>",
                3: "<artline>",
                4: "<artline>",
                5: "<artline>",
                6: f"<end  {i:02}>",
            },
            description="A test card.",
            health=Stat(0,0,1),
            attack=Stat(1,0,2),
            armor=Stat(1,0,2),
            barrier=Stat(1,0,2),
            value=Stat(1,0,2),
        ) for i in range(2,10)]
        mock_cards.insert(0, Card(
                name=f"Test Card {1}",
                number=1,
                rarity="uncommon",
                art={
                    1: f"<start{1:02}>",
                    2: "<artline>",
                    3: "<artline>",
                    4: "<artline>",
                    5: "<artline>",
                    6: f"<end  {1:02}>",
                },
                description="A test card.",
                health=Stat(1,0,1),
                attack=Stat(2,0,2),
                armor=Stat(2,0,2),
                barrier=Stat(2,0,2),
                value=Stat(2,0,2),
            ))
        mock_cards.append(
            Card(
            name=f"Test Card {10}",
            number=10,
            rarity="rare",
            art={
                1: f"<start{10:02}>",
                2: "<artline>",
                3: "<artline>",
                4: "<artline>",
                5: "<artline>",
                6: f"<end  {10:02}>",
            },
            description="A test card.",
            health=Stat(1,1,1),
            attack=Stat(1,1,1),
            armor=Stat(1,1,1),
            barrier=Stat(1,1,1),
            value=Stat(1,1,1),
        ))
        self.assertEqual(len(mock_cards), 10)
        animation = PackAnimation(mock_cards)
        frames = animation.generate_animation_frames()
        print(frames[10])
        with self.subTest(msg="No cards are revealed in frame 0"):
            print(frames[0])
            self.assertNotIn("<start01>", frames[0])

        with self.subTest(msg="no holos in common frames"):
            print(frames[8])
            self.assertNotIn("\x1b[34m┏━━*****━━┓\x1b[0m", frames[8])
            self.assertIn("<start01>", frames[8])

        with self.subTest(msg="no holos in common frame 2"):
            print(frames[9])
            self.assertNotIn("\x1b[34m┏━━*****━━┓\x1b[0m", frames[9])
            self.assertIn("<start09>", frames[9])

        with self.subTest(msg="holo/stars in perfect/holo frame"):
            print(frames[10])
            self.assertIn("\x1b[32m┏━━*****━━┓\x1b[0m", frames[10])
            self.assertIn("<start10>", frames[10])

        with self.subTest(msg="snapshot looks correct"):
            print(frames[10])
            #save frames to file
            with open("frames_snapshot.txt", "w", encoding="utf-8") as f:
                    f.write(frames[10])
            #snapshot test
            self.assertIn("\x1b[32m┏━━*****━━┓\x1b[0m ┌─────────┐ ┌─────────┐ ┌─────────┐\n", frames[10])
            self.assertIn("\x1b[32m┗━━*****━━┛\x1b[0m └─────────┘ └─────────┘ └─────────┘\n", frames[10])
            self.assertIn("\n", frames[10])
            self.assertIn("            ┌─────────┐ \x1b[34m┏━━*****━━┓\x1b[0m\n", frames[10])
            self.assertIn("            │<start09>│ \x1b[34m┃\x1b[0m<start10>\x1b[34m┃\x1b[0m\n", frames[10])
            self.assertIn("            └─────────┘ \x1b[34m┗━━*****━━┛\x1b[0m\n", frames[10])

if __name__ == '__main__':
    unittest.main()
    