"""
Underdog Rules
"""

from ..utils import *


class TBUD_1:
	"""TBUD Summon Early Minion"""
	events = OWN_TURN_BEGIN.on(
		(CURRENT_HEALTH(FRIENDLY_HERO) < CURRENT_HEALTH(ENEMY_HERO)) & (
			Summon(CONTROLLER, RandomMinion(cost=RandomNumber(2, 3)))
		)
	)
