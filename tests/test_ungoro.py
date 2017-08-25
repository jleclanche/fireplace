from utils import *

def test_frozen_crusher():
	game = prepare_game()
	frozen_crusher = game.player1.give("UNG_079").play()
	game.end_turn(); game.end_turn()
	assert not frozen_crusher.frozen
	frozen_crusher.attack(game.player2.hero)
	assert frozen_crusher.frozen
	assert game.player2.hero.health == 30 - 8
	game.end_turn(); game.end_turn()
	assert frozen_crusher.frozen
	game.end_turn(); game.end_turn()
	assert not frozen_crusher.frozen

def test_nesting_roc():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	nesting_roc1 = game.player1.give("UNG_801").play()
	assert not nesting_roc1.taunt
	nesting_roc2 = game.player1.give("UNG_801").play()
	assert nesting_roc2.taunt
