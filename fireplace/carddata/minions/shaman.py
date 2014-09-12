from ..card import *


# Healing Totem
class NEW1_009(Card):
	def endTurn(self):
		if self.game.currentPlayer is self.controller:
			targets = self.controller.getTargets(TARGET_FRIENDLY_MINIONS)
			for target in targets:
				target.heal(1)


# Fire Elemental
class CS2_042(Card):
	activate = damageTarget(3)


# Dust Devil
class EX1_243(Card):
	overload = 2


# Earth Elemental
class EX1_250(Card):
	overload = 3


# Mana Tide Totem
class EX1_575(Card):
	def endTurn(self):
		if self.game.currentPlayer is self.controller:
			self.controller.draw()


# Windspeaker
class EX1_587(Card):
	activate = buffTarget("EX1_587e")

class EX1_587e(Card):
	windfury = True
