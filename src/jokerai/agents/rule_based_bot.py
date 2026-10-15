"""A deterministic heuristic baseline, not a trained or strength-rated agent."""

from jokerai.agents.random_caller_random_player import RandomCallerRandomPlayer
from jokerai.rules import EMPTY, int_to_card, legal_actions, winner_index


class RuleBasedAgent(RandomCallerRandomPlayer):
    def call(self, observation):
        estimate = round(
            sum(
                1.0
                if card.is_joker()
                else 0.65
                if card.suit == observation["wild_suit"]
                else 0.5
                if card.value == 14
                else 0.1
                for card in self.hand
            )
        )
        self.desired = min(self.legal_bids(observation), key=lambda bid: (abs(bid - estimate), bid))
        return self.desired

    def choose_action(self, observation, actions=None):
        trick = [int_to_card(int(i)) for i in observation["in_play"] if i != EMPTY]
        if actions is None:
            hand = [int_to_card(int(i)) for i in observation["player0hand"] if i != EMPTY]
            actions = legal_actions(hand, trick, observation["wild_suit"])
        if not actions:
            raise ValueError("No legal action is available.")
        trump = observation["wild_suit"]

        def strength(action):
            card = int_to_card(action)
            if action == 35:
                return -1
            return card.value + (100 if card.value in (15, 16) else 20 if card.suit == trump else 0)

        ordered = sorted(actions, key=lambda action: (strength(action), action))
        wants = (
            observation[f"player{self.number}desired"] > observation[f"player{self.number}taken"]
        )
        if not trick:
            return ordered[-1] if wants else ordered[0]
        winners = [
            a for a in ordered if winner_index(trick + [int_to_card(a)], trump) == len(trick)
        ]
        losers = [a for a in ordered if a not in winners]
        return (winners or ordered)[0] if wants else (losers or ordered)[0]
