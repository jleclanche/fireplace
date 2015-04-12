from ..utils import *


##
# Minions

# Metaltooth Leaper
class GVG_048:
	def action(self):
		targets = self.controller.field.filter(race=Race.MECHANICAL).exclude(self)
		for target in targets:
			self.buff(target, "GVG_048e")


# Gahz'rilla
class GVG_049:
	def SELF_DAMAGE(self, source, amount):
		self.buff(self, "GVG_049e")

class GVG_049e:
	atk = lambda self, i: i*2


##
# Spells

# Call Pet
class GVG_017:
	def action(self):
		card = self.controller.draw()
		if card.type == CardType.MINION and card.race == Race.BEAST:
			self.buff(card, "GVG_017e")


# Cobra Shot
class GVG_073:
	def action(self, target):
		self.hit(target, 3)
		self.hit(self.controller.opponent.hero, 3)


##
# Weapons

# Glaivezooka
class GVG_043:
	def action(self):
		if self.controller.field:
			self.buff(random.choice(self.controller.field), "GVG_043e")
