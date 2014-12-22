"""
Heroes and their Hero Powers
"""

from ..utils import *


# Garrosh Hellscream
class HERO_01:
	power = "CS2_102"

# Armor Up!
class CS2_102:
	action = gainArmor(2)


# Thrall
class HERO_02:
	power = "CS2_049"

# Totemic Call
class CS2_049:
	def action(self):
		entourage = self.data.entourage
		for minion in self.controller.field:
			if minion.id in entourage:
				entourage.remove(minion.id)
		self.controller.summon(random.choice(entourage))

# Healing Totem
class NEW1_009:
	def OWN_TURN_END(self):
		targets = self.controller.getTargets(TARGET_FRIENDLY_MINIONS)
		for target in targets:
			self.heal(target, 1)



# Valeera Sanguinar
class HERO_03:
	power = "CS2_083b"

# Dagger Mastery
class CS2_083b:
	def action(self):
		self.controller.summon("CS2_082")


# Uther Lightbringer
class HERO_04:
	power = "CS2_101"

# Reinforce
class CS2_101:
	action = summonMinion("CS2_101t")


# Rexxar
class HERO_05:
	power = "DS1h_292"

# Steady Shot
class DS1h_292:
	action = damageEnemyHero(2)


# Malfurion Stormrage
class HERO_06:
	power = "CS2_017"

# Shapeshift
class CS2_017:
	def action(self):
		self.controller.hero.buff("CS2_017o")

# Claws
class CS2_017o:
	attack = 1


# Gul'dan
class HERO_07:
	power = "CS2_056"

# Life Tap
class CS2_056:
	def action(self):
		self.hit(self.controller.hero, 2)
		self.controller.draw()


# Jaina Proudmoore
class HERO_08:
	power = "CS2_034"

# Fireblast
class CS2_034:
	action = damageTarget(1)


# Anduin Wrynn
class HERO_09:
	power = "CS1h_001"

# Lesser Heal
class CS1h_001:
	action = healTarget(2)


# Lord Jaraxxus
class EX1_323h:
	power = "EX1_tk33"

# INFERNO!
class EX1_tk33:
	action = summonMinion("EX1_tk34")
