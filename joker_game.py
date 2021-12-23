import random
import numpy as np

def main():
    class Card(object):
        def __init__(self, value, suit):
            self.value = value
            self.suit = suit
            self.showing = True

        def __repr__(self):
            value_name = ""
            suit_name = ""
            if self.showing:
                if self.value == 4:
                    value_name = "Six"
                elif self.value == 5:
                    value_name = "Seven"
                elif self.value == 6:
                    value_name = "Eight"
                elif self.value == 7:
                    value_name = "Nine"
                elif self.value == 8:
                    value_name = "Ten"
                elif self.value == 9:
                    value_name = "Jack"
                elif self.value == 10:
                    value_name = "Queen"
                elif self.value == 11:
                    value_name = "King"
                elif self.value == 12:
                    value_name = "Ace"
                elif self.value == 13:
                    value_name = "Joker"
                if self.suit == 0:
                    suit_name = "Diamonds"
                elif self.suit == 1:
                    suit_name = "Clubs"
                elif self.suit == 2:
                    suit_name = "Hearts"
                elif self.suit == 3:
                    suit_name = "Spades"
                if value_name == "Joker":
                    return "Joker"
                else:
                    return value_name + " of " + suit_name
            else:
                return "[CARD]"


    class StandardJokerDeck(list):
        def __init__(self):
            super().__init__()
            suits = list(range(4))
            values = list(range(5, 13))
            # Ranks 7 through A are added
            [[self.append(Card(i, j)) for j in suits] for i in values]
            # Ranks Six and Ace are added
            self.extend([Card(13, 0), Card(13, 0), Card(6, 0), Card(6, 2)]) 

        def __repr__(self):
            return f"Standard deck of cards\n{len(self)} cards remaining"

        def shuffle(self):
            random.shuffle(self)
            print("\n\n--deck shuffled--")

        def get(self, index):
            self[index]

        def deal(self, location, times=1):
            for i in range(times):
                location.cards.append(self.pop(0))

        def burn(self):
            self.pop(0)

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

        def compute_score(self, user):
            called = self.called
            taken = self.taken
            if called == 0 and taken == 0:
                return 50
            elif taken == 0:
                return -200
            elif taken != called:
                return (taken * 10)
            else:
                return (taken * 50 + 50)


    class Game(object):
        def __init__(self):
            self.deck = StandardJokerDeck()
            self.wildcard = Card(0,0)
            self.first_suit = Card(0,5)
            self.cards_dealt = 0
            self.round = 0
            self.play = 0
            self.users = [Player(0), Player(1), Player(2), Player(3)]
            self.dealer = random.randint(0, 3)

        def get_place_in_playing_order(self, player_id):
            dealer = self.dealer
            for i in range(1,4):
                if (self.dealer + i) % 4 == player_id:
                    out = i
            out

        def get_wildsuit(self):
            if self.wildcard.value != 13:
                return self.wildcard.suit
            else:
                return 4

        def next_dealer(self):
            (self.dealer + 1) % 4

        def set_dealer(self):
            self.dealer = self.next_dealer()

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
                self.play - 1
            elif self.round == 2:
                self.play + 7
            elif self.round == 3:
                self.play + 11
            elif self.round == 4:
                self.play + 19
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

            if firsts == []:
                if wilds == []:
                    return self
                else:
                    for card in joks:
                        wilds.append(card)
                    return wilds
            else:
                for card in joks:
                    firsts.append(card)
                return firsts

        def playing_phase(self):
            starter = self.dealer
            for i in range(0, self.cards_dealt):
                played = []
                for j in range(1, 5):
                    id = (starter + j) % 4
                    choices = self.playable(id, self.get_wildsuit(), self.first_suit)
                    choice = choices[self.get_card_choice(id)]
                    self.users[id].cards.remove(choice)
                    played.append(choice)
                    if j == 1:
                        self.first_suit = choice.suit
            
                starter = self.compute_winner(played)
                self.users[starter].taken += 1
            for i in self.users:
                i.score += i.compute_score()

        def reset_users(self):
            for user in self.users:
                user.called = 0
                user.taken = 0
                user.cards = []
        
        def set_random_calls(self):
            calls = []
            already = 0
            for i in range(1, 5):
                id = (self.dealer + i) % 4
                if i == 4:
                    call = self.get_random_call(already)
                else:
                    call = self.get_random_call(None)
                    already.append(call)
                calls.append(call)
            self.set_calls(calls[0],calls[1],calls[2],calls[3])
        
        def get_random_call(self, already):
            rand = random.randint(0, self.cards_dealt)
            if already != None:
                while rand == self.cards_dealt - already:
                    rand = random.randint(0, self.cards_dealt) 
            return rand

        def play_round(self):
            self.deck = StandardJokerDeck()
            self.deal_to_users()
            self.set_random_calls()
            self.playing_phase()
            self.reset_users()

        def get_wild_choice(self):
            0

        def get_card_choice(self, player):
            random.randint(0, len(self.users[player].cards))