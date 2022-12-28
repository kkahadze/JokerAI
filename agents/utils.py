import random

def random_call(observation):
    dealt = observation["dealt"]
    return random.randint(0, dealt)