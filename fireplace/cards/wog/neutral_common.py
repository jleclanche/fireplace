from ..utils import *


##
# Minions

# Tentacle of N'Zoth
class OG_151:
	deathrattle = Hit(ALL_MINIONS, 1)


# Bilefin Tidehunter
class OG_156:
	play = Summon(CONTROLLER, "OG_156a")


# Zealous Initiate
class OG_158:
	deathrattle = Buff(RANDOM_FRIENDLY_MINION, "OG_158e")

OG_158e = buff(+1, +1)
