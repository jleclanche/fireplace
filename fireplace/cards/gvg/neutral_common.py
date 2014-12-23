from ..utils import *


##
# Minions

# Explosive Sheep
class GVG_076:
	def deathrattle(self):
		for target in self.game.board:
			self.hit(target, 2)


# Clockwork Gnome
class GVG_082:
	deathrattle = giveSparePart


# Micro Machine
class GVG_103:
	def TURN_BEGIN(self, player):
		# That card ID is not a mistake
		self.buff(self, "GVG_076a")

# Pistons
class GVG_076a:
	Atk = 1
