import gym
from gym import spaces
import numpy as np

class JokerEnv(gym.Env):
    metadata = {}

    def __init__(self):
        # Observations are dictionaries containing the player's hand
        self.observation_space = spaces.Dict(
            {
                # all can be any card or no card (meaning that the current player is the first to play)
                "in_play": spaces.MultiDiscrete([37, 37, 37]), 
                "wild_suit": spaces.Discrete(4),
                "players": spaces.Dict(
                    {
                        "0": spaces.Dict(
                            {
                                # the first one is 36 since the player must have at least one card in possesion when taking an action
                                "hand": spaces.MultiDiscrete([36, 37, 37, 37, 37, 37, 37, 37, 37]), 
                                "desired": spaces.Discrete(10), # 0-9
                                "taken": spaces.Discrete(10), # 0-9
                            }        
                        ),
                        "1": spaces.Dict(
                            {
                                "desired": spaces.Discrete(10), # 0-9
                                "taken": spaces.Discrete(10), # 0-9
                            }        
                        ),
                        "2": spaces.Dict(
                            {
                                "desired": spaces.Discrete(10), # 0-9
                                "taken": spaces.Discrete(10), # 0-9
                            }        
                        ),
                        "3": spaces.Dict(
                            {
                                "desired": spaces.Discrete(10), # 0-9
                                "taken": spaces.Discrete(10), # 0-9
                            }        
                        ),
                        
                    }
                )

                "player": spaces.Dict(
                    {
                        # the first one is 36 since the player must have at least one card in possesion when taking an action
                        "hand": spaces.MultiDiscrete([36, 37, 37, 37, 37, 37, 37, 37, 37]), 
                        "desired": spaces.Discrete(10), # 0-9
                        "taken": spaces.Discrete(10), # 0-9
                    }
                ),
                
                # "gone": spaces.MultiBinary(36),
            }
        )

        # Actions represent the card that a player chooses to play.
        self.action_space = spaces.Discrete(36)


