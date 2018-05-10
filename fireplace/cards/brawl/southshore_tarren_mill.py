"""
Southshore vs. Tarren Mill
"""
from ..utils import *


class TBST_002:
	"""OLDN3wb Mage"""
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_MINION, 1))


class TBST_003:
	"""OLDN3wb Healer"""
	events = OWN_TURN_END.on(Heal(SELF_ADJACENT, 2))


class TBST_004:
	"""OLDLegit Healer"""
	events = OWN_TURN_END.on(
		Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + MINION + KILLED_THIS_TURN)))
	)


class TBST_005:
	"""OLDPvP Rogue"""
	events = Death(MINION, SELF).on(Stealth(SELF))


class TBST_006:
	"""OLDTBST Push Common Card"""
	pass
