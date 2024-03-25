#!/usr/bin/env python
import argparse
import sys

from utils import *

from fireplace import cards


PREFIXES = {
	GREEN: "Implemented",
	RED: "Not implemented",
}


def main():
	impl = 0
	unimpl = 0

	p = argparse.ArgumentParser()
	p.add_argument(
		"--implemented",
		action="store_true",
		dest="implemented",
		help="Show only implemented cards"
	)
	p.add_argument(
		"--unimplemented",
		action="store_true",
		dest="unimplemented",
		help="Show only unimplemented cards"
	)
	p.add_argument(
		"--collectible",
		action="store_true",
		dest="collectible",
		help="Show only collectible cards"
	)

	args = p.parse_args(sys.argv[1:])

	if not args.implemented and not args.unimplemented:
		args.implemented = True
		args.unimplemented = True

	cards.db.initialize()
	for id in sorted(cards.db):
		card = cards.db[id]
		if args.collectible and not card.collectible:
			continue

		implemented = check_implemented(card)
		color = GREEN if implemented else RED
		name = color + "%s: %s" % (PREFIXES[color], card.name) + ENDC

		if implemented:
			impl += 1
			if args.implemented:
				print("%s (%s)" % (name, id))
		else:
			unimpl += 1
			if args.unimplemented:
				print("%s (%s)" % (name, id))

	total = impl + unimpl

	print("%i / %i cards implemented (%i%%)" % (impl, total, (impl / total) * 100))


if __name__ == "__main__":
	main()
