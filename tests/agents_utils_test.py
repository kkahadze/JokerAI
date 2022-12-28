from agents.random_caller_random_player import RandomCallerRandomPlayer
from src.game import Game
from src.player import Player
from agents.utils import random_call

def test_random_call():
    '''
    This tests the random_call function to assure that it is not providing an invalid call
    '''
    for i in range(1, 10):
        call = random_call({"dealt": i})
        assert call <= i and call >= 0
        

