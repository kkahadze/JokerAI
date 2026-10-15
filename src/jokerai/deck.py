"""The 36 physical cards; Joker declarations are actions, never dealt cards."""

import random

from jokerai.card import Card


class Deck(list):
    def __init__(self, rng=None):
        self.rng = rng if rng is not None else random.Random()
        super().__init__([Card(value, suit) for suit in range(4) for value in range(7, 15)])
        self.extend([Card(16, 0), Card(16, 1), Card(6, 0), Card(6, 2)])
        self.shuffle()

    def shuffle(self):
        self.rng.shuffle(self)

    def deal(self, location, times=1):
        if not isinstance(times, int) or not 0 <= times <= len(self):
            raise ValueError("Cannot deal more cards than the deck contains.")
        location.extend(self[:times])
        del self[:times]

    def burn(self):
        return self.pop(0)

    def get(self, index):
        return self[index]
