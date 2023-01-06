import random
from src.player import Player
from src.game import Game
from src.card import Card

from agents.random_caller_random_player import RandomCallerRandomPlayer
from src.utils import int_to_card, card_to_int

def test_init():
    game = Game()
    assert game is not None
    assert game.players[0].number == 0 and game.players[1].number == 1 and game.players[2].number == 2 and game.players[3].number == 3
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None

    game = Game([Player(6), Player(7), Player(8), Player(9)])
    assert game is not None
    assert game.players[0].number == 6 and game.players[1].number == 7 and game.players[2].number == 8 and game.players[3].number == 9
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None

def test_reset_vars():
    # The following test makes sure that reset_vars() 
    # resets deck, players, round, play, dealer, wild_suit, jokers_remaining, in_play

    game = Game([Player(6), Player(7), Player(8), Player(9)])
    game.reset_vars()
    assert game is not None
    assert game.players[0].number == 6 and game.players[1].number == 7 and game.players[2].number == 8 and game.players[3].number == 9
    assert game.players[0].hand is not None and game.players[1].hand is not None and game.players[2].hand is not None and game.players[3].hand is not None
    assert game.round == 1
    assert game.play == 1
    assert game.dealer == (game.first_to_play - 1) % 4

def test_get_num_to_deal(): # add more tests
    game = Game(only_nines=True)
    game.reset_vars()
    assert game.get_num_to_deal() == 9

    game = Game() 
    game.reset_vars()
    assert game.get_num_to_deal() == 1

    game = Game()
    game.reset_vars()
    game.round = 2
    assert game.get_num_to_deal() == 9

    game = Game()
    game.reset_vars()
    game.round = 3
    assert game.get_num_to_deal() == 8

    game = Game()
    game.reset_vars()
    game.round = 4
    assert game.get_num_to_deal() == 9

    game = Game()
    game.reset_vars()
    game.round = 1
    game.play = 5
    assert game.get_num_to_deal() == 5

    game = Game()
    game.reset_vars()
    game.round = 1
    game.play = 8
    assert game.get_num_to_deal() == 8

    game = Game()
    game.reset_vars()
    game.round = 3
    game.play = 8
    assert game.get_num_to_deal() == 1

    game = Game()
    game.reset_vars()
    game.round = 3
    game.play = 2
    assert game.get_num_to_deal() == 7

    game = Game(only_nines=True)
    game.reset_vars()
    for round in range(1, 5):
        for play in range(1, 5):
            assert game.get_num_to_deal() == 9

def test_get_calls():
    # This function tests the get_calls() function in game.py to assure that it sets the calls of each player to a valid int corresponding to
    # the type of agent
    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)])
    game.reset_vars()
    game.get_calls()
    for player_num in range(game.first_to_play, game.first_to_play + 4):
        game.deck.deal(game.players[player_num % 4].hand, times = game.get_num_to_deal()) # player num needs to be modded to get the correct players
    calls = game.get_calls()

    assert calls[0] >= 0 and calls[0] <=1
    assert calls[1] >= 0 and calls[1] <=1
    assert calls[2] >= 0 and calls[2] <=1
    assert calls[3] >= 0 and calls[3] <=1

def test_deal():
    # This function tests the deal() function in game.py to assure that it deals the correct number of cards to each player
    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)])
    game.reset_vars()
    game.get_calls()
    game.deal()

    assert len(game.players[0].hand) == 1
    assert len(game.players[1].hand) == 1
    assert len(game.players[2].hand) == 1
    assert len(game.players[3].hand) == 1
    
    assert game.players[0].hand[0] != game.players[1].hand[0] and game.players[0].hand[0] != game.players[2].hand[0] and game.players[0].hand[0] != game.players[3].hand[0]

    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)], only_nines=True)
    game.reset_vars()
    game.get_calls()
    game.deal()

    assert len(game.players[0].hand) == 9
    assert len(game.players[1].hand) == 9
    assert len(game.players[2].hand) == 9
    assert len(game.players[3].hand) == 9

    assert game.players[0].hand[0] != game.players[1].hand[0] and game.players[0].hand[0] != game.players[2].hand[0] and game.players[0].hand[0] != game.players[3].hand[0]

def test_reset_play():
    # This function tests the reset_play() function in game.py to assure that it resets the played variable to an
    #  empty list and resets the first suit
    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)])
    game.reset()
    game.player_0_play(1, first=game.first_to_play == 0)
        
    game.pre_plays()

    if game.is_done():
        return
            
    game.reset_play()

    assert game.in_play == []
    assert game.first_suit == 4

# def test_add_play():
#     # This function tests the add_play() function in game.py to assure that it adds the correct card to the in_play list
#     game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)])
#     game.reset_vars()
#     game.deal()
#     game.first_to_play = 0
#     choice = random.choice(game.players[0].hand)
#     game.add_play(card_to_int(choice), first=True)
#     assert choice in game.in_play
#     assert game.first_suit == choice.suit

def test_is_done():
    # This function tests the is_done() function in game.py to assure that it returns True when the game is done and False when it is not
    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)], only_nines=True)
    game.reset_vars()
    game.deal()
    game.step(1)
    assert game.is_done() == False

    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)], only_nines=True)
    game.reset_vars()
    game.play = 4
    game.round = 4
    game.update_play()
    assert game.is_done() == True

    game = Game([RandomCallerRandomPlayer(0), RandomCallerRandomPlayer(1), RandomCallerRandomPlayer(2), RandomCallerRandomPlayer(3)], only_nines=False)
    game.reset_vars()
    game.play = 8
    game.round = 3
    game.update_play()
    assert game.is_done() == False

    game.round = 4
    game.play = 4
    game.update_play()
    assert game.is_done() == True

def test_winner():
    game = Game()
    game.first_suit = 3
    game.wild_suit = 0
    
    assert game.winner([Card(6, 3), Card(7, 3), Card(6, 2), Card(7, 2)]) == 1
    assert game.winner([Card(6, 3), Card(7, 3), Card(6, 2), Card(9, 1)]) == 1
    assert game.winner([Card(6, 3), Card(7, 3), Card(6, 0), Card(9, 2)]) == 2
    assert game.winner([Card(6, 0), Card(7, 0), Card(16, 1), Card(16, 0)]) == 3
    assert game.winner([Card(12, 3), Card(7, 1), Card(16, 2), Card(9, 1)]) == 2
    
    assert game.winner([Card(15, 3), Card(16, 1), Card(16, 2), Card(9, 0)]) == 2
    assert game.winner([Card(5, 3), Card(6, 3), Card(12, 2), Card(9, 0)]) == 3
    assert game.winner([Card(15, 3), Card(16, 1), Card(12, 2), Card(9, 0)]) == 1

def test_update_takes():
    game = Game()
    game.reset_vars()
    game.first_suit = 3
    game.wild_suit = 0
    game.first_to_play = 0

    game.in_play = [Card(6, 3), Card(7, 3), Card(6, 2), Card(7, 2)]
    game.update_take()

    assert game.players[1].taken == 1

def test_process_hand_results():
    game = Game()
    game.reset_vars()
    game.first_suit = 3
    game.wild_suit = 0
    game.first_to_play = 0
    game.in_play = [Card(6, 3), Card(7, 3), Card(6, 2), Card(7, 2)]
    game.process_hand_results()

    assert game.players[1].taken == 1
    assert game.in_play == []
    assert game.first_suit == 4

def test_get_calls():
    game = Game()
    game.reset_vars()
    for player_num in range(game.first_to_play, game.first_to_play + 4):
        cards_per_player = game.get_num_to_deal()
        game.deck.deal(game.players[player_num % 4].hand, times = cards_per_player) # player num needs to be modded to get the correct players
        
    game.get_calls()

    assert game.players[0].taken >= 0 and game.players[0].taken <= 1
    assert game.players[1].taken >= 0 and game.players[1].taken <= 1
    assert game.players[2].taken >= 0 and game.players[2].taken <= 1
    assert game.players[3].taken >= 0 and game.players[3].taken <= 1

def test_get_num_to_deal():
    game = Game(only_nines=False)
    game.reset_vars()
    assert game.get_num_to_deal() == 1

    game = Game(only_nines=True)
    game.reset_vars()
    assert game.get_num_to_deal() == 9

def test_game_reset():
    game = Game([RandomCallerRandomPlayer(5), RandomCallerRandomPlayer(6), RandomCallerRandomPlayer(7), RandomCallerRandomPlayer(8)])
    game.deck.pop(0)
    game.in_play = [Card(6, 3), Card(7, 3), Card(6, 2), Card(7, 2)]
    game.round = 12
    game.play = 12
    game.first_to_play = 12
    game.first_suit = 11

    game.reset()

    assert len(game.deck) == 32
    assert isinstance(len(game.in_play), int) and len(game.in_play) >= 0 and len(game.in_play) <= 3
    assert game.round == 1
    assert game.play == 1
    assert game.first_to_play >= 0 and game.first_to_play <= 3
    assert game.first_to_play == 0 or game.first_suit == game.in_play[0].suit

    assert game.players[0].number == 5
    assert game.players[1].number == 6
    assert game.players[2].number == 7
    assert game.players[3].number == 8

def test_game_reset_vars():
    game = Game()
    game.reset_vars()
    assert game.round == 1
    assert game.play == 1
    assert game.first_to_play >= 0 and game.first_to_play <= 3
    assert game.first_suit == 4

def test_reset_and_one_step():
    random.seed(1)
    game = Game()
    game.reset()
    first = game.first_to_play
    if first == 0:
        assert game.first_suit == 4
    else:
        assert game.first_suit == game.in_play[0].suit

    assert game.play == 1
    assert game.round == 1
    assert [card not in game.in_play for card in game.players[0].hand].count(True) == game.get_num_to_deal()
    assert all([len(player.hand) >= 0 and len(player.hand) <= 1 for player in game.players[1:4]])

    dealer = game.dealer

    game.step(card_to_int(game.players[0].play(game.to_obs())))

    assert game.play == 2
    assert game.round == 1
    assert game.dealer == (dealer + 1) % 4
    dealer = game.dealer

    assert sum([player.taken for player in game.players]) == 0
    assert not all([not player.score for player in game.players])

def test_one_game():
    game = Game()
    game.reset()
    # game.print_game()
    while not game.is_done():
        game.step(card_to_int(game.players[0].play(game.to_obs())))
        # game.print_game()

def test_100_games():
    random.seed(3)
    for i in range(100):
        game = Game()
        game.reset()
        # # game.print_game()
        while not game.is_done():
            game.step(card_to_int(game.players[0].play(game.to_obs())))
        #     # game.print_game()
    
# def test_1000_games():
#     random.seed(3)
#     for i in range(1000):
#         game = Game()
#         game.reset()
#         # # game.print_game()
#         while not game.is_done():
#             game.step(card_to_int(game.players[0].play(game.to_obs())))
#         #     # game.print_game()

def test_second_card_wins():
    game = Game()

    for i in range(50):
        
        game.in_play = [Card(6, 1), # Transformed Joker
                        Card(7, 3), 
                        Card(6, 3), 
                        Card(7, 2)]
        assert game.winner(game.in_play) == 0
        
        game.in_play = [Card(6, 1), # Joker
                        Card(7, 1), 
                        Card(6, 3), 
                        Card(7, 2)]
        assert game.winner(game.in_play) == 1
        
        game.in_play = [Card(6, 0), # Transformed Joker
                        Card(7, 3), 
                        Card(6, 0), # Non-Joker 6 
                        Card(7, 2)]
        assert game.winner(game.in_play) == 0
        
        game.in_play = [Card(6, 0), # Transformed Joker
                        Card(7, 3), 
                        Card(6, 0), # Non-Joker 6
                        Card(16, 2)] # Joker
        assert game.winner(game.in_play) == 3

        game.in_play = [Card(6, 1), # Transformed Joker
                        Card(7, 1), 
                        Card(6, 0), 
                        Card(16, 2)] # Joker
        assert game.winner(game.in_play) == 3

        game.in_play = [Card(15, 2), # Joker
                        Card(7, 1), 
                        Card(6, 0), 
                        Card(16, 2)] # Joker
        assert game.winner(game.in_play) == 3

        game.in_play = [Card(15, 2), # Joker
                        Card(7, 1), 
                        Card(6, 0), 
                        Card(14, 1)]
        assert game.winner(game.in_play) == 0

        game.in_play = [Card(6, 3), 
                        Card(7, 1),
                        Card(6, 0),
                        Card(14, 1)]
        assert game.winner(game.in_play) == 0

        game.in_play = [Card(6, 3), 
                        Card(7, 1),
                        Card(6, 0),
                        Card(7, 3)]
        if game.wild_suit == 0:
            assert game.winner(game.in_play) == 0
        elif game.wild_suit == 1:
            assert game.winner(game.in_play) == 1
        else:
            assert game.winner(game.in_play) == 3

        game.in_play = [Card(6, 0),
                        Card(6, 1),
                        Card(6, 0),
                        Card(6, 2)]

        assert game.winner(game.in_play) == 0

