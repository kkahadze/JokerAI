from src.player import Player
import random
from agents.utils import get_complement
from src.utils import playable

class RandomCallerRandomPlayer(Player):
    def __init__(self, number):
        super().__init__(number)
        
    def call(self, observation = None):
        complement = get_complement(observation)
        call = random.randint(0, len(self.hand))
        while call == complement:
            call = random.randint(0, len(self.hand))
        self.desired = call
        return call

    def play(self, observation = None):
        choice = random.choice(playable(self.hand))
        self.hand.remove(choice)
        return choice

    def to_obs(self):
        if self.number == 0:
            return {
                "hand": self.hand,
                "desired": self.desired,
                "taken": self.taken,
            }
        else:
            return {
                "desired": self.desired,
                "taken": self.taken,
            }