from .card import Card
from ..enums import Race
from ..targeting import *


# Enhanced
class CS2_122e(Card):
	atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source


# Furious Howl
class DS1_175o(Card):
	atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST and target is not self.source
