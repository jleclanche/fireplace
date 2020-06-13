from ..utils import *


##
# Minions

class UNG_022:
	"""Mirage Caller"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


class UNG_032:
	"""Crystalline Oracle"""
	pass


class UNG_034:
	"""Radiant Elemental"""
	pass


class UNG_035:
	"""Curious Glimmerroot"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	pass


class UNG_037:
	"""Tortollan Shellraiser"""
	pass


class UNG_963:
	"""Lyra the Sunshard"""
	pass


##
# Spells

class UNG_029:
	"""Shadow Visions"""
	pass


class UNG_030:
	"""Binding Heal"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_854:
	"""Free From Amber"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class UNG_940:
	"""Awaken the Makers"""
	pass
