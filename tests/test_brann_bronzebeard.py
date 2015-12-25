from utils import *


BRANN_BRONZEBEARD = "LOE_077"


def _prepare_game():
	game = prepare_game()
	brann = game.player1.give(BRANN_BRONZEBEARD)
	brann.play()
	game.end_turn(); game.end_turn()

	game.player1.discard_hand()

	return game, brann


def test_brann_abusive_sergeant():
	game, brann = _prepare_game()
	abusive = game.player1.give("CS2_188")
	abusive.play(target=brann)
	assert brann.atk == 2 + (2 * 2)


def test_brann_injured_blademaster():
	game, brann = _prepare_game()
	blademaster = game.player1.give("CS2_181")
	blademaster.play()
	assert blademaster.dead


def test_brann_novice_engineer():
	game, brann = _prepare_game()
	novice = game.player1.give("EX1_015")
	novice.play()
	assert len(game.player1.hand) == 2


def test_brann_youthful_brewmaster():
	game, brann = _prepare_game()
	brewmaster = game.player1.give("EX1_049")
	brewmaster.play(target=brann)
	assert brann in game.player1.hand
