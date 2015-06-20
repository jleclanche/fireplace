from ..utils import *


##
# Minions

# Lucifron
class BRMC_85:
	action = [Buff(ALL_MINIONS - SELF, "CS2_063e")]


# Moira Bronzebeard
class BRMC_87:
	deathrattle = [Summon(CONTROLLER, "BRM_028")]


# Son of the Flame
class BRMC_91:
	action = [Hit(TARGET, 6)]


# Golemagg
class BRMC_95:
	def cost(self, value):
		return value - self.controller.hero.damage


# High Justice Grimstone
class BRMC_96:
	events = [
		OWN_TURN_BEGIN.on(Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY)))
	]


# Garr
class BRMC_99:
	events = [
		SELF_DAMAGE.on(Summon(CONTROLLER, "BRMC_99e"))
	]
