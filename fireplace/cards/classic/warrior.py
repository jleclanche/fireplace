from ..utils import *


##
# Hero Powers

# Armor Up! (Garrosh Hellscream)
class CS2_102:
	activate = GainArmor(FRIENDLY_HERO, 2)

# Armor Up! (Magni Bronzebeard)
class CS2_102_H1:
	activate = CS2_102.activate


##
# Minions

# Armorsmith
class EX1_402:
	events = Damage(FRIENDLY_MINIONS).on(GainArmor(FRIENDLY_HERO, 1))


# Grommash Hellscream
class EX1_414:
	enrage = Refresh(SELF, buff="EX1_414e")

EX1_414e = buff(atk=6)


# Cruel Taskmaster
class EX1_603:
	play = Buff(TARGET, "EX1_603e"), Hit(TARGET, 1)

EX1_603e = buff(atk=2)

# Frothing Berserker
class EX1_604:
	events = Damage(ALL_MINIONS).on(Buff(SELF, "EX1_604o"))

EX1_604o = buff(atk=1)


##
# Spells

# Charge
class CS2_103:
	play = Buff(TARGET, "CS2_103e2")

CS2_103e2 = buff(atk=2, charge=True)


# Rampage
class CS2_104:
	play = Buff(TARGET, "CS2_104e")

CS2_104e = buff(+3, +3)


# Heroic Strike
class CS2_105:
	play = Buff(FRIENDLY_HERO, "CS2_105e")

CS2_105e = buff(atk=4)

# Execute
class CS2_108:
	play = Destroy(TARGET)


# Cleave
class CS2_114:
	play = Hit(RANDOM_ENEMY_MINION * 2, 2)


# Slam
class EX1_391:
	play = Hit(TARGET, 2), Dead(TARGET) | Draw(CONTROLLER)


# Battle Rage
class EX1_392:
	play = Draw(CONTROLLER) * Count(FRIENDLY_CHARACTERS + DAMAGED)


# Whirlwind
class EX1_400:
	play = Hit(ALL_MINIONS, 1)


# Brawl
class EX1_407:
	play = (
		Find(ALL_MINIONS + ALWAYS_WINS_BRAWLS) &
		Destroy(ALL_MINIONS - RANDOM(ALL_MINIONS + ALWAYS_WINS_BRAWLS)) |
		Destroy(ALL_MINIONS - RANDOM_MINION)
	)


# Mortal Strike
class EX1_408:
	powered_up = CURRENT_HEALTH(FRIENDLY_HERO) <= 12
	play = powered_up & Hit(TARGET, 6) | Hit(TARGET, 4)


# Upgrade!
class EX1_409:
	play = (
		Find(FRIENDLY_WEAPON) &
		Buff(FRIENDLY_WEAPON, "EX1_409e") |
		Summon(CONTROLLER, "EX1_409t")
	)

EX1_409e = buff(+1, +1)


# Shield Slam
class EX1_410:
	play = Hit(TARGET, ARMOR(FRIENDLY_HERO))


# Shield Block
class EX1_606:
	play = GainArmor(FRIENDLY_HERO, 5), Draw(CONTROLLER)


# Inner Rage
class EX1_607:
	play = Buff(TARGET, "EX1_607e"), Hit(TARGET, 1)

EX1_607e = buff(atk=2)


# Commanding Shout
class NEW1_036:
	play = Buff(FRIENDLY_MINIONS, "NEW1_036e"), Buff(FRIENDLY_HERO, "NEW1_036e2")

class NEW1_036e2:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "NEW1_036e"))

NEW1_036e = buff(health_minimum=1)


# Warsong Commander
class EX1_084:
	update = Refresh(FRIENDLY_MINIONS + CHARGE, buff="EX1_084e")

EX1_084e = buff(atk=1)


##
# Weapons

# Gorehowl
class EX1_411:
	update = Attacking(FRIENDLY_HERO, MINION) & Refresh(SELF, buff="EX1_411e")
	events = Attack(FRIENDLY_HERO, MINION).after(Buff(SELF, "EX1_411e2"))

EX1_411e = buff(immune=True)
EX1_411e2 = buff(atk=-1)
