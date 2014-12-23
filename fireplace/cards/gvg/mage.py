from ..utils import *


##
# Spells

# Flamecannon
class GVG_001:
	def action(self):
		self.hit(random.choice(self.controller.opponent.field), 4)


# Echo of Medivh
class GVG_005:
	def action(self):
		for minion in self.controller.field:
			self.controller.give(minion.id)
