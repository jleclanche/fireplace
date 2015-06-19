from ..utils import *


##
# Minions

# Lucifron
class BRMC_85:
	action = [Buff(ALL_MINIONS - SELF, "CS2_063e")]


# Moira Bronzebeard
class BRMC_87:
	deathrattle = [Summon(CONTROLLER, "BRM_028")]


# Golemagg
class BRMC_95:
	def cost(self, value):
		return value - self.controller.hero.damage
