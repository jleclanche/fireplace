import random
from ..card import *
from fireplace.enums import CardType


# Holy Nova
class CS1_112(Card):
	def activate(self):
		for target in self.owner.getTargets(TARGET_ALL_CHARACTERS):
			if target.owner == self.owner:
				target.heal(2)
			else:
				target.damage(2)


# Shadow Word: Pain
class CS2_234(Card):
	activate = lambda self, target: target.destroy()


# Mind Blast
class DS1_233(Card):
	def activate(self):
		self.owner.opponent.hero.damage(5)


# Mindgames
class EX1_345(Card):
	def activate(self):
		creatures = [c for c in self.owner.opponent.deck if c.type == CardType.MINION]
		if creatures:
			creature = random.choice(creatures).id
		else:
			creature = "EX1_345t"
		self.owner.summon(creature)


# Shadow Word: Death
class EX1_622(Card):
	activate = lambda self, target: target.destroy()


# Holy Fire
class EX1_624(Card):
	def activate(self, target):
		target.damage(5)
		self.owner.hero.heal(5)
