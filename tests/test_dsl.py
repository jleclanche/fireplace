#!/usr/bin/env python
import pytest
from utils import *
from fireplace.dsl import *
from fireplace.exceptions import *
from fireplace.card import Card


def test_selector():
	game = prepare_game()
	game.player1.discard_hand()
	alex = game.player1.give("EX1_561")
	selector = PIRATE | DRAGON + MINION
	assert len(selector.eval(game.player1.hand, game.player1)) >= 1

	selector = IN_HAND + DRAGON + FRIENDLY
	targets = selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] == alex


def test_empty_selector():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	selector = IN_HAND

	targets = selector.eval(game.player1.hand, game.player1)
	assert not targets


def test_random_card_picker():
	picker = RandomCardPicker()
	ids = picker.find_cards()
	for id in ids:
		card = Card(id)
		assert card.type is not CardType.HERO
		assert card.type is not CardType.ENCHANTMENT
		assert card.type is not CardType.HERO_POWER


def test_controller():
	game = prepare_game()
	game.player1.discard_hand()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert Controller().evaluate(wisp) is game.player1


def test_self_selector():
	game = prepare_game()
	selector = SELF
	for source in game:
		targets = selector.eval(game, source)
		assert len(targets) == 1
		assert targets[0] is source


def test_owner_selector():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	blessing_wisdom = game.player1.give("EX1_363")
	blessing_wisdom.play(target=wisp)
	targets = OWNER.eval(game, wisp.buffs[0])
	assert len(targets) == 1
	assert targets[0] is wisp


def test_id_selector():
	game = prepare_game()
	for entity in game.entities:
		id = getattr(entity, "id", None)
		if id:
			targets = ID(id).eval(game, game.player1)
			assert len(targets) >= 1
			assert targets[0].id == id


def test_target_selector():
	game = prepare_game()
	moonfire = game.player1.give(MOONFIRE)
	target = game.player1.hero
	# Set this manually for the selector
	moonfire.target = target

	targets = TARGET.eval(game, moonfire)
	assert len(targets) == 1
	assert targets[0] == target


def test_high_low_atk_selectors():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()

	# Give two wisps and make sure we only get back one
	wisp = game.player1.give(WISP)
	wisp2 = game.player1.give(WISP)

	IN_HAND = EnumSelector(Zone.HAND)
	high_selector = HIGHEST_ATK(IN_HAND)
	low_selector = LOWEST_ATK(IN_HAND)

	targets = high_selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] == wisp

	targets = low_selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] == wisp

	alex = game.player1.give("EX1_561")
	mountain = game.player1.give("EX1_105")

	targets = high_selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] in [alex, mountain]

	targets = low_selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] == wisp


def test_controlled_by_selector():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()

	wisp = game.player1.give(WISP)
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)

	wisp.play()
	goldshire.play()

	MINION = EnumSelector(CardType.MINION)
	IN_PLAY = EnumSelector(Zone.PLAY)
	selector = MINION + IN_PLAY + FRIENDLY

	for source in [wisp, goldshire, game.player1]:
		targets = selector.eval(game, source)
		assert len(targets) == 2
		assert set(targets) == set([wisp, goldshire])

	selector = MINION + IN_PLAY + ENEMY
	targets = selector.eval(game, game.player2)
	assert len(targets) == 2
	assert set(targets) == set([wisp, goldshire])

	moonfire = game.player1.give(MOONFIRE)
	moonfire.target = game.player1.hero
	selector = MINION + IN_PLAY + CONTROLLED_BY(TARGET) + (AttrValue(GameTag.HEALTH) == 1)
	targets = selector.eval(game, moonfire)
	assert len(targets) == 1
	assert targets[0] == wisp


def test_random_selector():
	game = prepare_game()
	selector = RANDOM(EnumSelector(CardType.MINION))
	targets = selector.eval(game, game.player1)
	assert len(targets) == 1

	targets = (selector * 3).eval(game, game.player1)
	assert len(targets) == 3


def test_positional_selectors():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	wisp3 = game.player1.give(WISP)
	wisp3.play()
	wisp4 = game.player1.give(WISP)
	wisp4.play()
	defender = game.player1.give("EX1_093")
	defender.play(index=2)
	assert game.player1.field == [wisp1, wisp2, defender, wisp3, wisp4]

	left = LEFT_OF(SELF).eval(game, defender)
	assert len(left) == 1
	assert left[0] is wisp2

	right = RIGHT_OF(SELF).eval(game, defender)
	assert len(right) == 1
	assert right[0] is wisp3

	adjacent = ADJACENT(SELF).eval(game, defender)
	assert len(adjacent) == 2
	assert adjacent[0] is wisp2
	assert adjacent[1] is wisp3


def test_hijack():
	game = prepare_game()
	vial = game.player1.give("LOEA16_8")
	with hijacked(RANDOM_ENEMY_MINION, FRIENDLY_HERO):
		with pytest.raises(GameOver):
			vial.play()
