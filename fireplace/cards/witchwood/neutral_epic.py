from ..utils import *


##
# Minions


class GIL_117:
    """Worgen Abomination"""

    # At the end of your turn, deal 2 damage to all other damaged minions.
    events = OWN_TURN_END.on(Hit(ALL_MINIONS - SELF + DAMAGED, 2))


class GIL_124:
    """Mossy Horror"""

    # <b>Battlecry:</b> Destroy all other_minions with 2_or_less_Attack.
    play = Destroy(ALL_MINIONS - SELF + (ATK <= 2))


class GIL_581:
    """Sandbinder"""

    # <b>Battlecry:</b> Draw an Elemental from your deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + ELEMENTAL))


class GIL_614:
    """Voodoo Doll"""

    # <b>Battlecry:</b> Choose a minion. <b>Deathrattle:</b> Destroy the chosen minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    deathrattle = HAS_TARGET & Destroy(TARGET)


class GIL_616:
    """Splitting Festeroot"""

    # <b>Deathrattle:</b> Summon two 2/2 Splitting Saplings.
    deathrattle = Summon(CONTROLLER, "GIL_616t")


class GIL_616t:
    """Splitting Sapling"""

    # <b>Deathrattle:</b> Summon two 1/1 Woodchips.
    deathrattle = Summon(CONTROLLER, "GIL_616t2")


class GIL_682:
    """Muck Hunter"""

    # <b>Rush</b> <b>Battlecry:</b> Summon two 2/1_Mucklings for your opponent.
    play = Summon(OPPONENT, "GIL_682t") * 2


class GIL_815:
    """Baleful Banker"""

    # <b>Battlecry:</b> Choose a friendly minion. Shuffle a copy into your deck.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Shuffle(CONTROLLER, Copy(TARGET))


class GIL_819:
    """Witch's Cauldron"""

    # After a friendly minion dies, add a random Shaman spell to your hand.
    events = Death(FRIENDLY_MINIONS).on(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.SHAMAN))
    )
