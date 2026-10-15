"""Shared legal-action and winner rules for all four seats.

Physical Jokers have value 16. Actions turn one into a high (16) or low (5)
following Joker, or a suited high (15) / low (5) lead declaration.
"""

from numbers import Integral

from jokerai.card import Card

EMPTY = 44
ACTION_COUNT = 44


def card_to_int(card, first=False):
    if card.value == 6:
        if card.suit not in (0, 2):
            raise ValueError("Only red sixes are physical cards.")
        return card.suit // 2
    if card.value == 16:
        return 34
    if card.value == 5:
        if first and card.suit not in range(4):
            raise ValueError("A leading Joker must declare a suit.")
        return 36 + card.suit if first else 35
    if card.value == 15:
        if card.suit not in range(4):
            raise ValueError("A high Joker lead must declare a suit.")
        return 40 + card.suit
    if 7 <= card.value <= 14 and card.suit in range(4):
        return (card.value - 7) * 4 + card.suit + 2
    raise ValueError("Unknown card.")


def int_to_card(index, restricted_suits=None):
    """Decode without randomness. 44 is padding, never a legal action.

    restricted_suits is retained for old callers; it chooses the first permitted
    suit deterministically. New follower actions use suit 4 (no declared suit).
    """
    if isinstance(index, bool) or not isinstance(index, Integral):
        raise ValueError("Card/action index must be an integer.")
    if index == EMPTY:
        return None
    if not 0 <= index < ACTION_COUNT:
        raise ValueError("Card/action index must be between 0 and 44.")
    if index < 2:
        return Card(6, index * 2)
    if index < 34:
        return Card((index - 2) // 4 + 7, (index - 2) % 4)
    if index in (34, 35):
        permitted = [s for s in range(4) if s not in restricted_suits] if restricted_suits else [4]
        if not permitted:
            raise ValueError("No permitted suit.")
        return Card(16 if index == 34 else 5, permitted[0])
    return Card(5, index - 36) if index < 40 else Card(15, index - 40)


def legal_actions(hand, in_play, wild_suit):
    ordinary = [card for card in hand if not card.is_joker()]
    if in_play:
        lead = in_play[0]
        following = [card for card in ordinary if card.suit == lead.suit]
        if following and lead.value == 15:
            following = [max(following, key=lambda card: card.value)]
        trumps = [card for card in ordinary if card.suit == wild_suit]
        ordinary = following or trumps or ordinary
    actions = [card_to_int(card) for card in ordinary]
    if any(card.is_joker() for card in hand):
        actions.extend(range(36, 44) if not in_play else (34, 35))
    return sorted(set(actions))


def winner_index(cards, wild_suit):
    if not cards:
        raise ValueError("A trick must contain cards.")
    high_jokers = [i for i, card in enumerate(cards) if card.value == 16]
    if high_jokers:
        return high_jokers[-1]
    if cards[0].value == 15:
        return 0
    lead_suit = cards[0].suit

    def weight(card):
        if card.value == 5 and card.suit == 4:
            return -1
        return card.value + (
            200 if card.suit == wild_suit else 100 if card.suit == lead_suit else 0
        )

    return max(range(len(cards)), key=lambda index: weight(cards[index]))


def consume_card(hand, action):
    """Remove exactly one physical card, even when declaring one of two Jokers."""
    played_card = int_to_card(action)
    if played_card is None:
        raise ValueError("Padding cannot be played.")
    if action >= 34:
        index = next((i for i, card in enumerate(hand) if card.is_joker()), None)
    else:
        index = next((i for i, card in enumerate(hand) if card_to_int(card) == action), None)
    if index is None:
        raise ValueError("The requested card is not in this hand.")
    hand.pop(index)
    return played_card
