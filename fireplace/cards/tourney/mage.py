from ..utils import *


##
# Secrets

# Effigy
class AT_002:
	events = Death(FRIENDLY + MINION).on(
		lambda self, minion: Summon(self.controller, RandomMinion(cost=minion.cost))
	)
