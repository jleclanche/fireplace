import random
from ..card import *


# Sacrificial Pact
class NEW1_003(Card):
	def activate(self, target):
		target.destroy()
		self.owner.hero.heal(5)
