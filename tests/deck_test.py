from src.card import Card
from src.deck import Deck

def test_deck_init():
    deck = Deck()
    assert len(deck) == 36
    assert Card(6, 0) in deck # Six of Diamonds
    assert Card(0, 0) not in deck

def test_deck_shuffle():
    assert Deck().shuffle() != Deck()

