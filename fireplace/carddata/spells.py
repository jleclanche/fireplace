from ..cards import Spell


# The Coin
class GAME_005(Spell):
	cost = 0

	def action(self):
		self.owner.additionalCrystals += 1
