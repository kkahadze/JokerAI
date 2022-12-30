import random

def random_call(observation):
    dealt = observation["dealt"]
    return random.randint(0, dealt)

def get_complement(observation):
    dealt = observation["dealt"]
    called = get_called(observation)
    return dealt - called

def get_called(observation):
    return sum([player['desired'] if player['desired'] != -1 else 0 for player in observation['players']])