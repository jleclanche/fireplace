#!/usr/bin/env python
import re
import string
import sys; sys.path.append(".."); sys.path.append("../data/extras")
from data.extras import chooseone
from fireplace import cards
from fireplace.cards import debug, game, tutorial, classic, naxxramas, gvg, blackrock
from fireplace.enums import CardType, CardSet

import buffs


GREEN = "\033[92m"
YELLOW = "\033[33m"
RED = "\033[91m"
ENDC = "\033[0m"
PREFIXES = {
	GREEN: "Implemented",
	YELLOW: "Potentially implemented",
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


def cleanup_description(description):
	ret = description
	ret = re.sub("<i>.+</i>", "", ret)
	ret = re.sub("(<b>|</b>)", "", ret)
	ret = re.sub("(" + "|".join(SOLVED_KEYWORDS) + ")", "", ret)
	ret = re.sub("<[^>]*>", "", ret)
	exclude_chars = string.punctuation + string.whitespace
	ret = "".join([ch for ch in ret if ch not in exclude_chars])
	return ret


def potentially_implemented(card):
	return card.auras or "Enrage" in card.description or hasattr(chooseone, card.id)


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
			for set in (debug, game, tutorial, classic, naxxramas, gvg, blackrock):
				if hasattr(set, id):
					color = GREEN
					break
			else:
				if potentially_implemented(card):
					color = YELLOW
				else:
					color = RED

		name = color + "%s: %s" % (PREFIXES[color], card.name) + ENDC
		print("%s (%s)" % (name, id))


if __name__ == "__main__":
	main()
