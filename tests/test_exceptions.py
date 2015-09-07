#!/usr/bin/env python
import pytest
from utils import *
from fireplace.exceptions import GameOver, InvalidAction


def test_concede():
	game = prepare_game()
	with pytest.raises(GameOver):
		game.player1.concede()
	assert game.player1.playstate == PlayState.LOST
	assert game.player2.playstate == PlayState.WON


def test_play_on_wrong_turn():
	game = prepare_game()
	wisp = game.player2.give(WISP)
	with pytest.raises(InvalidAction):
		wisp.play()


def test_play_card_in_deck():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	with pytest.raises(InvalidAction):
		wisp.play()


def test_play_twice():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	with pytest.raises(InvalidAction):
		wisp.play()


def test_play_without_target():
	game = prepare_game()
	game.player1.summon(WISP)
	abusive = game.player1.give("CS2_188")
	with pytest.raises(InvalidAction):
		abusive.play()


def test_play_with_invalid_target():
	game = prepare_game()
	game.player1.summon(WISP)
	abusive = game.player1.give("CS2_188")
	assert game.player1.hero not in abusive.targets
	with pytest.raises(InvalidAction):
		abusive.play(target=game.player1.hero)


def test_play_choose_without_choice():
	game = prepare_game()
	powerofwild = game.player1.give("EX1_160")
	with pytest.raises(InvalidAction):
		powerofwild.play()


def test_attack_without_charge():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	with pytest.raises(InvalidAction):
		wisp.attack(game.player2.hero)


def test_attack_on_wrong_turn():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	with pytest.raises(InvalidAction):
		wisp.attack(game.player2.hero)


def test_attack_with_dead_minion():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn(); game.end_turn()

	game.player1.give(MOONFIRE).play(target=wisp)
	with pytest.raises(InvalidAction):
		wisp.attack(game.player2.hero)


def test_attack_invalid_target():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	game.end_turn(); game.end_turn()

	assert game.player1.hero not in wisp.targets
	with pytest.raises(InvalidAction):
		wisp.attack(game.player1.hero)


def test_attack_without_weapon():
	game = prepare_game()
	with pytest.raises(InvalidAction):
		game.player1.hero.attack(game.player2.hero)


def test_attack_own_minion():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	axe = game.player1.give("CS2_106")
	axe.play()
	with pytest.raises(InvalidAction):
		game.player1.hero.attack(wisp)


def test_hero_power_on_wrong_turn():
	game = prepare_game(WARRIOR, WARRIOR)
	game.end_turn()

	with pytest.raises(InvalidAction):
		game.player1.hero.power.use()


def test_hero_power_twice():
	game = prepare_game(WARRIOR, WARRIOR)
	game.player1.hero.power.use()
	with pytest.raises(InvalidAction):
		game.player1.hero.power.use()


def test_hero_power_without_target():
	game = prepare_game(MAGE, MAGE)
	with pytest.raises(InvalidAction):
		game.player1.hero.power.use()
