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
	action = buffTarget("CS2_073e")
	combo = buffTarget("CS2_073e2")


# Deadly Poison
class CS2_074:
	def action(self):
		self.buff(self.controller.weapon, "CS2_074e")


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
		for target in self.controller.opponent.field:
			self.hit(target, self.controller.weapon.atk)
		self.controller.weapon.destroy()


# Eviscerate
class EX1_124:
	action = damageTarget(2)
	combo = damageTarget(4)


# Betrayal
class EX1_126:
	def action(self, target):
		for minion in target.adjacentMinions:
			target.hit(minion, target.atk)


# Conceal
class EX1_128:
	def action(self):
		for target in self.controller.field:
			self.buff(target, "EX1_128e")

class EX1_128e:
	def OWN_TURN_BEGIN(self):
		self.destroy()


# Fan of Knives
class EX1_129:
	def action(self):
		for target in self.controller.opponent.field:
			self.hit(target, 1)
		self.controller.draw()


# Headcrack
class EX1_137:
	action = damageEnemyHero(2)

	def combo(self):
		self.hit(self.controller.opponent.hero, 2)
		self.game.register("TURN_END",
			lambda *args: self.controller.give("EX1_137"),
		once=True)


# Shadowstep
class EX1_144:
	def action(self, target):
		target.bounce()
		self.buff(target, "EX1_144e")


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
