"""
Underdog Rules
"""

from ..utils import *


# TBUD Summon Early Minion
class TBUD_1:
	events = OWN_TURN_BEGIN.on(
		(CURRENT_HEALTH(FRIENDLY_HERO) < CURRENT_HEALTH(ENEMY_HERO)) & (
			Summon(CONTROLLER, RandomMinion(cost=RandomNumber(2, 3)))
		)
	)
