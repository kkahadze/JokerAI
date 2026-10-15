import random

import pytest

from jokerai.agents import RandomCallerRandomPlayer, RuleBasedAgent
from jokerai.agents.utils import get_called, get_complement, last_to_call, random_call
from jokerai.card import Card


def observation():
    return {
        "dealt": 4,
        "in_play": [2, 44, 44],
        "wild_suit": 1,
        "player0hand": [6, 31, 34] + [44] * 6,
        **{f"player{i}desired": value for i, value in enumerate([-1, 1, 0, 2])},
        **{f"player{i}taken": 0 for i in range(4)},
    }


def test_call_helpers_sum_values_and_recognize_any_last_seat():
    obs = observation()
    assert get_called(obs) == 3
    assert last_to_call(obs)
    assert get_complement(obs) == 1
    obs["player0desired"], obs["player2desired"] = 1, -1
    assert last_to_call(obs, 2)
    assert get_complement(obs, 2) == 0
    assert not last_to_call(obs, 0)
    for i in range(1, 10):
        assert 0 <= random_call({"dealt": i}, random.Random(i)) <= i


@pytest.mark.parametrize("agent_type", [RandomCallerRandomPlayer, RuleBasedAgent])
def test_agents_are_initialized_and_decisions_do_not_remove_cards(agent_type):
    agent = agent_type(0, rng=random.Random(1))
    agent.hand = [Card(8, 0), Card(14, 1), Card(16, 0)]
    before = list(agent.hand)
    obs = observation()
    assert agent.call(obs) in (0, 2, 3)
    obs["player0desired"] = agent.desired
    assert agent.choose_action(obs) in (6, 34, 35)
    assert agent.play(obs) is not None
    assert agent.hand == before


def test_rule_agent_tries_to_win_then_avoids_extra_tricks():
    agent = RuleBasedAgent(0)
    obs = observation()
    obs["player0desired"] = 1
    assert agent.choose_card(obs) == Card(8, 0)
    assert agent.choose_action(obs) == 6  # cheapest card beating the led seven
    obs["player0taken"] = 1
    assert agent.choose_action(obs) == 35  # discard the Joker low


def test_rule_agent_leads_and_single_option_are_total():
    agent = RuleBasedAgent(0)
    obs = observation()
    obs["in_play"] = [44, 44, 44]
    obs["player0desired"] = 2
    assert agent.choose_action(obs) in range(40, 44)
    assert agent.choose_action(obs, [6]) == 6
    with pytest.raises(ValueError):
        agent.choose_action(obs, [])
