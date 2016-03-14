#!/usr/bin/env python
import argparse
import re
import string
import sys; sys.path.append("..")
from fireplace import cards
from fireplace.utils import get_script_definition
from hearthstone.enums import CardSet


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"
PREFIXES = {
	GREEN: "Implemented",
	RED: "Not implemented",
}

SOLVED_KEYWORDS = [
	"Windfury", "Charge", "Divine Shield", "Taunt", "Stealth",
	r"Can't be targeted by spells or Hero Powers\.",
	r"Can't attack\.",
	"Destroy any minion damaged by this minion.",
	r"Your Hero Power deals \d+ extra damage.",
	r"Spell Damage \+\d+",
	r"Overload: \(\d+\)",
]

DUMMY_CARDS = (
	"PlaceholderCard",  # Placeholder Card
	"CS2_022e",  # Polymorph
	"EX1_246e",  # Hexxed
	"EX1_345t",  # Shadow of Nothing
	"GAME_006",  # NOOOOOOOOOOOO
	"LOEA04_27",  # Animated Statue
	"Mekka4e",  # Transformed
	"NEW1_025e",  # Bolstered (Unused)
	"TU4c_005",  # Hidden Gnome
	"TU4c_007",  # Mukla's Big Brother

	# Dynamic buffs set by their parent
	"CS2_236e",  # Divine Spirit
	"EX1_304e",  # Consume (Void Terror)
	"LOE_030e",  # Hollow (Unused)
	"NEW1_018e",  # Treasure Crazed (Bloodsail Raider)
)


def cleanup_description(description):
	ret = description
	ret = re.sub("<i>.+</i>", "", ret)
	ret = re.sub("(<b>|</b>)", "", ret)
	ret = re.sub("(" + "|".join(SOLVED_KEYWORDS) + ")", "", ret)
	ret = re.sub("<[^>]*>", "", ret)
	exclude_chars = string.punctuation + string.whitespace
	ret = "".join([ch for ch in ret if ch not in exclude_chars])
	return ret


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
		description = cleanup_description(card.description)
		implemented = False

		if not description:
			# Minions without card text or with basic abilities are implemented
			implemented = True
		elif card.card_set == CardSet.CREDITS:
			implemented = True

		if id in DUMMY_CARDS:
			implemented = True

		carddef = get_script_definition(id)
		if carddef:
			implemented = True

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
