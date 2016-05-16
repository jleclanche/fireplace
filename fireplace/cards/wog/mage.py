from ..utils import *


##
# Minions

class OG_083:
	"Twilight Flamecaller"
	play = Hit(ENEMY_MINIONS, 1)


class OG_085:
	"Demented Frostcaller"
	events = OWN_SPELL_PLAY.after(Freeze(RANDOM(ENEMY_CHARACTERS - MORTALLY_WOUNDED - FROZEN)))


class OG_120:
	"Anomalus"
	deathrattle = Hit(ALL_MINIONS, 8)


class OG_207:
	"Faceless Summoner"
	play = Summon(CONTROLLER, RandomMinion(cost=3))
