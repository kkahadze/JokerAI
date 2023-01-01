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
            if not choices:
                print("Player 0: No playable cards")
                print("Player {}: Hand: {}".format(self.number, self.hand))
        else:
            choices = self.opp_playable(observation)
            if not choices:
                print("Player {}: No playable cards".format(self.number))
                print("Player {}: Hand: {}".format(self.number, self.hand))
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
        print("_________________")
        wild_suit = observation["wild_suit"]
        first_suit = observation["first_suit"]
        first_to_play = observation["first_to_play"]
        
        opp_playable = []

        if self.number == first_to_play or len(self.hand) == 1:
            opp_playable = self.hand
        
        else:
            if first_suit != 4:
                if self.have_suit(first_suit):
                    opp_playable = filter_by_suit_with_joks(self.hand, first_suit)
                    print("I Have first suit!")
                else:
                    if not wildsuit_exists(observation):
                        opp_playable = self.hand
                        print("I Don't have first suit!")
                        print("Wild suit doesn't exist!")
                    else:
                        if self.number == 0:
                            have_wild = have_wild_suit(observation)
                        else:
                            have_wild = have_wild_suit(observation, self.number, self.hand)

                        if not have_wild:
                            opp_playable = self.hand
                            print("I Don't have first suit!")
                            print("I Don't have wild suit but it exists!")
                        else:
                            opp_playable = filter_by_suit_with_joks(self.hand, wild_suit)
                            print("I Don't have first suit!")
                            print("I have wild suit!")
            elif not wildsuit_exists(observation):
                opp_playable =  self.hand
                print("Wild suit doesn't exist!")
                print("First suit doesn't exist!")
            else:
                if not self.have_suit(wild_suit):
                    opp_playable =  self.hand
                    print("Wildsuit exists!")
                    print("I don't have wild suit!")
                    print("First suit doesn't exist!")
                else:
                    opp_playable =  filter_by_suit_with_joks(self.hand, wild_suit)
                    print("Wildsuit exists!")
                    print("I have wild suit!")
                    print("First suit doesn't exist!")
        
        if not opp_playable:
            print("Player {}: Hand: {}".format(self.number, self.hand))
            print("Player {}: Wild suit: {}".format(self.number, wild_suit))
            print("Player {}: First suit: {}".format(self.number, first_suit))
            print("Player {}: First to play: {}".format(self.number, first_to_play))
            
        return opp_playable

    def have_suit(self, suit):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False