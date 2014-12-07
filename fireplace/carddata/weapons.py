from .card import *


# Perdition's Blace
class EX1_133(Card):
	action = damageTarget(1)
	combo = damageTarget(2)


# Doomhammer
class EX1_567(Card):
	overload = 2


# Sword of Justice
class EX1_366(Card):
	def OWN_MINION_SUMMONED(self, minion):
		minion.buff("EX1_366e")
		self.durability -= 1

class EX1_366e(Card):
	Atk = 1
	Health = 1


# Death's Bite
class FP1_021(Card):
	def deathrattle(self):
		for target in self.controller.game.board:
			self.hit(target, 1)
