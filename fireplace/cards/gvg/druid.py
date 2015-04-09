from ..utils import *


##
# Minions

# Druid of the Fang
class GVG_080:
	def action(self):
		if self.poweredUp:
			self.morph("GVG_080t")
