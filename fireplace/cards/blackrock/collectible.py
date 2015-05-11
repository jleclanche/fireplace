from ..utils import *


##
# Minions

# Flamewaker
class BRM_002:
	events = [
		OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 2)
	]


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
