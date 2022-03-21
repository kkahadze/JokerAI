import csv
import random
import numpy as np
import csv
import sys
import time
import pickle

from sklearn.neighbors import KNeighborsClassifier
from display import Display as dp
from game import Player, Card, StandardJokerDeck


class Simulation(object):
    def __init__(self):
        self.places = []
        self.dealt = []
        self.wild = []
        self.num_wild = []
        self.num_joks = []
        self.already_called = []
        self.correct = []
        self.taken = []

    def run(self, games, model_wanted):
        for _ in range(games): # amount of games to be simulated
            if model_wanted:
                filename = 'finalized_model.sav'
                file = open(filename, 'rb')
                model = pickle.load(file)
                file.close()
                game = SimulatedGame(model)
            else:
                game = SimulatedGame(None)

            for _ in range(24): # 24 plays a game
                game.update_round()
                game.deal_to_users()
                game.set_wildcard()
                
                for j in range(4):
                    self.num_wild.append(len(list(filter(lambda x: x.suit == game.get_wildsuit() and x.value != 13, list(game.users[j].cards)))))
                    self.num_joks.append(len(list(filter(lambda x: x.value == 13, list(game.users[j].cards)))))
                    for k in range(1,5):
                        if (((game.dealer + k) % 4) == j):
                            self.places.append(k)
                    self.dealt.append(game.cards_dealt)
                    self.wild.append(game.get_wildsuit() != 4)
                   
                game.play_round()
                
                for j in range(4):
                    adder = 0
                    place = 1
                    for k in range(1,5):
                        if (((game.dealer + k) % 4) == j):
                            place = k
                    for k in range(1, place):
                        adder += (game.users[j - k].called)
                    self.already_called.append(adder)

                for j in range(4): # Adding results of hand
                    self.correct.append(game.users[j].called == game.users[j].taken)
                    self.taken.append(game.users[j].taken) 
                game.reset_users()

    def write_to_csv(self):
        with open('joker_simulations.csv', mode='w') as joker_file:
            joker_writer = csv.writer(joker_file, delimiter=',')
            for i in range(len(self.places)):
                joker_writer.writerow([self.places[i], self.dealt[i],self.wild[i],self.num_wild[i],self.num_joks[i],self.already_called[i],self.correct[i],self.taken[i]])

class SimulatedGame(object):
    def __init__(self, model):
        self.deck = StandardJokerDeck()
        self.wildcard, self.first_suit = Card(0,0),  Card(0,5)
        self.cards_dealt, self.round, self.play = 0, 0, 0
        self.users = [Player(0), Player(1), Player(2), Player(3)]
        self.dealer = random.randint(0, 3)
        self.model = model

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
        for i in range(4):
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
            for i in range(4):
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

        for i in range(self.cards_dealt):
            played = []
            for j in range(4):
                player = (starter + j) % 4
                choice = self.get_card_choice(player, played, starter)
                self.users[player].cards.remove(choice)
                played.append(choice)
                if j == 0:
                    self.first_suit = choice.suit

            # using slicing to left rotate by 3
            played = played[(4 - starter):] + played[:(4 - starter)] # Rotates the array of played cards in order to index it by player id

            starter = self.compute_winner(played) # The winner of the hand becomes the starter of the next hand
            self.users[starter].taken += 1
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
        for i in range(1,5):
            player = (self.dealer + i) % 4
            if self.get_wildsuit() == 4 : 
                wild = 0 
            else: 
                wild = 1
            adder = 0
            for j in range(1, i):
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