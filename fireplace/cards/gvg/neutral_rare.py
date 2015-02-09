from ..utils import *


##
# Minions

# Bomb Lobber
class GVG_099:
	def action(self):
		targets = self.controller.opponent.field
		if targets:
			self.hit(random.choice(targets), 4)
