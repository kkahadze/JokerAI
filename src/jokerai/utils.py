"""Small observation helpers. Card encoding and legality live in rules.py."""

from jokerai.rules import EMPTY, card_to_int, int_to_card, legal_actions

__all__ = ["card_to_int", "int_to_card", "playable", "obs_to_string", "cards_in_hand"]


def truncate_at_first_none(cards):
    for i, card in enumerate(cards):
        if card is None:
            return cards[:i]
    return cards


def cards_in_hand(observation):
    return sum(index != EMPTY for index in observation["player0hand"])


def first_to_play(observation):
    return observation["in_play"][0] == EMPTY


def first_suit_index(observation):
    if first_to_play(observation):
        return None
    return int_to_card(int(observation["in_play"][0])).suit


def first_suit_exists(observation):
    return first_suit_index(observation) in range(4)


def wildsuit_exists(observation):
    return observation["wild_suit"] in range(4)


def suit_count(cards):
    counts = [0] * 4
    for index in cards:
        if 0 <= index < 34:
            counts[int_to_card(int(index)).suit] += 1
    return tuple(counts)


def least_common_suit_in_hand(observation):
    counts = suit_count(observation["player0hand"])
    return min(range(4), key=lambda suit: counts[suit])


def most_common_suit_in_hand(observation):
    counts = suit_count(observation["player0hand"])
    return max(range(4), key=lambda suit: counts[suit])


def wildsuit_count(observation):
    return (
        suit_count(observation["player0hand"])[observation["wild_suit"]]
        if wildsuit_exists(observation)
        else 0
    )


def have_wild_suit(observation):
    return wildsuit_count(observation) > 0


def additional_hands_desired(observation):
    return observation["player0desired"] - observation["player0taken"]


def want_to_win(observation):
    return additional_hands_desired(observation) > 0


def playable(observation):
    hand = [int_to_card(int(index)) for index in observation["player0hand"] if index != EMPTY]
    trick = [int_to_card(int(index)) for index in observation["in_play"] if index != EMPTY]
    return [int_to_card(action) for action in legal_actions(hand, trick, observation["wild_suit"])]


def int_to_suit(suit):
    return ("Diamonds", "Clubs", "Hearts", "Spades", "No Wild Suit")[suit]


def obs_to_string(observation):
    hand = [int_to_card(int(i)) for i in observation["player0hand"] if i != EMPTY]
    played = [int_to_card(int(i)) for i in observation["in_play"] if i != EMPTY]
    return (
        f"Cards played: {played}\nTrump: {int_to_suit(observation['wild_suit'])}\n"
        f"Hand: {hand}\nCall: {observation['player0desired']}\nTaken: {observation['player0taken']}\n"
    )
