#!/usr/bin/env python
import argparse
import os
import re
import string
import sys
import textwrap

from hearthstone.enums import CardClass, CardSet, CardType, Rarity

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
	"Windfury",
	"Charge",
	"Divine Shield",
	"Taunt",
	"Stealth",
	"Poisonous",
	"Lifesteal",
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


def single_card(card):
	str = ""
	str += "\n\n"
	str += f"class {card.id}:\n"
	str += f'\t"""{card.name}"""\n'
	description_lines = []
	for des in card.description.split("\n"):
		description_lines.append(des.strip())
	description = " ".join(description_lines)
	for des in textwrap.wrap(description, width=85):
		str += f"\t# {des}\n"
	str += "\tpass\n"
	return str


def main():
	p = argparse.ArgumentParser()
	p.add_argument(
		"--card_set",
		dest="card_set",
		type=int,
		default=CardSet.GILNEAS,
		help="Generate cards of card set"
	)
	p.add_argument(
		"--card_id",
		dest="card_id",
		help="Generate single card"
	)
	p.add_argument(
		"--output_dir",
		dest="output_dir",
		default="./fireplace/cards/witchwood",
		help="Generate code output dir",
	)
	args = p.parse_args(sys.argv[1:])
	cards.db.initialize()

	if args.card_id:
		card = cards.db[args.card_id]
		print(single_card(card))
		return

	os.makedirs(args.output_dir, exist_ok=True)

	with open(f"{args.output_dir}/__init__.py", "a") as out:
		out.write("from .druid import *\n")
		out.write("from .hunter import *\n")
		out.write("from .mage import *\n")
		out.write("from .paladin import *\n")
		out.write("from .priest import *\n")
		out.write("from .rogue import *\n")
		out.write("from .shaman import *\n")
		out.write("from .warlock import *\n")
		out.write("from .warrior import *\n")
		out.write("from .neutral_common import *\n")
		out.write("from .neutral_rare import *\n")
		out.write("from .neutral_epic import *\n")
		out.write("from .neutral_legendary import *\n")

	kws = [
		{"card_class": CardClass.DRUID},
		{"card_class": CardClass.HUNTER},
		{"card_class": CardClass.MAGE},
		{"card_class": CardClass.PALADIN},
		{"card_class": CardClass.PRIEST},
		{"card_class": CardClass.ROGUE},
		{"card_class": CardClass.SHAMAN},
		{"card_class": CardClass.WARLOCK},
		{"card_class": CardClass.WARRIOR},
		{"card_class": CardClass.NEUTRAL, "rarity": Rarity.COMMON},
		{"card_class": CardClass.NEUTRAL, "rarity": Rarity.RARE},
		{"card_class": CardClass.NEUTRAL, "rarity": Rarity.EPIC},
		{"card_class": CardClass.NEUTRAL, "rarity": Rarity.LEGENDARY},
	]
	for kw in kws:
		card_class = kw["card_class"]
		if card_class == CardClass.NEUTRAL:
			rarity = kw["rarity"]
			filename = (
				args.output_dir + "/" + card_class.name.lower() + "_" + rarity.name.lower() + ".py"
			)
		else:
			filename = args.output_dir + "/" + card_class.name.lower() + ".py"

		with open(filename, "a+") as out:
			out.write("from ..utils import *\n")

		for card_type in [
			CardType.MINION,
			CardType.SPELL,
			CardType.WEAPON,
			CardType.HERO,
		]:
			tmp_cards = []
			for id in cards.filter(
				card_set=args.card_set, collectible=True, type=card_type, **kw
			):
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

				if not implemented:
					tmp_cards.append(card)
			if len(tmp_cards) > 0:
				with open(filename, "a+") as out:
					out.write("\n\n")
					out.write("##\n")
					out.write(f"# {card_type.name.capitalize()}s")
					for card in tmp_cards:
						out.write(single_card(card))


if __name__ == "__main__":
	main()
