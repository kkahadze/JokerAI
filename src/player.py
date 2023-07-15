from src.utils import int_to_card, card_to_int, playable, winner, adjust_for_order
from src.card import Card

class Player():
    def __init__(self, number_in):
        self.number = number_in
        self.hand = []
        self.score = 0
        self.desired = -1
        self.taken = 0

    def set_taken(self, taken):
        self.taken = taken

    def add_take(self):
        self.taken += 1

    def set_desired(self, amount):
        self.desired = amount

    def __repr__(self):
        return "Player " + str(self.number)

    def right(self) -> int:
        return (self.number + 1) % 4

    def left(self) -> int:
        return (self.number - 1) % 4

    def across(self) -> int:
        return (self.number + 2) % 4
    
    def update_score(self, dealt: int):
        if self.desired == self.taken: 
            if self.taken == dealt:
                self.score += dealt * 100 # 1 -> 100, 2 -> 200, 3 -> 300, 4 -> 400 ... 
            else:
                self.score += self.taken * 50 + 50 # 1 -> 100, 2 -> 150, 3 -> 200, 4 -> 250 ...
        elif self.taken == 0: # 0 -> -200, bust/ხვიშტი
            self.score -= 200
        else: # 1 -> 10, 2 -> 20, 3 -> 30, 4 -> 40 ...
            self.score += self.taken * 10

    def have_jokers(self):
        for card in self.hand:
            if card.value == 16:
                return True
        return False
    
    def get_joker(self):
        for card in self.hand:
            if card.value == 16:
                return card
        return None
    
    def winnable(self, observation): # must be tested
        first_to_play = observation["first_to_play"]
        first_suit = observation["first_suit"]
        wild_suit = observation["wild_suit"]
        played = [int_to_card(card_int) for card_int in observation["in_play"]]
        observation["player0hand"] = [card_to_int(card) for card in self.hand]
        options = playable(observation)

        if first_to_play == self.number or self.have_jokers():
            return True
        elif (1 in [1 if card and (card.value == 15 or card.value == 16) else 0 for card in played]): # if there is a joker or 2 in play
            return False
        elif True not in [card.suit == first_suit or card.suit == wild_suit for card in options]:
            return False
        else:
            cur_winner = winner(observation)
            for option in options:
                if option.suit == wild_suit and played[cur_winner].suit == wild_suit and option.value > played[cur_winner].value:
                    return True
                elif option.suit == first_suit and played[cur_winner].suit != wild_suit and option.value > played[cur_winner].value:
                    return True
            return False
        
    def winnable_card(self, observation): 
        first_to_play = observation["first_to_play"]
        first_suit = observation["first_suit"]
        wild_suit = observation["wild_suit"]
        played = [int_to_card(card_int) for card_int in observation["in_play"]]
        observation["player0hand"] = [card_to_int(card) for card in self.hand]
        options = playable(observation)

        if first_to_play == self.number:
            return options[0]
        elif self.have_jokers():
            return self.get_joker()
        elif (1 in [1 if card and (card.value == 15 or card.value == 16) else 0 for card in played]): # if there is a joker or 2 in play
            return None
        elif True not in [card and (card.suit == first_suit or card.suit == wild_suit) for card in options]:
            return None
        else:
            cur_winner = winner(observation)
            for option in options:
                if option.suit == wild_suit and ((played[cur_winner].suit == wild_suit and option.value > played[cur_winner].value) or (played[cur_winner].suit != wild_suit)):
                    return option
                elif option.suit == first_suit and played[cur_winner].suit != wild_suit and option.value > played[cur_winner].value:
                    return option
            return None
        
    def losable(self, observation): # must be tested
        first_to_play = observation["first_to_play"]
        first_suit = observation["first_suit"]
        wild_suit = observation["wild_suit"]
        played = [int_to_card(card_int) for card_int in observation["in_play"]]
        observation["player0hand"] = [card_to_int(card) for card in self.hand]
        options = playable(observation)
        cur_winner = winner(observation)

        if first_to_play == self.number or self.have_jokers():
            return True
        elif (1 in [1 if card and (card.value == 15 or card.value == 16) else 0 for card in played]): # if there is a joker or 2 in play
            return True
        elif True in [card.suit == played[cur_winner].suit and card.value < played[cur_winner].value for card in options]:
            return True
        elif True in [card.suit != wild_suit and card.suit != first_suit and (cur_winner and card.value < played[cur_winner].value) for card in options]:
            return True
        else:
            return False

    def losable_card(self, observation): # needs testing
        first_to_play = observation["first_to_play"]
        first_suit = observation["first_suit"]
        wild_suit = observation["wild_suit"]
        played = [int_to_card(card_int) for card_int in observation["in_play"]]
        observation["player0hand"] = [card_to_int(card) for card in self.hand]
        options = adjust_for_order(playable(observation), first_to_play == self.number)
        cur_winner = winner(observation)
        
        if len(options) == 1 or (Card(16, 0) in played and (not self.have_jokers())) or first_to_play == self.number:
            return options[0]
        elif self.have_jokers():
            return self.get_joker()        

        for card in options:
            if card and card.value == 16:
                return card
            if card.suit == played[cur_winner].suit and card.value < played[cur_winner].value:
                return card
            if card.suit != wild_suit and card.suit != first_suit and card.value < played[cur_winner].value:
                return card
            if card.suit != wild_suit and card.suit != first_suit:
                return card
        
        return options[0]
        
    def lowest_valued_card():
        return 1

    def reset(self):
        self.desired = -1
        self.taken = 0
        self.hand = []
