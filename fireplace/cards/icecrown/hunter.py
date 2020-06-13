from ..utils import *


##
# Minions

class ICC_021:
	"""Exploding Bloatbat"""
	pass


class ICC_204:
	"""Professor Putricide"""
	pass


class ICC_243:
	"""Corpse Widow"""
	pass


class ICC_415:
	"""Stitched Tracker"""
	pass


class ICC_419:
	"""Bearshark"""
	pass


class ICC_825:
	"""Abominable Bowman"""
	pass


##
# Spells

class ICC_049:
	"""Toxic Arrow"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class ICC_052:
	"""Play Dead"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class ICC_200:
	"""Venomstrike Trap"""
	pass


##
# Heros

class ICC_828:
	"""Deathstalker Rexxar"""
	pass
