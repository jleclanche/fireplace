from ..utils import *


##
# Minions

class OG_150:
	"Aberrant Berserker"
	enrage = Refresh(SELF, buff="OG_150e")

OG_150e = buff(atk=2)


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


class OG_249:
	"Infested Tauren"
	deathrattle = Summon(CONTROLLER, "OG_249a")


class OG_256:
	"Spawn of N'Zoth"
	deathrattle = Buff(FRIENDLY_MINIONS, "OG_256e")

OG_256e = buff(+1, +1)


class OG_323:
	"Polluted Hoarder"
	deathrattle = Draw(CONTROLLER)
