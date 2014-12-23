from ..utils import *

##
# Minions

# Defias Ringleader
class EX1_131:
	combo = summonMinion("EX1_131t")


# SI:7 Agent
class EX1_134:
	combo = damageTarget(2)


# Edwin VanCleef
class EX1_613:
	def combo(self):
		for i in range(self.controller.cardsPlayedThisTurn):
			self.buff(self, "EX1_613e")

class EX1_613e:
	Atk = 2
	Health = 2


# Kidnapper
class NEW1_005:
	combo = bounceTarget


# Master of Disguise
class NEW1_014:
	def battlecry(self, target):
		target.stealthed = True


##
# Spells

# Backstab
class CS2_072:
	action = damageTarget(2)


# Cold Blood
class CS2_073:
	action = buffTarget("CS2_073e2")
	combo = buffTarget("CS2_073e")

class CS2_073e:
	Atk = 4

class CS2_073e2:
	Atk = 2


# Deadly Poison
class CS2_074:
	def action(self):
		self.buff(self.controller.hero.weapon, "CS2_074e")

class CS2_074e:
	Atk = 2


# Sinister Strike
class CS2_075:
	action = damageEnemyHero(3)


# Assassinate
class CS2_076:
	action = destroyTarget


# Sprint
class CS2_077:
	action = drawCards(4)


# Blade Flurry
class CS2_233:
	def action(self):
		damage = self.controller.hero.weapon.atk
		self.controller.hero.weapon.destroy()
		for target in self.controller.opponent.field:
			self.hit(target, damage)


# Eviscerate
class EX1_124:
	action = damageTarget(2)
	combo = damageTarget(4)


# Betrayal
class EX1_126:
	def action(self, target):
		for minion in target.adjacentMinions:
			target.hit(minion, target.atk)


# Fan of Knives
class EX1_129:
	def action(self):
		for target in self.controller.opponent.field:
			self.hit(target, 1)
		self.controller.draw()


# Shiv
class EX1_278:
	def action(self, target):
		self.hit(target, 1)
		self.controller.draw()


# Sap
class EX1_581:
	action = bounceTarget


# Vanish
class NEW1_004:
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			target.bounce()


##
# Weapons

# Perdition's Blace
class EX1_133:
	action = damageTarget(1)
	combo = damageTarget(2)
