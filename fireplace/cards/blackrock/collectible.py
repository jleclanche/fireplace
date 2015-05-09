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

# Dragon's Breath
class BRM_003:
	action = [Hit(TARGET, 4)]

	def cost(self, value):
		return value - self.game.minionsKilledThisTurn
