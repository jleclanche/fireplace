"""
Cards used in the Tutorial missions
"""
from ..utils import *


##
# Hero Powers

# Shotgun Blast
class TU4d_003:
	action = [Damage(TARGET, 1)]


# Flames of Azzinoth
class TU4e_002:
	action = [Summon(CONTROLLER, "TU4e_002t") * 2]


##
# Minions

# Barrel (Unused)
class TU4c_003:
	deathrattle = [Summon(OPPONENT, "TU4c_005")]


# Crazy Monkey
class TU4f_007:
	action = [Give(OPPONENT, "TU4c_006")]

class TU4c_006:
	action = [Buff(TARGET, "TU4c_006")]


##
# Spells

# Hogger SMASH!
class TU4a_004:
	action = [Hit(TARGET, 4)]


# Barrel Toss
class TU4c_002:
	action = [Hit(TARGET, 2)]


# Stomp
class TU4c_004:
	action = [Hit(ENEMY_CHARACTERS, 2)]


# Will of Mukla
class TU4c_008:
	action = [Heal(FRIENDLY_HERO, 8)]


# Flame Burst
class TU4e_005:
	action = [Hit(RANDOM_ENEMY_CHARACTER, 1) * 5]


# Legacy of the Emperor
class TU4f_004:
	action = [Buff(FRIENDLY_MINIONS, "TU4f_004o")]
