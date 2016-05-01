from ..utils import *


##
# Minions

# Fiery Bat
class OG_179:
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


# Forlorn Stalker
class OG_292:
	play = Buff(FRIENDLY_HAND + MINION + DEATHRATTLE, "OG_292e")

OG_292e = buff(+1, +1)
