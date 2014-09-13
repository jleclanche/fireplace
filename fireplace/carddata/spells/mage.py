from ..card import *


# Arcane Intellect
class CS2_023(Card):
	action = drawCards(2)


# Frostbolt
class CS2_024(Card):
	def action(self, target):
		target.damage(3)
		target.freeze()


# Arcane Explosion
class CS2_025(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ENEMY_MINIONS):
			target.damage(1)


# Frost Nova
class CS2_026(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ENEMY_MINIONS):
			target.freeze()


# Blizzard
class CS2_028(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ENEMY_MINIONS):
			target.damage(2)
			target.freeze()


# Fireball
class CS2_029(Card):
	action = damageTarget(6)


# Ice Lance
class CS2_031(Card):
	def action(self, target):
		if target.frozen:
			target.damage(4)
		else:
			target.freeze()


# Cone of Cold
class EX1_275(Card):
	def action(self, target):
		for minion in target.adjacentMinions:
			minion.damage(1)
			minion.freeze()
		target.damage(1)
		target.freeze()


# Pyroblast
class EX1_279(Card):
	action = damageTarget(10)
