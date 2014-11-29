#!/usr/bin/env python
import os
import sys; sys.path.append("..")
from fireplace import xmlcard
from fireplace.cards import Card


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"


def main():
	for card in sorted(os.listdir(xmlcard._path)):
		id = os.path.splitext(card)[0]
		card = Card(id)
		unimplemented = card.data.__class__ is xmlcard.XMLCard
		if unimplemented:
			color = RED
		else:
			color = GREEN

		print(color + str(card) + ENDC + " (%s)" % (id))


if __name__ == "__main__":
	main()
