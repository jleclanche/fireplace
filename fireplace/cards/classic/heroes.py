"""
Hero Power definitions
"""

from ..utils import *


# Armor Up! (Garrosh Hellscream)
class CS2_102:
	action = gainArmor(2)


# Totemic Call (Thrall)
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


# Dagger Mastery (Valeera Sanguinar)
class CS2_083b:
	def action(self):
		self.controller.summon("CS2_082")


# Reinforce (Uther Lightbringer)
class CS2_101:
	action = summonMinion("CS2_101t")


# Steady Shot (Rexxar)
class DS1h_292:
	action = damageEnemyHero(2)


# Shapeshift (Malfurion Stormrage)
class CS2_017:
	action = buffSelf("CS2_017o")


# Life Tap (Gul'dan)
class CS2_056:
	def action(self):
		self.hit(self.controller.hero, 2)
		self.controller.draw()


# Fireblast (Jaina Proudmoore)
class CS2_034:
	action = damageTarget(1)


# Lesser Heal (Anduin Wrynn)
class CS1h_001:
	action = healTarget(2)


# INFERNO! (Lord Jaraxxus)
class EX1_tk33:
	action = summonMinion("EX1_tk34")
