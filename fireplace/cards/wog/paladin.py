from ..utils import *


##
# Minions

class OG_006:
	"Vilefin Inquisitor"
	play = Summon(CONTROLLER, "OG_006b")

class OG_006b:
	"The Tidal Hand"
	activate = Summon(CONTROLLER, "OG_006a")


class OG_221:
	"Selfless Hero"
	deathrattle = GiveDivineShield(RANDOM_FRIENDLY_MINION)


##
# Spells



##
# Weapons

class OG_222:
	"Rallying Blade"
	play = Buff(FRIENDLY_MINIONS + DIVINE_SHIELD, "OG_222e")

OG_222e = buff(+1, +1)
