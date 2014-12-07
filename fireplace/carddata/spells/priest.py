import random
from ..card import *
from fireplace.enums import CardType


# Power Word: Shield
class CS2_004(Card):
	def action(self, target):
		target.buff("CS2_004e")
		self.controller.draw()

class CS2_004e(Card):
	Health = 2


# Holy Nova
class CS1_112(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			if target.controller == self.controller:
				self.heal(target, 2)
			else:
				self.hit(target, 2)


# Mind Control
class CS1_113(Card):
	def action(self, target):
		self.controller.takeControl(target)


# Mind Vision
class CS2_003(Card):
	def action(self):
		if self.controller.opponent.hand:
			self.controller.give(random.choice(self.controller.opponent.hand).id)


# Shadow Word: Pain
class CS2_234(Card):
	action = destroyTarget


# Mind Blast
class DS1_233(Card):
	action = damageEnemyHero(5)


# Silence
class EX1_332(Card):
	action = silenceTarget


# Mindgames
class EX1_345(Card):
	def action(self):
		creatures = [c for c in self.controller.opponent.deck if c.type == CardType.MINION]
		if creatures:
			creature = random.choice(creatures).id
		else:
			creature = "EX1_345t"
		self.controller.summon(creature)


# Circle of Healing
class EX1_621(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			self.heal(target, 4)


# Shadow Word: Death
class EX1_622(Card):
	action = destroyTarget


# Holy Fire
class EX1_624(Card):
	def action(self, target):
		self.hit(target, 5)
		self.heal(self.controller.hero, 5)
