from src.player import Player

def test_player_init():
    player1 = Player(0)
    assert player1.number == 0
    assert player1.hand == []
    assert player1.score == 0

    player2 = Player(1)
    assert player2.number == 1

def test_player_repr():
    player1 = Player(0)
    assert repr(player1) == "Player 0"

    player2 = Player(1)
    assert repr(player2) == "Player 1"

def test_player_get_right():
    player1 = Player(0)
    assert player1.right() == 1

    player2 = Player(1)
    assert player2.right() == 2

def test_player_get_left():
    player1 = Player(0)
    assert player1.left() == 3

    player2 = Player(1)
    assert player2.left() == 0

def test_player_get_across():
    player1 = Player(0)
    assert player1.across() == 2

    player2 = Player(1)
    assert player2.across() == 3

def test_update_score():
    player = Player(0)
    player.update_score(1, 1, 1)
    assert player.score == 100

    player.update_score(1, 1, 2)
    assert player.score == 200

    player.update_score(3, 3, 3)
    assert player.score == 500
