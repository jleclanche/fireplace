"""
Spare Parts
"""

from ..utils import *


# Armor Plating
class PART_001:
	action = buffTarget("PART_001e")


# Time Rewinder
class PART_002:
	action = bounceTarget


# Rusty Horn
class PART_003:
	def action(self, target):
		target.taunt = True


# Finicky Cloakfield
class PART_004:
	action = buffTarget("PART_004e")

class PART_004e:
	def OWN_TURN_BEGIN(self):
		self.destroy()


# Emergency Coolant
class PART_005:
	def action(self, target):
		target.frozen = True


# Reversing Switch
class PART_006:
	action = buffTarget("PART_006a")

class PART_006a:
	atk = lambda self, i: self.atk
	health = lambda self, i: self.health

	def apply(self, target):
		self.health = target.atk
		self.atk = target.health


# Whirling Blades
class PART_007:
	action = buffTarget("PART_007e")
