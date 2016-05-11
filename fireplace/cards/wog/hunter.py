from ..utils import *


##
# Minions

class OG_179:
	"Fiery Bat"
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


class OG_292:
	"Forlorn Stalker"
	play = Buff(FRIENDLY_HAND + MINION + DEATHRATTLE, "OG_292e")

OG_292e = buff(+1, +1)
