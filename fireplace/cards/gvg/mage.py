from ..utils import *


##
# Minions

# Goblin Blastmage
class GVG_004:
	def action(self):
		if self.poweredUp:
			for i in range(4):
				self.hit(random.choice(self.controller.opponent.characters), 1)


##
# Spells

# Flamecannon
class GVG_001:
	def action(self):
		self.hit(random.choice(self.controller.opponent.field), 4)


# Unstable Portal
class GVG_003:
	def action(self):
		card = self.controller.give(randomCollectible(type=CardType.MINION))
		self.buff(card, "GVG_003e")


# Echo of Medivh
class GVG_005:
	def action(self):
		for minion in self.controller.field:
			self.controller.give(minion.id)
