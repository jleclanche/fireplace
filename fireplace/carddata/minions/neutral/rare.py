import random
from ...card import *
from fireplace.enums import CardType, Race


# Injured Blademaster
class CS2_181(Card):
	def action(self):
		self.hit(self, 4)


# Young Priestess
class EX1_004(Card):
	def OWN_TURN_END(self):
		other_minions = [t for t in self.controller.field if t is not self]
		if other_minions:
			random.choice(other_minions).buff("EX1_004e")

class EX1_004e(Card):
	Health = 1


# Alarm-o-Bot
class EX1_006(Card):
	def OWN_TURN_BEGIN(self):
		minions = self.controller.hand.filterByType(CardType.MINION)
		if minions:
			self.bounce()
			self.controller.summon(random.choice(minions))

# Ancient Watcher
class EX1_045(Card):
	cantAttack = True


# Coldlight Oracle
class EX1_050(Card):
	def action(self):
		self.controller.draw(2)
		self.controller.opponent.draw(2)


# Mind Control Tech
class EX1_085(Card):
	def action(self):
		if len(self.controller.opponent.field) >= 4:
			self.controller.takeControl(random.choice(self.controller.opponent.field))


# Arcane Golem
class EX1_089(Card):
	def action(self):
		self.controller.opponent.maxMana += 1


# Defender of Argus
class EX1_093(Card):
	def action(self):
		for target in self.adjacentMinions:
			target.buff("EX1_093e")

class EX1_093e(Card):
	Atk = 1
	Health = 1
	taunt = True


# Abomination
class EX1_097(Card):
	def deathrattle(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			self.hit(target, 2)


# Coldlight Seer
class EX1_103(Card):
	def action(self):
		for minion in self.controller.field:
			if minion.race == Race.MURLOC:
				minion.buff("EX1_103e")

class EX1_103e(Card):
	Health = 2


# Ancient Mage
class EX1_584(Card):
	def action(self):
		for target in self.adjacentMinions:
			target.buff("EX1_584e")

class EX1_584e(Card):
	spellpower = 1


# Imp Master
class EX1_597(Card):
	def OWN_TURN_END(self):
		self.hit(self, 1)
		self.controller.summon("EX1_598")


# Nerubian Egg
class FP1_007(Card):
	deathrattle = summonMinion("FP1_007t")


# Sludge Belcher
class FP1_012(Card):
	deathrattle = summonMinion("FP1_012t")


# Wild Pyromancer
class NEW1_020(Card):
	def AFTER_OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			for target in self.controller.getTargets(TARGET_ALL_MINIONS):
				self.hit(target, 1)


# Bloodsail Corsair
class NEW1_025(Card):
	def action(self):
		weapon = self.controller.opponent.hero.weapon
		if self.controller.opponent.hero.weapon:
			weapon.durability -= 1


# Master Swordsmith
class NEW1_037(Card):
	def OWN_TURN_END(self):
		other_minions = [t for t in self.controller.field if t is not self]
		if other_minions:
			random.choice(other_minions).buff("NEW1_037e")

class NEW1_037e(Card):
	Atk = 1


# Stampeding Kodo
class NEW1_041(Card):
	def action(self):
		targets = [t for t in self.controller.opponent.field if t.atk <= 2]
		if targets:
			random.choice(targets).destroy()
