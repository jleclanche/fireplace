import random
from ..card import *



# Claw
class CS2_005(Card):
	def action(self):
		buffSelf(self, "CS2_005o")
		self.controller.hero.armor += 2

class CS2_005o(Card):
	atk = 2


# Healing Touch
class CS2_007(Card):
	action = healTarget(8)


# Moonfire
class CS2_008(Card):
	action = damageTarget(1)


# Mark of the Wild
class CS2_009(Card):
	action = buffTarget("CS2_009e")

class CS2_009e(Card):
	atk = 2
	health = 2
	taunt = True


# Savage Roar
class CS2_011(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			target.buff("CS2_011o")

class CS2_011o(Card):
	atk = 2


# Swipe
class CS2_012(Card):
	def action(self, target):
		for character in self.controller.getTargets(TARGET_ENEMY_CHARACTERS):
			if character is target:
				self.hit(character, 4)
			else:
				self.hit(character, 1)


# Wild Growth
class CS2_013(Card):
	def action(self):
		if self.controller.maxMana < self.controller.MAX_MANA:
			self.controller.maxMana += 1
		else:
			self.controller.give("CS2_013t")

class CS2_013t(Card):
	action = drawCard


# Soul of the Forest
class EX1_158(Card):
	def action(self):
		for target in self.controller.field:
			target.buff("EX1_158e")

class EX1_158e(Card):
	def deathrattle(self):
		self.controller.summon("EX1_158t")


# Naturalize
class EX1_161(Card):
	def action(self, target):
		target.destroy()
		self.controller.opponent.draw(2)


# Starfire
class EX1_173(Card):
	def action(self, target):
		self.hit(character, 5)
		self.controller.draw()


# Bite
class EX1_570(Card):
	def action(self):
		buffSelf(self, "EX1_570e")
		self.controller.hero.armor += 4

class EX1_570e(Card):
	atk = 4


# Force of Nature
class EX1_571(Card):
	def action(self):
		for i in range(3):
			self.controller.summon("EX1_tk9")

class EX1_tk9(Card):
	def onTurnEnd(self, player):
		self.destroy()


# Savagery
class EX1_578(Card):
	def action(self, target):
		self.hit(target, self.controller.hero.atk)
