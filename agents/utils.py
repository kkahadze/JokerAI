import random

def random_call(observation):
    dealt = observation["dealt"]
    return random.randint(0, dealt)

def get_complement(observation):
    dealt = observation["dealt"]
    if last_to_call(observation):
        called = get_called(observation)
        complement = dealt - called
        return complement
    else:
        return None

def get_called(observation):
    return sum([observation['player{num}desired'.format(player_num)] if observation['player{num}desired'.format(player_num)] != -1 else 0 for player_num in range(4)])
    
def last_to_call(observation, player_num = 0):
    for i in range(4):
        key = "player{num}desired".format(num=i)
        if observation[key] == -1 and i != player_num:
            return False
    return True
