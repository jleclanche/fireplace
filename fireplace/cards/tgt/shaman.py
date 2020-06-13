from ..utils import *


##
# Minions

class AT_046:
	"""Tuskarr Totemic"""
	play = Summon(CONTROLLER, RandomTotem())


class AT_047:
	"""Draenei Totemcarver"""
	play = Buff(SELF, "AT_047e") * Count(FRIENDLY_MINIONS + TOTEM)


AT_047e = buff(+1, +1)


class AT_049:
	"""Thunder Bluff Valiant"""
	inspire = Buff(FRIENDLY_MINIONS + TOTEM, "AT_049e")


AT_049e = buff(+1, +1)


class AT_054:
	"""The Mistcaller"""
	# The Enchantment ID is correct
	play = Buff(FRIENDLY_HAND | FRIENDLY_DECK, "AT_045e")


AT_045e = buff(+1, +1)


##
# Spells

class AT_048:
	"""Healing Wave"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = JOUST & Heal(TARGET, 14) | Heal(TARGET, 7)


class AT_051:
	"""Elemental Destruction"""
	play = Hit(ALL_MINIONS, RandomNumber(4, 5))


class AT_053:
	"""Ancestral Knowledge"""
	play = Draw(CONTROLLER) * 2


##
# Weapons

class AT_050:
	"""Charged Hammer"""
	deathrattle = Summon(CONTROLLER, "AT_050t")


class AT_050t:
	activate = Hit(TARGET, 2)
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
