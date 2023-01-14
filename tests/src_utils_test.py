from src.utils import least_common_suit_in_hand, wildsuit_count, suit_count, card_to_int, int_to_card, want_to_win, first_to_play, garunteed_win_with_jok, most_common_suit_in_hand, choose_suit_for_take, choose_suit_for_highest, playable, truncate_at_first_none, obs_to_string, cards_in_hand, int_to_suit, filter_by_suit_with_joks, first_suit_exists, first_suit_index, playable, contains_suit, highest_of_suit, get_transformed_joker, indexes_of_transformed_jokers
from src.card import Card
from src.env import JokerEnv

# def test_card_to_int():
#     card = Card(6, 0)
#     assert card_to_int(card) == 0

#     card = Card(6, 2)
#     assert card_to_int(card) == 1

#     card = Card(7, 0)
#     assert card_to_int(card) == 2

#     card = Card(15, 0)
#     assert card_to_int(card) == 34

#     card = Card(15, 1)
#     assert card_to_int(card) == 35

#     card = Card(11, 1)
#     assert card_to_int(card) == 19

#     for suit in range(0, 4):
#         for value in range(6, 15):
#             if value == 6 or value == 15:
#                 continue
#             assert card_to_int(Card(value, suit)) == (value - 7) * 4 + (suit) + 2

def test_int_to_card():
    card = int_to_card(0)
    assert card.value == 6 and card.suit == 0

    card = int_to_card(1)
    assert card.value == 6 and card.suit == 2

    card = int_to_card(2)
    assert card.value == 7 and card.suit == 0

    card = int_to_card(34)
    assert card.value == 16 and card.suit == 0

    card = int_to_card(35)
    assert card.value == 5 

    card = int_to_card(19)
    assert card.value == 11 and card.suit == 1

    # for i in range(36):
    #     card = int_to_card(i)
    #     assert card_to_int(card) == i

    card = int_to_card(36)
    assert card.value == 5 and card.suit == 0

    card = int_to_card(37)
    assert card.value == 5 and card.suit == 1

    card = int_to_card(38)
    assert card.value == 5 and card.suit == 2

    card = int_to_card(39)
    assert card.value == 5 and card.suit == 3

    card = int_to_card(40)
    assert card.value == 15 and card.suit == 0

    card = int_to_card(41)
    assert card.value == 15 and card.suit == 1

    card = int_to_card(42)
    assert card.value == 15 and card.suit == 2

    card = int_to_card(43)
    assert card.value == 15 and card.suit == 3

    # Restricted suits for Take/წაიღოს
    card = int_to_card(35, restricted_suits=[0, 1])
    assert card.value == 5 and (card.suit == 2 or card.suit == 3)

    card = int_to_card(35, restricted_suits=[0, 2, 3])
    assert card.value == 5 and card.suit == 1    

def test_suit_count():
    hand = [Card(6, 0), Card(10, 3), Card(11, 1)]
    mapped_hand = map(lambda x : card_to_int(x), hand)
    assert suit_count(mapped_hand) == (1, 1, 0, 1)

    hand = [Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]
    mapped_hand = map(lambda x : card_to_int(x), hand)
    assert suit_count(mapped_hand) == (2, 3, 0, 2)

def test_least_common_suit_in_hand():
    obs = {"players": {"0": {"hand": map(lambda x: card_to_int(x), list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}}}
    assert least_common_suit_in_hand(obs) == 2

def test_most_common_suit_in_hand():
    obs = {"players": {"0": {"hand": map(lambda x: card_to_int(x), list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}}}
    assert most_common_suit_in_hand(obs) == 1
def test_wilsuit_count():
    obs = {"players": {"0": {"hand": map(
        lambda x: card_to_int(x), 
        list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}},
        "wild_suit": 2
        }
    assert wildsuit_count(obs) == 0

    obs = {"players": {"0": {"hand": map(
        lambda x: card_to_int(x), 
        list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]))}},
        "wild_suit": 1
        }
    assert wildsuit_count(obs) == 3

def test_want_to_win():
    obs = {
        "players": {
            "0": {
                "hand": map(
                    lambda x: card_to_int(x), 
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
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
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
                ),
                "desired": 2,
                "taken": 2,
            }
        },
        "wild_suit": 1
    }
    assert not want_to_win(obs)
    
def test_first_to_play():
    obs = {"in_play": [46, 46, 46]}
    assert first_to_play(obs)

def test_garunteed_win_with_jok():
    obs = {
        "in_play": [13, 3, 46],
        "jokers_remaining": 1
        }
    assert garunteed_win_with_jok(obs)

    obs = {
        "in_play": [13, 3, 46],
        "jokers_remaining": 0
    }
    assert not garunteed_win_with_jok(obs)

    obs = {
        "in_play": [13, 3, 1],
        "jokers_remaining": 1,
    }
    assert garunteed_win_with_jok(obs)
    
    obs = {
        "in_play": [13, 3, 46],
        "jokers_remaining": 2,
    }
    assert not garunteed_win_with_jok(obs)

def test_truncate_at_first_none():
    assert truncate_at_first_none([1, 2, 3, None, 4, 5]) == [1, 2, 3]
    assert truncate_at_first_none([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert truncate_at_first_none([1, 2, 3, None, None, 4, 5]) == [1, 2, 3]
    assert truncate_at_first_none([1, 2, 3, None, None, None, 4, 5]) == [1, 2, 3]
    assert truncate_at_first_none([None]) == []

def test_obs_to_string():
    obs = {
        "in_play": [13, 3, 46],
        "jokers_remaining": 1,
        "players": {
            "0": {
                "hand": map(
                    lambda x: card_to_int(x),
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
                ),
                "desired": 4,
                "taken": 0
            },
            "1": {
                "desired": 4,
                "taken": 0
            },
            "2": {
                "desired": 4,
                "taken": 0
            },
            "3": {
                "desired": 4,
                "taken": 0
            }
        },
        "wild_suit": 1
        
    }

    assert obs_to_string(obs) == "Cards Played: [Nine of Spades, Seven of Clubs]\nWildsuit: Clubs\nHand: [Six of Diamonds, Ten of Spades, Jack of Clubs, Joker (Highs) of Clubs, Joker (Highs) of Diamonds, Ten of Clubs, Seven of Clubs, Eight of Spades, Jack of Diamonds]\nDesired: 4\nTaken: 0\nOpponent 1 Desired: 4\nOpponent 1 Taken: 0\nOpponent 2 Desired: 4\nOpponent 2 Taken: 0\nOpponent 3 Desired: 4\nOpponent 3 Taken: 0\nJokers Remaining: 1\n"
    

def test_cards_in_hand():
    obs = {
        "players": {
            "0": {
                "hand": map(
                    lambda x: card_to_int(x),
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
                ),
                "desired": 4,
                "taken": 0
            }
        }
    }
    assert cards_in_hand(obs) == 9

def test_int_to_suit():
    assert int_to_suit(0) == "Diamonds"
    assert int_to_suit(1) == "Clubs"
    assert int_to_suit(2) == "Hearts"
    assert int_to_suit(3) == "Spades"
    assert int_to_suit(4) == "No Wild Suit"

def test_filter_by_suit_with_joks():
    cards = [Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]
    filtered = filter_by_suit_with_joks(cards, 1)
    assert filtered == [Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1)]

def test_first_suit_exists():
    obs = {
        "in_play": [46, 46, 46],
    }
    assert not first_suit_exists(obs)

    obs = {
        "in_play": [1, 46, 46],
    }
    assert first_suit_exists(obs)

    obs = {
        "in_play": [1, 2, 46],
    }
    assert first_suit_exists(obs)

def test_first_suit_index():
    obs = {
        "in_play": [46, 46, 46],
    }
    assert not first_suit_index(obs)

    obs = {
        "in_play": [1, 46, 46],
    }
    assert first_suit_index(obs) == 2

    obs = {
        "in_play": [1, 2, 46],
    }
    assert first_suit_index(obs) == 2

    obs = {
        "in_play": [3, 2, 3],
    }

    assert first_suit_index(obs) == 1

def test_playable():
    obs = {
        "in_play": [46, 46, 46],
        "jokers_remaining": 2,
        "players": {
            "0": {
                "hand": map(
                    lambda x: card_to_int(x),
                    list([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
                ),
                "desired": 4,
                "taken": 0
            }
        },
        "wild_suit": 1
    }

    assert playable(obs) == [Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)]

    obs = {
        "in_play": [1, 46, 46],
        "jokers_remaining": 2,
        "players": {
            "0": {
                "hand": list(map(
                    lambda x: card_to_int(x),
                    list([Card(6, 0), Card(10, 2), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 2), Card(11, 0)])
                )),
                "desired": 4,
                "taken": 0
            }
        },
        "wild_suit": 2
    }

    cur_playable = playable(obs)
    assert cur_playable == [Card(10, 2), Card(15, 1), Card(15, 0), Card(8, 2)]

    for i in range(100):
        env = JokerEnv()
        obs = env.observation_space.sample()
        sample_hand = obs['players']['0']['hand'] # for printing the hand
        if 46 not in sample_hand:
            cur_playable = playable(obs)
            assert cur_playable

def test_contains_suit():
    assert contains_suit(1, [Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])
    assert not contains_suit(2, [Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)])

def test_highest_of_suit():
    assert highest_of_suit([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)], 1).is_joker()
    assert highest_of_suit([Card(6, 0), Card(10, 3), Card(11, 1), Card(15, 1), Card(15, 0), Card(10, 1), Card(7, 1), Card(8, 3), Card(11, 0)], 2) == None
    assert highest_of_suit([Card(6, 0), Card(10, 3), Card(11, 1), Card(7, 1), Card(15, 0), Card(10, 1), Card(7, 2), Card(8, 3), Card(11, 0)], 1) == Card(11, 1)

def test_contains_transformed_joker():
    cards = [
        Card(6, 0),
        Card(10, 3),
        Card(11, 1),
        Card(15, 1),
    ]
    assert get_transformed_joker(cards) == None

    cards = [
        Card(6, 0),
        Card(10, 3),
        Card(11, 1),
        Card(6, 0),
    ]
    assert get_transformed_joker(cards)

