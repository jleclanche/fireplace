#!/usr/bin/env python
import argparse
import os
import sys
import textwrap

from hearthstone.enums import CardClass, CardSet, CardType, Rarity
from utils import *

from fireplace import cards


def single_card(card):
    tab = " " * 4
    str = ""
    str += "\n\n"
    str += f"class {card.id}:\n"
    str += f'{tab}"""{card.name}"""\n'
    str += "\n"
    description_lines = []
    for des in card.description.split("\n"):
        description_lines.append(des.strip())
    description = " ".join(description_lines)
    for des in textwrap.wrap(description, width=73):
        str += f"{tab}# {des}\n"
    if card.requirements:
        str += f"{tab}requirements = {{\n"
        for req, value in card.requirements.items():
            str += f"{tab}{tab}PlayReq.{req.name}: {value},\n"
        str += f"{tab}}}\n"
    str += f"{tab}pass\n"
    return str


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--card_set",
        dest="card_set",
        type=int,
        default=CardSet.BLACK_TEMPLE,
        help="Generate cards of card set",
    )
    p.add_argument("--card_id", dest="card_id", help="Generate single card")
    p.add_argument(
        "--output_dir",
        dest="output_dir",
        default="./fireplace/cards/outlands",
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
        out.write("from .demonhunter import *\n")
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
        {"card_class": CardClass.DEMONHUNTER},
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
                args.output_dir
                + "/"
                + card_class.name.lower()
                + "_"
                + rarity.name.lower()
                + ".py"
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
                card_set=args.card_set,
                collectible=True,
                type=card_type,
                can_pick_from_subsets=True,
                **kw,
            ):
                card = cards.db[id]
                implemented = check_implemented(card)
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
