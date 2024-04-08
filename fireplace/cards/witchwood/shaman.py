from ..utils import *


##
# Minions


class GIL_530:
    """Murkspark Eel"""

    # <b>Battlecry:</b> If your deck has only even-Cost cards, deal_2 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_ONLY_EVEN_COST_CARD_IN_DECK: 0,
    }
    powered_up = EvenCost(FRIENDLY_DECK)
    play = powered_up & Hit(TARGET, 2)


class GIL_531:
    """Witch's Apprentice"""

    # <b>Taunt</b> <b>Battlecry:</b> Add a random Shaman spell to your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))


class GIL_583:
    """Totem Cruncher"""

    # <b>Taunt</b> <b>Battlecry:</b> Destroy your Totems. Gain +2/+2 for each destroyed.
    play = Destroy(FRIENDLY_MINIONS + TOTEM).then(Buff(SELF, "GIL_583e"))


GIL_583e = buff(+2, +2)


class GIL_807:
    """Bogshaper"""

    # Whenever you cast a spell, draw a minion from your_deck.
    events = Play(CONTROLLER, SPELL).after(ForceDraw(FRIENDLY_DECK + MINION))


class GIL_820:
    """Shudderwock"""

    # [x]<b>Battlecry:</b> Repeat all other <b>Battlecries</b> from cards you played this
    # game <i>(targets chosen randomly)</i>.
    play = ExtraBattlecry(
        RANDOM(CARDS_PLAYED_THIS_GAME + BATTLECRY - ID("GIL_820")) * 30, None
    )


##
# Spells


class GIL_586:
    """Earthen Might"""

    # [x]Give a minion +2/+2. If it's an Elemental, add a random Elemental to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(TARGET, "GIL_586e"),
        Find(TARGET + ELEMENTAL) & Give(CONTROLLER, RandomElemental()),
    )


GIL_586e = buff(+2, +2)


class GIL_600:
    """Zap!"""

    # Deal $2 damage to a minion. <b>Overload:</b> (1)
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class GIL_836:
    """Blazing Invocation"""

    # <b>Discover</b> a <b>Battlecry</b> minion.
    play = DISCOVER(RandomMinion(battlecry=True))


##
# Heros


class GIL_504:
    """Hagatha the Witch"""

    # <b>Battlecry:</b> Deal 3 damage to all minions.
    play = Hit(ALL_MINIONS, 3)


class GIL_504h:
    """Bewitch"""

    # [x]<b>Passive Hero Power</b> After you play a minion, add a random Shaman spell to
    # your hand.
    tags = {enums.PASSIVE_HERO_POWER: True}
    events = Play(CONTROLLER, MINION).on(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))
    )
