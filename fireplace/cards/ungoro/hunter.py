from ..utils import *


##
# Minions

class UNG_800:
	"""Terrorscale Stalker"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class UNG_912:
	"""Jeweled Macaw"""
	pass


class UNG_913:
	"""Tol'vir Warden"""
	pass


class UNG_914:
	"""Raptor Hatchling"""
	pass


class UNG_915:
	"""Crackling Razormaw"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20}
	pass


class UNG_919:
	"""Swamp King Dred"""
	pass


##
# Spells

class UNG_910:
	"""Grievous Bite"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_916:
	"""Stampede"""
	pass


class UNG_917:
	"""Dinomancy"""
	pass


class UNG_920:
	"""The Marsh Queen"""
	pass
