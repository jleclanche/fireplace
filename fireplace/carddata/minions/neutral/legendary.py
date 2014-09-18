import random
from ...card import *


# Ragnaros the Firelord
class EX1_298(Card):
	cantAttack = True
	def endTurn(self):
		random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS)).damage(8)


# Harrison Jones
class EX1_558(Card):
	def action(self):
		weapon = self.controller.opponent.hero.weapon
		if weapon:
			weapon.destroy()
			self.controller.draw(weapon.durability)
