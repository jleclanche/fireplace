"""
Southshore vs. Tarren Mill
"""
from ..utils import *


# OLDN3wb Mage
class TBST_002:
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_MINION, 1))


# OLDN3wb Healer
class TBST_003:
	events = OWN_TURN_END.on(Heal(SELF_ADJACENT, 2))


# OLDLegit Healer
class TBST_004:
	events = OWN_TURN_END.on(
		Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + MINION + KILLED_THIS_TURN)))
	)


# OLDPvP Rogue
class TBST_005:
	events = Death(MINION, SELF).on(Stealth(SELF))


# OLDTBST Push Common Card
class TBST_006:
	pass
