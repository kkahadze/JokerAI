import random
import numpy as np
import csv
import sys
import time
import pickle
from sklearn.neighbors import KNeighborsClassifier
from display import Display as dp

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        values = {
            4: lambda: "Six",
            5: lambda: "Seven",
            6: lambda: "Eight",
            7: lambda: "Nine",
            8: lambda: "Ten",
            9: lambda: "Jack",
            10: lambda: "Queen",
            11: lambda: "King",
            12: lambda: "Ace",
            13: lambda: "Joker",
        }
        suits = {
            0: lambda : "Diamonds",
            1: lambda : "Clubs",
            2: lambda : "Hearts",
            3: lambda : "Spades",
        }
        
        value_name = values[self.value]()
        suit_name = suits[self.suit]()

        if value_name == "Joker":
            return "Joker"
        else:
            return value_name + " of " + suit_name


class StandardJokerDeck(list):
    def __init__(self):
        super().__init__()
        suits = list(range(4))
        values = list(range(5, 13))
        # Ranks 7 through A are added
        [[self.append(Card(i, j)) for j in suits] for i in values]
        # Ranks Six and Ace are added
        self.extend([Card(13, 0), Card(13, 0), Card(4, 0), Card(4, 2)]) 

    def __repr__(self):
        out = ""
        for card in self:
            out += (str(card) + "\n")
        return out

    def shuffle(self):
        random.shuffle(self)

    def get(self, index):
        return self[index]

    def deal(self, location, times=1):
        for i in range(times):
            location.cards.append(self.burn())

    def burn(self):
        return self.pop(0)

class Player(object):
    def __init__(self, id_in):
        self.id = id_in
        self.score = 0
        self.cards = []
        self.called = 0
        self.taken = 0

    def __repr__(self):
        id = self.id
        return id

class Game(object): # Non simulated game currently uses model every time
    def __init__(self):
        self.deck = StandardJokerDeck()
        self.wildcard = Card(0,0)
        self.first_suit = Card(0,5)
        self.cards_dealt = 0
        self.round = 0
        self.play = 0
        self.users = [Player(0), Player(1), Player(2), Player(3)]
        self.dealer = random.randint(0, 3)
        self.model = None

    def get_place_in_playing_order(self, player_id):
        dealer = self.dealer
        out = 5
        for i in range(1,5):
            if (dealer + i) % 4 == player_id:
                out = i
        return out

    def get_wildsuit(self):
        if self.wildcard.value != 13:
            return self.wildcard.suit
        else:
            return 4

    def next_dealer(self):
        return (self.dealer + 1) % 4

    def set_dealer(self):
        self.dealer = (self.dealer + 1) % 4

    def update_round(self): 
        self.set_dealer()
        out = None

        if self.round == 1 and self.play == 8:
            self.round += 1
            self.play = 1
        elif self.round == 0 and self.play == 0:
            self.round = 1
            self.play = 1
        elif self.round == 2 and self.play == 4:
            self.round = 3
            self.play = 1
        elif self.round == 3 and self.play == 8 :
            self.round = 4
            self.play = 1
        else:
            self.play += 1

        if self.round == 1 or self.round == 3:
            self.cards_dealt = self.play
        else:
            self.cards_dealt = 9

        out

    def set_calls(self, u0, u1, u2, u3):
        self.users[0].called = u0
        self.users[1].called = u1
        self.users[2].called = u2
        self.users[3].called = u3

    def get_play_index_of_game(self):
        if self.round == 1:
            return self.play - 1
        elif self.round == 2:
            return self.play + 7
        elif self.round == 3:
            return self.play + 11
        elif self.round == 4:
            return self.play + 19
        else:
            None

    def deal_to_users(self):
        random.shuffle(self.deck)
        for i in range(0, 4):
            self.deck.deal(self.users[i], self.cards_dealt)

    def set_wildcard(self):
        if self.round == 2 or self.round == 4:
            choices = self.users[(self.dealer + 1) % 4].cards[0:3]
            choice = self.get_wild_choice()
            self.wildcard = choices[choice]
        else:
            self.wildcard = self.deck[0]

    def card_to_weight(self, card):
        weight = 0
        if card.suit == self.get_wildsuit():
            weight += 200
        elif card.suit == self.first_suit:
            weight += 100
        if card.value == 13:
            weight += 400
        else:
            weight += int(card.value)
        return weight

    def compute_winner(self, played):
        jok = 5
        joks = 0
        for i in range(1,5):
            if played[(self.dealer + i) % 4].value == 13:
                    jok = (self.dealer + i) % 4
                    joks += 1
        if joks == 2:
            return jok
        else:
            weights = []
            for i in range(0,4):
                weights.append(self.card_to_weight(played[i]))
            return (np.argmax(np.asarray(weights)))

    def playable(self, player, wildsuit, first_suit):
        firsts = list(filter(lambda x: x.suit == first_suit and not x.value == 13, self.users[player].cards))
        wilds = list(filter(lambda x: x.suit == wildsuit and not x.value == 13, self.users[player].cards))
        joks = list(filter(lambda x: x.value == 13, self.users[player].cards))

        if self.first_suit == None:
            return self.users[player].cards
        elif firsts == []:
            if wilds == []:
                return self.users[player].cards
            else:
                for card in joks:
                    wilds.append(card)
                return wilds
        else:
            for card in joks:
                firsts.append(card)
            return firsts

    def playing_phase(self):
        starter = (self.dealer + 1) % 4
        dp.wild(self.get_wildsuit())

        for i in range(self.cards_dealt):
            dp.cards_in_hand(self.users[0].cards)
            played = []
            for j in range(0, 4):
                player = (starter + j) % 4
                choices = self.playable(player, self.get_wildsuit(), self.first_suit)
                if player == 0:
                    choices = self.playable(player, self.get_wildsuit(), self.first_suit)
                    dp.playable(choices)
                    choice = choices[dp.ask_card_choice(len(choices))]
                else:
                    choice = self.get_card_choice(player, played, starter)
                self.users[player].cards.remove(choice)
                played.append(choice)
                if j == 0:
                    self.first_suit = choice.suit
                dp.cards(played)
                time.sleep(.5)
            
            # using slicing to left rotate by 3
            played = played[(4 - starter):] + played[:(4 - starter)] # Rotates the array of played cards in order to index it by player id

            starter = self.compute_winner(played) # The winner of the hand becomes the starter of the next hand
            self.users[starter].taken += 1
            dp.winner_of_hand(self, starter)
            time.sleep(1)
            self.first_suit = None

        for i in range(4):
            self.users[i].score += self.get_player_score(i)

    def reset_users(self):
        for user in self.users:
            user.called = 0
            user.taken = 0
            user.cards = []
        
    def get_player_score(self, player_id):
        player = self.users[player_id]
        called = player.called
        taken = player.taken
        if taken == 0 and called > 0:
            return -200
        elif taken != called:
            return (taken * 10)
        elif taken == self.cards_dealt:
            return taken * 100
        else:
            return (taken * 50 + 50)

    def set_random_calls(self):
        calls = []
        already = 0
        for i in range(1, 5):
            id = (self.dealer + i) % 4
            if i == 4:
                call = self.get_random_call(already)
            else:
                call = self.get_random_call(None)
                already += call
            calls.append(call)
        self.set_calls(calls[0],calls[1],calls[2],calls[3])

    def get_random_call(self, already):
        # Cap can be set to only record hands with little cards
        cap = self.cards_dealt
        rand = random.randint(0, cap)
        if already != None:
            while rand == self.cards_dealt - already:
                rand = random.randint(0, cap) 
        return rand
    
    def set_predicted_calls(self, model):
        calls = [0] * 4
        for i in range(1,4): # Should this be 0 - 4?
            player = (self.dealer + i) % 4
            if (player == 0):
                dp.wild(self.get_wildsuit())
                dp.cards_in_hand(self.users[player].cards)
                call = dp.ask_call(self.cards_dealt)
            else:
                if self.get_wildsuit() == 4 : 
                    wild = 0 
                else: 
                    wild = 1
                adder = 0
                for j in range(0, i - 1):
                    adder += self.users[(player - j) % 4].called
                call = self.get_prediction(
                                            i / 3, 
                                            (self.cards_dealt - 1) / 8,
                                            wild,
                                            len(list(filter(lambda x: x.suit == self.get_wildsuit() and x.value != 13, self.users[player].cards))) / 9,
                                            len(list(filter(lambda x: x.value == 13, self.users[player].cards))) / 2,
                                            adder / 27,
                                            model
                                            )
            calls[(self.dealer + i) % 4] = call
            self.set_calls(calls[0],calls[1],calls[2],calls[3])
            
    def get_prediction(self, place, dealt, wild, num_wilds, num_joks, already, model):
        mp = model.predict([[place, dealt, wild, num_wilds, num_joks, already]])
        return mp[0]

    def play_round(self):
        self.deck = StandardJokerDeck()
        if self.model == None:
            self.set_random_calls()
        else:
            self.set_predicted_calls(self.model)
        self.playing_phase()
        dp.scores(self)

    def get_wild_choice(self):
        return 0

    def get_weakest(self, cards):
        weakest = cards[0]

        if len(cards) == 1:
            return weakest
        else:
            for card in cards:
                if card.value < weakest.value:
                    weakest = card
            return weakest
    
    def get_strongest(self, cards):
        strongest = cards[0]

        if len(cards) == 1:
            return strongest
        else:
            non_joks = list(filter(lambda x: x.value != 13, cards))
            if len(non_joks) == 0:
                return strongest
            for card in cards:
                if card.value > strongest.value and card.value != 13:
                    strongest = card
            return strongest


    def get_card_choice(self, player_id, played, starter):
        player = self.users[player_id]
        cards = self.playable(player_id, self.get_wildsuit(), self.first_suit)

        if player_id == starter:
            if len(cards) == player.called - player.taken:
                return self.get_strongest(cards)
            else:
                return self.get_weakest(cards)
        else:
            beatable = True
            aggressive = player.taken != player.called
            contains_wild = False
            for card in played: # Determine if the cards currently played are beatable
                if card.suit == self.get_wildsuit():
                    contains_wild = True
                    if (len(list(filter(lambda x: x.suit == self.get_wildsuit() and card.value > card.value, cards))) == 0):
                        beatable = False
                    
            if not contains_wild:
                for card in played:
                    if (len(list(filter(lambda x: x.suit == self.first_suit and card.value > card.value, cards))) == 0):
                        beatable = False
                    else:
                        beatable = True
                        break
            
            if beatable and aggressive:
                return self.get_strongest(cards)
            else:
                return self.get_weakest(cards) 

    def load_model(self):
        filename = 'finalized_model.sav'
        file = open(filename, 'rb')
        self.model = pickle.load(file)
        file.close()

    def run(self):
        game = Game()
        game.load_model()
        for i in range(0, 24): # 24 plays a game
            game.update_round()
            game.deal_to_users()
            game.set_wildcard()   
            game.play_round()
            game.reset_users()