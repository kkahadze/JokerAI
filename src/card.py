import random

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        values = {
            5: lambda: "Joker (Take)", # Special card to indicate a Joker being played as Take/წაიგოს
            6: lambda: "Six",
            7: lambda: "Seven",
            8: lambda: "Eight",
            9: lambda: "Nine",
            10: lambda: "Ten",
            11: lambda: "Jack",
            12: lambda: "Queen",
            13: lambda: "King",
            14: lambda: "Ace",
            15: lambda: "Joker (Highs)", # Special card to indicate a Joker being played as High/ვიში
            16: lambda: "Joker",
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
    
    def is_suit(self, suit):
        '''
        Returns True if the card is the same suit as "suit".
        '''
        return self.suit == suit

    def __lt__ (self, other):
        return self.rank() < other.rank()

    def __gt__ (self, other):
        return self.rank() > other.rank()

    def __eq__ (self, other):
        if isinstance(other, Card):
            return self.rank() == other.rank() and self.suit == other.suit
        else:
            return False

    def __ne__ (self, other):
        if isinstance(other, Card):
            return self.rank() != other.rank() or self.suit != other.suit
        else:
            return True

    def __le__ (self, other):     
        return self.rank() <= other.rank()  

    def __ge__ (self, other):
        return self.rank() >= other.rank()      
    
    def __hash__(self):
        return hash((self.value, self.suit))
    
    def __str__(self):
        return self.__repr__()  

    def is_joker(self):
        return self.value == 15