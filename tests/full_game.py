#!/usr/bin/env python
import sys; sys.path.append("..")
import logging
from fireplace import cards
from fireplace.utils import play_full_game


def test_full_game():
	return play_full_game(False)


def main():
	turns = []
	runtime = []

	logging.disable(logging.CRITICAL)

	cards.db.initialize()
	if len(sys.argv) > 1:
		numgames = sys.argv[1]
		if not numgames.isdigit():
			sys.stderr.write("Usage: %s [NUMGAMES]\n" % (sys.argv[0]))
			exit(1)
	else:
		numgames = 1

	for i in range(int(numgames)):
		game = test_full_game()
		turns.append(game.turn)
		runtime.append(game.runtime)

	avg_runtime_per_game = sum(runtime) / len(runtime)
	avg_turns_per_game = sum(turns) / len(turns)
	avg_games_per_second = int(numgames) / sum(runtime)
	avg_turns_per_second = sum(turns) / sum(runtime)

	print("Average runtime over " + str(numgames) + " games: %.2f sec" % avg_runtime_per_game)
	print("Average turns per game: %.2f" % avg_turns_per_game)
	print("Average games per second: %.2f" % avg_games_per_second)
	print("Average turns per second: %.2f" % avg_turns_per_second)

if __name__ == "__main__":
	main()
