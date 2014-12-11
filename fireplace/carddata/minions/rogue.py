import random
from ..card import *


# Defias Ringleader
class EX1_131(Card):
	combo = summonMinion("EX1_131t")


# SI:7 Agent
class EX1_134(Card):
	combo = damageTarget(2)


# Edwin VanCleef
class EX1_613(Card):
	def combo(self):
		for i in range(self.controller.cardsPlayedThisTurn):
			self.buff("EX1_613e")

class EX1_613e(Card):
	Atk = 2
	Health = 2


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
		target.stealthed = True
