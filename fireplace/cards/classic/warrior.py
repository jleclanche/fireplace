from ..utils import *


##
# Hero Powers

class CS2_102:
	"Armor Up! (Garrosh Hellscream)"
	activate = GainArmor(FRIENDLY_HERO, 2)

class CS2_102_H1:
	"Armor Up! (Magni Bronzebeard)"
	activate = CS2_102.activate


##
# Minions

class EX1_398:
	"Arathi Weaponsmith"
	play = Summon(CONTROLLER, "EX1_398t")


class EX1_402:
	"Armorsmith"
	events = Damage(FRIENDLY_MINIONS).on(GainArmor(FRIENDLY_HERO, 1))


class EX1_414:
	"Grommash Hellscream"
	enrage = Refresh(SELF, buff="EX1_414e")

EX1_414e = buff(atk=6)


class EX1_603:
	"Cruel Taskmaster"
	play = Buff(TARGET, "EX1_603e"), Hit(TARGET, 1)

EX1_603e = buff(atk=2)

class EX1_604:
	"Frothing Berserker"
	events = Damage(ALL_MINIONS).on(Buff(SELF, "EX1_604o"))

EX1_604o = buff(atk=1)


##
# Spells

class CS2_103:
	"Charge"
	play = Buff(TARGET, "CS2_103e2")

CS2_103e2 = buff(atk=2, charge=True)


class CS2_104:
	"Rampage"
	play = Buff(TARGET, "CS2_104e")

CS2_104e = buff(+3, +3)


class CS2_105:
	"Heroic Strike"
	play = Buff(FRIENDLY_HERO, "CS2_105e")

CS2_105e = buff(atk=4)

class CS2_108:
	"Execute"
	play = Destroy(TARGET)


class CS2_114:
	"Cleave"
	play = Hit(RANDOM_ENEMY_MINION * 2, 2)


class EX1_391:
	"Slam"
	play = Hit(TARGET, 2), Dead(TARGET) | Draw(CONTROLLER)


class EX1_392:
	"Battle Rage"
	play = Draw(CONTROLLER) * Count(FRIENDLY_CHARACTERS + DAMAGED)


class EX1_400:
	"Whirlwind"
	play = Hit(ALL_MINIONS, 1)


class EX1_407:
	"Brawl"
	play = (
		Find(ALL_MINIONS + ALWAYS_WINS_BRAWLS) &
		Destroy(ALL_MINIONS - RANDOM(ALL_MINIONS + ALWAYS_WINS_BRAWLS)) |
		Destroy(ALL_MINIONS - RANDOM_MINION)
	)


class EX1_408:
	"Mortal Strike"
	powered_up = CURRENT_HEALTH(FRIENDLY_HERO) <= 12
	play = powered_up & Hit(TARGET, 6) | Hit(TARGET, 4)


class EX1_409:
	"Upgrade!"
	play = (
		Find(FRIENDLY_WEAPON) &
		Buff(FRIENDLY_WEAPON, "EX1_409e") |
		Summon(CONTROLLER, "EX1_409t")
	)

EX1_409e = buff(+1, +1)


class EX1_410:
	"Shield Slam"
	play = Hit(TARGET, ARMOR(FRIENDLY_HERO))


class EX1_606:
	"Shield Block"
	play = GainArmor(FRIENDLY_HERO, 5), Draw(CONTROLLER)


class EX1_607:
	"Inner Rage"
	play = Buff(TARGET, "EX1_607e"), Hit(TARGET, 1)

EX1_607e = buff(atk=2)


class NEW1_036:
	"Commanding Shout"
	play = Buff(FRIENDLY_MINIONS, "NEW1_036e"), Buff(CONTROLLER, "NEW1_036e2")

class NEW1_036e2:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "NEW1_036e"))

NEW1_036e = buff(health_minimum=1)


class EX1_084:
	"Warsong Commander"
	update = Refresh(FRIENDLY_MINIONS + CHARGE, buff="EX1_084e")

EX1_084e = buff(atk=1)


##
# Weapons

class EX1_411:
	"Gorehowl"
	update = Attacking(FRIENDLY_HERO, MINION) & Refresh(SELF, buff="EX1_411e")
	events = Attack(FRIENDLY_HERO, MINION).after(Buff(SELF, "EX1_411e2"))

EX1_411e = buff(immune=True)
EX1_411e2 = buff(atk=-1)
