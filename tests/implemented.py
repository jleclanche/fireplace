#!/usr/bin/env python
import os
import sys; sys.path.append("..")
from fireplace import cards
from fireplace.cards import debug, game, classic, naxxramas, gvg, removed


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"


def main():
	for id in sorted(cards.db):
		card = cards.db[id]
		for set in (debug, game, classic, naxxramas, gvg, removed):
			if hasattr(set, id):
				color = GREEN
				break
			elif not card.description:
				# Minions without card text are implemented
				color = GREEN
				break
		else:
			color = RED
		print(color + card.name + ENDC + " (%s)" % (id))


if __name__ == "__main__":
	main()
