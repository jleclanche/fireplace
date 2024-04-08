from ..utils import *


##
# Minions


class BT_255:
    """Kael'thas Sunstrider"""

    # Every third spell you cast each turn costs (0).
    update = (Count(CARDS_PLAYED_THIS_TURN + SPELL) % Number(3) == 2) & (
        Refresh(FRIENDLY_HAND + SPELL, buff="BT_255e")
    )


class BT_255e:
    cost = SET(0)
