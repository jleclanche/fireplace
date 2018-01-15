from utils import *

def test_keening_banshee():
	"ICC_911"
	game = prepare_game()
	banshee = game.player1.give("ICC_911")
	banshee.play()
	assert len(game.player1.field) == 1
	assert len(game.player1.deck) == 26

	game.player1.give(WISP).play()
	assert len(game.player1.field) == 2
	assert len(game.player1.deck) == 26 - 3

	game.player1.give(WISP).play()
	assert len(game.player1.field) == 3
	assert len(game.player1.deck) == 26 - 3 - 3

	game.end_turn()

	game.player2.give(WISP).play() # this shouldn't affect the deck
	assert len(game.player1.deck) == 26 - 3 - 3


def test_frozen_clone():
	"ICC_082"
	game = prepare_game()
	secret = game.player1.give("ICC_082")
	secret.play()
	assert len(game.player1.field) == 0
	assert len(game.player1.secrets) == 1
	assert len(game.player1.hand) == 4

	game.end_turn()

	game.player2.give(WISP).play()

	assert len(game.player2.field) == 1
	assert len(game.player1.hand) == 4 + 2
	assert len(game.player1.secrets) == 0

	assert game.player1.hand[-1].id == WISP
	assert game.player1.hand[-2].id == WISP

