from ..utils import *


##
# Minions


class BT_009:
    """Imprisoned Sungill"""

    # <b>Dormant</b> for 2 turns. When this awakens, summon two 1/1 Murlocs.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Summon(CONTROLLER, "BT_009t") * 2


class BT_019:
    """Murgur Murgurgle"""

    # [x]<b>Divine Shield</b> <b>Deathrattle:</b> Shuffle 'Murgurgle Prime'
    # into your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_019t")


class BT_019t:
    """Murgurgle Prime"""

    # <b>Divine Shield</b> <b>Battlecry:</b> Summon 4 random Murlocs. Give them
    # <b>Divine Shield</b>.
    play = Summon(CONTROLLER, RandomMurloc()).then(GiveDivineShield(Summon.CARD)) * 4


class BT_020:
    """Aldor Attendant"""

    # <b>Battlecry:</b> Reduce the Cost_of your Librams by_(1) this game.
    play = Buff(CONTROLLER, "BT_020e")


class BT_020e:
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + LIBRAM, {GameTag.COST: -1})


class BT_026:
    """Aldor Truthseeker"""

    # <b>Taunt</b>. <b>Battlecry:</b> Reduce the Cost of your Librams by (2)
    # this game.
    play = Buff(CONTROLLER, "BT_026e")


class BT_026e:
    update = Refresh(FRIENDLY + (IN_HAND | IN_DECK) + LIBRAM, {GameTag.COST: -2})


class BT_334:
    """Lady Liadrin"""

    # [x]<b>Battlecry:</b> Add a copy of each spell you cast on friendly
    # characters this game to your hand.
    play = Give(
        CONTROLLER, Copy(SHUFFLE(CARDS_PLAYED_THIS_GAME + CAST_ON_FRIENDLY_CHARACTERS))
    )


##
# Spells


class BT_011:
    """Libram of Justice"""

    # Equip a 1/4 weapon. Change the Health of all enemy minions to 1.
    play = Summon(CONTROLLER, "BT_011t"), Buff(ENEMY_MINIONS, "BT_011e")


class BT_011e:
    max_health = SET(1)


class BT_024:
    """Libram of Hope"""

    # Restore 8 Health. Summon an 8/8 Guardian with <b>Taunt</b> and_<b>Divine
    # Shield</b>.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 8), Summon(CONTROLLER, "BT_024t")


class BT_025:
    """Libram of Wisdom"""

    # [x]Give a minion +1/+1 and "<b>Deathrattle:</b> Add a 'Libram of Wisdom'
    # spell to your hand."
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "BT_025e")


class BT_025e:
    tags = {GameTag.ATK: +1, GameTag.HEALTH: +1, GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, "BT_025")


class BT_292:
    """Hand of A'dal"""

    # Give a minion +2/+2. Draw a card.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "BT_292e"), Draw(CONTROLLER)


BT_292e = buff(+2, +2)


##
# Weapons


class BT_018:
    """Underlight Angling Rod"""

    # After your Hero attacks, add a random Murloc to your hand.
    events = Attack(FRIENDLY_HERO).after(Give(CONTROLLER, RandomMurloc()))
