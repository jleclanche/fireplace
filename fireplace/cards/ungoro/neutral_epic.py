from ..utils import *


##
# Minions

class UNG_085:
	"""Emerald Hive Queen"""
	pass


class UNG_087:
	"""Bittertide Hydra"""
	pass


class UNG_088:
	"""Tortollan Primalist"""
	pass


class UNG_089:
	"""Gentle Megasaur"""
	pass


class UNG_099:
	"""Charged Devilsaur"""
	pass


class UNG_113:
	"""Bright-Eyed Scout"""
	pass


class UNG_847:
	"""Blazecaller"""
	requirements = {
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABE_AND_ELEMENTAL_PLAYED_LAST_TURN: 0}
	pass


class UNG_848:
	"""Primordial Drake"""
	pass


class UNG_946:
	"""Gluttonous Ooze"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass
