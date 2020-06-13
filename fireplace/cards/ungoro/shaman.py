from ..utils import *


##
# Minions

class UNG_019:
	"""Air Elemental"""
	pass


class UNG_201:
	"""Primalfin Totem"""
	pass


class UNG_202:
	"""Fire Plume Harbinger"""
	pass


class UNG_208:
	"""Stone Sentinel"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class UNG_211:
	"""Kalimos, Primal Lord"""
	pass


class UNG_938:
	"""Hot Spring Guardian"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


##
# Spells

class UNG_025:
	"""Volcano"""
	pass


class UNG_817:
	"""Tidal Surge"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_942:
	"""Unite the Murlocs"""
	pass


class UNG_956:
	"""Spirit Echo"""
	pass
