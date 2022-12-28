from src.player import Player
from src.game import Game

from agents.random_caller_random_player import RandomCallerRandomPlayer

def test_init():
    game = Game()
    assert game is not None
    assert game.players[0].number == 0 and game.players[1].number == 1 and game.players[2].number == 2 and game.players[3].number == 3
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None

    game = Game([Player(6), Player(7), Player(8), Player(9)])
    assert game is not None
    assert game.players[0].number == 6 and game.players[1].number == 7 and game.players[2].number == 8 and game.players[3].number == 9
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None

def test_reset_vars():
    # The following test makes sure that reset_vars() 
    # resets deck, players, round, play, dealer, wild_suit, jokers_remaining, in_play

    game = Game([Player(6), Player(7), Player(8), Player(9)])
    game.reset_vars()
    assert game is not None
    assert game.players[0].number == 6 and game.players[1].number == 7 and game.players[2].number == 8 and game.players[3].number == 9
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None
    assert game.round == 1
    assert game.play == 1
    assert game.dealer == (game.first_to_play - 1) % 4

def test_get_num_to_deal(): # add more tests
    game = Game(only_nines=True)
    game.reset_vars()
    assert game.get_num_to_deal() == 9

    game = Game() 
    game.reset_vars()
    assert game.get_num_to_deal() == 1

    game = Game()
    game.reset_vars()
    game.round = 2
    assert game.get_num_to_deal() == 9

    game = Game()
    game.reset_vars()
    game.round = 3
    assert game.get_num_to_deal() == 8

    game = Game()
    game.reset_vars()
    game.round = 4
    assert game.get_num_to_deal() == 9

    game = Game()
    game.reset_vars()
    game.round = 1
    game.play = 5
    assert game.get_num_to_deal() == 5

    game = Game()
    game.reset_vars()
    game.round = 1
    game.play = 8
    assert game.get_num_to_deal() == 8

    game = Game()
    game.reset_vars()
    game.round = 3
    game.play = 8
    assert game.get_num_to_deal() == 1

    game = Game()
    game.reset_vars()
    game.round = 3
    game.play = 2
    assert game.get_num_to_deal() == 7

    game = Game(only_nines=True)
    game.reset_vars()
    for round in range(1, 5):
        for play in range(1, 5):
            assert game.get_num_to_deal() == 9

def test_get_calls():
    # This function tests the get_calls() function in game.py to assure that it sets the calls of each player to a valid int corresponding to
    # the type of agent
    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)])
    game.reset_vars()
    game.get_calls()
    for player_num in range(game.first_to_play, game.first_to_play + 4):
        game.deck.deal(game.players[player_num % 4].hand, times = game.get_num_to_deal()) # player num needs to be modded to get the correct players
    calls = game.get_calls()

    assert calls[0] >= 0 and calls[0] <=1
    assert calls[1] >= 0 and calls[1] <=1
    assert calls[2] >= 0 and calls[2] <=1
    assert calls[3] >= 0 and calls[3] <=1