from ..card import *


# Cruel Taskmaster
class EX1_603(Card):
	def action(self, target):
		target.buff("EX1_603e")
		self.hit(target, 1)

class EX1_603e(Card):
	Atk = 2
