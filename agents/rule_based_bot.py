from src.utils import first_to_play, want_to_win, choose_suit_for_highest, choose_suit_for_take, playable

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

    def choose_card(self, observation):
        playable = playable(observation)

        if len(playable) == 1:
            return playable[0]
        else:
            hand = observation["players"]["0"]["hand"]
            
            
                    