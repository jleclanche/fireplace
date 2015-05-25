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


# Axe Flinger
class BRM_016:
	events = [
		SELF_DAMAGE.on(Hit(ENEMY_HERO, 2))
	]


# Dragon Egg
class BRM_022:
	events = [
		SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_022t"))
	]


# Volcanic Drake
class BRM_025:
	def cost(self, value):
		return value - self.game.minionsKilledThisTurn


# Hungry Dragon
class BRM_026:
	def action(self):
		return [Summon(CONTROLLER, randomCollectible(type=CardType.MINION, cost=1))]


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
