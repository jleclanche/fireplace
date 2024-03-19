#!/usr/bin/env python
from importlib import import_module

from hearthstone.enums import CardType
from utils import *

from fireplace import cards
from fireplace.utils import CARD_SETS


def main():
	cards.db.initialize()

	for id in cards.db:
		card = cards.db[id]
		for cardset in CARD_SETS:
			module_dir = f"fireplace.cards.{cardset}"
			module = import_module(module_dir)
			if hasattr(module, id):
				carddef = getattr(module, id)
				if (
					card.requirements and
					not hasattr(carddef, "requirements") and
					card.type != CardType.ENCHANTMENT
				):
					print(GREEN, card.name, ENDC)

					req_lines = []
					req_lines.append("\trequirements = {\n")
					for req, value in card.requirements.items():
						req_lines.append(f"\t\tPlayReq.{req.name}: {value},\n")
					req_lines.append("\t}\n")

					filepath = carddef.__module__.replace(".", "/") + ".py"
					with open(filepath, "r") as f:
						lines = f.readlines()

					finded = False

					for i, line in enumerate(lines):
						if not finded:
							if line.startswith(f"class {id}:") or line.startswith(f"class {id}("):
								finded = True
						else:
							if not line.startswith('\t"') and not line.startswith("\t#"):
								lines = lines[:i] + req_lines + lines[i:]
								break

					with open(filepath, "w") as f:
						f.writelines(lines)


if __name__ == "__main__":
	main()
