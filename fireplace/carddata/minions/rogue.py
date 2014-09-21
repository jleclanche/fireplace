import random
from ..card import *


# Defias Ringleader
class EX1_131(Card):
	combo = summonMinion("EX1_131t")


# SI:7 Agent
class EX1_134(Card):
	combo = damageTarget(2)


# Anub'ar Ambusher
class FP1_026(Card):
	def deathrattle(self):
		if self.controller.field:
			random.choice(self.controller.field).bounce()


# Kidnapper
class NEW1_005(Card):
	combo = bounceTarget


# Master of Disguise
class NEW1_014(Card):
	def battlecry(self, target):
		target.stealth()
