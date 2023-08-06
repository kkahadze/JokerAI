    # SUIT: DIAMONDS    CLUBS   HEARTS    SPADES
    # VALUES
    # 6:        0         1       2         3
    # 7:        4         5       6         7
    # 8:        8         9       10        11
    # 9:        12        13      14        15
    # 10:       16        17      18        19
    # JACK:     20        21      22        23
    # QUEEN:    24        25      26        27
    # KING:     28        29      30        31
    # ACE:      32        33      34        35

from src.utils import filter_by_suit_with_joks, have_wild_suit, playable, card_to_int, wildsuit_exists, adjust_for_order
from src.player import Player
from agents.utils import get_compliment
import random
from src.card import Card
from src.utils import int_to_card, card_to_int, playable, winner

class RuleBasedBot(Player):
    def __init__(self, number, env = None):
        super().__init__(number)
        self.env = env
    
    def call(self, observation = None):
        compliment = get_compliment(observation)
        wild_suit = observation["wild_suit"]
        call_amount = 0

        for card in self.hand:
            if card.value == 16:
                call_amount += 1 
        
        wilds = 0
        for card in self.hand:
            if card.suit == wild_suit and (card.value > 10 or observation["dealt"] <= 2):
                wilds += 1
        
        call_amount += (wilds)

        if compliment and compliment == call_amount:
            if call_amount == 0:
                call_amount = 1
            else:
                call_amount = call_amount - 1
        
        super().call(call_amount)
        return self.desired

    def play(self, observation):
        observation['player0hand'] = [card_to_int(card) for card in self.hand]
        if self.number == 0:
            choices = playable(observation)
        else:
            choices = self.opp_playable(observation)

        dont_want_more = (self.desired - self.taken) <= 0
        want_more = not dont_want_more

        if dont_want_more:
            if self.have_jokers():
                choice = self.get_joker()
                self.hand.remove(choice)
                return Card(5, 4)
            elif (self.losable(observation)):
                choice = self.losable_card(observation)
                self.hand.remove(choice)
                return choice
        
        if want_more and self.winnable(observation) and self.number != observation["first_to_play"]:
            choice = self.winnable_card(observation)
            self.hand.remove(choice)
            return choice
            
        choice = random.choice(choices)
        self.hand.remove(choice.base())
        return choice


    def to_obs(self):
        if self.number == 0:
            return {
                "hand": [card_to_int(self.hand[i]) if i < len(self.hand) else 44 for i in range(9)],
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
    