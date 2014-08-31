"""
Heroes and their Hero Powers
"""
from ..targeting import *


# Garrosh Hellscream
class HERO_01:
	power = "CS2_102"

# Armor Up!
class CS2_102:
	def activate(self):
		self.owner.hero.gainArmor(2)


# Thrall
class HERO_02:
	power = "CS2_049"  # Totemic Call


# Valeera Sanguinar
class HERO_03:
	power = "CS2_083b"  # Dagger Mastery


# Uther Lightbringer
class HERO_04:
	power = "CS2_101"  # Reinforce


# Rexxar
class HERO_05:
	power = "DS1h_292"  # Steady Shot


# Malfurion Stormrage
class HERO_06:
	power = "CS2_017"  # Shapeshift


# Gul'dan
class HERO_07:
	power = "CS2_056"  # Life Tap


# Jaina Proudmoore
class HERO_08:
	power = "CS2_034"

# Fireblast
class CS2_034:
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.damage(1)


# Anduin Wrynn
class HERO_09:
	power = "CS1h_001"  # Lesser Heal


# Lord Jaraxxus
class EX1_323h:
	power = "EX1_tk33"  # INFERNO!
