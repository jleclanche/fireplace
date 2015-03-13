from ..utils import *


##
# Minions

# Hobgoblin
class GVG_104:
	def OWN_MINION_SUMMON(self, minion):
		if minion.atk == 1:
			self.buff(minion, "GVG_104a")
