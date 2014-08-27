from ..cards import Spell


# The Coin
class GAME_005(Spell):
	def activate(self):
		self.owner.additionalCrystals += 1
