#!/usr/bin/env python
from utils import *
from fireplace.dsl import *


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
