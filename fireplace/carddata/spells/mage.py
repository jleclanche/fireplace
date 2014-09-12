from ..card import *


# Arcane Intellect
class CS2_023(Card):
	action = drawCards(2)


# Arcane Explosion
class CS2_025(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ENEMY_MINIONS):
			target.damage(1)


# Fireball
class CS2_029(Card):
	action = damageTarget(6)


# Pyroblast
class EX1_279(Card):
	action = damageTarget(10)
