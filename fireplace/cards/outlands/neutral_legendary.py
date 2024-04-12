from ..utils import *


##
# Minions


class BT_126:
    """Teron Gorefiend"""

    # [x]<b>Battlecry:</b> Destroy all other friendly minions.
    # <b>Deathrattle:</b> Resummon them with +1/+1.
    pass


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
    pass


class BT_737:
    """Maiev Shadowsong"""

    # <b>Battlecry:</b> Choose a minion. It goes <b>Dormant</b> for 2 turns.
    pass


class BT_850:
    """Magtheridon"""

    # [x]<b>Dormant</b>. <b>Battlecry:</b> Summon three 1/3 enemy Warders. When
    # they die, destroy all minions and awaken.
    pass
