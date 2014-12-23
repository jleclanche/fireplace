from ..utils import *


##
# Spells

# Flamecannon
class GVG_001:
	def action(self):
		self.hit(random.choice(self.controller.opponent.field), 4)
