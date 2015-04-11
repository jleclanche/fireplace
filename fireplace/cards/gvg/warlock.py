from ..utils import *


##
# Minions

# Mistress of Pain
class GVG_018:
	def DAMAGE(self, source, target, amount):
		if source is self:
			self.heal(self.controller.hero, amount)


##
# Spells

# Darkbomb
class GVG_015:
	action = damageTarget(3)
