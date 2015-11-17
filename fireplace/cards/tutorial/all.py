"""
Cards used in the Tutorial missions
"""
from ..utils import *


##
# Hero Powers

# Shotgun Blast
class TU4d_003:
	play = Damage(TARGET, 1)


# Flames of Azzinoth
class TU4e_002:
	play = Summon(CONTROLLER, "TU4e_002t") * 2


##
# Minions

# Barrel (Unused)
class TU4c_003:
	deathrattle = Summon(OPPONENT, "TU4c_005")


# Crazy Monkey
class TU4f_007:
	play = Give(OPPONENT, "TU4c_006")

class TU4c_006:
	play = Buff(TARGET, "TU4c_006e")

# Bananas
TU4c_006e = buff(+1, +1)


##
# Spells

# Hogger SMASH!
class TU4a_004:
	play = Hit(TARGET, 4)


# Barrel Toss
class TU4c_002:
	play = Hit(TARGET, 2)


# Stomp
class TU4c_004:
	play = Hit(ENEMY_CHARACTERS, 2)


# Will of Mukla
class TU4c_008:
	play = Heal(FRIENDLY_HERO, 8)

# Might of Mukla (Unused)
TU4c_008e = buff(atk=8)


# Flame Burst
class TU4e_005:
	play = Hit(RANDOM_ENEMY_CHARACTER, 1) * 5


# Legacy of the Emperor
class TU4f_004:
	play = Buff(FRIENDLY_MINIONS, "TU4f_004o")

TU4f_004o = buff(+2, +2)


# Transcendence
class TU4f_006:
	play = Buff(FRIENDLY_HERO, "TU4f_006o")

class TU4f_006o:
	events = Death(FRIENDLY + MINION).on(
		Find(FRIENDLY_MINIONS) | Destroy(SELF)
	)

	tags = {
		GameTag.CANT_BE_ATTACKED: True,
		GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True,
	}
