from ..utils import *


##
# Spells

# Dragon's Breath
class DragonsBreath:
	action = [Hit(TARGET, 4)]

	def cost(self, value):
		return value - self.game.minionsKilledThisTurn
