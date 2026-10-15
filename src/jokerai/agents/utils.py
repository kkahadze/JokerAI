"""Bidding helpers shared by baseline policies."""

import random


def random_call(observation, rng=None):
    return (rng or random).randint(0, observation["dealt"])


def get_called(observation):
    return sum(max(0, observation[f"player{i}desired"]) for i in range(4))


def last_to_call(observation, player_num=0):
    return all(observation[f"player{i}desired"] != -1 for i in range(4) if i != player_num)


def get_complement(observation, player_num=0):
    return (
        observation["dealt"] - get_called(observation)
        if last_to_call(observation, player_num)
        else None
    )


# Preserve the historical misspelling for callers migrating their imports.
get_compliment = get_complement
