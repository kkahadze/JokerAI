
class RuleBasedAgent():
    def __init__(self, env):
        self.env = env

    # SUIT: DIAMONDS    CLUBS   HEARTS    SPADES
    # VALUES
    # 6:        0         1       2         3
    # 7:        4         5       6         7
    # 8:        8         9       10        11
    # 9:        12        13      14        15
    # 10:       16        17      18        19
    # JACK:     20        21      22        23
    # QUEEN:    24        25      26        27
    # KING:     28        29      30        31
    # ACE:      32        33      34        35
        
    def act(self, observation):
        unimplemented()

    def choose_how_to_play_joker(self, observation):
        '''
        Returns the best way to play the joker given the current observation, 
        0 - 3 = ვიში/Highest (Diamonds to Spades), 
        4-7 = წაიღოს/Take (Diamonds to Spades), 
        8 = Play Default
        9 = Play Under
        '''

        # Variables that the optimal play of a Joker depends on

        if first_to_play(observation):
            if want_to_win(observation):
                return 4 + choose_suit_for_highest()
            else:
                return choose_suit_for_take()
        else: # second, third or fourth to play
            if want_to_win(observation):
                return 8
            else:
                return 9

def want_to_win(observation):
    # This should eventually be learned by our model but a rule based approach will do for now
    if observation.players[0].desired != observation.players[0].taken:
        return True
    else:
        return False

def first_to_play(observation):
    if observation.in_play[0] == 36:
        return True
    else:
        return False

def choose_suit_for_highest(observation):
    # This should also eventually be learned, for now, the choice of suit is based on 

    if additional_hands_desired > 1 and wildcards_in_hand <= additional_hands_desired + 1:
        return 
    
def get_wildsuit(observation):
    return observation.wild_suit