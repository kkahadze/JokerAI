import random
from src.deck import Deck
from src.player import Player
from agents.random_caller_random_player import RandomCallerRandomPlayer

from src.utils import card_to_int, int_to_card, contains_suit, highest_of_suit, index_of_highest_of_suit, int_to_suit, index_of_latest_base_joker, indexes_of_transformed_jokers, get_transformed_joker

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
        self.deal()
        self.get_calls()

        player_num = self.first_to_play
        if player_num != 0: 
            players_before = range(self.first_to_play, 4)
            self.get_plays(players_before)

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
        self.first_suit = 4
        self.in_play = []
        self.done = False

        # self.wild_value = 0 
        # self.gone = [0 for i in range(36)]

    def step(self, action):
        self.player_0_play(action, first=self.first_to_play == 0)
        self.pre_plays()
        self.process_hand_results()

        if self.is_done():
            return
        
        if self.hand_empty():
            self.new_hand()
        
        if not self.done:
            self.post_plays()

    def pre_plays(self):
        if self.first_to_play != 1:
            rest_of_players = range(1, (self.first_to_play + 3) % 4)
            self.get_plays(rest_of_players)

    def post_plays(self):
        if self.first_to_play != 0:
            rest_of_players = range(self.first_to_play, 4)
            self.get_plays(rest_of_players)

    def get_num_to_deal(self):
        return self.deal_amounts[self.round - 1][self.play - 1]

    def new_hand(self):
        self.update_score()
        self.update_play()
        if not self.done:
            self.deal()
            self.get_calls()

    def update_score(self):
        for player in self.players:
            player.update_score(self.get_num_to_deal())

    def get_calls(self):
        for player_num in range(4):
            self.players[player_num].call(self.to_obs())

    def deal(self):
        self.deck = Deck()
        for player_number in range(4):
            self.deck.deal(self.players[player_number].hand, times = self.get_num_to_deal())
        if self.deck:
            wild_card = self.deck[0]
            self.wild_card = wild_card
            if wild_card.value != 16:
                self.wild_suit = wild_card.suit
            else:
                self.wild_suit = 4

    def to_obs(self):
        in_play_ints = []
        for card_num in range(3):
            if card_num < len(self.in_play):
                in_play_ints.append(card_to_int(self.in_play[card_num]))
            else:
                in_play_ints.append(44)

        return {
            "dealt": self.get_num_to_deal(),
            "first_to_play": self.first_to_play,
            "dealer": self.dealer,
            "wild_suit": self.wild_suit,
            "first_suit": self.first_suit,
            "jokers_remaining": self.jokers_remaining,
            "in_play": in_play_ints,
            "players": {str(player.number) : player.to_obs() 
                            for player in self.players
                        }
        }

    def update_play(self):
        if self.play == len(self.deal_amounts[self.round - 1]): # if it is time to go to the next round
            self.play = 1
            self.round += 1
        else:
            self.play += 1

        if self.round == 5:
            self.done = True

        self.dealer = (self.dealer + 1) % 4
        self.reset_players()

    def reset_players(self):
        for player in self.players:
            player.reset()

    def hand_empty(self):
        return len(self.players[0].hand) == 0

    def get_plays(self, players):
        for player_num in players:
            choice = self.ask_to_play(player_num)
            if player_num == self.first_to_play:
                self.first_suit = choice.suit
            self.in_play.append(choice)

    def ask_to_play(self, player_num):
        return self.players[player_num].play(self.to_obs())

    def process_hand_results(self):
        winner = self.update_take()
        self.first_to_play = winner
        self.reset_play()

    def update_take(self):
        play_winner = (self.first_to_play + self.winner(self.in_play)) % 4
        self.players[play_winner].add_take()
        return play_winner

    def winner(self, cards):
        wildsuit = self.wild_suit
        first_suit = cards[0].suit

        if 16 in [card.value for card in cards]: # joker was played
            return index_of_latest_base_joker(cards)
        elif 15 in [card.value for card in cards]: # joker (vishi) was played
            return 0
        else:
            transformed_joker = get_transformed_joker(cards)
            if transformed_joker:
                indexes_of_indenticals = indexes_of_transformed_jokers(cards)
                is_transformed_suit = [True if card.suit == cards[indexes_of_indenticals[0]].suit else False for card in cards]
                if is_transformed_suit.count(True) == len(indexes_of_indenticals):
                    return indexes_of_indenticals[0]
            elif wildsuit == 4: # no wildsuit
                return index_of_highest_of_suit(cards, first_suit)
            else:
                if first_suit == wildsuit:
                    return index_of_highest_of_suit(cards, first_suit)
                elif contains_suit(wildsuit, cards): # a wildsuit was played
                    return index_of_highest_of_suit(cards, wildsuit)
                else:
                    return index_of_highest_of_suit(cards, first_suit)

    def reset_play(self):
        self.in_play = []
        self.first_suit = 4

    def is_done(self):
        return self.done

    def player_0_play(self, play, first):
        card = int_to_card(play)
        if first:
            self.first_suit = card.suit
        self.in_play.append(card)

    def print_game(self):
        obs = self.to_obs()
        print("____________________________________________________________________________")
        print()
        print("Round: " + str(self.round))
        print("Play: " + str(self.play))
        print("Dealt: " + str(obs["dealt"]))
        print("Wildsuit: " + int_to_suit(obs['wild_suit']))
        print("First to play: " + str(obs['first_to_play']))

        for num, player in enumerate(obs["players"].values()):
            print("Player: " + str(num))
            print("Hand: " + str(self.players[num].hand))
            print("Calls: " + str(player["desired"]))
            print("Takes: " + str(player["taken"]))
            print("")

        print("In play: " + str(self.in_play))
        print("Current scores: \n Player 0: " + str(self.players[0].score) + "\n Player 1: " + str(self.players[1].score) + "\n Player 2: " + str(self.players[2].score) + "\n Player 3: " + str(self.players[3].score) + "\n")

    def print_obs(self):
        obs = self.to_obs()
        print("____________________________________________________________________________")
        print("Dealt: " + str(obs["dealt"]))
        print("Wildsuit: " + int_to_suit(obs['wild_suit']))
        print("First to play: " + str(obs['first_to_play']))
        for num, player in enumerate(obs["players"].values()):
            print("Player: " + str(num))
            if num == 0:
                print("Hand: " + str(player["hand"]))
            print("Calls: " + str(player["desired"]))
            print("Takes: " + str(player["taken"]))
        print("In play: " + str(self.in_play))