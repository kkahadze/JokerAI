import random
from src.deck import Deck
from src.player import Player
from agents.random_caller_random_player import RandomCallerRandomPlayer

from src.utils import int_to_card, contains_suit

class Game:
    def __init__(self, players_in: list = [RandomCallerRandomPlayer(i) for i in range(4)], only_nines=False):
        self.player_types = [type(player) for player in players_in]

        if only_nines:
            self.deal_amounts = [
                [9, 9, 9, 9],
                [9, 9, 9, 9],
                [9, 9, 9, 9],
                [9, 9, 9, 9],
            ]
        else:
            self.deal_amounts = [
                [1, 2, 3, 4, 5, 6, 7, 8],
                [9, 9, 9, 9],
                [8, 7, 6, 5, 4, 3, 2, 1],
                [9, 9, 9, 9],
            ]

        self.deck = Deck()
        self.players = players_in # Initializes all players (0-3) with empty hands
        self.round = 0
        self.play = 0
        self.dealer = 0
        self.wild_suit = 4
        # self.wild_value = 0 
        self.jokers_remaining = 2
        self.in_play = []

        # self.gone = [0 for i in range(36)]

    def reset(self):
        self.reset_vars()

        for player_num in range(self.first_to_play, self.first_to_play + 4):
            self.deck.deal(self.players[player_num % 4].hand, times = self.get_num_to_deal()) # player num needs to be modded to get the correct players
        
        calls = self.get_calls()

        player_num = self.first_to_play

        while player_num % 4 != 0: # while is is not "my" turn
            self.ask_to_play(player_num % 4)
            player_num += 1

    def reset_vars(self): # resets deck, players, round, play, dealer, wild_suit, jokers_remaining, in_play and done
        self.deck = Deck()
        self.players = [self.player_types[0](self.players[0].number),
                        self.player_types[1](self.players[1].number),
                        self.player_types[2](self.players[2].number),
                        self.player_types[3](self.players[3].number)]
        self.round = 1
        self.play = 1
        self.first_to_play = random.randint(0, 3)
        self.dealer = (self.first_to_play + 3) % 4
        self.wild_suit = 4
        self.done = False

        # self.wild_value = 0 
        # self.gone = [0 for i in range(36)]

    def step(self, action):
        card = int_to_card(action)
        self.play_card(card)
        
        self.pre_plays()

        if self.is_done():
            return

        self.process_hand_results()
        
        if self.hand_empty():
            self.new_hand()
            
        self.post_plays()


    def next_hand(self):
        return        

    def pre_plays(self):
        if self.first_to_play != 1:
            for i in range(1, (self.first_to_play + 3) % 4):
                self.ask_to_play(i)

    def post_plays(self):
        if self.first_to_play != 0:
            rest_of_players = range(self.first_to_play, 4)
            self.get_plays(rest_of_players)

    def get_num_to_deal(self):
        return self.deal_amounts[self.round - 1][self.play - 1]

    def new_hand(self):
        self.deal()
        self.get_calls()

    def get_calls(self):
        return [self.players[player_num].call(self.to_obs()) for player_num in range(4)]

    def deal(self):
        for player_number in range(4):
            self.deck.deal(self.players[player_number].hand, times = self.get_num_to_deal())
        self.update_play()

    def to_obs(self):
        return {}

    def update_play(self):
        if self.play == len(self.deal_amounts[self.round - 1]) - 1: # if it is time to go to the next round
            self.play = 1
            self.round += 1
        else:
            self.play += 1
        
        if self.round == 5:
            self.done = True

    def hand_empty(self):
        return len(self.players[0].hand) == 0

    # calls and plays should be stored in player objects

    def get_plays(self, players):
        for player_num in players:
            self.add_play(self.players[player_num].play(self.to_obs()))

    def add_play(self, play):
        self.in_play.append(play)

    def ask_to_play(self, player_num):
        return self.players[player_num].play(self.to_obs())

    def process_hand_results(self):
        self.reset_play()
        self.update_takes()

    def update_takes(self):
        play_winner = self.winner()
        self.players[play_winner].add_take()

    def winner(self, cards):
        wildsuit = self.wild_suit
        first_suit = cards[0].suit

        if wildsuit == 4: # no wildsuit
            return self.highest_of_suit(cards, first_suit)
        else:
            if first_suit == wildsuit:
                return self.highest_of_suit(cards, first_suit)
            elif contains_suit(cards, wildsuit): # a wildsuit was playes
                return self.highest_of_suit(cards, wildsuit)
            else:
                return self.highest_of_suit(cards, first_suit)

    def highest_of_suit(self, cards, suit):
        highest = 0
        for i, card in enumerate(cards):
            if card.suit == suit and card.value > highest:
                highest = i
        return cards[highest]

    def reset_play(self):
        self.in_play = []
        self.first_suit = 4

    def is_done(self):
        return self.done