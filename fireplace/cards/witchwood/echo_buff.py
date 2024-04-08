from ..utils import *


class GIL_000:
    """Echo Enchant"""

    events = REMOVED_IN_PLAY

    class Hand:
        events = OWN_TURN_END.on(Destroy(OWNER))
        update = Refresh(OWNER, {GameTag.COST: lambda self, i: max(i, 1)}, priority=100)
