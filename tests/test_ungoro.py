from utils import *

def test_bittertide_hydra():
	game = prepare_game()
	bittertide_hydra = game.player1.give("UNG_087").play()
	game.end_turn()
	assert game.player1.hero.health == 30
	moonfire = game.player2.give(MOONFIRE).play(target=bittertide_hydra)
	assert game.player1.hero.health == 30 - 3
	pyroblast = game.player2.give("EX1_279").play(target=bittertide_hydra)
	assert game.player1.hero.health == 30 - 3 - 3

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

def test_gluttonous_ooze():
	game = prepare_game();
	ooze = game.player1.give("UNG_946").play()
	assert game.player1.hero.armor == 0
	game.end_turn()
	waraxe = game.player2.give("CS2_106").play()
	game.end_turn()
	ooze2 = game.player1.give("UNG_946").play()
	assert game.player1.hero.armor == 3
	assert waraxe.dead

def test_nesting_roc():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	nesting_roc1 = game.player1.give("UNG_801").play()
	assert not nesting_roc1.taunt
	nesting_roc2 = game.player1.give("UNG_801").play()
	assert nesting_roc2.taunt
