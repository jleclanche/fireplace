#!/usr/bin/env python
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
	"Can't Attack",
	"Always wins Brawls.",
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
	"tourney": None,
}


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
	for id in sorted(cards.db):
		card = cards.db[id]
		description = cleanup_description(card.description)
		if not description:
			# Minions without card text or with basic abilities are implemented
			color = GREEN
		elif card.type == CardType.ENCHANTMENT:
			if id in buffs.__dict__:
				color = GREEN
		elif card.card_set == CardSet.CREDITS:
			color = GREEN
		else:
			for set in CARD_SETS.values():
				if hasattr(set, id):
					color = GREEN
					break
			else:
				if "Enrage" in card.description or card.choose_cards:
					color = GREEN
				else:
					color = RED

		name = color + "%s: %s" % (PREFIXES[color], card.name) + ENDC
		print("%s (%s)" % (name, id))


if __name__ == "__main__":
	main()
