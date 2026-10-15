import copy

import gymnasium as gym
import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env

import jokerai  # noqa: F401 -- registration
from jokerai.env import JokerEnv


def test_official_gymnasium_contract_checker():
    check_env(JokerEnv(render_mode="ansi"), skip_render_check=True)


@pytest.mark.parametrize("only_nines", [False, True])
@pytest.mark.parametrize("opponent", ["random", "rule-based"])
@pytest.mark.parametrize("bid_policy", ["random", "rule-based"])
def test_every_observation_and_terminal_mask_in_complete_episode(only_nines, opponent, bid_policy):
    env = JokerEnv(only_nines=only_nines, opponent=opponent, bid_policy=bid_policy)
    obs, info = env.reset(seed=8)
    env.action_space.seed(9)
    steps = 0
    while True:
        assert env.observation_space.contains(obs)
        assert obs["player0hand"].shape == (9,)
        assert info["action_mask"].shape == (44,)
        action = env.action_space.sample(mask=info["action_mask"])
        previous = copy.deepcopy(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        steps += 1
        assert not truncated
        assert env.observation_space.contains(obs)
        assert obs is not previous
        if terminated:
            assert steps == 144
            assert reward in (0.0, 1.0)
            assert not info["action_mask"].any()
            assert (obs["player0hand"] == 44).all()
            assert obs["dealt"] == 0
            with pytest.raises(RuntimeError):
                env.step(0)
            break
        assert reward == 0.0
        assert info["action_mask"].any()
    env.close()


def test_same_seed_same_actions_same_trajectory_and_no_aliasing():
    a, b = JokerEnv(opponent="rule-based"), JokerEnv(opponent="rule-based")
    obs_a, info_a = a.reset(seed=91)
    obs_b, info_b = b.reset(seed=91)
    first = copy.deepcopy(obs_a)
    original = obs_a
    for _ in range(144):
        for key in obs_a:
            np.testing.assert_equal(obs_a[key], obs_b[key])
        np.testing.assert_array_equal(info_a["action_mask"], info_b["action_mask"])
        action = int(np.flatnonzero(info_a["action_mask"])[0])
        obs_a, reward_a, term_a, trunc_a, info_a = a.step(action)
        obs_b, reward_b, term_b, trunc_b, info_b = b.step(action)
        assert (reward_a, term_a, trunc_a) == (reward_b, term_b, trunc_b)
    for key in first:
        np.testing.assert_equal(original[key], first[key])
    assert info_a["scores"] == info_b["scores"]
    a.reset(seed=91)
    for key in first:
        np.testing.assert_equal(a.game.to_obs()[key], first[key])


def test_unavailable_action_penalty_is_nonmutating_and_masks_agree():
    env = JokerEnv()
    obs, info = env.reset(seed=0)
    bad = int(np.flatnonzero(info["action_mask"] == 0)[0])
    rng_before = env.game.rng.getstate()
    result, reward, terminated, truncated, new_info = env.step(bad)
    for key in obs:
        np.testing.assert_equal(obs[key], result[key])
    assert reward == -1.0 and not terminated and not truncated
    assert new_info["invalid_action"]
    np.testing.assert_array_equal(info["action_mask"], new_info["action_mask"])
    assert env.game.rng.getstate() == rng_before


@pytest.mark.parametrize("action", [-1, 44, True, np.bool_(True), 0.5, "0"])
def test_out_of_space_actions_raise(action):
    env = JokerEnv()
    env.reset(seed=0)
    with pytest.raises(ValueError):
        env.step(action)


def test_registration_rendering_and_lifecycle():
    with gym.make("JokerAI-v0", render_mode="ansi") as env:
        with pytest.raises(gym.error.ResetNeeded):
            env.step(0)
        obs, info = env.reset(seed=1)
        assert env.observation_space.contains(obs)
        assert "Scores:" in env.render()
    with pytest.raises(ValueError):
        JokerEnv(opponent="unfinished")
    with pytest.raises(ValueError):
        JokerEnv(bid_policy="unfinished")
    with pytest.raises(ValueError):
        JokerEnv(render_mode="rgb_array")
    with pytest.raises(ValueError):
        JokerEnv().reset(options={"ignored": True})
