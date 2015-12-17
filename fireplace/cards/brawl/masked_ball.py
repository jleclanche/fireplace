"""
The Masked Ball
"""

from ..utils import *


# Mysterious Pilot
class TB_Pilot1:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=COST(SELF)))
	tags = {GameTag.DEATHRATTLE: True}
