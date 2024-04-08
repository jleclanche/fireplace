from ..utils import *


##
# Minions


class TRL_247:
    """Soulwarden"""

    # <b>Battlecry:</b> Add 3 random cards you discarded this game to your hand.
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY + DISCARDED) * 3))


class TRL_251:
    """Spirit of the Bat"""

    # <b>Stealth</b> for 1 turn. After a friendly minion dies, give a minion in your hand
    # +1/+1.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Death(FRIENDLY_MINIONS).on(Buff(RANDOM(FRIENDLY_HAND + MINION), "TRL_251e")),
    )


TRL_251e = buff(+1, +1)


class TRL_252:
    """High Priestess Jeklik"""

    # [x]<b>Taunt</b>, <b>Lifesteal</b> When you discard this, add 2 copies of it to your
    # hand.
    discard = Give(CONTROLLER, Copy(SELF)) * 2


class TRL_253:
    """Hir'eek, the Bat"""

    # <b>Battlecry:</b> Fill your board with copies of this minion.
    play = SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 7


class TRL_257:
    """Blood Troll Sapper"""

    # After a friendly minion dies, deal 2 damage to the enemy hero.
    events = Death(FRIENDLY_MINIONS).on(Hit(FRIENDLY_HERO, 2))


class TRL_551:
    """Reckless Diretroll"""

    # <b>Taunt</b> <b>Battlecry:</b> Discard your lowest Cost card.
    play = Discard(LOWEST_COST(FRIENDLY_HAND))


##
# Spells


class TRL_245:
    """Shriek"""

    # Discard your lowest Cost card. Deal $2 damage to all minions.
    play = (Discard(LOWEST_COST(FRIENDLY_HAND)), Hit(ALL_MINIONS, 2))


class TRL_246:
    """Void Contract"""

    # Destroy half of each player's deck.
    play = (
        Destroy(RANDOM(FRIENDLY_DECK)) * (Count(FRIENDLY_DECK) / 2),
        Destroy(RANDOM(ENEMY_DECK)) * (Count(ENEMY_DECK) / 2),
    )


class TRL_249:
    """Grim Rally"""

    # Destroy a friendly minion. Give your minions +1/+1.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET), Buff(FRIENDLY_MINIONS, "TRL_249e")


TRL_249e = buff(+1, +1)


class TRL_555:
    """Demonbolt"""

    # Destroy a minion. Costs (1) less for each minion you control.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    cost_mod = -Count(FRIENDLY_MINIONS)
    play = Destroy(TARGET)
