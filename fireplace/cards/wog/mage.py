from ..utils import *


##
# Minions

class OG_083:
	"Twilight Flamecaller"
	play = Hit(ENEMY_MINIONS, 1)


class OG_120:
	"Anomalus"
	deathrattle = Hit(ALL_MINIONS, 8)


class OG_207:
	"Faceless Summoner"
	play = Summon(CONTROLLER, RandomMinion(cost=3))
