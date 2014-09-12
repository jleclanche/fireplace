import random
from ..card import *
from fireplace.enums import CardType


# Holy Nova
class CS1_112(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			if target.controller == self.controller:
				target.heal(2)
			else:
				target.damage(2)


# Shadow Word: Pain
class CS2_234(Card):
	action = lambda self, target: target.destroy()


# Mind Blast
class DS1_233(Card):
	def action(self):
		self.controller.opponent.hero.damage(5)


# Mindgames
class EX1_345(Card):
	def action(self):
		creatures = [c for c in self.controller.opponent.deck if c.type == CardType.MINION]
		if creatures:
			creature = random.choice(creatures).id
		else:
			creature = "EX1_345t"
		self.controller.summon(creature)


# Shadow Word: Death
class EX1_622(Card):
	action = lambda self, target: target.destroy()


# Holy Fire
class EX1_624(Card):
	def action(self, target):
		target.damage(5)
		self.controller.hero.heal(5)
