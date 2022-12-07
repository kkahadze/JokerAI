import random

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        values = {
            6: lambda: "Six",
            7: lambda: "Seven",
            8: lambda: "Eight",
            9: lambda: "Nine",
            10: lambda: "Ten",
            11: lambda: "Jack",
            12: lambda: "Queen",
            13: lambda: "King",
            14: lambda: "Ace",
            15: lambda: "Joker",
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
    
    def rank(self):
        '''
        Returns the rank of the card 0 indexed. 6 is the lowest rank (0), and Joker (15) is the highest rank ().
        '''
        return self.value - 6

    def same_suit(self, other):
        '''
        Returns True if the card is the same suit as the other card.
        '''
        return self.suit == other.suit

    def __lt__ (self, other):
        return self.rank() < other.rank()

    def __gt__ (self, other):
        return self.rank() > other.rank()

    def __eq__ (self, other):
        return self.rank() == other.rank()

    def __ne__ (self, other):
        return self.rank() != other.rank()

    def __le__ (self, other):     
        return self.rank() <= other.rank()  

    def __ge__ (self, other):
        return self.rank() >= other.rank()      
    
    def __hash__(self):
        return hash((self.value, self.suit))
    
    def __str__(self):
        return self.__repr__()  
# class StandardJokerDeck(list):
#     def __init__(self):
#         super().__init__()
#         suits = list(range(4))
#         values = list(range(5, 13))
#         # Ranks 7 through A are added
#         [[self.append(Card(i, j)) for j in suits] for i in values]
#         # Ranks Six and Ace are added
#         self.extend([Card(13, 0), Card(13, 0), Card(4, 0), Card(4, 2)]) 

#     def __repr__(self):
#         out = ""
#         for card in self:
#             out += (str(card) + "\n")
#         return out

#     def shuffle(self):
#         random.shuffle(self)

#     def get(self, index):
#         return self[index]

#     def deal(self, location, times=1):
#         for i in range(times):
#             location.cards.append(self.burn())

#     def burn(self):
#         return self.pop(0)