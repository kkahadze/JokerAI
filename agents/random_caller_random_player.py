from src.player import Player
import random

class RandomCallerRandomPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        
    def call(self, observation = None):
        call = random.randint(0, len(self.hand))
        self.desired = call
        return call

    def play(self, observation = None):        
        choice = random.choice(self.hand)
        self.hand.remove(choice)
        return choice
