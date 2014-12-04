import random
from fireplace.enums import Race
from ..card import *


# Blood Imp
class CS2_059(Card):
	def OWN_TURN_END(self):
		if self.controller.field:
			random.choice(self.controller.field).buff("CS2_059o")

class CS2_059o(Card):
	Health = 1


# Felguard
class EX1_301(Card):
	def action(self):
		self.controller.maxMana -= 1


# Succubus
class EX1_306(Card):
	action = discard(1)


# Doomguard
class EX1_310(Card):
	action = discard(2)


# Pit Lord
class EX1_313(Card):
	def action(self):
		self.hit(self.controller.hero, 5)


# Flame Imp
class EX1_319(Card):
	def action(self):
		self.hit(self.controller.hero, 3)


# Lord Jaraxxus
class EX1_323(Card):
	def action(self):
		self.removeFromField()
		self.controller.summon("EX1_323h")
		self.controller.summon("EX1_323w")


# Voidcaller
class FP1_022(Card):
	def deathrattle(self):
		demons = self.controller.hand.filterByRace(Race.DEMON)
		if demons:
			self.controller.summon(random.choice(demons))
