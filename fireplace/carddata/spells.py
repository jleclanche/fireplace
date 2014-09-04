import random
from ..enums import Race
from ..targeting import *
from .card import Card


# The Coin
class GAME_005(Card):
	def activate(self):
		self.owner.buff("GAME_005e")

class GAME_005e(Card):
	mana = 1
	oneTurnEffect = True


# Holy Nova
class CS1_112(Card):
	targeting = TARGET_ALL_CHARACTERS
	def activate(self):
		for target in self.targets:
			if target.owner == self.owner:
				target.heal(2)
			else:
				target.damage(2)

# Cleave
class CS2_114(Card):
	targeting = TARGET_ENEMY_MINIONS
	minTargets = 2
	def activate(self):
		targets = random.sample(self.targets, 2)
		for target in targets:
			target.damage(2)


# Soul of the Forest
class EX1_158(Card):
	targeting = TARGET_FRIENDLY_MINIONS
	def activate(self):
		for target in self.targets:
			target.buff("EX1_158e")

class EX1_158e(Card):
	def deathrattle(self):
		self.owner.owner.summon("EX1_158t")


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
