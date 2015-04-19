from ..utils import *


##
# Minions

# Goblin Sapper
class GVG_095:
	def atk(self, i):
		if len(self.controller.opponent.hand) >= 6:
			return i + 4
		return i


# Bomb Lobber
class GVG_099:
	def action(self):
		targets = self.controller.opponent.field
		if targets:
			self.hit(random.choice(targets), 4)
