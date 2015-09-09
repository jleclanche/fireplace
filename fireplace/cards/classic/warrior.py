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
	enrage = Refresh(SELF, {GameTag.ATK: +6})


# Cruel Taskmaster
class EX1_603:
	play = Buff(TARGET, "EX1_603e"), Hit(TARGET, 1)


# Frothing Berserker
class EX1_604:
	events = Damage(ALL_MINIONS).on(Buff(SELF, "EX1_604o"))


##
# Spells

# Charge
class CS2_103:
	play = Buff(TARGET, "CS2_103e2")


# Rampage
class CS2_104:
	play = Buff(TARGET, "CS2_104e")


# Heroic Strike
class CS2_105:
	play = Buff(FRIENDLY_HERO, "CS2_105e")


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
	play = Draw(CONTROLLER) * Count(FRIENDLY_MINIONS + DAMAGED)


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
	play = (Attr(FRIENDLY_HERO, "health") <= 12) & Hit(TARGET, 6) | Hit(TARGET, 4)


# Upgrade!
class EX1_409:
	play = (
		Find(FRIENDLY_WEAPON) &
		Buff(FRIENDLY_WEAPON, "EX1_409e") |
		Summon(CONTROLLER, "EX1_409t")
	)


# Shield Slam
class EX1_410:
	play = Hit(TARGET, Attr(FRIENDLY_HERO, GameTag.ARMOR))


# Shield Block
class EX1_606:
	play = GainArmor(FRIENDLY_HERO, 5), Draw(CONTROLLER)


# Inner Rage
class EX1_607:
	play = Buff(TARGET, "EX1_607e"), Hit(TARGET, 1)


# Commanding Shout
class NEW1_036:
	play = Buff(FRIENDLY_MINIONS, "NEW1_036e"), Buff(FRIENDLY_HERO, "NEW1_036e2")

class NEW1_036e2:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.Args.CARDS, "NEW1_036e"))


# Warsong Commander
class EX1_084:
	events = Summon(CONTROLLER, MINION + (ATK <= 3)).after(Buff(Summon.Args.CARDS, "EX1_084e"))
