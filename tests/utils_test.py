from src.utils import least_common_suit_in_hand, wildsuit_count, suit_count, card_to_int, int_to_card
from src.card import Card
from src.env import JokerEnv

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
    # hand = [Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 1), Card(14, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]

    assert suit_count(mapped_hand) == (1, 1, 0, 1)

# def test_least_common_suit_in_hand():
#     hand = [Card(6, 0), Card(10, 3), Card(11, 1), Card(14, 3), Card(14, 1), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]
#     mapped_hand = map(lambda x : card_to_int(x), hand)


#     env = JokerEnv()
#     obs = env.observation_space.sample()
#     print(obs)

#     assert least_common_suit_in_hand(obs) == 1

