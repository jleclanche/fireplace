import random
from ..card import *


# Lightwarden
class EX1_001(Card):
	def HEAL(self, source, target, amount):
		self.buff("EX1_001e")

class EX1_001e(Card):
	Atk = 2


# Cabal Shadow Priest
class EX1_091(Card):
	def action(self, target):
		self.controller.takeControl(target)


# Lightspawn
class EX1_335(Card):
	def UPDATE(self):
		if self.atk != self.health:
			# self.atk = self.health
			# Haha! You thought this would be that easy, huh? THINK AGAIN!
			# Attack is the sum of the ATK of the entity and all its slots.
			# This matters because auras are applied to lightspawn, and lightspawn
			# doesn't actually respect those auras.
			# Now, we can either hack around this with internal buffs, tags etc... or we
			# can set the attack to *less* than the health, taking buffs into account.
			# Incidentally, this means that Lightspawn's GameTag.ATK can go negative.
			# Tell me, Blizzard, is it really such a coincidence its base attack is 0?
			self.atk = self.health - self.extraAtk


# Lightwell
class EX1_341(Card):
	def OWN_TURN_BEGIN(self):
		targets = [t for t in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS) if t.damage]
		self.heal(random.choice(targets), 3)


# Temple Enforcer
class EX1_623(Card):
	action = buffTarget("EX1_623e")

class EX1_623e(Card):
	Health = 3


# Dark Cultist
class FP1_023(Card):
	def deathrattle(self):
		if self.controller.field:
			random.choice(self.controller.field).buff("FP1_023e")

class FP1_023e(Card):
	Health = 3
