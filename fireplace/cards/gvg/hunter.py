from ..utils import *


##
# Minions

# Metaltooth Leaper
class GVG_048:
	def action(self):
		for target in self.controller.field:
			self.buff(target, "GVG_048e")

class GVG_048e:
	Atk = 2


##
# Spells

# Cobra Shot
class GVG_073:
	def action(self, target):
		self.hit(target, 3)
		self.hit(self.controller.opponent.hero, 3)


##
# Weapons

# Glaivezooka
class GVG_043:
	def action(self):
		if self.controller.field:
			self.buff(random.choice(self.controller.field), "GVG_043e")

class GVG_043e:
	Atk = 1
