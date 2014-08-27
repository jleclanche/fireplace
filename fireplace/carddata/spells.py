from ..cards import Spell
from ..targeting import *


# The Coin
class GAME_005(Spell):
	def activate(self):
		self.owner.additionalCrystals += 1

# Holy Nova
class CS1_112(Spell):
	targeting = TARGET_ALL_CHARACTERS
	def activate(self):
		for target in self.targets:
			if target.owner == self.owner:
				target.heal(2)
			else:
				target.damage(2)
