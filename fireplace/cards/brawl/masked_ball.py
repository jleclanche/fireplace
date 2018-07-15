"""
The Masked Ball
"""

from ..utils import *


class TB_Pilot1:
	"""Mystery Pilot"""
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=COST(SELF)))
	tags = {GameTag.DEATHRATTLE: True}
