"""Joker engine, baseline policies, and Gymnasium environment."""

from gymnasium.envs.registration import register

from jokerai.env import JokerEnv
from jokerai.game import Game

register(id="JokerAI-v0", entry_point="jokerai.env:JokerEnv")

__all__ = ["Game", "JokerEnv"]
