from src.card import Card
from collections import OrderedDict
import random
import pandas as pd

def additional_hands_desired(observation):
    return observation['player0desired'] - observation['player0taken']

def card_to_int(card: Card, first=False) -> int:
    if card.value == 6:
        return card.suit // 2 # 0 if Diamonds, 1 if Heart
    elif card.value == 16:
        return 34  # 34 if red, 35 if black
    elif card.value == 5:
        if card.suit < 4:
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
        # if restricted_suits:
        #     suit = random.choice(list(filter(lambda suit: suit not in restricted_suits, range(4))))
        # else:
        #     suit = random.choice(range(4))
        return Card(16, 0)
    elif card_index == 35:
        # if restricted_suits:
        #     suit = random.choice(list(filter(lambda suit: suit not in restricted_suits, range(4))))
        # else:
        #     suit = random.choice(range(4))
        return Card(5, 4)
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
    diamonds, clubs, hearts, spades = suit_count(observation['player0hand'])

    if diamonds <= clubs and diamonds <= hearts and diamonds <= spades:
        return 0
    elif clubs <= diamonds and clubs <= hearts and clubs <= spades:
        return 1
    elif hearts <= diamonds and hearts <= clubs and hearts <= spades:
        return 2
    elif spades <= diamonds and spades <= clubs and spades <= hearts:
        return 3

def most_common_suit_in_hand(observation: OrderedDict) -> int:
    diamonds, clubs, hearts, spades = suit_count(observation['player0hand'])

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
    return suit_count(observation['player0hand'])[wildsuit]

def want_to_win(observation: OrderedDict):
    '''
    This should eventually be learned by our model but a rule based approach will do for now.
    This rule based approach returns True if the player wants to win, and False if they want to take
    '''
    if observation['player0desired'] != observation['player0taken']:
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
    diamonds, clubs, hearts, spades = suit_count(observation['player0hand'])
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
    if observation["in_play"][-1] != 44:
        return True
    elif observation["jokers_remaining"] == 1:
        return True
    else:
        return False

def beatable_obs(observation):
    return False
        
def cards_in_hand(observation):
    hand = observation["player0hand"]
    return len(hand)

def obs_to_string(observation):
    obs_string = ""

    card_ints = observation["in_play"]
    wildsuit = observation["wild_suit"]
    hand0_ints, desired0, taken0 = observation["player0hand"], observation["player0desired"], observation["player0taken"]
    desired1, taken1 = observation["player1desired"], observation["player1taken"]
    desired2, taken2 = observation["player2desired"], observation["player2taken"]
    desired3, taken3 = observation["player3desired"], observation["player3taken"]
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
    hand = truncate_at_first_none(list(map(lambda card_int: int_to_card(card_int), observation["player0hand"])))

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
    return suit in list(map(lambda card: card.suit if card else -1, hand))

def has_first_suit(observation):
    '''
    Returns True if Player 0's hand contains the first suit
    '''
    return contains_suit(first_suit_index(observation), truncate_at_first_none(list(map(lambda card_int: int_to_card(card_int), observation["player0hand"]))))

def have_wild_suit(observation, number = 0, cards = []):
    '''
    Returns True if Player 0's hand contains the wildsuit
    '''
    wildsuit = get_wildsuit(observation)
    if number == 0:
        player_cards = observation["player0hand"]
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
        if card and card.suit == suit and card.value >= max:
            max = card.value
            highest = i
    
    if max:
        return highest
    else:
        return None

def index_of_latest_base_joker(cards):
    index = -1
    for i, card in enumerate(cards):
        if card and card.value == 16:
            index = i
    if index == -1:
        for i, card in enumerate(cards):
            if card and card.value == 15:
                index = i
    return index

def get_transformed_joker(cards):
    for card in cards:
        if card and card.value == 6 and cards.count(card) > 1:
            return card

def indexes_of_transformed_jokers(cards):
    indexes = []
    for i, card in enumerate(cards):
        if card and card.value == 6 and cards.count(card) > 1:
            indexes.append(i)
    return indexes

def adjust_for_order(hand, first):
    playable_hand = []
    if first:
        for card in hand:
            if card.value == 16:
                for i in range(4):
                    playable_hand.append(Card(15, i))
                    playable_hand.append(Card(5, i))
            else:
                playable_hand.append(card)
    else:
        for card in hand:
            if card.value == 16:
                playable_hand.append(Card(5, 4))
                playable_hand.append(Card(16, 0))
            else:
                playable_hand.append(card)

    return playable_hand

def winner(observation):
    wildsuit = observation["wild_suit"]
    cards = [int_to_card(card_int) for card_int in observation["in_play"]]

    if cards.count(None) == 2:
        return 0
    
    if cards.count(None) == 3:
        return None
    
    first_suit = observation["first_suit"] # something wrong here


    if 16 in [card.value if card else -1 for card in cards]: # joker was played
        return index_of_latest_base_joker(cards)
    elif 15 in [card.value if card else -1 for card in cards]: # joker (vishi) was played
        return index_of_latest_base_joker(cards)
    elif (5 in [card.value if card else -1 for card in cards]): # joker (waigos) was played
        for card in cards:
            if card and card.suit == cards[0].suit and card.value > 5:
                return cards.index(card)
        return 0
    else:
        transformed_joker = get_transformed_joker(cards)
        if transformed_joker:
            indexes_of_indenticals = indexes_of_transformed_jokers(cards)
            is_transformed_suit = [True if card and card.suit == cards[indexes_of_indenticals[0]].suit else False for card in cards]
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
                index_of_highest = index_of_highest_of_suit(cards, first_suit)
                return index_of_highest
            
def flatten_obs(obs):
    return {'dealt': obs['dealt'],
            'wild_suit': obs['wild_suit'],
            'player0hand_0': obs['player0hand'][0],
            'player0hand_1': obs['player0hand'][1],
            'player0hand_2': obs['player0hand'][2],
            'player0hand_3': obs['player0hand'][3],
            'player0hand_4': obs['player0hand'][4],
            'player0hand_5': obs['player0hand'][5],
            'player0hand_6': obs['player0hand'][6],
            'player0hand_7': obs['player0hand'][7],
            'player0hand_8': obs['player0hand'][8],
            'player0desired': obs['player0desired'],
            'player0taken': obs['player0taken'],
            'player1taken': obs['player1taken'],
            'player1desired': obs['player1desired'],
            'player2taken': obs['player2taken'],
            'player2desired': obs['player2desired'],
            'player3taken': obs['player3taken'],
            'player3desired': obs['player3desired'],
            'jokers_remaining': obs['jokers_remaining'],
            'first_to_play': obs['first_to_play'],
            'first_suit': obs['first_suit'],
            'in_play_0': obs['in_play'][0] if len(obs['in_play']) > 0 else 44,
            'in_play_1': obs['in_play'][1] if len(obs['in_play']) > 1 else 44,
            'in_play_2': obs['in_play'][2] if len(obs['in_play']) > 2 else 44,
            'dealer': obs['dealer'],
            }

def clean_data_for_call_decision_training(call_data):

    # Assuming your data is stored in a variable named data
    data = call_data

    # Create an empty list to store the transformed data
    transformed_data = []

    for item in data:
        # Clone the dictionary to not modify the original data
        clone = item[0].copy()
        # Add the last number of each entry as a new key-value pair to the dictionary
        clone['result'] = item[1]
        # Append the transformed dictionary to the list
        transformed_data.append(clone)

    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(transformed_data)

    # Handling 'in_play'
    in_play_df = pd.DataFrame(df['in_play'].to_list(), 
                            columns=['in_play' + str(i) for i in range(1, len(df['in_play'].iloc[0])+1)])
    df = pd.concat([df.drop('in_play', axis=1), in_play_df], axis=1)

    # Handling 'player0hand'
    player0hand_df = pd.DataFrame(df['hand'].to_list(), 
                                columns=['hand' + str(i) for i in range(1, len(df['hand'].iloc[0])+1)])
    df = pd.concat([df.drop('hand', axis=1), player0hand_df], axis=1)

    columns_to_keep = ['dealt', 'desired', 'first_to_play', 'dealer', 'wild_suit', 'player0desired',
                    'player1desired', 'player2desired',
                    'player3desired', 'result',  'hand1', 'hand2', 'hand3', 'hand4', 
                    'hand5', 'hand6', 'hand7', 'hand8', 'hand9', 'deciding_player']

    df = df[df['result'] != 0]
    df = df.loc[:, columns_to_keep]

    return df
