import full_game
import random

# At around 2-5 games per second, this generally takes a couple minutes
ITERATIONS = 500


def test_full_games():
	random.seed(271818)
	for _ in range(ITERATIONS):
		full_game.test_full_game()
