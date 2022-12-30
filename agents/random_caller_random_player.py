from src.player import Player
import random
from agents.utils import get_complement
from src.utils import playable, card_to_int

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

    def play(self, observation):
        if self.number == 0:
            choices = playable(observation)
        else:
            choices = playable(observation, self.hand)
        choice = random.choice(choices)
        self.hand.remove(choice)
        return choice

    def to_obs(self):
        if self.number == 0:
            return {
                "hand": [card_to_int(card) for card in self.hand],
                "desired": self.desired,
                "taken": self.taken,
            }
        else:
            return {
                "desired": self.desired,
                "taken": self.taken,
            }
    
    def opp_playable(self, observation, wild_suit, first_suit):
        if first_suit == 4:
            return self.hand
        else:
            return [card for card in self.hand if card[0] == first_suit or card[0] == wild_suit]