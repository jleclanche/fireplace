from ..utils import *


##
# Minions

class ICC_075:
	"""Despicable Dreadlord"""
	pass


class ICC_218:
	"""Howlfiend"""
	pass


class ICC_407:
	"""Gnomeferatu"""
	pass


class ICC_841:
	"""Blood-Queen Lana'thel"""
	pass


class ICC_903:
	"""Sanguine Reveler"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


##
# Spells

class ICC_041:
	"""Defile"""
	pass


class ICC_055:
	"""Drain Soul"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class ICC_206:
	"""Treachery"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class ICC_469:
	"""Unwilling Sacrifice"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


##
# Heros

class ICC_831:
	"""Bloodreaver Gul'dan"""
	pass
