"""Single-agent game engine: one step consumes seat zero's card and a full trick."""

import copy
import random
from numbers import Integral

import numpy as np

from jokerai.agents.random_caller_random_player import RandomCallerRandomPlayer
from jokerai.deck import Deck
from jokerai.rules import EMPTY, card_to_int, consume_card, legal_actions, winner_index


class Game:
    def __init__(self, players_in=None, only_nines=False, seed=None):
        if players_in is None:
            players_in = [RandomCallerRandomPlayer(i) for i in range(4)]
        if len(players_in) != 4 or [p.number for p in players_in] != list(range(4)):
            raise ValueError("Provide four players numbered 0, 1, 2, 3 in seat order.")
        self.players = copy.deepcopy(players_in)
        self.rng = random.Random(seed)
        self.only_nines = only_nines
        self.deal_amounts = (
            [[9] * 4 for _ in range(4)]
            if only_nines
            else [
                list(range(1, 9)),
                [9] * 4,
                list(range(8, 0, -1)),
                [9] * 4,
            ]
        )
        self.deck = Deck(self.rng)
        self.round = self.play = 0
        self.wild_suit = self.first_suit = 4
        self.dealer = self.first_to_play = 0
        self.in_play = []
        self.jokers_remaining = 0
        self.done = False
        self.started = False
        self.history = []

    def reset_vars(self, seed=None):
        if seed is not None:
            self.rng.seed(seed)
        for player in self.players:
            player.reset()
            player.score = 0
            player.rng = self.rng
        self.deck = Deck(self.rng)
        self.round = self.play = 1
        self.first_to_play = self.rng.randrange(4)
        self.dealer = (self.first_to_play - 1) % 4
        self.wild_suit = self.first_suit = 4
        self.in_play = []
        self.jokers_remaining = 0
        self.done = False
        self.started = False
        self.history = []
        self.tricks = []

    def reset(self, seed=None):
        self.reset_vars(seed)
        self.deal()
        self.get_calls()
        self.started = True
        self.post_plays()
        return self.to_obs()

    def get_num_to_deal(self):
        return self.deal_amounts[self.round - 1][self.play - 1] if 1 <= self.round <= 4 else 0

    def deal(self):
        self.deck = Deck(self.rng)
        for player in self.players:
            player.reset()
            self.deck.deal(player.hand, self.get_num_to_deal())
        self.wild_card = self.deck[0] if self.deck else None
        self.wild_suit = (
            self.wild_card.suit if self.wild_card and not self.wild_card.is_joker() else 4
        )
        self.jokers_remaining = sum(card.is_joker() for p in self.players for card in p.hand)
        self.first_to_play = (self.dealer + 1) % 4
        self.reset_play()
        self.tricks = []

    def get_calls(self):
        for player in self.players:
            player.desired = -1
        for offset in range(1, 5):
            number = (self.dealer + offset) % 4
            player = self.players[number]
            allowed = player.legal_bids(self.to_obs())
            bid = player.call(self.to_obs())
            if not isinstance(bid, Integral) or bid not in allowed:
                raise ValueError(f"Player {number} returned an illegal bid.")
            player.desired = int(bid)
        return [p.desired for p in self.players]

    def legal_actions(self, player=0):
        if self.done:
            return []
        return legal_actions(self.players[player].hand, self.in_play, self.wild_suit)

    def _play_action(self, player, action):
        if (
            isinstance(action, bool)
            or not isinstance(action, Integral)
            or action not in self.legal_actions(player)
        ):
            raise ValueError(f"Illegal action {action!r} for player {player}.")
        card = consume_card(self.players[player].hand, int(action))
        if card.is_joker():
            self.jokers_remaining -= 1
        if not self.in_play:
            self.first_suit = card.suit
        self.in_play.append(card)

    def step(self, action):
        if not self.started or self.done:
            raise RuntimeError("Call reset() before stepping a new or completed game.")
        self._play_action(0, action)
        self.pre_plays()
        self.process_hand_results()
        if self.hand_empty():
            self.new_hand()
        if not self.done:
            self.post_plays()
        return self.to_obs()

    def get_plays(self, players):
        for number in players:
            choice = self.players[number].play(self.to_obs())
            self._play_action(number, card_to_int(choice, first=not self.in_play))

    def pre_plays(self):
        # Finish the trick after seat zero, stopping before the original leader.
        self.get_plays(range(1, self.first_to_play if self.first_to_play else 4))

    def post_plays(self):
        if self.first_to_play:
            self.get_plays(range(self.first_to_play, 4))

    def winner(self, cards):
        return winner_index(cards, self.wild_suit)

    def update_take(self):
        if len(self.in_play) != 4:
            raise RuntimeError("A completed trick must contain exactly four cards.")
        winner = (self.first_to_play + self.winner(self.in_play)) % 4
        self.players[winner].add_take()
        return winner

    def process_hand_results(self):
        winner = self.update_take()
        self.tricks.append(
            {"leader": self.first_to_play, "winner": winner, "cards": tuple(self.in_play)}
        )
        self.first_to_play = winner
        self.reset_play()

    def reset_play(self):
        self.in_play = []
        self.first_suit = 4

    def hand_empty(self):
        return not self.players[0].hand

    def update_score(self):
        for player in self.players:
            player.update_score(self.get_num_to_deal())

    def new_hand(self):
        self.update_score()
        self.history.append(
            {
                "dealt": self.get_num_to_deal(),
                "dealer": self.dealer,
                "bids": [p.desired for p in self.players],
                "taken": [p.taken for p in self.players],
                "scores": [p.score for p in self.players],
                "tricks": list(self.tricks),
            }
        )
        self.update_play()
        if not self.done:
            self.deal()
            self.get_calls()

    def update_play(self):
        if self.play == len(self.deal_amounts[self.round - 1]):
            self.round += 1
            self.play = 1
        else:
            self.play += 1
        self.done = self.round == 5
        self.dealer = (self.dealer + 1) % 4

    def is_done(self):
        return self.done

    def highest_score_player(self):
        return max(range(4), key=lambda number: self.players[number].score)

    def to_obs(self):
        hand = [card_to_int(card) for card in self.players[0].hand]
        played = [card_to_int(card, first=(i == 0)) for i, card in enumerate(self.in_play)]
        obs = {
            "dealt": self.get_num_to_deal(),
            "round": self.round,
            "play": self.play,
            "first_to_play": self.first_to_play,
            "dealer": self.dealer,
            "wild_suit": self.wild_suit,
            "first_suit": self.first_suit,
            "jokers_remaining": self.jokers_remaining,
            "in_play": np.array(played + [EMPTY] * (3 - len(played)), dtype=np.int64),
            "player0hand": np.array(hand + [EMPTY] * (9 - len(hand)), dtype=np.int64),
            "scores": np.array([p.score for p in self.players], dtype=np.int64),
        }
        for i, player in enumerate(self.players):
            obs[f"player{i}taken"] = player.taken
            obs[f"player{i}desired"] = player.desired
        return obs

    def print_game(self):
        print(self.to_obs())

    def print_obs(self):
        self.print_game()
