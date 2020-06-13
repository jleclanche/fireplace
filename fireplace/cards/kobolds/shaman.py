from ..utils import *


##
# Minions

class LOOT_062:
	"""Kobold Hermit"""
	pass


class LOOT_358:
	"""Grumble, Worldshaker"""
	pass


class LOOT_517:
	"""Murmuring Elemental"""
	pass


class LOOT_518:
	"""Windshear Stormcaller"""
	pass


##
# Spells

class LOOT_060:
	"""Crushing Hand"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class LOOT_064:
	"""Lesser Sapphire Spellstone"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class LOOT_344:
	"""Primal Talismans"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	pass


class LOOT_373:
	"""Healing Rain"""
	pass


class LOOT_504:
	"""Unstable Evolution"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


##
# Weapons

class LOOT_506:
	"""The Runespear"""
	pass
