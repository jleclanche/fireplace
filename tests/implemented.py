#!/usr/bin/env python
import re
import string
import sys; sys.path.append(".."); sys.path.append("../data/extras")
from data.extras import chooseone
from fireplace import cards
from fireplace.cards import debug, game, classic, naxxramas, gvg, blackrock
from fireplace.enums import CardType

import buffs


GREEN = "\033[92m"
YELLOW = "\033[33m"
RED = "\033[91m"
ENDC = "\033[0m"
PREFIXES = {
	GREEN: "Implemented: ",
	YELLOW: "Potentially implemented: ",
	RED: "Not implemented: ",
}

SOLVED_KEYWORDS = [
	"Windfury", "Charge", "Divine Shield", "Taunt", "Stealth",
	"Spell Damage \+[0-9]+",
	"Can't be targeted by spells or Hero Powers",
	"Overload: \([0-9]+\)",
	"50% chance to attack the wrong enemy",
	"Can't Attack",
]


def cleanup_description(description):
	ret = description
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
		if not cleanup_description(card.description):
			# Minions without card text or with basic abilities are implemented
			color = GREEN
		elif card.type == CardType.ENCHANTMENT:
			if id in buffs.__dict__:
				color = GREEN
		else:
			for set in (debug, game, classic, naxxramas, gvg, blackrock):
				if hasattr(set, id):
					color = GREEN
					break
			else:
				if potentially_implemented(card):
					color = YELLOW
				else:
					color = RED
		print(color + PREFIXES[color] + card.name + ENDC + " (%s)" % (id))


if __name__ == "__main__":
	main()
