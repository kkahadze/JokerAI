import random

def random_call(observation):
    dealt = observation["dealt"]
    return random.randint(0, dealt)

def get_compliment(observation):
    dealt = observation["dealt"]
    if last_to_call(observation):
        called = get_called(observation)
        complement = dealt - called
        return complement
    else:
        return None

def get_called(observation):
    count = 0
    for number in range(4):
        tag = 'player{num}desired'.format(num=number)
        if observation[tag] != -1:
            count += observation[tag]
    return count
    
def last_to_call(observation, player_num = 0):
    for i in range(4):
        key = "player{num}desired".format(num=i)
        if observation[key] == -1 and i != player_num:
            return False
    return True
