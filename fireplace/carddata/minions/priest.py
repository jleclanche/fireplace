from ..card import *


# Cabal Shadow Priest
class EX1_091(Card):
	def action(self, target):
		self.controller.takeControl(target)


# Temple Enforcer
class EX1_623(Card):
	action = buffTarget("EX1_623e")

class EX1_623e(Card):
	health = 3
