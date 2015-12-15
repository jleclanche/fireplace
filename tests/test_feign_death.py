from utils import *


FEIGN_DEATH = "GVG_026"


def test_feign_death():
	game = prepare_game()
	game.player1.discard_hand()
	fd = game.player1.give("GVG_026")
	creeper = game.player1.give("FP1_002")
	webspinner = game.player1.give("FP1_011")
	creeper.play()
	webspinner.play()
	fd.play()
	assert not creeper.dead
	assert not webspinner.dead
	assert len(game.player1.field) == 4
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.BEAST


def test_feign_death_anubar_ambusher():
	game = prepare_game()
	anubar = game.player1.give("FP1_026")
	anubar.play()
	game.player1.give(FEIGN_DEATH).play()
	assert anubar in game.player1.hand


def test_feign_death_baron_rivendare():
	game = prepare_game()
	fd = game.player1.give("GVG_026")
	rivendare = game.player1.give("FP1_031")
	rivendare.play()
	creeper = game.player1.give("FP1_002")
	creeper.play()
	fd.play()
	assert not creeper.dead
	assert len(game.player1.field) == 6


def test_feign_death_dark_cultist():
	game = prepare_game()
	fd = game.player1.give("GVG_026")
	cultist = game.player1.give("FP1_023")
	cultist.play()
	fd.play()
	assert not cultist.buffs
	assert cultist.health == 4
