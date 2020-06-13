from ..utils import *


##
# Minions

class ICC_065:
	"""Bone Baron"""
	pass


class ICC_240:
	"""Runeforge Haunter"""
	pass


class ICC_809:
	"""Plague Scientist"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_FOR_COMBO: 0}
	pass


class ICC_811:
	"""Lilian Voss"""
	pass


class ICC_910:
	"""Spectral Pillager"""
	requirements = {PlayReq.REQ_TARGET_FOR_COMBO: 0}
	pass


##
# Spells

class ICC_201:
	"""Roll the Bones"""
	pass


class ICC_221:
	"""Leeching Poison"""
	requirements = {PlayReq.REQ_WEAPON_EQUIPPED: 0}
	pass


class ICC_233:
	"""Doomerang"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_WEAPON_EQUIPPED: 0}
	pass


##
# Weapons

class ICC_850:
	"""Shadowblade"""
	pass


##
# Heros

class ICC_827:
	"""Valeera the Hollow"""
	pass
