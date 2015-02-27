#!/usr/bin/env python
import os
import sys; sys.path.append("..")
from fireplace import cards
from fireplace.cards import debug, game, classic, naxxramas, gvg, removed
from fireplace.card import Card


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"


def main():
	for id in sorted(cards.__dict__):
		cls = getattr(cards, id)
		if not hasattr(cls, "tags"):
			continue
		for set in (debug, game, classic, naxxramas, gvg, removed):
			if hasattr(set, id):
				color = GREEN
				break
		else:
			color = RED
		print(color + cls.tags[185] + ENDC + " (%s)" % (id))


if __name__ == "__main__":
	main()
