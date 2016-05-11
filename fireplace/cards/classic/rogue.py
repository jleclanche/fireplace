from ..utils import *


##
# Rogue

class CS2_083b:
	"Dagger Mastery"
	activate = Find(FRIENDLY_WEAPON + ID("AT_034")) | Summon(CONTROLLER, "CS2_082")

# Sharpened (Unused)
CS2_083e = buff(atk=1)


##
# Minions

class EX1_131:
	"Defias Ringleader"
	combo = Summon(CONTROLLER, "EX1_131t")


class EX1_134:
	"SI:7 Agent"
	combo = Hit(TARGET, 2)


class EX1_613:
	"Edwin VanCleef"
	combo = Buff(SELF, "EX1_613e") * Attr(CONTROLLER, GameTag.NUM_CARDS_PLAYED_THIS_TURN)

EX1_613e = buff(+2, +2)


class NEW1_005:
	"Kidnapper"
	combo = Bounce(TARGET)


class NEW1_014:
	"Master of Disguise"
	play = Buff(TARGET - STEALTH, "NEW1_014e")

class NEW1_014e:
	"Disguised"
	tags = {GameTag.STEALTH: True}
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


##
# Spells

class CS2_072:
	"Backstab"
	play = Hit(TARGET, 2)


class CS2_073:
	"Cold Blood"
	play = Buff(TARGET, "CS2_073e")
	combo = Buff(TARGET, "CS2_073e2")

CS2_073e = buff(atk=2)
CS2_073e2 = buff(atk=4)


class CS2_074:
	"Deadly Poison"
	play = Buff(FRIENDLY_WEAPON, "CS2_074e")

CS2_074e = buff(atk=2)


class CS2_075:
	"Sinister Strike"
	play = Hit(ENEMY_HERO, 3)


class CS2_076:
	"Assassinate"
	play = Destroy(TARGET)


class CS2_077:
	"Sprint"
	play = Draw(CONTROLLER) * 4


class CS2_233:
	"Blade Flurry"
	play = Hit(ENEMY_MINIONS, ATK(FRIENDLY_WEAPON)), Destroy(FRIENDLY_WEAPON)


class EX1_124:
	"Eviscerate"
	play = Hit(TARGET, 2)
	combo = Hit(TARGET, 4)


class EX1_126:
	"Betrayal"
	play = Hit(SELF_ADJACENT, ATK(SELF), source=TARGET)


class EX1_128:
	"Conceal"
	play = (
		Buff(FRIENDLY_MINIONS - STEALTH, "EX1_128e"),
		Stealth(FRIENDLY_MINIONS),
	)

class EX1_128e:
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class EX1_129:
	"Fan of Knives"
	play = Hit(ENEMY_MINIONS, 1), Draw(CONTROLLER)


class EX1_137:
	"Headcrack"
	play = Hit(ENEMY_HERO, 2)
	combo = (play, TURN_END.on(Give(CONTROLLER, "EX1_137")))


class EX1_144:
	"Shadowstep"
	play = Bounce(TARGET), Buff(TARGET, "EX1_144e")

@custom_card
class EX1_144e:
	tags = {
		GameTag.CARDNAME: "Shadowstep Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -2,
	}
	events = REMOVED_IN_PLAY


class EX1_145:
	"Preparation"
	play = Buff(CONTROLLER, "EX1_145o")

class EX1_145o:
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
	events = OWN_SPELL_PLAY.on(Destroy(SELF))


class EX1_278:
	"Shiv"
	play = Hit(TARGET, 1), Draw(CONTROLLER)


class EX1_581:
	"Sap"
	play = Bounce(TARGET)


class NEW1_004:
	"Vanish"
	play = Bounce(ALL_MINIONS)


##
# Weapons

class EX1_133:
	"Perdition's Blade"
	play = Hit(TARGET, 1)
	combo = Hit(TARGET, 2)
