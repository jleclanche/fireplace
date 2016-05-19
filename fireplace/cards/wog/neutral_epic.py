from ..utils import *


##
# Minions

class OG_151:
	"Tentacle of N'Zoth"
	deathrattle = Hit(ALL_MINIONS, 1)


class OG_271:
	"Scaled Nightmare"
	events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_271e"))

class OG_271e:
	atk = lambda self, i: i * 2
