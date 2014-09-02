from ..enums import Race
from ..targeting import *


# Enhanced
class CS2_122e:
	atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self


# Furious Howl
class DS1_175o:
	atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.type == Race.BEAST and target is not self
