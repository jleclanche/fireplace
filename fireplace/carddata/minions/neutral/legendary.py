import random
from ...card import *


# The Black Knight
class EX1_002(Card):
	action = destroyTarget


# Bloodmage Thalnos
class EX1_012(Card):
	deathrattle = drawCard


# Sylvanas Windrunner
class EX1_016(Card):
	def deathrattle(self):
		if self.controller.opponent.field:
			self.controller.takeControl(random.choice(self.controller.opponent.field))


# Cairne Bloodhoof
class EX1_110(Card):
	deathrattle = summonMinion("EX1_110t")


# Leeroy Jenkins
class EX1_116(Card):
	def action(self):
		self.controller.opponent.summon("EX1_116t")
		self.controller.opponent.summon("EX1_116t")


# Baron Geddon
class EX1_249(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			if target is not self:
				self.hit(target, 2)


# Ragnaros the Firelord
class EX1_298(Card):
	cantAttack = True
	def TURN_END(self, player):
		self.hit(random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS)), 8)


# Nat Pagle
class EX1_557(Card):
	def OWN_TURN_BEGIN(self):
		if random.choice((0, 1)):
			self.controller.draw()


# Harrison Jones
class EX1_558(Card):
	def action(self):
		weapon = self.controller.opponent.hero.weapon
		if weapon:
			weapon.destroy()
			self.controller.draw(weapon.durability)


# Malygos
class EX1_563(Card):
	spellpower = 5


# The Beast
class EX1_577(Card):
	def deathrattle(self):
		self.controller.opponent.summon("EX1_finkle")


# Illidan Stormrage
class EX1_614(Card):
	def OWN_CARD_PLAYED(self, card):
		self.controller.summon("EX1_614t")


# Deathwing
class NEW1_030(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			# Let's not kill ourselves in the process
			if target is not self:
				target.destroy()
		self.controller.discardHand()
