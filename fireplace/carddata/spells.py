import random
from ..enums import Race
from ..targeting import *
from .card import *


# The Coin
class GAME_005(Card):
	activate = selfBuff("GAME_005e")

class GAME_005e(Card):
	mana = 1
	oneTurnEffect = True


# Claw
class CS2_005(Card):
	def activate(self):
		selfBuff(self, "CS2_005o")
		self.owner.gainArmor(2)

class CS2_005o(Card):
	attack = 2


# Healing Touch
class CS2_007(Card):
	targeting = TARGET_ANY_CHARACTER
	activate = healTarget(8)


# Moonfire
class CS2_008(Card):
	targeting = TARGET_ANY_CHARACTER
	activate = damageTarget(1)


# Mark of the Wild
class CS2_009(Card):
	targeting = TARGET_ANY_MINION
	activate = buffTarget("CS2_009e")

class CS2_009e(Card):
	attack = 2
	health = 2
	taunt = True


# Wild Growth
class CS2_013(Card):
	def activate(self):
		if self.owner.maxMana < self.owner.MAX_MANA:
			self.owner.gainMana(1)
		else:
			self.owner.give("CS2_013t")

class CS2_013t(Card):
	activate = drawCard


# Naturalize
class EX1_161(Card):
	targeting = TARGET_ANY_MINION
	def activate(self, target):
		target.destroy()
		self.owner.opponent.draw(2)


# Bite
class EX1_570(Card):
	def activate(self):
		selfBuff(self, "EX1_570e")
		self.owner.gainArmor(4)


# Holy Nova
class CS1_112(Card):
	targeting = TARGET_ALL_CHARACTERS
	def activate(self):
		for target in self.targets:
			if target.owner == self.owner:
				target.heal(2)
			else:
				target.damage(2)

# Cleave
class CS2_114(Card):
	targeting = TARGET_ENEMY_MINIONS
	minTargets = 2
	def activate(self):
		targets = random.sample(self.targets, 2)
		for target in targets:
			target.damage(2)


# Soul of the Forest
class EX1_158(Card):
	targeting = TARGET_FRIENDLY_MINIONS
	def activate(self):
		for target in self.targets:
			target.buff("EX1_158e")

class EX1_158e(Card):
	def deathrattle(self):
		self.owner.owner.summon("EX1_158t")


# Arcane Shot
class DS1_185(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.damage(2)


# Deadly Shot
class EX1_617(Card):
	def activate(self):
		random.choice(self.owner.opponent.field).destroy()


# Animal Companion
class NEW1_031(Card):
	def activate(self):
		self.owner.summon(random.choice(self.entourage))


# Kill Command
class EX1_539(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		for minion in self.owner.field:
			if minion.race == Race.BEAST:
				return target.damage(5)
		target.damage(3)
