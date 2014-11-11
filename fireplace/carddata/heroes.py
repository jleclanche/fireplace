"""
Heroes and their Hero Powers
"""
import random
from .card import *


# Garrosh Hellscream
class HERO_01(Card):
	power = "CS2_102"

# Armor Up!
class CS2_102(Card):
	def action(self):
		self.controller.hero.armor += 2


# Thrall
class HERO_02(Card):
	power = "CS2_049"

# Totemic Call
class CS2_049(Card):
	def action(self):
		entourage = self.data.entourage
		for minion in self.controller.field:
			if minion.id in entourage:
				entourage.remove(minion.id)
		self.controller.summon(random.choice(entourage))


# Valeera Sanguinar
class HERO_03(Card):
	power = "CS2_083b"

# Dagger Mastery
class CS2_083b(Card):
	def action(self):
		self.controller.summon("CS2_082")


# Uther Lightbringer
class HERO_04(Card):
	power = "CS2_101"

# Reinforce
class CS2_101(Card):
	action = summonMinion("CS2_101t")


# Rexxar
class HERO_05(Card):
	power = "DS1h_292"

# Steady Shot
class DS1h_292(Card):
	action = damageEnemyHero(2)


# Malfurion Stormrage
class HERO_06(Card):
	power = "CS2_017"

# Shapeshift
class CS2_017(Card):
	def action(self):
		self.controller.hero.buff("CS2_017o")

# Claws
class CS2_017o(Card):
	attack = 1


# Gul'dan
class HERO_07(Card):
	power = "CS2_056"

# Life Tap
class CS2_056(Card):
	def action(self):
		self.controller.hero.damage(2)
		self.controller.draw()


# Jaina Proudmoore
class HERO_08(Card):
	power = "CS2_034"

# Fireblast
class CS2_034(Card):
	def action(self, target):
		target.damage(1)


# Anduin Wrynn
class HERO_09(Card):
	power = "CS1h_001"

# Lesser Heal
class CS1h_001(Card):
	def action(self, target):
		target.heal(2)


# Lord Jaraxxus
class EX1_323h(Card):
	power = "EX1_tk33"

# INFERNO!
class EX1_tk33(Card):
	action = summonMinion("EX1_tk34")
