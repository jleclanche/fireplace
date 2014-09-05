import random
from fireplace.enums import Race
from ..card import *


# Arcane Shot
class DS1_185(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.damage(2)


# Deadly Shot
class EX1_617(Card):
	def activate(self):
		random.choice(self.owner.opponent.field).destroy()


# Animal Companion
class NEW1_031(Card):
	def activate(self):
		self.owner.summon(random.choice(self.entourage))


# Kill Command
class EX1_539(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		for minion in self.owner.field:
			if minion.race == Race.BEAST:
				return target.damage(5)
		target.damage(3)
