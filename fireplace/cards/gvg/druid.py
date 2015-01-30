from ..utils import *


##
# Minions

# Druid of the Fang
class GVG_080:
	def action(self):
		for target in self.controller.field:
			if target.race == Race.BEAST:
					self.morph("GVG_080t")
					break
