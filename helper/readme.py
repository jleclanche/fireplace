#!/usr/bin/env python
from hearthstone.enums import CardSet
from utils import *

from fireplace import cards


VERSION = "17.6.0.53261"
WIKI_HOST = "https://hearthstone.wiki.gg/wiki"

CARD_SET_NAME = {
    CardSet.BASIC: "Basic",
    CardSet.EXPERT1: "Classic",
    CardSet.HOF: "Hall of Fame",
    CardSet.NAXX: "Curse of Naxxramas",
    CardSet.GVG: "Goblins vs Gnomes",
    CardSet.BRM: "Blackrock Mountain",
    CardSet.TGT: "The Grand Tournament",
    CardSet.HERO_SKINS: "Hero Skins",
    CardSet.TB: "Tavern Brawl",
    CardSet.LOE: "The League of Explorers",
    CardSet.OG: "Whispers of the Old Gods",
    CardSet.KARA: "One Night in Karazhan",
    CardSet.GANGS: "Mean Streets of Gadgetzan",
    CardSet.UNGORO: "Journey to Un'Goro",
    CardSet.ICECROWN: "Knights of the Frozen Throne",
    CardSet.LOOTAPALOOZA: "Kobolds & Catacombs",
    CardSet.GILNEAS: "The Witchwood",
    CardSet.BOOMSDAY: "The Boomsday Project",
    CardSet.TROLL: "Rastakhan's Rumble",
    CardSet.DALARAN: "Rise of Shadows",
    CardSet.ULDUM: "Saviours of Uldum",
    CardSet.DRAGONS: "Descent of Dragons",
    CardSet.BLACK_TEMPLE: "Ashes of Outlands",
    CardSet.WILD_EVENT: "Wild Event",
    CardSet.YEAR_OF_THE_DRAGON: "Galakrond's Awakening",
    CardSet.SCHOLOMANCE: "Scholomance Academy",
    CardSet.DEMON_HUNTER_INITIATE: "Demon Hunter Initiate",
}


def main():
    cards.db.initialize()
    unimpl_cards = []

    print(f"{BLUE}## Cards Implementation{ENDC}")
    print()
    print(f"{BLUE}Now updated to [Patch {VERSION}]({WIKI_HOST}/Patch_{VERSION}){ENDC}")

    for card_set in CardSet:
        impl = 0
        unimpl = 0
        for id in cards.db.filter(
            card_set=card_set,
            collectible=True,
            can_pick_from_subsets=True,
            include_default_hero=True,
        ):
            card = cards.db[id]
            implemented = check_implemented(card)

            if implemented:
                impl += 1
            else:
                unimpl += 1
                unimpl_cards.append(card)

        total = impl + unimpl
        if total > 0:
            if impl == total:
                color = GREEN
            elif impl == 0:
                color = RED
            else:
                color = YELLOW
            print(
                "%s* **%i%%** %s (%i of %i card%s)%s"
                % (
                    color,
                    (impl / total) * 100,
                    CARD_SET_NAME[card_set],
                    impl,
                    total,
                    "s" if total > 1 else "",
                    ENDC,
                )
            )

    if unimpl_cards:
        print()
        print(f"{RED}Not Implemented{ENDC}")
        for card in unimpl_cards:
            print(f"{RED}* {card.name} ({card.id}){ENDC}")


if __name__ == "__main__":
    main()
