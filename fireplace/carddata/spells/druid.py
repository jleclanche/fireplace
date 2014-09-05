import random
from ..card import *



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


# Soul of the Forest
class EX1_158(Card):
	def activate(self):
		for target in self.owner.board:
			target.buff("EX1_158e")

class EX1_158e(Card):
	def deathrattle(self):
		self.owner.owner.summon("EX1_158t")
