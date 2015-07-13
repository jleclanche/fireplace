from ..utils import *


##
# Hero Powers

# Armor Up! (Garrosh Hellscream)
class CS2_102:
	activate = [GainArmor(FRIENDLY_HERO, 2)]

# Armor Up! (Magni Bronzebeard)
class CS2_102_H1:
	activate = CS2_102.activate


##
# Minions

# Armorsmith
class EX1_402:
	events = [
		Damage(FRIENDLY_MINIONS).on(GainArmor(FRIENDLY_HERO, 1))
	]


# Cruel Taskmaster
class EX1_603:
	action = [Buff(TARGET, "EX1_603e"), Hit(TARGET, 1)]


# Frothing Berserker
class EX1_604:
	events = [
		Damage(ALL_MINIONS).on(Buff(SELF, "EX1_604o"))
	]


##
# Spells

# Charge
class CS2_103:
	action = [Buff(TARGET, "CS2_103e2")]


# Rampage
class CS2_104:
	action = [Buff(TARGET, "CS2_104e")]


# Heroic Strike
class CS2_105:
	action = [Buff(FRIENDLY_HERO, "CS2_105e")]


# Execute
class CS2_108:
	action = [Destroy(TARGET)]


# Cleave
class CS2_114:
	action = [Hit(RANDOM_ENEMY_MINION * 2, 2)]


# Slam
class EX1_391:
	action = [Hit(TARGET, 2), Dead(TARGET) | Draw(CONTROLLER)]


# Battle Rage
class EX1_392:
	def action(self):
		damaged = self.controller.characters.filter(damaged=True)
		return [Draw(CONTROLLER) * len(damaged)]


# Whirlwind
class EX1_400:
	action = [Hit(ALL_MINIONS, 1)]


# Brawl
class EX1_407:
	action = [Destroy(ALL_MINIONS - RANDOM_MINION)]


# Mortal Strike
class EX1_408:
	def action(self, target):
		if self.controller.hero.health <= 12:
			return [Hit(TARGET, 6)]
		else:
			return [Hit(TARGET, 4)]


# Upgrade!
class EX1_409:
	def action(self):
		if self.controller.weapon:
			return [Buff(FRIENDLY_WEAPON, "EX1_409e")]
		else:
			return [Summon(CONTROLLER, "EX1_409t")]


# Shield Slam
class EX1_410:
	def action(self, target):
		return [Hit(TARGET, self.controller.hero.armor)]


# Shield Block
class EX1_606:
	action = [GainArmor(FRIENDLY_HERO, 5), Draw(CONTROLLER)]


# Inner Rage
class EX1_607:
	action = [Buff(TARGET, "EX1_607e"), Hit(TARGET, 1)]


# Commanding Shout
class NEW1_036:
	action = [Buff(FRIENDLY_MINIONS, "NEW1_036e")]
