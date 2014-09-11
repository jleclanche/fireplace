import random
from ..card import *



# Claw
class CS2_005(Card):
	def activate(self):
		buffSelf(self, "CS2_005o")
		self.owner.hero.gainArmor(2)

class CS2_005o(Card):
	attack = 2


# Healing Touch
class CS2_007(Card):
	activate = healTarget(8)


# Moonfire
class CS2_008(Card):
	activate = damageTarget(1)


# Mark of the Wild
class CS2_009(Card):
	activate = buffTarget("CS2_009e")

class CS2_009e(Card):
	attack = 2
	health = 2
	taunt = True


# Savage Roar
class CS2_011(Card):
	def activate(self):
		for target in self.owner.getTargets(TARGET_FRIENDLY_CHARACTERS):
			target.buff("CS2_011o")

class CS2_011o(Card):
	attack = 2


# Swipe
class CS2_012(Card):
	def activate(self, target):
		for character in self.owner.getTargets(TARGET_ENEMY_CHARACTERS):
			if character is target:
				character.damage(4)
			else:
				character.damage(1)


# Wild Growth
class CS2_013(Card):
	def activate(self):
		if self.owner.maxMana < self.owner.MAX_MANA:
			self.owner.gainMana(1)
		else:
			self.owner.give("CS2_013t")

class CS2_013t(Card):
	activate = drawCard


# Soul of the Forest
class EX1_158(Card):
	def activate(self):
		for target in self.owner.field:
			target.buff("EX1_158e")

class EX1_158e(Card):
	def deathrattle(self):
		self.owner.owner.summon("EX1_158t")


# Naturalize
class EX1_161(Card):
	def activate(self, target):
		target.destroy()
		self.owner.opponent.draw(2)


# Starfire
class EX1_173(Card):
	def activate(self, target):
		target.damage(5)
		self.owner.draw()


# Bite
class EX1_570(Card):
	def activate(self):
		buffSelf(self, "EX1_570e")
		self.owner.hero.gainArmor(4)


# Force of Nature
class EX1_571(Card):
	def activate(self):
		for i in range(3):
			self.owner.summon("EX1_tk9")

class EX1_tk9(Card):
	endTurn = lambda self: self.destroy()


# Savagery
class EX1_578(Card):
	def activate(self, target):
		target.damage(self.owner.hero.attack)
