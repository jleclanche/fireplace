import random
from ..targeting import *


# The Coin
class GAME_005:
	def activate(self):
		self.owner.buff("GAME_005e")

class GAME_005e:
	mana = 1
	oneTurnEffect = True



# Holy Nova
class CS1_112:
	targeting = TARGET_ALL_CHARACTERS
	def activate(self):
		for target in self.targets:
			if target.owner == self.owner:
				target.heal(2)
			else:
				target.damage(2)

# Cleave
class CS2_114:
	targeting = TARGET_ENEMY_MINIONS
	minTargets = 2
	def activate(self):
		targets = random.sample(self.targets, 2)
		for target in targets:
			target.damage(2)
