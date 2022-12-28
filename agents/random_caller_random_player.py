from src.player import Player
import random

class RandomCallerRandomPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        
    def call(self, observation):
        return random.randint(0, 1)

    def play(self, observation):
        return random.randint(0, 1)
