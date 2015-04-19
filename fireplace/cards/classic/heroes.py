"""
Hero Power definitions
"""

from ..utils import *


# Armor Up! (Garrosh Hellscream)
class CS2_102:
	action = [GainArmor(FRIENDLY_HERO, 2)]


# Totemic Call (Thrall)
class CS2_049:
	def action(self):
		entourage = self.data.entourage
		for minion in self.controller.field:
			if minion.id in entourage:
				entourage.remove(minion.id)
		return [Summon(CONTROLLER, random.choice(entourage))]

# Healing Totem
class NEW1_009:
	OWN_TURN_END = [Heal(FRIENDLY_MINIONS, 1)]


# Dagger Mastery (Valeera Sanguinar)
class CS2_083b:
	action = [Summon(CONTROLLER, "CS2_082")]


# Reinforce (Uther Lightbringer)
class CS2_101:
	action = [Summon(CONTROLLER, "CS2_101t")]


# Steady Shot (Rexxar)
class DS1h_292:
	action = [Hit(ENEMY_HERO, 2)]


# Shapeshift (Malfurion Stormrage)
class CS2_017:
	action = [Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)]


# Life Tap (Gul'dan)
class CS2_056:
	action = [Hit(FRIENDLY_HERO, 2), Draw(CONTROLLER, 1)]


# Fireblast (Jaina Proudmoore)
class CS2_034:
	action = [Hit(TARGET, 1)]


# Lesser Heal (Anduin Wrynn)
class CS1h_001:
	action = [Heal(TARGET, 2)]


# INFERNO! (Lord Jaraxxus)
class EX1_tk33:
	action = [Summon(CONTROLLER, "EX1_tk34")]
