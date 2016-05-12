from ..utils import *


##
# Minions

class OG_202:
	"Mire Keeper"
	choose = ("OG_202a", "OG_202b")

class OG_202a:
	play = Summon(CONTROLLER, "OG_202c")

class OG_202b:
	play = AT_MAX_MANA(CONTROLLER) | GainEmptyMana(CONTROLLER, 1)


class OG_313:
	"Addled Grizzly"
	events = Summon(CONTROLLER, MINION).after(
		Buff(Summon.CARD, "OG_313e")
	)

OG_313e = buff(+1, +1)
