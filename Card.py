from Color import Color

class Card(Color):
    """Card class"""
    def __init__(self, card):
        super().__init__()
        self.card = card
        self.rank = card[0] if len(card) == 2 else card[0:2]  # handle 10 rank value
        self.suit = card[-1]
        self.color = self.suit

        @property
        def rank(self):
            self.rank = rank
        def suit(self):
            self.suit = suit
