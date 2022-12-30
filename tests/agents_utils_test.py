from agents.random_caller_random_player import RandomCallerRandomPlayer
from src.game import Game
from src.player import Player
from agents.utils import random_call
import random
from src.utils import card_to_int

def test_random_call():
    '''
    This tests the random_call function to assure that it is not providing an invalid call
    '''
    for i in range(1, 10):
        call = random_call({"dealt": i})
        assert call <= i and call >= 0
        
def test_get_complement():
    game = Game([RandomCallerRandomPlayer(i) for i in range(4)])
    game.reset()
    for i in range(9):
        assert sum([player.desired for player in game.players]) != game.get_num_to_deal()
        game.step(card_to_int(game.players[0].play()))