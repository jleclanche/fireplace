#!/usr/bin/env python
import argparse
import re
import string
import sys

if __name__ == "__main__":
	sys.path.append("..")

from fireplace import cards
from fireplace.utils import get_script_definition
from hearthstone.enums import CardSet
from hearthstone.stringsfile import load_globalstrings

GREEN = "\033[92m"
RED = "\033[91m"
ORANGE = "\u001b[38;5;208m"
ENDC = "\033[0m"
PREFIXES = {
	GREEN: "Implemented",
	RED: "Not implemented",
}

SOLVED_KEYWORDS = [
	"Windfury", "Charge", "Divine Shield", "Taunt", "Stealth", "Lifesteal",
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


def resolve_implemented_cards():
	implemented_cards = set()
	unimplemented_cards = set()

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

		if implemented:
			implemented_cards.add(card)
		else:
			unimplemented_cards.add(card)

	return implemented_cards, unimplemented_cards


def main():
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

	implemented_cards, unimplemented_cards = resolve_implemented_cards()

	for card in sorted(implemented_cards | unimplemented_cards, key=lambda x: x.id):

		implemented = card in implemented_cards

		color = GREEN if implemented else RED
		name = color + "%s: %s" % (PREFIXES[color], card.name) + ENDC

		if args.unimplemented and not implemented:
			print("%s (%s)" % (name, card.id))
		elif args.implemented and implemented:
			print("%s (%s)" % (name, card.id))

	total = len(implemented_cards) + len(unimplemented_cards)

	globalstrings = load_globalstrings()
	print("\nState of Implementation (Standard Cards)\n")

	card_set_impl_details = []

	for card_set in CardSet:
		if not card_set.is_standard:
			continue

		impl = sum(c.card_set == card_set for c in implemented_cards)
		unimpl = sum(c.card_set == card_set for c in unimplemented_cards)

		color = GREEN if unimpl == 0 else ORANGE
		card_set_name = color + globalstrings[card_set.name_global]['TEXT'] + ENDC

		card_set_impl_details.append((globalstrings[card_set.name_global]['TEXT'], impl, unimpl))

		print("{}: {}/{} cards implemented ({:.1f}%)".format(card_set_name, impl, impl + unimpl,
															 100 * impl / (impl + unimpl)))

	standard_impl = sum(c.card_set.is_standard for c in implemented_cards)
	standard_unimpl = sum(c.card_set.is_standard for c in unimplemented_cards)
	standard_total = standard_impl + standard_unimpl

	standard_percentage = (standard_impl / standard_total) * 100

	print("%i / %i of standard cards implemented (%i%%)" % (standard_impl, standard_total, standard_percentage))

	print("%i / %i cards implemented (%i%%)" % (len(implemented_cards), total, (len(implemented_cards) / total) * 100))

	return card_set_impl_details, standard_percentage


if __name__ == "__main__":
	main()
