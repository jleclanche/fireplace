from ..cards import Minion


# Novice Engineer
class EX1_015(Minion):
	attack = 1
	health = 1
	cost = 2

	def battlecry(self):
		self.owner.draw()
