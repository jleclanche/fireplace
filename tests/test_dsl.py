#!/usr/bin/env python
from utils import *
from fireplace.dsl import *
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
	ids = picker.cards
	for id in ids:
		card = Card(id)
		assert card.type is not CardType.HERO
		assert card.type is not CardType.ENCHANTMENT
		assert card.type is not CardType.HERO_POWER
