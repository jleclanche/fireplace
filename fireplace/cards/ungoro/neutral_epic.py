from ..utils import *

##
# Minions

class UNG_085:
	"Emerald Hive Queen"
	update = Refresh(IN_HAND + MINION, {GameTag.COST: +2})

class UNG_087:
	"Bittertide Hydra"
	events = SELF_DAMAGE.on(Hit(FRIENDLY_HERO, 3))

# class UNG_088:
#	"Tortollan Primalist"

# class UNG_089:
#	"Gentle Megasaur"

# class UNG_099:
# 	"Charged Devilsaur"

# class UNG_113:
# 	"Bright-Eyed Scout"

# class UNG_847:
#	"Blazecaller"

class UNG_848:
	"Primordial Drake"
	play = Hit(ALL_MINIONS - SELF, 2)

class UNG_946:
	"Gluttonous Ooze"
	play = (
		GainArmor(FRIENDLY_HERO, 1) * Attr(ENEMY_WEAPON, GameTag.ATK),
		Destroy(ENEMY_WEAPON)
	)
