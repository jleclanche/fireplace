#!/usr/bin/env python
from utils import *
from fireplace.exceptions import InvalidAction
import pytest


def test_play_on_wrong_turn():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player2.give(WISP)
		wisp.play()


def test_play_card_in_deck():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		wisp.shuffle_into_deck()
		wisp.play()


def test_play_double():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		wisp.play()
		wisp.play()


def test_play_without_target():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		game.player1.summon(WISP)
		abusive = game.player1.give("CS2_188")
		abusive.play()


def test_play_with_invalid_target():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		game.player1.summon(WISP)
		abusive = game.player1.give("CS2_188")
		assert game.player1.hero not in abusive.targets
		abusive.play(target=game.player1.hero)


def test_play_choose_without_choice():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		powerofwild = game.player1.give("EX1_160")
		powerofwild.play()


def test_attack_without_charge():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		wisp.attack(game.player2.hero)


def test_attack_on_wrong_turn():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		wisp.play()
		game.end_turn()

		wisp.attack(game.player2.hero)


def test_attack_dead_minion():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		wisp.play()
		game.end_turn()

		wisp.attack(game.player2.hero)


def test_attack_invalid_target():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		game.end_turn(); game.end_turn()
		assert game.player1.hero not in wisp.targets
		wisp.attack(game.player1.hero)


def test_attack_without_weapon():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		game.player1.hero.attack(game.player2.hero)


def test_attack_own_minion():
	with pytest.raises(InvalidAction):
		game = prepare_game()
		wisp = game.player1.give(WISP)
		wisp.play()
		game.player1.hero.attack(wisp)


def test_hero_power_on_wrong_turn():
	with pytest.raises(InvalidAction):
		game = prepare_game(WARRIOR, WARRIOR)
		game.end_turn()

		game.player1.hero.power.use()


def test_hero_power_without_target():
	with pytest.raises(InvalidAction):
		game = prepare_game(MAGE, MAGE)
		game.player1.hero.power.use()
