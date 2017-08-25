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

def test_bright_eyed_scout():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	assert game.player1.mana == 10
	assert wisp.cost == 0
	scout = game.player1.give("UNG_113").play()
	assert game.player1.mana == 6
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0] == wisp
	assert wisp.cost == 5
	wisp.play()
	assert game.player1.mana == 1

def test_earthen_scales():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	scales = game.player1.give("UNG_108").play(target=wisp)
	assert wisp.atk == 2
	assert wisp.health == 2
	assert game.player1.hero.armor == 2

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

def test_giant_anaconda():
	game = prepare_empty_game()
	anaconda1 = game.player1.give("UNG_086").play()
	anaconda1.destroy()
	assert len(game.player1.field) == 0

	game.end_turn(); game.end_turn()
	anaconda2 = game.player1.give("UNG_086").play()
	ogre = game.player1.give("CS2_200")
	for i in range(8):
		game.player1.give(WISP)
	assert len(game.player1.hand) == 9
	anaconda2.destroy()
	assert len(game.player1.field) == 1
	assert len(game.player1.hand) == 8
	assert game.player1.field[0] == ogre

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

def test_hemet_jungle_hunter():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).shuffle_into_deck()
	ice_barrier = game.player1.give("EX1_289").shuffle_into_deck()
	fireball = game.player1.give("CS2_029").shuffle_into_deck()
	antonidas = game.player1.give("EX1_559").shuffle_into_deck()

	hemet = game.player1.give("UNG_840")
	assert len(game.player1.deck) == 4
	hemet.play()
	assert len(game.player1.deck) == 2
	for card in game.player1.deck:
		assert card.cost > 3


def test_nesting_roc():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	nesting_roc1 = game.player1.give("UNG_801").play()
	assert not nesting_roc1.taunt
	nesting_roc2 = game.player1.give("UNG_801").play()
	assert nesting_roc2.taunt
