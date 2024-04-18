import os
from importlib import import_module

from hearthstone import cardxml
from hearthstone.enums import CardType, GameTag, Race, ZodiacYear

from ..enums import BoardEnum
from ..logging import log
from ..utils import CARD_SETS


year = ZodiacYear.PHOENIX
default_language = "enUS"
standard_board_skins = [
    BoardEnum.STORMWIND,
    BoardEnum.ORGRIMMAR,
    BoardEnum.PANDARIA,
    BoardEnum.STRANGLETHORN,
    BoardEnum.DALARAN,
    BoardEnum.ULDUM_TOMB,
    BoardEnum.ULDUM_CITY,
    BoardEnum.DRAGONBLIGHT,
    BoardEnum.OUTLAND,
]


def get_script_definition(id, card=None):
    """
    Find and return the script definition for card
    """
    if not card:
        card = db[id]

    if GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID in card.tags:
        dbf_id = card.tags[GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID]
        if dbf_id < card.dbf_id and dbf_id in db.dbf:
            id = db.dbf[dbf_id]

    for cardset in CARD_SETS:
        module = import_module("fireplace.cards.%s" % (cardset))
        if hasattr(module, id):
            cls = getattr(module, id)
            methods = [
                attr
                for attr in dir(cls)
                if not (attr.startswith("__") or attr.endswith("__"))
            ]
            if len(methods) > 0:
                return cls


class CardDB(dict[str, cardxml.CardXML]):
    def __init__(self):
        self.initialized = False
        self.dbf = {}

    @staticmethod
    def merge(id, card, cardscript=None):
        """
        Find the xmlcard and the card definition of \a id
        Then return a merged class of the two
        """
        if card is None:
            card = cardxml.CardXML(id)

        if cardscript is None:
            cardscript = get_script_definition(id, card)

        if cardscript:
            card.scripts = type(id, (cardscript,), {})
        else:
            card.scripts = type(id, (), {})

        scriptnames = (
            "activate",
            "combo",
            "deathrattle",
            "draw",
            "inspire",
            "play",
            "enrage",
            "update",
            "powered_up",
            "outcast",
            "awaken",
            "reward",
            "add_progress",
            "discard",
            "secret_deathrattles",
            "magnetic",
            "overkill",
        )

        for script in scriptnames:
            actions = getattr(card.scripts, script, None)
            if actions is None:
                # Set the action by default to avoid runtime hasattr() calls
                setattr(card.scripts, script, ())
            elif not callable(actions):
                if not hasattr(actions, "__iter__"):
                    # Ensure the actions are always iterable
                    setattr(card.scripts, script, (actions,))

        for script in ("events", "secret", "quest", "sidequest", "dormant_events"):
            events = getattr(card.scripts, script, None)
            if events is None:
                setattr(card.scripts, script, [])
            elif not hasattr(events, "__iter__"):
                setattr(card.scripts, script, [events])

        if not hasattr(card.scripts, "cost_mod"):
            card.scripts.cost_mod = None

        if not hasattr(card.scripts, "Hand"):
            card.scripts.Hand = type("Hand", (), {})

        if not hasattr(card.scripts.Hand, "events"):
            card.scripts.Hand.events = []

        if not hasattr(card.scripts.Hand.events, "__iter__"):
            card.scripts.Hand.events = [card.scripts.Hand.events]

        if not hasattr(card.scripts.Hand, "update"):
            card.scripts.Hand.update = ()

        if not hasattr(card.scripts.Hand.update, "__iter__"):
            card.scripts.Hand.update = (card.scripts.Hand.update,)

        if not hasattr(card.scripts, "Deck"):
            card.scripts.Deck = type("Deck", (), {})

        if not hasattr(card.scripts.Deck, "events"):
            card.scripts.Deck.events = []

        if not hasattr(card.scripts.Deck.events, "__iter__"):
            card.scripts.Deck.events = [card.scripts.Deck.events]

        if not hasattr(card.scripts.Deck, "update"):
            card.scripts.Deck.update = ()

        if not hasattr(card.scripts.Deck.update, "__iter__"):
            card.scripts.Deck.update = (card.scripts.Deck.update,)

        # Set choose one cards
        if hasattr(cardscript, "choose"):
            card.choose_cards = cardscript.choose[:]
        else:
            card.choose_cards = []

        if hasattr(cardscript, "tags"):
            for tag, value in cardscript.tags.items():
                card.tags[tag] = value

        if hasattr(cardscript, "requirements"):
            card.requirements = cardscript.requirements
        else:
            card.requirements = {}

        if hasattr(cardscript, "entourage"):
            card.entourage = cardscript.entourage
        else:
            card.entourage = []

        if hasattr(cardscript, "progress_total"):
            card.scripts.progress_total = cardscript.progress_total
        else:
            card.scripts.progress_total = 0

        if hasattr(cardscript, "dormant_turns"):
            card.scripts.dormant_turns = cardscript.dormant_turns
        else:
            card.scripts.dormant_turns = 0

        if hasattr(cardscript, "cardtext_entity_0"):
            card.cardtext_entity_0 = cardscript.cardtext_entity_0

        if hasattr(cardscript, "cardtext_entity_1"):
            card.cardtext_entity_1 = cardscript.cardtext_entity_1

        card.is_standard = card.card_set in year.standard_card_sets

        return card

    def initialize(self, locale=default_language):
        log.info("Initializing card database")
        self.initialized = True
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "CardDefs.xml")
        db2, _ = cardxml.load(locale=locale)
        for id, card in db2.items():
            self.dbf[card.dbf_id] = id
        db, _ = cardxml.load(path=filename, locale=locale)
        for id, card in db.items():
            self[id] = self.merge(id, card)
            self.dbf[card.dbf_id] = id

        log.info("Merged %i cards", len(self))

    def filter(self, **kwargs):
        """
        Returns a list of card IDs matching the given filters. Each filter, if not
        None, is matched against the registered card database.
        cards.
        Examples arguments:
        \a collectible: Whether the card is collectible or not.
        \a type: The type of the card (hearthstone.enums.CardType)
        \a race: The race (tribe) of the card (hearthstone.enums.Race)
        \a rarity: The rarity of the card (hearthstone.enums.Rarity)
        \a cost: The mana cost of the card
        """
        if not self.initialized:
            self.initialize()

        cards = self.values()

        if "can_pick_from_subsets" not in kwargs:
            cards = [
                card
                for card in cards
                if not bool(card.tags.get(GameTag.DONT_PICK_FROM_SUBSETS))
            ]
        else:
            kwargs.pop("can_pick_from_subsets")

        # exclude default hero
        if "include_default_hero" not in kwargs:
            cards = [card for card in cards if not card.id.startswith("HERO_")]
        else:
            kwargs.pop("include_default_hero")

        if "type" not in kwargs:
            kwargs["type"] = [
                CardType.SPELL,
                CardType.WEAPON,
                CardType.HERO,
                CardType.MINION,
            ]

        if "race" in kwargs:
            kwargs["races"] = kwargs.pop("race")

        if "exclude" in kwargs:
            exclude = [card.id for card in kwargs.pop("exclude")]
            cards = [card for card in cards if card.id not in exclude]

        for attr, value in kwargs.items():
            if value is not None:
                # What? this doesn't work?
                # cards = __builtins__["filter"](lambda c: getattr(c, attr) == value, cards)

                if attr == "card_class":
                    if hasattr(value, "__iter__"):
                        cards = [
                            card
                            for card in cards
                            if any(v in card.classes for v in value)
                        ]
                    else:
                        cards = [card for card in cards if value in card.classes]
                if attr == "races":
                    cards = [card for card in cards if value in card.races]
                else:
                    cards = [
                        card
                        for card in cards
                        if (hasattr(value, "__iter__") and getattr(card, attr) in value)
                        or getattr(card, attr) == value
                    ]

        return [card.id for card in cards]


# Here we import every card from every set and load the cardxml database.
# For every card, we will "merge" the class with its Python definition if
# it exists.
if "db" not in globals():
    db = CardDB()
    filter = db.filter
