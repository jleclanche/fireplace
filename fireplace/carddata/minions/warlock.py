import random
from ..card import *


# Blood Imp
class CS2_059(Card):
	def endTurn(self):
		if self.game.currentPlayer is self.owner:
			if self.owner.field:
				random.choice(self.owner.field).buff("CS2_059o")

class CS2_059o(Card):
	health = 1


# Felguard
class EX1_301(Card):
	def activate(self):
		self.owner.loseMana(1)


# Succubus
class EX1_306(Card):
	activate = discard(1)


# Doomguard
class EX1_310(Card):
	activate = discard(2)


# Pit Lord
class EX1_313(Card):
	def activate(self):
		self.owner.hero.damage(5)


# Flame Imp
class EX1_319(Card):
	def activate(self):
		self.owner.hero.damage(3)


# Lord Jaraxxus
class EX1_323(Card):
	def activate(self):
		self.removeFromField()
		self.owner.setHero("EX1_323h")
