from .card import *


# Perdition's Blace
class EX1_133(Card):
	action = damageTarget(1)
	combo = damageTarget(2)


# Doomhammer
class EX1_567(Card):
	overload = 2


# Death's Bite
class FP1_021(Card):
	def deathrattle(self):
		for target in self.controller.game.board:
			target.damage(1)
