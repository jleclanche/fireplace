from ..utils import *


##
# Minions


##
# Spells

class BT_801:
	"""Eye Beam"""
	play = Hit(TARGET, 3)
	update = Refresh(OUTERMOST_HAND + SELF, {GameTag.COST: SET(1)})
