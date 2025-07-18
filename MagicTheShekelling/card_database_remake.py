normal_frame_6x9 = {
    "top": "┏━━━━━━━━━┓",
    "mid": "┃{0}┃",
"bottom":  "┗━━━━━━━━━┛"};

holo_frame_6x9 = {
    "top": "┏━★★★★★━┓",
    "mid": "┃{0}┃",
"bottom":  "┗━★★★★★━┛"};

class CardDatabase:
    def __init__(self):
        self.special_cards = {}

    def generate_cards_database(self):
        """Generate all 151 cards with their stats and ASCII art"""
        cards = {}

        self.cards = {
            "common": {
                "ph": {
                    art: {
                    }
                },

            },
            "uncommon": {
                "ph": {
                    art: {
                        1: "         ", 
                        2: "         ", 
                        3: "         ", 
                        4: "         ", 
                        5: "         ", 
                        6: "         "
                    }
                },

            },
            "rare": {
                "Imperial Imp": {
                    art: {
                        1: " \ ═╬═ /  ", 
                        2: " |  ║  | ", 
                        3: "( ☼╲ ╱☼ )", 
                        4: " \  ▼  / ", 
                        5: "  \___/  ", 
                        6: " /    '\ "
                    },
                }, 
            },
            "mythic": {
                "Immaculate Imp": {
                    art: {
                        1: "  / ║ \  ", 
                        2: " / ═╬═ \ ", 
                        3: "( ☼╲ ╱☼ )", 
                        4: " \ ◄▬► / ", 
                        5: "  \___/  ", 
                        6: " /    '\ "
                    },
                },
                "Impeccable Imp": {
                    art: {
                        1: "  / ║ \  ", 
                        2: " / ═╬═ \ ", 
                        3: "( ☼╲ ╱☼ )", 
                        4: " \ ▼▾▼  / ", 
                        5: "  \___/  ", 
                        6: " /    '\ "
                    },
                },
                "Chris in a Calculator": {
                    art: {
                        1: "   +1    ", 
                        2: " [ CHRIS]", 
                        3: " [][][][]", 
                        4: " [][][][]", 
                        5: " [][][][]", 
                        6: "         "
                    }
                },
                "I buy experiences!": {
                    art: {
                        1: "    I    ", 
                        2: "( ಠ ͜ʖ ರೃ)", 
                        3: "   BUY   ", 
                        4: "( ಠ ͜ʖ ರೃ)", 
                        5: "EXPER    ", 
                        6: "   IENCES"
                    },
                },
                "Daves 'Guild'": {
                    art: {
                        1: "  )  )   ", 
                        2: "\       /", 
                        3: " ∋)╭╮(∈  ", 
                        4: "_∋)╰╯(∈_/", 
                        5: "  /*\   |", 
                        6: " /╰╧╯\  |"
                    },
                },
                "ph": {
                    art: {
                        1: "         ", 
                        2: "         ", 
                        3: "         ", 
                        4: "         ", 
                        5: "         ", 
                        6: "         "
                    },
                },
                "ph": {
                    art: {
                        1: "         ", 
                        2: "         ", 
                        3: "         ", 
                        4: "         ", 
                        5: "         ", 
                        6: "         "
                    },
                },
                "ph": {
                    art: {
                        1: "         ", 
                        2: "         ", 
                        3: "         ", 
                        4: "         ", 
                        5: "         ", 
                        6: "         "
                    },
                },
                "ph": {
                    art: {
                        1: "         ", 
                        2: "         ", 
                        3: "         ", 
                        4: "         ", 
                        5: "         ", 
                        6: "         "
                    },
                },
                "The One True Liberal": {
                    art: {
                        1: "!! ___  /", 
                        2: "  (   )/ ", 
                        3: " /|    |", 
                        4: "/ |  =[++", 
                        5: "  |    | ", 
                        6: " /   ) ) "
                    },
                },
                "Ascended Shitty Wizard": {
                    art: {
                        1: "  /\     ", 
                        2: "_/  \_   ", 
                        3: "(-━ᶗ━) * ", 
                        4: " /**\╭/  ", 
                        5: "/****\   ", 
                        6: " |  |    "
                    },
                },
            },
            "legendary": {
                "Toms Mirror Stash": {
                    art: {
                        1: "    ___  ", 
                        2: "   /o *\ ", 
                        3: "T {* ∞ o}", 
                        4: "O  \* o/ ", 
                        5: "M   ˘˘˘  ", 
                        6: "STASH    "
                    }
                },
                "Tim's D&D Campaigns": {
                    art: {
                        1: "Tims     ", 
                        2: "   _____,", 
                        3: "  / 5e //", 
                        4: " /____// ", 
                        5: "(____(/  ", 
                        6: "   Dreams"
                    }
                },
                "Spirit of the lap": {
                    art: {
                        1: "    __   ",
                        2: " __/  \_ ", 
                        3: "'-0---0-'", 
                        4: "  ╭‼╮aah!", 
                        5: "ꞈ/▐█▌\,  ", 
                        6: " _╱▀╲_   "
                    }
                },
                "Dave's Pinny Money": {
                    art: {
                        1: "║  $$$  ║",
                        2: "║=======║", 
                        3: "║ooo-,,╗║",
                        4: "║    |\║║",
                        5: "║|_  _|║║",
                        6: "╚══╩╩══╩╝",
                    }
                },
                "Machiavellian Mangles": {
                    art: {
                        1: " ,.''.,, ", 
                        2: "( ◣\/◢ ) ", 
                        3: " |  ┺  | ", 
                        4: " \ ▼▼▼ / ", 
                        5: "║ ΔΔΔΔΔ ║", 
                        6: "╚3▒▒▒▒▒Ɛ╝"
                    }
                },
                "League Start with the Boys": {
                    art: {
                        1: "   [POE] ", 
                        2: "  __=== o", 
                        3: " Zz|   | ", 
                        4: "zZ       ",
                        5: "|_o>-<  _",  
                        6: "|--tom--|",
                    }
                }
            }
        }