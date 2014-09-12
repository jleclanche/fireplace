import random
from fireplace.enums import Zone
from ..card import *


# Charge
class CS2_103(Card):
	activate = buffTarget("CS2_103e")

class CS2_103e(Card):
	atk = 2
	charge = True


# Rampage
class CS2_104(Card):
	activate = buffTarget("CS2_104e")

class CS2_104e(Card):
	atk = 3
	health = 3


# Heroic Strike
class CS2_105e(Card):
	activate = buffSelf("CS2_105e")

class CS2_105e(Card):
	atk = 4


# Execute
class CS2_108(Card):
	def activate(self, target):
		target.destroy()


# Cleave
class CS2_114(Card):
	def activate(self):
		targets = random.sample(self.controller.opponent.field, 2)
		for target in targets:
			target.damage(2)


# Slam
class EX1_391(Card):
	def activate(self, target):
		target.damage(2)
		if target.zone == Zone.PLAY:
			self.controller.draw()


# Battle Rage
class EX1_392(Card):
	def activate(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			if target.isDamaged():
				self.controller.draw()


# Whirlwind
class EX1_400(Card):
	def activate(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			target.damage(1)


# Brawl
class EX1_407(Card):
	def activate(self):
		board = self.controller.getTargets(TARGET_ALL_MINIONS)
		for minion in random.sample(board, len(board) - 1):
			minion.destroy()


# Mortal Strike
class EX1_408(Card):
	def activate(self, target):
		target.damage(6 if self.controller.hero.health <= 12 else 4)


# Upgrade!
class EX1_409(Card):
	def activate(self):
		self.controller.hero.weapon.buff("EX1_409e")

class EX1_409e(Card):
	atk = 1
	durability = 1


# Shield Slam
class EX1_410(Card):
	def activate(self, target):
		target.damage(self.controller.hero.armor)


# Shield Block
class EX1_606(Card):
	def activate(self):
		self.controller.hero.gainArmor(5)
		self.controller.draw()


# Inner Rage
class EX1_607(Card):
	def activate(self, target):
		target.buff("EX1_607e")
		target.damage(1)

class EX1_607e(Card):
	atk = 2
