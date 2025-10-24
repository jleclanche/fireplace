from ..utils import *


##
# Minions


class UNG_840:
    """Hemet, Jungle Hunter"""

    play = Destroy(FRIENDLY_DECK + (COST <= 3))


class UNG_843:
    """The Voraxx"""

    events = Play(CONTROLLER, SPELL, SELF).after(
        CastSpell(Play.CARD, Summon(CONTROLLER, "UNG_999t2t1"))
    )


class UNG_851:
    """Elise the Trailblazer"""

    play = Shuffle(CONTROLLER, "UNG_851t1")


class UNG_851t1:
    """Un\'Goro Pack"""

    play = Give(CONTROLLER, RandomCollectible(card_set=CardSet.UNGORO)) * 5


class UNG_900:
    """Spiritsinger Umbra"""

    events = Summon(CONTROLLER, MINION).after(Deathrattle(Summon.CARD))


class UNG_907:
    """Ozruk"""

    play = Buff(SELF, "UNG_907e") * Attr(CONTROLLER, enums.ELEMENTAL_PLAYED_LAST_TURN)


UNG_907e = buff(health=5)
