"""Retained winner fixtures from the original suite, now with the corrected engine."""

from jokerai.card import Card
from jokerai.game import Game


def test_winner():
    game = Game()
    game.first_suit = 3
    game.wild_suit = 0

    assert game.winner([Card(6, 3), Card(7, 3), Card(6, 2), Card(7, 2)]) == 1
    assert game.winner([Card(6, 3), Card(7, 3), Card(6, 2), Card(9, 1)]) == 1
    assert game.winner([Card(6, 3), Card(7, 3), Card(6, 0), Card(9, 2)]) == 2
    assert game.winner([Card(6, 0), Card(7, 0), Card(16, 1), Card(16, 0)]) == 3
    assert game.winner([Card(12, 3), Card(7, 1), Card(16, 2), Card(9, 1)]) == 2

    assert game.winner([Card(15, 3), Card(16, 1), Card(16, 2), Card(9, 0)]) == 2
    assert game.winner([Card(5, 3), Card(6, 3), Card(12, 2), Card(9, 0)]) == 3
    assert game.winner([Card(15, 3), Card(16, 1), Card(12, 2), Card(9, 0)]) == 1


def test_second_card_wins():
    game = Game()

    for i in range(50):
        game.in_play = [
            Card(6, 1),  # Transformed Joker
            Card(7, 3),
            Card(6, 3),
            Card(7, 2),
        ]
        assert game.winner(game.in_play) == 0

        game.in_play = [
            Card(6, 1),  # Joker
            Card(7, 1),
            Card(6, 3),
            Card(7, 2),
        ]
        assert game.winner(game.in_play) == 1

        game.in_play = [
            Card(6, 0),  # Transformed Joker
            Card(7, 3),
            Card(6, 0),  # Non-Joker 6
            Card(7, 2),
        ]
        assert game.winner(game.in_play) == 0

        game.in_play = [
            Card(6, 0),  # Transformed Joker
            Card(7, 3),
            Card(6, 0),  # Non-Joker 6
            Card(16, 2),
        ]  # Joker
        assert game.winner(game.in_play) == 3

        game.in_play = [
            Card(6, 1),  # Transformed Joker
            Card(7, 1),
            Card(6, 0),
            Card(16, 2),
        ]  # Joker
        assert game.winner(game.in_play) == 3

        game.in_play = [
            Card(15, 2),  # Joker
            Card(7, 1),
            Card(6, 0),
            Card(16, 2),
        ]  # Joker
        assert game.winner(game.in_play) == 3

        game.in_play = [
            Card(15, 2),  # Joker
            Card(7, 1),
            Card(6, 0),
            Card(14, 1),
        ]
        assert game.winner(game.in_play) == 0

        game.in_play = [Card(6, 3), Card(7, 1), Card(6, 0), Card(14, 1)]
        assert game.winner(game.in_play) == 0

        game.in_play = [Card(6, 3), Card(7, 1), Card(6, 0), Card(7, 3)]
        if game.wild_suit == 0:
            assert game.winner(game.in_play) == 0
        elif game.wild_suit == 1:
            assert game.winner(game.in_play) == 1
        else:
            assert game.winner(game.in_play) == 3

        game.in_play = [Card(6, 0), Card(6, 1), Card(6, 0), Card(6, 2)]

        assert game.winner(game.in_play) == 0
