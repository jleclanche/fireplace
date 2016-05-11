from ..utils import *


##
# Minions

class OG_151:
	"Tentacle of N'Zoth"
	deathrattle = Hit(ALL_MINIONS, 1)


class OG_156:
	"Bilefin Tidehunter"
	play = Summon(CONTROLLER, "OG_156a")


class OG_158:
	"Zealous Initiate"
	deathrattle = Buff(RANDOM_FRIENDLY_MINION, "OG_158e")

OG_158e = buff(+1, +1)
