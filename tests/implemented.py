#!/usr/bin/env python
import argparse
import importlib
import re
import string
import sys; sys.path.append(".."); sys.path.append("../fireplace/cards/data")
from fireplace import cards
from fireplace.enums import CardType, CardSet

import buffs


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"
PREFIXES = {
	GREEN: "Implemented",
	RED: "Not implemented",
}

SOLVED_KEYWORDS = [
	"Windfury", "Charge", "Divine Shield", "Taunt", "Stealth",
	"Can't be targeted by spells or Hero Powers",
	"Destroy any minion damaged by this minion.",
	"50% chance to attack the wrong enemy",
	"Can't attack",
	"Always wins Brawls.",
	r"Your Hero Power deals \d+ extra damage.",
	r"Spell Damage \+\d+",
	r"Overload: \(\d+\)",
]

CARD_SETS = {
	"debug": None,
	"game": None,
	"tutorial": None,
	"classic": None,
	"naxxramas": None,
	"gvg": None,
	"blackrock": None,
	"tgt": None,
}

DUMMY_CARDS = (
	"CS1_113e",  # Mind Control
	"CS2_022e",  # Polymorph
	"EX1_246e",  # Hexxed
	"Mekka4e",  # Transformed
	"NEW1_025e",  # Bolstered (Unused)
	"XXX_009e",  # Empty Enchant
	"XXX_058e",  # Weapon Nerf Enchant

	# Dynamic buffs set by their parent
	"EX1_304e",  # Consume (Void Terror)
	"NEW1_018e",  # Treasure Crazed (Bloodsail Raider)
)


for cardset in CARD_SETS:
	CARD_SETS[cardset] = importlib.import_module("fireplace.cards.%s" % (cardset))


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

	for id in sorted(cards.db):
		card = cards.db[id]
		description = cleanup_description(card.description)
		implemented = False

		if not description:
			# Minions without card text or with basic abilities are implemented
			implemented = True
		elif card.type == CardType.ENCHANTMENT:
			if id in buffs.__dict__:
				implemented = True
			else:
				implemented = False
		elif card.card_set == CardSet.CREDITS:
			implemented = True

		if id in DUMMY_CARDS:
			implemented = True

		for set in CARD_SETS.values():
			if hasattr(set, id):
				implemented = True
				break
		else:
			if "Enrage" in card.description or card.choose_cards:
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
