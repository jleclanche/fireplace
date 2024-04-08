from ..utils import *


##
# Minions


class BOT_291:
    """Storm Chaser"""

    # <b>Battlecry:</b> Draw a spell from your deck that costs_(5) or more.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST >= 5)))


class BOT_407:
    """Thunderhead"""

    # [x]After you play a card with <b>Overload</b>, summon two 1/1 Sparks with
    # <b>Rush</b>.
    events = Play(CONTROLLER, OVERLOAD).after(
        SummonBothSides(CONTROLLER, "BOT_102t") * 2
    )


class BOT_411:
    """Electra Stormsurge"""

    # <b>Battlecry:</b> Your next spell this turn casts twice.
    play = Buff(CONTROLLER, "BOT_411e")


class BOT_411e:
    events = Play(CONTROLLER, SPELL).after(
        Battlecry(Play.CARD, Play.TARGET), Destroy(SELF)
    )


class BOT_533:
    """Menacing Nimbus"""

    # <b>Battlecry:</b> Add a random Elemental to your hand.
    play = Give(CONTROLLER, RandomElemental())


class BOT_543:
    """Omega Mind"""

    # [x]<b>Battlecry:</b> If you have 10 Mana Crystals, your spells have <b>Lifesteal</b>
    # this turn.
    powered_up = AT_MAX_MANA(CONTROLLER)
    play = powered_up & Buff(CONTROLLER, "BOT_543e")


class BOT_543e:
    update = Refresh(FRIENDLY + SPELL, {GameTag.LIFESTEAL: True})


##
# Spells


class BOT_093:
    """Elementary Reaction"""

    # Draw a card. Copy it if_you played an Elemental last turn.
    play = Draw(CONTROLLER).then(
        ELEMENTAL_PLAYED_LAST_TURN & Give(CONTROLLER, ExactCopy(Draw.CARD))
    )


class BOT_099:
    """Eureka!"""

    # Summon a copy of_a_random minion from your hand.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, ExactCopy(RANDOM(FRIENDLY_HAND + MINION)))


class BOT_245:
    """The Storm Bringer"""

    # Transform your minions into random <b>Legendary</b> minions.
    play = Morph(FRIENDLY_MINIONS, RandomLegendaryMinion())


class BOT_246:
    """Beakered Lightning"""

    # Deal $1 damage to all minions. <b>Overload:</b> (2)
    play = Hit(ALL_MINIONS, 1)


class BOT_451:
    """Voltaic Burst"""

    # Summon two 1/1 Sparks with <b>Rush</b>. <b>Overload:</b> (1)
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BOT_102t") * 2
