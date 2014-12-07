from ..card import *


# The Coin
class GAME_005(Card):
	def action(self):
		self.controller.tempMana += 1


# RFG

# Adrenaline Rush
class NEW1_006(Card):
	action = drawCard
	combo = drawCards(2)
