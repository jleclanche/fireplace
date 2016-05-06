from full_game import test_full_game
from utils import *


def run_selector(game, alex):
	selector = PIRATE | DRAGON + MINION
	assert len(selector.eval(game.player1.hand, game.player1)) >= 1

	selector = IN_HAND + DRAGON + FRIENDLY
	targets = selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] == alex


def test_selectors(benchmark):
	game = prepare_game()
	game.player1.discard_hand()
	alex = game.player1.give("EX1_561")

	benchmark(run_selector, game, alex)


def test_fullgame(benchmark):
	random.seed(1857)
	benchmark(test_full_game)
