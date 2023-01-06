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
        adjusted_hand = adjust_for_order(self.hand, first_to_play == self.number)

        if self.number == first_to_play or len(self.hand) == 1:
            opp_playable = adjusted_hand
        
        else:
            if first_suit != 4:
                if self.have_suit(first_suit):
                    opp_playable = filter_by_suit_with_joks(self.hand, first_suit)
                else:
                    if not wildsuit_exists(observation):
                        opp_playable = self.hand
                    else:
                        if self.number == 0:
                            have_wild = have_wild_suit(observation)
                        else:
                            have_wild = have_wild_suit(observation, self.number, self.hand)

                        if not have_wild:
                            opp_playable = self.hand
                        else:
                            opp_playable = filter_by_suit_with_joks(self.hand, wild_suit)
            elif not wildsuit_exists(observation):
                opp_playable =  self.hand
            else:
                if not self.have_suit(wild_suit):
                    opp_playable =  self.hand
                else:
                    opp_playable =  filter_by_suit_with_joks(self.hand, wild_suit)
                        
        return opp_playable

    def have_suit(self, suit):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False

def adjust_for_order(hand, first):
    playable_hand = []
    if first:
        for card in hand:
            if card.value == 16:
                for i in range(4):
                    playable_hand.append(15, i)
                    playable_hand.append(5, i)
            else:
                playable_hand.append(card)
    else:
        for card in hand:
            if card.value == 16:
                playable_hand.append(5, 0)
                playable_hand.append(16, 0)
            else:
                playable_hand.append(card)

    return playable_hand