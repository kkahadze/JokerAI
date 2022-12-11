# from joker_game import Game, StandardJokerDeck, Player, Card
# from joker_display import Display
# from joker_simulation import Simulation
# import unittest   # The test framework

# # Values:
#     # 6: 4
#     # 7: 5
#     # 8: 6
#     # 9: 7
#     # 10: 8
#     # Jack : 9
#     # Queen : 10
#     # King : 11
#     # Ace : 11
#     # Joker : 13

# # Suits
#     # Diamonds: 0
#     # Clubs: 1
#     # Hearts: 2
#     # Spades: 3


# class Test_Units(unittest.TestCase):
#     def test_card_repr(self):
#         cards = [Card(4, 1), Card(13, 0), Card(10, 2), Card(11, 3)]
#         assert repr(cards[0]) == "Six of Clubs"
#         assert repr(cards[1]) == "Joker"
#         assert repr(cards[2]) == "Queen of Hearts"
#         assert repr(cards[3]) == "King of Spades"
    
#     def test_create_deck(self):
#         deck = StandardJokerDeck()
#         assert len(list(filter(lambda x: x.value == 4, deck))) == 2
#         assert len(list(filter(lambda x: x.value == 13, deck))) == 2
#         assert len(list(filter(lambda x: x.suit == 0 and x.value != 13, deck))) == 9
#         assert len(list(filter(lambda x: x.suit == 1 and x.value != 13, deck))) == 8
#         assert len(list(filter(lambda x: x.suit == 2 and x.value != 13, deck))) == 9
#         assert len(list(filter(lambda x: x.suit == 3 and x.value != 13, deck))) == 8
    
#     def test_shuffle(self):
#         deck = StandardJokerDeck()
#         old = deck.copy()
#         deck.shuffle()
#         assert (deck != old)
    
#     def test_get_player_score(self):
#         game = Game()
#         game.users[0].taken = 4
#         game.users[0].called = 4
#         game.cards_dealt = 4
#         assert game.get_player_score(0) == 400
#         game.cards_dealt = 5
#         assert game.get_player_score(0) == 250
#         game.users[0].taken = 3
#         assert game.get_player_score(0) == 30
#         game.users[0].taken = 0
#         assert game.get_player_score(0) == -200
    
#     def test_set_dealer(self):
#         game = Game()
#         og_dealer = game.dealer
#         assert game.get_place_in_playing_order(og_dealer) == 4
#         game.set_dealer()
#         assert game.get_place_in_playing_order(og_dealer) == 3
#         game.set_dealer()
#         assert game.get_place_in_playing_order(og_dealer) == 2
#         game.set_dealer()
#         assert game.get_place_in_playing_order(og_dealer) == 1
#         game.set_dealer()
#         assert game.get_place_in_playing_order(og_dealer) == 4
    
#     def test_get_place_in_playing_order(self):
#         game = Game()
#         total = 0
#         for i in range(0,4):
#             total += game.get_place_in_playing_order(i)
#         assert total == 10
    
#     def test_update_round(self):
#         game = Game()
#         assert (game.round == 0 and game.play == 0)
#         game.update_round()
#         assert (game.round == 1 and game.play == 1)
#         for i in range(8):
#             game.update_round()
#         assert game.round == 2 and game.play == 1
#         for i in range(4):
#             game.update_round()
#         assert game.round == 3 and game.play == 1
#         for i in range(8):
#             game.update_round()
#         assert game.round == 4 and game.play == 1
        
#     def test_get_play_index_of_game(self):
#         game = Game()
#         last = 1
#         game.update_round()
#         game.update_round()
#         game.update_round()
#         for i in range(22):
#             index = game.get_play_index_of_game()
#             assert index == last + 1
#             last = index
#             game.update_round()
    
#     def test_card_to_weight(self):
#         game = Game()
#         game.first_suit = 1
#         game.wildcard = Card(7, 2)
#         nothing = game.card_to_weight(Card(0, 12))
#         first = game.card_to_weight(Card(11,1))
#         wild = game.card_to_weight(Card(10, 2))
#         jok = game.card_to_weight(Card(13, 0))

#         assert nothing < first and nothing < wild and nothing < jok
#         assert first > nothing and first < wild and first < jok
#         assert wild > nothing and wild > first and wild < jok
#         assert jok > nothing and jok > first and jok > wild

#     def test_compute_winner(self):
#         game = Game()
#         game.dealer = 3
#         game.wildcard = Card(7, 0)
#         game.first_suit = 0
#         played = [Card(12, 0), Card(13, 0), Card(11, 2), Card(13, 0)]
#         assert game.compute_winner(played) == 3 # Second Joker wins
#         played = [Card(12, 0), Card(12, 1), Card(12, 2), Card(12, 3)]
#         assert game.compute_winner(played) == 0
#         played = [Card(6, 1), Card(10, 1), Card(12, 2), Card(8, 3)]
#         assert game.compute_winner(played) == 2

#     def test_playable(self):
#         game = Game()
#         game.users[0].cards = [Card(7, 1), Card(7, 3), Card(12, 2), Card(7, 3), Card(7, 2), Card(13, 1)]
#         assert str(game.playable(0, Card(10, 0), 0)) == str([Card(7, 1), Card(7, 3), Card(12, 2), Card(7, 3), Card(7, 2), Card(13, 1)])
#         assert str(game.playable(0, Card(10, 0), 0)) == str([Card(7, 1), Card(7, 3), Card(12, 2), Card(7, 3), Card(7, 2), Card(13, 1)])

# if __name__ == '__main__':
#     unittest.main()
