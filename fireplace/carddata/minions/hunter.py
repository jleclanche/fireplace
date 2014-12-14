import random
from fireplace.enums import Race
from ..card import *


# Houndmaster
class DS1_070(Card):
	action = buffTarget("DS1_070o")

class DS1_070o(Card):
	Atk = 2
	Health = 2
	Taunt = True


# Timber Wolf
class DS1_175(Card):
	aura = "DS1_175o"

# Furious Howl
class DS1_175o(Card):
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST and target is not self.source


# Tundra Rhino
class DS1_178(Card):
	aura = "DS1_178e"

# Charge
class DS1_178e(Card):
	Charge = True
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST


# Scavenging Hyena
class EX1_531(Card):
	def OWN_MINION_DESTROYED(self, minion):
		if minion.race == Race.BEAST:
			self.buff("EX1_531e")

class EX1_531e(Card):
	Atk = 2
	Health = 1


# Savannah Highmane
class EX1_534(Card):
	def deathrattle(self):
		self.controller.summon("EX1_534t")
		self.controller.summon("EX1_534t")


# Webspinner
class FP1_011(Card):
	def deathrattle(self):
		self.controller.give(random.choice(self.data.entourage))
