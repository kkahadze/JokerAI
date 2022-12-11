from src.card import Card
from src.deck import Deck

class Table:
    def __init__(self, deck=Deck()):
        self.deck = deck
        self.players = []
        self.deck.shuffle()
        self.deal()