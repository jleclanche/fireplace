#!/usr/bin/env python
import sys

from hearthstone.enums import PlayState

from fireplace import cards
from fireplace.exceptions import GameOver
from fireplace.utils import play_full_game, play_full_mcts_game


sys.path.append("..")


def test_full_game():
	do_mcts = True
	if not do_mcts:
		try:
			play_full_game()
		except GameOver:
			print("Game completed normally.")
	else:
		won = 0
		lost = 0
		for i in range(100):
			game = play_full_mcts_game()
			mcts_player = game.players[0]

			if mcts_player.playstate == PlayState.WON:
				won += 1
				print("won game, currently:" + str(won) + "/" + str(i+1))
			else:
				lost += 1
				print("lost game, currently:" + str(won) + "/" + str(i+1))
		print("w/l")
		print(won)
		print(lost)
		print(float(won/lost))



def main():
	cards.db.initialize()
	if len(sys.argv) > 1:
		numgames = sys.argv[1]
		if not numgames.isdigit():
			sys.stderr.write("Usage: %s [NUMGAMES]\n" % (sys.argv[0]))
			exit(1)
		for i in range(int(numgames)):
			test_full_game()
	else:
		test_full_game()


if __name__ == "__main__":
	main()
