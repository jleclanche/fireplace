import argparse
import sys
import urllib.parse
import re
from itertools import groupby
import inspect

from hearthstone.enums import CardSet
from hearthstone.stringsfile import load_globalstrings

if __name__ == '__main__':
	sys.path.append("..")

from implemented import resolve_implemented_cards
from fireplace.utils import get_script_definition

FILE_HEADER = (
"""
\"\"\"
Card Definitions for {expansion_name}
Part of Fireplace: The Hearthstone simulator in Python
\"\"\"

from ..utils import *
""")

CARDDEF_TEMPLATE = (
"""

class {id}:
	\"\"\" 
	{name} - ({type})
	{description}
	{link}
	\"\"\"
{line1}\
{line2}\
{line3}\
""")

BATTLECRY_LINE = (
"""\
	play = None
"""
)
DEATHRATTLE_LINE = (
"""\
	deathrattle = None
"""
)
PASS_LINE = (
"""\
	pass
"""
)

PLAYER_CLASS_COMMENT = (
"""
###############################################################################
##                                                                           ##
##{:^75}##
##                                                                           ##
###############################################################################
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

	parser.add_argument('--output', type=argparse.FileType('w', encoding='UTF-8'), help="Output file "
																						"(use - for stdout)")
	parser.add_argument('--parse-user-implemented', action='store_true', help="Will try to parse and include any "
																			  "old-style card definitions. (use "
																			  "carefully) - silent errors possible")
	args = parser.parse_args(args)

	outfile = args.output

	globalstrings = load_globalstrings()
	existing_implementation_regex = "class {id}:\n\t\"([^\"]*)\"\n((?s)(?:(?!\nclass|\n# class).)*)"

	standard_card_sets = list(filter(lambda x: x.is_standard, list(CardSet)))

	for i, cardset in enumerate(standard_card_sets):
		print("{} - {}".format(i + 1, globalstrings[cardset.name_global]['TEXT']))

	cardset_selection = int(input("Select a Card Set (1-{}): ".format(len(list(standard_card_sets)))))

	card_set = standard_card_sets[cardset_selection - 1]

	outfile.write(FILE_HEADER.format(
		expansion_name=globalstrings[card_set.name_global]['TEXT']
	))

	implemented, unimplemented = resolve_implemented_cards()

	if args.parse_user_implemented:
		user_implemented = set(filter(lambda x:
									x.description is not None
									and get_script_definition(x.id) is not None,
								  implemented))
	else:
		user_implemented = set()

	unimplemented = user_implemented | unimplemented

	unimplemented = filter(lambda x: x.card_set == card_set, unimplemented)
	unimplemented = sorted(unimplemented, key=lambda x: (-x.card_class, x.id))

	for key, group in groupby(unimplemented, key=lambda x: x.card_class):

		outfile.write(PLAYER_CLASS_COMMENT.format(globalstrings[key.name_global]['TEXT']))

		for card in group:

			if card in user_implemented: # this card already has an implementation. Copy it

				regex = existing_implementation_regex.format(id=card.id)
				# find the card's file
				f = inspect.getsourcefile(get_script_definition(card.id))

				with open(f, 'r') as sourcefile:
					source = sourcefile.read()
					match = re.search(regex, source)
					if match is None:
						continue
					if match.group(2) == "":
						print(card.id)
						print(repr(regex))
						print(source)
						print("-----")
						print(match.group(2))
						exit()
					outfile.write(CARDDEF_TEMPLATE.format(
						id=card.id,
						name=card.name,
						type=globalstrings[card.type.name_global]['TEXT'],
						description=prettify_description(card.description),
						link=make_gamepedia_link(card),
						line1=match.group(2),
						line2="",
						line3=""
					))
			else:
				outfile.write(CARDDEF_TEMPLATE.format(
					id=card.id,
					name=card.name,
					type=globalstrings[card.type.name_global]['TEXT'],
					description=prettify_description(card.description),
					link=make_gamepedia_link(card),
					line1=BATTLECRY_LINE if card.battlecry else "",
					line2=DEATHRATTLE_LINE if card.deathrattle else "",
					line3=PASS_LINE if not card.battlecry and not card.deathrattle else "",
				).replace("\n", "\n# ")) # comment out the block

	outfile.close()


if __name__ == '__main__':
	sys.path.append("..")
	main(*sys.argv[1:])
