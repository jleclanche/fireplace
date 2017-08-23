from ..utils import *


##
# Minions

class OG_034:
	"Silithid Swarmer"
	update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & (
		Refresh(SELF, {GameTag.CANT_ATTACK: True})
	)


class OG_147:
	"Corrupted Healbot"
	deathrattle = Heal(ENEMY_HERO, 8)


class OG_161:
	"Corrupted Seer"
	play = Hit(ALL_MINIONS - MURLOC, 2)


# class OG_162:
#	"Disciple of C'Thun"


class OG_254:
	"Eater of Secrets"
	play = (
		Buff(SELF, "OG_254e") * Count(ENEMY_SECRETS),
		Destroy(ENEMY_SECRETS)
	)

OG_254e = buff(+1, +1)

# class OG_255:
# 	"Doomcaller"


class OG_320:
	"Midnight Drake"
	play = Buff(SELF, "OG_320e") * Count(FRIENDLY_HAND)

OG_320e = buff(atk=1)


class OG_322:
	"Blackwater Pirate"
	update = Refresh(FRIENDLY_HAND + WEAPON, {GameTag.COST: -2})


# class OG_339:
# 	"Skeram Cultist"
