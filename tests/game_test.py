from src.player import Player
from src.game import Game

def test_init():
    game = Game()
    assert game is not None
    assert game.players[0].number == 0 and game.players[1].number == 1 and game.players[2].number == 2 and game.players[3].number == 3
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None

    game = Game([Player(6), Player(7), Player(8), Player(9)])
    assert game is not None
    assert game.players[0].number == 6 and game.players[1].number == 7 and game.players[2].number == 8 and game.players[3].number == 9
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None
    