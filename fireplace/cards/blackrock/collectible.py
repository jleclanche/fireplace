from ..utils import *


##
# Minions

# Flamewaker
class BRM_002:
	events = [
		OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 2)
	]


# Imp Gang Boss
class BRM_006:
	events = [
		SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_006t"))
	]


# Dark Iron Skulker
class BRM_008:
	action = [Hit(ENEMY_MINIONS - DAMAGED, 2)]


# Volcanic Lumberer
class BRM_009:
	def cost(self, value):
		return value - self.game.minionsKilledThisTurn


##
# Spells

# Solemn Vigil
class BRM_001:
	action = [Draw(CONTROLLER) * 2]

	def cost(self, value):
		return value - self.game.minionsKilledThisTurn


# Dragon's Breath
class BRM_003:
	action = [Hit(TARGET, 4)]

	def cost(self, value):
		return value - self.game.minionsKilledThisTurn


# Demonwrath
class BRM_005:
	action = [Hit(ALL_MINIONS - DEMON, 2)]
