from ..utils import *


##
# Minions

# Shadowbomber
class GVG_009:
	def action(self):
		for target in (self.currentPlayer.hero, self.currentPlayer.opponent.hero):
			self.hit(target, 3)


# Shrinkmeister
class GVG_011:
	action = buffTarget("GVG_011a")


##
# Spells

# Lightbomb
class GVG_008:
	def action(self):
		for target in self.game.board:
			self.hit(target, target.atk)


# Velen's Chosen
class GVG_010:
	action = buffTarget("GVG_010b")
