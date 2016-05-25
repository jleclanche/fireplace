from ..utils import *


##
# Minions

class OG_234:
	"Darkshire Alchemist"
	play = Heal(TARGET, 5)


class OG_335:
	"Shifting Shade"
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


##
# Spells

class OG_094:
	"Power Word: Tentacles"
	play = Buff(TARGET, "OG_094e")

OG_094e = buff(+2, +6)


class OG_100:
	"Shadow Word: Horror"
	play = Destroy(ALL_MINIONS + (ATK <= 2))
