from ..card import *


# Blessing of Might
class CS2_087(Card):
	action = buffTarget("CS2_087e")

class CS2_087e(Card):
	Atk = 3


# Holy Light
class CS2_089(Card):
	action = healTarget(6)


# Blessing of Kings
class CS2_092(Card):
	action = buffTarget("CS2_092e")

class CS2_092e(Card):
	Atk = 4
	Health = 4


# Consecration
class CS2_093(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ENEMY_CHARACTERS):
			self.hit(target, 2)


# Hammer of Wrath
class CS2_094(Card):
	def action(self, target):
		self.hit(target, 3)
		self.controller.draw()


# Divine Favor
class EX1_349(Card):
	def action(self):
		diff = len(self.controller.opponent.hand) - len(self.controller.hand)
		self.controller.draw(max(0, diff))


# Lay on Hands
class EX1_354(Card):
	def action(self, target):
		self.heal(target, 8)
		self.controller.draw(3)


# Holy Wrath
class EX1_365(Card):
	def action(self, target):
		drawn = self.controller.draw()
		self.hit(target, drawn[0].cost)


# Hand of Protection
class EX1_371(Card):
	def action(self, target):
		target.shield = True
