"""Run after `pip install .`: use the legal mask to sample valid actions."""

import gymnasium as gym

import jokerai  # noqa: F401 -- registers JokerAI-v0

with gym.make("JokerAI-v0", opponent="rule-based") as env:
    obs, info = env.reset(seed=42)
    env.action_space.seed(42)
    while True:
        action = env.action_space.sample(mask=info["action_mask"])
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            print({"reward": reward, "scores": info["scores"]})
            break
