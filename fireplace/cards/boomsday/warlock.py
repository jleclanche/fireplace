from ..utils import *


##
# Minions


class BOT_224:
    """Doubling Imp"""

    # <b>Battlecry:</b> Summon a copy of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class BOT_226:
    """Nethersoul Buster"""

    # <b>Battlecry:</b> Gain +1 Attack for each damage your hero has taken this turn.
    play = Buff(SELF, "BOT_226e") * DAMAGED_THIS_TURN(FRIENDLY_HERO)


BOT_226e = buff(atk=1)


class BOT_433:
    """Dr. Morrigan"""

    # <b>Deathrattle:</b> Swap this with a minion from your deck.
    deathrattle = Swap(SELF, RANDOM(FRIENDLY_DECK + MINION))


class BOT_443:
    """Void Analyst"""

    # <b>Deathrattle:</b> Give all Demons in your hand +1/+1.
    deathrattle = Buff(FRIENDLY_HAND + DEMON, "BOT_443e")


BOT_443e = buff(+1, +1)


class BOT_536:
    """Omega Agent"""

    # [x]<b>Battlecry:</b> If you have 10 Mana Crystals, summon _2 copies of this minion.
    powered_up = AT_MAX_MANA(CONTROLLER)
    play = powered_up & SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 2


##
# Spells


class BOT_222:
    """Spirit Bomb"""

    # Deal $4 damage to a minion and your hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), Hit(FRIENDLY_HERO, 4)


class BOT_263:
    """Soul Infusion"""

    # Give the left-most minion in your hand +2/+2.
    play = Buff((FRIENDLY_HAND + MINION)[:1], "BOT_263e")


BOT_263e = buff(+2, +2)


class BOT_521:
    """Ectomancy"""

    # Summon copies of all Demons you control.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + DEMON))


class BOT_568:
    """The Soularium"""

    # Draw 3 cards. At the end of your turn, discard them.
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "BOT_568e")) * 3


class BOT_568e:
    class Hand:
        events = OWN_TURN_END.on(Discard(OWNER))

    events = REMOVED_IN_PLAY


class BOT_913:
    """Demonic Project"""

    # Each player transforms a random minion in their hand into a Demon.
    play = (
        Morph(RANDOM(FRIENDLY_HAND + MINION), RandomDemon()),
        Morph(RANDOM(ENEMY_HAND + MINION), RandomDemon()),
    )
