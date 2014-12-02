import random
from fireplace.enums import GameTag, Race
from ..card import *


# Frost Shock
class CS2_037(Card):
	def action(self, target):
		self.hit(target, 1)
		target.frozen = True


# Ancestral Spirit
class CS2_038(Card):
	action = buffTarget("CS2_038e")

class CS2_038e(Card):
	def deathrattle(self):
		self.controller.summon(self.id)


# Windfury
class CS2_039(Card):
	def action(self, target):
		target.setTag(GameTag.WINDFURY, True)


# Ancestral Healing
class CS2_041(Card):
	def action(self, target):
		self.heal(target, target.maxHealth)
		target.buff("CS2_041e")


# Rockbiter Weapon
class CS2_045(Card):
	action = buffTarget("CS2_045e")

class CS2_045e(Card):
	Atk = 3


# Bloodlust
class CS2_046(Card):
	def action(self):
		for target in self.controller.field:
			target.buff("CS2_046e")

class CS2_046e(Card):
	Atk = 3


# Lightning Bolt
class EX1_238(Card):
	action = damageTarget(3)


# Lava Burst
class EX1_241(Card):
	overload = 2
	action = damageTarget(5)


# Totemic Might
class EX1_244(Card):
	def action(self):
		for target in self.controller.field:
			if target.race == Race.TOTEM:
				target.buff("EX1_244e")


class EX1_244e(Card):
	Health = 2


class EX1_248(Card):
	overload = 2
	def action(self):
		self.owner.summon("EX1_tk11")
		self.owner.summon("EX1_tk11")


# Forked Lightning
class EX1_251(Card):
	overload = 2
	def action(self):
		targets = random.sample(self.controller.opponent.field, 2)
		for target in targets:
			self.hit(target, 2)


# Lightning Storm
class EX1_259(Card):
	overload = 2
	def action(self):
		for target in self.controller.opponent.field:
			self.hit(target, random.choice((2, 3)))


# Reincarnate
class FP1_025(Card):
	def action(self, target):
		target.destroy()
		self.controller.summon(target.id)
