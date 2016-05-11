"""
Spare Parts
"""

from ..utils import *


class PART_001:
	"Armor Plating"
	play = Buff(TARGET, "PART_001e")
	tags = {GameTag.SPARE_PART: True}

PART_001e = buff(health=1)


class PART_002:
	"Time Rewinder"
	play = Bounce(TARGET)
	tags = {GameTag.SPARE_PART: True}


class PART_003:
	"Rusty Horn"
	play = Taunt(TARGET)
	tags = {GameTag.SPARE_PART: True}


class PART_004:
	"Finicky Cloakfield"
	play = Buff(TARGET - STEALTH, "PART_004e")
	tags = {GameTag.SPARE_PART: True}


class PART_004e:
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class PART_005:
	"Emergency Coolant"
	play = Freeze(TARGET)
	tags = {GameTag.SPARE_PART: True}


class PART_006:
	"Reversing Switch"
	play = Buff(TARGET, "PART_006a")
	tags = {GameTag.SPARE_PART: True}

PART_006a = AttackHealthSwapBuff()


class PART_007:
	"Whirling Blades"
	play = Buff(TARGET, "PART_007e")
	tags = {GameTag.SPARE_PART: True}

PART_007e = buff(atk=1)
