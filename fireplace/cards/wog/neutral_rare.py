from ..utils import *


##
# Minions

# Silithid Swarmer:
class OG_034:
	update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & (
		Refresh(SELF, {GameTag.CANT_ATTACK: True})
	)


# Corrupted Healbot
class OG_147:
	deathrattle = Heal(ENEMY_HERO, 8)


# Tentacle of N'Zoth
class OG_151:
	deathrattle = Hit(ALL_MINIONS, 1)
