import random
from fireplace.enums import Race
from ..card import *


# Multi-Shot
class DS1_183(Card):
	def action(self):
		targets = random.sample(self.controller.opponent.field, 2)
		for target in targets:
			self.hit(target, 3)


# Arcane Shot
class DS1_185(Card):
	def action(self, target):
		self.hit(target, 3)


# Explosive Shot
class EX1_537(Card):
	def action(self, target):
		for minion in target.adjacentMinions:
			self.hit(minion, 2)
		self.hit(target, 5)


# Unleash the Hounds
class EX1_538(Card):
	def action(self):
		for i in range(len(self.controller.opponent.field)):
			self.controller.summon("EX1_538t")


# Kill Command
class EX1_539(Card):
	def action(self, target):
		for minion in self.controller.field:
			if minion.race == Race.BEAST:
				return self.hit(target, 5)
		self.hit(target, 3)


# Flare
class EX1_544(Card):
	def action(self):
		for minion in self.controller.getTargets(TARGET_ALL_MINIONS):
			if minion.stealthed:
				minion.stealthed = False
		for secret in self.controller.opponent.secrets:
			secret.destroy()
		self.controller.draw()


# Deadly Shot
class EX1_617(Card):
	def action(self):
		random.choice(self.controller.opponent.field).destroy()


# Animal Companion
class NEW1_031(Card):
	def action(self):
		self.controller.summon(random.choice(self.entourage))
