"""
Spare Parts
"""

from ..utils import *


# Armor Plating
class PART_001:
	play = Buff(TARGET, "PART_001e")

PART_001e = buff(health=1)


# Time Rewinder
class PART_002:
	play = Bounce(TARGET)


# Rusty Horn
class PART_003:
	play = Taunt(TARGET)


# Finicky Cloakfield
class PART_004:
	play = Buff(TARGET - STEALTH, "PART_004e")


class PART_004e:
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


# Emergency Coolant
class PART_005:
	play = Freeze(TARGET)


# Reversing Switch
class PART_006:
	play = SwapAttackAndHealth(TARGET, "PART_006a")


# Whirling Blades
class PART_007:
	play = Buff(TARGET, "PART_007e")

PART_007e = buff(atk=1)
