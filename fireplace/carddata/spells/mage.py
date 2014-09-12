from ..card import *


# Arcane Intellect
class CS2_023(Card):
	activate = drawCards(2)


# Arcane Explosion
class CS2_025(Card):
	def activate(self):
		for target in self.controller.getTargets(TARGET_ENEMY_MINIONS):
			target.damage(1)


# Fireball
class CS2_029(Card):
	activate = damageTarget(6)


# Pyroblast
class EX1_279(Card):
	activate = damageTarget(10)
