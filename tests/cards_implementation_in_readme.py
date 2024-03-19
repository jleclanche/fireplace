#!/usr/bin/env python
import argparse
import re
import string
import sys

from hearthstone.enums import CardSet, GameTag

from fireplace import cards
from fireplace.utils import get_script_definition


sys.path.append("..")


GREEN = "\033[92m"
RED = "\033[91m"
ENDC = "\033[0m"
PREFIXES = {
	GREEN: "Implemented",
	RED: "Not implemented",
}

SOLVED_KEYWORDS = [
	"[x]",
	"Windfury",
	"Charge",
	"Divine Shield",
	"Taunt",
	"Stealth",
	"Poisonous",
	"Lifesteal",
	"Rush",
	"Echo",
	"Reborn",
	r"Can't be targeted by spells or Hero Powers\.",
	r"Can't attack\.",
	"Destroy any minion damaged by this minion.",
	r"Your Hero Power deals \d+ extra damage.",
	r"Spell Damage \+\d+",
	r"Overload: \(\d+\)",
	r"This is an Elemental, Mech,\nDemon, Murloc, Dragon,\nBeast, Pirate and Totem\.",
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

	# Kazakus Potion
	"CFM_621t",  # Kazakus Potion
	"CFM_621t11",  # Lesser Potion
	"CFM_621t12",  # Greater Potion
	"CFM_621t13",  # Superior Potion
	"CFM_621t14",  # Kazakus Potion
	"CFM_621t15",  # Kazakus Potion

	"CFM_643e2",  # Smuggling
	"CFM_668t",  # Doppelgangster
	"CFM_668t2",  # Doppelgangster

	"OG_118e",  # Renounce Darkness

	# The Boomsday Project
	"BOT_914",  # Whizbang the Wonderful

	# Rise of Shadows
	"DAL_800",  # Zayle, Shadow Cloak
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
	cards.db.initialize()
	unimpl_cards = []
	for card_set in CardSet:
		impl = 0
		unimpl = 0
		for id in cards.db.filter(card_set=card_set, collectible=True):
			card = cards.db[id]

			if card.tags.get(GameTag.HIDE_WATERMARK, 0):
				continue

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
				impl += 1
			else:
				unimpl += 1
				unimpl_cards.append(card)

		total = impl + unimpl
		if total > 0:
			print("* **%i%** %s (%i of %i cards)", (impl / total) * 100, card_set.name, impl, total)


if __name__ == "__main__":
	main()
