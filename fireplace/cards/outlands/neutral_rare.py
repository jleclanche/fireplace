from ..utils import *


##
# Minions


class BT_155:
    """Scrapyard Colossus"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 7/7 Felcracked Colossus with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "BT_155t")


class BT_721:
    """Blistering Rot"""

    # [x]At the end of your turn, summon a Rot with stats equal to this
    # minion's.
    events = OWN_TURN_END.on(
        SummonCustomMinion(CONTROLLER, "BT_721t", 1, ATK(SELF), CURRENT_HEALTH(SELF))
    )


class BT_731:
    """Infectious Sporeling"""

    # After this damages a minion, turn it into an Infectious_Sporeling.
    events = Damage(source=SELF).on(Morph(Damage.TARGET, "BT_731"))
