from ..card import *


# The Coin
class GAME_005(Card):
	def action(self):
		self.controller.tempMana += 1
