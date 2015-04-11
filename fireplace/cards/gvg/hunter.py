from ..utils import *


##
# Minions

# Metaltooth Leaper
class GVG_048:
	def action(self):
		for target in self.controller.field:
			if target.race == Race.MECHANICAL and target is not self:
				self.buff(target, "GVG_048e")


# Gahz'rilla
class GVG_049:
	def SELF_DAMAGE(self, source, amount):
		self.buff(self, "GVG_049e")


class GVG_049e:
	atk = lambda self, i: i*2


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
