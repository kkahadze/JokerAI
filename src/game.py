import random
from src.deck import Deck
from src.player import Player
from agents.random_caller_random_player import RandomCallerRandomPlayer
from src.utils import playable, adjust_for_order

from src.utils import card_to_int, int_to_card, int_to_suit, winner

class Game:
    def __init__(self, players_in: list = [RandomCallerRandomPlayer(i) for i in range(4)], only_nines=False):
        self.player_types = [type(player) for player in players_in]
        if only_nines:
            self.only_nines = True
            self.deal_amounts = [
                [9, 9, 9, 9],
                [9, 9, 9, 9],
                [9, 9, 9, 9],
                [9, 9, 9, 9],
            ]
        else:
            self.only_nines = False
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
        self.info = {}
        self.call_data = []
        self.wanted_and_tooks = []

    def reset(self):
        self.reset_vars()
        self.deal()
        call_order = [(self.first_to_play + i) % 4 for i in range(4)]
        self.get_calls(call_order)

        player_num = self.first_to_play
        if player_num != 0: 
            players_before = range(self.first_to_play, 4)
            self.get_plays(players_before)
        self.info = {"rands": 0, 
                     "choice": 0,
                     "xishti": 0,
                        "bust": 0,
                        "success": 0,
                     }
        self.call_data = []
        self.wanted_and_tooks = []
        

    def reset_vars(self): # resets deck, players, round, play, dealer, wild_suit, jokers_remaining, in_play and done
        self.deck = Deck()
        for player in self.players:
            player.reset()
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
        self.player_0_play(action)
        self.pre_plays()
        self.process_hand_results()
        
        if self.hand_empty() and self.get_num_to_deal():
            self.new_hand()
        
        if not self.done:
            self.post_plays()
        else:
            self.done = True

    def pre_plays(self):
        if self.first_to_play != 1:
            rest_of_players = range(1, (self.first_to_play + 3) % 4 + 1)
            self.get_plays(rest_of_players)

    def post_plays(self):
        if self.first_to_play != 0:
            rest_of_players = range(self.first_to_play, 4)
            self.get_plays(rest_of_players)

    def get_num_to_deal(self):
        if self.round == 5 or self.round == 4 and self.play > 4:
            return None
        else:
            return self.deal_amounts[self.round - 1][self.play - 1]

    def new_hand(self):
        self.update_score()
        self.update_play()
        if not self.done:
            self.deal()
            call_order = [(self.first_to_play + i) % 4 for i in range(4)]
            self.get_calls(call_order)
        else:
            self.done = True

    def update_score(self):
        for player in self.players:
            player.update_score(self.get_num_to_deal(), self)
            if player.desired != player.taken:
                self.wanted_and_tooks.append((player.desired, player.taken))
            self.call_data.append(player.get_call_data())

    def get_calls(self, players):
        for player_num in players:
            self.players[player_num].record_decision_time_obs(self.to_obs())
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
        player_dict = {str(player.number) : player.to_obs() 
                            for player in self.players
                        }

        in_play_ints = []
        for card_num in range(3):
            if card_num < len(self.in_play):
                in_play_ints.append(card_to_int(self.in_play[card_num]))
            else:
                in_play_ints.append(44)
        out = {
            "dealt": self.get_num_to_deal(),
            "first_to_play": self.first_to_play,
            "dealer": self.dealer,
            "wild_suit": self.wild_suit,
            "first_suit": self.first_suit,
            "jokers_remaining": self.jokers_remaining,
            "in_play": in_play_ints,

            "hand": [],

            "player0taken": player_dict["0"]['taken'],
            "player0desired": player_dict["0"]['desired'],

            "player1taken": player_dict["1"]['taken'],
            "player1desired": player_dict["1"]['desired'],

            "player2taken": player_dict["2"]['taken'],
            "player2desired": player_dict["2"]['desired'],

            "player3taken": player_dict["3"]['taken'],
            "player3desired": player_dict["3"]['desired'],
        }

        for i in range(9):
            out['hand'].append(card_to_int(self.players[0].hand[i]) if i < len(self.players[0].hand) else 44)

        return out

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
            choice = self.ask_to_play(player_num % 4)
            if self.in_play == []:
                self.first_suit = choice.suit
            self.in_play.append(choice)

    def ask_to_play(self, player_num):
        card_played = self.players[player_num].play(self.to_obs())
        return card_played

    def process_hand_results(self):
        winner = self.update_take()
        self.first_to_play = winner
        self.reset_play()

    def update_take(self):
        play_winner = (self.first_to_play + winner(self.to_obs())) % 4
        self.players[play_winner].add_take()
        return play_winner

    def reset_play(self):
        self.in_play = []
        self.first_suit = 4

    def is_done(self):
        return self.done

    def player_0_play(self, play): # may just need to be combined with other plays
        card_chosen = int_to_card(play)

        # if card_chosen in self.players[0].hand:
        #     self.players[0].hand.remove(card_chosen)
        # elif self.first_to_play == 0 and card_chosen.base() in self.players[0].hand:
        #     self.players[0].hand.remove(card_chosen.base())
        # else:
        #     playab = playable(self.to_obs())
        #     first_to_play = self.first_to_play == 0
        #     adjusted = adjust_for_order(playab, first_to_play)
        #     card_chosen = random.choice(adjusted)
        #     base_card = card_chosen.base()
        #     self.players[0].hand.remove(base_card)
        
        if self.in_play == []:
            self.first_suit = card_chosen.suit


        self.in_play.append(card_chosen)

    def print_game(self):
        print("____________________________________________________________________________")
        print()
        print("Round: " + str(self.round))
        print("Play: " + str(self.play))
        print("Dealt: " + str(self.get_num_to_deal()))
        print("Wildsuit: " + int_to_suit(self.wild_suit))
        print("First to play: " + str(self.first_to_play))

        for num in range(4):
            print("Player: " + str(num))
            print("Hand: " + str(self.players[num].hand))
            print("Calls: " + str(self.players[num].desired))
            print("Takes: " + str(self.players[num].taken))
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

    def highest_score_player(self):
        max_player = 0
        for i in range(1, 4):
            if self.players[i].score > self.players[max_player].score:
                max_player = i
        return max_player
    
    def print_game_state(self):
        # Print out the cards every player has
        for player in self.players:
            print("Player " + str(player.number) + " has: " + str(player.hand))
        print("")

        # Print out the cards that have been played
        print("Cards in play: " + str(self.in_play))

        #  

    # def record_call_decision_time_obs(self, player):
    #     obs = self.to_obs()
    #     obs["player0hand"] = [card_to_int(card) for card in self.players[player].hand]
    #     self.decision_time_obs.append(obs)

    # def record_result_of_decision(self, player):
    #     self.success.append(self.players[player].desired == len(self.players[player].hand))