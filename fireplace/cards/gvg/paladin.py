from ..utils import *


##
# Minions

# Quartermaster
class GVG_060:
	play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "GVG_060e")

GVG_060e = buff(+2, +2)


# Cobalt Guardian
class GVG_062:
	events = Summon(CONTROLLER, MECH).on(GiveDivineShield(SELF))


# Bolvar Fordragon
class GVG_063:
	class Hand:
		events = Death(FRIENDLY + MINION).on(Buff(SELF, "GVG_063a"))

GVG_063a = buff(atk=1)


# Scarlet Purifier
class GVG_101:
	play = Hit(ALL_MINIONS + DEATHRATTLE, 2)


##
# Spells

# Seal of Light
class GVG_057:
	play = Heal(FRIENDLY_HERO, 4), Buff(FRIENDLY_HERO, "GVG_057a")

GVG_057a = buff(atk=2)


# Muster for Battle
class GVG_061:
	play = Summon(CONTROLLER, "CS2_101t") * 3, Summon(CONTROLLER, "CS2_091")


##
# Weapons

# Coghammer
class GVG_059:
	play = SetTag(RANDOM_FRIENDLY_MINION, (GameTag.TAUNT, GameTag.DIVINE_SHIELD))
