"""
Spare Parts
"""

from ..utils import *


# Armor Plating
class PART_001:
	play = Buff(TARGET, "PART_001e")
	tags = {GameTag.SPARE_PART: True}

PART_001e = buff(health=1)


# Time Rewinder
class PART_002:
	play = Bounce(TARGET)
	tags = {GameTag.SPARE_PART: True}


# Rusty Horn
class PART_003:
	play = Taunt(TARGET)
	tags = {GameTag.SPARE_PART: True}


# Finicky Cloakfield
class PART_004:
	play = Buff(TARGET - STEALTH, "PART_004e")
	tags = {GameTag.SPARE_PART: True}


class PART_004e:
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


# Emergency Coolant
class PART_005:
	play = Freeze(TARGET)
	tags = {GameTag.SPARE_PART: True}


# Reversing Switch
class PART_006:
	play = Buff(TARGET, "PART_006a")
	tags = {GameTag.SPARE_PART: True}

PART_006a = AttackHealthSwapBuff()


# Whirling Blades
class PART_007:
	play = Buff(TARGET, "PART_007e")
	tags = {GameTag.SPARE_PART: True}

PART_007e = buff(atk=1)
