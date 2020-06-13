from ..utils import *


##
# Minions

class UNG_020:
	"""Arcanologist"""
	pass


class UNG_021:
	"""Steam Surger"""
	pass


class UNG_027:
	"""Pyros"""
	pass


class UNG_846:
	"""Shimmering Tempest"""
	pass


##
# Spells

class UNG_018:
	"""Flame Geyser"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_024:
	"""Mana Bind"""
	pass


class UNG_028:
	"""Open the Waygate"""
	pass


class UNG_941:
	"""Primordial Glyph"""
	pass


class UNG_948:
	"""Molten Reflection"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_955:
	"""Meteor"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass
