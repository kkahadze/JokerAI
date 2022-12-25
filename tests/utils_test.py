from src.utils import least_common_suit_in_hand, wildsuit_count, suit_count, card_to_int, int_to_card
from src.card import Card

def test_card_to_int():
    card = Card(6, 0)
    assert card_to_int(card) == 0

    card = Card(6, 2)
    assert card_to_int(card) == 1

    card = Card(7, 0)
    assert card_to_int(card) == 2

    card = Card(14, 0)
    assert card_to_int(card) == 34

    card = Card(14, 1)
    assert card_to_int(card) == 35

    card = Card(11, 1)
    assert card_to_int(card) == 19

def test_suit_count():
    hand = [Card(6, 0), Card(10, 3), Card(11, 1)]
    mapped_hand = map(lambda x : card_to_int(x), hand)
    assert suit_count(mapped_hand) == (1, 1, 0, 1)

    hand = [Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]
    mapped_hand = map(lambda x : card_to_int(x), hand)
    assert suit_count(mapped_hand) == (2, 3, 0, 2)

def test_least_common_suit_in_hand():
    obs = {"players": {"0": {"hand": map(lambda x: card_to_int(x), list([Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}}}
    assert least_common_suit_in_hand(obs) == 2

def test_wilsuit_count():
    obs = {"players": {"0": {"hand": map(
        lambda x: card_to_int(x), 
        list([Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}},
        "wild_suit": 2
        }
    assert wildsuit_count(obs) == 0

    obs = {"players": {"0": {"hand": map(
        lambda x: card_to_int(x), 
        list([Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}},
        "wild_suit": 1
        }
    assert wildsuit_count(obs) == 3



    
