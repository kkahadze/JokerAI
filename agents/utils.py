import random

def random_call(observation):
    dealt = observation["dealt"]
    return random.randint(0, dealt)

def get_complement(observation):
    dealt = observation["dealt"]
    if last_to_go(observation):
        called = get_called(observation)
        return dealt - called
    else:
        return None

def get_called(observation):
    return sum([player['desired'] if player['desired'] != -1 else 0 for player in observation['players']])
    
def last_to_go(observation):
    return 36 not in observation['in_play']