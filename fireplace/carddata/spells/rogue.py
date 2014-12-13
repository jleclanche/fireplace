from ..card import *


# Backstab
class CS2_072(Card):
	action = damageTarget(2)


# Cold Blood
class CS2_073(Card):
	action = buffTarget("CS2_073e2")
	combo = buffTarget("CS2_073e")


# Deadly Poison
class CS2_074(Card):
	def action(self):
		self.controller.hero.weapon.buff("CS2_074e")

class CS2_074e(Card):
	Atk = 2


# Sinister Strike
class CS2_075(Card):
	action = damageEnemyHero(3)


# Assassinate
class CS2_076(Card):
	action = destroyTarget


# Sprint
class CS2_077(Card):
	action = drawCards(4)


# Blade Flurry
class CS2_233(Card):
	def action(self):
		damage = self.controller.hero.weapon.atk
		self.controller.hero.weapon.destroy()
		for target in self.controller.opponent.field:
			self.hit(target, damage)


# Eviscerate
class EX1_124(Card):
	action = damageTarget(2)
	combo = damageTarget(4)


# Betrayal
class EX1_126(Card):
	def action(self, target):
		for minion in target.adjacentMinions:
			if minion:
				target.hit(minion, target.atk)


# Fan of Knives
class EX1_129(Card):
	def action(self):
		for target in self.controller.opponent.field:
			self.hit(target, 1)
		self.controller.draw()


# Shiv
class EX1_278(Card):
	def action(self, target):
		self.hit(target, 1)
		self.controller.draw()


# Sap
class EX1_581(Card):
	action = bounceTarget


# Vanish
class NEW1_004(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			target.bounce()
