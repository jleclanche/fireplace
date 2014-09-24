from ...enums import GameTag
from ..card import *


# Guardian of Kings
class CS2_088(Card):
	def action(self):
		self.controller.hero.heal(6)


# Argent Protector
class EX1_362(Card):
	def action(self, target):
		target.setTag(GameTag.DIVINE_SHIELD, True)


# Tirion Fordring
class EX1_383(Card):
	action = equipWeapon("EX1_383t")
