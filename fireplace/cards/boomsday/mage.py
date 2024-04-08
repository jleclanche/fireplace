from ..utils import *


##
# Minions


class BOT_103:
    """Stargazer Luna"""

    # After you play the right-most card in your hand, draw a card.
    events = Play(CONTROLLER).after(
        Find(Play.CARD + PLAY_RIGHT_MOST) & Draw(CONTROLLER)
    )


class BOT_256:
    """Astromancer"""

    # [x]<b>Battlecry:</b> Summon a random minion with Cost equal to your hand size.
    play = Summon(CONTROLLER, RandomMinion(cost=Count(FRIENDLY_HAND)))


class BOT_531:
    """Celestial Emissary"""

    # <b>Battlecry:</b> Your next spell_this turn has <b>Spell_Damage +2</b>.
    play = Buff(CONTROLLER, "BOT_531e")


class BOT_531e:
    update = Refresh(CONTROLLER, {GameTag.SPELLPOWER: 2})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class BOT_601:
    """Meteorologist"""

    # <b>Battlecry:</b> For each card in your hand, deal 1 damage to a random enemy.
    play = Hit(RANDOM_ENEMY_MINION, 1) * Count(FRIENDLY_HAND)


##
# Spells


class BOT_101:
    """Astral Rift"""

    # Add 2 random minions to your hand.
    play = Give(CONTROLLER, RandomMinion()) * 2


class BOT_254:
    """Unexpected Results"""

    # [x]Summon two random $2-Cost minions <i>(improved by <b>Spell Damage</b>)</i>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RandomMinion(cost=SPELL_DAMAGE(2)))


class BOT_257:
    """Luna's Pocket Galaxy"""

    # Change the Cost of minions in your deck to (1).
    play = Buff(FRIENDLY_DECK + MINION, "BOT_257e")


class BOT_257e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class BOT_453:
    """Shooting Star"""

    # Deal $1 damage to a minion and the minions next to it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Hit(TARGET_ADJACENT, 1)


class BOT_600:
    """Research Project"""

    # Each player draws 2_cards.
    play = Draw(PLAYER) * 2
