from ..card import *


# Guardian of Kings
class CS2_088(Card):
	def action(self):
		self.controller.hero.heal(6)
