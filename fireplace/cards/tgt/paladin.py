from ..utils import *


##
# Minions

# Murloc Knight
class AT_076:
    inspire = Summon(CONTROLLER, RandomMurloc())


# Eadric the Pure
class AT_081:
    play = Buff(ALL_MINIONS, "AT_081e")


##
# Spells

# Seal of Champions
class AT_074:
    play = Buff(TARGET, "AT_074e2")


##
# Secrets

# Competitive Spirit
class AT_073:
    events = OWN_TURN_BEGIN.on(
        Buff(FRIENDLY_MINIONS, "AT_073e"), Reveal(SELF)
    )
