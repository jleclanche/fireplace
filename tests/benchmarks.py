"""
Fireplace micro-benchmarks.

Note that py.test will skip these by default. To run (with pytest-benchmark installed):

	py.test fireplace/benchmarks.py

To increase the number of iterations, set --benchmark-min-rounds.
"""

import sys; sys.path.append("..")
import fireplace.utils
import pytest
from full_game import test_full_game
from utils import *

ARBITRARY_SEED = 1857


def run_selector(game, alex):
	selector = PIRATE | DRAGON + MINION
	assert len(selector.eval(game.player1.hand, game.player1)) >= 1

	selector = IN_HAND + DRAGON + FRIENDLY
	targets = selector.eval(game, game.player1)
	assert len(targets) == 1
	assert targets[0] == alex


@pytest.mark.benchmark(
	group="selector"
)
def test_selectors(benchmark):
	game = prepare_game()
	game.player1.discard_hand()
	alex = game.player1.give("EX1_561")

	benchmark(run_selector, game, alex)


def seeded_fullgame():
	random.seed(ARBITRARY_SEED)
	test_full_game()


@pytest.mark.benchmark(
	group="fullgame",
	min_rounds=50
)
def test_fullgame(benchmark):
	benchmark(seeded_fullgame)


@pytest.mark.benchark(
	group="turn"
)
def test_singleturn(benchmark):
	benchmark.weave(fireplace.utils.play_turn, lazy=True)
	seeded_fullgame()
