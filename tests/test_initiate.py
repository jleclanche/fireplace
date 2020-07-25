from utils import *


def test_nethrandamus():
	game = prepare_game()
	nethrandamus = game.player1.give("BT_481")
	assert nethrandamus.upgrade_counter == 0
	for i in range(7):
		game.player1.give(WISP).play()
	game.player1.give("EX1_400").play()
	assert nethrandamus.upgrade_counter == 7
	nethrandamus.play()
	assert game.player1.field[0].cost == 7
	assert game.player1.field[-1].cost == 7


def test_mana_burn():
	game = prepare_game()
	mana_burn = game.player1.give("BT_753")
	mana_burn.play()
	game.end_turn()
	assert game.player2.mana == 8


def test_flamereaper():
	game = prepare_game()
	flamereaper = game.player1.give("BT_271")
	flamereaper.play()
	game.end_turn()
	for i in range(3):
		game.player2.give(WISP).play()
	game.end_turn()
	assert len(game.player2.field) == 3
	game.player1.hero.attack(game.player2.field[1])
	assert len(game.player2.field) == 0


def test_outcast():
	game = prepare_empty_game()
	game.player1.give(WISP)
	illidari_felblade1 = game.player1.give("BT_814")
	illidari_felblade2 = game.player1.give("BT_814")
	illidari_felblade1.play()
	illidari_felblade2.play()
	assert not illidari_felblade1.immune
	assert illidari_felblade2.immune
