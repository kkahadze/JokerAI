import random

import numpy as np
import pytest

from jokerai.agents import RandomCallerRandomPlayer, RuleBasedAgent
from jokerai.card import Card
from jokerai.game import Game


def test_independent_games_and_caller_owned_players():
    players = [RandomCallerRandomPlayer(i) for i in range(4)]
    a, b = Game(players), Game()
    a.reset(seed=3)
    assert all(not p.hand for p in players)
    assert all(not p.hand for p in b.players)
    a.players[0].score = 123
    a.reset(seed=3)
    assert all(p.score == 0 for p in a.players)


@pytest.mark.parametrize("leader", range(4))
def test_all_seats_play_exactly_once_after_seat_zero(leader):
    game = Game(only_nines=True)
    game.reset_vars(seed=1)
    game.deal()
    game.get_calls()
    game.first_to_play = leader
    game.started = True
    game.post_plays()
    assert len(game.in_play) == (4 - leader) % 4
    before = sum(len(p.hand) for p in game.players)
    game.step(game.legal_actions()[0])
    assert len(game.tricks[0]["cards"]) == 4
    assert sum(p.taken for p in game.players) == 1
    assert len(game.players[0].hand) == 8
    assert sum(len(p.hand) for p in game.players) <= before - 1


@pytest.mark.parametrize("only_nines", [False, True])
@pytest.mark.parametrize("agent_type", [RandomCallerRandomPlayer, RuleBasedAgent])
def test_fifty_complete_games_conserve_cards_tricks_and_scores(only_nines, agent_type):
    for seed in range(50):
        game = Game([agent_type(i) for i in range(4)], only_nines=only_nines)
        game.reset(seed=seed)
        steps = 0
        while not game.done:
            hand_before = tuple(game.players[0].hand)
            action = game.players[0].choose_action(game.to_obs())
            assert tuple(game.players[0].hand) == hand_before, "agents must not remove cards"
            assert action in game.legal_actions()
            game.step(action)
            steps += 1
            assert steps <= 144
        assert steps == 144
        schedule = [n for section in game.deal_amounts for n in section]
        assert [h["dealt"] for h in game.history] == schedule
        expected_scores = [0] * 4
        previous_dealer = None
        for hand in game.history:
            n = hand["dealt"]
            assert len(hand["tricks"]) == n
            assert sum(hand["taken"]) == n
            assert sum(hand["bids"]) != n
            if previous_dealer is not None:
                assert hand["dealer"] == (previous_dealer + 1) % 4
            previous_dealer = hand["dealer"]
            assert hand["tricks"][0]["leader"] == (hand["dealer"] + 1) % 4
            for prev, current in zip(hand["tricks"], hand["tricks"][1:]):
                assert current["leader"] == prev["winner"]
            cards = [c for trick in hand["tricks"] for c in trick["cards"]]
            assert len(cards) == 4 * n
            ordinary = [c for c in cards if not c.is_joker()]
            assert len(set(ordinary)) == len(ordinary)
            assert sum(c.is_joker() for c in cards) <= 2
            for i, (bid, taken) in enumerate(zip(hand["bids"], hand["taken"])):
                points = (
                    -200
                    if taken == 0 and bid > 0
                    else (
                        taken * 100
                        if taken == bid == n
                        else taken * 50 + 50
                        if bid == taken
                        else taken * 10
                    )
                )
                expected_scores[i] += points
            assert hand["scores"] == expected_scores
        assert [p.score for p in game.players] == expected_scores
        assert all(not p.hand for p in game.players)
        assert game.legal_actions() == []
        assert game.get_num_to_deal() == 0
        with pytest.raises(RuntimeError):
            game.step(0)


@pytest.mark.parametrize("dealer", range(4))
def test_bidding_uses_seat_order_and_forbids_dealer_complement(dealer):
    game = Game()
    game.reset_vars(seed=2)
    game.dealer = dealer
    game.deal()
    order = []
    for player in game.players:
        original = player.call

        def call(obs, player=player, original=original):
            order.append(player.number)
            return original(obs)

        player.call = call
    bids = game.get_calls()
    assert order == [(dealer + offset) % 4 for offset in range(1, 5)]
    assert all(0 <= bid <= 1 for bid in bids)
    assert sum(bids) != 1


def test_trump_clears_in_nine_card_deal_and_jokers_are_never_trump():
    game = Game()
    game.reset_vars(seed=4)
    game.wild_suit = 2
    game.round = 2
    game.deal()
    assert game.wild_suit == 4
    assert game.jokers_remaining == 2
    for seed in range(100):
        game.reset(seed=seed)
        if game.wild_card.is_joker():
            assert game.wild_suit == 4
            break
    else:
        pytest.fail("fixture did not produce a turned-up Joker")


@pytest.mark.parametrize("action", [-1, 44, 1.5, True, "1"])
def test_bad_actions_do_not_mutate_engine(action):
    game = Game()
    game.reset(seed=2)
    before = repr(game.to_obs()), game.rng.getstate(), tuple(game.players[0].hand)
    with pytest.raises(ValueError):
        game.step(action)
    assert before == (repr(game.to_obs()), game.rng.getstate(), tuple(game.players[0].hand))


def test_out_of_turn_unavailable_action_does_not_mutate_engine():
    game = Game()
    game.reset(seed=4)
    action = next(a for a in range(44) if a not in game.legal_actions())
    before = repr(game.to_obs())
    with pytest.raises(ValueError):
        game.step(action)
    assert repr(game.to_obs()) == before


def test_two_jokers_consume_one_physical_card_per_declaration():
    game = Game()
    game.reset_vars(seed=2)
    game.players[0].hand = [Card(16, 0), Card(16, 1)]
    game.jokers_remaining = 2
    game._play_action(0, 40)
    assert len(game.players[0].hand) == 1
    assert game.jokers_remaining == 1
    game._play_action(0, 34)
    assert game.players[0].hand == []
    assert game.jokers_remaining == 0


def test_global_random_state_is_untouched_and_seeded_games_match():
    random.seed(11)
    before = random.getstate()
    a, b = Game(), Game()
    a.reset(seed=17)
    b.reset(seed=17)
    for _ in range(144):
        for key in a.to_obs():
            np.testing.assert_equal(a.to_obs()[key], b.to_obs()[key])
        action = a.legal_actions()[0]
        a.step(action)
        b.step(action)
    assert random.getstate() == before


def test_reset_required_and_seat_validation():
    with pytest.raises(RuntimeError):
        Game().step(0)
    with pytest.raises(ValueError):
        Game([RandomCallerRandomPlayer(0)] * 4)
