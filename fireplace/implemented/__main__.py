import argparse
import sys
from .. import cards
from . import is_implemented


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"
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
	args = p.parse_args(sys.argv[1:])

	if not args.implemented and not args.unimplemented:
		args.implemented = True
		args.unimplemented = True

	cards.db.initialize()
	for id in sorted(cards.db):
		card = cards.db[id]

		implemented = is_implemented(card)

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


main()
