"""Reproducible baseline evaluation, without model files or notebook setup."""

import argparse
import json
import random

from jokerai.agents import RandomCallerRandomPlayer, RuleBasedAgent
from jokerai.env import JokerEnv


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--agent", choices=["random", "rule-based"], default="rule-based")
    parser.add_argument("--opponent", choices=["random", "rule-based"], default="random")
    parser.add_argument("--only-nines", action="store_true")
    args = parser.parse_args(argv)
    if args.games < 1:
        parser.error("--games must be positive")
    if args.seed < 0:
        parser.error("--seed must be nonnegative")
    agent_type = RuleBasedAgent if args.agent == "rule-based" else RandomCallerRandomPlayer
    agent = agent_type(0, rng=random.Random(args.seed))
    results = []
    with JokerEnv(opponent=args.opponent, bid_policy=args.agent, only_nines=args.only_nines) as env:
        for index in range(args.games):
            obs, info = env.reset(seed=args.seed + index)
            done = False
            steps = 0
            while not done:
                action = agent.choose_action(obs)
                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                steps += 1
            results.append(
                {
                    "seed": args.seed + index,
                    "scores": info["scores"],
                    "win": bool(reward),
                    "steps": steps,
                }
            )
    print(
        json.dumps(
            {
                "agent": args.agent,
                "opponent": args.opponent,
                "games": results,
                "wins": sum(game["win"] for game in results),
            },
            indent=2,
        )
    )
