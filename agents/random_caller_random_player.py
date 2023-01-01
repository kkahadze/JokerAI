from src.player import Player
import random
from agents.utils import get_complement
from src.utils import playable, card_to_int, first_to_play, filter_by_suit_with_joks, wildsuit_exists, get_wildsuit, have_wild_suit

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
            choices = self.opp_playable(observation)
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
    
    def opp_playable(self, observation):
        wild_suit = observation["wild_suit"]
        first_suit = observation["first_suit"]
        first_to_play = observation["first_to_play"]
        
        if self.number == first_to_play or len(self.hand) == 1:
            return self.hand
        
        else:
            if first_suit != 4:
                if self.have_suit(first_suit):
                    return filter_by_suit_with_joks(self.hand, first_suit)
                else:
                    if not wildsuit_exists(observation):
                        return self.hand
                    else:
                        if not have_wild_suit(observation):
                            return self.hand
                        else:
                            return filter_by_suit_with_joks(self.hand, wild_suit)
            elif not wildsuit_exists(observation):
                return self.hand
            else:
                if not self.have_suit(wild_suit):
                    return self.hand
                else:
                    return filter_by_suit_with_joks(self.hand, wild_suit)

    def have_suit(self, suit):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False