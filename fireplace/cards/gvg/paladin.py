from ..utils import *


##
# Minions

class GVG_060:
	"""Quartermaster"""
	play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "GVG_060e")


GVG_060e = buff(+2, +2)


class GVG_062:
	"""Cobalt Guardian"""
	events = Summon(CONTROLLER, MECH).on(GiveDivineShield(SELF))


class GVG_063:
	"""Bolvar Fordragon"""
	class Hand:
		events = Death(FRIENDLY + MINION).on(Buff(SELF, "GVG_063a"))


GVG_063a = buff(atk=1)


class GVG_101:
	"""Scarlet Purifier"""
	play = Hit(ALL_MINIONS + DEATHRATTLE, 2)


##
# Spells

class GVG_057:
	"""Seal of Light"""
	play = Heal(FRIENDLY_HERO, 4), Buff(FRIENDLY_HERO, "GVG_057a")


GVG_057a = buff(atk=2)


class GVG_061:
	"""Muster for Battle"""
	play = Summon(CONTROLLER, "CS2_101t") * 3, Summon(CONTROLLER, "CS2_091")


##
# Weapons

class GVG_059:
	"""Coghammer"""
	play = SetTag(RANDOM_FRIENDLY_MINION, (GameTag.TAUNT, GameTag.DIVINE_SHIELD))
