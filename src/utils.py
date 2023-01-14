from src.card import Card
from collections import OrderedDict
import random

def additional_hands_desired(observation):
    return observation['players']['0']['desired'] - observation['players']['0']['taken']

def card_to_int(card: Card, first=False) -> int:
    if card.value == 6:
        return card.suit // 2 # 0 if Diamonds, 1 if Heart
    elif card.value == 16:
        return 34  # 34 if red, 35 if black
    elif card.value == 5:
        if first:
            return 36 + card.suit
        else:
            return 35
    elif card.value == 15:
        return card.suit + 40
    else:
        return (card.value - 7) * 4 + (card.suit) + 2

def int_to_card(card_index: int, restricted_suits = None) -> Card:
    if card_index > 43:
        return None
    elif card_index < 2:
        return Card(6, card_index * 2)
    elif card_index == 34:
        if restricted_suits:
            suit = random.choice(list(filter(lambda suit: suit not in restricted_suits, range(4))))
        else:
            suit = random.choice(range(4))
        return Card(16, suit)
    elif card_index == 35:
        if restricted_suits:
            suit = random.choice(list(filter(lambda suit: suit not in restricted_suits, range(4))))
        else:
            suit = random.choice(range(4))
        return Card(5, suit)
    elif card_index >= 36 and card_index <= 39:
        return Card(5, (card_index - 36))
    elif card_index >= 40 and card_index <= 43:
        return Card(15, (card_index - 40))
    else:
        return Card((card_index - 2) // 4 + 7, (card_index - 2) % 4)

def int_to_suit(suit_index: int) -> str:
    if suit_index == 0:
        return 'Diamonds'
    elif suit_index == 1:
        return 'Clubs'
    elif suit_index == 2:
        return 'Hearts'
    elif suit_index == 3:
        return 'Spades'
    elif suit_index == 4:
        return 'No Wild Suit'

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

def most_common_suit_in_hand(observation: OrderedDict) -> int:
    diamonds, clubs, hearts, spades = suit_count(observation['players']['0']['hand'])

    if diamonds >= clubs and diamonds >= hearts and diamonds >= spades:
        return 0
    elif clubs >= diamonds and clubs >= hearts and clubs >= spades:
        return 1
    elif hearts >= diamonds and hearts >= clubs and hearts >= spades:
        return 2
    elif spades >= diamonds and spades >= clubs and spades >= hearts:
        return 3

def wildsuit_count(observation: OrderedDict) -> int:
    wildsuit = observation['wild_suit']
    return suit_count(observation['players']['0']['hand'])[wildsuit]

def want_to_win(observation: OrderedDict):
    '''
    This should eventually be learned by our model but a rule based approach will do for now.
    This rule based approach returns True if the player wants to win, and False if they want to take
    '''
    if observation['players']['0']['desired'] != observation['players']['0']['taken']:
        return True
    else:
        return False

def first_to_play(observation: OrderedDict) -> bool:
    if observation['in_play'][0] == 46:
        return True
    else:
        return False

def choose_suit_for_highest(observation: OrderedDict) -> int:
    '''
    This should also eventually be learned, for now, the choice of suit is based on the amount of hands that the player wants,
    as well as the amount of wildcards in their hand.
    '''

    more_wanted = additional_hands_desired(observation)
    wildsuits_in_hand = wildsuit_count(observation)

    if more_wanted > 1 and wildsuits_in_hand <= more_wanted + 1:
        return observation['wild_suit']
    elif more_wanted == 0:
        return least_common_suit_in_hand(observation)

def choose_suit_for_take(observation):
    '''
    This should also eventually be learned, or better yet completely based on what cards have gone.
    '''
    most_common_suit = most_common_suit_in_hand(observation)
    diamonds, clubs, hearts, spades = suit_count(observation['players']['0']['hand'])
    counts = [diamonds, clubs, hearts, spades]
    common_count = counts[most_common_suit]

    if common_count > 1 and common_count < 5:
        return most_common_suit_in_hand(observation)
    else:
        return random.randint(0, 3)

def garunteed_win_with_jok(observation):
    '''
    Returns True if a player can garunteed by playing a joker
`    '''
    if observation["in_play"][-1] != 46:
        return True
    elif observation["jokers_remaining"] == 1:
        return True
    else:
        return False

def beatable_obs(observation):
    return False
        
def cards_in_hand(observation):
    hand = observation["players"]["0"]["hand"]
    return 9 - [card == 44 for card in hand].count(True)

def obs_to_string(observation):
    obs_string = ""

    card_ints = observation["in_play"]
    wildsuit = observation["wild_suit"]
    hand0_ints, desired0, taken0 = observation["players"]["0"]["hand"], observation["players"]["0"]["desired"], observation["players"]["0"]["taken"]
    desired1, taken1 = observation["players"]["1"]["desired"], observation["players"]["1"]["taken"]
    desired2, taken2 = observation["players"]["2"]["desired"], observation["players"]["2"]["taken"]
    desired3, taken3 = observation["players"]["3"]["desired"], observation["players"]["3"]["taken"]
    jokers_remaining = observation["jokers_remaining"]

    cards = list(map(lambda card_int: int_to_card(card_int), card_ints))
    cards = truncate_at_first_none(cards)
    
    obs_string += "Cards Played: " + str(cards) + "\n"
    obs_string += "Wildsuit: " + str(int_to_suit(wildsuit)) + "\n"
    
    hand0 = list(map(lambda card_int: int_to_card(card_int), hand0_ints))
    hand0 = truncate_at_first_none(hand0)

    obs_string += "Hand: " + str(hand0) + "\n"
    obs_string += "Desired: " + str(desired0) + "\n"
    obs_string += "Taken: " + str(taken0) + "\n"

    obs_string += "Opponent 1 Desired: " + str(desired1) + "\n"
    obs_string += "Opponent 1 Taken: " + str(taken1) + "\n"

    obs_string += "Opponent 2 Desired: " + str(desired2) + "\n"
    obs_string += "Opponent 2 Taken: " + str(taken2) + "\n"

    obs_string += "Opponent 3 Desired: " + str(desired3) + "\n"
    obs_string += "Opponent 3 Taken: " + str(taken3) + "\n"

    obs_string += "Jokers Remaining: " + str(jokers_remaining) + "\n"

    return obs_string


def print_obs(observation):
    print(obs_to_string(observation))
    
def truncate_at_first_none(cards: list):
    '''
    Truncates a list of cards at the first None, else returns the entire list if no None is found
    '''
    for i, card in enumerate(cards):
        if card == None:
            return cards[:i]
    return cards

def playable(observation): # Returns a list of cards that can be played, accounting for jokers
    hand = truncate_at_first_none(list(map(lambda card_int: int_to_card(card_int), observation["players"]["0"]["hand"])))

    if cards_in_hand(observation) == 1:
        return [hand[0]]
    else:
        if first_to_play(observation):
            return hand

        else:
            if first_suit_exists(observation):
                if has_first_suit(observation):
                    return filter_by_suit_with_joks(hand, first_suit_index(observation))
                else:
                    if not wildsuit_exists(observation):
                        return hand
                    else:
                        if not have_wild_suit(observation):
                            return hand
                        else:
                            return filter_by_suit_with_joks(hand, get_wildsuit(observation))
            elif not wildsuit_exists(observation):
                return hand
            else:
                if not have_wild_suit(observation):
                    return hand
                else:
                    return filter_by_suit_with_joks(hand, get_wildsuit(observation))

def filter_by_suit_with_joks(cards: list, suit: str):
    '''
    Filters the cards inputted to only include cards of the given suit and jokers
    '''
    return list(filter(lambda card: card.suit == suit or card.value == 16 or card.value == 15 or card.value == 5, cards))

def filter_by_suit_without_joks(cards: list, suit: str):
    '''
    Filters the cards inputted to only include cards of the given suit
    '''
    return list(filter(lambda card: card.suit == suit, cards))

def first_suit_exists(observation):
    '''
    Returns True if the first suit exists in the current observation
    '''
    cards = truncate_at_first_none(list(map(lambda card_int: int_to_card(card_int), observation["in_play"])))
    if cards:
        return cards[0].suit
    else:
        return False

def first_suit_index(observation):
    '''
    Returns the index of the first suit in the current observation
    '''
    cards = truncate_at_first_none(list(map(lambda card_int: int_to_card(card_int), observation["in_play"])))
    if cards:
        return cards[0].suit
    else:
        return None

def wildsuit_exists(observation):
    '''
    Returns True if the wildsuit exists in the current observation
    '''
    return observation["wild_suit"] != 4

def get_wildsuit(observation):
    '''
    Returns the wildsuit in the current observation
    '''
    return observation["wild_suit"]

def contains_suit(suit, hand):
    '''
    Returns True if the hand contains the given suit
    '''
    return suit in list(map(lambda card: card.suit, hand))

def has_first_suit(observation):
    '''
    Returns True if Player 0's hand contains the first suit
    '''
    return contains_suit(first_suit_index(observation), truncate_at_first_none(list(map(lambda card_int: int_to_card(card_int), observation["players"]["0"]["hand"]))))

def have_wild_suit(observation, number = 0, cards = []):
    '''
    Returns True if Player 0's hand contains the wildsuit
    '''
    wildsuit = get_wildsuit(observation)
    if number == 0:
        player_cards = observation["players"]["0"]["hand"]
        wildsuit_cards = list(filter(lambda card_int: card_int == wildsuit, player_cards))
        truncated_wild_ints = truncate_at_first_none(wildsuit_cards)
        truncated_wilds = list(map(lambda card_int: int_to_card(card_int), truncated_wild_ints))
        return contains_suit(wildsuit, truncated_wilds)
    else:
        return contains_suit(wildsuit, cards)
    

def highest_of_suit(cards, suit):
    highest = 0
    max = 0
    for i, card in enumerate(cards):
        if card.suit == suit and card.value > max:
            max = card.value
            highest = i
    
    if max:
        return cards[highest]
    else:
        return None

def index_of_highest_of_suit(cards, suit):
    highest = 0
    max = 0
    for i, card in enumerate(cards):
        if card.suit == suit and card.value >= max:
            max = card.value
            highest = i
    
    if max:
        return highest
    else:
        return None

def index_of_latest_base_joker(cards):
    index = -1
    for i, card in enumerate(cards):
        if card.value == 16:
            index = i
    return index

def get_transformed_joker(cards):
    for card in cards:
        if card.value == 6 and cards.count(card) > 1:
            return card

def indexes_of_transformed_jokers(cards):
    indexes = []
    for i, card in enumerate(cards):
        if card.value == 6 and cards.count(card) > 1:
            indexes.append(i)
    return indexes