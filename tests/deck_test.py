import random

import pytest

from jokerai.card import Card
from jokerai.deck import Deck


def test_deck_has_36_unique_physical_cards_and_two_real_jokers():
    deck = Deck()
    assert len(deck) == len(set(deck)) == 36
    assert sorted((c.value, c.suit) for c in deck if c.is_joker()) == [(16, 0), (16, 1)]
    assert Card(6, 0) in deck and Card(6, 2) in deck
    assert Card(6, 1) not in deck and Card(6, 3) not in deck


def test_shuffle_is_seeded_and_preserves_cards():
    a, b = Deck(random.Random(10)), Deck(random.Random(10))
    assert a == b
    before = set(a)
    a.shuffle()
    assert set(a) == before
    assert a != b


def test_deal_and_overdeal_are_atomic():
    deck, hand = Deck(), []
    deck.deal(hand, 9)
    assert len(deck) == 27 and len(hand) == 9
    assert not set(deck).intersection(hand)
    with pytest.raises(ValueError):
        deck.deal(hand, 28)
    assert len(deck) == 27 and len(hand) == 9
