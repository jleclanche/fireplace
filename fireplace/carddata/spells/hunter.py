import random
from fireplace.enums import Race
from ..card import *


# Multi-Shot
class DS1_183(Card):
	def activate(self):
		targets = random.sample(self.owner.opponent.field, 2)
		for target in targets:
			target.damage(3)


# Arcane Shot
class DS1_185(Card):
	def activate(self, target):
		target.damage(2)


# Unleash the Hounds
class EX1_538(Card):
	def activate(self):
		for i in range(len(self.owner.opponent.field)):
			self.owner.summon("EX1_538t")


# Kill Command
class EX1_539(Card):
	def activate(self, target):
		for minion in self.owner.field:
			if minion.race == Race.BEAST:
				return target.damage(5)
		target.damage(3)


# Flare
class EX1_544(Card):
	def activate(self):
		for minion in self.owner.getTargets(TARGET_ALL_MINIONS):
			minion.stealth = False
		for secret in self.owner.opponent.secrets:
			secret.destroy()
		self.owner.draw()


# Deadly Shot
class EX1_617(Card):
	def activate(self):
		random.choice(self.owner.opponent.field).destroy()


# Animal Companion
class NEW1_031(Card):
	def activate(self):
		self.owner.summon(random.choice(self.entourage))
