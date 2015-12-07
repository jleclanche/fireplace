from utils import *


LORD_JARAXXUS = "EX1_323"
LORD_JARAXXUS_HERO = "EX1_323h"
LORD_JARAXXUS_WEAPON = "EX1_323w"
INFERNO = "EX1_tk33"
INFERNO_TOKEN = "EX1_tk34"


def test_jaraxxus():
	game = prepare_game(WARRIOR, WARRIOR)
	game.player1.hero.power.use()
	game.player1.give(LIGHTS_JUSTICE).play()
	assert game.player1.weapon.id == LIGHTS_JUSTICE
	game.end_turn(); game.end_turn()

	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 2
	game.player1.give(LORD_JARAXXUS).play()
	assert game.player1.hero.id == LORD_JARAXXUS_HERO
	assert game.player1.weapon.id == LORD_JARAXXUS_WEAPON
	assert game.player1.hero.health == 15
	assert game.player1.hero.armor == 0
	assert game.player1.hero.power.id == INFERNO
	assert len(game.player1.field) == 0
	game.end_turn(); game.end_turn()

	game.player1.hero.power.use()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == INFERNO_TOKEN


def test_jaraxxus_cult_master():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.summon("EX1_595")
	game.player1.give(LORD_JARAXXUS).play()
	assert len(game.player1.field) == 1
	assert not game.player1.hand
