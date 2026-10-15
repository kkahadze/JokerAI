"""Gymnasium contract for seat zero against three seeded local opponents."""

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from jokerai.agents import RandomCallerRandomPlayer, RuleBasedAgent
from jokerai.game import Game
from jokerai.rules import ACTION_COUNT, EMPTY


class JokerEnv(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 1}

    def __init__(self, only_nines=False, opponent="random", bid_policy="random", render_mode=None):
        if opponent not in ("random", "rule-based"):
            raise ValueError("opponent must be 'random' or 'rule-based'.")
        if bid_policy not in ("random", "rule-based"):
            raise ValueError("bid_policy must be random or rule-based.")
        if render_mode not in (None, "ansi"):
            raise ValueError("Only ansi rendering is supported.")
        self.render_mode = render_mode
        self.only_nines = only_nines
        self.opponent = opponent
        self.bid_policy = bid_policy
        fields = {
            "in_play": spaces.MultiDiscrete([EMPTY + 1] * 3),
            "player0hand": spaces.MultiDiscrete([EMPTY + 1] * 9),
            "wild_suit": spaces.Discrete(5),
            "first_suit": spaces.Discrete(5),
            "first_to_play": spaces.Discrete(4),
            "dealer": spaces.Discrete(4),
            "jokers_remaining": spaces.Discrete(3),
            "dealt": spaces.Discrete(10),
            "round": spaces.Discrete(6),
            "play": spaces.Discrete(9),
            "scores": spaces.Box(-100_000, 100_000, (4,), dtype=np.int64),
        }
        for i in range(4):
            fields[f"player{i}taken"] = spaces.Discrete(10)
            fields[f"player{i}desired"] = spaces.Discrete(11, start=-1)
        self.observation_space = spaces.Dict(fields)
        self.action_space = spaces.Discrete(ACTION_COUNT)
        self.game = None

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        if options:
            raise ValueError(
                "No reset options are supported; configure the environment at construction."
            )
        agent_type = RuleBasedAgent if self.opponent == "rule-based" else RandomCallerRandomPlayer
        bidder_type = (
            RuleBasedAgent if self.bid_policy == "rule-based" else RandomCallerRandomPlayer
        )
        players = [bidder_type(0)] + [agent_type(i) for i in range(1, 4)]
        self.game = Game(players, only_nines=self.only_nines)
        # One local stream controls deals, bids and all stochastic opponents.
        obs = self.game.reset(seed=int(self.np_random.integers(0, 2**63)))
        return obs, self._info()

    def _info(self):
        mask = np.zeros(ACTION_COUNT, dtype=np.int8)
        mask[self.game.legal_actions()] = 1
        return {"action_mask": mask, "scores": [p.score for p in self.game.players]}

    def step(self, action):
        if self.game is None or self.game.done:
            raise RuntimeError("Call reset() before stepping a new or completed episode.")
        if not self.action_space.contains(action) or isinstance(action, (bool, np.bool_)):
            raise ValueError("Action must be an integer from 0 through 43.")
        if int(action) not in self.game.legal_actions():
            # Standard RL algorithms may sample an unavailable card. Reject it
            # without mutating the game and return a penalty plus the legal mask.
            return self.game.to_obs(), -1.0, False, False, {**self._info(), "invalid_action": True}
        self.game.step(int(action))
        # Sparse terminal win reward; shared first place counts as a win.
        reward = float(
            self.game.done and self.game.players[0].score == max(p.score for p in self.game.players)
        )
        return self.game.to_obs(), reward, self.game.done, False, self._info()

    def render(self):
        if self.render_mode != "ansi":
            return None
        if self.game is None:
            return "JokerAI: call reset() to start."
        return (
            f"Round {self.game.round}, deal {self.game.play}; trump {self.game.wild_suit}\n"
            f"Your hand: {self.game.players[0].hand}\n"
            f"In play: {self.game.in_play}\n"
            f"Scores: {[p.score for p in self.game.players]}"
        )
