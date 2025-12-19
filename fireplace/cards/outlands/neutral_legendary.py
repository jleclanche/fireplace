from ..utils import *


##
# Minions


class BT_126:
    """Teron Gorefiend"""

    # [x]<b>Battlecry:</b> Destroy all other friendly minions.
    # <b>Deathrattle:</b> Resummon them with +1/+1.
    play = Destroy(FRIENDLY_MINIONS - SELF).then(
        StoringBuff(SELF, "BT_126e", Destroy.TARGET)
    )


class BT_126e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, STORE_CARD).then(Buff(Summon.CARD, "BT_126e2"))


BT_126e2 = buff(+1, +1)


class BT_255:
    """Kael'thas Sunstrider"""

    # Every third spell you cast each turn costs (0).
    update = (Count(CARDS_PLAYED_THIS_TURN + SPELL) % 3 == 2) & (
        Refresh(FRIENDLY_HAND + SPELL, buff="BT_255e")
    )


class BT_255e:
    cost = SET(0)


class BT_735:
    """Al'ar"""

    # <b>Deathrattle</b>: Summon a 0/3 Ashes of Al'ar that resurrects this
    # minion on your next turn.
    deathrattle = Summon(CONTROLLER, "BT_735t")


class BT_735t:
    """Ashes of Al'ar"""

    # At the start of your turn, transform this into Al'ar.
    events = OWN_TURN_BEGIN.on(Morph(SELF, "BT_735"))


class BT_737:
    """Maiev Shadowsong"""

    # <b>Battlecry:</b> Choose a minion. It goes <b>Dormant</b> for 2 turns.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Dormant(TARGET, 2)


class BT_850:
    """Magtheridon"""

    # [x]<b>Dormant</b>. <b>Battlecry:</b> Summon three 1/3 enemy Warders. When
    # they die, destroy all minions and awaken.
    tags = {GameTag.DORMANT: True}
    progress_total = 3
    play = Summon(OPPONENT, "BT_850t") * 3
    dormant_events = Death(ENEMY_MINIONS + ID("BT_850t")).on(
        AddProgress(SELF, Death.ENTITY)
    )
    reward = Awaken(SELF)
    awaken = Destroy(ALL_MINIONS - SELF)
