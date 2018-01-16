import argparse
import sys
import urllib.parse
import re

from hearthstone.enums import CardSet
from hearthstone.stringsfile import load_globalstrings

if __name__ == '__main__':
	sys.path.append("..")

from implemented import resolve_implemented_cards

FILE_HEADER = (
"""
\"\"\"
Card Definitions for {expansion_name}
Part of Fireplace: The Hearthstone simulator in Python
\"\"\"
""")

CARDDEF_TEMPLATE = (
"""

# class {id}:
# \t\"\"\" 
# \t{name} - ({type})
# \t{description}
# \t{link}
# \t\"\"\"
{battlecry}\
{deathrattle}\
# \tpass
""")

BATTLECRY_LINE = (
"""\
# \t# play = None
"""
)
DEATHRATTLE_LINE = (
"""\
# \t# deathrattle = None
"""
)


def make_gamepedia_link(card):
	return "https://hearthstone.gamepedia.com/" + urllib.parse.quote_plus(card.name.replace(" ", "_"))


def prettify_description(description):
	ret = description
	ret = re.sub("<i>.+</i>", "", ret)
	ret = re.sub("(<b>|</b>)", "", ret)
	ret = re.sub("<[^>]*>", "", ret)
	ret = re.sub("\[x]", "", ret)
	ret = re.sub("[\r\n\t\f]", " ", ret)

	return ret


def main(*args):
	parser = argparse.ArgumentParser(description='Create boilerplate for a new expansion.')

	parser.add_argument('--output', type=argparse.FileType('w', encoding='UTF-8'))
	args = parser.parse_args(args)

	outfile = args.output

	globalstrings = load_globalstrings()

	standard_card_sets = list(filter(lambda x: x.is_standard, list(CardSet)))

	for i, cardset in enumerate(standard_card_sets):
		print("{} - {}".format(i + 1, globalstrings[cardset.name_global]['TEXT']))

	cardset_selection = int(input("Select a Card Set (1-{}): ".format(len(list(standard_card_sets)))))

	card_set = standard_card_sets[cardset_selection - 1]

	outfile.write(FILE_HEADER.format(
		expansion_name=globalstrings[card_set.name_global]['TEXT']
	))

	implemented, unimplemented = resolve_implemented_cards()

	for card in unimplemented:

		if card.card_set != card_set:
			continue

		outfile.write(CARDDEF_TEMPLATE.format(
			id=card.id,
			name=card.name,
			type=globalstrings[card.type.name_global]['TEXT'],
			description=prettify_description(card.description),
			link=make_gamepedia_link(card),
			battlecry=BATTLECRY_LINE if card.battlecry else "",
			deathrattle=DEATHRATTLE_LINE if card.deathrattle else "",
		))

	outfile.close()


if __name__ == '__main__':
	sys.path.append("..")
	main(*sys.argv[1:])
