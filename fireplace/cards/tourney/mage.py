from ..utils import *


##
# Secrets

# Effigy
class PH_MAGE_001:
	events = Death(FRIENDLY + MINION).on(
		lambda self, minion: Summon(self.controller, RandomMinion(cost=minion.cost))
	)
