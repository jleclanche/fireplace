from ..card import *


# Arcane Intellect
class CS2_023(Card):
	activate = drawCards(2)


# Arcane Explosion
class CS2_025(Card):
	def activate(self):
		for target in self.getTargets(TARGET_ENEMY_MINIONS):
			target.damage(1)


# Fireball
class CS2_029(Card):
	targeting = TARGET_ANY_CHARACTER
	activate = damageTarget(6)


# Pyroblast
class EX1_279(Card):
	targeting = TARGET_ANY_CHARACTER
	activate = damageTarget(10)
