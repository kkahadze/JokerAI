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
    return sum([player['desired'] if player['desired'] != -1 else 0 for player in observation['players'].values()])
    
def last_to_call(observation, player_num = 0):
    for i, player in enumerate(observation['players'].values()):
        if player['desired'] == -1 and player_num != i:
            return False
    return True
