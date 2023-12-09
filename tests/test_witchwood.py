from utils import *


def test_duskhaven_hunter():
	game = prepare_empty_game()
	game.player1.give("GIL_200")
	game.player1.give("GIL_128").play()
	assert game.player1.hand[0].atk == 4
	assert game.player1.hand[0].health == 10
	game.skip_turn()
	assert game.player1.hand[0].atk == 10
	assert game.player1.hand[0].health == 4


def test_echo():
	game = prepare_empty_game()
	game.player1.give("GIL_680")
	for _ in range(3):
		game.player1.hand[0].play()
		assert game.player1.hand[0].id == "GIL_680"
	game.end_turn()
	assert len(game.player1.hand) == 0
	assert len(game.player1.field) == 3
