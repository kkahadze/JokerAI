from src.card import Card
from collections import OrderedDict

def card_to_int(card: Card) -> int:
    if card.value == 6:
        return card.suit // 2 # 0 if Diamonds, 1 if Heart
    elif card.value == 14:
        return 34 + card.suit # 34 if red, 35 if black
    else:
        return (card.value - 7) * 4 + (card.suit) + 2

def suit_count(cards) -> tuple:
    diamonds = 0
    clubs = 0
    hearts = 0
    spades = 0

    for card in cards:
        if card > 33:
            continue
        elif card == 0:
            diamonds += 1
        elif card == 1:
            hearts += 1
        elif (card - 2) % 4 == 0:
            diamonds += 1
        elif (card - 2) % 4 == 1:
            clubs += 1
        elif (card - 2) % 4 == 2:
            hearts += 1
        elif (card - 2) % 4 == 3:
            spades += 1
    
    return diamonds, clubs, hearts, spades

def least_common_suit_in_hand(observation: OrderedDict) -> int:
    diamonds, clubs, hearts, spades = suit_count(observation['players']['0']['hand'])

    if diamonds <= clubs and diamonds <= hearts and diamonds <= spades:
        return 0
    elif clubs <= diamonds and clubs <= hearts and clubs <= spades:
        return 1
    elif hearts <= diamonds and hearts <= clubs and hearts <= spades:
        return 2
    elif spades <= diamonds and spades <= clubs and spades <= hearts:
        return 3

def wildsuit_count(observation: OrderedDict) -> int:
    wildsuit = observation['wild_suit']
    return suit_count(observation['players']['0']['hand'])[wildsuit]

def int_to_card(card: int) -> Card:
    return Card(card % 9 + 6, card // 9)

def want_to_win(observation: OrderedDict):
    '''
    This should eventually be learned by our model but a rule based approach will do for now.
    This rule based approach returns True if the player wants to win, and False if they want to take
    '''
    if observation.players[0].desired != observation.players[0].taken:
        return True
    else:
        return False

def first_to_play(observation: OrderedDict) -> bool:
    if observation.in_play[0] == 36:
        return True
    else:
        return False

def choose_suit_for_highest(observation: OrderedDict) -> int:
    '''
    This should also eventually be learned, for now, the choice of suit is based on the amount of hands that the player wants,
    as well as the amount of wildcards in their hand.
    '''

    more_wanted = additional_hands_desired(observation.players[0].desired - observation.players[0].taken)
    wildsuits_in_hand = wildsuit_count(observation)

    if more_wanted > 1 and wildsuits_in_hand <= more_wanted + 1:
        return observation.wild_suit
    elif more_wanted == 0:
        return least_common_suit_in_hand(observation)

def choose_suit_for_take(observation):
    '''
    This should also eventually be learned. For now, this is based on
    '''
    if want_to_win(observation):
        return least_common_suit_in_hand(observation)
