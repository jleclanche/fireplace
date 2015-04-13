"""
Cards removed from the game
"""

from ..utils import *


# Dagger Mastery
class CS2_083:
	def action(self):
		if self.controller.weapon:
			self.buff(self.controller.weapon, "CS2_083e")
		else:
			self.controller.summon("CS2_082")

class CS2_083e:
	Atk = 1


# Blessing of Wisdom (Owner draws)
class EX1_363e2:
	def SELF_ATTACK(self, target):
		self.owner.controller.draw()


# Repairs! (Antique Healbot)
class GVG_069a:
	Health = 4


# Adrenaline Rush
class NEW1_006:
	action = drawCard
	combo = drawCards(2)


# Bolstered (Bloodsail Corsair)
class NEW1_025e:
	Health = 1
