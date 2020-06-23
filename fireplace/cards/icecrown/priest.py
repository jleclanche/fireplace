from ..utils import *


##
# Minions

class ICC_210:
	"""Shadow Ascendant"""
	pass


class ICC_212:
	"""Acolyte of Agony"""
	pass


class ICC_214:
	"""Obsidian Statue"""
	pass


class ICC_215:
	"""Archbishop Benedictus"""
	pass


##
# Spells

class ICC_207:
	"""Devour Mind"""
	pass


class ICC_213:
	"""Eternal Servitude"""
	requirements = {
		PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class ICC_235:
	"""Shadow Essence"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class ICC_802:
	"""Spirit Lash"""
	pass


class ICC_849:
	"""Embrace Darkness"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


##
# Heros

class ICC_830:
	"""Shadowreaper Anduin"""
	pass
