from ..utils import *


##
# Minions

# Bolvar Fordragon
class GVG_063:
	@hand
	def OWN_MINION_DESTROY(self, minion):
		self.buff(self, "GVG_063a")
