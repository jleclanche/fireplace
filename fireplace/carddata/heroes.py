"""
Heroes and their Hero Powers
"""
from ..targeting import *
from .card import Card


# Garrosh Hellscream
class HERO_01(Card):
	power = "CS2_102"

# Armor Up!
class CS2_102(Card):
	def activate(self):
		self.owner.hero.gainArmor(2)


# Thrall
class HERO_02(Card):
	power = "CS2_049"  # Totemic Call


# Valeera Sanguinar
class HERO_03(Card):
	power = "CS2_083b"

# Dagger Mastery
class CS2_083b(Card):
	def activate(self):
		self.owner.equip("CS2_082")


# Uther Lightbringer
class HERO_04(Card):
	power = "CS2_101"

# Reinforce
class CS2_101(Card):
	def activate(self):
		self.owner.summon("CS2_101t")


# Rexxar
class HERO_05(Card):
	power = "DS1h_292"

# Steady Shot
class DS1h_292(Card):
	def activate(self):
		self.owner.opponent.hero.damage(2)


# Malfurion Stormrage
class HERO_06(Card):
	power = "CS2_017"

# Shapeshift
class CS2_017(Card):
	def activate(self):
		self.owner.hero.buff("CS2_017o")

# Claws
class CS2_017o(Card):
	attack = 1


# Gul'dan
class HERO_07(Card):
	power = "CS2_056"

# Life Tap
class CS2_056(Card):
	def activate(self):
		self.owner.hero.damage(2)
		self.owner.draw()


# Jaina Proudmoore
class HERO_08(Card):
	power = "CS2_034"

# Fireblast
class CS2_034(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.damage(1)


# Anduin Wrynn
class HERO_09(Card):
	power = "CS1h_001"

# Lesser Heal
class CS1h_001(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.heal(2)


# Lord Jaraxxus
class EX1_323h(Card):
	power = "EX1_tk33"

# INFERNO!
class EX1_tk33(Card):
	def activate(self):
		self.owner.summon("EX1_tk34")
