import random
from ...card import *


# Cairne Bloodhoof
class EX1_110(Card):
	deathrattle = summonMinion("EX1_110t")


# Baron Geddon
class EX1_249(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			if target is not self:
				self.hit(target, 2)


# Ragnaros the Firelord
class EX1_298(Card):
	cantAttack = True
	def onTurnEnd(self, player):
		self.hit(random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS)), 8)


# Nat Pagle
class EX1_557(Card):
	def onOwnTurnBegin(self):
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


# Deathwing
class NEW1_030(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			# Let's not kill ourselves in the process
			if target is not self:
				target.destroy()
		self.controller.discardHand()
