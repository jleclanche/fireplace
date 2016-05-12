from ..utils import *


##
# Minions

class OG_313:
	"Addled Grizzly"
	events = Summon(CONTROLLER, MINION).after(
		Buff(Summon.CARD, "OG_313e")
	)

OG_313e = buff(+1, +1)
