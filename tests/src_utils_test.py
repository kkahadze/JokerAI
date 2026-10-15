import pytest

from jokerai.card import Card
from jokerai.rules import card_to_int, consume_card, int_to_card, legal_actions, winner_index
from jokerai.utils import (
    cards_in_hand,
    first_suit_exists,
    first_suit_index,
    first_to_play,
    have_wild_suit,
    least_common_suit_in_hand,
    most_common_suit_in_hand,
    obs_to_string,
    playable,
    suit_count,
    truncate_at_first_none,
    want_to_win,
    wildsuit_count,
)


@pytest.mark.parametrize("index", range(44))
def test_action_encoding_round_trip_is_deterministic(index):
    card = int_to_card(index)
    assert card == int_to_card(index)
    assert card_to_int(card, first=36 <= index <= 43) == index


@pytest.mark.parametrize("index", [-1, 45, 46, True, 1.5, "2"])
def test_invalid_card_indices(index):
    with pytest.raises(ValueError):
        int_to_card(index)


def test_empty_padding_and_real_hand_size():
    assert int_to_card(44) is None
    assert cards_in_hand({"player0hand": [0, 34] + [44] * 7}) == 2
    assert truncate_at_first_none([1, None, 2]) == [1]
    assert truncate_at_first_none([1, 2]) == [1, 2]


def test_suit_count_ignores_jokers_and_padding():
    assert suit_count([0, 1, 2, 3, 4, 5, 34, 34, 44]) == (2, 1, 2, 1)
    obs = {"player0hand": [0, 2, 34, 44], "wild_suit": 0}
    assert have_wild_suit(obs)
    assert wildsuit_count(obs) == 2
    assert most_common_suit_in_hand(obs) == 0
    assert least_common_suit_in_hand(obs) == 1
    obs["wild_suit"] = 4
    assert wildsuit_count(obs) == 0


def test_diamonds_are_a_real_leading_suit():
    assert first_to_play({"in_play": [44, 44, 44]})
    obs = {"in_play": [0, 44, 44]}
    assert first_suit_exists(obs)
    assert first_suit_index(obs) == 0
    assert not first_suit_exists({"in_play": [44, 44, 44]})


def test_follow_suit_before_trump_and_allow_jokers():
    hand = [Card(7, 0), Card(14, 1), Card(10, 2), Card(16, 0)]
    assert legal_actions(hand, [Card(8, 0)], 1) == [2, 34, 35]
    assert legal_actions(hand[1:], [Card(8, 0)], 1) == [31, 34, 35]
    assert legal_actions(hand[2:], [Card(8, 0)], 1) == [16, 34, 35]
    assert legal_actions(hand, [], 1) == [2, 16, 31] + list(range(36, 44))


def test_high_declaration_requires_highest_of_requested_suit():
    hand = [Card(7, 0), Card(14, 0), Card(14, 1), Card(16, 0)]
    assert legal_actions(hand, [Card(15, 0)], 1) == [30, 34, 35]
    assert legal_actions(hand, [Card(5, 0)], 1) == [2, 30, 34, 35]
    assert winner_index([Card(15, 0), Card(14, 1), Card(14, 0)], 1) == 0
    assert winner_index([Card(15, 0), Card(16, 4), Card(16, 4)], 1) == 2


def test_low_joker_cannot_steal_trick_or_count_as_owned_suit():
    assert winner_index([Card(7, 0), Card(5, 4), Card(14, 1)], 4) == 0
    assert legal_actions([Card(16, 0), Card(14, 1)], [Card(8, 0)], 4) == [31, 34, 35]
    assert winner_index([Card(5, 0), Card(14, 0), Card(7, 1)], 1) == 2


def test_ordinary_card_consumption_and_missing_card():
    hand = [Card(7, 0)]
    assert consume_card(hand, 2) == Card(7, 0)
    assert not hand
    with pytest.raises(ValueError):
        consume_card(hand, 2)


def test_observation_helpers_use_new_contract():
    obs = {
        "in_play": [0, 44, 44],
        "player0hand": [2, 31, 34] + [44] * 6,
        "wild_suit": 1,
        "player0desired": 1,
        "player0taken": 0,
    }
    assert playable(obs) == [Card(7, 0), Card(16, 4), Card(5, 4)]
    assert want_to_win(obs)
    obs["player0taken"] = 2
    assert not want_to_win(obs)
    assert "Seven of Diamonds" in obs_to_string(obs)


@pytest.mark.parametrize("action", [-1, 44, 45, 1.5])
def test_invalid_consumption_never_removes_a_card(action):
    hand = [Card(16, 0), Card(7, 0)]
    before = list(hand)
    with pytest.raises(ValueError):
        consume_card(hand, action)
    assert hand == before
