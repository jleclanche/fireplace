from ..utils import *


##
# Minions

class OG_023:
	"""Primal Fusion"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "OG_023t") * Count(FRIENDLY_MINIONS + TOTEM)


OG_023t = buff(+1, +1)


class OG_026:
	"""Eternal Sentinel"""
	play = UnlockOverload(CONTROLLER)


class OG_209:
	"""Hallazeal the Ascended"""
	events = Damage(source=SPELL + FRIENDLY).on(Heal(FRIENDLY_HERO, Damage.AMOUNT))


class OG_328:
	"""Master of Evolution"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Evolve(TARGET, 1)


##
# Spells

class OG_027:
	"""Evolve"""
	play = Evolve(FRIENDLY_MINIONS, 1)


class OG_206:
	"""Stormcrack"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 4)


##
# Weapons

class OG_031:
	"""Hammer of Twilight"""
	deathrattle = Summon(CONTROLLER, "OG_031a")
