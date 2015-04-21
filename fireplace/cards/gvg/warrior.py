from ..utils import *


##
# Minions

# Shieldmaiden
class GVG_053:
	action = [GainArmor(FRIENDLY_HERO, 5)]


# Screwjank Clunker
class GVG_055:
	action = [Buff(TARGET, "GVG_055e")]


##
# Spells

# Crush
class GVG_052:
	action = [Destroy(TARGET)]
	def cost(self, value):
		for minion in self.controller.field:
			if minion.damaged:
				return value - 4
		return value
