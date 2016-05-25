from ..utils import *


##
# Minions

class OG_034:
	"Silithid Swarmer"
	update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & (
		Refresh(SELF, {GameTag.CANT_ATTACK: True})
	)


class OG_254:
	"Eater of Secrets"
	play = (
		Buff(SELF, "OG_254e") * Count(ENEMY_SECRETS),
		Destroy(ENEMY_SECRETS)
	)

OG_254e = buff(+1, +1)


class OG_322:
	"Blackwater Pirate"
	update = Refresh(FRIENDLY_HAND + WEAPON, {GameTag.COST: -2})
