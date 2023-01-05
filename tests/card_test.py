from src.card import Card

def test_card_rank():
    assert Card(15, 0).rank() == 9
    assert Card(6, 0).rank() == 0
    assert Card(14, 0).rank() == 8

def test_card_repr():
    assert repr(Card(16, 0)) == "Joker"
    assert repr(Card(6, 0)) == "Six of Diamonds"
    assert repr(Card(14, 0)) == "Ace of Diamonds"

def test_card_same_suit():
    assert Card(15, 0).same_suit(Card(15, 1)) == False
    assert Card(6, 0).same_suit(Card(6, 0)) == True
    assert Card(14, 0).same_suit(Card(14, 0)) == True
    assert Card(14, 0).same_suit(Card(14, 1)) == False