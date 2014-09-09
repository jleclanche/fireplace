import random
from ..card import *


# Cleave
class CS2_114(Card):
	def activate(self):
		targets = random.sample(self.owner.opponent.field, 2)
		for target in targets:
			target.damage(2)
