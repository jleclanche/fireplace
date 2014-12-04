from ...card import *
from fireplace.enums import Race


# Big Game Hunter
class EX1_005(Card):
	action = destroyTarget


# Murloc Warleader
class EX1_507(Card):
	aura = "EX1_507e"

class EX1_507e(Card):
	Atk = 2
	Health = 1
	def isValidTarget(self, target):
		return target.race == Race.MURLOC and target is not self.source


# Hungry Crab
class NEW1_017(Card):
	def action(self, target):
		target.destroy()
		self.buff("NEW1_017e")

class NEW1_017e(Card):
	Atk = 2
	Health = 2


# Doomsayer
class NEW1_021(Card):
	def OWN_TURN_BEGIN(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			target.destroy()


# Southsea Captain
class NEW1_027(Card):
	aura = "NEW1_027e"

class NEW1_027e(Card):
	Atk = 1
	Health = 1
	def isValidTarget(self, target):
		return target.race == Race.PIRATE and target is not self.source
