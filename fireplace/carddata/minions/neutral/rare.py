from ...card import *


# Abomination
class EX1_097(Card):
	def deathrattle(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			target.damage(2)


# Bloodsail Corsair
class NEW1_025(Card):
	def action(self):
		weapon = self.controller.opponent.hero.weapon
		if self.controller.opponent.hero.weapon:
			weapon.loseDurability(1)
