from ..utils import *


##
# Minions

# Tentacle of N'Zoth
class OG_151:
	deathrattle = Hit(ALL_MINIONS, 1)


# Bilefin Tidehunter
class OG_156:
	Summon(CONTROLLER, "OG_156a")


class OG_158:
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "LOE_061e")

OG_158e = buff(+1, +1)
