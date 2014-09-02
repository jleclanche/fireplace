import random
from ..targeting import *
from .card import Card


# The Coin
class GAME_005(Card):
	def activate(self):
		self.owner.buff("GAME_005e")

class GAME_005e(Card):
	mana = 1
	oneTurnEffect = True



# Holy Nova
class CS1_112(Card):
	targeting = TARGET_ALL_CHARACTERS
	def activate(self):
		for target in self.targets:
			if target.owner == self.owner:
				target.heal(2)
			else:
				target.damage(2)

# Cleave
class CS2_114(Card):
	targeting = TARGET_ENEMY_MINIONS
	minTargets = 2
	def activate(self):
		targets = random.sample(self.targets, 2)
		for target in targets:
			target.damage(2)
