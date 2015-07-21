"""
Spare Parts
"""

from ..utils import *


# Armor Plating
class PART_001:
	play = Buff(TARGET, "PART_001e")


# Time Rewinder
class PART_002:
	play = Bounce(TARGET)


# Rusty Horn
class PART_003:
	play = SetTag(TARGET, {GameTag.TAUNT: True})


# Finicky Cloakfield
class PART_004:
	play = Buff(TARGET, "PART_004e")

class PART_004e:
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


# Emergency Coolant
class PART_005:
	play = Freeze(TARGET)


# Reversing Switch
class PART_006:
	play = Buff(TARGET, "PART_006a")


# Whirling Blades
class PART_007:
	play = Buff(TARGET, "PART_007e")
