from ..utils import *


##
# Minions

# Bolvar Fordragon
class GVG_063:
	@hand
	def OWN_MINION_DESTROY(self, minion):
		return [Buff(SELF, "GVG_063a")]
