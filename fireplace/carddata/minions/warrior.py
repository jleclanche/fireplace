from fireplace.enums import CardType
from ..card import *


# Armorsmith
class EX1_402(Card):
	def OWN_DAMAGE(self, source, target, amount):
		if target.type == CardType.MINION:
			self.controller.hero.armor += 1


# Cruel Taskmaster
class EX1_603(Card):
	def action(self, target):
		target.buff("EX1_603e")
		self.hit(target, 1)

class EX1_603e(Card):
	Atk = 2
