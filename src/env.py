import gym
from gym import spaces
from src.game import Game
import numpy as np

class JokerEnv(gym.Env):
    metadata = {}

    def __init__(self):
        # Observations are dictionaries containing the player's hand
        self.observation_space = spaces.Dict(
            {
                # all can be any card or no card (meaning that the current player is the first to play)
                "in_play": spaces.MultiDiscrete([47, 47, 47]), # 0-43, 44 = no card
                "wild_suit": spaces.Discrete(5), # 0-4, 4 = no wild suit
                # "wild_value": spaces.Discrete(10), # 0-9
                "player0hand": spaces.MultiDiscrete([35, 36, 36, 36, 36, 36, 36, 36, 36]), # 0-35, 36 = no card
                "player0desired": spaces.Discrete(11), # 0 - 9
                "player0taken": spaces.Discrete(10), # 0-9

                "player1taken": spaces.Discrete(10), # 0-9
                "player1desired": spaces.Discrete(11), # 0 - 9

                "player2taken": spaces.Discrete(10), # 0-9
                "player2desired": spaces.Discrete(11), # 0 - 9

                "player3taken": spaces.Discrete(10), # 0-9
                "player3desired": spaces.Discrete(11), # 0 - 9

                "jokers_remaining": spaces.Discrete(3), # 0-2
                "dealt": spaces.Discrete(10), # 0-9
                # "gone": spaces.MultiBinary(36)
                # "scores": spaces.MultiDiscrete([10, 10, 10, 10]), # others scores (who does it benefit to hurt)
                # "streak": spaces.MultiBinary(4) # premia 
            }
        )
        
        # WRONG
        # Actions represent the card that a player chooses to play.
        # SUIT: DIAMONDS    CLUBS   HEARTS    SPADES
        # VALUES
        # 6:        0                 1         
        # 7:        2         3       4         5
        # 8:        6         7       8         9
        # 9:        10        11      12        13
        # 10:       14        15      16        17
        # JACK:     18        19      20        21
        # QUEEN:    22        23      24        25
        # KING:     26        27      28        29
        # ACE:      30        31      32        33
        
        # Joker Regular:          34
        # Joker Nizhe:            35
                                    
        #                          SUIT:     DIAMONDS    CLUBS   HEARTS    SPADES
        #             Values:              
        # Joker Take(წაიღოს):                  36        37      38        39       
        # Joker Highest(ვიში):                 40        41      42        43
        
        self.action_space = spaces.Discrete(44)

    def step(self, action):
        # Execute one time step within the environment
        self.game.step(action)
        obs = self.game.to_obs()
        reward = 1 if self.game.highest_score_player() == 0 else 0
        done = self.game.round == 5
        return obs, reward, self.game.done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.game = Game()
        self.game.reset()
        return self.game.to_obs()
