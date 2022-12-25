from src.utils import least_common_suit_in_hand, wildsuit_count, suit_count, card_to_int, int_to_card, want_to_win, first_to_play, garunteed_win_with_jok
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

def test_int_to_card():
    card = int_to_card(0)
    assert card.value == 6 and card.suit == 0

    card = int_to_card(1)
    assert card.value == 6 and card.suit == 2

    card = int_to_card(2)
    assert card.value == 7 and card.suit == 0

    card = int_to_card(34)
    assert card.value == 14 and card.suit == 0

    card = int_to_card(35)
    assert card.value == 14 and card.suit == 1

    card = int_to_card(19)
    assert card.value == 11 and card.suit == 1

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

def test_want_to_win():
    obs = {
        "players": {
            "0": {
                "hand": map(
                    lambda x: card_to_int(x), 
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
                ),
                "desired": 4,
                "taken": 0
            }
        },
        "wild_suit": 1
    }
    assert want_to_win(obs)

    obs = {
        "players": {
            "0": {
                "hand": map(
                    lambda x: card_to_int(x), 
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
                ),
                "desired": 2,
                "taken": 2,
            }
        },
        "wild_suit": 1
    }
    assert not want_to_win(obs)
    
def test_first_to_play():
    obs = {"in_play": [36, 36, 36]}
    assert first_to_play(obs)

def test_garunteed_win_with_jok():
    obs = {
        "in_play": [13, 3, 36],
        "jokers_remaining": 1
        }
    assert garunteed_win_with_jok(obs)

    obs = {
        "in_play": [13, 3, 36],
        "jokers_remaining": 0
    }
    assert not garunteed_win_with_jok(obs)

    obs = {
        "in_play": [13, 3, 1],
        "jokers_remaining": 1,
    }
    assert garunteed_win_with_jok(obs)
    
    obs = {
        "in_play": [13, 3, 36],
        "jokers_remaining": 2,
    }
    assert not garunteed_win_with_jok(obs)




