from ..utils import *


##
# Rogue

# Dagger Mastery
class CS2_083b:
	activate = Find(FRIENDLY_WEAPON + ID("AT_034")) | Summon(CONTROLLER, "CS2_082")

# Sharpened (Unused)
CS2_083e = buff(atk=1)


##
# Minions

# Defias Ringleader
class EX1_131:
	combo = Summon(CONTROLLER, "EX1_131t")


# SI:7 Agent
class EX1_134:
	combo = Hit(TARGET, 2)


# Edwin VanCleef
class EX1_613:
	combo = Buff(SELF, "EX1_613e") * Attr(CONTROLLER, GameTag.NUM_CARDS_PLAYED_THIS_TURN)

EX1_613e = buff(+2, +2)


# Kidnapper
class NEW1_005:
	combo = Bounce(TARGET)


# Master of Disguise
class NEW1_014:
	play = Buff(TARGET - STEALTH, "NEW1_014e")

# Disguised
class NEW1_014e:
	tags = {GameTag.STEALTH: True}
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


##
# Spells

# Backstab
class CS2_072:
	play = Hit(TARGET, 2)


# Cold Blood
class CS2_073:
	play = Buff(TARGET, "CS2_073e")
	combo = Buff(TARGET, "CS2_073e2")

CS2_073e = buff(atk=2)
CS2_073e2 = buff(atk=4)


# Deadly Poison
class CS2_074:
	play = Buff(FRIENDLY_WEAPON, "CS2_074e")

CS2_074e = buff(atk=2)


# Sinister Strike
class CS2_075:
	play = Hit(ENEMY_HERO, 3)


# Assassinate
class CS2_076:
	play = Destroy(TARGET)


# Sprint
class CS2_077:
	play = Draw(CONTROLLER) * 4


# Blade Flurry
class CS2_233:
	play = Hit(ENEMY_MINIONS, ATK(FRIENDLY_WEAPON)), Destroy(FRIENDLY_WEAPON)


# Eviscerate
class EX1_124:
	play = Hit(TARGET, 2)
	combo = Hit(TARGET, 4)


# Betrayal
class EX1_126:
	play = Hit(SELF_ADJACENT, ATK(SELF), source=TARGET)


# Conceal
class EX1_128:
	play = (
		Buff(FRIENDLY_MINIONS - STEALTH, "EX1_128e"),
		Stealth(FRIENDLY_MINIONS),
	)

class EX1_128e:
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


# Fan of Knives
class EX1_129:
	play = Hit(ENEMY_MINIONS, 1), Draw(CONTROLLER)


# Headcrack
class EX1_137:
	play = Hit(ENEMY_HERO, 2)
	combo = (play, TURN_END.on(Give(CONTROLLER, "EX1_137")))


# Shadowstep
class EX1_144:
	play = Bounce(TARGET), Buff(TARGET, "EX1_144e")

@custom_card
class EX1_144e:
	tags = {
		GameTag.CARDNAME: "Shadowstep Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -2,
	}
	events = REMOVED_IN_PLAY


# Preparation
class EX1_145:
	play = Buff(FRIENDLY_HERO, "EX1_145o")

class EX1_145o:
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
	events = OWN_SPELL_PLAY.on(Destroy(SELF))


# Shiv
class EX1_278:
	play = Hit(TARGET, 1), Draw(CONTROLLER)


# Sap
class EX1_581:
	play = Bounce(TARGET)


# Vanish
class NEW1_004:
	play = Bounce(ALL_MINIONS)


##
# Weapons

# Perdition's Blace
class EX1_133:
	play = Hit(TARGET, 1)
	combo = Hit(TARGET, 2)
