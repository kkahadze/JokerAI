from src.card import Card
import random

class Deck(list):
    def __init__(self):
        suits = list(range(4))
        values = list(range(7, 15))
        # Ranks 7 through A are added
        super().__init__([Card(i, j) for j in suits for i in values])
        # Ranks Six and Ace are added
        self.extend([Card(15, 0), Card(15, 1), Card(6, 0), Card(6, 2)]) 
        self.shuffle()
    
    def ordered_deck(self):
        suits = list(range(4))
        values = list(range(7, 15))
        return [Card(i, j) for j in suits for i in values]

    def __repr__(self):
        out = ""
        for card in self:
            out += (str(card) + "\n")
        return out

    def shuffle(self):
        random.shuffle(self)

    def get(self, index):
        return self[index]

    def deal(self, location, times=1):
        for _ in range(times):
            location.append(self.burn())

    def burn(self):
        return self.pop(0)