from ..utils import *


##
# Minions

# Goblin Auto-Barber
class GVG_023:
	action = buffWeapon("GVG_023a")


##
# Spells

# Tinker's Sharpsword Oil
class GVG_022:
	action = buffWeapon("GVG_022a")

	def action(self):
		if self.controller.weapon:
			self.buff(self.controller.weapon, "GVG_022a")
		if self.controller.field:
			self.buff(random.choice(self.controller.field), "GVG_022b")


##
# Weapons

# Cogmaster's Wrench
class GVG_024:
	def atk(self, i):
		if self.controller.field.filter(race=Race.MECHANICAL):
			return i + 2
		return i
