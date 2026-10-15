"""Uniform random legal calls and plays, using an injectable local RNG."""

import random

from jokerai.agents.utils import get_complement
from jokerai.player import Player
from jokerai.rules import EMPTY, int_to_card, legal_actions


class RandomCallerRandomPlayer(Player):
    def __init__(self, number=0, rng=None):
        super().__init__(number)
        self.rng = rng if rng is not None else random.Random()

    def legal_bids(self, observation):
        forbidden = get_complement(observation, self.number)
        return [bid for bid in range(len(self.hand) + 1) if bid != forbidden]

    def call(self, observation):
        self.desired = self.rng.choice(self.legal_bids(observation))
        return self.desired

    def choose_action(self, observation, actions=None):
        if actions is None:
            hand = [int_to_card(int(i)) for i in observation["player0hand"] if i != EMPTY]
            trick = [int_to_card(int(i)) for i in observation["in_play"] if i != EMPTY]
            actions = legal_actions(hand, trick, observation["wild_suit"])
        if not actions:
            raise ValueError("No legal action is available.")
        return self.rng.choice(actions)

    def play(self, observation):
        trick = [int_to_card(int(i)) for i in observation["in_play"] if i != EMPTY]
        actions = legal_actions(self.hand, trick, observation["wild_suit"])
        return int_to_card(self.choose_action(observation, actions))

    def choose_card(self, observation):
        """Choose from the public seat-zero observation, without needing a hand."""
        return int_to_card(self.choose_action(observation))
