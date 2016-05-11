import pytest
from utils import *
from fireplace.exceptions import GameOver


LORD_JARAXXUS = "EX1_323"
LORD_JARAXXUS_HERO = "EX1_323h"
LORD_JARAXXUS_WEAPON = "EX1_323w"
INFERNO = "EX1_tk33"
INFERNO_TOKEN = "EX1_tk34"


def test_jaraxxus():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
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


def test_jaraxxus_knife_juggler():
	game = prepare_game()
	juggler = game.player1.summon("NEW1_019")
	game.player1.give(LORD_JARAXXUS).play()
	assert game.player2.hero.health == 30


def test_jaraxxus_molten_giant():
	game = prepare_game()
	jaraxxus = game.player1.give("EX1_323")
	molten = game.player1.give("EX1_620")
	jaraxxus.play()
	assert game.player1.hero.health == 15
	assert molten.cost == 25


def test_jaraxxus_mirror_entity():
	game = prepare_game()
	mirror = game.player1.give("EX1_294")
	mirror.play()
	game.end_turn()

	jaraxxus = game.player2.give(LORD_JARAXXUS)
	jaraxxus.play()
	assert not game.player1.secrets
	assert game.player2.hero.id == LORD_JARAXXUS_HERO
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == LORD_JARAXXUS


def test_jaraxxus_repentance():
	game = prepare_game()
	repentance = game.player1.give("EX1_379")
	repentance.play()
	game.end_turn()

	jaraxxus = game.player2.give(LORD_JARAXXUS)
	jaraxxus.play()
	assert not game.player1.secrets
	assert game.player2.hero.id == LORD_JARAXXUS_HERO
	assert game.player2.hero.health == game.player2.hero.max_health == 1


def test_jaraxxus_snipe():
	game = prepare_game()
	snipe = game.player1.give("EX1_609")
	snipe.play()
	game.end_turn()

	jaraxxus = game.player2.give(LORD_JARAXXUS)
	jaraxxus.play()
	assert not game.player1.secrets
	assert game.player2.hero.damage == 4
	assert game.player2.hero.health == 11


def test_jaraxxus_sacred_trial():
	game = prepare_game()
	trial = game.player1.give("LOE_027")
	trial.play()
	game.end_turn()

	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	jaraxxus = game.player2.give(LORD_JARAXXUS)
	jaraxxus.play()
	# Will not trigger as 4th minion due to timing
	assert trial in game.player1.secrets
	assert not game.player2.hero.dead
	game.end_turn(); game.end_turn()

	wisp4 = game.player2.summon(WISP)
	assert not wisp4.dead
	jaraxxus = game.player2.give(LORD_JARAXXUS)
	with pytest.raises(GameOver):
		jaraxxus.play()
		assert trial not in game.player1.secrets
		assert game.player2.hero.dead
