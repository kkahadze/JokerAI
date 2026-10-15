# Migrating to 0.1

This is an explicit breaking cleanup of the unpublished 0.0.1 API.

| Before | Now |
| --- | --- |
| `from src.env import JokerEnv` | `from jokerai import JokerEnv` |
| `from src.game import Game` | `from jokerai import Game` |
| `from agents.rule_based_bot import RuleBasedAgent` | `from jokerai.agents import RuleBasedAgent` |
| `obs = env.reset()` | `obs, info = env.reset(seed=42)` |
| `obs, reward, done, info = env.step(action)` | `obs, reward, terminated, truncated, info = env.step(action)` |
| Removing seat zero's card before `step()` | Submit one legal action; the engine removes the card |
| Random suits during action decoding | Deterministic action decoding |
| Variable hand length / inconsistent empty codes | Hand length 9, trick length 3, padding 44 |
| Process-global `random.seed(...)` | Per-environment `reset(seed=...)` |
| Reward 1 while ahead, even mid-game | Reward 1 only for terminal first place (ties included); otherwise 0 |

Python 3.10+ is required. Gymnasium replaces legacy Gym. Install with `pip install
.` from this repository; do not add `src` to `PYTHONPATH` or rely on the working
directory to import modules.

`Game.reset(seed=...)` returns an observation at seat zero's next decision.
`Game.step(action)` plays seat zero's card, completes exactly one four-card
trick, advances scoring/deals as needed, and plays opponents up to the next
seat-zero decision. `Game.legal_actions()` lists legal integer actions.
`Game.step()` rejects illegal actions with `ValueError` without changing state.
`Game.history` records completed deals, bids, tricks, takers and cumulative scores.

`JokerEnv(bid_policy="rule-based")` selects the heuristic for seat zero's automatic
bids (default: `"random"`). Opponent policies are set independently with
`opponent="random"` or `"rule-based"`. The CLI uses `--agent` for both seat zero's
bids and card decisions.

`JokerEnv` keeps an in-range unavailable action nonmutating and returns reward −1
and `info['invalid_action'] = True`. This supports unmasked RL algorithms without
crashing. Such self-loops do not terminate: use `info['action_mask']`, or add a
Gymnasium `TimeLimit` wrapper if evaluating an unmasked policy. Out-of-range or
noninteger actions raise `ValueError`; stepping before reset or after termination
raises `RuntimeError`. There is no internal truncation limit.

Agents expose nonmutating `choose_action(observation)` and `choose_card(observation)`
for seat zero. Inside the game, each seat's `play(observation)` uses that agent's
own hand. `call(observation)` selects a legal bid and updates the agent's desired
trick count. `RuleBasedAgent(number=0)` is a deterministic heuristic, not an
evaluated claim of strong play. `RandomCallerRandomPlayer(number=0, rng=...)`
accepts a local Python `random.Random` instance. Opponent RNGs inside a game are
controlled by the game's seed.

Obsolete unused utility heuristics and stub functions were removed. Import card
encoding from `jokerai.rules` (also re-exported by `jokerai.utils`). Do not encode
a low suited Joker lead with the default `card_to_int` call: use `first=True`, or
prefer the integer action from `choose_action` directly.
