# JokerAI

A reproducible Joker card-game engine, Gymnasium environment, and two usable
baseline agents: random and rule-based. One environment step is one seat-zero
card decision followed by the remaining opponents' moves for that trick.

## Install

Requires Python 3.10 or newer. Install from this repository:

```sh
git clone --depth 1 https://github.com/kkahadze/JokerAI.git
cd JokerAI
python -m venv .venv
source .venv/bin/activate
python -m pip install .
```

On Windows, activate with `.venv\Scripts\activate`. Runtime dependencies are
Gymnasium and NumPy; no model download, API key, GPU or notebook is needed.

## Run a reproducible baseline

```sh
jokerai --games 10 --seed 42 --agent rule-based --opponent random
# Equivalent:
python -m jokerai --games 10 --seed 42
```

The command prints JSON with seeds, scores, wins and step counts. The rule-based
policy estimates a bid from its hand and tries to take or avoid tricks according
to that bid. It is a simple heuristic, not a pretrained or strength-rated model.
Both agents use the same legal-action rules as the environment.

## Use the environment

```python
from jokerai import JokerEnv

with JokerEnv(opponent="rule-based") as env:
    observation, info = env.reset(seed=42)
    env.action_space.seed(42)
    while True:
        action = env.action_space.sample(mask=info["action_mask"])
        observation, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            print(reward, info["scores"])
            break
```

Importing `jokerai` also registers `gymnasium.make("JokerAI-v0")`. See the runnable
[rollout example](examples/rollout.py), [rules and observation contract](docs/rules-and-observations.md),
and [0.1 migration notes](docs/api-migration.md). Observations have fixed shapes,
and reset seeds control deals, calls and opponents without changing global RNG state.

This implements the original project's Joker declarations and scoring with a
consistent 44-action interface. Nine-card deals have no trump; section bonuses
and choosing trump are not implemented. Seat zero's bid is automatic; this
environment trains card play, not bidding. Set `bid_policy="rule-based"` to use
heuristic bids for seat zero; its default is random. The CLI uses `--agent` for
both bids and card decisions. Use the action mask to avoid invalid
move penalties. A full episode contains 144 valid card decisions.

## Develop and verify

```sh
python -m pip install -e '.[dev]'
python -m pytest
ruff check src tests examples
ruff format --check src tests examples
python -m build
```

Tests cover retained card/player/winner fixtures, every action encoding, legal
moves and Joker declarations, bidding order, all four trick leaders, observation
bounds including termination, local seeding, CLI reproducibility, and complete
games using both agent types. Gymnasium's official environment checker is part
of the suite. CI tests Python 3.10, 3.12 and 3.14, checks an installed wheel from
outside the source tree, and uploads wheel/sdist artifacts.

The implementation lives under `src/jokerai/`: `rules.py` is shared by the
engine and agents, `game.py` owns physical card removal and scoring, and `env.py`
adapts it to the [Gymnasium API](https://gymnasium.farama.org/api/env/).

## Historical research

The old notebooks remain under `notebooks/`, explicitly marked as historical and
with stale outputs cleared. Obsolete entry points, incompatible simulation/UI
code, and the unused 59.5 MB pickled model were removed from the current tree.
[Recovery instructions and the original checksum](docs/legacy-artifacts.md)
preserve access through Git history; history was not rewritten. A full clone
still includes the old binary, so the install example uses a shallow clone.
